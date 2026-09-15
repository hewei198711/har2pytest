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
    assert allure_compat.install_async_step_support() is False


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

    assert asyncio.run(doit(1)) == 2


@allure.feature("Allure异步兼容")
@allure.story("装饰器用法")
@allure.title("测试异步函数裸装饰器（@allure.step 无括号）")
def test_bare_step_async():
    @allure.step
    async def bare(x):
        return x

    assert asyncio.run(bare(9)) == 9


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


# ==================== 上下文管理器用法测试 ====================


@allure.feature("Allure异步兼容")
@allure.story("上下文管理器用法")
@allure.title("测试同步 with 上下文管理器")
def test_step_context_manager():
    with allure.step("with 上下文"):
        assert True


@allure.feature("Allure异步兼容")
@allure.story("上下文管理器用法")
@allure.title("测试异步 async with 上下文管理器")
def test_async_step_context_manager():
    async def run_async_with():
        async with allure.step("async with 上下文"):  # type: ignore[attr-defined]
            await asyncio.sleep(0)
            return 42

    assert asyncio.run(run_async_with()) == 42
