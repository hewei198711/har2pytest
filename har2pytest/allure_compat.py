"""Allure async step 兼容补丁。

问题
----
原生 ``@allure.step`` 是同步装饰器：装饰 **async** 函数时，step 上下文在
“返回协程对象”那一刻就已退出，而函数体（请求/响应 ``allure.attach``）在
``await`` 之后才真正执行，导致 Request/Response 附件泄漏到测试级、
step 显示 0s。同步函数无此问题。

方案
----
不改生成用例的 step 模板。把 ``allure.step`` 替换为 async 感知的包装（装饰器 + 上下文管理器双用法）：
- async 函数 → 返回 async wrapper，在协程内部保持 step 上下文直到 ``await`` 结束；
- 同步函数 / ``with allure.step(...)`` / 裸装饰器 ``@allure.step`` → 委托原生实现；
- 若当前 allure 已原生支持 async step，则跳过不包装。

启用
----
默认在导入 ``har2pytest`` 时自动安装（见 ``har2pytest/__init__.py``），
无需手工调用，也不需要修改任何 conftest / 生成用例的 step 模板。

如确需在更早时机手动启用（例如仅使用 allure、未导入 har2pytest 的用例），
在 conftest.py 顶部调用一次::

    from har2pytest.allure_compat import install_async_step_support
    install_async_step_support()

该函数幂等：重复调用无副作用；若检测到 allure 已原生支持 async step，
会自动跳过安装。
"""

from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from typing import Any

_original_step: Any = None


def _native_async_aware() -> bool:
    """探测当前 allure 的 step 实现是否已原生支持 coroutine。

    通过检查 step 相关可调用对象的字节码里是否出现协程处理关键字判断；
    无法判断时返回 False（保守地安装兼容包装，不影响正确性）。
    """
    try:
        import allure

        targets = []
        step_fn = getattr(allure, "step", None)
        if step_fn is not None:
            targets.append(step_fn)
        try:
            from allure_commons import _allure

            targets.append(_allure.StepContext.__call__)
        except Exception:  # pragma: no cover - 不同版本结构
            pass
        keywords = {"iscoroutinefunction", "iscoroutine", "awaitable", "asyncio", "ensure_future", "create_task"}
        for target in targets:
            code = getattr(target, "__code__", None)
            if code is None:
                continue
            if set(code.co_names) & keywords:
                return True
        return False
    except Exception:  # pragma: no cover - 无 allure 环境
        return False


def _decorate(func: Callable, title: str, args: tuple = (), kwargs: dict | None = None) -> Callable:
    """按函数类型生成装饰包装：async 在协程内部保持 step 上下文，sync 走原生。"""
    step = _original_step(title, *args, **(kwargs or {}))
    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def wrapper(*a, **kw):
            with step:
                return await func(*a, **kw)

        return wrapper

    return step(func)


class _AsyncAwareAllureStep:
    """兼容 async 函数的 allure.step（装饰器 + 上下文管理器双用法）。"""

    def __init__(self, title, *args, **kwargs):
        self._title = title
        self._args = args
        self._kwargs = kwargs
        self._ctx: Any = None

    def __call__(self, func: Callable) -> Callable:
        # 装饰器用法：async 函数在协程内部保持 step 上下文
        return _decorate(func, self._title, self._args, self._kwargs)

    def __enter__(self):
        # with allure.step("...") 上下文管理器用法
        self._ctx = _original_step(self._title, *self._args, **self._kwargs)
        return self._ctx.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._ctx is None:
            return False
        return self._ctx.__exit__(exc_type, exc_val, exc_tb)

    async def __aenter__(self):
        # async with allure.step("...") 上下文管理器用法
        self._ctx = _original_step(self._title, *self._args, **self._kwargs)
        return self._ctx.__enter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._ctx is None:
            return False
        return self._ctx.__exit__(exc_type, exc_val, exc_tb)


def _async_aware_step(title_or_func: Any = None, *args, **kwargs) -> Any:
    """替换后的 ``allure.step``：兼容裸装饰器 / 带标题装饰器 / 上下文管理器。"""
    if callable(title_or_func):
        # 裸装饰器用法：@allure.step 直接装饰函数
        name = getattr(title_or_func, "__name__", "step")
        return _decorate(title_or_func, name)
    return _AsyncAwareAllureStep(title_or_func, *args, **kwargs)


def install_async_step_support() -> bool:
    """把 ``allure.step`` 替换为 async 感知包装（幂等；原生已支持则跳过）。

    Returns:
        True 表示本次安装了兼容包装；False 表示无需/未安装
        （已装过、原生已支持 async step、或未安装 allure）。
    """
    global _original_step
    try:
        import allure as _allure_module
    except Exception:  # pragma: no cover - 无 allure 环境
        return False

    # 幂等：进程内已替换过（以 allure 模块属性为唯一标志）
    if getattr(_allure_module, "_har2pytest_async_aware", False):
        return False

    _original_step = _allure_module.step

    # 版本探测：原生已支持 async step 则不包装，避免与未来版本冲突
    if _native_async_aware():
        setattr(_allure_module, "_har2pytest_async_aware", True)
        return False

    _allure_module.step = _async_aware_step
    setattr(_allure_module, "_har2pytest_async_aware", True)
    return True
