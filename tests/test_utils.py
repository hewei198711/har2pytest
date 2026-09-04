"""
测试 utils.py 模块
"""

import logging
import os
from unittest.mock import AsyncMock, MagicMock

import allure

from har2pytest import utils as utils_module
from har2pytest.models import ParsedRequestInfo
from har2pytest.utils import (
    _API_FILE_CACHE,
    _format_nested,
    clear_api_file_cache,
    deduplicate_values,
    format_directory,
    format_headers_for_python,
    format_parameter_value,
    format_params_for_python,
    get_output_dir,
    header_value_formatter,
    merge_request_params,
    parse_api_file,
    sanitize_param_name,
    write_test_file,
)


@allure.feature("工具函数")
@allure.story("URL提取")
@allure.title("测试从文件中提取URL")
def test_parse_api_file_url(tmp_path):
    test_content = '''def user_login(data=data, headers=headers):
    """
    用户登录
    /user/login
    """
    url = "/user/login"
'''
    api_file = tmp_path / "test_url.py"
    api_file.write_text(test_content, encoding="utf-8")

    result = parse_api_file(str(api_file))
    assert result is not None
    assert result.description == "用户登录"
    assert result.url == "/user/login"


@allure.feature("工具函数")
@allure.story("URL提取")
@allure.title("测试从API文件中提取URL")
def test_extract_url_from_api_file(tmp_path):
    _API_FILE_CACHE.clear()
    test_content = '''from har2pytest.client import client

def user_order_getStoreAgentOrderList(data=data, headers=headers):
    """
    PC店铺查询兑换订单列表
    /user/order/getStoreAgentOrderList

    参数说明:
    - orderNo: 兑换流水号
    - pageNum: 页码
    """

    url = "/user/order/getStoreAgentOrderList"
'''

    api_file = tmp_path / "test_api.py"
    api_file.write_text(test_content, encoding="utf-8")

    result = parse_api_file(str(api_file))
    assert result is not None
    assert result.description == "PC店铺查询兑换订单列表"
    assert result.url == "/user/order/getStoreAgentOrderList"


@allure.feature("工具函数")
@allure.story("参数值格式化")
@allure.title("测试参数值格式化为Python字符串")
def test_format_parameter_value():
    assert format_parameter_value("test") == '"test"'

    assert format_parameter_value(123) == "123"
    assert format_parameter_value(123.456) == "123.456"

    assert format_parameter_value(True) == "True"
    assert format_parameter_value(False) == "False"

    assert format_parameter_value(None) == "None"

    assert format_parameter_value([1, 2, 3]) == "[1, 2, 3]"

    assert format_parameter_value({"a": 1, "b": 2}) == '{"a": 1, "b": 2}'


@allure.feature("工具函数")
@allure.story("Headers提取")
@allure.title("测试从API文件中提取headers配置")
def test_parse_api_file_headers(tmp_path):
    test_content = '''from har2pytest.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['token']}",
}

def user_login(data=data, headers=headers):
    """
    用户登录
    /user/login
    """

    url = "/user/login"
'''

    api_file = tmp_path / "test_api_headers.py"
    api_file.write_text(test_content, encoding="utf-8")

    result = parse_api_file(str(api_file))
    assert result is not None
    headers = result.headers
    assert "channel" in headers
    assert headers["channel"] == "pc"
    assert "content-type" in headers
    assert headers["content-type"] == "application/json;charset=UTF-8"


@allure.feature("工具函数")
@allure.story("参数名清理")
@allure.title("测试清理参数名避免 Python 关键字冲突")
def test_sanitize_param_name():
    """测试清理参数名，对于 Python 关键字追加下划线后缀。"""
    assert sanitize_param_name("from") == "from_"
    assert sanitize_param_name("class") == "class_"
    assert sanitize_param_name("def") == "def_"
    assert sanitize_param_name("return") == "return_"
    assert sanitize_param_name("user_id") == "user_id"
    assert sanitize_param_name("from_user") == "from_user"


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试基本类型去重")
def test_deduplicate_values_primitives():
    """验证基本类型值的去重。"""
    assert deduplicate_values([1, 2, 2, 3]) == [1, 2, 3]
    assert deduplicate_values(["a", "b", "a"]) == ["a", "b"]
    assert deduplicate_values([True, False, True]) == [True, False]
    assert deduplicate_values([None, None, 1]) == [None, 1]


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试 dict 去重（含键顺序不同）")
def test_deduplicate_values_dicts():
    """验证 dict 去重，sort_keys 确保键顺序不影响去重。"""
    result = deduplicate_values([{"b": 2, "a": 1}, {"a": 1, "b": 2}])
    assert result == [{"b": 2, "a": 1}]


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试 list 去重")
def test_deduplicate_values_lists():
    """验证 list 去重。"""
    result = deduplicate_values([[1, 2], [1, 2], [3, 4]])
    assert result == [[1, 2], [3, 4]]


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试 raw string 与 JSON 序列化结果不碰撞")
def test_deduplicate_values_no_cross_type_collision():
    """验证 raw string 不会与 json.dumps 输出碰撞导致错误去重。"""
    result = deduplicate_values(['{"a": 1}', {"a": 1}])
    assert len(result) == 2
    assert '{"a": 1}' in result
    assert {"a": 1} in result


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试嵌套结构去重")
def test_deduplicate_values_nested():
    """验证嵌套 list/dict 结构的去重。"""
    result = deduplicate_values(
        [
            {"items": [{"b": 2, "a": 1}]},
            {"items": [{"a": 1, "b": 2}]},
        ]
    )
    assert len(result) == 1


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试无docstring时函数名从文件名提取")
def test_parse_api_file_function_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "my_api_func.py"
    api_file.write_text("def my_api_func(headers=headers):\n    pass\n", encoding="utf-8")

    result = parse_api_file(str(api_file))

    assert result.function_name == "my_api_func"
    assert result.description == ""
    assert result.url is None


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试单引号docstring解析")
def test_parse_api_file_single_quote_docstring(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "single_quote.py"
    api_file.write_text(
        "def single_quote(headers=headers):\n    '''\n    单引号描述\n    /api/single-quote\n    '''\n",
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))

    assert result.description == "单引号描述"
    assert result.url == "/api/single-quote"


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试params嵌套字典与dotted key备注提取")
def test_parse_api_file_params_nested_remarks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    content = '''params = {
    "pageNum": 1,  # 页码
    "payDTO": {
        "accountName": "test",  # 账户名
    },
}

def api_demo(params=params, headers=headers):
    """
    接口描述
    /api/demo
    """
'''
    api_file = tmp_path / "api_demo.py"
    api_file.write_text(content, encoding="utf-8")

    result = parse_api_file(str(api_file))

    assert result.function_name == "api_demo"
    assert result.params == {"pageNum": 1, "payDTO": {"accountName": "test"}}
    assert result.param_remarks["pageNum"] == "页码"
    # 嵌套 dict 的备注使用 dotted key
    assert result.param_remarks["payDTO.accountName"] == "账户名"


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试data为JSON数组形式时解析为list")
def test_parse_api_file_data_list(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    content = '''data = [{"app_id": "uc-pc", "page": "home"}, {"app_id": "uc-pc"}]

def behavior_collect(data=data, headers=headers):
    """
    行为采集
    /isomer/datacollect/behaviorCollect
    """
'''
    api_file = tmp_path / "behavior.py"
    api_file.write_text(content, encoding="utf-8")

    result = parse_api_file(str(api_file))

    assert isinstance(result.data, list)
    assert result.data[0]["app_id"] == "uc-pc"
    assert len(result.data) == 2


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试files参数提取")
def test_parse_api_file_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    content = '''files = {
    "file": "test.txt",  # 上传文件
}

def upload(files=files, headers=headers):
    """
    上传
    /api/upload
    """
'''
    api_file = tmp_path / "upload.py"
    api_file.write_text(content, encoding="utf-8")

    result = parse_api_file(str(api_file))

    assert result.files == {"file": "test.txt"}
    assert result.param_remarks["file"] == "上传文件"


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试文件不存在时记录错误日志")
def test_parse_api_file_not_found(caplog):
    caplog.set_level(logging.ERROR, logger="har2pytest")

    result = parse_api_file("nonexistent_xyz.py")

    # 函数名仍从文件路径提取，读取失败记录错误日志
    assert result.function_name == "nonexistent_xyz"
    assert "读取API文件" in caplog.text


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试解析结果缓存与清除")
def test_parse_api_file_cache(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "cached_api.py"
    api_file.write_text('def cached_api():\n    """\n    旧描述\n    /old\n    """\n', encoding="utf-8")

    first = parse_api_file(str(api_file))
    assert first.description == "旧描述"

    # 修改文件内容后再次解析，命中缓存结果不变
    api_file.write_text('def cached_api():\n    """\n    新描述\n    /new\n    """\n', encoding="utf-8")
    second = parse_api_file(str(api_file))
    assert second.description == "旧描述"

    # 清除缓存后重新解析，读到最新内容
    clear_api_file_cache()
    third = parse_api_file(str(api_file))
    assert third.description == "新描述"


@allure.feature("工具函数")
@allure.story("输出目录")
@allure.title("测试无task_id时输出目录为基础目录")
def test_get_output_dir_without_task_id(tmp_path):
    result = get_output_dir(str(tmp_path))
    assert result == str(tmp_path)
    assert os.path.isdir(result)


@allure.feature("工具函数")
@allure.story("输出目录")
@allure.title("测试带task_id时创建子目录")
def test_get_output_dir_with_task_id(tmp_path):
    result = get_output_dir(str(tmp_path), "task_4291")
    assert result == str(tmp_path / "task_4291")
    assert os.path.isdir(result)


@allure.feature("工具函数")
@allure.story("文件写入")
@allure.title("测试写入测试文件")
def test_write_test_file(tmp_path):
    target = tmp_path / "output.py"

    write_test_file(str(target), "content = 1\n")

    assert target.read_text(encoding="utf-8") == "content = 1\n"


@allure.feature("工具函数")
@allure.story("目录格式化")
@allure.title("测试目录不存在时记录警告并返回")
async def test_format_directory_missing_dir(caplog):
    caplog.set_level(logging.WARNING, logger="har2pytest")

    await format_directory("nonexistent_dir_xyz")

    assert "格式化目录不存在" in caplog.text


@allure.feature("工具函数")
@allure.story("目录格式化")
@allure.title("测试依次执行ruff check与ruff format")
async def test_format_directory_success(monkeypatch, tmp_path):
    proc = MagicMock()
    proc.returncode = 0
    proc.wait = AsyncMock()
    create_subprocess = AsyncMock(return_value=proc)
    monkeypatch.setattr(utils_module.asyncio, "create_subprocess_exec", create_subprocess)

    await format_directory(str(tmp_path))

    assert create_subprocess.await_count == 2
    # 第一次调用: ruff check --fix --ignore E402 --no-respect-gitignore <dir>
    first_args = create_subprocess.await_args_list[0].args
    assert first_args[2] == "ruff"
    assert first_args[3] == "check"
    assert first_args[4] == "--fix"
    assert first_args[5] == "--ignore"
    assert first_args[6] == "E402"
    assert first_args[7] == "--no-respect-gitignore"
    assert first_args[8] == str(tmp_path)
    # 第二次调用: ruff format --no-respect-gitignore <dir>
    second_args = create_subprocess.await_args_list[1].args
    assert second_args[2] == "ruff"
    assert second_args[3] == "format"
    assert second_args[4] == "--no-respect-gitignore"
    assert second_args[5] == str(tmp_path)


@allure.feature("工具函数")
@allure.story("目录格式化")
@allure.title("测试ruff返回非零退出码时记录警告")
async def test_format_directory_ruff_nonzero(monkeypatch, tmp_path, caplog):
    caplog.set_level(logging.WARNING, logger="har2pytest")
    proc = MagicMock()
    proc.returncode = 1
    proc.wait = AsyncMock()
    monkeypatch.setattr(utils_module.asyncio, "create_subprocess_exec", AsyncMock(return_value=proc))

    await format_directory(str(tmp_path))

    assert "返回非零退出码" in caplog.text


@allure.feature("工具函数")
@allure.story("目录格式化")
@allure.title("测试subprocess异常时记录警告")
async def test_format_directory_exception(monkeypatch, tmp_path, caplog):
    caplog.set_level(logging.WARNING, logger="har2pytest")
    monkeypatch.setattr(utils_module.asyncio, "create_subprocess_exec", AsyncMock(side_effect=OSError("boom")))

    await format_directory(str(tmp_path))

    assert "执行失败" in caplog.text


@allure.feature("工具函数")
@allure.story("请求参数合并")
@allure.title("测试query参数与body参数合并")
def test_merge_request_params_query_and_post():
    info = ParsedRequestInfo(query_params={"page": 1, "size": 10}, post_data={"name": "test"})

    result = merge_request_params(info)

    assert result == {"page": 1, "size": 10, "name": "test"}


@allure.feature("工具函数")
@allure.story("请求参数合并")
@allure.title("测试post_data覆盖同名query参数")
def test_merge_request_params_post_overrides_query():
    info = ParsedRequestInfo(query_params={"name": "query"}, post_data={"name": "post"})

    result = merge_request_params(info)

    assert result == {"name": "post"}


@allure.feature("工具函数")
@allure.story("请求参数合并")
@allure.title("测试非字典post_data跳过合并")
def test_merge_request_params_non_dict_post_data(caplog):
    caplog.set_level(logging.DEBUG, logger="har2pytest")
    info = ParsedRequestInfo(query_params={"page": 1}, post_data=[{"app_id": "uc-pc"}])

    result = merge_request_params(info)

    # list 类型的 post_data（JSON 数组请求体）不参与合并
    assert result == {"page": 1}
    assert "post_data不是字典类型" in caplog.text


@allure.feature("工具函数")
@allure.story("请求参数合并")
@allure.title("测试query与body均为空时返回空字典")
def test_merge_request_params_empty():
    result = merge_request_params(ParsedRequestInfo())
    assert result == {}


@allure.feature("工具函数")
@allure.story("Headers格式化")
@allure.title("测试header值格式化")
def test_header_value_formatter():
    # 普通字符串包装引号
    assert header_value_formatter("pc") == '"pc"'
    # 已带引号的字符串原样返回
    assert header_value_formatter('"pc"') == '"pc"'
    # f-string 中的 os.environ 下标访问转为安全访问
    assert header_value_formatter("f\"bearer {os.environ['token']}\"") == "f\"bearer {os.environ.get('token', '')}\""


@allure.feature("工具函数")
@allure.story("Headers格式化")
@allure.title("测试headers字典格式化为Python代码")
def test_format_headers_for_python():
    headers = {"channel": "pc", "authorization": "f\"bearer {os.environ['token']}\""}

    result = format_headers_for_python(headers)

    assert '"channel": "pc"' in result
    assert "os.environ.get('token', '')" in result


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试空参数字典返回空字典字面量")
def test_format_params_for_python_empty():
    assert format_params_for_python({}) == "{}"


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试嵌套字典注释与dotted key查找")
def test_format_params_for_python_comments_and_nested():
    params = {"user": {"name": "t", "age": 1}}
    comments = {"user": "用户", "user.name": "用户名", "user.age": "年龄"}

    result = format_params_for_python(params, comments=comments)

    assert '"name":' in result
    assert "# 用户名" in result
    assert "# 年龄" in result
    # 所有 key 均有注释时不生成 TODO 回退
    assert "TODO" not in result


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试无对应注释时生成TODO回退注释")
def test_format_params_for_python_todo_fallback():
    result = format_params_for_python({"a": 1}, comments={"other": "x"})

    assert "# TODO: 添加参数说明" in result


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试注释中的换行符被替换为空格")
def test_format_params_for_python_comment_newline_sanitized():
    result = format_params_for_python({"a": 1}, comments={"a": "多行\n注释"})

    assert "# 多行 注释" in result


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试内联格式输出")
def test_format_params_for_python_inline():
    result = format_params_for_python({"a": 1, "b": 2}, inline=True)

    assert result.startswith("{")
    assert '"a": 1' in result
    assert '"b": 2' in result
    assert result.endswith("}")


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试自定义值格式化函数")
def test_format_params_for_python_custom_formatter():
    params = {"auth": "f\"bearer {os.environ['token']}\""}

    result = format_params_for_python(params, value_formatter=header_value_formatter)

    assert "os.environ.get('token', '')" in result


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试嵌套值递归格式化为Python字面量")
def test_format_nested_complex():
    value = {"a": [1, None, True], "b": {"c": "中文"}}

    result = _format_nested(value)

    # None/True 使用 Python 字面量，中文字符保留
    assert result == '{"a": [1, None, True], "b": {"c": "中文"}}'


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试不支持类型使用repr兜底")
def test_format_parameter_value_fallback_repr():
    result = format_parameter_value(object())

    assert result.startswith("<object object")


@allure.feature("工具函数")
@allure.story("参数格式化")
@allure.title("测试嵌套值不支持类型使用repr兜底")
def test_format_nested_fallback_repr():
    result = _format_nested({1, 2})

    assert result.startswith("{1, 2}")


@allure.feature("工具函数")
@allure.story("API文件解析")
@allure.title("测试参数解析失败时记录错误日志")
def test_parse_api_file_invalid_dict(caplog, tmp_path, monkeypatch):
    caplog.set_level(logging.ERROR, logger="har2pytest")
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "broken.py"
    api_file.write_text("data = {broken\n", encoding="utf-8")

    result = parse_api_file(str(api_file))

    assert result.data == {}
    assert "解析 data 字典失败" in caplog.text
