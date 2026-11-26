"""数据库参数探测模块。

api 生成阶段按 URL→表 映射连接数据库，把接口参数名（驼峰转蛇形后与表列名
比对）匹配到表字段，取一条示例记录的值组装为 ``db_params`` 写入 api.json，
供 complex_scenario 等消费端作为参数示例值（摆脱对 HAR 录制值的依赖）。

表来源优先级：
1. ``DB_CONFIG.api_table_map`` 显式映射（最权威，可带 where 过滤）；
2. 自动反查 information_schema：先按接口语义（URL 词元 + 描述中文）推断
   业务域，在 ``DB_CONFIG.domain_schemas`` 配置的域库内优先查找（多域取库
   并集，无结果再回退全库；三类元数据反查均排除 MySQL 系统库）；候选集 =
   参数列反查 ∪ URL 词元表名匹配，按
   “非通用命中列数 + 表名与 URL 关键词相似度 + 参数列唯一索引加分
   - 表名多余词段惩罚 - 备份表惩罚”打分，唯一最高分胜出（同分时
   preferred_tables 人工先验消歧）；
3. 主表匹配不到的参数逐个独立找表（跨表接口如 demoNo 在会员主表、demoCode
   在产品主表各自查各自的表），域推断以参数自身语义（备注中文 + 参数名
   词元）优先；
4. 仍未命中 → 跳过探测（日志提示手动配 api_table_map），不阻断生成。

字段匹配支持复数参数去尾 s（ids → id 列），常规形态未命中时按“列名包含
参数名”的子串兜底（如 messagecontent 包含 content）。接口描述/URL 含
“新增/添加”字样的接口，探测值生成与库中已有值不冲突的值（数值 MAX+1、
字符串加随机后缀）；
含“编辑/修改”字样的接口，唯一索引列同样生成不冲突值，主键列取已有值。
数组形声明的参数（如 ids: []）自动包装为单元素列表；有枚举声明的参数
（param_values 含枚举列表）直接取首个枚举值，不查库。

探测失败（未配置、驱动缺失、连不上库、表或字段不存在）一律跳过并记录日志；
``password_env`` 填环境变量名时密码从环境变量读取（不落盘），直接填密码明文
亦可（环境变量查不到即当作密码）。
"""

from __future__ import annotations

import fnmatch
import os
import re
import secrets
import threading
import time
from typing import Any

from .config import APIConfig
from .logger import logger
from .url_matcher import URLMatcher

# 探测失败原因只警告一次（避免批量生成时刷屏）
_warned_reasons: set[str] = set()

# 数据库驱动的真实模块名（探测时延迟 import，未安装则跳过）
_DRIVER_NAME = "pymysql"

# 自动找表：URL 分词后的通用词元（不参与表名相似度判定）。
# 含 URL 惯例段（mgmt/esb）与通用动词（query/detail/save），
# 这些词元几乎出现在每个接口路径中，对表名区分度为零。
_URL_STOP_WORDS = {
    "add",
    "admin",
    "api",
    "app",
    "batch",
    "by",
    "check",
    "count",
    "create",
    "data",
    "delete",
    "detail",
    "details",
    "do",
    "download",
    "edit",
    "esb",
    "export",
    "find",
    "for",
    "get",
    "import",
    "info",
    "list",
    # log/logs 是动作留痕而非业务实体：saveDownloadLog 的业务实体是
    # cms_material，保留 log 词元会让两张 *_log 子表凭表名精确命中
    # 压过主表（实测 42/37 分并列而放弃探测）
    "log",
    "logs",
    "mgmt",
    "modify",
    "of",
    "page",
    "query",
    "record",
    "records",
    "save",
    "search",
    "test",
    "the",
    "update",
    "upload",
    "v1",
    "v2",
    "v3",
    "web",
    "with",
}

# 自动找表：通用列不参与命中统计。
# id/type/status 等列几乎每张业务表都有，只命中它们不代表找对了表
# （否则 saveReturnVisit 这类接口会凭 id 命中数百张表）。
_GENERIC_COLUMNS = {
    "create_time",
    "created_at",
    "id",
    "is_deleted",
    "status",
    "type",
    "update_time",
    "updated_at",
}

# 自动找表：表名中的备份/临时词段（bak/copy/tmp 或纯数字段如 20261027）。
# 备份表与主表列结构相同且常带唯一索引，需降权避免与主表并列。
_BACKUP_SEGMENTS = {"bak", "copy", "del", "tmp"}

# 自动找表：参数列为唯一索引的表加分值（查询参数如 demoNo 常对应主表唯一键）。
_UNIQUE_INDEX_BONUS = 8

# 自动找表：表名含备份词段或纯数字段的惩罚分。
_BACKUP_PENALTY = 6

# 自动找表：表名中未被任何 URL 词元覆盖的词段，每段扣分（主表优先）。
# 子表/关联表往往在主表名上追加业务限定词（如 prmt_monthly_promotion
# 对比 prmt_combine_promotion），不扣分时它们凭多命中一个通用列就能
# 压过语义正确的主表；取 8 而非 3 是为了大于表名包含关系的 3 分差。
_EXTRA_SEGMENT_PENALTY = 8

# 自动找表：排除 MySQL 系统库的 SQL 条件，三个元数据反查（COLUMNS/STATISTICS/
# TABLES）共用，避免只在一处排除造成不一致——系统表同样含 id/name 等列，
# 会凭通用列混进候选（实测 information_schema.INNODB_FT_CONFIG 被 8 个接口选为主表）。
_SYSTEM_SCHEMA_FILTER = "TABLE_SCHEMA NOT IN ('information_schema','mysql','performance_schema','sys')"

# 自动找表：进程内候选缓存（列名集合 + 库范围 + 是否含通用列 → 候选表），
# 批量生成时按相同参数列集合的接口只需反查一次元数据库。
_candidate_cache: dict[tuple[frozenset[str], tuple[str, ...], bool], dict[str, int]] = {}

# 自动找表：进程内唯一索引表缓存（列名集合 → 表集合）。
_unique_cache: dict[tuple[frozenset[str], tuple[str, ...]], set[str]] = {}

# 自动找表：进程内表名匹配缓存（URL 词元集合 + 库范围 → 候选表），与
# _candidate_cache 同范式：参数级独立找表对每个参数都用同一接口关键词调用
# _tables_by_name，缓存避免重复的 information_schema.TABLES 全表扫描。
_name_cache: dict[tuple[frozenset[str], tuple[str, ...]], dict[str, int]] = {}

# 连接失败熔断：最近一次连接失败的时刻（monotonic）。TTL 内后续 _connect 直接
# 返回 None，避免库不可达时批量生成的每个接口都吃满 connect_timeout（累计数小时）。
_connect_failed_at: float | None = None
_CONNECT_RETRY_TTL = 60.0

# 批量性能：schema 快照（全非系统库的 TABLES/COLUMNS/唯一索引 STATISTICS 一次性
# 拉取，实测 3 万列约 0.7s），此后三个元数据反查全部内存计算，不再逐接口发
# information_schema 查询（每次 0.2~0.3s，是批量生成的主要开销）。快照为全库
# 超集，域收窄与 DB_CONFIG.databases 限定在计算时过滤；批量期间 schema 变更忽略。
_schema_snapshot: dict[str, Any] | None = None
_snapshot_lock = threading.Lock()

# 批量性能：线程局部连接复用（probe 跑在 asyncio.to_thread 工作线程，每线程
# 一条连接跨接口复用，避免每接口都吃一次 TCP+认证握手，实测约 0.28s/次）。
_conn_local = threading.local()
_cached_conns: list[Any] = []
_conn_lock = threading.Lock()

# 批量性能：表结构（DESCRIBE）缓存，同表跨接口共享（结构批量期间视为静态）。
_structure_cache: dict[str, tuple[list[str], list[str], list[str], dict[str, str]]] = {}


def _warn_once(reason: str, message: str) -> None:
    """同一类探测失败原因只警告一次。"""
    if reason in _warned_reasons:
        return
    _warned_reasons.add(reason)
    logger.warning(message)


def _snake_case(name: str) -> str:
    """把驼峰参数名转为蛇形（demoVisitOperator → demo_visit_operator）。"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _table_segments(table_name: str) -> list[str]:
    """表名部分（去 schema 前缀）按 _ 切分的词段。"""
    return table_name.split(".", 1)[-1].split("_")


def _seg_matches(seg: str, kw: str) -> bool:
    """词段与关键词是否匹配（精确相等或互相包含）。"""
    return seg == kw or kw in seg or seg in kw


def _global_databases() -> list[str]:
    """DB_CONFIG.databases 全局库范围（缺省空列表 = 不限定）。"""
    return (APIConfig.DB_CONFIG() or {}).get("databases") or []


def _quote_table(table: str) -> str:
    """库.表 → 反引号引用形式（`库`.`表`），转义内嵌反引号，统一 SQL 标识符引用。"""
    return ".".join(f"`{p.replace('`', '``')}`" for p in table.split(".", 1))


def _map_matches(pattern: str, api_url: str) -> bool:
    """判断 api_table_map 的键是否命中接口 URL（精确 / 通配 / 路径模板）。"""
    norm_pattern = URLMatcher.normalize_url(pattern)
    norm_url = URLMatcher.normalize_url(api_url)
    if norm_url == norm_pattern:
        return True
    if "*" in norm_pattern and fnmatch.fnmatchcase(norm_url, norm_pattern):
        return True
    matched, _ = URLMatcher.match_url_pattern(norm_url, norm_pattern)
    if matched:
        return True
    matched, _ = URLMatcher.match_url_pattern(norm_pattern, norm_url)
    return matched


def _find_table_mapping(api_url: str) -> tuple[str, str] | None:
    """按 api_table_map 匹配接口 URL，返回 (table, where 过滤条件)。"""
    db_config = APIConfig.DB_CONFIG()
    if not db_config:
        return None
    mapping = db_config.get("api_table_map") or {}
    if not isinstance(mapping, dict):
        return None
    for pattern, entry in mapping.items():
        if not _map_matches(str(pattern), api_url):
            continue
        if isinstance(entry, str):
            return entry, ""
        if isinstance(entry, dict) and entry.get("table"):
            return str(entry["table"]), str(entry.get("where") or "")
        return None
    return None


def _word_terms(text: str) -> list[str]:
    """按驼峰/下划线/非字母数字切词（小写、去重保序，不过滤停用词）。"""
    terms: list[str] = []
    for word in re.split(r"[^a-z0-9]+", _snake_case(text)):
        if word and word not in terms:
            terms.append(word)
    return terms


def _url_keywords(api_url: str) -> list[str]:
    """从接口 URL 提取业务关键词词元（驼峰分词、去通用词元、去重保序）。"""
    return [word for word in _url_word_terms(api_url) if word not in _URL_STOP_WORDS]


def _score_table_name(table_name: str, keywords: list[str]) -> int:
    """表名与 URL 关键词的相似度打分（词段精确匹配 5 分、互相包含 3 分）。

    只对表名部分打分：schema 名常含业务词元（如 demo_center_member），
    对全名分词会把 schema 词段算进所有同库表，产生无区分度的并列分。
    按 (关键词,词段) 对累加：表名重复词段（如 product_product）对同一关键词
    多次命中会累加，这是「表名与该词相关性更强」的弱信号，有意保留：改成
    每关键词取最高档会削弱主表识别（实测 getPromotionProductInfo 的主表
    product_product 会被只有普通引用列的 demo_promotion 反超）。与 _match_keyword_count
    的「每关键词计一次覆盖」口径不同是故意的：后者是布尔准入阈值，前者是分级排序。
    """
    segments = _table_segments(table_name)
    score = 0
    for kw in keywords:
        for seg in segments:
            if seg == kw:
                score += 5
            elif kw in seg or seg in kw:
                score += 3
    return score


def _get_schema_snapshot(conn: Any) -> dict[str, Any] | None:
    """懒构建全库 schema 快照（进程内一次），失败返回 None（降级为跳过自动找表）。

    三个反查函数（_candidate_tables/_tables_by_name/_unique_index_tables）共用，
    数据形态：tables {库: {表}}、columns {库: {表: {小写列名}}}、
    unique {库: {表: {小写唯一索引列名}}}。构建失败只告警一次，与原先
    逐查询失败的降级行为一致。
    """
    global _schema_snapshot
    if _schema_snapshot is not None:
        return _schema_snapshot
    with _snapshot_lock:
        if _schema_snapshot is not None:
            return _schema_snapshot
        tables: dict[str, set[str]] = {}
        columns: dict[str, dict[str, set[str]]] = {}
        unique: dict[str, dict[str, set[str]]] = {}
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES WHERE {_SYSTEM_SCHEMA_FILTER}"
                )
                for schema, table in cur.fetchall():
                    tables.setdefault(str(schema), set()).add(str(table))
                cur.execute(
                    "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME "
                    f"FROM information_schema.COLUMNS WHERE {_SYSTEM_SCHEMA_FILTER}"
                )
                for schema, table, column in cur.fetchall():
                    columns.setdefault(str(schema), {}).setdefault(str(table), set()).add(str(column).lower())
                cur.execute(
                    "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME "
                    f"FROM information_schema.STATISTICS WHERE NON_UNIQUE = 0 AND {_SYSTEM_SCHEMA_FILTER}"
                )
                for schema, table, column in cur.fetchall():
                    unique.setdefault(str(schema), {}).setdefault(str(table), set()).add(str(column).lower())
        except Exception as e:
            _warn_once("snapshot_fail", f"构建 schema 快照失败，跳过自动找表: {e}")
            return None
        _schema_snapshot = {"tables": tables, "columns": columns, "unique": unique}
        return _schema_snapshot


def _snapshot_schemas(snapshot: dict[str, Any], databases: list[str] | None) -> list[str]:
    """参与计算的库范围：databases 非空取交集，空/None 为全部（与原 SQL IN 语义一致）。

    库全集取三类元数据的并集（真实库中三者一致，并集兼容只有
    部分元数据的场景，与原逐查询独立过滤的语义对齐）。
    """
    universe = set(snapshot["tables"]) | set(snapshot["columns"]) | set(snapshot["unique"])
    if databases:
        return [s for s in databases if s in universe]
    return sorted(universe)


def _candidate_tables(
    conn: Any,
    param_names: list[str],
    databases: list[str] | None = None,
    include_generic: bool = False,
) -> dict[str, int]:
    """反查 information_schema 找包含参数列的表，返回 {库.表: 命中列数}。

    缺省只统计非通用列（打分主判据）；include_generic=True 时连 id/status
    等通用列一并统计，用于校验表名候选能否真的为参数供值。
    databases 为 None 时用 DB_CONFIG.databases 全局限定；域收窄阶段由调用方
    传入域库列表（优先在域内查，无结果再回退全局范围）。
    数据源为进程内 schema 快照（_get_schema_snapshot，批量只拉一次），
    本函数在快照上按“参数列名集合 + databases 范围 + 是否含通用列”缓存计算结果。
    """
    if databases is None:
        databases = _global_databases()
    snake_names = sorted({c for p in param_names for c in _column_candidates(p)})
    if not snake_names:
        return {}
    cache_key = (frozenset(snake_names), tuple(databases), include_generic)
    if cache_key in _candidate_cache:
        return _candidate_cache[cache_key]
    snapshot = _get_schema_snapshot(conn)
    if snapshot is None:
        return {}
    wanted = set(snake_names)
    hits: dict[str, int] = {}
    for schema in _snapshot_schemas(snapshot, databases):
        for table, cols in snapshot["columns"].get(schema, {}).items():
            matched = cols & wanted
            if not include_generic:
                matched -= _GENERIC_COLUMNS
            if matched:
                hits[f"{schema}.{table}"] = len(matched)
    # 缓存上限保护：参数集合种类超限时整体清空，避免进程内无界增长
    if len(_candidate_cache) >= 500:
        _candidate_cache.clear()
    _candidate_cache[cache_key] = hits
    return hits


def _table_backup_penalty(table_name: str) -> int:
    """表名含备份/临时词段（bak/copy/tmp/del，允许数字后缀）或纯数字段时返回惩罚分。"""
    for seg in _table_segments(table_name):
        stem = re.sub(r"\d+$", "", seg)
        if stem in _BACKUP_SEGMENTS or seg.isdigit():
            return _BACKUP_PENALTY
    return 0


def _unique_index_tables(conn: Any, param_names: list[str], databases: list[str] | None = None) -> set[str]:
    """反查参数列为唯一索引（含主键）的表集合，作为主表识别信号。

    查询参数如 demoNo 通常对应主表（demo_member_info）的唯一键列，引用表
    （demo_order 等）仅作外键引用。该集合用于候选表打分加分（不区分主表
    与引用表时，众多含 demo_no 列的引用表无法消歧），数据源为 schema 快照，
    计算结果进程内缓存。databases 语义同 _candidate_tables（None 走全局配置）。
    """
    if databases is None:
        databases = _global_databases()
    snake_names = sorted({c for p in param_names for c in _column_candidates(p)})
    if not snake_names:
        return set()
    cache_key = (frozenset(snake_names), tuple(databases))
    if cache_key in _unique_cache:
        return _unique_cache[cache_key]
    snapshot = _get_schema_snapshot(conn)
    if snapshot is None:
        return set()
    wanted = set(snake_names)
    tables: set[str] = set()
    for schema in _snapshot_schemas(snapshot, databases):
        for table, cols in snapshot["unique"].get(schema, {}).items():
            if cols & wanted:
                tables.add(f"{schema}.{table}")
    # 缓存上限保护：参数集合种类超限时整体清空，避免进程内无界增长
    if len(_unique_cache) >= 500:
        _unique_cache.clear()
    _unique_cache[cache_key] = tables
    return tables


def _match_keyword_count(table_name: str, keywords: list[str]) -> int:
    """统计表名覆盖的 URL 关键词数（词段精确匹配或互相包含均算覆盖）。"""
    segments = _table_segments(table_name)
    count = 0
    for kw in keywords:
        if any(_seg_matches(seg, kw) for seg in segments):
            count += 1
    return count


def _tables_by_name(conn: Any, keywords: list[str], databases: list[str] | None = None) -> dict[str, int]:
    """表名匹配候选：URL 业务词元覆盖表名的表（与列反查候选取并集）。

    LIKE 粗筛（任一关键词命中表名）后逐个严格校验：关键词覆盖率须达到
    全量（词元 ≤2 时）或全量减一（容忍最多一个干扰词元，如服务前缀），
    返回 {库.表: 覆盖词元数}。覆盖词元数在打分时充当命中数角色。
    不能只在列反查为空时才用：主表可能根本没有接口参数对应的列
    （如 prmt_combine_promotion 无 store_code 列），仅靠列反查会把它结构性排除。
    databases 语义同 _candidate_tables（None 走全局配置）。数据源为 schema
    快照：粗筛用大小写不敏感子串包含（等价原 SQL LIKE '%kw%' 的 CI  collation）。
    """
    if not keywords:
        return {}
    if databases is None:
        databases = _global_databases()
    cache_key = (frozenset(keywords), tuple(databases))
    if cache_key in _name_cache:
        return _name_cache[cache_key]
    snapshot = _get_schema_snapshot(conn)
    if snapshot is None:
        return {}
    required = len(keywords) if len(keywords) <= 2 else len(keywords) - 1
    lowered = [kw.lower() for kw in keywords]
    candidates: dict[str, int] = {}
    for schema in _snapshot_schemas(snapshot, databases):
        for table in snapshot["tables"].get(schema, ()):
            name_lower = table.lower()
            if not any(kw in name_lower for kw in lowered):
                continue
            count = _match_keyword_count(table, keywords)
            if count >= required:
                candidates[f"{schema}.{table}"] = count
    # 缓存上限保护：词元集合种类超限时整体清空，避免进程内无界增长
    if len(_name_cache) >= 500:
        _name_cache.clear()
    _name_cache[cache_key] = candidates
    return candidates


def _preferred_tables() -> set[str]:
    """DB_CONFIG.preferred_tables 配置的主表集合（同分消歧用，小写归一）。

    只作排序次级键、不参与加分：人工先验是“两张表旗鼓相当时选哪张”，
    若改成绝对加分（曾为 +10），会员主表这类被配置的大表会凭一个通用
    store_code 列压过业务语义正确的活动主表（promotionInfo 取错值的根因）。
    """
    db_config = APIConfig.DB_CONFIG() or {}
    return {str(t).lower() for t in (db_config.get("preferred_tables") or [])}


def _domain_schemas() -> dict[str, dict[str, Any]]:
    """DB_CONFIG.domain_schemas：业务域 → {schemas 库清单, url 词表, cn 词表}。

    域名与英文词元小写归一，库名保留配置原样（直接进 SQL 的 TABLE_SCHEMA IN）。
    未配 schemas 的域直接忽略（无法收窄到库范围的域定义无意义）。
    """
    raw = (APIConfig.DB_CONFIG() or {}).get("domain_schemas") or {}
    if not isinstance(raw, dict):
        return {}
    specs: dict[str, dict[str, Any]] = {}
    for domain, spec in raw.items():
        if not isinstance(spec, dict):
            continue
        schemas = [str(s) for s in (spec.get("schemas") or []) if s]
        if not schemas:
            continue
        specs[str(domain).lower()] = {
            "schemas": schemas,
            "url": [str(w).lower() for w in (spec.get("url") or [])],
            "cn": [str(w) for w in (spec.get("cn") or []) if w],
        }
    return specs


def _infer_domains(terms: list[str], cn_text: str) -> list[str]:
    """按英文词元与中文文本推断业务域（命中任一词表即入选，可多域）。

    推断结果只作“优先查找范围”而非硬过滤：词表必然有覆盖不到的写法
    （实测存量产物中约 120 个接口现有表与推断域库不一致，其中多数是词表
    误判，如 saveInvoiceSensitive 实属订单域），因此域内无结果时须回退全库。
    """
    lowered = {t.lower() for t in terms}
    domains: list[str] = []
    for domain, spec in _domain_schemas().items():
        if lowered & set(spec["url"]) or any(w in cn_text for w in spec["cn"]):
            domains.append(domain)
    return domains


def _domain_databases(domains: list[str]) -> list[str]:
    """域列表 → 库并集（去重保序），并与 DB_CONFIG.databases 全局范围取交集。

    取交集而不是覆盖：全局 databases 是用户显式划定的可见库边界，
    域配置不得把查询扩到边界之外；交集为空时返回空列表（跳过域阶段）。
    """
    specs = _domain_schemas()
    scope = {str(s).lower() for s in _global_databases()}
    out: list[str] = []
    seen: set[str] = set()
    for domain in domains:
        for schema in specs.get(domain, {}).get("schemas", []):
            key = schema.lower()
            if key in seen or (scope and key not in scope):
                continue
            seen.add(key)
            out.append(schema)
    return out


def _extra_segment_penalty(table_name: str, keywords: list[str]) -> int:
    """表名中未被任何 URL 词元覆盖的词段惩罚（主表优先，子表限定词降权）。

    keywords 为空时不罚：此时没有语义基准，按表名长短扣分等于凭空偏好短名。
    """
    if not keywords:
        return 0
    segments = _table_segments(table_name)
    extra = sum(1 for seg in segments if not any(_seg_matches(seg, kw) for kw in keywords))
    return extra * _EXTRA_SEGMENT_PENALTY


def _discover_in_scope(
    conn: Any,
    api_url: str,
    param_names: list[str],
    keywords: list[str],
    databases: list[str] | None,
    param_scope: bool = False,
) -> tuple[str, int] | None:
    """在指定库范围内做候选并集 + 打分 + 歧义判定（None 走全局配置）。

    域阶段（databases 非 None）的无候选/并列不告警：那只是中间结果，
    最终失败由回退的全库阶段统一告警，避免“建议配 api_table_map”误报。
    param_scope=True（参数级独立找表）时不施加多余词段惩罚：跨域参数的
    正确主表（活动接口里的会员主表）表名天然与接口词元无关，罚它等于
    系统性偏向接口本域的子表；此时主表识别交给唯一索引信号。
    """
    col_hits = _candidate_tables(conn, param_names, databases)
    name_hits = _tables_by_name(conn, keywords, databases)
    if name_hits:
        # 表名候选必须至少含一个参数列（含通用列）才能入选：主表可能只
        # 命中主键 id（被非通用过滤掉），但不能含任何参数列的表无法供值，
        # 让它凭表名抢分会顶掉真正能取到值的表（如 storeCode 参数级找表
        # 时选中无 store_code 列的活动主表，导致该参数永远取不到值）
        any_hits = _candidate_tables(conn, param_names, databases, include_generic=True)
        name_hits = {t: h for t, h in name_hits.items() if t in any_hits}
    candidates = dict(name_hits)
    for table, hits in col_hits.items():
        candidates[table] = max(hits, candidates.get(table, 0))
    if not candidates:
        if databases is None:
            logger.debug(f"接口 {api_url} 自动找表无候选表，跳过参数探测")
        return None
    # 唯一索引加分只认非通用参数列：id 这类通用列几乎每张表都是主键，
    # 计入会让所有候选同拿加分，主表识别信号恒真而失效
    biz_params = [p for p in param_names if not any(c in _GENERIC_COLUMNS for c in _column_candidates(p))]
    unique_tables = _unique_index_tables(conn, biz_params, databases)
    preferred = _preferred_tables()
    scored = sorted(
        (
            (
                hits * 10
                + _score_table_name(table, keywords)
                + (_UNIQUE_INDEX_BONUS if table in unique_tables else 0)
                - (0 if param_scope else _extra_segment_penalty(table, keywords))
                - _table_backup_penalty(table),
                table.lower() in preferred,
                table,
            )
            for table, hits in candidates.items()
        ),
        reverse=True,
    )
    # 同分且同为（或同不为）preferred 才算真歧义：preferred 是排序次级键，
    # 同分时应由它破局而不是放弃探测
    if len(scored) > 1 and scored[1][0] == scored[0][0] and scored[1][1] == scored[0][1]:
        if databases is None:
            names = ", ".join(item[2] for item in scored[:5])
            _warn_once(
                f"ambiguous:{api_url}",
                f"接口 {api_url} 自动找表有多个并列候选（{names}），请在 DB_CONFIG.api_table_map 中显式配置该接口的表映射",
            )
        return None
    winner = scored[0][2]
    # 命中数保持「列反查命中列数」语义（仅表名命中时为覆盖词元数），胜出后单独取
    return winner, col_hits.get(winner, candidates[winner])


def _auto_discover_table(
    conn: Any,
    api_url: str,
    param_names: list[str],
    description: str = "",
    param_remark: str = "",
    param_scope: bool = False,
) -> tuple[str, int] | None:
    """api_table_map 未命中时自动找表，返回 (库.表, 命中数)。

    两阶段查找：先按语义推断业务域、只在域库内找（多域取并集），域内无
    唯一胜出者再回退全库——域词表覆盖不全时不至于漏探。
    param_scope=True 表示参数级独立找表（跨域参数），域推断以参数自身
    语义（param_remark 中文 + 参数名词元）优先，推断不出才用接口语义。

    打分公式与候选并集理由见 _discover_in_scope。返回的命中数保持“列反查
    命中列数”语义（仅表名命中时为覆盖词元数），供日志与调用方提示用。
    """
    keywords = _url_keywords(api_url)
    domains = _infer_domains(keywords, description)
    if param_scope and len(param_names) == 1:
        param_domains = _infer_domains(_word_terms(param_names[0]), param_remark)
        if param_domains:
            domains = param_domains
    schemas = _domain_databases(domains)
    if schemas:
        found = _discover_in_scope(conn, api_url, param_names, keywords, schemas, param_scope)
        if found:
            return found
    return _discover_in_scope(conn, api_url, param_names, keywords, None, param_scope)


def _connect(db_config: dict[str, Any]) -> Any:
    """按 DB_CONFIG 建立数据库连接；不可用/失败时返回 None。

    线程局部复用：同一工作线程的后续调用直接返回已有连接（ping 保活，
    断线自动重连），避免批量生成逐接口 TCP+认证握手；连接由
    close_cached_connections 统一清理（批量结束时调用）。
    连接失败后进入熔断期（_CONNECT_RETRY_TTL 秒），期内后续调用直接返回 None，
    避免库不可达时批量生成的每个接口都吃满 connect_timeout；成功后清除熔断标记。
    """
    global _connect_failed_at
    if _connect_failed_at is not None and time.monotonic() - _connect_failed_at < _CONNECT_RETRY_TTL:
        return None
    cached = getattr(_conn_local, "conn", None)
    if cached is not None:
        try:
            cached.ping(reconnect=True)
            return cached
        except Exception:
            _conn_local.conn = None
    host = db_config.get("host")
    user = db_config.get("user")
    if not host or not user:
        _warn_once("missing_host_user", "DB_CONFIG 缺少 host/user，跳过数据库参数探测")
        return None
    # password_env 兼容两种写法：
    # 1) 填环境变量名（如 TEST_DB_PWD）→ 密码从该环境变量读取，不落盘；
    # 2) 直接填密码明文 → 环境变量查不到时把该值本身当密码使用。
    env_name = db_config.get("password_env") or ""
    password = os.environ.get(env_name)
    if password is None:
        password = env_name
    try:
        import pymysql
    except ImportError:
        _warn_once(
            "no_driver",
            "未安装 pymysql，跳过数据库参数探测（pip install pymysql 后可启用）",
        )
        return None
    try:
        conn = pymysql.connect(
            host=host,
            port=int(db_config.get("port") or 3306),
            user=user,
            password=password,
            charset="utf8mb4",
            connect_timeout=5,
            read_timeout=15,
        )
    except Exception as e:
        _connect_failed_at = time.monotonic()
        _warn_once("connect_fail", f"数据库连接失败（{host}），跳过参数探测: {e}")
        return None
    _connect_failed_at = None
    _conn_local.conn = conn
    with _conn_lock:
        _cached_conns.append(conn)
    return conn


def close_cached_connections() -> None:
    """关闭 _connect 缓存的全部连接（批量生成结束时调用）。

    其他线程的线程局部引用无需逐一清理：下次 _connect 的 ping(reconnect=True)
    会在已关闭连接上自动重连。
    """
    with _conn_lock:
        conns = list(_cached_conns)
        _cached_conns.clear()
    for conn in conns:
        try:
            conn.close()
        except Exception:
            pass


def _table_columns(cur: Any, table: str) -> tuple[list[str], list[str], list[str], dict[str, str]] | None:
    """返回表的 (列名列表, 主键列, 唯一索引列, 列名→类型 映射)。

    DESCRIBE 的 Key 列直接标注索引性质：PRI=主键、UNI=唯一索引、
    MUL=普通索引，无需额外 SHOW INDEX 查询。结果进程内缓存：
    批量生成时同表被多接口共享，结构批量期间视为静态。
    """
    cached = _structure_cache.get(table)
    if cached is not None:
        return cached
    try:
        cur.execute(f"DESCRIBE {_quote_table(table)}")
        rows = cur.fetchall()
    except Exception as e:
        _warn_once(f"describe_fail:{table}", f"读取表结构失败（{table}），跳过参数探测: {e}")
        return None
    columns = [str(r[0]).lower() for r in rows]
    primary = [str(r[0]).lower() for r in rows if r[3] == "PRI"]
    unique_cols = [str(r[0]).lower() for r in rows if r[3] == "UNI"]
    column_types = {str(r[0]).lower(): str(r[1]).lower() for r in rows}
    structure = (columns, primary, unique_cols, column_types)
    # 缓存上限保护：表种类超限时整体清空，避免进程内无界增长
    if len(_structure_cache) >= 500:
        _structure_cache.clear()
    _structure_cache[table] = structure
    return structure


def _column_candidates(name: str) -> list[str]:
    """参数名 → 列名候选（原样小写、驼峰转蛇形、复数去尾 s）。

    复数集合参数（如 ids）与单数列名（id）不同形：去掉尾部 s 再试，
    仅当列集合恰好存在单数列时才命中，不会误伤 status 这类词尾 s 词。
    """
    candidates = [name.lower()]
    snake = _snake_case(name)
    if snake not in candidates:
        candidates.append(snake)
    if snake.endswith("s") and len(snake) > 1:
        singular = snake[:-1]
        if singular not in candidates:
            candidates.append(singular)
    return candidates


def _match_columns(param_names: list[str], columns: list[str]) -> dict[str, str]:
    """把参数名匹配到表列名，返回 {参数名: 列名}。

    常规候选（原样/蛇形/去尾 s）未命中时，用“列名包含参数名”的子串兜底
    （如 messagecontent 包含 content，字段名带表名/业务前缀的常见形态）；
    包含列唯一时命中，多列并列时只保留以参数名结尾的列，仍不唯一则跳过
    不猜。兜底排在常规候选之后，不影响已有精确匹配行为。
    """
    matched: dict[str, str] = {}
    column_set = set(columns)
    for param in param_names:
        for candidate in _column_candidates(param):
            if candidate in column_set:
                matched[param] = candidate
                break
    # 子串兜底：等所有参数的精确匹配完成后再做，避免兜底抢占其他
    # 参数的精确命中列
    used = set(matched.values())
    for param in param_names:
        if param in matched:
            continue
        snake = _snake_case(param)
        contained = [c for c in columns if c not in used and snake in c]
        if len(contained) != 1:
            contained = [c for c in contained if c.endswith(snake)]
        if len(contained) == 1:
            matched[param] = contained[0]
            used.add(contained[0])
    return matched


def _fetch_sample_row(
    cur: Any, table: str, matched_columns: dict[str, str], where: str, primary: list[str]
) -> dict[str, Any] | None:
    """按条件取一条示例记录（主键倒序优先，其次首条）。"""
    columns_sql = ", ".join(f"`{c}`" for c in matched_columns.values())
    sql = f"SELECT {columns_sql} FROM {_quote_table(table)}"
    if where:
        sql += f" WHERE {where}"
    if primary:
        sql += f" ORDER BY `{primary[0]}` DESC"
    sql += " LIMIT 1"
    try:
        cur.execute(sql)
        row = cur.fetchone()
    except Exception as e:
        _warn_once(f"query_fail:{table}", f"查询示例记录失败（{table}），跳过参数探测: {e}")
        return None
    if not row:
        return None
    return dict(zip(matched_columns.values(), row))


# 数值列类型前缀：DESCRIBE 的 Type 字段以这些前缀开头时按数值处理（MAX+1）
_NUMERIC_TYPE_PREFIXES = (
    "bigint",
    "decimal",
    "double",
    "float",
    "int",
    "mediumint",
    "numeric",
    "smallint",
    "tinyint",
)


def _is_create_api(description: str, api_url: str) -> bool:
    """接口语义是否为新增（描述含新增/添加字样，或 URL 词元含 add/create）。"""
    if any(word in description for word in ("新增", "添加")):
        return True
    return any(word in ("add", "create") for word in _url_word_terms(api_url))


def _is_edit_api(description: str, api_url: str) -> bool:
    """接口语义是否为编辑（描述含编辑/修改字样，或 URL 词元含 edit/modify/update）。"""
    if any(word in description for word in ("编辑", "修改")):
        return True
    return any(word in ("edit", "modify", "update") for word in _url_word_terms(api_url))


def _url_word_terms(api_url: str) -> list[str]:
    """URL 全部词元（含 add/edit 这类表名停用词，语义判断用）。

    "/" 本就是 _word_terms 的非字母数字分隔符，直接对去 query 后的整串切词
    与逐路径段切词再合并等价（小写、去重保序一致）。
    """
    return _word_terms(api_url.split("?", 1)[0])


def _fresh_value(cur: Any, table: str, column: str, column_type: str, sample: Any) -> Any:
    """生成与库中已有值不冲突的示例值（数值 MAX+1、字符串加随机后缀）。

    新增接口传库中已有值大概率触发唯一性校验（敏感词判重等），
    故按列类型生成新值；随机后缀碰撞概率可忽略，不额外查重。
    """
    if column_type.startswith(_NUMERIC_TYPE_PREFIXES):
        try:
            cur.execute(f"SELECT MAX(`{column}`) FROM {_quote_table(table)}")
            row = cur.fetchone()
            max_value = row[0] if row and row[0] is not None else 0
            # 过 _to_jsonable：DECIMAL 列的 MAX 是 decimal.Decimal，直接返回会让
            # api.json 的 json.dump 抛 TypeError（只捕 OSError）而中断该接口生成
            return _to_jsonable(max_value + 1)
        except Exception:
            # MAX 查询失败退回原示例值（不阻断探测）
            return sample
    suffix = secrets.token_hex(3)
    if sample:
        return f"{sample}_t{suffix}"
    return f"t{suffix}"


def _to_jsonable(value: Any) -> Any:
    """把数据库驱动返回的非 JSON 类型（datetime/Decimal 等）转为可序列化值。"""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, dict)):
        return value
    return str(value)


def _probe_group(
    cur: Any,
    table: str,
    group_params: list[str],
    where: str,
    is_create: bool,
    is_edit: bool,
    declared_values: dict[str, Any] | None,
) -> dict[str, Any]:
    """对一张表探测一组参数的示例值，返回 {参数名: {"value", "remark"}}。

    值策略：新增/添加类接口全部参数生成不冲突值（避免唯一性校验拦截）；
    编辑/修改类接口主键列取已有值（存在性优先）、唯一索引列生成不冲突值；
    其余接口一律取已有示例值。数组形声明的参数包装为单元素列表。
    """
    structure = _table_columns(cur, table)
    if structure is None:
        return {}
    columns, primary, unique_cols, column_types = structure
    matched = _match_columns(group_params, columns)
    if not matched:
        return {}
    row = _fetch_sample_row(cur, table, matched, where, primary)
    if row is None:
        return {}
    values: dict[str, Any] = {}
    for param, column in matched.items():
        sample = _to_jsonable(row.get(column))
        if sample is None:
            continue
        value: Any = sample
        remark = f"示例值来自 {table}.{column}"
        if where:
            remark += f"（{where}）"
        if is_create:
            # 新增接口传已有值大概率触发业务唯一性校验（敏感词判重等），
            # 所有参数（含主键，数值 MAX+1）改为不冲突值
            value = _fresh_value(cur, table, column, column_types.get(column, ""), sample)
            remark += "，已生成不冲突值（新增接口）"
        elif is_edit and column in unique_cols:
            # 编辑接口：唯一索引列传已有值会被唯一性校验拦截；
            # 主键列保持已有值（编辑必须指向已存在记录）
            value = _fresh_value(cur, table, column, column_types.get(column, ""), sample)
            remark += "，已生成不冲突值（唯一索引列）"
        if declared_values and isinstance(declared_values.get(param), list):
            value = [value]
        values[param] = {"value": value, "remark": remark}
    return values


def probe_db_params(
    api_url: str,
    param_names: list[str],
    description: str = "",
    declared_values: dict[str, Any] | None = None,
    enum_values: dict[str, Any] | None = None,
    param_remarks: dict[str, str] | None = None,
) -> dict[str, Any] | None:
    """探测接口参数的数据库示例值。

    表来源优先级：api_table_map 显式映射 → 语义域库内自动找表 → 全库
    自动找表（候选唯一命中）→ 参数级独立找表（主表匹配不到的参数，如
    demoNo 在会员主表、demoCode 在产品主表，各自查各自的表）→ 未命中参数跳过。

    有枚举声明的参数（enum_values 含该键，如 platform 的 [1,2,3]）直接取
    第一个枚举值，不查库；其余参数按新增/编辑语义生成不冲突值或取已有值。

    Args:
        api_url: 接口 URL（或路径模板），用于匹配 DB_CONFIG.api_table_map 的键。
        param_names: 接口参数名列表（按 api.json params/data 键集合传入）。
        description: 接口描述（用于识别新增/编辑语义，并参与业务域推断）。
        declared_values: {参数名: 声明值}（api.json params/data 原始值，
            声明值为 list 的参数探测后包装为单元素列表）。
        enum_values: {参数名: 首个枚举值}（api.json param_values 各枚举首值，
            该键命中时参数直接取枚举值，不参与查库）。
        param_remarks: {参数名: Swagger 备注}（参数级独立找表时用于按参数
            语义推断业务域，如 storeCode 备注“门店编码”→ 店铺库）。

    Returns:
        {"table": 表名, "values": {参数名: {"value": 值, "remark": 来源说明}}}
        或 None（未配置映射 / 探测失败 / 无匹配字段或示例行）。
    """
    db_config = APIConfig.DB_CONFIG()
    if not db_config:
        return None

    values: dict[str, Any] = {}
    # 有枚举声明的参数直接取首个枚举值，不查库；数组形声明的参数与非枚举
    # 路径（_probe_group）一致包装为单元素列表。枚举提取先于建连：纯枚举
    # 接口无需连库（库不可达时也能产出枚举示例值）。
    if enum_values:
        for param, enum_value in enum_values.items():
            if param in param_names and enum_value is not None:
                if isinstance((declared_values or {}).get(param), list):
                    enum_value = [enum_value]
                values[param] = {
                    "value": enum_value,
                    "remark": "示例值来自接口参数枚举",
                }
    pending = [p for p in param_names if p not in values]
    if not pending:
        return {"table": "", "values": values}

    conn = _connect(db_config)
    if conn is None:
        return None
    is_create = _is_create_api(description, api_url)
    is_edit = _is_edit_api(description, api_url)
    # 连接归 _connect 的线程局部缓存所有，此处不关闭（批量跨接口复用，
    # 结束时由 close_cached_connections 统一清理）
    main_table = ""
    groups: dict[str, tuple[list[str], str]] = {}
    mapping = _find_table_mapping(api_url)
    if mapping:
        table, where = mapping
        groups[table] = (list(pending), where)
    else:
        discovered = _auto_discover_table(conn, api_url, pending, description=description)
        if discovered:
            table, hit_count = discovered
            logger.info(
                f"接口 {api_url} 自动发现候选表 {table}（匹配度 {hit_count}），"
                "建议在 DB_CONFIG.api_table_map 中固化该映射"
            )
            groups[table] = (list(pending), "")

    with conn.cursor() as cur:
        for table, (group_params, where) in groups.items():
            if not main_table:
                main_table = table
            values.update(_probe_group(cur, table, group_params, where, is_create, is_edit, declared_values))
        # 参数级独立找表：主表匹配不到的参数（跨表接口，如 demoNo 在
        # 会员主表、demoCode 在产品主表）逐个反查自己的候选表
        unmatched = [p for p in pending if p not in values]
        per_param: dict[str, str] = {}
        for param in unmatched:
            found = _auto_discover_table(
                conn,
                api_url,
                [param],
                description=description,
                param_remark=str((param_remarks or {}).get(param) or ""),
                param_scope=True,
            )
            if found:
                per_param[param] = found[0]
        merged: dict[str, list[str]] = {}
        for param, table in per_param.items():
            merged.setdefault(table, []).append(param)
        for table, group_params in merged.items():
            if not main_table:
                main_table = table
            values.update(_probe_group(cur, table, group_params, "", is_create, is_edit, declared_values))

    if not values:
        return None
    return {"table": main_table, "values": values}


def extract_db_values(db_params: dict[str, Any] | None) -> dict[str, Any]:
    """从 db_params 元数据提取 {参数名: 值}（消费端取示例值用）。"""
    if not db_params:
        return {}
    values = db_params.get("values") or {}
    result: dict[str, Any] = {}
    for key, entry in values.items():
        if isinstance(entry, dict):
            value = entry.get("value")
            if value is not None:
                result[key] = value
        elif entry is not None:
            result[key] = entry
    return result
