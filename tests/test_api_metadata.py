"""
测试 api_metadata API 元数据与 parse_api_file 的结构化读取。

背景：生成器产出 .py 模块的同时写入 <module>.api.json API 元数据，
url/描述/参数备注与 params/data/files/headers 的**当前值**都取自元数据
（生成时快照）。parse_api_file 只消费 .api.json：没有元数据（或元数据
损坏）时抛出“缺少 API 元数据”ValueError，元数据缺必需字段 url 时抛出
ValueError；元数据缺某个当前值字段时该字段按缺省处理——**不再回退解析
.py 源码/docstring/模块级赋值**。
"""

import json

import allure
import pytest

from har2pytest.api_metadata import (
    CONSTANT_PARAMS_FIELD,
    metadata_path,
    read_api_metadata,
    write_api_metadata,
)
from har2pytest.utils import clear_api_file_cache, parse_api_file

# 优先级测试共享的 .py 内容：手工修改了默认值（999），与生成期快照（1）不一致
_STALE_PY_CONTENT = '''params = {
    "pageNum": "999",  # 页数
}

def user_list(params=params, headers=headers):
    """
    文档中的旧描述
    /doc/old
    """
    url = "/user/list"
    return client.get(url=url, params=params)
'''


@allure.feature("API 元数据")
@allure.story("API 元数据读写")
@allure.title("测试元数据文件路径与写入读取")
def test_metadata_path_and_roundtrip(tmp_path):
    py_file = tmp_path / "user_list.py"

    assert metadata_path(str(py_file)) == str(tmp_path / "user_list.api.json")

    meta_file = write_api_metadata(
        str(py_file),
        function_name="user_list",
        url="/user/list",
        description="用户列表",
        method="GET",
        service_package="center_application",
        param_remarks={"keyword": "关键词", "payDTO.accountName": "账户名"},
        params={"keyword": "TS001", "pageNum": 1},
        data=None,
        files=None,
        headers={"channel": "pc"},
    )
    assert meta_file is not None
    assert meta_file.endswith(".api.json")

    data = read_api_metadata(str(py_file))
    assert data is not None
    assert data["url"] == "/user/list"
    assert data["description"] == "用户列表"
    assert data["param_remarks"]["keyword"] == "关键词"
    assert data["param_remarks"]["payDTO.accountName"] == "账户名"
    # 当前值字段随生成固化；未提供（None）的字段不写入
    assert data["params"] == {"keyword": "TS001", "pageNum": 1}
    assert data["headers"] == {"channel": "pc"}
    assert "data" not in data
    assert "files" not in data


@allure.feature("API 元数据")
@allure.story("API 元数据读写")
@allure.title("测试 source 参数写入与空 param_remarks 不写入")
def test_write_source_and_empty_param_remarks(tmp_path):
    py_file = tmp_path / "demo.py"
    write_api_metadata(
        str(py_file),
        function_name="demo",
        url="/demo",
        method="GET",
        source="har",
        param_remarks={},
    )
    data = read_api_metadata(str(py_file))
    assert data is not None
    assert data["source"] == "har"
    assert "param_remarks" not in data


@allure.feature("API 元数据")
@allure.story("API 元数据读写")
@allure.title("测试写入失败时 write_api_metadata 返回 None")
def test_write_returns_none_on_os_error(tmp_path, monkeypatch):
    py_file = tmp_path / "demo.py"
    call_count = 0
    original_dump = json.dump

    def fail_once(obj, fp, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise OSError("disk full")
        return original_dump(obj, fp, **kwargs)

    monkeypatch.setattr("json.dump", fail_once)
    assert write_api_metadata(str(py_file), url="/demo", method="GET") is None


@allure.feature("API 元数据")
@allure.story("API 元数据读取")
@allure.title("测试缺失/损坏元数据返回 None")
def test_metadata_read_missing_and_corrupt(tmp_path):
    py_file = tmp_path / "api_demo.py"
    assert read_api_metadata(str(py_file)) is None

    meta_file = tmp_path / "api_demo.api.json"
    meta_file.write_text("{broken json", encoding="utf-8")
    assert read_api_metadata(str(py_file)) is None


@allure.feature("API 元数据")
@allure.story("API 元数据读取")
@allure.title("测试元数据 JSON 为非 dict 时返回 None")
def test_read_returns_none_for_non_dict_json(tmp_path):
    py_file = tmp_path / "demo.py"
    meta_file = tmp_path / "demo.api.json"
    meta_file.write_text("[1, 2, 3]", encoding="utf-8")
    assert read_api_metadata(str(py_file)) is None


@allure.feature("API 元数据")
@allure.story("结构化读取优先级")
@allure.title("测试元数据当前值字段优先于 .py 模块级赋值")
def test_parse_prefers_sidecar_current_values(tmp_path):
    clear_api_file_cache()
    py_file = tmp_path / "user_list.py"
    py_file.write_text(_STALE_PY_CONTENT, encoding="utf-8")
    # API 元数据含生成期当前值快照
    write_api_metadata(
        str(py_file),
        function_name="user_list",
        url="/user/list",
        description="用户列表(规范描述)",
        method="GET",
        param_remarks={"pageNum": "页数(规范)"},
        params={"pageNum": "1"},
        headers={"channel": "pc"},
    )

    result = parse_api_file(str(py_file))

    # 描述/URL/备注来自 API 元数据，而不是 docstring 反解
    assert result.description == "用户列表(规范描述)"
    assert result.url == "/user/list"
    assert result.param_remarks.get("pageNum") == "页数(规范)"
    # 当前值字段元数据优先：.py 虽被手工改成 999，仍读元数据快照 1
    assert result.params.get("pageNum") == "1"
    assert result.headers.get("channel") == "pc"


@allure.feature("API 元数据")
@allure.story("结构化读取优先级")
@allure.title("测试元数据缺当前值字段时按缺省处理")
def test_parse_sidecar_missing_current_field_defaults(tmp_path):
    clear_api_file_cache()
    py_file = tmp_path / "user_list.py"
    py_file.write_text(_STALE_PY_CONTENT, encoding="utf-8")
    # 旧版/缺字段元数据：没有 params 当前值，只有规范字段
    write_api_metadata(
        str(py_file),
        function_name="user_list",
        url="/user/list",
        description="用户列表(规范描述)",
        method="GET",
    )

    result = parse_api_file(str(py_file))

    # 描述/URL/备注来自 API 元数据
    assert result.description == "用户列表(规范描述)"
    assert result.url == "/user/list"
    # .py 模块级赋值（999）不再回退读取：元数据没给 params → 保持空缺省
    assert result.params == {}


@allure.feature("API 元数据")
@allure.story("结构化读取优先级")
@allure.title("测试无元数据时抛出缺少 API 元数据 ValueError")
@allure.description("缺少 .api.json 元数据时直接报错，不回退解析 .py 源码")
def test_parse_missing_sidecar_raises(tmp_path):
    clear_api_file_cache()
    py_file = tmp_path / "order_info.py"
    py_file.write_text(
        '''params = {
    "orderNo": "1001",  # 订单号
}

def order_info(params=params):
    """
    订单详情
    /order/info
    """
    url = "/order/info"
''',
        encoding="utf-8",
    )

    # .py 内容不再被解析：缺少同名 .api.json 元数据直接报错（含重新生成提示）
    with pytest.raises(ValueError, match="缺少 API 元数据"):
        parse_api_file(str(py_file))


@allure.feature("API 元数据")
@allure.story("结构化读取优先级")
@allure.title("测试元数据缺 url 字段时 parse_api_file 抛出 ValueError")
def test_parse_missing_url_raises(tmp_path):
    clear_api_file_cache()
    py_file = tmp_path / "no_url.py"
    py_file.write_text("def no_url(headers=headers):\n    pass\n", encoding="utf-8")
    write_api_metadata(str(py_file), function_name="no_url", method="GET")

    with pytest.raises(ValueError, match="url"):
        parse_api_file(str(py_file))


@allure.feature("API 元数据")
@allure.story("结构化读取优先级")
@allure.title("测试 param_remarks 非 dict 时 parse_api_file 安全处理不崩溃")
def test_parse_non_dict_param_remarks_safe(tmp_path):
    clear_api_file_cache()
    py_file = tmp_path / "bad_remarks.py"
    py_file.write_text(_STALE_PY_CONTENT, encoding="utf-8")
    meta_file = tmp_path / "bad_remarks.api.json"
    meta_file.write_text(
        '{"url": "/user/list", "method": "GET", "param_remarks": "not a dict"}',
        encoding="utf-8",
    )

    result = parse_api_file(str(py_file))

    assert result.url == "/user/list"
    assert result.param_remarks == {}


# ==================== constant_params 读写测试 ====================


@allure.feature("API 元数据")
@allure.story("constant_params 读写")
@allure.title("测试 constant_params 写入与读取 roundtrip")
def test_constant_params_roundtrip(tmp_path):
    py_file = tmp_path / "order_list.py"
    constant = {"header": "1", "isDisSelfStoreOrder": "0"}
    write_api_metadata(
        str(py_file),
        function_name="order_list",
        url="/order/list",
        method="POST",
        constant_params=constant,
    )
    data = read_api_metadata(str(py_file))
    assert data is not None
    assert CONSTANT_PARAMS_FIELD in data
    assert data[CONSTANT_PARAMS_FIELD] == constant


@allure.feature("API 元数据")
@allure.story("constant_params 读写")
@allure.title("测试 constant_params 为 None 时不写入")
def test_constant_params_none_not_written(tmp_path):
    py_file = tmp_path / "demo.py"
    write_api_metadata(str(py_file), url="/demo", method="GET")
    data = read_api_metadata(str(py_file))
    assert data is not None
    assert CONSTANT_PARAMS_FIELD not in data


@allure.feature("API 元数据")
@allure.story("constant_params 读写")
@allure.title("测试 parse_api_file 读取 constant_params")
def test_parse_api_file_reads_constant_params(tmp_path):
    clear_api_file_cache()
    py_file = tmp_path / "order_list.py"
    py_file.write_text(
        'def order_list(params=params):\n    pass\n',
        encoding="utf-8",
    )
    write_api_metadata(
        str(py_file),
        function_name="order_list",
        url="/order/list",
        method="POST",
        constant_params={"header": "1", "isDisSelfStoreOrder": "0"},
    )
    result = parse_api_file(str(py_file))
    assert result.constant_params == {"header": "1", "isDisSelfStoreOrder": "0"}


# ==================== HAR 派生字段读写测试 ====================


@allure.feature("API 元数据")
@allure.story("HAR 派生字段读写")
@allure.title("测试 har_param_values 写入与读取 roundtrip")
def test_har_param_values_roundtrip(tmp_path):
    py_file = tmp_path / "order_list.py"
    values = {"keyword": ["A", "B"], "pageNum": ["1", "2"]}
    write_api_metadata(
        str(py_file),
        url="/order/list",
        method="POST",
        har_param_values=values,
    )
    data = read_api_metadata(str(py_file))
    assert data is not None
    assert data["har_param_values"] == values


@allure.feature("API 元数据")
@allure.story("HAR 派生字段读写")
@allure.title("测试 har_params 写入与读取 roundtrip")
def test_har_params_roundtrip(tmp_path):
    py_file = tmp_path / "order_list.py"
    baseline = {"keyword": "A", "pageNum": "1"}
    write_api_metadata(
        str(py_file),
        url="/order/list",
        method="POST",
        har_params=baseline,
    )
    data = read_api_metadata(str(py_file))
    assert data is not None
    assert data["har_params"] == baseline


@allure.feature("API 元数据")
@allure.story("API 元数据读写")
@allure.title("测试当前值字段空 dict 时仍写入（只跳过 None）")
def test_write_empty_dict_current_values_written(tmp_path):
    py_file = tmp_path / "demo.py"
    write_api_metadata(
        str(py_file),
        url="/demo",
        method="GET",
        params={},
        data={},
        files={},
        headers={},
    )
    data = read_api_metadata(str(py_file))
    assert data is not None
    assert data["params"] == {}
    assert data["data"] == {}
    assert data["files"] == {}
    assert data["headers"] == {}


@allure.feature("API 元数据")
@allure.story("API 元数据读写")
@allure.title("测试 service_package 写入与读取")
def test_service_package_roundtrip(tmp_path):
    py_file = tmp_path / "demo.py"
    write_api_metadata(
        str(py_file),
        url="/demo",
        method="GET",
        service_package="mall_mobile_application",
    )
    data = read_api_metadata(str(py_file))
    assert data is not None
    assert data["service_package"] == "mall_mobile_application"
