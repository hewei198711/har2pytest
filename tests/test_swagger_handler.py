"""
测试 swagger_updater.py 模块
"""

import allure

from har2pytest.config import APIConfig
from har2pytest.swagger_handler import SwaggerHandler


@allure.feature("Swagger文档更新器")
@allure.story("确定服务包")
def test_determine_service_package():
    """测试根据URL判断服务包"""
    # 触发配置初始化
    APIConfig.get_config("SERVICE_MAPPING")

    # 临时设置 SERVICE_MAPPING 配置
    original_service_mapping = APIConfig._config.get("SERVICE_MAPPING", {})
    APIConfig._config["SERVICE_MAPPING"] = {"mobile": "mall_mobile_application", "user": "mall_center_user"}

    try:
        assert APIConfig.determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"
        assert APIConfig.determine_service_package("/user/123/info") == "mall_center_user"
        assert APIConfig.determine_service_package("") == "apis"
    finally:
        # 恢复原始配置
        APIConfig._config["SERVICE_MAPPING"] = original_service_mapping


@allure.feature("Swagger文档更新器")
@allure.story("在Swagger中查找API信息")
def test_find_api_info_in_swagger():
    """测试在Swagger文档中查找API信息"""
    updater = SwaggerHandler()

    # 测试Swagger数据
    swagger_data = {
        "paths": {
            "/user/login": {
                "post": {
                    "summary": "用户登录",
                    "description": "用户登录接口",
                    "parameters": [
                        {"name": "username", "description": "用户名"},
                        {"name": "password", "description": "密码"},
                    ],
                }
            }
        }
    }

    # 测试查找存在的API
    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")
    assert api_info["summary"] == "用户登录"
    assert api_info["description"] == "用户登录接口"
    assert api_info["parameters"]["username"] == "用户名"
    assert api_info["parameters"]["password"] == "密码"

    # 测试查找不存在的API
    api_info = updater.find_api_info_in_swagger(swagger_data, "/nonexistent", "GET")
    assert api_info["summary"] == ""
    assert api_info["description"] == ""
    assert api_info["parameters"] == {}


@allure.feature("Swagger文档更新器")
@allure.story("带basePath的API路径匹配")
def test_find_api_info_with_basepath():
    """测试带basePath的API路径匹配"""
    updater = SwaggerHandler()

    # 测试带basePath的Swagger数据
    swagger_data = {
        "basePath": "/appStore",
        "paths": {
            "/storage/upload": {
                "post": {
                    "summary": "文件上传",
                    "description": "文件上传接口",
                    "parameters": [
                        {"name": "storageType", "description": "存储类型"},
                        {"name": "clientKey", "description": "客户端密钥"},
                    ],
                }
            }
        },
    }

    # 测试带basePath的API路径
    api_info = updater.find_api_info_in_swagger(swagger_data, "/appStore/storage/upload", "POST")
    assert api_info["summary"] == "文件上传"
    assert api_info["description"] == "文件上传接口"
    assert api_info["parameters"]["storageType"] == "存储类型"
    assert api_info["parameters"]["clientKey"] == "客户端密钥"


@allure.feature("Swagger文档更新器")
@allure.story("模型引用处理")
def test_model_reference_handling():
    """测试模型引用处理"""
    updater = SwaggerHandler()

    # 测试带模型引用的Swagger数据
    swagger_data = {
        "paths": {
            "/user/login": {
                "post": {
                    "summary": "用户登录",
                    "description": "用户登录接口",
                    "parameters": [{"name": "dto", "in": "body", "schema": {"$ref": "#/definitions/LoginRequest"}}],
                }
            }
        },
        "definitions": {
            "LoginRequest": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "用户名"},
                    "password": {"type": "string", "description": "密码"},
                },
            }
        },
    }

    # 测试模型引用处理
    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")
    assert api_info["summary"] == "用户登录"
    assert api_info["description"] == "用户登录接口"
    assert api_info["parameters"]["username"] == "用户名"
    assert api_info["parameters"]["password"] == "密码"


@allure.feature("Swagger文档更新器")
@allure.story("获取默认值")
def test_get_default_value():
    """测试获取参数默认值"""
    handler = SwaggerHandler()

    # 测试不同类型的默认值
    assert handler._get_default_value("string") == ""
    assert handler._get_default_value("int") == 0
    assert handler._get_default_value("integer") == 0
    assert handler._get_default_value("number") == 0.0
    assert handler._get_default_value("float") == 0.0
    assert handler._get_default_value("boolean") is False
    assert handler._get_default_value("array") == []
    assert handler._get_default_value("object") == {}
    # 未知类型返回空字符串
    assert handler._get_default_value("unknown") == ""


@allure.feature("Swagger文档更新器")
@allure.story("从Swagger提取参数")
def test_extract_params_from_swagger():
    """测试从Swagger文档提取参数"""
    handler = SwaggerHandler()

    swagger_data = {
        "definitions": {
            "UserRequest": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "用户名"},
                    "password": {"type": "string", "description": "密码"},
                },
            }
        }
    }

    parameters = [
        {"name": "query_param", "in": "query", "type": "string", "description": "查询参数"},
        {"name": "path_param", "in": "path", "type": "integer", "description": "路径参数"},
        {"name": "body_param", "in": "body", "schema": {"$ref": "#/definitions/UserRequest"}},
    ]

    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
        handler._extract_params_from_swagger(parameters, swagger_data)
    )

    assert query_params == {"query_param": ""}
    assert path_params == {"path_param": 0}
    assert has_query_param is True
    assert has_body_param is True
    assert param_descriptions["query_param"] == "查询参数"
    assert param_descriptions["path_param"] == "路径参数"
    assert param_descriptions["username"] == "用户名"
    assert param_descriptions["password"] == "密码"


@allure.feature("Swagger文档更新器")
@allure.story("从Swagger提取参数-直接properties")
def test_extract_params_from_swagger_with_properties():
    """测试从Swagger文档提取参数（直接properties）"""
    handler = SwaggerHandler()

    swagger_data = {}

    parameters = [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "名称"},
                    "age": {"type": "integer", "description": "年龄"},
                },
            },
        }
    ]

    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
        handler._extract_params_from_swagger(parameters, swagger_data)
    )

    assert has_body_param is True
    assert param_descriptions["name"] == "名称"
    assert param_descriptions["age"] == "年龄"


@allure.feature("Swagger文档更新器")
@allure.story("从Swagger提取参数-无参数")
def test_extract_params_from_swagger_empty():
    """测试从Swagger文档提取空参数"""
    handler = SwaggerHandler()

    swagger_data = {}
    parameters = []

    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
        handler._extract_params_from_swagger(parameters, swagger_data)
    )

    assert query_params == {}
    assert post_data == {}
    assert path_params == {}
    assert has_query_param is False
    assert has_body_param is False
    assert param_descriptions == {}


@allure.feature("Swagger文档更新器")
@allure.story("Swagger缓存")
def test_swagger_cache():
    """测试Swagger文档缓存机制"""
    handler = SwaggerHandler()

    # 测试缓存存储
    test_data = {"paths": {"/test": {"get": {"summary": "test"}}}}
    handler.swagger_cache["http://test.com"] = test_data

    # 测试缓存读取
    cached_data = handler.swagger_cache.get("http://test.com")
    assert cached_data == test_data
    assert cached_data is not None
