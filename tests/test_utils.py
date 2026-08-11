"""
测试 utils.py 模块
"""

import os

import allure

from har2pytest.utils import (
    _API_FILE_CACHE,
    deduplicate_values,
    format_parameter_value,
    parse_api_file,
    sanitize_param_name,
)


@allure.feature("工具函数")
@allure.story("URL提取")
@allure.title("测试从文件中提取URL")
def test_parse_api_file_url():
    test_content = '''def user_login(data=data, headers=headers):
    """
    用户登录
    /user/login
    """
    url = "/user/login"
'''
    with open("test_url.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("test_url.py")
        assert result is not None
        assert result.description == "用户登录"
        assert result.url == "/user/login"
    finally:
        if os.path.exists("test_url.py"):
            os.remove("test_url.py")


@allure.feature("工具函数")
@allure.story("URL提取")
@allure.title("测试从API文件中提取URL")
def test_extract_url_from_api_file():
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

    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("test_api.py")
        assert result is not None
        assert result.description == "PC店铺查询兑换订单列表"
        assert result.url == "/user/order/getStoreAgentOrderList"
    finally:
        import os

        if os.path.exists("test_api.py"):
            os.remove("test_api.py")


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
def test_parse_api_file_headers():
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

    with open("test_api_headers.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("test_api_headers.py")
        assert result is not None
        headers = result.headers
        assert "channel" in headers
        assert headers["channel"] == "pc"
        assert "content-type" in headers
        assert headers["content-type"] == "application/json;charset=UTF-8"
    finally:
        if os.path.exists("test_api_headers.py"):
            os.remove("test_api_headers.py")


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
    result = deduplicate_values([
        {"items": [{"b": 2, "a": 1}]},
        {"items": [{"a": 1, "b": 2}]},
    ])
    assert len(result) == 1
