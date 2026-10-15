"""参数化项构建与标准化。

提供从 API 文件参数或 HAR 请求参数构建 pytest 参数化项的纯函数，
包括分页参数过滤、时间参数过滤、组合参数归并与分页退化逻辑。
"""

from __future__ import annotations

from typing import Any

from .config import APIConfig
from .utils import deduplicate_values


def is_valid_param(value: Any) -> bool:
    """判断参数值是否有效。

    有效参数定义为：非空字符串、非 None、非空列表/集合。

    Args:
        value: 参数值

    Returns:
        如果参数有效返回 True，否则返回 False
    """
    if value is None or value == "":
        return False
    if isinstance(value, (list, set)):
        return len(value) > 0
    return True


def build_param_items_from_api(
    api_params: dict[str, Any],
    param_values: dict[str, list[Any]],
    is_batch_mode: bool = False,
) -> list[dict[str, Any]]:
    """从 API 文件参数构建参数化项列表。

    直接读取 api.json 中预计算的 ``param_values`` 枚举值字典，不再对备注
    重新调用 ``parse_state_values``，避免与 ``api_generator`` 重复解析。

    处理顺序：
    1. 遍历 ``param_values``，为每个有枚举值的非分页/非时间参数构建参数化项；
    2. 遍历 ``api_params`` 中剩余参数，用当前值作为默认值（batch 模式包含空值）。

    枚举值不存入返回项（下游通过 param_values 参数取用），本函数只决定
    哪些参数进入参数化列表。

    Args:
        api_params: API 文件中的所有参数（包括 params 和 data）
        param_values: 从 api.json 读取的参数枚举值字典
            （参数名 -> 枚举值列表，由 api_generator 预计算）
        is_batch_mode: 是否为 batch 模式（为 True 时包含空值参数）

    Returns:
        参数化项列表，每个元素为 ``{"param_name": ...}``
    """
    param_items: list[dict[str, Any]] = []
    handled: set[str] = set()

    # 1. 有枚举值的参数：直接读取 param_values
    for param_name, values in param_values.items():
        if APIConfig.is_pagination_param(param_name) or APIConfig.is_time_param(param_name):
            continue
        if not values:
            continue
        handled.add(param_name)
        param_items.append({"param_name": param_name})

    # 2. 无枚举值的参数：用 api_params 当前值作为默认值
    for param_name, param_value in api_params.items():
        if param_name in handled:
            continue
        # 跳过分页参数与时间参数（时间参数由 list_query_data datetime 动态计算）
        if APIConfig.is_pagination_param(param_name) or APIConfig.is_time_param(param_name):
            continue
        # 非 batch 模式只收有效参数；batch 模式连空值（""/None/空容器）一并收录
        if is_valid_param(param_value) or is_batch_mode:
            param_items.append({"param_name": param_name})

    return param_items


def normalize_params_for_parametrization(
    requests_params: list[dict[str, Any]],
    constant_params: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """标准化参数化数据结构。

    将多个请求的参数整理为适合 pytest 参数化的格式，支持单参数和组合参数。
    过滤分页参数、时间参数和常量参数，对有效参数进行去重归类。

    Args:
        requests_params: 多个请求的参数字典列表
        constant_params: 常量参数（不参与参数化，由 HAR 分析得出并写入 api.json）

    Returns:
        参数化项列表，每个元素包含参数名、参数值列表和其他参数
    """
    param_value_map: dict[str, dict[str, Any]] = {}
    constant_params = constant_params or {}

    for req in requests_params:
        valid_params: dict[str, Any] = {}
        other_params: dict[str, Any] = {}

        for param_name, param_value in req.items():
            # 常量参数、分页参数、时间参数不参与参数化，归入 other_params 作为固定值
            if (
                param_name in constant_params
                or APIConfig.is_pagination_param(param_name)
                or APIConfig.is_time_param(param_name)
            ):
                other_params[param_name] = param_value
            elif is_valid_param(param_value):
                valid_params[param_name] = param_value
            else:
                other_params[param_name] = param_value

        if not valid_params:
            continue

        if len(valid_params) > 1:
            # 组合参数
            sorted_names = sorted(valid_params.keys())
            combo_key = ",".join(sorted_names)
            combo_value = [valid_params[name] for name in sorted_names]

            if combo_key not in param_value_map:
                param_value_map[combo_key] = {"values": [], "other_params": other_params}
            param_value_map[combo_key]["values"].append(combo_value)
        else:
            # 单参数
            param_name, param_value = next(iter(valid_params.items()))
            if param_name not in param_value_map:
                param_value_map[param_name] = {"values": [], "other_params": other_params}
            param_value_map[param_name]["values"].append(param_value)

    # 构建最终结果并去重
    merged_result = []
    for param_name, data in param_value_map.items():
        merged_result.append({"param_name": param_name, param_name: deduplicate_values(data["values"]), "other_params": data["other_params"]})

    # 过滤分页参数与时间参数后没有任何有效参数（如列表接口仅携带 pageNum/pageSize 或时间参数），
    # 退化为一条基于分页参数的默认参数化项，避免后续误报"没有有效的测试参数"。
    if not merged_result:
        return build_pagination_only_items(requests_params, constant_params)
    return merged_result


def build_pagination_only_items(
    requests_params: list[dict[str, Any]],
    constant_params: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """请求仅有分页/无效参数时，退化为单条默认参数化项。

    列表类接口常只携带 ``pageNum``/``pageSize``（也可能全为空值参数），
    过滤分页参数后没有可变的"有效参数"。此时把分页参数本身当作变量，
    生成一条能正常发请求的参数化项：变量取各请求中的取值（去重），
    其余参数作为固定值放入 ``other_params``。

    Args:
        requests_params: 请求参数字典列表（每项为非空 dict）。
        constant_params: 常量参数（不参与参数化）；变量选择时排除，
            全常量请求没有可用变量时返回空列表。

    Returns:
        含 0 或 1 条参数化项的列表；无可用参数时返回空列表。
    """
    constant_params = constant_params or {}
    if not requests_params:
        return []
    first = requests_params[0]
    # 变量优先选包含分页关键字的参数（如 pageNum），否则退而求其次取首个键；
    # 常量参数由 constant_params 单独承载，不得被选为参数化变量
    var = next(
        (p for p in first if APIConfig.is_pagination_param(p) and p not in constant_params),
        next((p for p in first if p not in constant_params), None),
    )
    if var is None:
        return []
    values = deduplicate_values([r[var] for r in requests_params if var in r and is_valid_param(r[var])])
    if not values:
        values = [first[var]]
    other_params = {key: value for key, value in first.items() if key != var}
    return [{"param_name": var, var: values, "other_params": other_params}]
