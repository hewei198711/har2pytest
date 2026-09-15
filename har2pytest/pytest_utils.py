"""pytest 测试工具函数"""

from collections.abc import Callable

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

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
