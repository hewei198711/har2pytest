"""
测试 allure_compat.py 模块（async step 兼容包装）。
"""

import asyncio

import allure

from har2pytest import allure_compat


# ==================== 安装与探测测试 ====================


@allure.feature("Allure异步兼容")
@allure.story("安装与探测")
@allure.title("测试安装幂等性：重复调用无副作用")
def test_install_idempotent():
    # 可能已被根 conftest 安装；再次调用应幂等且不抛错
    allure_compat.install_async_step_support()
    # 第二次调用应返回 False（已安装或原生支持）
    assert allure_compat.install_async_step_support() is False
    # 验证 allure.step 已被替换或原生支持
    assert hasattr(allure, "step")


@allure.feature("Allure异步兼容")
@allure.story("安装与探测")
@allure.title("测试原生异步感知探测返回布尔值")
def test_native_aware_probe_returns_bool():
    assert isinstance(allure_compat._native_async_aware(), bool)


# ==================== 装饰器用法测试 ====================


@allure.feature("Allure异步兼容")
@allure.story("装饰器用法")
@allure.title("测试异步函数带标题装饰器")
def test_async_step_decorator():
    @allure.step("带标题 async step")
    async def doit(x):
        return x + 1

    # 验证返回值正确
    assert asyncio.run(doit(1)) == 2
    # 验证 functools.wraps 保留了函数元数据
    assert doit.__name__ == "doit"


@allure.feature("Allure异步兼容")
@allure.story("装饰器用法")
@allure.title("测试异步函数裸装饰器（@allure.step 无括号）")
def test_bare_step_async():
    @allure.step
    async def bare(x):
        return x

    assert asyncio.run(bare(9)) == 9
    # 验证裸装饰器使用函数名作为标题
    assert bare.__name__ == "bare"


@allure.feature("Allure异步兼容")
@allure.story("装饰器用法")
@allure.title("测试同步函数带标题装饰器")
def test_sync_step_decorator():
    @allure.step("同步 step")
    def sync_step(x):
        return x * 2

    assert sync_step(2) == 4


@allure.feature("Allure异步兼容")
@allure.story("装饰器用法")
@allure.title("测试同步函数裸装饰器（@allure.step 无括号）")
def test_bare_step_sync():
    @allure.step
    def bare_sync(x):
        return x + 10

    assert bare_sync(5) == 15


@allure.feature("Allure异步兼容")
@allure.story("装饰器用法")
@allure.title("测试异步函数装饰器异常传播")
def test_async_step_decorator_exception():
    @allure.step("会抛异常的 async step")
    async def fail():
        raise ValueError("async error")

    import pytest
    with pytest.raises(ValueError, match="async error"):
        asyncio.run(fail())


# ==================== 上下文管理器用法测试 ====================


@allure.feature("Allure异步兼容")
@allure.story("上下文管理器用法")
@allure.title("测试同步 with 上下文管理器")
def test_step_context_manager():
    with allure.step("with 上下文"):
        result = 1 + 1
        assert result == 2


@allure.feature("Allure异步兼容")
@allure.story("上下文管理器用法")
@allure.title("测试同步上下文管理器异常传播")
def test_sync_step_context_manager_exception():
    import pytest
    with pytest.raises(RuntimeError, match="sync error"):
        with allure.step("会抛异常的 with 上下文"):
            raise RuntimeError("sync error")


@allure.feature("Allure异步兼容")
@allure.story("上下文管理器用法")
@allure.title("测试异步 async with 上下文管理器")
def test_async_step_context_manager():
    async def run_async_with():
        async with allure.step("async with 上下文"):  # type: ignore[attr-defined]
            await asyncio.sleep(0)
            return 42

    assert asyncio.run(run_async_with()) == 42


@allure.feature("Allure异步兼容")
@allure.story("边界场景")
@allure.title("测试 _async_aware_step 入口函数 None 标题")
def test_async_aware_step_none_title():
    # _async_aware_step(None) 应返回 _AsyncAwareAllureStep 实例
    result = allure_compat._async_aware_step(None)
    assert isinstance(result, allure_compat._AsyncAwareAllureStep)
    assert result._title is None
