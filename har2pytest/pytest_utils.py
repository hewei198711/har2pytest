"""pytest 测试工具函数"""

from collections.abc import Callable
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
    非空列表值（覆盖 ``records``/``rows`` 等命名）；无匹配时返回空列表。
    """
    if not isinstance(resp_data, dict):
        return []
    for key in ("lists", "list"):
        items = resp_data.get(key)
        if isinstance(items, list):
            return items
    return next(
        (
            v
            for v in resp_data.values()
            if isinstance(v, list) and v and all(isinstance(i, dict) for i in v)
        ),
        [],
    )


def collect_list_query_data(data: Any, list_query_data: dict[str, Any]) -> None:
    """从响应 JSON 收集字段值到 list_query_data（原地更新）。

    优先精确匹配参数名（不区分大小写），响应字段无同名参数时降级前缀模糊匹配
    （双向包含：响应字段名以参数名开头，如参数 ``operator`` 可匹配响应字段
    ``operatorNo``/``operatorName``，命中多个时取第一个；或参数名包含响应
    字段名，如参数 ``demoCodeList`` 包含响应字段 ``demoCode``，值包装为
    单元素列表）；响应值优先：首条记录的匹配值覆盖已有值（含录制值），
    同一参数只收集一次。时间参数（``APIConfig.is_time_param`` 命中）不参与
    收集：其值由 list_query_data 的 datetime 表达式动态提供，避免响应记录中的
    同语义时间戳字段（如 ``commitTime``）污染搜索条件。

    Args:
        data: 接口响应 JSON（``await r.json()`` 结果）
        list_query_data: list_query_data 类属性字典（原地写入）
    """
    resp_data = data.get("data", {}) if isinstance(data, dict) else {}
    items = extract_list_items(resp_data)
    # 时间参数不参与收集：值由 list_query_data 的 datetime 表达式动态提供
    collectable_params = [p for p in list_query_data if not APIConfig.is_time_param(p)]
    collected = set()
    for item in items:
        if isinstance(item, dict):
            for k, v in item.items():
                if isinstance(v, (str, int, float)) and v not in ("", None):
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
                        # 参数名包含响应字段名（如 demoCodeList 包含 demoCode）
                        param_name = next(
                            (
                                p
                                for p in collectable_params
                                if p.lower().startswith(k.lower()) and p not in collected
                            ),
                            None,
                        )
                        is_reverse_match = True
                    if param_name and param_name not in collected:
                        collected.add(param_name)
                        list_query_data[param_name] = [v] if is_reverse_match else v
