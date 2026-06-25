"""
测试 utils.py 模块
"""

import allure

from har2pytest.utils import (
    _API_FILE_CACHE,
    format_parameter_value,
    parse_api_file,
)


@allure.feature("工具函数")
@allure.story("URL提取")
@allure.title("测试从文件中提取URL")
def test_parse_api_file_url():
    test_content = '''def _user_login(data=data, headers=headers):
    """
    用户登录
    /user/login
    """
    url = "/user/login"
'''
    with open("test_url.txt", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("test_url.txt")
        assert result is not None
        assert result["description"] == "用户登录"
        assert result["url"] == "/user/login"
    finally:
        import os

        if os.path.exists("test_url.txt"):
            os.remove("test_url.txt")


@allure.feature("工具函数")
@allure.story("URL提取")
@allure.title("测试从API文件中提取URL")
def test_extract_url_from_api_file():
    _API_FILE_CACHE.clear()
    test_content = '''from util.client import client

def _user_order_getStoreAgentOrderList(data=data, headers=headers):
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
        assert result["description"] == "PC店铺查询兑换订单列表"
        assert result["url"] == "/user/order/getStoreAgentOrderList"
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
    test_content = '''from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}

def _user_login(data=data, headers=headers):
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
        headers = result["headers"]
        assert "channel" in headers
        assert headers["channel"] == "pc"
        assert "content-type" in headers
        assert headers["content-type"] == "application/json;charset=UTF-8"
    finally:
        import os

        if os.path.exists("test_api_headers.py"):
            os.remove("test_api_headers.py")