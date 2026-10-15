"""测试 har2pytest.utils 中参数格式化、文件处理、API 文件解析、参数合并、URL 规范化、值去重与参数名清理等工具函数的功能与边界。"""

import json
import logging
from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from har2pytest import utils as utils_module
from har2pytest.models import ParsedRequestInfo
from har2pytest.utils import (
    _extract_date_format_from_remark,
    build_time_pairs,
    clear_api_file_cache,
    deduplicate_values,
    extract_service_package,
    format_directory,
    format_headers_for_python,
    format_parameter_value,
    format_params_for_python,
    header_value_formatter,
    merge_request_params,
    parse_api_file,
    sanitize_param_name,
    sanitize_remark,
    write_test_file,
)

# ==================== API 文件解析测试 ====================


@allure.feature("工具函数")
@allure.story("URL提取")
@allure.title("测试从 API 元数据(.api.json)中提取URL与描述")
def test_parse_api_file_url(tmp_path):
    api_file = tmp_path / "test_url.py"
    api_file.write_text("def user_login():\n    pass\n", encoding="utf-8")

    # 描述与 URL 以元数据为准（不再解析 .py 的 docstring）
    api_file.with_suffix(".api.json").write_text(
        json.dumps({"url": "/user/login", "description": "用户登录"}, ensure_ascii=False),
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))
    assert result is not None
    assert result.description == "用户登录"
    assert result.url == "/user/login"


# ==================== 参数值格式化测试 ====================


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
@allure.title("测试从 API 元数据(.api.json)中提取headers配置")
def test_parse_api_file_headers(tmp_path):
    api_file = tmp_path / "test_api_headers.py"
    api_file.write_text("def user_login():\n    pass\n", encoding="utf-8")

    # headers 当前值以元数据为准（原 .py 模块级赋值 → .api.json 的 headers 字段）
    api_file.with_suffix(".api.json").write_text(
        json.dumps(
            {
                "url": "/user/login",
                "description": "用户登录",
                "headers": {
                    "channel": "pc",
                    "client": "op",
                    "content-type": "application/json;charset=UTF-8",
                    "authorization": "f\"bearer {os.environ['token']}\"",
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))
    assert result is not None
    headers = result.headers
    assert "channel" in headers
    assert headers["channel"] == "pc"
    assert "content-type" in headers
    assert headers["content-type"] == "application/json;charset=UTF-8"


# ==================== 参数名清理测试 ====================


@allure.feature("工具函数")
@allure.story("参数名清理")
@allure.title("测试清理参数名避免 Python 关键字冲突")
def test_sanitize_param_name():
    assert sanitize_param_name("from") == "from_"
    assert sanitize_param_name("class") == "class_"
    assert sanitize_param_name("def") == "def_"
    assert sanitize_param_name("return") == "return_"
    assert sanitize_param_name("user_id") == "user_id"
    assert sanitize_param_name("from_user") == "from_user"
    # 空字符串返回默认前缀
    assert sanitize_param_name("") == "param_"
    # 数字开头时加 param_ 前缀
    assert sanitize_param_name("123abc") == "param_123abc"


# ==================== 值去重测试 ====================


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试基本类型去重")
def test_deduplicate_values_primitives():
    assert deduplicate_values([1, 2, 2, 3]) == [1, 2, 3]
    assert deduplicate_values(["a", "b", "a"]) == ["a", "b"]
    assert deduplicate_values([True, False, True]) == [True, False]
    assert deduplicate_values([None, None, 1]) == [None, 1]


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试 dict 去重（含键顺序不同）")
def test_deduplicate_values_dicts():
    result = deduplicate_values([{"b": 2, "a": 1}, {"a": 1, "b": 2}])
    assert result == [{"b": 2, "a": 1}]


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试 list 去重")
def test_deduplicate_values_lists():
    result = deduplicate_values([[1, 2], [1, 2], [3, 4]])
    assert result == [[1, 2], [3, 4]]


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试 raw string 与 JSON 序列化结果不碰撞")
def test_deduplicate_values_no_cross_type_collision():
    result = deduplicate_values(['{"a": 1}', {"a": 1}])
    assert len(result) == 2
    assert '{"a": 1}' in result
    assert {"a": 1} in result


@allure.feature("工具函数")
@allure.story("值去重")
@allure.title("测试嵌套结构去重")
def test_deduplicate_values_nested():
    result = deduplicate_values(
        [
            {"items": [{"b": 2, "a": 1}]},
            {"items": [{"a": 1, "b": 2}]},
        ]
    )
    assert len(result) == 1


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试函数名取自文件名且元数据无 description 时缺省为空")
def test_parse_api_file_function_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "my_api_func.py"
    api_file.write_text("def my_api_func(headers=headers):\n    pass\n", encoding="utf-8")
    # 元数据只给必需字段 url、不给 description → 描述缺省为空字符串
    api_file.with_suffix(".api.json").write_text(
        json.dumps({"url": "/api/my_api_func"}),
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))

    assert result.function_name == "my_api_func"
    assert result.description == ""
    assert result.url == "/api/my_api_func"


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试元数据中的嵌套params与dotted key备注")
def test_parse_api_file_params_nested_remarks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "api_demo.py"
    api_file.write_text("def api_demo(params=params, headers=headers):\n    pass\n", encoding="utf-8")
    # params 当前值与备注(含 dotted key)取自元数据
    api_file.with_suffix(".api.json").write_text(
        json.dumps(
            {
                "url": "/api/demo",
                "description": "接口描述",
                "params": {"pageNum": 1, "payDTO": {"accountName": "test"}},
                "param_remarks": {"pageNum": "页码", "payDTO.accountName": "账户名"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))

    assert result.function_name == "api_demo"
    assert result.params == {"pageNum": 1, "payDTO": {"accountName": "test"}}
    assert result.param_remarks["pageNum"] == "页码"
    # 嵌套 dict 的备注使用 dotted key
    assert result.param_remarks["payDTO.accountName"] == "账户名"


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试元数据备注中的换行符被压成单行")
def test_parse_api_file_remarks_newline_flattened(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "gift_order.py"
    api_file.write_text("def gift_order(data=data, headers=headers):\n    pass\n", encoding="utf-8")
    api_file.with_suffix(".api.json").write_text(
        json.dumps(
            {
                "url": "/mgmt/activityGift/giftOrder/pageQuery",
                "description": "分页查询礼物订单活动列表",
                "data": {"orderStatusList": []},
                "param_remarks": {
                    "orderStatusList": "订单状态集合（参考OrderStatus枚举）：\n1:待支付, 2:待发货",
                    "receiverName": "收礼人姓名",
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))

    assert result.param_remarks["orderStatusList"] == "订单状态集合（参考OrderStatus枚举）： 1:待支付, 2:待发货"
    assert "\n" not in result.param_remarks["orderStatusList"]
    assert result.param_remarks["receiverName"] == "收礼人姓名"


# ==================== 参数备注清洗测试 ====================


@allure.feature("工具函数")
@allure.story("参数备注清洗")
@allure.title("测试备注文本规范化为单行")
def test_sanitize_remark():
    # 换行、制表符、续行缩进统一折叠为单个空格
    assert sanitize_remark("第一行\n    第二行\t第三行") == "第一行 第二行 第三行"
    assert sanitize_remark("  两侧空白  ") == "两侧空白"
    assert sanitize_remark("状态：\r\n1:待支付") == "状态： 1:待支付"
    # 中文全角空格保留原样
    assert sanitize_remark("待支付\u3000已取消") == "待支付\u3000已取消"
    # 非字符串返回空串
    assert sanitize_remark(None) == ""
    assert sanitize_remark(123) == ""


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试元数据中data为JSON数组形式时解析为list")
def test_parse_api_file_data_list(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "behavior.py"
    api_file.write_text("def behavior_collect(data=data, headers=headers):\n    pass\n", encoding="utf-8")
    # data 当前值取自元数据（JSON 数组请求体 → list）
    api_file.with_suffix(".api.json").write_text(
        json.dumps(
            {
                "url": "/isomer/datacollect/behaviorCollect",
                "description": "行为采集",
                "data": [{"app_id": "uc-pc", "page": "home"}, {"app_id": "uc-pc"}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))

    assert isinstance(result.data, list)
    assert result.data[0]["app_id"] == "uc-pc"
    assert len(result.data) == 2


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试元数据中的files参数与备注提取")
def test_parse_api_file_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "upload.py"
    api_file.write_text("def upload(files=files, headers=headers):\n    pass\n", encoding="utf-8")
    # files 当前值与备注取自元数据（原 .py 行内 # 注释 → param_remarks）
    api_file.with_suffix(".api.json").write_text(
        json.dumps(
            {
                "url": "/api/upload",
                "description": "上传",
                "files": {"file": "test.txt"},
                "param_remarks": {"file": "上传文件"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = parse_api_file(str(api_file))

    assert result.files == {"file": "test.txt"}
    assert result.param_remarks["file"] == "上传文件"


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试无同名 .api.json 元数据时抛出缺少元数据 ValueError")
def test_parse_api_file_not_found():
    # .py 是否存在不再影响解析：没有同名 .api.json 元数据直接报错并提示重新生成
    with pytest.raises(ValueError, match="缺少 API 元数据"):
        parse_api_file("nonexistent_xyz.py")


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试解析结果缓存与清除(元数据为准)")
def test_parse_api_file_cache(tmp_path, monkeypatch):
    clear_api_file_cache()
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "cached_api.py"
    api_file.write_text("def cached_api():\n    pass\n", encoding="utf-8")
    meta_file = api_file.with_suffix(".api.json")
    meta_file.write_text(
        json.dumps({"url": "/old", "description": "旧描述"}, ensure_ascii=False),
        encoding="utf-8",
    )

    first = parse_api_file(str(api_file))
    assert first.description == "旧描述"

    # 修改元数据后再次解析，命中缓存结果不变
    meta_file.write_text(
        json.dumps({"url": "/new", "description": "新描述"}, ensure_ascii=False),
        encoding="utf-8",
    )
    second = parse_api_file(str(api_file))
    assert second.description == "旧描述"

    # 清除缓存后重新解析，读到最新元数据
    clear_api_file_cache()
    third = parse_api_file(str(api_file))
    assert third.description == "新描述"


# ==================== 文件写入测试 ====================


@allure.feature("工具函数")
@allure.story("文件写入")
@allure.title("测试写入测试文件")
def test_write_test_file(tmp_path):
    target = tmp_path / "output.py"

    write_test_file(str(target), "content = 1\n")

    assert target.read_text(encoding="utf-8") == "content = 1\n"


# ==================== 目录格式化测试 ====================


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


# ==================== 请求参数合并测试 ====================


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


# ==================== Headers格式化测试 ====================


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
    # 非字符串类型使用 repr 兆底
    assert header_value_formatter(123) == "123"


@allure.feature("工具函数")
@allure.story("Headers格式化")
@allure.title("测试headers字典格式化为Python代码")
def test_format_headers_for_python():
    headers = {"channel": "pc", "authorization": "f\"bearer {os.environ['token']}\""}

    result = format_headers_for_python(headers)

    assert '"channel": "pc"' in result
    assert "os.environ.get('token', '')" in result


# ==================== 参数格式化测试 ====================


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
def test_format_parameter_value_complex():
    value = {"a": [1, None, True], "b": {"c": "中文"}}

    result = format_parameter_value(value)

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
def test_format_parameter_value_set_repr():
    result = format_parameter_value({1, 2})

    assert result.startswith("{1, 2}")


@allure.feature("工具函数")
@allure.story("API 文件解析")
@allure.title("测试有 .api.json 但缺必需字段 url 时抛出 ValueError(.py 不再解析)")
def test_parse_api_file_metadata_missing_url(tmp_path, monkeypatch):
    clear_api_file_cache()
    monkeypatch.chdir(tmp_path)
    api_file = tmp_path / "broken.py"
    # .py 语法损坏与否已不影响解析：元数据缺必需字段 url 即报错提示
    api_file.write_text("data = {broken\n", encoding="utf-8")
    api_file.with_suffix(".api.json").write_text(
        json.dumps({"description": "缺少url的元数据"}, ensure_ascii=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="url"):
        parse_api_file(str(api_file))


# ==================== 时间参数对解析测试 ====================


@allure.feature("工具函数")
@allure.story("时间参数对解析")
@allure.title("测试 build_time_pairs 识别时间对并提取格式")
def test_build_time_pairs_basic(monkeypatch):
    if utils_module.APIConfig._config is None:
        utils_module.APIConfig._config = utils_module.APIConfig._load_config()
    monkeypatch.setitem(
        utils_module.APIConfig._config, "TIME_PARAMS", ["starttime", "endtime"]
    )
    remarks = {
        "getTimeStartTime": "领取时间开始时间(yyyy-MM-dd)",
        "getTimeEndTime": "领取时间结束时间(yyyy-MM-dd)",
        "cardNo": "会员卡号",
    }
    result = build_time_pairs(remarks)
    assert "getTime" in result
    assert result["getTime"]["start"] == "getTimeStartTime"
    assert result["getTime"]["end"] == "getTimeEndTime"
    assert result["getTime"]["format"] == "%Y-%m-%d"


@allure.feature("工具函数")
@allure.story("时间参数对解析")
@allure.title("测试 build_time_pairs 无配对时返回空")
def test_build_time_pairs_no_pair(monkeypatch):
    if utils_module.APIConfig._config is None:
        utils_module.APIConfig._config = utils_module.APIConfig._load_config()
    monkeypatch.setitem(
        utils_module.APIConfig._config, "TIME_PARAMS", ["starttime", "endtime"]
    )
    # 只有 start 没有 end
    remarks = {"getTimeStartTime": "开始时间(yyyy-MM-dd)"}
    assert build_time_pairs(remarks) == {}


@allure.feature("工具函数")
@allure.story("时间参数对解析")
@allure.title("测试 build_time_pairs 空备注时返回空")
def test_build_time_pairs_empty_remarks(monkeypatch):
    if utils_module.APIConfig._config is None:
        utils_module.APIConfig._config = utils_module.APIConfig._load_config()
    monkeypatch.setitem(
        utils_module.APIConfig._config, "TIME_PARAMS", ["starttime", "endtime"]
    )
    assert build_time_pairs({}) == {}


# ==================== 服务包提取测试 ====================


@allure.feature("工具函数")
@allure.story("服务包提取")
@allure.title("测试从 API 文件路径提取服务包名")
def test_extract_service_package():
    # 正常子目录结构
    assert extract_service_package("/root/apis/user/info.py", "/root/apis") == "user"
    # 文件直接在 api_dir 下，无服务包
    assert extract_service_package("/root/apis/info.py", "/root/apis") is None
    # 多层嵌套取首段
    assert extract_service_package("/root/apis/trade/order/list.py", "/root/apis") == "trade"


# ==================== 时间参数对解析测试 ====================


@allure.feature("工具函数")
@allure.story("时间参数对解析")
@allure.title("测试 _extract_date_format_from_remark 格式提取")
@pytest.mark.parametrize("remark,expected", [
    ("领取时间开始时间(yyyy-MM-dd)", "%Y-%m-%d"),
    ("创建时间（yyyy-MM-dd HH:mm:ss）", "%Y-%m-%d %H:%M:%S"),
    ("无格式备注", "%Y-%m-%d"),  # 默认格式
    ("时间(yyyy/MM/dd)", "%Y/%m/%d"),
])
def test_extract_date_format_from_remark(remark, expected):
    assert _extract_date_format_from_remark(remark) == expected
