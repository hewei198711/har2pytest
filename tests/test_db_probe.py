"""测试 har2pytest.db_probe 模块中数据库参数探测的字段匹配、表映射、示例行查询与消费端提取的功能与边界。"""

import sys
import types
from datetime import datetime
from decimal import Decimal
from typing import Any

import allure
import pytest

from har2pytest import db_probe
from har2pytest.config import APIConfig
from har2pytest.db_probe import (
    _auto_discover_table,
    _candidate_tables,
    _column_candidates,
    _connect,
    _domain_databases,
    _domain_schemas,
    _extra_segment_penalty,
    _find_table_mapping,
    _fresh_value,
    _infer_domains,
    _is_create_api,
    _is_edit_api,
    _map_matches,
    _match_columns,
    _match_keyword_count,
    _score_table_name,
    _snake_case,
    _table_backup_penalty,
    _tables_by_name,
    _to_jsonable,
    _unique_index_tables,
    _url_keywords,
    _word_terms,
    extract_db_values,
    probe_db_params,
)


@pytest.fixture(autouse=True)
def _reset_warn_cache():
    """每个测试前后清空模块级警告去重、各类缓存、schema 快照与连接熔断标记，保证测试间隔离。"""
    db_probe._warned_reasons.clear()
    db_probe._candidate_cache.clear()
    db_probe._unique_cache.clear()
    db_probe._name_cache.clear()
    db_probe._structure_cache.clear()
    db_probe._schema_snapshot = None
    db_probe._cached_conns.clear()
    db_probe._conn_local.conn = None
    db_probe._connect_failed_at = None
    yield
    db_probe._warned_reasons.clear()
    db_probe._candidate_cache.clear()
    db_probe._unique_cache.clear()
    db_probe._name_cache.clear()
    db_probe._structure_cache.clear()
    db_probe._schema_snapshot = None
    db_probe._cached_conns.clear()
    db_probe._conn_local.conn = None
    db_probe._connect_failed_at = None


def _fake_db_config(**overrides) -> dict:
    """构造测试用 DB_CONFIG 字典（虚构占位值）。"""
    config = {
        "host": "demo.mysql.example.com",
        "port": 3306,
        "user": "demo_tester",
        "password_env": "DEMO_TEST_DB_PWD",
        "api_table_map": {
            "/demo/save": {"table": "demo_db.demo_table", "where": "status = 0"},
        },
    }
    config.update(overrides)
    return config


def _patch_db_config(monkeypatch, config):
    """把 APIConfig.DB_CONFIG 访问器替换为返回指定配置。"""
    monkeypatch.setattr(APIConfig, "DB_CONFIG", classmethod(lambda cls: config))


class _FakeCursor:
    """伪造游标：返回预设列结构/反查候选行/唯一索引行/示例行，并记录执行过的 SQL。

    fetchall 按 SQL 内容分派：information_schema.STATISTICS 反查返回
    unique_rows，information_schema.COLUMNS 反查按 execute 的列名参数过滤
    discover_rows（模拟 WHERE COLUMN_NAME IN），information_schema.TABLES
    表名反查返回 name_rows（缺省从 discover_rows 取库.表二元组，因为列
    反查命中的表必然存在于 TABLES），DESCRIBE 返回 columns；fetchone
    按 MAX( 分派 max_row。columns/row 支持 dict（表名→值）时按 SQL 中
    出现的库/表名分派，支持多表跨表探测测试。
    """

    def __init__(self, columns, row, discover_rows=None, unique_rows=None, max_row=None, name_rows=None):
        self._columns = columns
        self._row = row
        self._discover_rows = discover_rows or []
        self._unique_rows = unique_rows or []
        self._max_row = max_row
        self._name_rows = name_rows
        self.sqls = []
        self.calls: list[tuple[str, list[Any]]] = []
        self._params: list[Any] = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, sql, params=None):
        self.sqls.append(sql)
        self._params = list(params) if params else []
        self.calls.append((sql, self._params))

    def _pick(self, mapping):
        """mapping 为 dict（表名→值）时按 SQL 中出现的库/表名分派，否则原样返回。"""
        if not isinstance(mapping, dict):
            return mapping
        last = self.sqls[-1]
        for table, value in mapping.items():
            parts = table.split(".", 1)
            if all(part in last for part in parts):
                return value
        return None

    def _in_schemas(self, rows):
        """模拟 SQL 尾部的 TABLE_SCHEMA IN (...) 库范围过滤（域收窄/全局 databases）。"""
        last = self.sqls[-1]
        if "TABLE_SCHEMA IN (" not in last:
            return rows
        count = last.split("TABLE_SCHEMA IN (", 1)[1].count("%s")
        schemas = set(self._params[-count:]) if count else set()
        return [r for r in rows if r[0] in schemas]

    def fetchall(self):
        if self.sqls:
            last = self.sqls[-1]
            if "STATISTICS" in last:
                return self._in_schemas(self._unique_rows)
            if "information_schema" in last:
                if "COLUMNS" in last and self._params:
                    rows = [r for r in self._discover_rows if str(r[2]) in self._params]
                    return self._in_schemas(rows)
                if "TABLES" in last:
                    rows = self._name_rows
                    if rows is None:
                        rows = sorted({(r[0], r[1]) for r in self._discover_rows})
                    return self._in_schemas(rows)
                return self._discover_rows
        return self._pick(self._columns) or []

    def fetchone(self):
        if self.sqls and "MAX(" in self.sqls[-1]:
            return self._max_row
        return self._pick(self._row)


class _FakeConn:
    """伪造连接：每次 cursor() 返回同一游标，close 置位，ping 计数（连接复用保活）。"""

    def __init__(self, columns, row, discover_rows=None, unique_rows=None, max_row=None, name_rows=None):
        self._cursor = _FakeCursor(columns, row, discover_rows, unique_rows, max_row, name_rows)
        self.closed = False
        self.ping_calls = 0

    def cursor(self):
        return self._cursor

    def ping(self, reconnect=True):
        self.ping_calls += 1

    def close(self):
        self.closed = True


# ==================== 字段匹配辅助函数测试 ====================


@pytest.mark.parametrize("name,expected", [
    pytest.param("demoVisitOperator", "demo_visit_operator", id="驼峰转蛇形"),
    pytest.param("id", "id", id="单词原样"),
    pytest.param("pageNum", "page_num", id="分页参数名"),
    pytest.param("already_snake", "already_snake", id="已是蛇形原样"),
])
@allure.feature("数据库参数探测")
@allure.story("字段匹配")
@allure.title("测试驼峰参数名转蛇形列名")
def test_snake_case_forms(name, expected):
    assert _snake_case(name) == expected


@pytest.mark.parametrize("params,columns,expected", [
    pytest.param(["id", "demoVisitRemark", "unknownField"], ["id", "demo_visit_remark", "created_at"], {"id": "id", "demoVisitRemark": "demo_visit_remark"}, id="原样与蛇形两种候选"),
    # ids 去尾 s 命中 id；status 精确命中自身，不退化匹配不存在的 statu
    pytest.param(["ids", "status"], ["id", "name", "status"], {"ids": "id", "status": "status"}, id="复数参数匹配单数列且不误伤词尾s词"),
    # 常规候选（content）不命中 → 唯一包含列 messagecontent 兜底命中
    pytest.param(["content"], ["id", "messagecontent", "pict_list", "mobile"], {"content": "messagecontent"}, id="子串兜底匹配"),
    # 精确候选优先：同时存在 content 与 messagecontent 时取 content
    pytest.param(["content"], ["content", "messagecontent"], {"content": "content"}, id="精确候选优先"),
    # 多列包含且仅一列以参数名结尾 → 取该列
    pytest.param(["content"], ["replycontent", "content_mark"], {"content": "replycontent"}, id="仅一列以参数名结尾"),
    # 多列都以参数名结尾 → 歧义跳过不猜
    pytest.param(["content"], ["replycontent", "democontent"], {}, id="多列结尾歧义跳过"),
    # 无包含列 → 跳过
    pytest.param(["content"], ["id", "remark"], {}, id="无包含列跳过"),
])
@allure.feature("数据库参数探测")
@allure.story("字段匹配")
@allure.title("测试参数名与表列名匹配各形态")
def test_match_columns_forms(params, columns, expected):
    assert _match_columns(params, columns) == expected


@pytest.mark.parametrize("name,expected", [
    pytest.param("ids", ["ids", "id"], id="复数去尾s候选"),
    pytest.param("demoVisitOperator", ["demovisitoperator", "demo_visit_operator"], id="驼峰原样与蛇形候选"),
    pytest.param("id", ["id"], id="单词单候选"),
    pytest.param("already_snake", ["already_snake"], id="蛇形单候选"),
])
@allure.feature("数据库参数探测")
@allure.story("字段匹配")
@allure.title("测试列名候选生成（原样、蛇形、复数去尾 s）")
def test_column_candidates_forms(name, expected):
    assert _column_candidates(name) == expected


@pytest.mark.parametrize("pattern,url,expected", [
    pytest.param("/demo/save", "/demo/save", True, id="精确命中"),
    pytest.param("/demo/*", "/demo/save", True, id="通配命中"),
    pytest.param("/demo/{action}", "/demo/save", True, id="路径模板命中"),
    pytest.param("/other/*", "/demo/save", False, id="不命中"),
])
@allure.feature("数据库参数探测")
@allure.story("表映射匹配")
@allure.title("测试 URL 精确、通配与路径模板三种命中方式")
def test_map_matches_forms(pattern, url, expected):
    assert _map_matches(pattern, url) is expected


@allure.feature("数据库参数探测")
@allure.story("表映射匹配")
@allure.title("测试按 URL 查找表映射（简写/对象/未命中）")
def test_find_table_mapping(monkeypatch):
    config = _fake_db_config(
        api_table_map={
            "/demo/save": "demo_db.demo_table_short",
            "/demo/{action}": {"table": "demo_db.demo_table_tpl", "where": "flag = 1"},
        }
    )
    _patch_db_config(monkeypatch, config)
    assert _find_table_mapping("/demo/save") == ("demo_db.demo_table_short", "")
    assert _find_table_mapping("/demo/update") == ("demo_db.demo_table_tpl", "flag = 1")
    assert _find_table_mapping("/no/match") is None


@allure.feature("数据库参数探测")
@allure.story("表映射匹配")
@allure.title("测试未配置 DB_CONFIG 或 api_table_map 时返回 None")
def test_find_table_mapping_without_config(monkeypatch):
    _patch_db_config(monkeypatch, None)
    assert _find_table_mapping("/demo/save") is None
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    assert _find_table_mapping("/demo/save") is None


# ==================== 自动找表测试 ====================


@pytest.mark.parametrize("url,expected", [
    pytest.param("/demo/queryDemoOrderDetail", ["demo", "order"], id="驼峰分词与停用词过滤"),
    pytest.param("/demo/order/order", ["demo", "order"], id="去重"),
    pytest.param("/mgmt/esb/get?page=1", [], id="全停用词返回空"),
])
@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试 URL 关键词提取（驼峰分词、停用词过滤、去重）")
def test_url_keywords_forms(url, expected):
    assert _url_keywords(url) == expected


@pytest.mark.parametrize("table,keywords,expected", [
    pytest.param("demo_order_info", ["order"], 5, id="精确命中5分"),
    pytest.param("demo_order_info", ["demo"], 5, id="词段精确5分"),
    pytest.param("demo_order_info", ["unknown"], 0, id="无关0分"),
    # 关键词 ecenter 包含词段 center（非精确匹配）→ 3 分
    pytest.param("demo_experience_center", ["ecenter"], 3, id="包含命中3分"),
    # schema 名含业务词元（如 demo_center_member）不参与打分，只对表名部分打分
    pytest.param("demo_center_member.demo_member_info", ["member"], 5, id="表名部分命中"),
    pytest.param("demo_center_member.demo_seller_data", ["member"], 0, id="仅schema含词元不打分"),
])
@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试表名与关键词相似度打分（精确 5 分、包含 3 分、无关 0 分）")
def test_score_table_name_forms(table, keywords, expected):
    assert _score_table_name(table, keywords) == expected


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试候选表反查：通用列不参与命中统计")
def test_candidate_tables_skip_generic_columns(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn([], None, discover_rows=[("demo_db", "demo_common", "id")])
    assert _candidate_tables(conn, ["id"]) == {}


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试候选表反查按 databases 限定库范围")
def test_candidate_tables_databases_filter(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={}, databases=["demo_db", "demo_user"]),
    )
    conn = _FakeConn([], None, discover_rows=[("demo_db", "demo_experience_center", "self_code")])
    result = _candidate_tables(conn, ["selfCode"])
    assert result == {"demo_db.demo_experience_center": 1}
    # 快照为全库超集，库范围在计算时过滤：换成不命中的库范围即无候选
    assert _candidate_tables(conn, ["selfCode"], databases=["demo_user"]) == {}


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试候选表反查按参数列集合进程内缓存")
def test_candidate_tables_cache(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn([], None, discover_rows=[("demo_db", "demo_experience_center", "self_code")])
    first = _candidate_tables(conn, ["selfCode"])
    second = _candidate_tables(conn, ["selfCode"])
    assert first == {"demo_db.demo_experience_center": 1}
    assert second == first
    info_queries = [s for s in conn._cursor.sqls if "information_schema" in s]
    # schema 快照一次性全量拉取元数据（TABLES/COLUMNS/STATISTICS 三查），
    # 后续相同参数集合走缓存不再发查询
    assert len(info_queries) == 3


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试自动找表唯一最高分候选胜出")
def test_auto_discover_table_unique_winner(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_experience_center", "self_code"),
            ("demo_db", "demo_order", "self_code"),
        ],
    )
    # URL 词元 [demo, center]：demo_experience_center 命中 demo+center 两词段胜出
    result = _auto_discover_table(conn, "/demo/center/query", ["selfCode"])
    assert result == ("demo_db.demo_experience_center", 1)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试自动找表并列候选时返回 None")
def test_auto_discover_table_ambiguous(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_order_a", "self_code"),
            ("demo_db", "demo_order_b", "self_code"),
        ],
    )
    assert _auto_discover_table(conn, "/demo/order/query", ["selfCode"]) is None


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试自动找表无候选表时返回 None")
def test_auto_discover_table_no_candidates(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn([], None, discover_rows=[])
    assert _auto_discover_table(conn, "/demo/center/query", ["selfCode"]) is None


@pytest.mark.parametrize("table,expected", [
    pytest.param("demo_db.demo_table", 0, id="正常表无惩罚"),
    pytest.param("demo_db.demo_table_bak_20261027", db_probe._BACKUP_PENALTY, id="bak日期后缀惩罚"),
    pytest.param("demo_db.demo_table_copy1", db_probe._BACKUP_PENALTY, id="copy后缀惩罚"),
])
@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试备份表惩罚各形态")
def test_table_backup_penalty_forms(table, expected):
    assert _table_backup_penalty(table) == expected


@pytest.mark.parametrize("table,expected", [
    pytest.param("demo_db.demo_table", "`demo_db`.`demo_table`", id="库表分段引用"),
    pytest.param("demo_table", "`demo_table`", id="单表引用"),
    pytest.param("demo_db.we`ird", "`demo_db`.`we``ird`", id="内嵌反引号转义"),
])
@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试 SQL 标识符统一反引号引用（库.表/单表/内嵌反引号转义）")
def test_quote_table_forms(table, expected):
    assert db_probe._quote_table(table) == expected


@pytest.mark.parametrize("table,keywords,expected", [
    pytest.param("demo_db.order_invoice_sensitive", ["isensitive", "invoice", "sensitive"], 3, id="精确与互相包含全命中"),
    pytest.param("demo_db.demo_table", ["demo", "unknown"], 1, id="部分命中"),
    pytest.param("demo_db.demo_table", ["unknown"], 0, id="无命中"),
])
@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试表名覆盖 URL 词元数统计（精确与互相包含）")
def test_match_keyword_count_forms(table, keywords, expected):
    assert _match_keyword_count(table, keywords) == expected


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试唯一索引表反查与进程内缓存")
def test_unique_index_tables(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn([], None, unique_rows=[("demo_db", "demo_member_info", "card_no")])
    result = _unique_index_tables(conn, ["cardNo"])
    assert result == {"demo_db.demo_member_info"}
    # 第二次走缓存，不再重复反查
    assert _unique_index_tables(conn, ["cardNo"]) == result
    stats_queries = [s for s in conn._cursor.sqls if "STATISTICS" in s]
    assert len(stats_queries) == 1


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试表名匹配兜底：词元覆盖率达标才入选")
def test_tables_by_name(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_invoice_sensitive", "sensitive_no"),
            ("demo_db", "demo_invoice", "invoice_no"),
        ],
    )
    result = _tables_by_name(conn, ["isensitive", "invoice", "sensitive"])
    # demo_invoice_sensitive 覆盖全部 3 词元；demo_invoice 只覆盖 1 个不入选
    assert result == {"demo_db.demo_invoice_sensitive": 3}


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试表名匹配按词元集合进程内缓存（参数级找表不重复全表扫描）")
def test_tables_by_name_cache(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_invoice_sensitive", "sensitive_no"),
            ("demo_db", "demo_invoice", "invoice_no"),
        ],
    )
    first = _tables_by_name(conn, ["isensitive", "invoice", "sensitive"])
    second = _tables_by_name(conn, ["isensitive", "invoice", "sensitive"])
    assert first == {"demo_db.demo_invoice_sensitive": 3}
    assert second == first
    tables_queries = [s for s in conn._cursor.sqls if "information_schema.TABLES" in s]
    assert len(tables_queries) == 1


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试唯一索引列候选表加分胜出（主表识别）")
def test_auto_discover_table_unique_index_bonus(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_member_info", "card_no"),
            ("demo_db", "demo_blacklist", "card_no"),
        ],
        unique_rows=[("demo_db", "demo_member_info", "card_no")],
    )
    # 同列命中数下：member_info 表名命中 demo+member 且唯一索引加分，胜出
    result = _auto_discover_table(conn, "/demo/member/query", ["cardNo"])
    assert result == ("demo_db.demo_member_info", 1)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试备份表同分时被惩罚降权")
def test_auto_discover_table_backup_penalty(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_member_info", "card_no"),
            ("demo_db", "demo_member_info_bak_20261027", "card_no"),
        ],
        unique_rows=[
            ("demo_db", "demo_member_info", "card_no"),
            ("demo_db", "demo_member_info_bak_20261027", "card_no"),
        ],
    )
    result = _auto_discover_table(conn, "/demo/member/query", ["cardNo"])
    assert result == ("demo_db.demo_member_info", 1)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试列反查无候选时退回表名匹配唯一命中")
def test_auto_discover_table_fallback_by_name(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[("demo_db", "demo_invoice_sensitive", "id")],
    )
    # ids→id 属通用列：列反查无候选 → 表名匹配（词元全覆盖）唯一命中
    result = _auto_discover_table(conn, "/demo/isensitive/mgmt/deleteInvoiceSensitive", ["ids"])
    assert result == ("demo_db.demo_invoice_sensitive", 4)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试 preferred_tables 同分消歧打破唯一索引并列")
def test_auto_discover_table_preferred_bonus(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_card_account", "card_no"),
            ("demo_db", "demo_card_wallet", "card_no"),
        ],
        unique_rows=[
            ("demo_db", "demo_card_account", "card_no"),
            ("demo_db", "demo_card_wallet", "card_no"),
        ],
    )
    # 两表同列命中、同为唯一索引、表名相似度相同 → 并列返回 None
    assert _auto_discover_table(conn, "/demo/member/query", ["cardNo"]) is None
    # 配置 preferred_tables 后同分破局（人工先验：card_account 是主表）
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={}, preferred_tables=["demo_db.demo_card_account"]),
    )
    assert _auto_discover_table(conn, "/demo/member/query", ["cardNo"]) == (
        "demo_db.demo_card_account",
        1,
    )


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试 preferred_tables 不得压过表名语义更高的候选表")
def test_auto_discover_table_preferred_not_override_score(monkeypatch):
    """回归：promotionInfo 的活动 id 曾被 preferred 的会员主表抢走。

    会员表凭通用 store_code 列入选，旧实现的 preferred 绝对加分（+10）
    叠上唯一索引加分后压过业务语义正确的活动主表；改为同分消歧键后，
    表名命中 URL 词元更多的活动主表必须胜出。
    """
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={}, preferred_tables=["demo_db.demo_member_info"]),
    )
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_member_info", "store_code"),
            ("demo_db", "demo_promotion_combine", "store_code"),
        ],
        unique_rows=[("demo_db", "demo_member_info", "store_code")],
    )
    result = _auto_discover_table(conn, "/demo/combine/promotionInfo", ["storeCode"])
    assert result == ("demo_db.demo_promotion_combine", 1)


# ==================== 业务域推断与库范围收窄测试 ====================


def _domain_specs() -> dict:
    """测试用业务域词表（会员/店铺/活动三域，虚构库名）。"""
    return {
        "member": {"schemas": ["demo_member_db"], "url": ["member", "card"], "cn": ["会员", "顾客"]},
        "store": {"schemas": ["demo_store_db"], "url": ["store"], "cn": ["门店", "店铺"]},
        "promotion": {"schemas": ["demo_prmt_db"], "url": ["promotion", "combine"], "cn": ["活动"]},
    }


@pytest.mark.parametrize("text,expected", [
    pytest.param("storeCode", ["store", "code"], id="驼峰切分"),
    pytest.param("demo_visit_operator", ["demo", "visit", "operator"], id="下划线切分"),
    # 与 _url_keywords 不同：停用词保留（add/edit 语义判定靠它）
    pytest.param("getInfo", ["get", "info"], id="停用词保留"),
])
@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试词元切分（驼峰/下划线，不过滤停用词）")
def test_word_terms_forms(text, expected):
    assert _word_terms(text) == expected


@pytest.mark.parametrize("url,expected", [
    pytest.param("/demo/addRecord?page=1", ["demo", "add", "record"], id="含停用词去query"),
    pytest.param("/demo/getInfo", ["demo", "get", "info"], id="驼峰切词去重保序"),
])
@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试 URL 全词元提取（含停用词、去 query、驼峰切词去重保序）")
def test_url_word_terms_forms(url, expected):
    assert db_probe._url_word_terms(url) == expected


@pytest.mark.parametrize("url,expected", [
    pytest.param("/mobile/cms/material/saveDownloadLog", ["mobile", "cms", "material"], id="过滤DownloadLog留痕词元"),
    pytest.param("/demo/logs/list", ["demo"], id="过滤logs词元"),
])
@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试 URL 关键词过滤 log/logs 留痕词元")
def test_url_keywords_stop_log_forms(url, expected):
    assert _url_keywords(url) == expected


@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试 domain_schemas 归一化与非法条目忽略")
def test_domain_schemas(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(
            api_table_map={},
            domain_schemas={
                "Member": {"schemas": ["demo_member_db"], "url": ["Member", "vip"], "cn": ["会员"]},
                "empty": {"url": ["x"]},
                "bad": "demo_db",
            },
        ),
    )
    assert _domain_schemas() == {"member": {"schemas": ["demo_member_db"], "url": ["member", "vip"], "cn": ["会员"]}}


@pytest.mark.parametrize("terms,description,expected", [
    pytest.param(["combine", "promotion"], "获取3S组合活动详情", ["promotion"], id="英文词元命中单域"),
    pytest.param(["member"], "会员活动", ["member", "promotion"], id="中文命中可多域"),
    pytest.param(["cms"], "素材下载", [], id="无命中返回空"),
    pytest.param([], "门店编码", ["store"], id="仅中文命中"),
])
@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试业务域推断：英文词元与中文任一命中即入选，可多域")
def test_infer_domains_forms(monkeypatch, terms, description, expected):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}, domain_schemas=_domain_specs()))
    assert _infer_domains(terms, description) == expected


@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试域库并集去重并与全局 databases 取交集")
def test_domain_databases(monkeypatch):
    specs = {
        "member": {"schemas": ["demo_member_db", "demo_shared"]},
        "promotion": {"schemas": ["demo_prmt_db", "demo_shared"]},
    }
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}, domain_schemas=specs))
    assert _domain_databases(["member", "promotion"]) == [
        "demo_member_db",
        "demo_shared",
        "demo_prmt_db",
    ]
    assert _domain_databases([]) == []
    # 全局 databases 是可见库边界：域库超出边界的部分被裁掉
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={}, domain_schemas=specs, databases=["demo_prmt_db"]),
    )
    assert _domain_databases(["member", "promotion"]) == ["demo_prmt_db"]
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={}, domain_schemas=specs, databases=["demo_other"]),
    )
    assert _domain_databases(["member"]) == []


@pytest.mark.parametrize("table,keywords,expected", [
    pytest.param("demo_db.prmt_combine_promotion", ["combine", "promotion"], db_probe._EXTRA_SEGMENT_PENALTY, id="一个未覆盖词段扣一分"),
    pytest.param("demo_db.prmt_monthly_promotion", ["combine", "promotion"], 2 * db_probe._EXTRA_SEGMENT_PENALTY, id="两个未覆盖词段扣两分"),
    pytest.param("demo_db.combine_promotion", ["combine", "promotion"], 0, id="全覆盖不罚"),
    pytest.param("demo_db.any_table", [], 0, id="无词元不罚"),
])
@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试表名多余词段惩罚（未覆盖词段每段扣分，无词元不罚）")
def test_extra_segment_penalty_forms(table, keywords, expected):
    assert _extra_segment_penalty(table, keywords) == expected


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试候选并集：主表无参数列时凭表名入选（promotionInfo 回归）")
def test_auto_discover_table_union_name_candidate(monkeypatch):
    """活动主表只有主键 id（通用列被过滤），仅靠列反查会把它结构性排除，
    让凭通用 store_code 入选的会员主表抢走活动 id。"""
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={}, preferred_tables=["demo_member_db.demo_member_info"]),
    )
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_member_db", "demo_member_info", "store_code"),
            ("demo_prmt_db", "demo_prmt_combine_promotion", "id"),
        ],
        unique_rows=[("demo_member_db", "demo_member_info", "store_code")],
    )
    result = _auto_discover_table(conn, "/demo/combine/promotionInfo", ["id", "storeCode"])
    assert result == ("demo_prmt_db.demo_prmt_combine_promotion", 3)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试表名候选须含参数列才入选（无法供值的表不得凭表名抢分）")
def test_auto_discover_table_name_candidate_needs_param_column(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[("demo_db", "demo_prmt_monthly_promotion", "store_code")],
        name_rows=[
            ("demo_db", "demo_prmt_combine_promotion"),
            ("demo_db", "demo_prmt_monthly_promotion"),
        ],
    )
    # 活动主表表名更贴合 URL，但无 store_code 列 → 不得入选
    result = _auto_discover_table(conn, "/demo/combine/promotionInfo", ["storeCode"], param_scope=True)
    assert result == ("demo_db.demo_prmt_monthly_promotion", 1)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试唯一索引反查排除通用参数列（id 不再让所有表同拿加分）")
def test_unique_index_query_skips_generic_columns(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_order_a", "store_code"),
            ("demo_db", "demo_order_b", "store_code"),
        ],
        unique_rows=[
            ("demo_db", "demo_order_a", "id"),
            ("demo_db", "demo_order_b", "store_code"),
        ],
    )
    # 通用列 id 不参与唯一索引加分：否则两表同拿加分并列返回 None；
    # 排除后仅 store_code 为唯一索引的 order_b 拿加分胜出
    result = _auto_discover_table(conn, "/demo/order/query", ["id", "storeCode"])
    assert result == ("demo_db.demo_order_b", 1)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试三个元数据反查均排除 MySQL 系统库（系统表不得当主表）")
def test_metadata_queries_exclude_system_schemas(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[("information_schema", "INNODB_FT_CONFIG", "store_code")],
        unique_rows=[("information_schema", "INNODB_FT_CONFIG", "PRIMARY")],
        name_rows=[("demo_db", "demo_order")],
    )
    _auto_discover_table(conn, "/demo/order/query", ["id", "storeCode"])
    meta = [sql for sql, _ in conn._cursor.calls if "information_schema." in sql]
    # COLUMNS 列反查（含通用列的二次校验会再查一次）+ STATISTICS 唯一索引 + TABLES 表名
    assert {sql.split("information_schema.")[1].split()[0] for sql in meta} == {"COLUMNS", "STATISTICS", "TABLES"}
    assert all("TABLE_SCHEMA NOT IN ('information_schema','mysql','performance_schema','sys')" in sql for sql in meta)


@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试域内优先查找：只在推断域的库内反查")
def test_auto_discover_table_domain_priority(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}, domain_schemas=_domain_specs()))
    discover_rows = [
        ("demo_member_db", "demo_member_info", "store_code"),
        ("demo_member_db", "demo_member_info", "card_no"),
        ("demo_member_db", "demo_member_info", "mobile"),
        ("demo_member_db", "demo_member_info", "email"),
        ("demo_member_db", "demo_member_info", "vip_level"),
        ("demo_prmt_db", "demo_prmt_combine_promotion", "id"),
    ]
    conn = _FakeConn([], None, discover_rows=discover_rows)
    params = ["id", "storeCode", "cardNo", "mobile", "email", "vipLevel"]
    result = _auto_discover_table(conn, "/demo/combine/promotionInfo", params, description="获取3S组合活动详情")
    assert result is not None
    assert result[0] == "demo_prmt_db.demo_prmt_combine_promotion"
    # 域收窄现为 schema 快照上的内存过滤（不再逐域发 SQL），结果级断言已锁定只选中活动域表
    # 对照：未配域词表时会员表凭 5 个非通用列命中胜出（证明收窄确实生效）
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    db_probe._candidate_cache.clear()
    conn2 = _FakeConn([], None, discover_rows=discover_rows)
    fallback = _auto_discover_table(conn2, "/demo/combine/promotionInfo", params)
    assert fallback is not None
    assert fallback[0] == "demo_member_db.demo_member_info"


@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试域内无候选时回退全库（词表误判不致于漏探）")
def test_auto_discover_table_domain_fallback(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}, domain_schemas=_domain_specs()))
    conn = _FakeConn([], None, discover_rows=[("demo_member_db", "demo_member_info", "store_code")])
    result = _auto_discover_table(conn, "/demo/combine/promotionInfo", ["storeCode"], description="获取3S组合活动详情")
    assert result == ("demo_member_db.demo_member_info", 1)


@allure.feature("数据库参数探测")
@allure.story("业务域推断")
@allure.title("测试参数级找表按参数备注定域（跨域参数不被接口主域带偏）")
def test_auto_discover_table_param_scope_domain(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}, domain_schemas=_domain_specs()))
    discover_rows = [
        ("demo_prmt_db", "demo_prmt_monthly_promotion", "store_code"),
        ("demo_store_db", "demo_store_profile", "store_code"),
    ]
    conn = _FakeConn([], None, discover_rows=discover_rows)
    result = _auto_discover_table(
        conn,
        "/demo/combine/promotionInfo",
        ["storeCode"],
        description="获取3S组合活动详情",
        param_remark="云商微店门店编码",
        param_scope=True,
    )
    assert result == ("demo_store_db.demo_store_profile", 1)
    # 对照：接口级找表用接口主域（活动）→ 选中活动库的表，
    # 证明参数级定域确实把跨域参数从接口主域里拉了出来
    db_probe._candidate_cache.clear()
    conn2 = _FakeConn([], None, discover_rows=discover_rows)
    result2 = _auto_discover_table(
        conn2,
        "/demo/combine/promotionInfo",
        ["storeCode"],
        description="获取3S组合活动详情",
    )
    assert result2 == ("demo_prmt_db.demo_prmt_monthly_promotion", 1)


@allure.feature("数据库参数探测")
@allure.story("自动找表")
@allure.title("测试参数级找表不罚表名多余词段（跨域主表凭唯一索引胜出）")
def test_auto_discover_table_param_scope_no_extra_penalty(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    discover_rows = [
        ("demo_db", "demo_member_info", "card_no"),
        ("demo_db", "demo_promotion", "card_no"),
    ]
    unique_rows = [("demo_db", "demo_member_info", "card_no")]
    url = "/demo/active/getPromotionProductInfo"
    conn = _FakeConn([], None, discover_rows=discover_rows, unique_rows=unique_rows)
    assert _auto_discover_table(conn, url, ["cardNo"], param_scope=True) == (
        "demo_db.demo_member_info",
        1,
    )
    # 对照：接口级找表仍罚词段，表名贴合 URL 的活动表胜出
    db_probe._candidate_cache.clear()
    db_probe._unique_cache.clear()
    conn2 = _FakeConn([], None, discover_rows=discover_rows, unique_rows=unique_rows)
    assert _auto_discover_table(conn2, url, ["cardNo"]) == ("demo_db.demo_promotion", 1)


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试 probe_db_params 透传参数备注：活动 id 取活动主表、门店编码取店铺表")
def test_probe_db_params_param_remarks_domain(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}, domain_schemas=_domain_specs()))
    columns = {
        "demo_prmt_db.demo_prmt_combine_promotion": [("id", "bigint", "NO", "PRI", None, "")],
        "demo_store_db.demo_store_profile": [
            ("id", "bigint", "NO", "PRI", None, ""),
            ("store_code", "varchar", "YES", "", None, ""),
        ],
    }
    row = {
        "demo_prmt_db.demo_prmt_combine_promotion": (87,),
        "demo_store_db.demo_store_profile": ("S001",),
    }
    conn = _FakeConn(
        columns,
        row,
        discover_rows=[
            ("demo_prmt_db", "demo_prmt_combine_promotion", "id"),
            ("demo_prmt_db", "demo_prmt_monthly_promotion", "store_code"),
            ("demo_store_db", "demo_store_profile", "store_code"),
        ],
    )
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)
    result = probe_db_params(
        "/demo/combine/promotionInfo",
        ["id", "storeCode"],
        description="获取3S组合活动详情",
        param_remarks={"id": "活动id", "storeCode": "云商微店门店编码"},
    )
    assert result is not None
    assert result["table"] == "demo_prmt_db.demo_prmt_combine_promotion"
    assert result["values"]["id"] == {
        "value": 87,
        "remark": "示例值来自 demo_prmt_db.demo_prmt_combine_promotion.id",
    }
    assert result["values"]["storeCode"] == {
        "value": "S001",
        "remark": "示例值来自 demo_store_db.demo_store_profile.store_code",
    }
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理


# ==================== 值序列化与消费端提取测试 ====================


@pytest.mark.parametrize("value,expected", [
    pytest.param(None, None, id="None原样"),
    pytest.param(123, 123, id="整数原样"),
    pytest.param("text", "text", id="字符串原样"),
    pytest.param(True, True, id="布尔原样"),
    pytest.param([1, 2], [1, 2], id="列表原样"),
    pytest.param({"a": 1}, {"a": 1}, id="字典原样"),
    pytest.param(datetime(2026, 1, 1, 12, 0, 0), "2026-01-01 12:00:00", id="datetime转字符串"),
    pytest.param(Decimal("3.14"), "3.14", id="Decimal转字符串"),
])
@allure.feature("数据库参数探测")
@allure.story("值序列化")
@allure.title("测试 datetime/Decimal 转为字符串、基本类型原样返回")
def test_to_jsonable_forms(value, expected):
    assert _to_jsonable(value) == expected


@pytest.mark.parametrize("db_params,expected", [
    pytest.param({
        "table": "demo_db.demo_table",
        "values": {
            "id": {"value": 9001, "remark": "示例值来自 demo_db.demo_table.id"},
            "remark": "short form",
            "skip_none": {"value": None},
            "skip_entry": None,
        },
    }, {"id": 9001, "remark": "short form"}, id="dict与简写提取且None过滤"),
    pytest.param(None, {}, id="None返回空字典"),
    pytest.param({}, {}, id="空字典返回空字典"),
])
@allure.feature("数据库参数探测")
@allure.story("消费端提取")
@allure.title("测试从 db_params 提取参数值（dict/简写/None 过滤）")
def test_extract_db_values_forms(db_params, expected):
    assert extract_db_values(db_params) == expected


# ==================== 不冲突值生成测试 ====================


@pytest.mark.parametrize("func,description,url,expected", [
    pytest.param(_is_create_api, "新增敏感词", "/demo/save", True, id="描述新增认create"),
    pytest.param(_is_create_api, "", "/demo/addRecord", True, id="URL_add认create"),
    pytest.param(_is_create_api, "查询列表", "/demo/query", False, id="查询不认create"),
    pytest.param(_is_edit_api, "编辑记录", "/demo/update", True, id="描述编辑认edit"),
    pytest.param(_is_edit_api, "新增记录", "/demo/save", False, id="新增不认edit"),
    # URL 词元与描述侧对齐：create 认新增、modify/update 认编辑（save 过泛不认）
    pytest.param(_is_create_api, "", "/demo/createRecord", True, id="URL_create认create"),
    pytest.param(_is_edit_api, "", "/demo/modifyRecord", True, id="URL_modify认edit"),
    pytest.param(_is_edit_api, "", "/demo/updateRecord", True, id="URL_update认edit"),
    pytest.param(_is_create_api, "", "/demo/saveRecord", False, id="URL_save过泛不认"),
])
@allure.feature("数据库参数探测")
@allure.story("不冲突值生成")
@allure.title("测试接口新增/编辑语义识别（描述与 URL 关键词）")
def test_is_create_and_edit_api_forms(func, description, url, expected):
    assert func(description, url) is expected


@allure.feature("数据库参数探测")
@allure.story("不冲突值生成")
@allure.title("测试不冲突值生成（数值 MAX+1、字符串加随机后缀）")
def test_fresh_value():
    conn = _FakeConn([], None, max_row=(50,))
    cur = conn.cursor()
    # 数值列：MAX+1
    assert _fresh_value(cur, "demo_db.demo_table", "id", "bigint", 50) == 51
    # 字符串列：加随机后缀，不查 MAX
    fresh_str = _fresh_value(cur, "demo_db.demo_table", "demo_name", "varchar", "决赛")
    assert fresh_str.startswith("决赛_t")
    assert len(fresh_str) == len("决赛_t") + 6
    # 空示例值：仅随机后缀
    assert _fresh_value(cur, "demo_db.demo_table", "demo_name", "varchar", None).startswith("t")


@allure.feature("数据库参数探测")
@allure.story("不冲突值生成")
@allure.title("测试 DECIMAL 列 MAX+1 转 JSON 可序列化字符串（不报 TypeError）")
def test_fresh_value_decimal_jsonable():
    conn = _FakeConn([], None, max_row=(Decimal("3.14"),))
    cur = conn.cursor()
    # DECIMAL 列的 MAX 是 decimal.Decimal，+1 后须过 _to_jsonable 转字符串，
    # 否则 api.json 的 json.dump（无 default=）抛 TypeError 中断该接口生成
    assert _fresh_value(cur, "demo_db.demo_table", "amount", "decimal", Decimal("3.14")) == "4.14"


# ==================== 探测主流程测试 ====================


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试探测成功返回 db_params（含 where 过滤与主键倒序 SQL）")
def test_probe_db_params_success(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/save": {"table": "demo_db.demo_table", "where": "status = 0"}}),
    )
    columns = [
        ("id", "bigint", "NO", "PRI", None, ""),
        ("demo_visit_remark", "varchar", "YES", "", None, ""),
    ]
    row = (9001, "顾客已回访")
    conn = _FakeConn(columns, row)
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params("/demo/save", ["id", "demoVisitRemark"])

    assert result is not None
    assert result["table"] == "demo_db.demo_table"
    assert result["values"]["id"] == {
        "value": 9001,
        "remark": "示例值来自 demo_db.demo_table.id（status = 0）",
    }
    assert result["values"]["demoVisitRemark"]["value"] == "顾客已回访"
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理
    # SELECT 带 WHERE 过滤、主键倒序、LIMIT 1（排除快照的 information_schema 查询）
    select_sql = [s for s in conn._cursor.sqls if s.startswith("SELECT") and "information_schema" not in s][0]
    assert "WHERE status = 0" in select_sql
    assert "ORDER BY `id` DESC" in select_sql


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试 api_table_map 未命中时自动找表并探测成功")
def test_probe_db_params_auto_discover(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    columns = [
        ("id", "bigint", "NO", "PRI", None, ""),
        ("self_code", "varchar", "YES", "", None, ""),
    ]
    # SELECT 只查询 self_code 一列，fetchone 返回单元素元组
    row = ("DEMO-CODE-1",)
    conn = _FakeConn(
        columns,
        row,
        discover_rows=[("demo_db", "demo_experience_center", "self_code")],
    )
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params("/demo/center/query", ["selfCode"])

    assert result is not None
    assert result["table"] == "demo_db.demo_experience_center"
    assert result["values"]["selfCode"] == {
        "value": "DEMO-CODE-1",
        "remark": "示例值来自 demo_db.demo_experience_center.self_code",
    }
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理
    # 先反查 information_schema，再走常规探测：DESCRIBE + SELECT（无 where）
    sqls = conn._cursor.sqls
    assert any("information_schema" in s for s in sqls)
    select_sql = [s for s in sqls if s.startswith("SELECT") and "information_schema" not in s][0]
    assert "FROM `demo_db`.`demo_experience_center`" in select_sql
    assert "WHERE" not in select_sql
    assert "ORDER BY `id` DESC" in select_sql
    assert select_sql.endswith("LIMIT 1")


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试无映射/连接失败/无匹配字段/无示例行时返回 None")
def test_probe_db_params_skip_paths(monkeypatch):
    # 无 api_table_map 映射 → 自动找表（id 属通用列无候选）→ None
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn([], None, discover_rows=[("demo_db", "demo_table", "id")])
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)
    assert probe_db_params("/demo/save", ["id"]) is None
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理
    # 数据库连接失败
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/save": "demo_db.demo_table"}),
    )
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: None)
    assert probe_db_params("/demo/save", ["id"]) is None
    # 参数未匹配任何表字段
    conn = _FakeConn([("name", "varchar", "YES", "", None, "")], ("demo",))
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)
    assert probe_db_params("/demo/save", ["id"]) is None
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理
    # 表无示例行
    conn = _FakeConn([("id", "bigint", "NO", "PRI", None, "")], None)
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)
    assert probe_db_params("/demo/save", ["id"]) is None
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试新增接口生成不冲突值（数值 MAX+1、字符串加后缀、数组包装）")
def test_probe_db_params_create_fresh(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/save": "demo_db.demo_table"}),
    )
    columns = [
        ("id", "bigint", "NO", "PRI", None, ""),
        ("demo_name", "varchar", "YES", "", None, ""),
    ]
    row = (50, "决赛")
    conn = _FakeConn(columns, row, max_row=(50,))
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params(
        "/demo/save",
        ["id", "demoName"],
        description="新增记录",
        declared_values={"id": 0, "demoName": "", "tags": []},
    )

    assert result is not None
    assert result["values"]["id"]["value"] == 51  # MAX(id)=50 → 51
    assert result["values"]["demoName"]["value"].startswith("决赛_t")
    assert "不冲突值" in result["values"]["demoName"]["remark"]


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试编辑接口主键取已有值、唯一索引列生成不冲突值")
def test_probe_db_params_edit_unique(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/update": "demo_db.demo_table"}),
    )
    columns = [
        ("id", "bigint", "NO", "PRI", None, ""),
        ("demo_code", "varchar", "YES", "UNI", None, ""),
        ("demo_remark", "varchar", "YES", "", None, ""),
    ]
    row = (9001, "CODE-1", "备注")
    conn = _FakeConn(columns, row)
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params("/demo/update", ["id", "demoCode", "demoRemark"], description="编辑记录")

    assert result is not None
    # 主键保持已有值（编辑必须指向已存在记录）
    assert result["values"]["id"]["value"] == 9001
    assert result["values"]["demoCode"]["value"].startswith("CODE-1_t")
    assert result["values"]["demoRemark"]["value"] == "备注"


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试普通查询接口唯一索引列仍取已有值")
def test_probe_db_params_query_keeps_existing(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/member/query": "demo_db.demo_member_info"}),
    )
    columns = [
        ("id", "bigint", "NO", "PRI", None, ""),
        ("card_no", "varchar", "YES", "UNI", None, ""),
    ]
    # _fetch_sample_row 只 SELECT card_no 一列，示例行须为单元素元组
    row = ("CARD-0001",)
    conn = _FakeConn(columns, row)
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params("/demo/member/query", ["cardNo"], description="查询顾客可参加的活动")

    assert result is not None
    # 查询接口传新值会查空：唯一索引列也取库中已有值
    assert result["values"]["cardNo"]["value"] == "CARD-0001"


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试有枚举声明的参数直接取首个枚举值不查库")
def test_probe_db_params_enum_value(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    connect_calls: list = []

    def _spy_connect(cfg):
        connect_calls.append(cfg)
        return _FakeConn([], None)

    monkeypatch.setattr(db_probe, "_connect", _spy_connect)

    result = probe_db_params(
        "/demo/active/getPromotionProductInfo",
        ["platform"],
        enum_values={"platform": 1},
    )

    assert result is not None
    # 纯枚举参数：枚举提取先于建连，根本不连库（table 为空串）
    assert result["table"] == ""
    assert result["values"]["platform"] == {
        "value": 1,
        "remark": "示例值来自接口参数枚举",
    }
    assert connect_calls == []


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试数组形声明的枚举参数包装为单元素列表")
def test_probe_db_params_enum_array_wrap(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: _FakeConn([], None))
    result = probe_db_params("/demo/query", ["ids"], declared_values={"ids": []}, enum_values={"ids": 5})
    assert result is not None
    # 与非枚举路径（_probe_group）一致：数组形声明的枚举参数包装为单元素列表
    assert result["values"]["ids"]["value"] == [5]


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试枚举+查库混合参数：枚举不查库、其余参数仍建连探测")
def test_probe_db_params_enum_mixed_connects(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/save": "demo_db.demo_table"}),
    )
    conn = _FakeConn([("id", "bigint", "NO", "PRI", None, "")], (9001,))
    connect_calls: list = []

    def _spy_connect(cfg):
        connect_calls.append(cfg)
        return conn

    monkeypatch.setattr(db_probe, "_connect", _spy_connect)
    result = probe_db_params("/demo/save", ["id", "platform"], enum_values={"platform": 1})
    assert result is not None
    # 含非枚举参数 id → 仍需建连查库（与纯枚举接口不连库对照）
    assert len(connect_calls) == 1
    assert result["values"]["platform"]["value"] == 1
    assert result["values"]["id"]["value"] == 9001
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试跨表接口参数级独立找表（cardNo 会员主表、serialNo 产品主表）")
def test_probe_db_params_cross_table(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(
            api_table_map={},
            preferred_tables=["demo_db.demo_member_info", "demo_db.demo_product_product"],
        ),
    )
    # 多表 fake：columns/row 为 dict，按 SQL 中的表名分派
    columns = {
        "demo_db.demo_product_product": [
            ("id", "bigint", "NO", "PRI", None, ""),
            ("serial_no", "varchar", "YES", "UNI", None, ""),
        ],
        "demo_db.demo_member_info": [
            ("id", "bigint", "NO", "PRI", None, ""),
            ("card_no", "varchar", "YES", "UNI", None, ""),
        ],
    }
    row = {
        "demo_db.demo_product_product": ("SN-0001",),
        "demo_db.demo_member_info": ("CARD-0001",),
    }
    conn = _FakeConn(
        columns,
        row,
        discover_rows=[
            ("demo_db", "demo_member_info", "card_no"),
            ("demo_db", "demo_promotion", "card_no"),
            ("demo_db", "demo_promotion", "serial_no"),
            ("demo_db", "demo_product_product", "serial_no"),
        ],
        unique_rows=[
            ("demo_db", "demo_member_info", "card_no"),
            ("demo_db", "demo_product_product", "serial_no"),
        ],
    )
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params(
        "/demo/active/getPromotionProductInfo",
        ["cardNo", "serialNo", "platform"],
        enum_values={"platform": 1},
    )

    assert result is not None
    # 整接口先探测主表 product_product（serialNo 命中）；cardNo 不匹配后
    # 参数级独立找表命中 member_info：card_no 在会员主表是唯一索引、
    # 在活动表只是普通引用列，且参数级找表不罚表名多余词段
    assert result["table"] == "demo_db.demo_product_product"
    assert result["values"]["serialNo"] == {
        "value": "SN-0001",
        "remark": "示例值来自 demo_db.demo_product_product.serial_no",
    }
    assert result["values"]["cardNo"] == {
        "value": "CARD-0001",
        "remark": "示例值来自 demo_db.demo_member_info.card_no",
    }
    # platform 有枚举声明：直接取首个枚举值，不查库
    assert result["values"]["platform"] == {
        "value": 1,
        "remark": "示例值来自接口参数枚举",
    }
    assert conn.closed is False  # 连接复用契约：probe 不再逐次关闭，由 close_cached_connections 统一清理


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试复数参数匹配主键列且数组包装为单元素列表")
def test_probe_db_params_delete_ids_wrap(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/delete": "demo_db.demo_table"}),
    )
    columns = [("id", "bigint", "NO", "PRI", None, "")]
    row = (50,)
    conn = _FakeConn(columns, row)
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params(
        "/demo/delete",
        ["ids"],
        description="删除敏感词",
        declared_values={"ids": []},
    )

    assert result is not None
    # ids 去尾 s 匹配 id 主键列，已有值包装成数组
    assert result["values"]["ids"] == {
        "value": [50],
        "remark": "示例值来自 demo_db.demo_table.id",
    }


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试删除接口自动找表（表名匹配兜底）并探测主键数组值")
def test_probe_db_params_delete_ids_auto_fallback(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    columns = [("id", "bigint", "NO", "PRI", None, "")]
    row = (50,)
    conn = _FakeConn(
        columns,
        row,
        discover_rows=[("demo_db", "demo_invoice_sensitive", "id")],
    )
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params(
        "/demo/isensitive/mgmt/deleteInvoiceSensitive",
        ["ids"],
        description="删除敏感词",
        declared_values={"ids": []},
    )

    assert result is not None
    assert result["table"] == "demo_db.demo_invoice_sensitive"
    assert result["values"]["ids"]["value"] == [50]


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试带前缀列名的参数探测成功（子串包含兜底）")
def test_probe_db_params_prefixed_column(monkeypatch):
    _patch_db_config(
        monkeypatch,
        _fake_db_config(api_table_map={"/demo/feedback/commit": "demo_cms.demo_message"}),
    )
    columns = [
        ("id", "bigint", "NO", "PRI", None, ""),
        ("messagecontent", "varchar", "YES", "", None, ""),
    ]
    # SELECT 只查 messagecontent 一列，示例行须为单元素元组
    row = ("演示留言",)
    conn = _FakeConn(columns, row)
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)

    result = probe_db_params("/demo/feedback/commit", ["content"], description="提交反馈")

    assert result is not None
    assert result["values"]["content"] == {
        "value": "演示留言",
        "remark": "示例值来自 demo_cms.demo_message.messagecontent",
    }


@allure.feature("数据库参数探测")
@allure.story("示例行探测")
@allure.title("测试未配置 DB_CONFIG 时直接返回 None（不触发连接）")
def test_probe_db_params_without_db_config(monkeypatch):
    _patch_db_config(monkeypatch, None)
    assert probe_db_params("/demo/save", ["id"]) is None


# ==================== 连接与密码读取测试 ====================


@pytest.fixture
def fake_pymysql(monkeypatch):
    """注入伪造 pymysql 模块，记录 connect 收到的参数并返回伪造连接。"""
    connect_calls = []
    fake_conn = _FakeConn([], None)

    def fake_connect(**kwargs):
        connect_calls.append(kwargs)
        return fake_conn

    fake_module = types.ModuleType("pymysql")
    # ModuleType 实例属性是动态的，用 setattr 绕过静态类型检查（无法为未知属性赋值）
    setattr(fake_module, "connect", fake_connect)
    monkeypatch.setitem(sys.modules, "pymysql", fake_module)
    return connect_calls


@allure.feature("数据库参数探测")
@allure.story("数据库连接")
@allure.title("测试 password_env 填环境变量名时从环境变量读取密码")
def test_connect_password_from_env(monkeypatch, fake_pymysql):
    monkeypatch.setenv("TEST_DB_PWD", "secret_from_env")
    conn = _connect(
        {
            "host": "demo.mysql.example.com",
            "user": "tester",
            "password_env": "TEST_DB_PWD",
        }
    )
    assert conn is not None
    assert fake_pymysql[0]["password"] == "secret_from_env"


@allure.feature("数据库参数探测")
@allure.story("数据库连接")
@allure.title("测试 password_env 直接填密码明文时原样使用")
def test_connect_password_plaintext(monkeypatch, fake_pymysql):
    # 环境变量不存在 → 把 password_env 的值本身当密码
    monkeypatch.delenv("DEMO_PWD_PLAIN", raising=False)
    conn = _connect(
        {
            "host": "demo.mysql.example.com",
            "user": "tester",
            "password_env": "demo-plain-pwd-123",
        }
    )
    assert conn is not None
    assert fake_pymysql[0]["password"] == "demo-plain-pwd-123"


@allure.feature("数据库参数探测")
@allure.story("数据库连接")
@allure.title("测试未配置 password_env 时密码为空串")
def test_connect_password_missing(monkeypatch, fake_pymysql):
    conn = _connect({"host": "demo.mysql.example.com", "user": "tester"})
    assert conn is not None
    assert fake_pymysql[0]["password"] == ""


@allure.feature("数据库参数探测")
@allure.story("数据库连接")
@allure.title("测试连接失败熔断：TTL 内不重复尝试，标记清除后恢复")
def test_connect_failure_circuit_breaker(monkeypatch):
    calls: list = []

    def failing_connect(**kwargs):
        calls.append(kwargs)
        raise OSError("connect timeout")

    fake_module = types.ModuleType("pymysql")
    setattr(fake_module, "connect", failing_connect)
    monkeypatch.setitem(sys.modules, "pymysql", fake_module)
    cfg = {"host": "demo.mysql.example.com", "user": "tester", "password_env": ""}
    assert _connect(cfg) is None
    # 熔断期内后续调用直接返回 None，不再吃 connect_timeout
    assert _connect(cfg) is None
    assert len(calls) == 1
    # 熔断标记清除后恢复尝试
    db_probe._connect_failed_at = None
    assert _connect(cfg) is None
    assert len(calls) == 2


@allure.feature("数据库参数探测")
@allure.story("数据库连接")
@allure.title("测试熔断期内短路不连接、过期后连接成功清除标记")
def test_connect_success_clears_breaker(monkeypatch, fake_pymysql):
    now = db_probe.time.monotonic()
    monkeypatch.setattr(db_probe.time, "monotonic", lambda: now)
    db_probe._connect_failed_at = now  # 刚失败，处于熔断期
    cfg = {"host": "demo.mysql.example.com", "user": "tester", "password_env": ""}
    assert _connect(cfg) is None  # 熔断期内短路，即使驱动可用也不连
    assert fake_pymysql == []
    # 时间推进超过 TTL → 恢复尝试并成功 → 清除熔断标记
    monkeypatch.setattr(db_probe.time, "monotonic", lambda: now + db_probe._CONNECT_RETRY_TTL + 1)
    assert _connect(cfg) is not None
    assert db_probe._connect_failed_at is None
    assert len(fake_pymysql) == 1


# ==================== 批量性能优化测试 ====================


@allure.feature("数据库参数探测")
@allure.story("批量性能")
@allure.title("测试连接线程局部复用：同线程二次调用不再握手，ping 保活")
def test_connect_reuses_thread_local_connection(monkeypatch, fake_pymysql):
    cfg = {"host": "demo.mysql.example.com", "user": "tester", "password_env": ""}
    first = _connect(cfg)
    second = _connect(cfg)
    assert first is second
    # 只发生一次 TCP+认证握手，第二次走 ping 保活
    assert len(fake_pymysql) == 1
    assert first.ping_calls == 1


@allure.feature("数据库参数探测")
@allure.story("批量性能")
@allure.title("测试缓存连接 ping 失败时自动重建新连接")
def test_connect_reconnects_on_ping_failure(monkeypatch):
    class _PingFailConn(_FakeConn):
        def ping(self, reconnect=True):
            raise OSError("server has gone away")

    conns: list = []

    def fake_connect(**kwargs):
        conn = _PingFailConn([], None) if not conns else _FakeConn([], None)
        conns.append(conn)
        return conn

    fake_module = types.ModuleType("pymysql")
    setattr(fake_module, "connect", fake_connect)
    monkeypatch.setitem(sys.modules, "pymysql", fake_module)
    cfg = {"host": "demo.mysql.example.com", "user": "tester", "password_env": ""}
    first = _connect(cfg)
    second = _connect(cfg)
    assert first is not second
    assert len(conns) == 2


@allure.feature("数据库参数探测")
@allure.story("批量性能")
@allure.title("测试 close_cached_connections 统一关闭缓存连接并清空注册表")
def test_close_cached_connections(monkeypatch, fake_pymysql):
    cfg = {"host": "demo.mysql.example.com", "user": "tester", "password_env": ""}
    conn = _connect(cfg)
    assert conn.closed is False
    db_probe.close_cached_connections()
    assert conn.closed is True
    assert db_probe._cached_conns == []


@allure.feature("数据库参数探测")
@allure.story("批量性能")
@allure.title("测试 schema 快照跨接口只构建一次（元数据查询不随接口数增长）")
def test_schema_snapshot_built_once_across_probes(monkeypatch):
    _patch_db_config(monkeypatch, _fake_db_config(api_table_map={}))
    conn = _FakeConn(
        [],
        None,
        discover_rows=[
            ("demo_db", "demo_order", "self_code"),
            ("demo_db", "demo_member_info", "card_no"),
        ],
    )
    monkeypatch.setattr(db_probe, "_connect", lambda cfg: conn)
    probe_db_params("/demo/order/query", ["selfCode"])
    probe_db_params("/demo/member/query", ["cardNo"])
    # 两个接口共用同一快照：TABLES/COLUMNS/STATISTICS 各一次，不逐接口反查
    meta = [s for s in conn._cursor.sqls if "information_schema" in s]
    assert len(meta) == 3


@allure.feature("数据库参数探测")
@allure.story("批量性能")
@allure.title("测试表结构 DESCRIBE 缓存：同表二次读取不再发查询")
def test_table_columns_cached_across_calls():
    conn = _FakeConn([("id", "bigint", "NO", "PRI", None, "")], None)
    cur = conn.cursor()
    first = db_probe._table_columns(cur, "demo_db.demo_table")
    second = db_probe._table_columns(cur, "demo_db.demo_table")
    assert first == second
    describes = [s for s in cur.sqls if s.startswith("DESCRIBE")]
    assert len(describes) == 1
