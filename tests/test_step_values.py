"""测试 har2pytest.step_values 模块中复杂场景步骤取值分析、表达式渲染与代码生成的功能与边界。"""

import allure
import pytest

from har2pytest.config import APIConfig
from har2pytest.models import ParsedRequestInfo
from har2pytest.step_values import (
    ParamSource,
    ScenarioValuePlan,
    StepValueContext,
    _flatten_containers,
    build_scenario_value_plan,
    flatten_data,
    make_step_key,
    render_param_dict_code,
    render_test_data_init,
    source_expression,
)


@pytest.fixture
def default_param_source_config(monkeypatch):
    """将步骤取值相关配置设为默认值（开启跟踪/空忽略名单）。"""
    monkeypatch.setattr(APIConfig, "TRACK_PARAM_SOURCES", classmethod(lambda cls: True))
    monkeypatch.setattr(APIConfig, "PARAM_SOURCE_IGNORE_KEYS", classmethod(lambda cls: []))


def _make_request(query=None, post=None, response=None, path=None):
    """构造带查询参数、请求体与响应的请求信息。"""
    return ParsedRequestInfo(
        url="/api/test",
        method="GET",
        query_params=query or {},
        post_data=post or {},
        path_params=path or {},
        response_content=response,
    )


# ==================== make_step_key ====================


@allure.feature("步骤取值处理")
@allure.story("步骤键生成")
@allure.title("测试步骤键取函数名最后两个字段")
def test_make_step_key_last_two_fields():
    used: set[str] = set()
    assert make_step_key("mgmt_order_orderInfo_orderNo", used) == "orderInfo_orderNo"
    assert make_step_key("mgmt_order_deliverInfo_orderNo", used) == "deliverInfo_orderNo"
    assert make_step_key("sys_api_getAllReturnReasonByType", used) == "api_getAllReturnReasonByType"


@allure.feature("步骤取值处理")
@allure.story("步骤键生成")
@allure.title("测试单字段函数名保留全名")
def test_make_step_key_single_field():
    used: set[str] = set()
    assert make_step_key("applyReturn", used) == "applyReturn"


@allure.feature("步骤取值处理")
@allure.story("步骤键生成")
@allure.title("测试键冲突时向前扩展字段")
def test_make_step_key_conflict():
    used: set[str] = set()
    assert make_step_key("mgmt_order_orderInfo_orderNo", used) == "orderInfo_orderNo"
    # 同名冲突 → 扩展到最后三个字段
    assert make_step_key("mgmt_order_orderInfo_orderNo", used) == "order_orderInfo_orderNo"


@allure.feature("步骤取值处理")
@allure.story("步骤键生成")
@allure.title("测试生成的键写入已用集合")
def test_make_step_key_updates_used():
    used: set[str] = set()
    make_step_key("mgmt_order_return_applyReturn", used)
    assert "return_applyReturn" in used


@allure.feature("步骤取值处理")
@allure.story("步骤键生成")
@allure.title("测试字段扩展耗尽后兜底返回全名")
def test_make_step_key_exhausted_full_name():
    used: set[str] = set()
    assert make_step_key("a_b_c", used) == "b_c"
    assert make_step_key("a_b_c", used) == "a_b_c"
    # 所有候选键用尽后兜底返回全名（即使已占用）
    assert make_step_key("a_b_c", used) == "a_b_c"


# ==================== flatten_data ====================


@allure.feature("步骤取值处理")
@allure.story("响应数据扁平化")
@allure.title("测试嵌套字典展平为路径映射")
def test_flatten_data_nested_dict():
    data = {"a": {"b": 1, "c": "x"}}
    assert flatten_data(data) == {("a", "b"): 1, ("a", "c"): "x"}


@allure.feature("步骤取值处理")
@allure.story("响应数据扁平化")
@allure.title("测试列表元素按索引展平")
def test_flatten_data_with_list():
    data = {"list": [{"k": 1}, {"k": 2}]}
    assert flatten_data(data) == {("list", 0, "k"): 1, ("list", 1, "k"): 2}


@allure.feature("步骤取值处理")
@allure.story("响应数据扁平化")
@allure.title("测试深层结构按最大深度截断")
def test_flatten_data_max_depth():
    data = {"a": {"b": {"c": {"d": {"e": 1}}}}}
    # 默认深度 4：路径长度 4 的 dict（最内层 {"e": 1}）不再展开
    assert flatten_data(data) == {}
    # 深度 5 时最内层叶子可展开
    assert flatten_data(data, max_depth=5) == {("a", "b", "c", "d", "e"): 1}


@allure.feature("步骤取值处理")
@allure.story("响应数据扁平化")
@allure.title("测试列表元素数量截断")
def test_flatten_data_list_item_limit():
    data = {"list": [1, 2, 3, 4, 5]}
    assert flatten_data(data) == {("list", 0): 1, ("list", 1): 2, ("list", 2): 3}


@allure.feature("步骤取值处理")
@allure.story("响应数据扁平化")
@allure.title("测试标量叶子直接记录")
def test_flatten_data_scalar():
    assert flatten_data(5) == {(): 5}
    assert flatten_data(None) == {(): None}


@allure.feature("步骤取值处理")
@allure.story("响应数据扁平化")
@allure.title("测试空容器不产生叶子")
def test_flatten_data_empty_container():
    assert flatten_data({"a": {}, "b": []}) == {}


# ==================== _flatten_containers ====================


@allure.feature("步骤取值处理")
@allure.story("响应容器索引")
@allure.title("测试嵌套容器按路径索引")
def test_flatten_containers_nested():
    data = {"a": {"b": 1}, "list": [{"k": 1}]}
    indexed = _flatten_containers(data)
    assert indexed[()] == data
    assert indexed[("a",)] == {"b": 1}
    assert indexed[("list",)] == [{"k": 1}]
    assert indexed[("list", 0)] == {"k": 1}
    # 叶子不进入容器索引
    assert ("a", "b") not in indexed


@allure.feature("步骤取值处理")
@allure.story("响应容器索引")
@allure.title("测试空容器不索引")
def test_flatten_containers_empty_skipped():
    data = {"a": {}, "b": [], "c": 1}
    indexed = _flatten_containers(data)
    assert indexed == {(): data}
    assert ("a",) not in indexed
    assert ("b",) not in indexed


@allure.feature("步骤取值处理")
@allure.story("响应容器索引")
@allure.title("测试深度与列表元素数量截断")
def test_flatten_containers_depth_and_item_limit():
    data = {
        "a": {"b": {"c": {"d": {"e": 1}}}},
        "list": [{"x": 1}, {"x": 2}, {"x": 3}, {"x": 4}],
    }
    indexed = _flatten_containers(data)
    # 路径长度达到 4 的容器不再向下展开
    assert ("a", "b", "c", "d") in indexed
    assert ("a", "b", "c", "d", "e") not in indexed
    # 列表仅前 3 个元素参与索引
    assert ("list", 2) in indexed
    assert ("list", 3) not in indexed


# ==================== build_scenario_value_plan ====================


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试空值参数保持字面量")
def test_build_plan_empty_value_literal(default_param_source_config):
    req = _make_request(query={"keyword": "", "code": None})
    plan = build_scenario_value_plan([req], ["step_1"])
    sources = plan.steps[0].param_sources
    assert sources["keyword"].kind == "literal"
    assert sources["code"].kind == "literal"


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试空容器参数保持字面量不进入 test_data")
def test_build_plan_empty_container_literal(default_param_source_config):
    """空列表/空字典参数直接传值（如 "giftList": []），不写入 test_data。"""
    req = _make_request(query={"couponList": [], "giftList": [], "extra": {}})
    plan = build_scenario_value_plan([req], ["step_1"])
    sources = plan.steps[0].param_sources
    for name in ("couponList", "giftList", "extra"):
        assert sources[name].kind == "literal"
    assert plan.test_data_values == {}
    code = render_param_dict_code(
        {"giftList": [], "extra": {}}, sources, indent=16
    )
    assert '"giftList": [],' in code
    assert '"extra": {},' in code


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试未命中前序响应的参数提升为用例级 test_data")
def test_build_plan_unmatched_value_test_data(default_param_source_config):
    req = _make_request(query={"remark": "111111111111111"})
    plan = build_scenario_value_plan([req], ["step_1"])
    source = plan.steps[0].param_sources["remark"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"remark": "111111111111111"}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试前序响应同名字段同值引用响应")
def test_build_plan_field_value_match_step_response(default_param_source_config):
    """参数 serialNo="AMT" 与搜索响应 list[0].serialNo 同名同值，应引用。"""
    first = _make_request(response={"code": 200, "data": {"list": [{"serialNo": "AMT"}]}})
    second = _make_request(query={"serialNo": "AMT"})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_action"])
    source = plan.steps[1].param_sources["serialNo"]
    assert source.kind == "step_response"
    assert source.step_key == "step_search"
    # dict 响应整存，引用路径含 list/0 前缀
    assert source.path == ("list", 0, "serialNo")
    assert plan.test_data_values == {}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试同名字段同值匹配不要求值长度")
def test_build_plan_field_value_match_short_value(default_param_source_config):
    """短值参数 qty="1" 与响应 qty=1 同名同值（str 归一），应引用。"""
    first = _make_request(response={"code": 200, "data": {"pageNum": 1, "list": [{"qty": 1}]}})
    second = _make_request(query={"qty": "1"})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    source = plan.steps[1].param_sources["qty"]
    assert source.kind == "step_response"
    assert source.step_key == "step_1"
    assert source.path == ("list", 0, "qty")
    assert plan.test_data_values == {}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试响应字段名与参数名不符时保持用例级 test_data")
def test_build_plan_field_name_mismatch_test_data(default_param_source_config):
    """参数 sourceType="0" 在前序响应中只有 favProFlag/couponFlag=0，字段名不符。"""
    first = _make_request(response={"code": 200, "data": {"favProFlag": 0}})
    second = _make_request(response={"code": 200, "data": {"couponFlag": 0}})
    third = _make_request(query={"sourceType": "0"})
    plan = build_scenario_value_plan([first, second, third], ["step_1", "step_2", "step_3"])
    source = plan.steps[2].param_sources["sourceType"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"sourceType": "0"}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试长值参数在字段名不符时退化为值匹配引用")
def test_build_plan_value_match_fallback_step_response(default_param_source_config):
    """参数 customerCard 与响应字段 cardNo 不同名但长值（≥5 字符）同值且唯一，应引用。"""
    first = _make_request(response={"code": 200, "data": {"cardNo": "3000473488"}})
    second = _make_request(query={"customerCard": "3000473488"})
    plan = build_scenario_value_plan([first, second], ["step_canBuy", "step_action"])
    source = plan.steps[1].param_sources["customerCard"]
    assert source.kind == "step_response"
    assert source.step_key == "step_canBuy"
    assert source.path == ("cardNo",)
    assert plan.test_data_values == {}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试短值参数不参与值匹配兜底")
def test_build_plan_value_match_short_value_test_data(default_param_source_config):
    # 值长度不足兜底门槛且字段名不符时保持 test_data，避免短值同值异义误引用；
    # 测试值取单字符，与兜底最小长度常量解耦
    first = _make_request(response={"code": 200, "data": {"code": "1"}})
    second = _make_request(query={"mark": "1"})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    source = plan.steps[1].param_sources["mark"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"mark": "1"}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试长值在多处出现时不参与值匹配兜底")
def test_build_plan_value_match_ambiguous_test_data(default_param_source_config):
    """同值在单步骤内多处出现时无法判定语义来源，保持 test_data。"""
    first = _make_request(
        response={"code": 200, "data": {"cardNo": "3000473488", "memberCard": "3000473488"}}
    )
    second = _make_request(query={"customerCard": "3000473488"})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    source = plan.steps[1].param_sources["customerCard"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"customerCard": "3000473488"}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试 dict 响应顶层字段可参与长值匹配兜底")
def test_build_plan_value_match_top_level_step_response(default_param_source_config):
    # dict 响应不再裁剪，顶层字段 serialNo 保存后可通过长值匹配被引用
    first = _make_request(
        response={"code": 200, "data": {"serialNo": "AMT12345", "list": [{"id": "26"}]}}
    )
    second = _make_request(query={"productCode": "AMT12345"})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_action"])
    source = plan.steps[1].param_sources["productCode"]
    assert source.kind == "step_response"
    assert source.step_key == "step_search"
    assert source.path == ("serialNo",)
    assert plan.test_data_values == {}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试字段名匹配不区分大小写")
def test_build_plan_field_name_case_insensitive(default_param_source_config):
    """参数 serialNo 匹配响应字段 SerialNo（不区分大小写）。"""
    first = _make_request(response={"code": 200, "data": {"SerialNo": "AMT"}})
    second = _make_request(query={"serialNo": "AMT"})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    source = plan.steps[1].param_sources["serialNo"]
    assert source.kind == "step_response"
    assert source.path == ("SerialNo",)


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试值命中前序响应时引用最早步骤")
def test_build_plan_step_response_earliest(default_param_source_config):
    first = _make_request(response={"code": 200, "data": {"orderNo": "SG001"}})
    second = _make_request(response={"code": 200, "data": {"orderNo": "SG001"}})
    third = _make_request(query={"orderNo": "SG001"})
    plan = build_scenario_value_plan([first, second, third], ["step_1", "step_2", "step_3"])
    source = plan.steps[2].param_sources["orderNo"]
    assert source.kind == "step_response"
    assert source.step_key == "step_1"
    assert source.path == ("orderNo",)


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试第一个步骤的路径参数提升为用例级 test_data")
def test_build_plan_first_step_path_param_test_data(default_param_source_config):
    first = _make_request(path={"orderNo": "SG014000261015000171"})
    plan = build_scenario_value_plan([first], ["orderInfo_orderNo"])
    source = plan.steps[0].param_sources["orderNo"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"orderNo": "SG014000261015000171"}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试后续步骤同名同值参数复用第一个步骤的来源")
def test_build_plan_path_param_step_response(default_param_source_config):
    """second 的 orderNo 与 first 同名同值，复用 first 的 test_data 来源。"""
    first = _make_request(path={"orderNo": "SG001"}, response={"code": 200, "data": {"orderNo": "SG001"}})
    second = _make_request(path={"orderNo": "SG001"})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    source = plan.steps[1].param_sources["orderNo"]
    assert source.kind == "test_data"
    assert source.param_name == "orderNo"


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试忽略名单匹配不区分大小写且支持多键")
def test_build_plan_ignore_keys_literal(default_param_source_config, monkeypatch):
    monkeypatch.setattr(APIConfig, "PARAM_SOURCE_IGNORE_KEYS", classmethod(lambda cls: ["SIGN", "token"]))
    req = _make_request(query={"sign": "abc123", "Token": "xyz", "name": "hello"})
    plan = build_scenario_value_plan([req], ["step_1"])
    sources = plan.steps[0].param_sources
    assert sources["sign"].kind == "literal"
    assert sources["Token"].kind == "literal"
    assert sources["name"].kind == "test_data"


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试步骤键数量少于请求时按键数截断")
def test_build_plan_less_keys_than_requests(default_param_source_config):
    reqs = [_make_request(query={"a": "1"}), _make_request(query={"b": "2"})]
    plan = build_scenario_value_plan(reqs, ["step_1"])
    assert [ctx.step_key for ctx in plan.steps] == ["step_1"]


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试深层列表响应中短值字段名不符时保持用例级 test_data")
def test_build_plan_deep_list_response(default_param_source_config):
    # 参数 reason2 与响应字段 returnReason 不同名且值过短，不参与值匹配兜底
    reason_resp = {
        "code": 200,
        "data": [{"returnReason": "一级原因", "reasonList": [{"returnReason": "二级原因"}]}],
    }
    first = _make_request(response=reason_resp)
    second = _make_request(post={"reason2": "因"})
    plan = build_scenario_value_plan([first, second], ["step_reason", "step_apply"])
    source = plan.steps[1].param_sources["reason2"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"reason2": "因"}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试同名用例级参数冲突时保留首个值")
def test_build_plan_test_data_conflict(default_param_source_config):
    first = _make_request(query={"remark": "1111"})
    second = _make_request(query={"remark": "2222"})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    assert plan.test_data_values == {"remark": "1111"}
    assert plan.steps[1].param_sources["remark"].kind == "test_data"


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试关闭取值跟踪时仍为每个步骤创建上下文")
def test_build_plan_track_disabled(monkeypatch):
    monkeypatch.setattr(APIConfig, "TRACK_PARAM_SOURCES", classmethod(lambda cls: False))
    reqs = [_make_request(query={"a": "1"}), _make_request(query={"b": "2"})]
    plan = build_scenario_value_plan(reqs, ["step_1", "step_2"])
    assert [ctx.step_key for ctx in plan.steps] == ["step_1", "step_2"]
    assert all(not ctx.param_sources for ctx in plan.steps)
    assert plan.test_data_values == {}
    # 关闭跟踪时存储标记保持默认值，存储行由 codegen 侧 track_enabled 短路
    assert all(ctx.store_response is True for ctx in plan.steps)


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试步骤键数量多于请求时按请求截断")
def test_build_plan_more_keys_than_requests(default_param_source_config):
    req = _make_request(query={"a": "12345"})
    plan = build_scenario_value_plan([req], ["step_1", "step_2"])
    assert [ctx.step_key for ctx in plan.steps] == ["step_1"]


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试同一 API 多次调用时同名同值参数复用第一个来源")
def test_build_plan_duplicate_api_same_step_key(default_param_source_config):
    """同一 API 函数被调用两次时，调用方应传入相同的步骤键。"""
    first = _make_request(
        query={"orderNo": "SG001"},
        response={"data": {"orderNo": "SG001", "status": "shipped"}},
    )
    second = _make_request(query={"remark": "1111"})
    third = _make_request(query={"orderNo": "SG001"})
    # 第一和第三个请求调用同一 API，步骤键均为 "orderInfo_orderNo"
    plan = build_scenario_value_plan(
        [first, second, third],
        ["orderInfo_orderNo", "remark", "orderInfo_orderNo"],
    )
    assert plan.steps[0].step_key == "orderInfo_orderNo"
    assert plan.steps[2].step_key == "orderInfo_orderNo"
    # 第三个请求的 orderNo 与第一个同名同值，复用第一个的 test_data 来源
    source = plan.steps[2].param_sources["orderNo"]
    assert source.kind == "test_data"
    assert source.param_name == "orderNo"


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试同名同值参数复用优先于值匹配兜底")
def test_build_plan_same_param_reuse_first_source(default_param_source_config):
    """第二次调用的 usrId 与第一次同名同值，复用 test_data['usrId']，
    不引用响应中同值异名字段 memberId。"""
    first = _make_request(
        query={"usrId": "800064658"},
        response={"code": 200, "data": {"memberId": "800064658"}},
    )
    second = _make_request(query={"usrId": "800064658"})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    source = plan.steps[1].param_sources["usrId"]
    assert source.kind == "test_data"
    assert source.param_name == "usrId"
    assert plan.test_data_values == {"usrId": "800064658"}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试 dict 参数与响应子结构相等时引用响应（键顺序无关）")
def test_build_plan_dict_container_step_response(default_param_source_config):
    first = _make_request(
        response={"code": 200, "data": {"product": {"id": "1", "name": "完美牌"}}}
    )
    second = _make_request(post={"product": {"name": "完美牌", "id": "1"}})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_settle"])
    source = plan.steps[1].param_sources["product"]
    assert source.kind == "step_response"
    assert source.step_key == "step_search"
    assert source.path == ("product",)


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试 list 参数与响应子结构字段相同时生成字段级投影")
def test_build_plan_list_container_step_response(default_param_source_config):
    """参数名 productList 与响应字段 items 不符，但元素字段同名同值，生成全引用投影。"""
    first = _make_request(response={"code": 200, "data": {"items": [{"id": "1", "qty": 2}]}})
    second = _make_request(post={"productList": [{"qty": 2, "id": "1"}]})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_settle"])
    source = plan.steps[1].param_sources["productList"]
    assert source.kind == "container_projection"
    assert source.step_key == "step_search"
    assert source.projection == [
        {"qty": ("ref", ("items", 0, "qty")), "id": ("ref", ("items", 0, "id"))}
    ]
    assert plan.test_data_values == {}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试容器与响应部分一致时生成字段级投影引用")
def test_build_plan_container_partial_match_projection(default_param_source_config):
    """搜索响应商品与结算请求商品部分字段不同，相等字段引用响应、其余保持原值。"""
    search_resp = {
        "code": 200,
        "data": {"list": [{"id": "26", "retailPrice": 200.0, "activityPrice": None}]},
    }
    first = _make_request(response=search_resp)
    settle_product = {"id": "26", "retailPrice": 200, "activityPrice": 200, "number": 1}
    second = _make_request(post={"productList": [settle_product]})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_settle"])
    source = plan.steps[1].param_sources["productList"]
    assert source.kind == "container_projection"
    assert source.step_key == "step_search"
    # 相等字段引用响应路径（200 == 200.0 数值兼容），不一致字段同名同值
    # 时提升为 test_data 引用（activityPrice=200、number=1 全用例唯一）
    assert source.projection == [
        {
            "id": ("ref", ("list", 0, "id")),
            "retailPrice": ("ref", ("list", 0, "retailPrice")),
            "activityPrice": ("test_data", "activityPrice"),
            "number": ("test_data", "number"),
        }
    ]
    assert plan.test_data_values == {"activityPrice": 200, "number": 1}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试投影不一致字段同名同值时提升为 test_data 引用")
def test_build_plan_projection_literal_same_value_promoted(default_param_source_config):
    """购买数量 quantity=1 在多个步骤同名同值，提升 test_data 集中修改。"""
    search_resp = {"code": 200, "data": {"list": [{"serialNo": "AMT", "title": "完美牌"}]}}
    first = _make_request(response=search_resp)
    product = {"serialNo": "AMT", "quantity": 1}
    second = _make_request(post={"productList": [product]})
    third = _make_request(post={"productList": [product]})
    plan = build_scenario_value_plan(
        [first, second, third], ["step_search", "step_settle", "step_commit"]
    )
    for step_ctx in plan.steps[1:]:
        source = step_ctx.param_sources["productList"]
        assert source.projection == [
            {"serialNo": ("ref", ("list", 0, "serialNo")), "quantity": ("test_data", "quantity")}
        ]
    assert plan.test_data_values == {"quantity": 1}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试投影不一致字段同名不同值时保持字面量")
def test_build_plan_projection_literal_diff_value_kept(default_param_source_config):
    """number 在不同步骤为 19 与 1，test_data 键冲突无法表达，保持字面量。"""
    search_resp = {"code": 200, "data": {"list": [{"serialNo": "AMT", "title": "完美牌"}]}}
    first = _make_request(response=search_resp)
    second = _make_request(post={"productList": [{"serialNo": "AMT", "number": 19}]})
    third = _make_request(post={"productList": [{"serialNo": "AMT", "number": 1}]})
    plan = build_scenario_value_plan(
        [first, second, third], ["step_search", "step_settle", "step_commit"]
    )
    for step_ctx, number in zip(plan.steps[1:], (19, 1)):
        source = step_ctx.param_sources["productList"]
        assert source.projection == [
            {"serialNo": ("ref", ("list", 0, "serialNo")), "number": ("literal", number)}
        ]
    assert plan.test_data_values == {}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试投影字面量与顶层用例级参数同名不同值时保持字面量")
def test_build_plan_projection_literal_top_level_conflict_kept(default_param_source_config):
    # 投影 quantity=1 与顶层用例级参数 quantity=5 同名不同值，提升会破坏
    # test_data 键语义，保持投影字面量
    search_resp = {"code": 200, "data": {"list": [{"serialNo": "AMT", "title": "完美牌"}]}}
    first = _make_request(response=search_resp)
    second = _make_request(post={"productList": [{"serialNo": "AMT", "quantity": 1}], "quantity": 5})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_settle"])
    source = plan.steps[1].param_sources["productList"]
    assert source.projection == [
        {"serialNo": ("ref", ("list", 0, "serialNo")), "quantity": ("literal", 1)}
    ]
    assert plan.test_data_values == {"quantity": 5}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试匹配叶子不足一半时保持用例级 test_data")
def test_build_plan_container_weak_match_test_data(default_param_source_config):
    """仅有少量字段相等时不拆散为投影，保持 test_data 集中管理。"""
    search_resp = {"code": 200, "data": {"list": [{"id": "26", "name": "完美"}]}}
    first = _make_request(response=search_resp)
    settle_product = {"id": "26", "price": 200, "qty": 1, "note": "1111"}
    second = _make_request(post={"productList": [settle_product]})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_settle"])
    source = plan.steps[1].param_sources["productList"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"productList": [settle_product]}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试纯叶子列表元素唯一出现在响应时生成元素级引用投影")
def test_build_plan_list_leaf_projection(default_param_source_config):
    """productCodes ["AMT"] 的元素唯一出现在搜索响应 list[0].serialNo，应引用。"""
    search_resp = {
        "code": 200,
        "data": {"list": [{"serialNo": "AMT", "title": "完美牌芦荟王浆矿物片"}]},
    }
    first = _make_request(response=search_resp)
    second = _make_request(post={"productCodes": ["AMT"]})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_action"])
    source = plan.steps[1].param_sources["productCodes"]
    assert source.kind == "container_projection"
    assert source.step_key == "step_search"
    assert source.projection == [("ref", ("list", 0, "serialNo"))]
    # 投影参数不再进入用例级 test_data
    assert plan.test_data_values == {}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试列表元素在响应中多次出现时保持用例级 test_data")
def test_build_plan_list_leaf_ambiguous_test_data(default_param_source_config):
    # 值 "1" 在响应中出现多次，元素级引用会误匹配，应保持 test_data
    search_resp = {"code": 200, "data": {"pageNum": 1, "list": [{"qty": 1}]}}
    first = _make_request(response=search_resp)
    second = _make_request(post={"productCodes": ["1"]})
    plan = build_scenario_value_plan([first, second], ["step_search", "step_action"])
    source = plan.steps[1].param_sources["productCodes"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"productCodes": ["1"]}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试列表元素引用命中不同步骤时整体保持用例级 test_data")
def test_build_plan_list_leaf_cross_step_test_data(default_param_source_config):
    # 渲染只支持单一步骤键，两个元素分别唯一出现在不同步骤 → 整体放弃
    first = _make_request(response={"data": {"codeA": "AMT123"}})
    second = _make_request(response={"data": {"codeB": "BMT456"}})
    third = _make_request(post={"productCodes": ["AMT123", "BMT456"]})
    plan = build_scenario_value_plan([first, second, third], ["step_1", "step_2", "step_3"])
    source = plan.steps[2].param_sources["productCodes"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"productCodes": ["AMT123", "BMT456"]}


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试列表元素引用比例不足一半时保持用例级 test_data")
def test_build_plan_list_leaf_low_ratio_test_data(default_param_source_config):
    # 3 个元素仅 1 个命中引用，比例 1/3 < 50% → 整体保持 test_data
    first = _make_request(response={"data": {"codeA": "AMT123"}})
    second = _make_request(post={"productCodes": ["AMT123", "X9", "Y8"]})
    plan = build_scenario_value_plan([first, second], ["step_1", "step_2"])
    source = plan.steps[1].param_sources["productCodes"]
    assert source.kind == "test_data"
    assert plan.test_data_values == {"productCodes": ["AMT123", "X9", "Y8"]}


# ==================== 响应整存引用 ====================


@allure.feature("步骤取值处理")
@allure.story("场景取值计划")
@allure.title("测试 list 响应整存后叶子引用含列表索引前缀")
def test_build_plan_list_response_leaf_reference(default_param_source_config):
    """data 是列表时整存，引用路径含 [0] 前缀（保留全部元素数据）。"""
    first = _make_request(response={"code": 200, "data": [{"returnReason": "一级原因"}]})
    second = _make_request(query={"returnReason": "一级原因"})
    plan = build_scenario_value_plan([first, second], ["step_reason", "step_apply"])
    source = plan.steps[1].param_sources["returnReason"]
    assert source.kind == "step_response"
    assert source.step_key == "step_reason"
    assert source.path == (0, "returnReason")


# ==================== source_expression ====================


@allure.feature("步骤取值处理")
@allure.story("取值表达式渲染")
@allure.title("测试用例级参数渲染为 test_data 引用")
def test_source_expression_test_data():
    source = ParamSource(kind="test_data", param_name="orderNo", value="SG001")
    assert source_expression(source) == "test_data['orderNo']"


@allure.feature("步骤取值处理")
@allure.story("取值表达式渲染")
@allure.title("测试步骤响应渲染为含列表索引的引用")
def test_source_expression_step_response():
    source = ParamSource(
        kind="step_response",
        param_name="reason2",
        step_key="step_reason",
        path=(0, "reasonList", 0, "returnReason"),
    )
    assert (
        source_expression(source)
        == "test_data['step_reason'][0]['reasonList'][0]['returnReason']"
    )


@allure.feature("步骤取值处理")
@allure.story("取值表达式渲染")
@allure.title("测试字面量来源渲染抛出异常")
def test_source_expression_literal_raises():
    with pytest.raises(ValueError, match="非引用型"):
        source_expression(ParamSource(kind="literal", param_name="a"))


# ==================== render_test_data_init ====================


@allure.feature("步骤取值处理")
@allure.story("test_data 初始化渲染")
@allure.title("测试无用例级参数时渲染空字典初始化")
def test_render_test_data_init_empty():
    plan = ScenarioValuePlan()
    lines = render_test_data_init(plan)
    assert lines[1] == " " * 8 + "test_data: dict = {"
    assert lines[2] == " " * 8 + "}"


@allure.feature("步骤取值处理")
@allure.story("test_data 初始化渲染")
@allure.title("测试渲染 test_data 初始化代码行")
def test_render_test_data_init_normal():
    plan = ScenarioValuePlan(test_data_values={"orderNo": "SG001", "applySource": "2"})
    lines = render_test_data_init(plan, indent=8)
    assert lines[0] == " " * 8 + "# 初始化测试数据字典，用于在步骤间传递数据"
    assert lines[1] == " " * 8 + "test_data: dict = {"
    assert lines[2] == f"{' ' * 12}'orderNo': \"SG001\","
    assert lines[3] == f"{' ' * 12}'applySource': \"2\","
    assert lines[4] == " " * 8 + "}"
    assert lines[5] == ""


# ==================== render_param_dict_code ====================


@allure.feature("步骤取值处理")
@allure.story("步骤参数字典渲染")
@allure.title("测试空字典渲染为花括号")
def test_render_param_dict_code_empty():
    assert render_param_dict_code({}, {}) == "{}"


@allure.feature("步骤取值处理")
@allure.story("步骤参数字典渲染")
@allure.title("测试混合来源渲染为字面量与引用表达式")
def test_render_param_dict_code_mixed():
    values = {
        "orderNo": "SG001",
        "reason1Remark": "111111",
        "empty": "",
    }
    sources = {
        "orderNo": ParamSource(
            kind="step_response", param_name="orderNo", step_key="step_1", path=("orderNo",)
        ),
        "reason1Remark": ParamSource(kind="test_data", param_name="reason1Remark"),
        "empty": ParamSource(kind="literal", param_name="empty", value=""),
    }
    code = render_param_dict_code(values, sources, indent=16)
    lines = code.split("\n")
    assert lines[0] == "{"
    assert lines[1] == f"{' ' * 16}\"orderNo\": test_data['step_1']['orderNo'],"
    assert lines[2] == f"{' ' * 16}\"reason1Remark\": test_data['reason1Remark'],"
    assert lines[3] == f"{' ' * 16}\"empty\": \"\","
    assert lines[4] == " " * 12 + "}"


@allure.feature("步骤取值处理")
@allure.story("步骤参数字典渲染")
@allure.title("测试投影来源渲染为引用与字面量混合的多行结构")
def test_render_param_dict_code_projection():
    values = {"productList": [{"id": "26", "qty": 1}]}
    sources = {
        "productList": ParamSource(
            kind="container_projection",
            param_name="productList",
            step_key="step_search",
            projection=[{"id": ("ref", ("list", 0, "id")), "qty": ("literal", 1)}],
        ),
    }
    code = render_param_dict_code(values, sources, indent=16)
    lines = code.split("\n")
    assert lines[0] == "{"
    assert lines[1] == f"{' ' * 16}\"productList\": ["
    assert lines[2] == f"{' ' * 24}{{"
    assert lines[3] == f"{' ' * 28}\"id\": test_data['step_search']['list'][0]['id'],"
    assert lines[4] == f"{' ' * 28}\"qty\": 1,"
    assert lines[5] == f"{' ' * 24}}},"
    assert lines[6] == f"{' ' * 20}],"
    assert lines[7] == " " * 12 + "}"


@allure.feature("步骤取值处理")
@allure.story("步骤参数字典渲染")
@allure.title("测试投影中提升叶子渲染为用例级 test_data 引用")
def test_render_param_dict_code_projection_test_data_leaf():
    values = {"productList": [{"id": "26"}]}
    sources = {
        "productList": ParamSource(
            kind="container_projection",
            param_name="productList",
            step_key="step_search",
            projection=[{"id": ("test_data", "id")}],
        ),
    }
    code = render_param_dict_code(values, sources, indent=16)
    assert "test_data['id']" in code


@allure.feature("步骤取值处理")
@allure.story("步骤参数字典渲染")
@allure.title("测试未提供来源的参数保持字面量")
def test_render_param_dict_code_no_sources():
    values = {"name": "hello", "count": 1}
    code = render_param_dict_code(values, {}, indent=16)
    assert '"name": "hello",' in code
    assert '"count": 1,' in code


# ==================== StepValueContext ====================


@allure.feature("步骤取值处理")
@allure.story("步骤取值上下文")
@allure.title("测试步骤取值上下文默认字段")
def test_step_value_context_defaults():
    ctx = StepValueContext(step_key="step_1")
    assert ctx.step_key == "step_1"
    assert ctx.param_sources == {}
    assert ctx.flattened == {}
    assert ctx.container_index == {}
    assert ctx.store_response is True


# ==================== store_response 引用分析 ====================


@allure.feature("步骤取值处理")
@allure.story("响应存储控制")
@allure.title("测试被后续引用的响应标记为需存储")
def test_build_plan_store_response_referenced(default_param_source_config):
    # 步骤 2 参数 orderNo 与步骤 1 参数同名不同值 → 不复用；
    # 字段名+值双匹配步骤 1 响应 → step_response 引用 → 步骤 1 需存储
    requests = [
        _make_request(post={"orderNo": "abc"}, response={"data": {"orderNo": "abc123"}}),
        _make_request(post={"orderNo": "abc123"}, response={"data": {"orderNo": "abc123"}}),
    ]
    plan = build_scenario_value_plan(requests, ["orderInfo_orderNo", "trade_orderCommit"])
    assert plan.steps[0].store_response is True
    assert plan.steps[1].store_response is False


@allure.feature("步骤取值处理")
@allure.story("响应存储控制")
@allure.title("测试未被引用的响应标记为不存储")
def test_build_plan_store_response_unreferenced(default_param_source_config):
    # 步骤 2 参数 other 与步骤 1 响应无匹配（短值不参与兜底）→ 步骤 1 响应未被引用
    requests = [
        _make_request(post={"orderNo": "abc"}, response={"data": {"remark": "ok"}}),
        _make_request(post={"other": 1}, response={"data": {}}),
    ]
    plan = build_scenario_value_plan(requests, ["step_a", "step_b"])
    assert plan.steps[0].store_response is False
    assert plan.steps[1].store_response is False


@allure.feature("步骤取值处理")
@allure.story("响应存储控制")
@allure.title("测试容器投影引用同样标记源步骤需存储")
def test_build_plan_store_response_projection_source(default_param_source_config):
    # 步骤 2 的列表参数对步骤 1 响应做元素级投影 → 步骤 1 需存储
    requests = [
        _make_request(post={}, response={"data": {"list": [{"id": "AMT", "name": "x"}]}}),
        _make_request(post={"productCodes": ["AMT"]}, response={"data": {}}),
    ]
    plan = build_scenario_value_plan(requests, ["product_search", "step_b"])
    assert plan.steps[0].store_response is True
    assert plan.steps[1].store_response is False
