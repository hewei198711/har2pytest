"""pytest 测试工具函数"""

import logging
from collections.abc import Callable

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)


def retry_step(counts: int = 2, times: int = 20) -> Callable:
    """
    测试步骤断言失败后重试装饰器。
    支持同步和异步函数（tenacity 自动适配）。

    Args:
        counts: 最大执行次数（含首次）
        times: 每次重试间隔秒数
    """

    def after(retry_state):
        logger.warning(
            "[retry_step] %s 第%d次失败, %ds后重试: %s",
            retry_state.fn.__name__,
            retry_state.attempt_number,
            times,
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
