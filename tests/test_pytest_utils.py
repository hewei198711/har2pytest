"""
测试 pytest_utils.py 模块
"""

import logging

import allure
import pytest

from har2pytest.pytest_utils import retry_step


@allure.feature("pytest工具函数")
@allure.story("重试装饰器")
@allure.title("测试同步函数失败后重试成功")
def test_retry_step_sync_success_after_retry(caplog):
    caplog.set_level(logging.WARNING, logger="har2pytest")
    attempts = []

    @retry_step(counts=3, times=0)
    def unstable():
        attempts.append(1)
        if len(attempts) < 2:
            raise AssertionError("first two attempts fail")
        return "ok"

    assert unstable() == "ok"
    assert len(attempts) == 2

    # 重试时输出警告日志（含函数名与失败信息）
    assert "[retry_step]" in caplog.text
    assert "unstable" in caplog.text
    assert "第1次失败" in caplog.text


@allure.feature("pytest工具函数")
@allure.story("重试装饰器")
@allure.title("测试同步函数一直失败时按次数重试并抛出异常")
def test_retry_step_sync_fail_always():
    attempts = []

    @retry_step(counts=3, times=0)
    def always_fail():
        attempts.append(1)
        raise AssertionError("boom")

    with pytest.raises(AssertionError, match="boom"):
        always_fail()
    # 总执行次数 = counts（含首次）
    assert len(attempts) == 3


@allure.feature("pytest工具函数")
@allure.story("重试装饰器")
@allure.title("测试非AssertionError异常不重试")
def test_retry_step_non_assertion_error_no_retry():
    attempts = []

    @retry_step(counts=3, times=0)
    def raise_value_error():
        attempts.append(1)
        raise ValueError("not retried")

    with pytest.raises(ValueError, match="not retried"):
        raise_value_error()
    # 仅 AssertionError 触发重试，其他异常立即抛出
    assert len(attempts) == 1


@allure.feature("pytest工具函数")
@allure.story("重试装饰器")
@allure.title("测试异步函数重试")
async def test_retry_step_async_retry():
    attempts = []

    @retry_step(counts=3, times=0)
    async def unstable_async():
        attempts.append(1)
        if len(attempts) < 3:
            raise AssertionError("fail")
        return "ok"

    assert await unstable_async() == "ok"
    assert len(attempts) == 3


@allure.feature("pytest工具函数")
@allure.story("重试装饰器")
@allure.title("测试异步函数一直失败时按次数重试并抛出异常")
async def test_retry_step_async_fail_always():
    attempts = []

    @retry_step(counts=2, times=0)
    async def always_fail_async():
        attempts.append(1)
        raise AssertionError("async boom")

    with pytest.raises(AssertionError, match="async boom"):
        await always_fail_async()
    assert len(attempts) == 2
