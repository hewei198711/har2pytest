"""测试数值范围对参数支持（非时间的 Start/End 配对，如金额/次数区间）。

覆盖五段链路：utils.build_value_pairs 类型判据识别（数值标量声明 +
后缀配对，时间对成员排除）→ api_metadata 落盘 value_pairs →
parse_api_file 读取 → ValuePairContext 消费 → 生成形态（list_query_data
None 基线 / test_0 聚合传参 / 区间组合用例与区间断言）与
collect_list_query_data 的 min/max 聚合通道。备注均为演示占位，不含真实业务信息。
"""

import allure
import pytest

from har2pytest.api_metadata import VALUE_PAIRS_FIELD, write_api_metadata
from har2pytest.config import APIConfig
from har2pytest.parametrized_codegen import (
    gen_batch_parametrized_test_methods,
    gen_list_query_data_class_attr,
    gen_test_0_collect_response_data,
)
from har2pytest.pytest_utils import collect_list_query_data
from har2pytest.testcase_generator import TestCaseGenerator
from har2pytest.time_pair import TimePairContext
from har2pytest.utils import build_value_pairs, clear_api_file_cache, parse_api_file
from har2pytest.value_pair import ValuePairContext

_VP_META = {"monthDemoAmt": {"start": "monthDemoAmtStart", "end": "monthDemoAmtEnd"}}

_RENDER_CTX = {
    "def_prefix": "    async def ",
    "body_indent": "        ",
    "status_attr": "status",
    "json_call": "await r.json()",
    "with_keyword": "async with",
}

# ==================== build_value_pairs 类型判据识别 ====================


@allure.feature("数值范围对")
@allure.story("类型判据识别")
@allure.title("测试 build_value_pairs 各声明形态配对与类型闸门")
@pytest.mark.parametrize("api_params,expected", [
    # None 为数值参数的类型感知默认值 → 配对
    (
        {"monthDemoAmtStart": None, "monthDemoAmtEnd": None},
        {"monthDemoAmt": {"start": "monthDemoAmtStart", "end": "monthDemoAmtEnd"}},
    ),
    # int/float 声明同样配对
    (
        {"demoScoreStart": 0, "demoScoreEnd": 100.5},
        {"demoScore": {"start": "demoScoreStart", "end": "demoScoreEnd"}},
    ),
    # begin 后缀归入 start 侧
    (
        {"demoPeriodBegin": None, "demoPeriodEnd": None},
        {"demoPeriod": {"start": "demoPeriodBegin", "end": "demoPeriodEnd"}},
    ),
    # 单侧无伴生 → 不配对
    ({"demoStatusEnd": None}, {}),
    # 字符串声明（""）不参与（endpoint 类命名不会误伤）
    ({"demoEndpointStart": "", "demoEndpointEnd": ""}, {}),
    # 数组声明（[]）不参与
    ({"demoRangeStart": [], "demoRangeEnd": []}, {}),
    # bool 是 int 子类须排除
    ({"demoFlagStart": True, "demoFlagEnd": False}, {}),
    # 双侧类型不一致（一侧字符串）→ 不配对
    ({"demoMixStart": None, "demoMixEnd": ""}, {}),
    # 空参数字典
    ({}, {}),
])
def test_build_value_pairs_forms(api_params, expected):
    assert build_value_pairs(api_params) == expected


@allure.feature("数值范围对")
@allure.story("类型判据识别")
@allure.title("测试已被时间对配对的成员排除（时间对机制优先）")
def test_build_value_pairs_time_members_excluded():
    api_params = {
        "demoTimeStart": None,
        "demoTimeEnd": None,
        "monthDemoAmtStart": None,
        "monthDemoAmtEnd": None,
    }
    time_pairs = {
        "demoTime": {"start": "demoTimeStart", "end": "demoTimeEnd", "format": "%Y-%m-%d"},
    }
    assert build_value_pairs(api_params, time_pairs) == _VP_META


# ==================== ValuePairContext 消费 ====================


@allure.feature("数值范围对")
@allure.story("上下文构建")
@allure.title("测试 build 活跃过滤与查找表映射")
def test_value_pair_context_build():
    api_params = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    meta = dict(_VP_META)
    # 不存在于 api_params 的键被过滤
    meta["ghostAmt"] = {"start": "ghostAmtStart", "end": "ghostAmtEnd"}
    ctx = ValuePairContext.build(meta, api_params)
    assert ctx.active_pairs == _VP_META
    assert ctx.start_to_end == {"monthDemoAmtStart": "monthDemoAmtEnd"}
    assert ctx.start_to_base == {"monthDemoAmtStart": "monthDemoAmt"}
    assert ctx.end_names == {"monthDemoAmtEnd"}
    assert ctx.all_names == {"monthDemoAmtStart", "monthDemoAmtEnd"}
    assert ctx.has_value_pairs is True


@allure.feature("数值范围对")
@allure.story("上下文构建")
@allure.title("测试单侧缺失过滤与空上下文")
def test_value_pair_context_empty():
    # end 缺失 → 整对不活跃
    ctx = ValuePairContext.build(_VP_META, {"monthDemoAmtStart": None})
    assert ctx.has_value_pairs is False
    assert ctx.all_names == set()
    empty = ValuePairContext.build(None, {})
    assert empty.has_value_pairs is False
    assert empty.start_to_end == {}


# ==================== list_query_data None 基线渲染 ====================


@allure.feature("数值范围对")
@allure.story("基线渲染")
@allure.title("测试数值对成员基线置 None 且优先于枚举值分支")
def test_gen_list_query_data_none_baseline():
    api_params = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    vp_ctx = ValuePairContext.build(_VP_META, api_params)
    lines = gen_list_query_data_class_attr(
        api_params, {"monthDemoAmtStart": [1, 2]}, TimePairContext(), vp_ctx,
    )
    text = "\n".join(lines)
    assert '"monthDemoAmtStart": None,' in text
    assert '"monthDemoAmtEnd": None,' in text
    assert "[1, 2]" not in text


# ==================== test_0 聚合传参渲染 ====================


@allure.feature("数值范围对")
@allure.story("收集传参")
@allure.title("测试 gen_test_0 传入数值对时 collect 调用带 value_pairs 关键字")
def test_gen_test_0_value_pairs_render():
    lines = gen_test_0_collect_response_data(
        _RENDER_CTX, "演示列表", "demo_list", "params",
        {"monthDemoAmtStart": None, "monthDemoAmtEnd": None},
        value_pairs=_VP_META,
    )
    text = "\n".join(lines)
    assert (
        "collect_list_query_data(data, self.__class__.list_query_data, "
        "value_pairs={'monthDemoAmt': {'start': 'monthDemoAmtStart', 'end': 'monthDemoAmtEnd'}})"
    ) in text


@allure.feature("数值范围对")
@allure.story("收集传参")
@allure.title("测试单时间参数与数值对共存时 collect 调用形态")
def test_gen_test_0_extra_and_value_pairs_render():
    lines = gen_test_0_collect_response_data(
        _RENDER_CTX, "演示列表", "demo_list", "params", {"orderDate": ""},
        extra_time_params=["orderDate"], value_pairs=_VP_META,
    )
    text = "\n".join(lines)
    assert (
        "collect_list_query_data(data, self.__class__.list_query_data, ['orderDate'], value_pairs="
    ) in text


@allure.feature("数值范围对")
@allure.story("收集传参")
@allure.title("测试无数值对时 collect 调用形态不变")
def test_gen_test_0_without_value_pairs():
    lines = gen_test_0_collect_response_data(
        _RENDER_CTX, "演示列表", "demo_list", "params", {"keyword": ""},
    )
    assert "collect_list_query_data(data, self.__class__.list_query_data)" in "\n".join(lines)


# ==================== collect_list_query_data min/max 聚合 ====================


@allure.feature("数值范围对")
@allure.story("min/max 聚合")
@allure.title("测试聚合所有记录词干字段的 min/max 写入 start/end")
def test_collect_value_pairs_min_max():
    resp = {"data": {"list": [
        {"monthDemoAmt": 5, "keyword": "演示A"},
        {"monthDemoAmt": 20.5, "keyword": "演示B"},
        {"monthDemoAmt": 3, "keyword": "演示C"},
    ]}}
    lqd = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    collect_list_query_data(resp, lqd, value_pairs=_VP_META)
    assert lqd["monthDemoAmtStart"] == 3
    assert lqd["monthDemoAmtEnd"] == 20.5
    # 主收集通道不受影响
    assert lqd["keyword"] == "演示A"


@allure.feature("数值范围对")
@allure.story("min/max 聚合")
@allure.title("测试词干匹配不区分大小写且排除 bool/不可解析字符串值")
def test_collect_value_pairs_field_gate():
    resp = {"data": {"list": [
        {"monthdemoamt": 8},
        {"monthDemoAmt": True},
        {"monthDemoAmt": "abc"},
        {"monthDemoAmt": 2},
    ]}}
    lqd = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None}
    collect_list_query_data(resp, lqd, value_pairs=_VP_META)
    assert lqd["monthDemoAmtStart"] == 2
    assert lqd["monthDemoAmtEnd"] == 8


@allure.feature("数值范围对")
@allure.story("min/max 聚合")
@allure.title("测试数值型字符串按 float 归一后参与数值 min/max 聚合")
def test_collect_value_pairs_numeric_string():
    # 金额接口常见 '5200.00' 字符串形态：按 float 解析参与聚合；
    # 断言 start=1700.0 可反向证明未按字符串字典序比较
    # （字典序下 '12626.00' < '5200.00'，start 会误取 12626.0）
    resp = {"data": {"list": [
        {"monthDemoAmt": "5200.00"},
        {"monthDemoAmt": 1700},
        {"monthDemoAmt": "12626.00"},
    ]}}
    lqd = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None}
    collect_list_query_data(resp, lqd, value_pairs=_VP_META)
    assert lqd["monthDemoAmtStart"] == 1700.0
    assert lqd["monthDemoAmtEnd"] == 12626.0


@allure.feature("数值范围对")
@allure.story("min/max 聚合")
@allure.title("测试未命中词干保持 None 且成员不被主收集污染")
def test_collect_value_pairs_degradation():
    # 响应无词干字段，但存在与 start 参数同名的字段：
    # 数值对成员不参与主收集，基线保持 None（消费侧降级跳过验证）
    resp = {"data": {"list": [{"monthDemoAmtStart": 999, "keyword": "演示"}]}}
    lqd = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    collect_list_query_data(resp, lqd, value_pairs=_VP_META)
    assert lqd["monthDemoAmtStart"] is None
    assert lqd["monthDemoAmtEnd"] is None
    assert lqd["keyword"] == "演示"


@allure.feature("数值范围对")
@allure.story("min/max 聚合")
@allure.title("测试 field_map 显式映射优先于词干匹配响应字段")
def test_collect_value_pairs_field_map():
    # 参数名 monthDemoAmtStart 与响应字段 monthReturnAmt 不同名：无映射时
    # 词干 monthDemoAmt 匹配落空保持 None，有映射时按 monthReturnAmt 聚合
    resp = {"data": {"list": [
        {"monthReturnAmt": 5, "keyword": "演示A"},
        {"monthReturnAmt": 20.5, "keyword": "演示B"},
        {"monthReturnAmt": 3, "keyword": "演示C"},
    ]}}
    lqd = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    collect_list_query_data(
        resp, lqd, value_pairs=_VP_META,
        field_map={"monthDemoAmtStart": "monthReturnAmt"},
    )
    assert lqd["monthDemoAmtStart"] == 3
    assert lqd["monthDemoAmtEnd"] == 20.5
    assert lqd["keyword"] == "演示A"
    # 对照：不传映射时保持 None 基线（消费侧降级跳过验证）
    lqd2 = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    collect_list_query_data(resp, lqd2, value_pairs=_VP_META)
    assert lqd2["monthDemoAmtStart"] is None
    assert lqd2["monthDemoAmtEnd"] is None


@allure.feature("数值范围对")
@allure.story("min/max 聚合")
@allure.title("测试 field_map 映射字段在响应中不存在时直接抛 ValueError")
def test_collect_value_pairs_field_map_missing_raises():
    # field_map 属手工配置：映射字段未命中数值时显式报错提示改正；
    # 响应虽存在词干字段 monthDemoAmt，也不得静默回退词干匹配兜底
    resp = {"data": {"list": [{"monthDemoAmt": 5}]}}
    lqd = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None}
    with pytest.raises(ValueError, match="monthReturnAmt"):
        collect_list_query_data(
            resp, lqd, value_pairs=_VP_META,
            field_map={"monthDemoAmtStart": "monthReturnAmt"},
        )


# ==================== 区间组合用例生成 ====================


@allure.feature("数值范围对")
@allure.story("区间组合用例")
@allure.title("测试 start 生成区间组合方法且 end 跳过独立用例")
def test_gen_batch_value_pair_combined_method():
    api_params = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    vp_ctx = ValuePairContext.build(_VP_META, api_params)
    param_items = [
        {
            "param_name": "monthDemoAmtStart",
            "other_params": {"monthDemoAmtEnd": None, "keyword": ""},
            "is_array_param": False,
        },
        {
            "param_name": "monthDemoAmtEnd",
            "other_params": {"monthDemoAmtStart": None, "keyword": ""},
            "is_array_param": False,
        },
    ]
    lines = gen_batch_parametrized_test_methods(
        _RENDER_CTX, param_items, "演示列表", "demo_list", "params", {},
        {"monthDemoAmtStart": "演示月金额-起", "monthDemoAmtEnd": "演示月金额-止"},
        value_pair_ctx=vp_ctx,
    )
    text = "\n".join(lines)
    # end 参数不生成独立用例，仅一个组合方法
    assert text.count("async def test_") == 1
    assert "test_1_demo_list" in text
    # 标题剥离"起/止"方向标记
    assert "演示月金额 查询" in text
    assert "演示月金额-起" not in text
    # Start/End 同传且引用 list_query_data 动态基线
    assert '"monthDemoAmtStart": self.list_query_data["monthDemoAmtStart"],' in text
    assert '"monthDemoAmtEnd": self.list_query_data["monthDemoAmtEnd"],' in text
    # 区间守卫用 is not None（0 是合法基线，不能用 truthy 守卫）
    assert (
        'if self.list_query_data["monthDemoAmtStart"] is not None '
        'and self.list_query_data["monthDemoAmtEnd"] is not None:'
    ) in text
    # 断言按词干匹配响应字段并验证落在区间内
    assert 'if k.lower() == "monthdemoamt":' in text
    assert (
        'assert v is None or float(self.list_query_data["monthDemoAmtStart"])'
        ' <= float(v) <= float(self.list_query_data["monthDemoAmtEnd"])'
    ) in text


@allure.feature("数值范围对")
@allure.story("区间组合用例")
@allure.title("测试 field_map 映射值注入区间断言字段匹配")
def test_gen_batch_value_pair_combined_method_field_map():
    api_params = {"monthDemoAmtStart": None, "monthDemoAmtEnd": None, "keyword": ""}
    vp_ctx = ValuePairContext.build(_VP_META, api_params)
    param_items = [
        {
            "param_name": "monthDemoAmtStart",
            "other_params": {"monthDemoAmtEnd": None, "keyword": ""},
            "is_array_param": False,
        },
        {
            "param_name": "monthDemoAmtEnd",
            "other_params": {"monthDemoAmtStart": None, "keyword": ""},
            "is_array_param": False,
        },
    ]
    lines = gen_batch_parametrized_test_methods(
        _RENDER_CTX, param_items, "演示列表", "demo_list", "params", {},
        {"monthDemoAmtStart": "演示月金额-起", "monthDemoAmtEnd": "演示月金额-止"},
        value_pair_ctx=vp_ctx,
        field_map={"monthDemoAmtStart": "monthReturnAmt"},
    )
    text = "\n".join(lines)
    # 断言按映射字段匹配，而非词干 monthdemoamt
    assert 'if k.lower() == "monthreturnamt":' in text
    assert 'if k.lower() == "monthdemoamt":' not in text


# ==================== 元数据落盘与读取 ====================


@allure.feature("数值范围对")
@allure.story("元数据链路")
@allure.title("测试 value_pairs 写入 api.json 并被 parse_api_file 读取")
def test_value_pairs_metadata_roundtrip(tmp_path):
    py_file = tmp_path / "demo_amt_list.py"
    write_api_metadata(
        str(py_file),
        function_name="demo_amt_list",
        url="/demo/amt/list",
        params={"monthDemoAmtStart": None, "monthDemoAmtEnd": None},
        value_pairs=_VP_META,
    )
    clear_api_file_cache()
    info = parse_api_file(str(py_file))
    assert info.value_pairs == _VP_META


@allure.feature("数值范围对")
@allure.story("元数据链路")
@allure.title("测试空 value_pairs 不写入元数据字段")
def test_value_pairs_empty_not_written(tmp_path):
    py_file = tmp_path / "demo_empty.py"
    write_api_metadata(
        str(py_file), function_name="demo_empty", url="/demo/empty", value_pairs={},
    )
    clear_api_file_cache()
    info = parse_api_file(str(py_file))
    assert info.value_pairs == {}
    assert VALUE_PAIRS_FIELD not in (py_file.with_suffix(".api.json")).read_text(encoding="utf-8")


# ==================== 生成器端到端接线 ====================


@pytest.fixture
def pagination_config(monkeypatch):
    """临时把 PAGINATION_PARAMS 设为 pageNum/pageSize（monkeypatch 自动恢复）。"""
    APIConfig.get_config("PAGINATION_PARAMS")
    config = APIConfig._config
    assert config is not None
    monkeypatch.setitem(config, "PAGINATION_PARAMS", {"pageNum": 1, "pageSize": 10})


@allure.feature("数值范围对")
@allure.story("生成器接线")
@allure.title("测试数值对接口生成 None 基线/聚合传参/区间组合用例")
def test_generate_parametrized_content_value_pairs(tmp_path, pagination_config):
    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "demo_amt_pageQuery.py"
    api_file.write_text(
        "def demo_amt_pageQuery(params=params, headers=headers):\n    pass\n",
        encoding="utf-8",
    )
    write_api_metadata(
        str(api_file),
        function_name="demo_amt_pageQuery",
        url="/demo/amt/pageQuery",
        description="演示金额列表",
        params={
            "monthDemoAmtStart": None, "monthDemoAmtEnd": None,
            "keyword": "", "pageNum": 1, "pageSize": 10,
        },
        param_remarks={
            "monthDemoAmtStart": "演示月金额-起",
            "monthDemoAmtEnd": "演示月金额-止",
            "keyword": "演示关键字",
        },
        value_pairs=_VP_META,
    )
    clear_api_file_cache()
    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path / "output"))
    content = generator.generate_parametrized_test_content(str(api_file), "test_task")
    assert content is not None
    # list_query_data 基线置 None（由 test_0 收集 min/max 覆盖）
    assert '"monthDemoAmtStart": None,' in content
    assert '"monthDemoAmtEnd": None,' in content
    # 数值对成员不参数化，由 start 生成区间组合用例
    assert '@pytest.mark.parametrize("monthDemoAmtStart"' not in content
    assert '"monthDemoAmtStart": self.list_query_data["monthDemoAmtStart"],' in content
    assert '"monthDemoAmtEnd": self.list_query_data["monthDemoAmtEnd"],' in content
    # test_0 聚合传参
    assert (
        "collect_list_query_data(data, self.__class__.list_query_data, "
        "value_pairs={'monthDemoAmt': {'start': 'monthDemoAmtStart', 'end': 'monthDemoAmtEnd'}})"
    ) in content
    # 区间断言与降级守卫
    assert 'if k.lower() == "monthdemoamt":' in content
    assert "float(v) <= float(" in content
    # 数值对不引入 datetime 动态值
    assert "from datetime import datetime" not in content