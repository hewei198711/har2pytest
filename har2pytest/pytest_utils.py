"""pytest 测试工具函数"""

from collections.abc import Callable, Iterable
from typing import Any

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from .config import APIConfig
from .logger import logger


def retry_step(counts: int = 2, times: int = 20) -> Callable:
    """
    测试步骤断言失败后重试装饰器。
    支持同步和异步函数（tenacity 自动适配）。

    Args:
        counts: 最大执行次数（含首次）
        times: 每次重试间隔秒数
    """

    def after(retry_state):
        # 最后一次失败后没有下一次重试，提示语不再说“Xs后重试”
        is_last = retry_state.attempt_number >= counts
        suffix = f"{times}s后重试" if not is_last else "重试次数已用完"
        logger.warning(
            "[retry_step] %s 第%d次失败, %s: %s",
            retry_state.fn.__name__,
            retry_state.attempt_number,
            suffix,
            retry_state.outcome.exception(),
        )

    decorator = retry(
        stop=stop_after_attempt(counts),
        wait=wait_fixed(times),
        retry=retry_if_exception_type(AssertionError),
        reraise=True,
        after=after,
    )
    return decorator  # pyright: ignore[reportReturnType]


def extract_list_items(resp_data: Any) -> list:
    """从响应 data 中提取明细列表。

    优先识别 ``lists``/``list`` 键；均不存在时降级取第一个元素为 dict 的
    非空列表值（覆盖 ``records``/``rows`` 等命名）；仍无匹配时递归查找
    嵌套分页对象内的列表（如 ``data.secondCouponInfos.list``）；
    无匹配时返回空列表。
    """
    if not isinstance(resp_data, dict):
        return []
    for key in ("lists", "list"):
        items = resp_data.get(key)
        if isinstance(items, list):
            return items
    for v in resp_data.values():
        if isinstance(v, list) and v and all(isinstance(i, dict) for i in v):
            return v
        if isinstance(v, dict):
            items = extract_list_items(v)
            if items:
                return items
    return []


def _num_value(v: Any) -> int | float | None:
    """数值范围对聚合的取值归一：int/float 原样返回，数值型字符串
    （金额接口常见的 '5200.00' 形态）按 float 解析；bool 与不可解析
    字符串返回 None（不参与 min/max 聚合）。"""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def collect_list_query_data(
    data: Any,
    list_query_data: dict[str, Any],
    extra_time_params: Iterable[str] | None = None,
    value_pairs: dict[str, dict[str, str]] | None = None,
    field_map: dict[str, str] | None = None,
) -> None:
    """从响应 JSON 收集字段值到 list_query_data（原地更新）。

    显式字段映射（``field_map``，{参数名: 响应字段名}，如
    ``{"like": "invoiceSensitive"}``）优先级最高：参数名与响应字段名
    无任何子串包含关系时（like/invoiceSensitive），三级匹配全部落空，
    需靠显式映射收集。

    优先精确匹配参数名（不区分大小写），响应字段无同名参数时降级前缀模糊匹配
    （双向包含：响应字段名以参数名开头，如参数 ``operator`` 可匹配响应字段
    ``operatorNo``/``operatorName``，命中多个时取第一个；或参数名包含响应
    字段名，如参数 ``demoCodeList`` 包含响应字段 ``demoCode``，值包装为
    单元素列表；反向匹配仅限基线为列表的参数（数组声明），标量声明
    （null/空串/数值）不参与，避免借汇总字段值破坏请求形态与范围语义）；
    响应值优先：首条记录的匹配值覆盖已有值（含录制值），
    同一参数只收集一次。时间参数（``APIConfig.is_time_param`` 命中或
    ``extra_time_params`` 传入的单时间参数）不参与收集：其值由
    list_query_data 的 datetime 表达式动态提供，避免响应记录中的
    同语义时间戳字段（如 ``commitTime``）污染搜索条件。
    数值范围对（``value_pairs`` 元数据，非时间的 Start/End 配对）在主收集
    之后聚合所有记录的 min/max 分别写入 start/end 基线（未命中时保持
    None，消费侧降级跳过区间验证）；匹配响应字段优先取 ``field_map`` 显式
    映射（参数名与响应字段名不同名时使用），未配置映射时按词干精确匹配；
    映射字段在响应中找不到数值时直接抛 ValueError——field_map 属手工配置，
    配错必须显式报错提示改正，不回退词干匹配掩盖错误。

    Args:
        data: 接口响应 JSON（``await r.json()`` 结果）
        list_query_data: list_query_data 类属性字典（原地写入）
        extra_time_params: 时间参数名集合（可选，TIME_PARAMS 闸门未命中的
            single_time_params 单时间参数与 epoch 时间对成员，其值由
            list_query_data 的 datetime 表达式动态提供，不参与收集）
        value_pairs: 数值范围对元数据（可选，{词干: {"start": 参数名, "end": 参数名}}，
            来自 api.json value_pairs 落盘，基线取响应词干字段的 min/max）
        field_map: 参数名到响应字段名的显式映射（可选，{参数名: 响应字段名}，
            如 {"like": "invoiceSensitive"}）：参数名与响应字段名无任何子串
            包含关系时三级匹配全部落空，由显式映射兜底；匹配优先级最高
    """
    resp_data = data.get("data", {}) if isinstance(data, dict) else {}
    items = extract_list_items(resp_data)
    # 时间参数不参与收集：值由 list_query_data 的 datetime 表达式动态提供
    extra = set(extra_time_params or ())
    # 数值对成员不参与主收集：基线由下方 value_pairs 聚合通道专门提供
    vp_members = {
        name for info in (value_pairs or {}).values() for name in (info["start"], info["end"])
    }
    collectable_params = [
        p
        for p in list_query_data
        # 数组类型参数（基线为 list）豁免时间关键字误伤：is_time_param 子串
        # 匹配会把 orderMonthList 命中 "ordermonth" 判为时间参数，但其值应
        # 由响应收集（与其他 List 参数一致），datetime 动态值仅供给标量时间参数
        if (isinstance(list_query_data[p], list) or not APIConfig.is_time_param(p))
        and p not in extra
        and p not in vp_members
    ]
    collected = set()
    field_map = field_map or {}
    for item in items:
        if isinstance(item, dict):
            for k, v in item.items():
                if isinstance(v, (str, int, float)) and v not in ("", None):
                    param_name = next(
                        (
                            p
                            for p, f in field_map.items()
                            if f.lower() == k.lower()
                            and p in collectable_params
                            and p not in collected
                        ),
                        None,
                    )
                    if param_name is None:
                        param_name = next(
                            (p for p in collectable_params if p.lower() == k.lower()), None
                        )
                    if param_name is None:
                        # 响应字段名以参数名开头（参数被响应字段名包含）
                        param_name = next(
                            (
                                p
                                for p in collectable_params
                                if k.lower().startswith(p.lower()) and p not in collected
                            ),
                            None,
                        )
                    is_reverse_match = False
                    if param_name is None:
                        # 参数名包含响应字段名（如 demoCodeList 包含 demoCode）；
                        # 仅限基线为列表的参数（api.json 数组声明）：标量声明
                        # （null/空串/数值，如 yearReturnAmtEnd）不得借汇总字段
                        # yearReturnAmt 反向命中被包成 [v]，破坏请求形态与范围语义
                        param_name = next(
                            (
                                p
                                for p in collectable_params
                                if p.lower().startswith(k.lower())
                                and isinstance(list_query_data[p], list)
                                and p not in collected
                            ),
                            None,
                        )
                        is_reverse_match = True
                    if param_name and param_name not in collected:
                        collected.add(param_name)
                        list_query_data[param_name] = [v] if is_reverse_match else v
    # 数值范围对聚合：min/max 分别写入 start/end（bool 是 int 子类须排除；
    # 未命中时保持 None 基线，消费侧降级跳过验证）。匹配字段优先取 field_map
    # 显式映射（参数名与响应字段名不同名时使用），未配置映射时按词干精确
    # 匹配；数值型字符串（如金额字段 '5200.00'）经 _num_value 归一后同样
    # 参与聚合。
    for base, info in (value_pairs or {}).items():
        mapped = field_map.get(info["start"]) or field_map.get(info["end"])
        match_field = mapped or base
        values = [
            _num_value(v)
            for item in items
            if isinstance(item, dict)
            for k, v in item.items()
            if k.lower() == match_field.lower()
        ]
        # 拆开过滤 None：推导式内嵌 _num_value(v) is not None 是第二次独立
        # 调用，类型检查器无法收窄，此处独立过滤后 min/max 收到纯数值序列
        values = [num for num in values if num is not None]
        if mapped and not values:
            raise ValueError(
                f"数值范围对 {info['start']}/{info['end']} 配置的 field_map 映射字段 "
                f"{match_field!r} 在响应记录中未找到数值，请修正 api.json 的 field_map 配置"
            )
        if values:
            list_query_data[info["start"]] = min(values)
            list_query_data[info["end"]] = max(values)
