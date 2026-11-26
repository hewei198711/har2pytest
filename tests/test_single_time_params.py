"""测试单时间参数动态值生成支持（一个参数自身承载时间，无 start/end 伴生）。

覆盖五段链路：utils 双条件识别（候选关键字 + 备注显式格式 token）→
api_metadata 落盘 single_time_params → parse_api_file 读取 →
TimePairContext.single_params 消费 → list_query_data datetime 动态表达式
（range=True 注入"当年起点,今天"逗号区间，False 注入当前单值）与
test_0 收集免疫（extra_time_params）。备注均为演示占位，不含真实业务信息。
"""

import allure
import pytest

from har2pytest.api_metadata import SINGLE_TIME_PARAMS_FIELD, write_api_metadata
from har2pytest.config import APIConfig
from har2pytest.parametrized_codegen import (
    gen_list_query_data_class_attr,
    gen_test_0_collect_response_data,
)
from har2pytest.pytest_utils import collect_list_query_data
from har2pytest.testcase_generator import TestCaseGenerator
from har2pytest.time_pair import TimePairContext
from har2pytest.utils import (
    _extract_date_format_from_remark,
    build_single_time_params,
    clear_api_file_cache,
    extract_explicit_date_format,
    parse_api_file,
)

# ==================== extract_explicit_date_format 显式格式提取 ====================


@allure.feature("单时间参数")
@allure.story("显式日期格式提取")
@allure.title("测试 extract_explicit_date_format 各形态提取与无 token 返回 None")
@pytest.mark.parametrize("remark,expected", [
    # 括号优先
    ("演示订单日期(yyyy-MM-dd)", "%Y-%m-%d"),
    ("演示时间（yyyy-MM-dd HH:mm:ss）", "%Y-%m-%d %H:%M:%S"),
    ("演示日期(yyyy/MM/dd)", "%Y/%m/%d"),
    # 裸 token 回落（年份 token 必须存在，大小写变体归一）
    ("演示业绩月份yyyyMM 202104", "%Y%m"),
    ("演示业绩月份YYYYMM", "%Y%m"),
    ("演示日期yyyy-mm-dd", "%Y-%m-%d"),
    # 括号无 token 时回落裸搜索
    ("演示日期(含)yyyy-MM-dd", "%Y-%m-%d"),
    # 无日期 token → None（不回落默认格式，双条件识别据此排除）
    ("无格式备注", None),
    ("演示日期(含)", None),
    ("演示月份 202104", None),
    ("演示限制开关:0-否,1-是,2-未知", None),
    ("", None),
])
def test_extract_explicit_date_format(remark, expected):
    assert extract_explicit_date_format(remark) == expected


@allure.feature("单时间参数")
@allure.story("显式日期格式提取")
@allure.title("测试 _extract_date_format_from_remark 包装后默认纯日期格式")
@pytest.mark.parametrize("remark,expected", [
    ("演示订单日期(yyyy-MM-dd)", "%Y-%m-%d"),
    ("无格式备注", "%Y-%m-%d"),
    ("演示日期(含)", "%Y-%m-%d"),
    ("演示业绩月份yyyyMM", "%Y%m"),
])
def test_extract_date_format_wrapper_regression(remark, expected):
    assert _extract_date_format_from_remark(remark) == expected


# ==================== build_single_time_params 双条件识别 ====================


@allure.feature("单时间参数")
@allure.story("双条件识别")
@allure.title("测试候选关键字+显式格式双条件命中与 range 标记")
def test_build_single_time_params_double_condition():
    remarks = {
        "orderDate": "演示订单日期(yyyy-MM-dd) 时间段用逗号分隔",
        "achievementMonth": "演示业绩月份yyyyMM 时间段用逗号分隔",
        "contrastDate": "演示对比日期(yyyy-MM-dd)",
    }
    result = build_single_time_params(remarks)
    assert result == {
        "orderDate": {"format": "%Y-%m-%d", "range": True},
        "achievementMonth": {"format": "%Y%m", "range": True},
        "contrastDate": {"format": "%Y-%m-%d", "range": False},
    }


@allure.feature("单时间参数")
@allure.story("双条件识别")
@allure.title("测试无格式 token/非候选关键字/已配对成员均排除")
def test_build_single_time_params_exclusions():
    remarks = {
        # 关键字命中但备注无显式格式 token（开关语义假阳性形态）→ 排除
        "demoLimitOrderDate": "演示限制开关:0-否,1-是,2-未知",
        # 有格式 token 但非候选关键字 → 排除
        "demoDate": "演示日期(yyyy-MM-dd)",
        # 候选关键字命中且已配对 → 排除（配对机制优先）
        "startOrderDate": "演示开始日期(yyyy-MM-dd)",
        "endOrderDate": "演示结束日期(yyyy-MM-dd)",
    }
    time_pairs = {
        "OrderDate": {
            "start": "startOrderDate",
            "end": "endOrderDate",
            "format": "%Y-%m-%d",
        },
    }
    assert build_single_time_params(remarks, time_pairs) == {}
    # time_pairs 为 None 时已配对排除不生效，但其余条件仍过滤
    result = build_single_time_params(remarks, None)
    assert set(result) == {"startOrderDate", "endOrderDate"}


@allure.feature("单时间参数")
@allure.story("双条件识别")
@allure.title("测试空备注字典返回空字典")
def test_build_single_time_params_empty():
    assert build_single_time_params({}) == {}
    assert build_single_time_params({}, None) == {}


# ==================== TimePairContext 单参数扩展 ====================


@allure.feature("单时间参数")
@allure.story("时间参数上下文")
@allure.title("测试 build 单参数活跃过滤/all_names/has_dynamic_time")
def test_time_pair_context_single_params():
    api_params = {"orderDate": "", "contrastDate": "", "keyword": ""}
    single_meta = {
        "orderDate": {"format": "%Y-%m-%d", "range": True},
        "contrastDate": {"format": "%Y-%m-%d", "range": False},
        # 不存在于 api_params 的键被过滤
        "ghostDate": {"format": "%Y-%m-%d", "range": True},
    }
    ctx = TimePairContext.build(None, api_params, single_time_params=single_meta)
    assert ctx.single_params == {
        "orderDate": ("%Y-%m-%d", True),
        "contrastDate": ("%Y-%m-%d", False),
    }
    assert ctx.all_names == {"orderDate", "contrastDate"}
    assert ctx.has_dynamic_time is True
    # 单参数不构成时间对，has_time_pairs 语义不变
    assert ctx.has_time_pairs is False
    assert ctx.param_role == {}
    assert ctx.start_to_end == {}


@allure.feature("单时间参数")
@allure.story("时间参数上下文")
@allure.title("测试时间对与单参数共存时 all_names 并入")
def test_time_pair_context_pairs_and_singles():
    api_params = {"startTime": "", "endTime": "", "orderDate": ""}
    pairs = {"Time": {"start": "startTime", "end": "endTime", "format": "%Y-%m-%d"}}
    singles = {"orderDate": {"format": "%Y-%m-%d", "range": True}}
    ctx = TimePairContext.build(pairs, api_params, single_time_params=singles)
    assert ctx.has_time_pairs is True
    assert ctx.has_dynamic_time is True
    assert ctx.all_names == {"startTime", "endTime", "orderDate"}
    assert ctx.single_params == {"orderDate": ("%Y-%m-%d", True)}


@allure.feature("单时间参数")
@allure.story("时间参数上下文")
@allure.title("测试 range 缺省为 False 与空上下文")
def test_time_pair_context_range_default_and_empty():
    ctx = TimePairContext.build(None, {"orderDate": ""}, {"orderDate": {"format": "%Y%m"}})
    assert ctx.single_params == {"orderDate": ("%Y%m", False)}
    empty = TimePairContext.build(None, {})
    assert empty.has_dynamic_time is False
    assert empty.has_time_pairs is False
    assert empty.single_params == {}


# ==================== list_query_data 动态表达式渲染 ====================


@allure.feature("单时间参数")
@allure.story("动态值注入")
@allure.title("测试 range=True 渲染当年起点,今天逗号区间表达式")
def test_gen_list_query_data_range_expression():
    tp_ctx = TimePairContext.build(
        None, {"orderDate": ""}, {"orderDate": {"format": "%Y-%m-%d", "range": True}},
    )
    lines = gen_list_query_data_class_attr({"orderDate": ""}, {}, tp_ctx)
    text = "\n".join(lines)
    assert (
        '"orderDate": datetime(datetime.now().year, 1, 1).strftime("%Y-%m-%d")'
        ' + "," + datetime.now().strftime("%Y-%m-%d"),'
    ) in text


@allure.feature("单时间参数")
@allure.story("动态值注入")
@allure.title("测试 range=False 渲染当前单值表达式")
def test_gen_list_query_data_single_value_expression():
    tp_ctx = TimePairContext.build(
        None, {"contrastDate": ""}, {"contrastDate": {"format": "%Y-%m-%d", "range": False}},
    )
    lines = gen_list_query_data_class_attr({"contrastDate": ""}, {}, tp_ctx)
    assert '"contrastDate": datetime.now().strftime("%Y-%m-%d"),' in "\n".join(lines)


@allure.feature("单时间参数")
@allure.story("动态值注入")
@allure.title("测试单参数优先于枚举值分支")
def test_gen_list_query_data_single_over_enum():
    tp_ctx = TimePairContext.build(
        None, {"orderDate": ""}, {"orderDate": {"format": "%Y%m", "range": False}},
    )
    lines = gen_list_query_data_class_attr({"orderDate": ""}, {"orderDate": [1, 2]}, tp_ctx)
    text = "\n".join(lines)
    assert 'datetime.now().strftime("%Y%m")' in text
    assert "[1, 2]" not in text


# ==================== test_0 收集免疫传参渲染 ====================

_RENDER_CTX = {
    "def_prefix": "    async def ",
    "body_indent": "        ",
    "status_attr": "status",
    "json_call": "await r.json()",
    "with_keyword": "async with",
}


@allure.feature("单时间参数")
@allure.story("收集免疫")
@allure.title("测试 gen_test_0 传入单参数名时 collect 调用带第三参")
def test_gen_test_0_extra_time_params_render():
    lines = gen_test_0_collect_response_data(
        _RENDER_CTX, "演示列表", "demo_list", "params", {"orderDate": ""},
        extra_time_params=["orderDate"],
    )
    text = "\n".join(lines)
    assert "collect_list_query_data(data, self.__class__.list_query_data, ['orderDate'])" in text
    # test_0 静态默认值消费点不注入 datetime 表达式
    assert "datetime" not in text


@allure.feature("单时间参数")
@allure.story("收集免疫")
@allure.title("测试无单参数时 collect 调用形态不变")
def test_gen_test_0_without_extra_time_params():
    lines = gen_test_0_collect_response_data(
        _RENDER_CTX, "演示列表", "demo_list", "params", {"keyword": ""},
    )
    assert "collect_list_query_data(data, self.__class__.list_query_data)" in "\n".join(lines)


@allure.feature("单时间参数")
@allure.story("收集免疫")
@allure.title("测试 collect_list_query_data 单参数豁免响应收集")
def test_collect_extra_time_params_immunity():
    resp = {"data": {"list": [{"orderDate": "2025-05-05", "keyword": "演示"}]}}
    baseline = "2025-01-01,2025-06-01"
    # 传入 extra_time_params：单参数不被响应同名字段污染
    lqd = {"orderDate": baseline, "keyword": ""}
    collect_list_query_data(resp, lqd, extra_time_params=["orderDate"])
    assert lqd["orderDate"] == baseline
    assert lqd["keyword"] == "演示"
    # 不传时 orderDate 不命中 TIME_PARAMS 闸门，会被响应值覆盖（免疫须显式传参）
    lqd2 = {"orderDate": baseline, "keyword": ""}
    collect_list_query_data(resp, lqd2)
    assert lqd2["orderDate"] == "2025-05-05"


# ==================== 元数据落盘与读取 ====================


@allure.feature("单时间参数")
@allure.story("元数据链路")
@allure.title("测试 single_time_params 写入 api.json 并被 parse_api_file 读取")
def test_single_time_params_metadata_roundtrip(tmp_path):
    py_file = tmp_path / "demo_trend_list.py"
    singles = {"orderDate": {"format": "%Y-%m-%d", "range": True}}
    write_api_metadata(
        str(py_file),
        function_name="demo_trend_list",
        url="/demo/trend/list",
        params={"orderDate": ""},
        single_time_params=singles,
    )
    clear_api_file_cache()
    info = parse_api_file(str(py_file))
    assert info.single_time_params == singles


@allure.feature("单时间参数")
@allure.story("元数据链路")
@allure.title("测试空 single_time_params 不写入元数据字段")
def test_single_time_params_empty_not_written(tmp_path):
    py_file = tmp_path / "demo_empty.py"
    write_api_metadata(
        str(py_file), function_name="demo_empty", url="/demo/empty", single_time_params={},
    )
    clear_api_file_cache()
    info = parse_api_file(str(py_file))
    assert info.single_time_params == {}
    assert SINGLE_TIME_PARAMS_FIELD not in (py_file.with_suffix(".api.json")).read_text(encoding="utf-8")


# ==================== 生成器端到端接线 ====================


@pytest.fixture
def pagination_config(monkeypatch):
    """临时把 PAGINATION_PARAMS 设为 pageNum/pageSize（monkeypatch 自动恢复）。"""
    APIConfig.get_config("PAGINATION_PARAMS")
    config = APIConfig._config
    assert config is not None
    monkeypatch.setitem(config, "PAGINATION_PARAMS", {"pageNum": 1, "pageSize": 10})


@allure.feature("单时间参数")
@allure.story("生成器接线")
@allure.title("测试单时间参数接口生成动态值/专门用例/收集免疫/datetime导入")
def test_generate_parametrized_content_single_time(tmp_path, pagination_config):
    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "demo_trend_getCount.py"
    api_file.write_text(
        "def demo_trend_getCount(params=params, headers=headers):\n    pass\n",
        encoding="utf-8",
    )
    write_api_metadata(
        str(api_file),
        function_name="demo_trend_getCount",
        url="/demo/trend/getCount",
        description="演示趋势统计",
        params={"orderDate": "", "achievementMonth": "", "dimension": None, "pageNum": 1, "pageSize": 10},
        param_remarks={
            "orderDate": "演示订单日期(yyyy-MM-dd) 时间段用逗号分隔",
            "achievementMonth": "演示业绩月份yyyyMM 时间段用逗号分隔",
            "dimension": "演示维度",
        },
        single_time_params={
            "orderDate": {"format": "%Y-%m-%d", "range": True},
            "achievementMonth": {"format": "%Y%m", "range": True},
        },
    )
    clear_api_file_cache()
    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path / "output"))
    content = generator.generate_parametrized_test_content(str(api_file), "test_task")
    assert content is not None
    # datetime 导入由 has_dynamic_time 触发（无时间对也导入）
    assert "from datetime import datetime" in content
    # list_query_data 注入逗号区间动态表达式
    assert (
        '"orderDate": datetime(datetime.now().year, 1, 1).strftime("%Y-%m-%d")'
        ' + "," + datetime.now().strftime("%Y-%m-%d"),'
    ) in content
    assert '"achievementMonth": datetime(datetime.now().year, 1, 1).strftime("%Y%m")' in content
    # 单参数永不参数化，走运行时取值分支生成专门查询用例
    assert '@pytest.mark.parametrize("orderDate"' not in content
    assert 'self.list_query_data["orderDate"]' in content
    assert 'self.list_query_data["achievementMonth"]' in content
    # test_0 与其余方法体的单时间参数置 ""（动态值仅由 list_query_data 提供）
    assert '"orderDate": ""' in content
    # 收集免疫：collect 调用带单参数名第三参
    assert (
        "collect_list_query_data(data, self.__class__.list_query_data, "
        "['achievementMonth', 'orderDate'])"
    ) in content