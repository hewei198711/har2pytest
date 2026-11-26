"""测试 epoch 时间对支持（integer 时间戳语义的 Start/End 配对迁移为时间对）。

覆盖链路：utils.build_epoch_time_pairs 时间语义迁移（备注关键字 + 秒时间戳
格式判定）→ TimePairContext 消费与 epoch_names → list_query_data 毫秒/秒
时间戳动态表达式 → 时间对组合用例与收集免疫（extra_time_params 并入
epoch 成员）。备注均为演示占位，不含真实业务信息。
"""

import allure
import pytest

from har2pytest.api_metadata import write_api_metadata
from har2pytest.config import APIConfig
from har2pytest.parametrized_codegen import gen_list_query_data_class_attr
from har2pytest.testcase_generator import TestCaseGenerator
from har2pytest.time_pair import TimePairContext
from har2pytest.utils import (
    EPOCH_MS_FORMAT,
    EPOCH_S_FORMAT,
    build_epoch_time_pairs,
    clear_api_file_cache,
)

# ==================== build_epoch_time_pairs 时间语义迁移 ====================


@allure.feature("epoch 时间对")
@allure.story("时间语义迁移")
@allure.title("测试时间备注的数值对迁入 epoch 时间对且默认为 epoch_ms")
def test_build_epoch_time_pairs_migrates_time_remarks():
    value_pairs = {
        "create": {"start": "createBegin", "end": "createEnd"},
        "amt": {"start": "amtStart", "end": "amtEnd"},
    }
    remarks = {
        "createBegin": "演示下单开始时间",
        "createEnd": "演示下单结束时间",
        "amtStart": "演示金额区间起点",
        "amtEnd": "演示金额区间终点",
    }
    result = build_epoch_time_pairs(value_pairs, remarks)
    assert result == {
        "create": {"start": "createBegin", "end": "createEnd", "format": "epoch_ms"},
    }


@allure.feature("epoch 时间对")
@allure.story("时间语义迁移")
@allure.title("测试备注含秒时间戳时 format 为 epoch_s")
def test_build_epoch_time_pairs_epoch_s():
    value_pairs = {"downloadAt": {"start": "downloadAtStart", "end": "downloadAtEnd"}}
    remarks = {
        "downloadAtStart": "演示下载开始时间(每秒时间戳)",
        "downloadAtEnd": "演示下载结束时间",
    }
    result = build_epoch_time_pairs(value_pairs, remarks)
    assert result == {
        "downloadAt": {"start": "downloadAtStart", "end": "downloadAtEnd", "format": "epoch_s"},
    }


@allure.feature("epoch 时间对")
@allure.story("时间语义迁移")
@allure.title("测试英文整词 date/time 命中迁移、单词内部子串不命中")
def test_build_epoch_time_pairs_english_whole_word():
    value_pairs = {
        "expiry": {"start": "expiryStart", "end": "expiryEnd"},
        "candidate": {"start": "candidateIdStart", "end": "candidateIdEnd"},
    }
    remarks = {
        "expiryStart": "演示到期 start date",
        # "candidate" 内部的 date 子串不命中整词匹配
        "candidateIdStart": "演示候选编号范围起点",
    }
    result = build_epoch_time_pairs(value_pairs, remarks)
    assert set(result) == {"expiry"}


@allure.feature("epoch 时间对")
@allure.story("时间语义迁移")
@allure.title("测试非时间备注不迁移且空输入返回空字典")
def test_build_epoch_time_pairs_exclusions():
    value_pairs = {"amt": {"start": "amtStart", "end": "amtEnd"}}
    remarks = {"amtStart": "演示金额区间起点", "amtEnd": "演示金额区间终点"}
    assert build_epoch_time_pairs(value_pairs, remarks) == {}
    assert build_epoch_time_pairs({}, {}) == {}


# ==================== TimePairContext epoch 消费 ====================


@allure.feature("epoch 时间对")
@allure.story("时间参数上下文")
@allure.title("测试 build 透传 epoch fmt、epoch_names 提取、has_dynamic_time 为真")
def test_time_pair_context_epoch_pair():
    api_params = {"createBegin": None, "createEnd": None, "keyword": ""}
    pairs = {"create": {"start": "createBegin", "end": "createEnd", "format": "epoch_ms"}}
    ctx = TimePairContext.build(pairs, api_params)
    assert ctx.param_role == {
        "createBegin": ("start", "epoch_ms"),
        "createEnd": ("end", "epoch_ms"),
    }
    assert ctx.epoch_names == {"createBegin", "createEnd"}
    assert ctx.has_dynamic_time is True
    assert ctx.has_time_pairs is True


@allure.feature("epoch 时间对")
@allure.story("时间参数上下文")
@allure.title("测试非 epoch 时间对 epoch_names 为空集")
def test_time_pair_context_string_pair_no_epoch_names():
    api_params = {"startTime": "", "endTime": ""}
    pairs = {"Time": {"start": "startTime", "end": "endTime", "format": "%Y-%m-%d"}}
    ctx = TimePairContext.build(pairs, api_params)
    assert ctx.epoch_names == set()
    assert ctx.has_dynamic_time is True


# ==================== list_query_data epoch 表达式渲染 ====================


@allure.feature("epoch 时间对")
@allure.story("动态值注入")
@allure.title("测试 epoch_ms 渲染毫秒时间戳表达式（start 当年起点 / end 当前）")
def test_gen_list_query_data_epoch_ms_expression():
    tp_ctx = TimePairContext.build(
        {"create": {"start": "createBegin", "end": "createEnd", "format": "epoch_ms"}},
        {"createBegin": None, "createEnd": None},
    )
    text = "\n".join(
        gen_list_query_data_class_attr({"createBegin": None, "createEnd": None}, {}, tp_ctx)
    )
    assert (
        '"createBegin": int(datetime(datetime.now().year, 1, 1).timestamp() * 1000),' in text
    )
    assert '"createEnd": int(datetime.now().timestamp() * 1000),' in text
    # 绝不渲染日期字符串（数值参数会被服务端拒绝）
    assert "strftime" not in text


@allure.feature("epoch 时间对")
@allure.story("动态值注入")
@allure.title("测试 epoch_s 渲染秒时间戳表达式（不乘 1000）")
def test_gen_list_query_data_epoch_s_expression():
    tp_ctx = TimePairContext.build(
        {"downloadAt": {"start": "downloadAtStart", "end": "downloadAtEnd", "format": "epoch_s"}},
        {"downloadAtStart": None, "downloadAtEnd": None},
    )
    text = "\n".join(
        gen_list_query_data_class_attr(
            {"downloadAtStart": None, "downloadAtEnd": None}, {}, tp_ctx
        )
    )
    assert '"downloadAtStart": int(datetime(datetime.now().year, 1, 1).timestamp()),' in text
    assert '"downloadAtEnd": int(datetime.now().timestamp()),' in text
    assert "* 1000" not in text


@allure.feature("epoch 时间对")
@allure.story("动态值注入")
@allure.title("测试 epoch 对优先于枚举值与数值对分支")
def test_gen_list_query_data_epoch_over_enum_and_value_pair():
    tp_ctx = TimePairContext.build(
        {"create": {"start": "createBegin", "end": "createEnd", "format": "epoch_ms"}},
        {"createBegin": None, "createEnd": None},
    )
    lines = gen_list_query_data_class_attr(
        {"createBegin": None, "createEnd": None}, {"createBegin": [1, 2]}, tp_ctx,
    )
    text = "\n".join(lines)
    assert "int(datetime(datetime.now().year, 1, 1).timestamp() * 1000)" in text
    assert "[1, 2]" not in text


# ==================== 生成器端到端接线 ====================


@pytest.fixture
def pagination_config(monkeypatch):
    """临时把 PAGINATION_PARAMS 设为 pageNum/pageSize（monkeypatch 自动恢复）。"""
    APIConfig.get_config("PAGINATION_PARAMS")
    config = APIConfig._config
    assert config is not None
    monkeypatch.setitem(config, "PAGINATION_PARAMS", {"pageNum": 1, "pageSize": 10})


@allure.feature("epoch 时间对")
@allure.story("生成器接线")
@allure.title("测试 epoch 时间对接口生成毫秒表达式/组合用例/收集免疫/datetime导入")
def test_generate_parametrized_content_epoch_pair(tmp_path, pagination_config):
    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "demo_group_order_page.py"
    api_file.write_text(
        "def demo_group_order_page(params=params, headers=headers):\n    pass\n",
        encoding="utf-8",
    )
    write_api_metadata(
        str(api_file),
        function_name="demo_group_order_page",
        url="/demo/group/order/page",
        description="演示分页查询",
        params={
            "createBegin": None,
            "createEnd": None,
            "orderNo": "",
            "pageNum": 1,
            "pageSize": 10,
        },
        param_remarks={
            "createBegin": "演示下单开始时间",
            "createEnd": "演示下单结束时间",
            "orderNo": "演示订单编号",
        },
        time_pairs={
            "create": {"start": "createBegin", "end": "createEnd", "format": "epoch_ms"},
        },
    )
    clear_api_file_cache()
    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path / "output"))
    content = generator.generate_parametrized_test_content(str(api_file), "test_task")
    assert content is not None
    # datetime 导入由 has_dynamic_time 触发
    assert "from datetime import datetime" in content
    # list_query_data 注入毫秒时间戳动态表达式
    assert (
        '"createBegin": int(datetime(datetime.now().year, 1, 1).timestamp() * 1000),'
        in content
    )
    assert '"createEnd": int(datetime.now().timestamp() * 1000),' in content
    # 时间对组合用例引用动态值（start/end 同传）
    assert 'self.list_query_data["createBegin"]' in content
    assert 'self.list_query_data["createEnd"]' in content
    # 收集免疫：collect 调用带 epoch 成员名第三参
    assert (
        "collect_list_query_data(data, self.__class__.list_query_data, "
        "['createBegin', 'createEnd'])"
    ) in content
    # 方法体基准中时间参数保持 None（数值声明），不注入表达式
    assert '"createBegin": None' in content
