# coding:utf-8
"""
测试 api_generator.py 模块
"""

import pytest
import allure
import os
from har2pytest.api_generator import APIGenerator


@allure.feature("API生成器")
@allure.story("提取函数名")
def test_extract_function_name():
    """测试从URL提取函数名"""
    # 测试普通URL
    assert APIGenerator.extract_function_name("/mobile/trade/orderCommit") == "_mobile_trade_orderCommit"
    
    # 测试带路径参数的URL
    assert APIGenerator.extract_function_name("/user/123/info") == "_user_123_info"
    
    # 测试根路径
    assert APIGenerator.extract_function_name("/") == "_"


@allure.feature("API生成器")
@allure.story("确定服务包")
def test_determine_service_package():
    """测试确定服务包"""
    # 测试普通URL
    assert APIGenerator.determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"
    
    # 测试带路径参数的URL
    assert APIGenerator.determine_service_package("/user/123/info") == "mall_center_user"
    
    # 测试空URL
    assert APIGenerator.determine_service_package("") == "custom_api"


@allure.feature("API生成器")
@allure.story("检查API是否存在")
def test_check_api_exists():
    """测试检查API是否存在"""
    generator = APIGenerator(output_dir="test_api")
    
    # 测试不存在的API
    assert not generator.check_api_exists("/mobile/trade/orderCommit", "custom_api")
    
    # 清理
    import shutil
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("格式化参数")
def test_format_params_for_api_file():
    """测试格式化参数"""
    generator = APIGenerator()
    
    # 测试空参数
    assert generator.format_params_for_api_file({}) == "{}"
    
    # 测试简单参数
    params = {"keyword": "TS001", "pageNum": 1}
    result = generator.format_params_for_api_file(params)
    assert "keyword" in result
    assert "TS001" in result
    assert "pageNum" in result
    assert "1" in result


@allure.feature("API生成器")
@allure.story("生成API文件内容")
def test_generate_file_content():
    """测试生成API文件内容"""
    generator = APIGenerator()
    
    request_info = {
        "method": "POST",
        "url": "/user/login",
        "query_params": {},
        "post_data": {"username": "test", "password": "123456"},
        "headers": {"content-type": "application/json"}
    }
    
    content = generator.generate_file_content(request_info, "_user_login")
    assert "# coding:utf-8" in content
    assert "from setting import TIMEOUT, VERIFY, access_token" in content
    assert "from util.client import client" in content
    assert "def _user_login" in content
    assert "url = \"/user/login\"" in content
    assert "data = {" in content
    assert "username" in content
    assert "test" in content
    assert "password" in content
    assert "123456" in content


@allure.feature("API生成器")
@allure.story("生成API文件")
def test_generate_api_file():
    """测试生成API文件"""
    generator = APIGenerator(output_dir="test_api")
    
    request_info = {
        "method": "POST",
        "url": "/user/login",
        "query_params": {},
        "post_data": {"username": "test", "password": "123456"},
        "headers": {"content-type": "application/json"}
    }
    
    filepath = generator.generate_api_file(request_info)
    assert filepath is not None
    assert os.path.exists(filepath)
    
    # 测试文件已存在的情况
    filepath2 = generator.generate_api_file(request_info)
    assert filepath2 is None
    
    # 清理
    import shutil
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")
