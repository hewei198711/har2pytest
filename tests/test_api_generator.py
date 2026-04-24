# coding:utf-8
"""
测试 api_generator.py 模块
"""

import shutil
import pytest
import allure
import os
from har2pytest.api_generator import APIGenerator
from har2pytest.config import APIConfig


@allure.feature("API生成器")
@allure.story("提取函数名")
def test_extract_function_name():
    """测试从URL提取函数名"""
    # 测试普通URL
    assert APIGenerator.extract_function_name("/mobile/trade/orderCommit") == "_mobile_trade_orderCommit"
    
    # 测试带路径参数的URL
    # 临时设置 PATH_URLS 配置
    original_path_urls = APIConfig._config.get('PATH_URLS', [])
    APIConfig._config['PATH_URLS'] = ["/user/{id}/info"]
    
    try:
        # 由于 PATH_URLS 中有匹配的模板 "/user/{id}/info"，所以使用模板中的参数名
        assert APIGenerator.extract_function_name("/user/123/info") == "_user_id_info"
    finally:
        # 恢复原始配置
        APIConfig._config['PATH_URLS'] = original_path_urls
    
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
    assert APIGenerator.determine_service_package("") == "apis"


@allure.feature("API生成器")
@allure.story("检查API是否存在")
def test_check_api_exists():
    """测试检查API是否存在"""
    generator = APIGenerator(output_dir="test_api")
    
    # 测试不存在的API
    assert not generator.check_api_exists("/mobile/trade/orderCommit", "apis")
    
    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("生成参数字符串")
def test_generate_params_string():
    """测试生成参数字符串"""
    generator = APIGenerator()
    
    # 测试空参数
    assert generator._generate_params_string({}) == "{}"
    
    # 测试简单参数
    params = {"keyword": "TS001", "pageNum": 1}
    result = generator._generate_params_string(params)
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
    assert "from util.client import client" in content
    assert "def _user_login" in content
    assert "url = \"/user/login\"" in content
    assert "data = {" in content
    assert "username" in content
    assert "test" in content
    assert "password" in content
    assert "123456" in content
    assert "headers = {" in content


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


@allure.feature("API生成器")
@allure.story("生成包含Swagger信息的API文件")
def test_generate_api_with_swagger_info():
    """测试生成包含Swagger文档信息的API文件"""
    generator = APIGenerator(output_dir="test_api")
    
    # 模拟请求信息
    request_info = {
        "method": "POST",
        "url": "/user/login",
        "query_params": {},
        "post_data": {"username": "test", "password": "123456"},
        "headers": {"content-type": "application/json"}
    }
    
    # 生成API文件
    filepath = generator.generate_api_file(request_info)
    assert filepath is not None
    assert os.path.exists(filepath)
    
    # 清理
    import shutil
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("从Swagger获取参数说明")
def test_parameter_description_from_swagger():
    """测试从Swagger文档获取参数说明"""
    generator = APIGenerator()
    
    # 模拟Swagger信息
    swagger_info = {
        "description": "用户登录接口",
        "parameters": {
            "username": "用户名",
            "password": "密码"
        },
        "summary": "用户登录"
    }
    
    # 模拟请求信息
    request_info = {
        "method": "POST",
        "url": "/user/login",
        "query_params": {},
        "post_data": {"username": "test", "password": "123456"},
        "headers": {"content-type": "application/json"}
    }
    
    # 生成文件内容
    content = generator.generate_file_content(request_info, "_user_login", swagger_info)
    assert "用户登录" in content
    assert "用户名" in content
    assert "密码" in content


@allure.feature("API生成器")
@allure.story("Swagger文档缓存")
def test_swagger_cache_usage():
    """测试Swagger文档缓存机制"""
    generator1 = APIGenerator()
    generator2 = APIGenerator()

    # 验证两个实例都有swagger_updater属性
    assert hasattr(generator1, 'swagger_updater')
    assert hasattr(generator2, 'swagger_updater')


@allure.feature("API生成器")
@allure.story("路径URL处理-配置有模板")
def test_path_url_with_config_template():
    """测试路径URL处理-配置有模板的情况"""
    generator = APIGenerator(output_dir="test_api")

    # 临时设置 PATH_URLS 配置
    original_path_urls = APIConfig._config.get('PATH_URLS', [])
    APIConfig._config['PATH_URLS'] = ["/user/{userId}/info", "/order/{orderId}/detail"]

    try:
        # 测试带路径参数的URL（有配置模板）
        request_info = {
            "method": "GET",
            "url": "/user/123/info",
            "query_params": {},
            "post_data": {},
            "headers": {"content-type": "application/json"}
        }

        content = generator.generate_file_content(request_info, "_user_userId_info")
        assert "def _user_userId_info" in content
        assert "/user/{userId}/info" in content
        assert 'userId' in content
        assert "params['userId']" in content
    finally:
        # 恢复原始配置
        APIConfig._config['PATH_URLS'] = original_path_urls

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("路径URL处理-配置无模板")
def test_path_url_without_config_template():
    """测试路径URL处理-配置无模板的情况（自动识别数字参数）"""
    generator = APIGenerator(output_dir="test_api")

    # 确保 PATH_URLS 配置不包含匹配的模板
    original_path_urls = APIConfig._config.get('PATH_URLS', [])
    APIConfig._config['PATH_URLS'] = ["/other/path"]

    try:
        # 测试带路径参数的URL（无配置模板，自动识别数字参数）
        request_info = {
            "method": "GET",
            "url": "/appStore/store/dis/mortgageOrder/detail/96453",
            "query_params": {},
            "post_data": {},
            "headers": {"content-type": "application/json"}
        }

        content = generator.generate_file_content(request_info, "_appStore_store_dis_mortgageOrder_detail_id")
        assert "def _appStore_store_dis_mortgageOrder_detail_id" in content
        assert "/appStore/store/dis/mortgageOrder/detail/{id}" in content
        assert "params['id']" in content
    finally:
        # 恢复原始配置
        APIConfig._config['PATH_URLS'] = original_path_urls

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("文件上传API生成")
def test_generate_api_file_upload():
    """测试生成文件上传API"""
    generator = APIGenerator(output_dir="test_api")

    # 测试文件上传场景
    request_info = {
        "method": "POST",
        "url": "/file/upload",
        "query_params": {},
        "post_data": {"file": "test.txt", "name": "test"},
        "headers": {"content-type": "multipart/form-data"}
    }

    content = generator.generate_file_content(request_info, "_file_upload")
    assert "import os" in content
    assert "from requests_toolbelt import MultipartEncoder" in content
    assert "def _file_upload" in content
    assert "MultipartEncoder" in content
    assert 'filename = os.path.basename(files["file"])' in content

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("URL编码API生成")
def test_generate_api_urlencode():
    """测试生成URL编码API"""
    generator = APIGenerator(output_dir="test_api")

    # 测试需要urlencode的场景
    request_info = {
        "method": "POST",
        "url": "/user/login",
        "query_params": {"username": "test", "password": "123456"},
        "post_data": {},
        "headers": {"content-length": "0"}
    }

    content = generator.generate_file_content(request_info, "_user_login")
    assert "from urllib.parse import urlencode" in content
    assert "def _user_login" in content
    assert "urlencode(data)" in content
    assert "application/x-www-form-urlencoded" in content

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("GET请求API生成")
def test_generate_api_get():
    """测试生成GET请求API"""
    generator = APIGenerator(output_dir="test_api")

    # 测试GET请求（带查询参数）
    request_info = {
        "method": "GET",
        "url": "/user/list",
        "query_params": {"pageNum": 1, "pageSize": 10},
        "post_data": {},
        "headers": {"content-type": "application/json"}
    }

    content = generator.generate_file_content(request_info, "_user_list")
    assert "def _user_list" in content
    assert 'client.get(url=url, params=params, headers=headers)' in content
    assert "pageNum" in content
    assert "pageSize" in content

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("POST请求API生成-JSON")
def test_generate_api_post_json():
    """测试生成POST请求API（JSON格式）"""
    generator = APIGenerator(output_dir="test_api")

    # 测试POST请求（JSON格式）
    request_info = {
        "method": "POST",
        "url": "/user/create",
        "query_params": {},
        "post_data": {"username": "test", "email": "test@example.com"},
        "headers": {"content-type": "application/json"}
    }

    content = generator.generate_file_content(request_info, "_user_create")
    assert "def _user_create" in content
    assert 'client.post(url=url, json=data, headers=headers)' in content
    assert "username" in content
    assert "test" in content
    assert "email" in content
    assert "test@example.com" in content

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("带Swagger信息的API生成")
def test_generate_api_with_swagger_info_complete():
    """测试带Swagger信息的完整API生成"""
    generator = APIGenerator(output_dir="test_api")

    # 模拟完整的Swagger信息
    swagger_info = {
        "description": "用户登录接口",
        "parameters": {
            "username": "用户名",
            "password": "密码"
        },
        "summary": "用户登录"
    }

    request_info = {
        "method": "POST",
        "url": "/user/login",
        "query_params": {},
        "post_data": {"username": "test", "password": "123456"},
        "headers": {"content-type": "application/json"}
    }

    content = generator.generate_file_content(request_info, "_user_login", swagger_info)
    assert "def _user_login" in content
    assert '"""' in content
    assert "用户登录" in content
    assert "用户名" in content
    assert "密码" in content
    assert "# 用户名" in content
    assert "# 密码" in content

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("路径参数自动识别-多个数字参数")
def test_path_url_multiple_numeric_params():
    """测试路径参数自动识别-多个数字参数的情况"""
    generator = APIGenerator(output_dir="test_api")

    # 确保 PATH_URLS 配置不包含匹配的模板
    original_path_urls = APIConfig._config.get('PATH_URLS', [])
    APIConfig._config['PATH_URLS'] = ["/other/path"]

    try:
        # 测试带多个路径参数的URL（无配置模板）
        request_info = {
            "method": "GET",
            "url": "/order/123/item/456",
            "query_params": {},
            "post_data": {},
            "headers": {"content-type": "application/json"}
        }

        content = generator.generate_file_content(request_info, "_order_order_id_item_id")
        assert "def _order_order_id_item_id" in content
        assert "order_id" in content
        assert "id" in content
    finally:
        # 恢复原始配置
        APIConfig._config['PATH_URLS'] = original_path_urls

    # 清理
    if os.path.exists("test_api"):
        shutil.rmtree("test_api")


@allure.feature("API生成器")
@allure.story("从Swagger文档提取参数")
def test_extract_params_from_swagger():
    """测试从Swagger文档提取参数"""
    generator = APIGenerator()

    # 测试只包含查询参数的Swagger参数
    query_params_only = [
        {"name": "pageNum", "in": "query", "type": "integer"},
        {"name": "pageSize", "in": "query", "type": "string"},
        {"name": "keyword", "in": "query", "type": "string"}
    ]
    swagger_data = {"paths": {}}

    query_params, post_data, has_query_param, has_body_param = \
        generator._extract_params_from_swagger(query_params_only, swagger_data)

    assert has_query_param is True
    assert has_body_param is False
    assert len(query_params) == 3
    assert query_params["pageNum"] == 0
    assert query_params["pageSize"] == ""
    assert query_params["keyword"] == ""
    assert post_data == {}

    # 测试只包含body参数的Swagger参数
    body_params_only = [
        {"name": "dto", "in": "body", "schema": {"$ref": "#/definitions/UserDto"}}
    ]
    swagger_data_with_def = {
        "definitions": {
            "UserDto": {
                "properties": {
                    "username": {"type": "string"},
                    "age": {"type": "integer"}
                }
            }
        }
    }

    query_params, post_data, has_query_param, has_body_param = \
        generator._extract_params_from_swagger(body_params_only, swagger_data_with_def)

    assert has_query_param is False
    assert has_body_param is True
    assert query_params == {}
    assert len(post_data) == 2
    assert post_data["username"] == ""
    assert post_data["age"] == 0

    # 测试同时包含查询参数和body参数的Swagger参数
    mixed_params = [
        {"name": "pageNum", "in": "query", "type": "integer"},
        {"name": "dto", "in": "body", "schema": {"$ref": "#/definitions/UserDto"}}
    ]

    query_params, post_data, has_query_param, has_body_param = \
        generator._extract_params_from_swagger(mixed_params, swagger_data_with_def)

    assert has_query_param is True
    assert has_body_param is True
    assert len(query_params) == 1
    assert query_params["pageNum"] == 0
    assert len(post_data) == 2
    assert post_data["username"] == ""
    assert post_data["age"] == 0

    # 测试空参数列表
    query_params, post_data, has_query_param, has_body_param = \
        generator._extract_params_from_swagger([], swagger_data)

    assert has_query_param is False
    assert has_body_param is False
    assert query_params == {}
    assert post_data == {}


@allure.feature("API生成器")
@allure.story("获取参数默认值")
def test_get_default_value():
    """测试根据参数类型获取默认值"""
    generator = APIGenerator()

    # 测试 string 类型
    assert generator._get_default_value("string") == ""

    # 测试 integer 类型
    assert generator._get_default_value("integer") == 0

    # 测试 boolean 类型
    assert generator._get_default_value("boolean") is False

    # 测试未知类型
    assert generator._get_default_value("unknown") == ""

    # 测试 None 类型
    assert generator._get_default_value(None) == ""


@allure.feature("API生成器")
@allure.story("提取body参数")
def test_extract_body_params():
    """测试从body参数schema中提取参数"""
    generator = APIGenerator()

    # 测试带 $ref 的模型引用
    schema_with_ref = {"$ref": "#/definitions/UserDto"}
    swagger_data = {
        "definitions": {
            "UserDto": {
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                    "age": {"type": "integer"},
                    "isActive": {"type": "boolean"}
                }
            }
        }
    }

    body_params = generator._extract_body_params(schema_with_ref, swagger_data)
    assert len(body_params) == 4
    assert body_params["username"] == ""
    assert body_params["password"] == ""
    assert body_params["age"] == 0
    assert body_params["isActive"] is False

    # 测试内联模型
    inline_schema = {
        "properties": {
            "name": {"type": "string"},
            "count": {"type": "integer"}
        }
    }

    body_params = generator._extract_body_params(inline_schema, swagger_data)
    assert len(body_params) == 2
    assert body_params["name"] == ""
    assert body_params["count"] == 0

    # 测试没有 properties 的模型
    empty_schema = {"$ref": "#/definitions/EmptyDto"}
    swagger_data_empty = {
        "definitions": {
            "EmptyDto": {}
        }
    }

    body_params = generator._extract_body_params(empty_schema, swagger_data_empty)
    assert body_params == {}

    # 测试不存在的模型引用
    not_exist_ref = {"$ref": "#/definitions/NotExistDto"}
    body_params = generator._extract_body_params(not_exist_ref, swagger_data)
    assert body_params == {}

    # 测试既没有 $ref 也没有 properties 的 schema
    simple_schema = {"type": "string"}
    body_params = generator._extract_body_params(simple_schema, swagger_data)
    assert body_params == {}
