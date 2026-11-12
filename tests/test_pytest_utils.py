"""测试 har2pytest.pytest_utils 模块中 retry_step 重试装饰器的同步/异步重试、异常类型过滤与日志输出，以及 collect_list_query_data 响应收集函数与 extract_list_items 明细提取的功能与边界。"""

import logging

import allure
import pytest

from har2pytest.config import APIConfig
from har2pytest.pytest_utils import collect_list_query_data, extract_list_items, retry_step

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


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试明细列表在records键下也能收集")
def test_collect_list_query_data_records_key():
    list_query_data = {"demoShop": "", "demoType": ""}
    collect_list_query_data(
        {"data": {"records": [{"demoShop": "SHOP01", "demoType": 0}]}},
        list_query_data,
    )
    assert list_query_data["demoShop"] == "SHOP01"
    assert list_query_data["demoType"] == 0


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试时间参数不参与响应收集")
def test_collect_list_query_data_skips_time_params(monkeypatch):
    if APIConfig._config is None:
        APIConfig._config = APIConfig._load_config()
    monkeypatch.setitem(APIConfig._config, "TIME_PARAMS", ["timestart", "timeend"])
    list_query_data = {
        "commitTimeEnd": "2026-11-05",
        "commitTimeStart": "2026-01-01",
        "payTimeEnd": "2026-11-05",
        "payTimeStart": "2026-01-01",
        "operator": "",
    }
    collect_list_query_data(
        {
            "data": {
                "list": [
                    {"commitTime": 1758872819000, "payTime": 1758872822000, "operator": "OP-1"},
                    {"commitTime": 1758872793000, "payTime": 1758872795000},
                ]
            }
        },
        list_query_data,
    )
    # 时间参数保持 datetime 计算值，不被响应记录中的 commitTime/payTime 时间戳污染
    assert list_query_data["commitTimeStart"] == "2026-01-01"
    assert list_query_data["commitTimeEnd"] == "2026-11-05"
    assert list_query_data["payTimeStart"] == "2026-01-01"
    assert list_query_data["payTimeEnd"] == "2026-11-05"
    # 非时间参数正常收集
    assert list_query_data["operator"] == "OP-1"


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试参数名包含响应字段名时反向匹配并包装为列表")
def test_collect_list_query_data_reverse_include_wrap():
    list_query_data = {"demoCodeList": [], "demoShop": ""}
    collect_list_query_data(
        {"data": {"records": [{"demoCode": "00001", "demoShop": "SHOP01"}]}},
        list_query_data,
    )
    # 参数 demoCodeList 包含响应字段 demoCode，值包装为单元素列表
    assert list_query_data["demoCodeList"] == ["00001"]
    assert list_query_data["demoShop"] == "SHOP01"


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试参数名包含响应字段名时任意参数均反向匹配")
def test_collect_list_query_data_reverse_include_generic():
    # 参数 demoQueryType 包含响应字段 demoQuery，同样反向命中并包装为列表
    list_query_data = {"demoQueryType": [0, 1, 2, 3, 4], "client": ""}
    collect_list_query_data(
        {"data": {"records": [{"demoQuery": "演示查询文本", "client": "PC"}]}},
        list_query_data,
    )
    assert list_query_data["demoQueryType"] == ["演示查询文本"]
    assert list_query_data["client"] == "PC"


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试无包含关系的字段不互相匹配")
def test_collect_list_query_data_no_prefix_relation():
    # current 与 createdAt 无前缀包含关系，不收集
    list_query_data = {"current": 1, "client": ""}
    collect_list_query_data(
        {"data": {"records": [{"createdAt": "2026-01-01 00:00:00", "client": "PC"}]}},
        list_query_data,
    )
    assert list_query_data["current"] == 1
    assert list_query_data["client"] == "PC"


@allure.feature("pytest工具函数")
@allure.story("响应收集函数")
@allure.title("测试精确匹配优先于反向包含匹配")
def test_collect_list_query_data_exact_before_reverse_include():
    # 参数 companyList：响应 companyList 字段精确命中；无同名字段时反向命中 company
    list_query_data = {"companyList": [], "demoCodeList": []}
    collect_list_query_data(
        {"data": {"records": [{"companyList": "A", "demoCode": "00001"}]}},
        list_query_data,
    )
    assert list_query_data["companyList"] == "A"
    assert list_query_data["demoCodeList"] == ["00001"]


# ==================== extract_list_items 明细提取函数测试 ====================


@allure.feature("pytest工具函数")
@allure.story("明细提取函数")
@allure.title("测试lists/list键优先提取")
def test_extract_list_items_list_key_priority():
    # list/lists 键存在时直接返回，不做 records 兜底
    assert extract_list_items({"lists": [{"a": 1}], "records": [{"b": 2}]}) == [{"a": 1}]
    assert extract_list_items({"list": [1, 2], "records": [{"b": 2}]}) == [1, 2]


@allure.feature("pytest工具函数")
@allure.story("明细提取函数")
@allure.title("测试无lists/list键时兜底提取records等命名")
def test_extract_list_items_records_fallback():
    assert extract_list_items({"records": [{"demoField": "V1"}]}) == [{"demoField": "V1"}]
    assert extract_list_items({"rows": [{"a": 1}, {"a": 2}]}) == [{"a": 1}, {"a": 2}]


@allure.feature("pytest工具函数")
@allure.story("明细提取函数")
@allure.title("测试非dict、无明细列表或仅非dict元素列表返回空")
def test_extract_list_items_empty_fallback():
    assert extract_list_items(None) == []
    assert extract_list_items({"total": 1}) == []
    assert extract_list_items({"ids": [1, 2]}) == []
    assert extract_list_items({"records": []}) == []
