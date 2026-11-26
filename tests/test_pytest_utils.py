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
@allure.title("测试单响应收集各匹配形态")
@pytest.mark.parametrize(
    "initial,response,expected",
    [
        # 响应同时存在同名与同前缀字段时，精确匹配值获胜
        pytest.param(
            {"operator": "", "ruleName": ""},
            {"data": {"list": [{"operator": "OP-100", "operatorNo": "NO-1", "ruleName": "R1"}]}},
            {"operator": "OP-100", "ruleName": "R1"},
            id="精确优先于前缀模糊",
        ),
        # 参数 operator 无同名字段，降级前缀匹配 operatorNo/operatorName，取遍历第一个
        pytest.param(
            {"operator": "", "ruleName": ""},
            {"data": {"list": [{"operatorNo": "NO-2", "operatorName": "张三", "ruleName": "R2"}]}},
            {"operator": "NO-2", "ruleName": "R2"},
            id="无精确降级前缀取第一个",
        ),
        pytest.param(
            {"demoShop": "", "demoType": ""},
            {"data": {"records": [{"demoShop": "SHOP01", "demoType": 0}]}},
            {"demoShop": "SHOP01", "demoType": 0},
            id="records键下收集",
        ),
        # 参数 demoCodeList 包含响应字段 demoCode，值包装为单元素列表
        pytest.param(
            {"demoCodeList": [], "demoShop": ""},
            {"data": {"records": [{"demoCode": "00001", "demoShop": "SHOP01"}]}},
            {"demoCodeList": ["00001"], "demoShop": "SHOP01"},
            id="反向包含包装列表",
        ),
        # 参数 demoQueryType 包含响应字段 demoQuery，同样反向命中并包装为列表
        pytest.param(
            {"demoQueryType": [0, 1, 2, 3, 4], "client": ""},
            {"data": {"records": [{"demoQuery": "演示查询文本", "client": "PC"}]}},
            {"demoQueryType": ["演示查询文本"], "client": "PC"},
            id="反向包含任意参数",
        ),
        # current 与 createdAt 无前缀包含关系，不收集
        pytest.param(
            {"current": 1, "client": ""},
            {"data": {"records": [{"createdAt": "2026-01-01 00:00:00", "client": "PC"}]}},
            {"current": 1, "client": "PC"},
            id="无包含关系不互配",
        ),
        # 参数 companyList：响应 companyList 字段精确命中；无同名字段时反向命中 company
        pytest.param(
            {"companyList": [], "demoCodeList": []},
            {"data": {"records": [{"companyList": "A", "demoCode": "00001"}]}},
            {"companyList": "A", "demoCodeList": ["00001"]},
            id="精确优先于反向包含",
        ),
        # 标量声明（数值基线）不参与反向匹配：响应只有汇总字段 yearReturnAmt/yearReturnCount，
        # 不得反向命中 End/Start 把标量包成 [v]（两条记录各取一值还会拼出倒挂范围），基线保持
        pytest.param(
            {"yearReturnAmtEnd": 10000, "yearReturnAmtStart": 1000, "yearReturnCountEnd": 5, "yearReturnCountStart": 1},
            {"data": {"records": [{"yearReturnAmt": 500, "yearReturnCount": 2}, {"yearReturnAmt": 800, "yearReturnCount": 9}]}},
            {"yearReturnAmtEnd": 10000, "yearReturnAmtStart": 1000, "yearReturnCountEnd": 5, "yearReturnCountStart": 1},
            id="标量声明不参与反向匹配",
        ),
        # api.json 声明 null（生成基线 None）同为标量：不被汇总字段反向收集，也不得包成 [v]
        pytest.param(
            {"yearReturnAmtEnd": None, "yearReturnAmtStart": None, "demoCodeList": []},
            {"data": {"records": [{"yearReturnAmt": 500, "demoCode": "00001"}]}},
            {"yearReturnAmtEnd": None, "yearReturnAmtStart": None, "demoCodeList": ["00001"]},
            id="null声明不参与反向匹配而数组声明正常包装",
        ),
        # 标量声明仅排除反向匹配：响应存在同名字段时精确收集仍生效
        pytest.param(
            {"yearReturnAmtEnd": 10000, "yearReturnAmtStart": 1000},
            {"data": {"records": [{"yearReturnAmtEnd": 600, "yearReturnAmtStart": 100}]}},
            {"yearReturnAmtEnd": 600, "yearReturnAmtStart": 100},
            id="标量声明精确匹配仍收集",
        ),
    ],
)
def test_collect_list_query_data_single_response_forms(initial, response, expected):
    list_query_data = dict(initial)
    collect_list_query_data(response, list_query_data)
    assert list_query_data == expected


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
@allure.title("测试显式字段映射优先于三级匹配")
def test_collect_list_query_data_field_map():
    # 参数名 like 与响应字段 invoiceSensitive 无任何子串包含关系，
    # 三级匹配全部落空；field_map 显式映射后才能收集到值
    list_query_data = {"like": "", "pageNum": 1}
    collect_list_query_data(
        {"data": {"list": [{"id": "50", "invoiceSensitive": "决赛"}]}},
        list_query_data,
        field_map={"like": "invoiceSensitive"},
    )
    assert list_query_data["like"] == "决赛"
    assert list_query_data["pageNum"] == 1
    # 未传 field_map 时收集不到（无子串关系）
    list_query_data = {"like": "", "pageNum": 1}
    collect_list_query_data(
        {"data": {"list": [{"id": "50", "invoiceSensitive": "决赛"}]}},
        list_query_data,
    )
    assert list_query_data["like"] == ""


# ==================== extract_list_items 明细提取函数测试 ====================


@allure.feature("pytest工具函数")
@allure.story("明细提取函数")
@allure.title("测试明细提取各形态")
@pytest.mark.parametrize(
    "resp_data,expected",
    [
        # list/lists 键存在时直接返回，不做 records 兜底
        pytest.param({"lists": [{"a": 1}], "records": [{"b": 2}]}, [{"a": 1}], id="lists键优先"),
        pytest.param({"list": [1, 2], "records": [{"b": 2}]}, [1, 2], id="list键优先"),
        pytest.param({"records": [{"demoField": "V1"}]}, [{"demoField": "V1"}], id="records兜底"),
        pytest.param({"rows": [{"a": 1}, {"a": 2}]}, [{"a": 1}, {"a": 2}], id="rows兜底"),
        pytest.param(None, [], id="非dict返回空"),
        pytest.param({"total": 1}, [], id="无明细列表返回空"),
        pytest.param({"ids": [1, 2]}, [], id="仅非dict元素列表返回空"),
        pytest.param({"records": []}, [], id="空明细列表返回空"),
        # 列表嵌套在分页对象内（如 data.secondCouponInfos.list）时递归查找
        pytest.param(
            {"secondCouponInfos": {"pageNum": 1, "total": 237, "list": [{"orderNo": "A1"}]}},
            [{"orderNo": "A1"}],
            id="嵌套分页对象内list递归",
        ),
        pytest.param(
            {"secondCouponInfos": {"total": 0, "list": []}},
            [],
            id="嵌套分页对象内空list返回空",
        ),
        pytest.param({"page": {"total": 0}}, [], id="嵌套对象无列表返回空"),
    ],
)
def test_extract_list_items_forms(resp_data, expected):
    assert extract_list_items(resp_data) == expected
