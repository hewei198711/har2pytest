"""
测试 utils.py 模块
"""

import allure

from har2pytest.url_matcher import get_url_from_api_file
from har2pytest.utils import (
    escape_string_for_python,
    format_parameter_value,
    get_headers_from_api_file,
)


@allure.feature("工具函数")
@allure.story("URL提取")
def test_get_url_from_api_file():
    """测试从文件中提取URL"""
    # 测试从文件中提取URL
    test_content = "some content https://example.com/api/test some more content"
    with open("test_url.txt", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = get_url_from_api_file("test_url.txt")
        assert result is not None
        assert result[1] == "https://example.com/api/test"
    finally:
        import os

        if os.path.exists("test_url.txt"):
            os.remove("test_url.txt")


@allure.feature("工具函数")
@allure.story("URL提取")
def test_extract_url_from_api_file():
    """测试从API文件中提取URL（真实的API文件格式）"""
    # 测试真实的API文件格式
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
        result = get_url_from_api_file("test_api.py")
        assert result is not None
        assert result[0] == "PC店铺查询兑换订单列表"
        assert result[1] == "/user/order/getStoreAgentOrderList"
    finally:
        import os

        if os.path.exists("test_api.py"):
            os.remove("test_api.py")


@allure.feature("工具函数")
@allure.story("参数值格式化")
def test_format_parameter_value():
    """测试参数值格式化为Python字符串"""
    # 测试字符串值
    assert format_parameter_value("test") == '"test"'

    # 测试数字值
    assert format_parameter_value(123) == "123"
    assert format_parameter_value(123.456) == "123.456"

    # 测试布尔值
    assert format_parameter_value(True) == "True"
    assert format_parameter_value(False) == "False"

    # 测试 None 值
    assert format_parameter_value(None) == "None"

    # 测试列表值
    assert format_parameter_value([1, 2, 3]) == "[1, 2, 3]"

    # 测试字典值
    assert format_parameter_value({"a": 1, "b": 2}) == '{"a": 1, "b": 2}'


@allure.feature("工具函数")
@allure.story("字符串转义")
def test_escape_string_for_python():
    """测试字符串转义为Python格式"""
    # 测试普通字符串
    assert escape_string_for_python("test") == "test"

    # 测试包含引号的字符串
    assert escape_string_for_python('test"quote') == 'test"quote'
    assert escape_string_for_python("test'quote") == "test'quote"

    # 测试包含换行符的字符串
    assert escape_string_for_python("test\nline") == "test\\nline"

    # 测试包含制表符的字符串
    assert escape_string_for_python("test\ttab") == "test\\ttab"


@allure.feature("工具函数")
@allure.story("Headers提取")
def test_get_headers_from_api_file():
    """测试从API文件中提取headers配置"""
    # 测试真实的API文件格式
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
        result = get_headers_from_api_file("test_api_headers.py")
        assert result is not None
        assert "channel" in result
        assert result["channel"] == '"pc"'
        assert "content-type" in result
        assert result["content-type"] == '"application/json;charset=UTF-8"'
    finally:
        import os

        if os.path.exists("test_api_headers.py"):
            os.remove("test_api_headers.py")
