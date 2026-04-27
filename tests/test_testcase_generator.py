# coding:utf-8
"""
测试 testcase_generator.py 模块
"""

import pytest
import allure
import os
from har2pytest.testcase_generator import TestCaseGenerator


@allure.feature("测试用例生成器")
@allure.story("提取函数名")
def test_extract_function_name_from_file():
    """测试从API文件中提取函数名"""
    # 创建测试API文件
    test_content = '''
# coding:utf-8

def _user_login(data=data, access_token=access_token):
    """
    用户登录
    /user/login
    """
    url = "/user/login"
    headers = {"Authorization": f"bearer {access_token}"}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
'''

    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        generator = TestCaseGenerator()
        function_name = generator.extract_function_name_from_file("test_api.py")
        assert function_name == "_user_login"
    finally:
        if os.path.exists("test_api.py"):
            os.remove("test_api.py")


@allure.feature("测试用例生成器")
@allure.story("提取参数字典")
def test_extract_api_params_dict_from_har():
    """测试从HAR请求信息中提取参数字典"""
    generator = TestCaseGenerator()

    # 测试POST请求带post_data
    request_info = {
        "method": "POST",
        "post_data": {"username": "test", "password": "123456"}
    }
    params = generator.extract_api_params_dict_from_har(request_info)
    assert params == {"username": "test", "password": "123456"}

    # 测试POST请求带query_params
    request_info = {
        "method": "POST",
        "query_params": {"page": 1, "size": 10}
    }
    params = generator.extract_api_params_dict_from_har(request_info)
    assert params == {"page": 1, "size": 10}

    # 测试GET请求带query_params
    request_info = {
        "method": "GET",
        "query_params": {"id": 123}
    }
    params = generator.extract_api_params_dict_from_har(request_info)
    assert params == {"id": 123}

    # 测试无参数的情况
    request_info = {
        "method": "GET"
    }
    params = generator.extract_api_params_dict_from_har(request_info)
    assert params is None


@allure.feature("测试用例生成器")
@allure.story("格式化参数")
def test_format_params_for_test_case():
    """测试格式化参数为测试用例中的参数字符串"""
    generator = TestCaseGenerator()

    # 测试空参数
    assert generator.format_params_for_test_case({}) == "{}"

    # 测试简单参数
    params = {"keyword": "TS001", "pageNum": 1}
    result = generator.format_params_for_test_case(params)
    assert "keyword" in result
    assert "TS001" in result
    assert "pageNum" in result
    assert "1" in result


@allure.feature("测试用例生成器")
@allure.story("处理参数到映射")
def test_process_params_to_map():
    """测试处理参数到映射"""
    generator = TestCaseGenerator()

    # 测试单个参数
    requests_params = [
        {"keyword": "TS001"},
        {"keyword": "TS002"},
        {"keyword": "TS001"}  # 重复值
    ]
    result = generator.process_params_to_map(requests_params)
    assert len(result) == 1
    assert "keyword" in result[0]
    assert len(result[0]["keyword"]) == 2  # 去重后应该有2个值
    assert "TS001" in result[0]["keyword"]
    assert "TS002" in result[0]["keyword"]

    # 测试组合参数
    requests_params = [
        {"startDate": "2026-01-01", "endDate": "2026-01-31"},
        {"startDate": "2026-02-01", "endDate": "2026-02-28"}
    ]
    result = generator.process_params_to_map(requests_params)
    assert len(result) == 1
    # 检查是否包含 startDate 和 endDate 的组合键（顺序可能不同）
    assert any("startDate" in key and "endDate" in key for key in result[0])
    # 检查组合键的值长度
    for key in result[0]:
        if "startDate" in key and "endDate" in key:
            assert len(result[0][key]) == 2


@allure.feature("测试用例生成器")
@allure.story("从URL提取服务包名")
def test_extract_service_package_from_url():
    """测试从URL中提取服务包名"""
    from har2pytest.config import APIConfig

    # 触发配置初始化
    APIConfig.get_config('SERVICE_MAPPING')

    # 临时设置 SERVICE_MAPPING 配置
    original_service_mapping = APIConfig._config.get('SERVICE_MAPPING', {})
    APIConfig._config['SERVICE_MAPPING'] = {
        "mobile": "mall_mobile_application",
        "user": "mall_center_user"
    }

    try:
        generator = TestCaseGenerator()
        assert generator.extract_service_package_from_url("/mobile/trade/orderCommit") == "mall_mobile_application"
        assert generator.extract_service_package_from_url("/user/123/info") == "mall_center_user"
        assert generator.extract_service_package_from_url("") == "apis"
    finally:
        # 恢复原始配置
        APIConfig._config['SERVICE_MAPPING'] = original_service_mapping


@allure.feature("测试用例生成器")
@allure.story("提取参数备注")
def test_extract_param_remarks_from_api_file():
    """测试从API文件中提取参数备注"""
    # 创建测试API文件
    test_content = """
# coding:utf-8

data = {
    "username": "test", # 用户名
    "password": "123456" # 密码
}

def _user_login(data=data, access_token=access_token):
    \"\"\"
    用户登录
    /user/login
    \"\"\"
    url = "/user/login"
    headers = {"Authorization": f"bearer {access_token}"}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
"""

    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        generator = TestCaseGenerator()
        remarks = generator.extract_param_remarks_from_api_file("test_api.py")
        assert remarks.get("username") == "用户名"
        assert remarks.get("password") == "密码"
    finally:
        if os.path.exists("test_api.py"):
            os.remove("test_api.py")