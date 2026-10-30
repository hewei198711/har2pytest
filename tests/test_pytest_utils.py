"""测试 har2pytest.pytest_utils 模块中 retry_step 重试装饰器的同步/异步重试、异常类型过滤与日志输出，以及 collect_list_query_data 响应收集函数的功能与边界。"""

import logging

import allure
import pytest

from har2pytest.pytest_utils import collect_list_query_data, retry_step

# ==================== retry_step 重试装饰器测试 ====================


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
def test_retry_step_sync_fail_always(caplog):
    caplog.set_level(logging.WARNING, logger="har2pytest")
    attempts = []

    @retry_step(counts=3, times=0)
    def always_fail():
        attempts.append(1)
        raise AssertionError("boom")

    with pytest.raises(AssertionError, match="boom"):
        always_fail()
    # 总执行次数 = counts（含首次）
    assert len(attempts) == 3
    # 最后一次失败时日志提示“重试次数已用完”
    assert "重试次数已用完" in caplog.text


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


@allure.feature("pytest工具函数")
@allure.story("重试装饰器")
@allure.title("测试默认参数 counts=2 时执行两次后成功")
async def test_retry_step_default_counts():
    attempts = []

    @retry_step(times=0)
    async def flaky():
        attempts.append(1)
        if len(attempts) < 2:
            raise AssertionError("first fail")
        return "ok"

    assert await flaky() == "ok"
    assert len(attempts) == 2


# ==================== collect_list_query_data 响应收集函数测试 ====================


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试精确匹配优先于前缀模糊匹配")
def test_collect_list_query_data_exact_match_priority():
    list_query_data = {"operator": "", "ruleName": ""}
    collect_list_query_data(
        {"data": {"list": [{"operator": "OP-100", "operatorNo": "NO-1", "ruleName": "R1"}]}},
        list_query_data,
    )
    # 响应同时存在同名与同前缀字段时，精确匹配值获胜
    assert list_query_data["operator"] == "OP-100"
    assert list_query_data["ruleName"] == "R1"


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试无精确匹配时降级前缀模糊匹配且取第一个")
def test_collect_list_query_data_fuzzy_fallback_first_match():
    list_query_data = {"operator": "", "ruleName": ""}
    collect_list_query_data(
        {"data": {"list": [{"operatorNo": "NO-2", "operatorName": "张三", "ruleName": "R2"}]}},
        list_query_data,
    )
    # 参数 operator 无同名字段，降级前缀匹配 operatorNo/operatorName，取遍历第一个
    assert list_query_data["operator"] == "NO-2"
    assert list_query_data["ruleName"] == "R2"


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试已收集参数不再被后续记录覆盖且响应值覆盖录制值")
def test_collect_list_query_data_first_record_wins():
    # 初始录制值非空，验证响应值优先覆盖；后续记录的同名/同前缀字段不再覆盖首条记录值
    list_query_data = {"operator": "RECORDED", "ruleName": "RECORDED-RULE"}
    collect_list_query_data(
        {
            "data": {
                "list": [
                    {"operator": "OP-3", "ruleName": "R3"},
                    {"operatorNo": "NO-3", "ruleName": "R3-2"},
                ]
            }
        },
        list_query_data,
    )
    assert list_query_data["operator"] == "OP-3"
    assert list_query_data["ruleName"] == "R3"


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试响应无数据时保持原值且非参数键不收集")
def test_collect_list_query_data_empty_response_keeps_original():
    list_query_data = {"operator": "OP-0", "ruleName": "R0"}
    # 响应 data 缺失/列表为空/字段值空均不更新
    collect_list_query_data({"code": 200}, list_query_data)
    collect_list_query_data({"data": {"list": []}}, list_query_data)
    collect_list_query_data(
        {"data": {"list": [{"operator": "", "otherField": "X"}]}},
        list_query_data,
    )
    assert list_query_data == {"operator": "OP-0", "ruleName": "R0"}
