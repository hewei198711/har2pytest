"""complex_scenario 步骤取值处理模块。

分析 HAR 请求序列，为每个步骤的参数计算取值来源：

- ``step_response``：值来自前序步骤的响应，生成
  ``test_data['步骤键']['json_path']`` 引用表达式；
- ``container_projection``：容器参数（dict/list）与响应某子结构部分一致时，
  逐字段生成引用表达式，不一致的字段同名同值（全用例唯一）时写入
  用例级 test_data 集中修改，否则保留 HAR 录制值字面量（如商品列表
  引用搜索响应，固定数量字段保持原值）；
- ``test_data``：用例级参数（未在前序响应中找到同名字段的同值叶子），
  生成 ``test_data['参数名']`` 引用，值统一放在测试方法顶部的
  ``test_data`` 初始化字典中，便于用户集中修改；
- ``collect_projection``：响应收集接口（COLLECT_RESPONSE_APIS 配置）的
  列表推导引用——list 参数元素与收集列表元素同字段对齐时渲染
  ``[i['字段名'] for i in test_data['collect_key']]``；
- ``literal``：空值或被忽略的参数，保持字面量原样输出。

取值规则：每个步骤的响应 ``data`` 字段压平保存为 ``路径 → 叶子值``；
每个步骤的传参在前序步骤的压平叶子中查找「字段名（不区分大小写）与值
均相同」的叶子 → 引用；未命中 → 写入用例级 test_data 并引用。容器参数
先按同名字段结构完全相等整体引用，再按字段级投影逐字段引用，纯叶子
列表参数按元素值唯一出现匹配。

响应存储：每个步骤的响应 ``data`` 一律整存（``test_data[步骤键] =
data['data']``），不做任何裁剪；dict 响应保留全部兄弟字段（如用户信息
对象的 memberOtherApps 之外字段），列表响应保留全部元素（如 App 绑定
列表的多个绑定记录）。引用时携带完整路径（如
``test_data['product_search']['list'][0]['serialNo']``）。

步骤键由 API 函数名按下划线分割取最后两个字段生成（如
``demo_api_field_value`` → ``field_value``），键冲突时
依次向前扩展字段直到唯一。

同时提供 ``test_data`` 初始化代码与步骤参数字典代码的渲染函数。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, replace
from typing import Any

from .config import APIConfig
from .logger import logger
from .models import ParsedRequestInfo
from .utils import format_parameter_value

# 响应数据扁平化的最大路径深度（避免深层结构导致组合爆炸）
_MAX_FLATTEN_DEPTH = 4
# 列表元素最多参与扁平化的数量（取值引用只可能用到靠前元素）
_MAX_LIST_ITEMS = 3
# 值匹配兜底的最小长度：数值型短值（如 "0"/"1"/"01"）不参与，避免同值异义
# 字段误引用（历史教训 sourceType=0 → favProFlag=0）；非数值（中文/字母）
# 仅需 2 字符即可参与兜底（短姓名/编码仍有区分度）
_VALUE_MATCH_MIN_LENGTH = 5
_TEXT_MATCH_MIN_LENGTH = 2


@dataclass
class ParamSource:
    """单个参数在某个步骤中的取值来源描述。"""

    kind: str  # "step_response" | "container_projection" | "collect_projection" | "json_projection" | "test_data" | "literal"
    param_name: str = ""  # 参数名（test_data 类来源时即 test_data 字典的键）
    step_key: str | None = None  # step_response/container_projection/collect_projection/json_projection 时的来源键
    path: tuple = ()  # step_response 时相对 data['data'] 的取值路径
    value: Any = None  # 字面量或 HAR 录制值
    projection: Any = None  # container_projection 时的投影树；collect_projection 时为字段名字符串；json_projection 时为请求键 → ("ref",路径)/("literal",值) 的有序字典
    note: str | None = None  # test_data 来源时附加到生成代码行尾的注释提示（如值多处出现未自动引用）


@dataclass
class StepValueContext:
    """单个步骤的取值上下文。"""

    step_key: str  # test_data 中该步骤响应数据的键
    param_sources: dict[str, ParamSource] = field(default_factory=dict)  # 参数名 → 来源
    flattened: dict[tuple[Any, ...], Any] = field(default_factory=dict)  # 响应 data 压平叶子 路径 → 值
    container_index: dict[tuple[Any, ...], Any] = field(default_factory=dict)  # 路径 → 容器（投影匹配候选）
    store_response: bool = True  # 响应是否被后续步骤引用（未引用则不生成存储行）
    collect: dict | None = None  # 响应收集接口配置（COLLECT_RESPONSE_APIS 命中项）
    response_data: Any = None  # 响应 data 原文（响应收集接口匹配用）


@dataclass
class ScenarioValuePlan:
    """整个场景的取值计划。"""

    steps: list[StepValueContext] = field(default_factory=list)
    test_data_values: dict[str, Any] = field(default_factory=dict)  # 用例级参数名 → 值


def make_step_key(api_function_name: str, used_keys: set[str]) -> str:
    """根据 API 函数名生成 test_data 步骤键。

    取函数名下划线分割后的最后两个字段（如 ``demo_api_field_value``
    → ``field_value``），字段不足两个时保留全名；键冲突时依次向前
    扩展字段直到唯一。
    """
    parts = api_function_name.split("_")
    for n in range(2, len(parts) + 1):
        key = "_".join(parts[-n:])
        if key not in used_keys:
            used_keys.add(key)
            return key
    # 全名仍冲突的兜底（API 文件名唯一，理论上不会发生）
    key = api_function_name
    used_keys.add(key)
    return key


def find_collect_config(url: str) -> dict | None:
    """返回 url 命中的响应收集接口配置（COLLECT_RESPONSE_APIS 子串匹配）。

    Args:
        url: HAR 请求 URL。

    Returns:
        命中的配置字典（含 url/collect_key 等键）；无命中或配置缺 collect_key
        时返回 None。
    """
    for cfg in APIConfig.COLLECT_RESPONSE_APIS():
        if not isinstance(cfg, dict):
            continue
        cfg_url = cfg.get("url")
        if not cfg_url or not cfg.get("collect_key"):
            continue
        if cfg_url in url:
            return cfg
    return None


def collect_append_path(cfg: dict) -> list:
    """返回响应收集配置的 append 路径（未配置时默认 ["datas"]）。"""
    return cfg.get("append_path") or ["datas"]


def collect_file_field(cfg: dict) -> str:
    """返回响应收集配置的文件字段名（未配置时默认 "file"）。"""
    return cfg.get("file_field") or "file"


def flatten_data(data: Any, max_depth: int = _MAX_FLATTEN_DEPTH) -> dict[tuple[Any, ...], Any]:
    """把响应 ``data`` 字段展平为 ``路径 tuple → 叶子值`` 的映射。

    dict 键与 list 索引按顺序拼接进路径：``{"list": [{"k": 1}]}`` 展平为
    ``("list", 0, "k") → 1``。路径长度达到 ``max_depth`` 的 dict/list 不再展开。
    """
    result: dict[tuple[Any, ...], Any] = {}

    def walk(node: Any, path: tuple) -> None:
        if isinstance(node, dict):
            if len(path) >= max_depth:
                return
            for key, value in node.items():
                walk(value, path + (key,))
        elif isinstance(node, list):
            if len(path) >= max_depth:
                return
            for idx, item in enumerate(node[:_MAX_LIST_ITEMS]):
                walk(item, path + (idx,))
        else:
            result[path] = node

    walk(data, ())
    return result


def _canonical_key(value: Any) -> str:
    """把值规范化为索引键：容器用键排序后的 JSON，叶子用 ``str(value)``。

    容器（dict/list）参与匹配时需要结构级比较，键顺序无关（``{"a": 1,
    "b": 2}`` 与 ``{"b": 2, "a": 1}`` 视为同一结构）；叶子保持原有
    ``str()`` 语义，兼容既有索引行为。
    """
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return str(value)


def _flatten_containers(data: Any, max_depth: int = _MAX_FLATTEN_DEPTH) -> dict[tuple[Any, ...], Any]:
    """把响应 ``data`` 字段中所有非空 dict/list 容器索引为 ``路径 → 容器``。

    与 :func:`flatten_data` 互补：后者只记录叶子值，复杂请求参数（如商品
    列表）无法匹配；本函数额外记录每个容器节点本身，使「请求参数与响应中
    某子结构完全相等」时可以建立 step_response 引用。空容器不索引（无引用
    价值），深度与列表元素数与叶子展平一致。
    """
    result: dict[tuple[Any, ...], Any] = {}

    def walk(node: Any, path: tuple) -> None:
        if isinstance(node, dict):
            if node:  # 空 dict 不索引
                result[path] = node
            if len(path) >= max_depth:
                return
            for key, value in node.items():
                walk(value, path + (key,))
        elif isinstance(node, list):
            if node:  # 空 list 不索引
                result[path] = node
            if len(path) >= max_depth:
                return
            for idx, item in enumerate(node[:_MAX_LIST_ITEMS]):
                walk(item, path + (idx,))

    walk(data, ())
    return result


def _response_data(response_content: Any) -> Any:
    """提取响应 JSON 的 ``data`` 字段；无法解析时返回 None。"""
    if not isinstance(response_content, dict):
        return None
    return response_content.get("data")


def _field_matches(path: tuple, name: str) -> bool:
    """路径末段是字段名且与参数名不区分大小写一致。"""
    return bool(path) and isinstance(path[-1], str) and path[-1].lower() == name.lower()


def _value_paths(flattened: dict, key: str) -> list[tuple]:
    """压平索引中值（str 归一）等于 key 的全部叶子路径。"""
    return [path for path, value in flattened.items() if str(value) == key]


_NUMERIC_TEXT_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")


def _value_match_eligible(key: str) -> bool:
    """值匹配兜底的门槛：数值型需 ≥5 字符（短数字码同值异义风险高），
    非数值（中文/字母）≥2 字符即可参与。"""
    if _NUMERIC_TEXT_PATTERN.fullmatch(key):
        return len(key) >= _VALUE_MATCH_MIN_LENGTH
    return len(key) >= _TEXT_MATCH_MIN_LENGTH


def _ambiguity_note(step_key: str, paths: list[tuple]) -> str:
    """同值在前序响应中多处出现时的生成注释（列候选路径供手工改引用）。

    ``paths`` 为该值出现的全部叶子路径（如 ``("order", "customerPhone")``），
    注释只展示前 3 条，其余以"等 N 处"概括，避免行尾过长。
    """
    shown = "、".join("/".join(str(seg) for seg in path) for path in paths[:3])
    if len(paths) > 3:
        shown += f" 等{len(paths)}处"
    else:
        shown += f" 共{len(paths)}处"
    return f"值在前序响应 {step_key} 中出现 {shown}，未自动引用，可手工改为引用"


def _find_json_projection(
    name: str, key: str, previous_indexes: list[StepValueContext]
) -> ParamSource | None:
    """JSON 对象字符串参数与前序响应字段的跨形态子集投影。

    请求值为合法 JSON 对象字符串且非空叶子数 ≥2（单叶子场景普通值兜底
    已覆盖）时，若所有非空叶子值均在前序同一步骤的压平索引中同值命中
    （完备子集，null/空串键保持字面量不参与匹配），且命中来源步骤键唯一
    （同一 API 多次调用共享同一步骤键视为同一来源），则命中：渲染时以
    json.dumps 把响应字段重组回字符串，保持接口声明的 string 形态
    （如 senderAddress 请求 JSON 串 ↔ getPendingWarehouseByCompanyCode
    扁平仓库对象）。

    不命中：非 JSON 对象字符串、叶子缺失（部分命中）、多个不同步骤键的
    响应均包含全量叶子（歧义候选）。
    """
    try:
        parsed = json.loads(key)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(parsed, dict) or not parsed:
        return None
    leaves = {
        k: str(v) for k, v in parsed.items() if v is not None and v != ""
    }
    if len(leaves) < 2:
        return None
    hit_keys: dict[str, dict] = {}  # 步骤键 → 请求键到响应路径的映射
    for prev in previous_indexes:
        ref_map: dict[str, tuple] | None = {}
        for k, v in leaves.items():
            paths = _value_paths(prev.flattened, v)
            if not paths:
                ref_map = None
                break
            ref_map[k] = paths[0]
        if ref_map is not None and prev.step_key not in hit_keys:
            hit_keys[prev.step_key] = ref_map
    if len(hit_keys) != 1:
        return None
    step_key, ref_map = next(iter(hit_keys.items()))
    # 按请求 JSON 原键序构造投影：命中键引用响应路径，null/空串键保持字面量
    projection = {
        k: (("ref", ref_map[k]) if k in leaves else ("literal", v))
        for k, v in parsed.items()
    }
    return ParamSource(
        kind="json_projection",
        param_name=name,
        step_key=step_key,
        value=key,
        projection=projection,
    )


def _collect_request_params(request_info: ParsedRequestInfo) -> dict[str, Any]:
    """收集单个请求的全部参数（路径、query 与 post body，后者优先）。"""
    path = request_info.path_params or {}
    query = request_info.query_params or {}
    post = request_info.post_data or {}
    if isinstance(query, dict) and isinstance(post, dict):
        return {**path, **query, **post}
    if isinstance(post, dict):
        return {**path, **post}
    return {**path, **query}


def build_scenario_value_plan(
    requests: list[ParsedRequestInfo],
    step_keys: list[str],
) -> ScenarioValuePlan:
    """分析请求序列，产出场景取值计划。

    Args:
        requests: 按执行顺序排列的请求信息（与生成的步骤函数一一对应）。
        step_keys: 各步骤在 test_data 中的键（顺序与 requests 一致）。

    Returns:
        ScenarioValuePlan：包含各步骤参数取值来源与用例级 test_data 值。
    """
    plan = ScenarioValuePlan()
    track_enabled = APIConfig.TRACK_PARAM_SOURCES()
    ignore_keys = {k.lower() for k in APIConfig.PARAM_SOURCE_IGNORE_KEYS()}

    # 前序步骤的取值上下文（按顺序累积，后面的步骤只能引用前面的响应）
    previous_indexes: list[StepValueContext] = []
    # 响应收集接口的文件参数值列表（collect_key → 值列表）与对应 files_key
    collect_files: dict[str, list] = {}
    collect_files_keys: dict[str, str] = {}

    for request_info, step_key in zip(requests, step_keys):
        step_ctx = StepValueContext(step_key=step_key)
        collect_cfg = find_collect_config(request_info.url) if track_enabled else None
        step_ctx.collect = collect_cfg
        if track_enabled:
            if collect_cfg is not None:
                # 响应收集接口：append 行相对整个响应 JSON 取值（如 data['datas']），
                # 保留响应原文供 collect 投影匹配；不建叶子/容器索引，
                # 避免普通匹配产生指向未整存响应的悬空引用
                if isinstance(request_info.response_content, dict):
                    step_ctx.response_data = request_info.response_content
            else:
                data = _response_data(request_info.response_content)
                if data is not None:
                    step_ctx.response_data = data
                    step_ctx.flattened = flatten_data(data)
                    step_ctx.container_index = _flatten_containers(data)
            for name, value in _collect_request_params(request_info).items():
                if collect_cfg is not None and name == collect_file_field(collect_cfg):
                    # 文件字段不进 test_data，改由循环形参逐次传入；
                    # 值收集进 files 列表（数量与接口调用次数一致）
                    collect_key = collect_cfg["collect_key"]
                    if collect_key not in collect_files:
                        collect_files[collect_key] = []
                        collect_files_keys[collect_key] = collect_cfg.get("files_key") or "files"
                    collect_files[collect_key].append(value)
                    continue
                step_ctx.param_sources[name] = _resolve_param_source(
                    name, value, ignore_keys, previous_indexes
                )
        plan.steps.append(step_ctx)
        previous_indexes.append(step_ctx)

    if not track_enabled:
        return plan

    # 汇总用例级参数（同名不同值的冲突保留首个，仅记录日志）
    for step_ctx in plan.steps:
        for name, source in step_ctx.param_sources.items():
            if source.kind != "test_data":
                continue
            if name in plan.test_data_values and plan.test_data_values[name] != source.value:
                logger.debug(f"[步骤取值] 用例级参数 {name} 在不同步骤值不一致，保留首个值")
                continue
            plan.test_data_values[name] = source.value

    # 响应收集接口的用例级键：收集列表（初始为空）与文件值列表
    for collect_key, files in collect_files.items():
        files_key = collect_files_keys[collect_key]
        plan.test_data_values.setdefault(collect_key, [])
        if files_key in plan.test_data_values and plan.test_data_values[files_key] != files:
            logger.debug(f"[步骤取值] 用例级参数 {files_key} 与响应收集文件列表冲突，保留原值")
        else:
            plan.test_data_values[files_key] = files

    # 投影字面量叶子同名同值提升为 test_data 引用（见函数 docstring）
    _promote_projection_literals(plan)

    # 只存储被后续步骤引用的响应：未被引用的步骤不生成存储行，
    # 避免大量无用响应（如埋点/校验接口）常驻 test_data 占用内存
    referenced_keys = {
        source.step_key
        for step_ctx in plan.steps
        for source in step_ctx.param_sources.values()
        if source.kind in ("step_response", "container_projection", "json_projection")
        and source.step_key is not None
    }
    for step_ctx in plan.steps:
        if step_ctx.collect is not None:
            # 响应收集接口不整存响应，改由渲染侧追加收集片段
            step_ctx.store_response = False
        else:
            step_ctx.store_response = step_ctx.step_key in referenced_keys

    return plan


def _collect_field_values(value: Any) -> dict[str, list[Any]]:
    """递归收集参数值中字段名 → 出现值列表（含嵌套容器）。"""
    fields: dict[str, list[Any]] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            fields.setdefault(key, []).append(item)
            for sub_key, sub_values in _collect_field_values(item).items():
                fields.setdefault(sub_key, []).extend(sub_values)
    elif isinstance(value, list):
        for item in value:
            for sub_key, sub_values in _collect_field_values(item).items():
                fields.setdefault(sub_key, []).extend(sub_values)
    return fields


def _promote_projection_literals(plan: ScenarioValuePlan) -> None:
    """投影字面量叶子同名同值提升为 test_data 引用。

    容器投影中与响应不一致的字段默认渲染字面量；若该字段名在全用例
    参数中值唯一（同名同值，如购买数量 quantity=1 出现在多个步骤），
    改为写入用例级 test_data 并引用，便于用户集中修改；值不一致时
    保持字面量（test_data 键冲突无法表达多个值，如 number 在不同步骤
    为 19 与 1）。空值叶子不提升。
    """
    field_values: dict[str, set[str]] = {}
    for step_ctx in plan.steps:
        for source in step_ctx.param_sources.values():
            for key, values in _collect_field_values(source.value).items():
                field_values.setdefault(key, set()).update(
                    _canonical_key(v) for v in values
                )

    def _walk(node: Any, key: str | None) -> Any:
        if isinstance(node, dict):
            for child_key, child in node.items():
                node[child_key] = _walk(child, child_key)
            return node
        if isinstance(node, list):
            # 列表内元素无字段名语义（dict 元素由自身分支确定键），
            # 避免字面量元素误用列表字段名参与提升判定
            return [_walk(item, None) for item in node]
        kind, payload = node
        if kind != "literal" or key is None:
            return node
        if payload is None or payload == "" or isinstance(payload, (dict, list)):
            return node
        if len(field_values.get(key, ())) != 1:
            return node
        if key in plan.test_data_values and (
            _canonical_key(plan.test_data_values[key]) != _canonical_key(payload)
        ):
            return node  # 与顶层用例级参数同名不同值，保持字面量
        plan.test_data_values[key] = payload
        return ("test_data", key)

    for step_ctx in plan.steps:
        for source in step_ctx.param_sources.values():
            if source.kind == "container_projection" and source.projection is not None:
                source.projection = _walk(source.projection, None)


def _leaf_equal(a: Any, b: Any) -> bool:
    """叶子相等判定：两者均非容器且值相等（200 == 200.0 成立）。"""
    if isinstance(a, (dict, list)) or isinstance(b, (dict, list)):
        return False
    return a == b


def _count_leaves(node: Any) -> int:
    """统计容器中的叶子（非 dict/list）数量，作为投影匹配度分母。"""
    if isinstance(node, dict):
        return sum(_count_leaves(v) for v in node.values())
    if isinstance(node, list):
        return sum(_count_leaves(i) for i in node)
    return 1


def _projection_tree(req: Any, resp: Any, resp_path: tuple) -> tuple[int, Any]:
    """递归构建请求值 ``req`` 相对响应值 ``resp`` 的字段级投影树。

    dict 按字段名（不区分大小写）对齐、list 按索引对齐：叶子相等
    （:func:`_leaf_equal`）时记为引用（``("ref", 路径)``），嵌套容器递归
    投影；其余记为字面量（``("literal", 值)``）。返回（引用字段数, 投影树）。
    """
    if isinstance(req, dict) and isinstance(resp, dict):
        score = 0
        tree = {}
        resp_keys = {k.lower(): k for k in resp}
        for key, rv in req.items():
            resp_key = resp_keys.get(key.lower())
            if resp_key is None:
                tree[key] = ("literal", rv)
                continue
            sv = resp[resp_key]
            if isinstance(rv, (dict, list)) and isinstance(sv, (dict, list)):
                sub_score, sub_tree = _projection_tree(rv, sv, resp_path + (resp_key,))
                if sub_score > 0:
                    score += sub_score
                    tree[key] = sub_tree
                else:
                    tree[key] = ("literal", rv)
            elif _leaf_equal(rv, sv):
                score += 1
                tree[key] = ("ref", resp_path + (resp_key,))
            else:
                tree[key] = ("literal", rv)
        return score, tree
    if isinstance(req, list) and isinstance(resp, list):
        score = 0
        items = []
        for idx, (rv, sv) in enumerate(zip(req, resp)):
            if isinstance(rv, (dict, list)) and isinstance(sv, (dict, list)):
                sub_score, sub_tree = _projection_tree(rv, sv, resp_path + (idx,))
                if sub_score > 0:
                    score += sub_score
                    items.append(sub_tree)
                else:
                    items.append(("literal", rv))
            elif _leaf_equal(rv, sv):
                score += 1
                items.append(("ref", resp_path + (idx,)))
            else:
                items.append(("literal", rv))
        # 响应列表更短时，多余元素保持字面量
        items.extend(("literal", rv) for rv in req[len(resp):])
        return score, items
    return 0, ("literal", req)


def _find_projection(
    value: Any,
    previous_indexes: list[StepValueContext],
) -> tuple[StepValueContext, tuple, Any] | None:
    """为容器参数寻找最佳字段级投影候选。

    遍历前序步骤响应索引中的所有容器，计算投影匹配分数（相等字段数），
    选择分数最高者；要求至少一半请求叶子可匹配（弱匹配保持 test_data
    集中管理，不拆散到步骤代码中）。并列时取更早步骤、更浅路径。

    Returns:
        (来源步骤上下文, 响应容器路径, 投影树)；无合格候选返回 None。
    """
    leaves = _count_leaves(value)
    if leaves == 0:
        return None
    best: tuple[int, int, int, StepValueContext, tuple, Any] | None = None
    for order, prev in enumerate(previous_indexes):
        for resp_path, resp_value in prev.container_index.items():
            score, tree = _projection_tree(value, resp_value, resp_path)
            if score * 2 < leaves:
                continue
            candidate = (score, -order, -len(resp_path), prev, resp_path, tree)
            if best is None or candidate[:3] > best[:3]:
                best = candidate
    if best is None:
        return None
    return best[3], best[4], best[5]


def _find_list_leaf_projection(
    value: list,
    previous_indexes: list[StepValueContext],
) -> tuple[StepValueContext, Any] | None:
    """为纯叶子列表参数寻找元素级引用投影（如 ``["AMT"]``）。

    列表每个元素为叶子时，若其值在前序步骤响应叶子索引中唯一出现（避免
    "1"/"0" 等高频短值误引用），记为引用；容器元素尝试字段级投影。所有
    引用元素必须来自同一步骤（渲染只支持单一步骤键），且引用叶子比例
    不低于一半，否则返回 None 保持 test_data 集中管理。
    """
    leaves = _count_leaves(value)
    if leaves == 0:
        return None
    ref_step: StepValueContext | None = None
    score = 0
    tree: list = []
    for item in value:
        if isinstance(item, (dict, list)):
            sub = _find_projection(item, previous_indexes)
            if sub is not None:
                prev, _resp_path, sub_tree = sub
                if ref_step is None:
                    ref_step = prev
                if prev is not ref_step:
                    return None
                score += _count_leaves(item)
                tree.append(sub_tree)
            else:
                tree.append(("literal", item))
            continue
        matched = False
        for prev in previous_indexes:
            # 唯一性判定基于完整响应压平，避免同值多处出现误引用
            paths = _value_paths(prev.flattened, str(item))
            if len(paths) != 1:
                continue
            path = paths[0]
            if ref_step is None:
                ref_step = prev
            if prev is not ref_step:
                return None
            score += 1
            tree.append(("ref", path))
            matched = True
            break
        if not matched:
            tree.append(("literal", item))
    if ref_step is None or score * 2 < leaves:
        return None
    return ref_step, tree


def _resolve_param_source(
    name: str,
    value: Any,
    ignore_keys: set[str],
    previous_indexes: list[StepValueContext],
) -> ParamSource:
    """判定单个参数的取值来源。

    规则：空值 → literal；忽略名单 → literal；前序步骤同名参数同值 → 复用
    第一个步骤的取值来源（相同接口请求保持一致，如第二次调用的 usrId
    沿用 test_data['usrId']）；叶子参数在前序步骤的压平响应叶子中找到
    「字段名（不区分大小写）与值（str 归一）均相同」的叶子 → step_response
    （取最早步骤）；字段名未命中时按值匹配兜底——数值型值 5 字符以上、
    非数值（中文/字母）2 字符以上，且在前序响应中单步骤唯一出现 →
    step_response 值匹配兜底（如 customerCard 引用响应 cardNo）；容器参数
    先按同名字段结构完全相等整体引用，再按字段级投影
    （至少一半叶子相等，相等字段引用响应路径、其余保持 HAR 录制值）
    → container_projection；纯叶子列表参数的元素在前序响应中唯一出现
    （且引用比例不低于一半）→ container_projection（元素级引用）；未命中
    → test_data 用例级（值写入 test_data 并引用）。
    """
    # 空值参数直接字面量输出（None/空字符串/空容器），不进入 test_data
    if value is None or value == "" or (
        isinstance(value, (dict, list, tuple)) and not value
    ):
        return ParamSource(kind="literal", param_name=name, value=value)
    if name.lower() in ignore_keys:
        return ParamSource(kind="literal", param_name=name, value=value)

    # 前序步骤同名参数同值 → 复用第一个步骤的取值来源（相同接口请求保持一致）
    for prev in previous_indexes:
        prev_source = prev.param_sources.get(name)
        if prev_source is not None and _canonical_key(prev_source.value) == _canonical_key(value):
            return replace(prev_source, param_name=name, value=value)

    if not isinstance(value, (dict, list)):
        # 叶子参数：前序响应中字段名（不区分大小写）与值均相同 → 引用
        key = str(value)
        for prev in previous_indexes:
            for path, resp_value in prev.flattened.items():
                if _field_matches(path, name) and str(resp_value) == key:
                    return ParamSource(
                        kind="step_response",
                        param_name=name,
                        step_key=prev.step_key,
                        path=path,
                        value=value,
                    )
        # 兜底：值匹配（字段名可不一致，如 customerCard 引用响应 cardNo）——
        # 数值型值 ≥5 字符、非数值（中文/字母）≥2 字符，且在前序响应中单步骤
        # 唯一出现；数值短值不参与避免同值异义误引用（sourceType=0 → favProFlag=0）
        if _value_match_eligible(key):
            ambiguous_note = None
            for prev in previous_indexes:
                paths = _value_paths(prev.flattened, key)
                if len(paths) != 1:
                    # 出现多次（同值异义候选）：不引用，但记下第一个歧义步骤
                    # 的候选路径，落 test_data 时生成注释提示用户可手工改引用
                    if ambiguous_note is None and len(paths) > 1:
                        ambiguous_note = _ambiguity_note(prev.step_key, paths)
                    continue
                path = paths[0]
                return ParamSource(
                    kind="step_response",
                    param_name=name,
                    step_key=prev.step_key,
                    path=path,
                    value=value,
                )
            # 值合格但无唯一引用：若曾在前序响应中出现多次，注释提示候选路径；
            # 从未出现则无候选不提示（如 senderAddress 两侧键集合不同的 JSON 串）
            if ambiguous_note is not None:
                return ParamSource(kind="test_data", param_name=name, value=value, note=ambiguous_note)
        # JSON 字符串子集投影：请求值为 JSON 对象字符串且全部非空叶子在前序
        # 同一步骤键的压平索引中同值命中（完备子集）时，引用响应字段并以
        # json.dumps 重组回字符串（senderAddress JSON 串 ↔ 仓库扁平对象）
        json_proj = _find_json_projection(name, key, previous_indexes)
        if json_proj is not None:
            return json_proj
        return ParamSource(kind="test_data", param_name=name, value=value)

    # 容器参数：前序响应中同名字段结构完全相等 → 整体引用
    value_key = _canonical_key(value)
    for prev in previous_indexes:
        for resp_path, resp_value in prev.container_index.items():
            if _field_matches(resp_path, name) and _canonical_key(resp_value) == value_key:
                return ParamSource(
                    kind="step_response",
                    param_name=name,
                    step_key=prev.step_key,
                    path=resp_path,
                    value=value,
                )

    # 响应收集接口投影：list 参数元素与收集列表元素同字段对齐 → 列表推导引用
    # （优先于字段级投影，配置显式指定优先，且普通投影无法命中未建索引的 collect 响应）
    collect_hit = _find_collect_projection(value, previous_indexes)
    if collect_hit is not None:
        collect_key, field = collect_hit
        return ParamSource(
            kind="collect_projection",
            param_name=name,
            step_key=collect_key,
            value=value,
            projection=field,
        )

    # 字段级投影（容器部分一致）
    projection = _find_projection(value, previous_indexes)
    if projection is not None:
        prev, _resp_path, tree = projection
        return ParamSource(
            kind="container_projection",
            param_name=name,
            step_key=prev.step_key,
            value=value,
            projection=tree,
        )

    # 纯叶子列表参数的元素级投影
    if isinstance(value, list):
        leaf_projection = _find_list_leaf_projection(value, previous_indexes)
        if leaf_projection is not None:
            prev, tree = leaf_projection
            return ParamSource(
                kind="container_projection",
                param_name=name,
                step_key=prev.step_key,
                value=value,
                projection=tree,
            )

    return ParamSource(kind="test_data", param_name=name, value=value)


def _collect_response_items(response_data: Any, cfg: dict) -> Any:
    """按配置 append_path 从响应 data 中取收集片段；路径不可达时返回 None。"""
    append_path = collect_append_path(cfg)
    items = response_data
    for part in append_path:
        if isinstance(items, dict) and part in items:
            items = items[part]
        else:
            return None
    return items


def _find_collect_projection(
    value: Any,
    previous_indexes: list[StepValueContext],
) -> tuple[str, str] | None:
    """为纯叶子列表参数寻找响应收集接口的列表推导投影。

    聚合前序同 collect_key 请求的 append 片段（收集列表元素），与参数元素
    按同一字段对齐（元素数一致且值 str 归一相等），命中返回
    (collect_key, 字段名)，渲染为
    ``[i[字段名] for i in test_data[collect_key]]``。仅对前序 collect 步骤
    响应生效（普通步骤响应不参与，避免产生悬空引用）。
    """
    if not isinstance(value, list) or not value:
        return None
    if any(isinstance(item, (dict, list)) for item in value):
        return None
    tried_keys: set[str] = set()
    for prev in previous_indexes:
        cfg = prev.collect
        if cfg is None:
            continue
        # 同一 collect_key 的多次调用聚合结果相同，只需尝试一次
        if cfg["collect_key"] in tried_keys:
            continue
        tried_keys.add(cfg["collect_key"])
        # 前序同 collect_key 请求的 append 片段按执行顺序聚合（收集列表元素）
        items = [
            _collect_response_items(p.response_data, p.collect)
            for p in previous_indexes
            if p.collect is not None and p.collect["collect_key"] == cfg["collect_key"]
        ]
        if not items or any(item is None for item in items):
            continue
        if len(items) != len(value):
            continue
        if not all(isinstance(item, dict) for item in items):
            continue
        for field_name, _ in items[0].items():
            if all(str(item.get(field_name)) == str(v) for item, v in zip(items, value)):
                return cfg["collect_key"], field_name
    return None


def _path_segments(path: tuple) -> str:
    """把取值路径渲染为下标访问段（如 ``['list'][0]['id']``）。"""
    return "".join(
        f"[{part!r}]" if isinstance(part, str) else f"[{part}]"
        for part in path
    )


def source_expression(source: ParamSource) -> str:
    """把取值来源渲染为 Python 表达式（test_data 引用）。"""
    if source.kind == "test_data":
        return f"test_data[{source.param_name!r}]"
    if source.kind == "step_response":
        return f"test_data[{source.step_key!r}]{_path_segments(source.path)}"
    raise ValueError(f"非引用型取值来源: {source.kind}")


def render_test_data_init(plan: ScenarioValuePlan, indent: int = 8) -> list[str]:
    """生成测试方法顶部的 test_data 初始化代码行。

    ``test_data`` 声明为 ``dict`` 注解：字典值既含用例级标量也含步骤响应
    对象，不注解会被类型检查器推断为 ``dict[str, str]``，导致后续
    ``test_data['步骤键']['字段']`` 下标报错。
    """
    lines = [" " * indent + "# 初始化测试数据字典，用于在步骤间传递数据"]
    lines.append(" " * indent + "test_data: dict = {")
    for name, value in plan.test_data_values.items():
        lines.append(f"{' ' * (indent + 4)}{name!r}: {format_parameter_value(value)},")
    lines.append(" " * indent + "}")
    lines.append("")
    return lines


def _projection_code(tree: Any, step_key: str, indent: int) -> list[str]:
    """渲染投影树为多行 Python 代码（首行为开括号，末行为闭合括号）。

    叶子 ``("ref", 路径)`` 渲染为 ``test_data[步骤键][...]`` 引用表达式，
    ``("literal", 值)`` 渲染为字面量。``indent`` 为闭合括号的缩进空格数，
    条目缩进 ``indent + 4``，与 :func:`render_param_dict_code` 的缩进约定一致。
    """
    if isinstance(tree, dict):
        lines = ["{"]
        for key, child in tree.items():
            child_lines = _projection_code(child, step_key, indent + 4)
            child_lines[-1] += ","
            key_str = json.dumps(key, ensure_ascii=False)
            lines.append(" " * (indent + 4) + f"{key_str}: " + child_lines[0])
            lines.extend(child_lines[1:])
        lines.append(" " * indent + "}")
        return lines
    if isinstance(tree, list):
        lines = ["["]
        for child in tree:
            child_lines = _projection_code(child, step_key, indent + 4)
            child_lines[-1] += ","
            lines.append(" " * (indent + 4) + child_lines[0])
            lines.extend(child_lines[1:])
        lines.append(" " * indent + "]")
        return lines
    kind, payload = tree
    if kind == "ref":
        return [f"test_data[{step_key!r}]{_path_segments(payload)}"]
    if kind == "test_data":
        return [f"test_data[{payload!r}]"]
    return [format_parameter_value(payload)]


def _json_projection_code(projection: dict, step_key: str, indent: int) -> list[str]:
    """渲染 json_projection 为 json.dumps(多行字典, ensure_ascii=False) 代码。

    按请求 JSON 原键序输出：``("ref", 路径)`` 叶子渲染为 test_data 引用，
    ``("literal", 值)``（null/空串键）渲染为字面量；首行为 ``json.dumps({``，
    末行为 ``}, ensure_ascii=False)``。ensure_ascii=False 保持中文原样与
    HAR 录制形态一致；重组后仍是字符串，符合接口 string 声明（data 渠道
    form-urlencoded 下不能渲染成 dict，会破坏请求形态）。
    """
    inner = " " * indent
    child = " " * (indent + 4)
    lines = ["json.dumps({"]
    for key, (kind, payload) in projection.items():
        if kind == "ref":
            expr = f"test_data[{step_key!r}]{_path_segments(payload)}"
        else:
            expr = format_parameter_value(payload)
        lines.append(f'{child}{json.dumps(key, ensure_ascii=False)}: {expr},')
    lines.append(inner + "}, ensure_ascii=False)")
    return lines


def render_param_dict_code(
    values: dict[str, Any],
    sources: dict[str, ParamSource],
    indent: int = 16,
    extra_items: dict[str, str] | None = None,
) -> str:
    """渲染步骤的 params/data 字典字面量（含 test_data 引用表达式）。

    与 format_params_for_python 的缩进约定一致：条目缩进 indent 空格，
    闭合花括号缩进 indent-4 空格，供 ``s_step_params.j2`` / ``s_step_data.j2``
    在 ``params = {{ code }}`` 处拼接。

    Args:
        values: 参数名 → 值（字面量或默认值）。
        sources: 参数名 → 取值来源（仅含可引用的参数）。
        indent: 条目缩进空格数（默认 16，与旧实现一致）。
        extra_items: 追加的键值对（键 → 原样代码串，如形参名），
            用于响应收集接口把文件字段渲染为循环形参引用。
    """
    if not values and not extra_items:
        return "{}"
    inner = " " * indent
    closing = " " * (indent - 4)
    lines = ["{"]
    for name, value in values.items():
        source = sources.get(name)
        if source is not None and source.kind in ("container_projection", "json_projection"):
            # 两种投影均携带来源步骤键（构造时取自 prev.step_key）
            assert source.step_key is not None
            step_key = source.step_key
            if source.kind == "container_projection":
                code_lines = _projection_code(source.projection, step_key, indent + 4)
            else:
                code_lines = _json_projection_code(source.projection, step_key, indent + 4)
            lines.append(f'{inner}"{name}": {code_lines[0]}')
            lines.extend(code_lines[1:-1])
            lines.append(code_lines[-1] + ",")
        elif source is not None and source.kind == "collect_projection":
            # 响应收集接口列表推导引用：[i['fileUrlKey'] for i in test_data['storage_upload']]
            assert source.step_key is not None
            field = source.projection
            expr = f"[i[{field!r}] for i in test_data[{source.step_key!r}]]"
            lines.append(f'{inner}"{name}": {expr},')
        elif source is not None and source.kind in ("test_data", "step_response"):
            expr = source_expression(source)
            # test_data 来源携带歧义注释时单独成行输出（行尾注释过长会
            # 导致 ruff format 把引用表达式折行，独立注释行更清晰）
            if source.kind == "test_data" and source.note:
                lines.append(f"{inner}# {source.note}")
            lines.append(f'{inner}"{name}": {expr},')
        else:
            expr = format_parameter_value(value)
            lines.append(f'{inner}"{name}": {expr},')
    for name, code in (extra_items or {}).items():
        lines.append(f'{inner}"{name}": {code},')
    lines.append(closing + "}")
    return "\n".join(lines)
