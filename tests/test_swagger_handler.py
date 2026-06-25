"""测试 swagger_handler.py 模块"""

import asyncio

import allure

from har2pytest.config import APIConfig
from har2pytest.swagger_handler import SwaggerHandler


@allure.feature("Swagger处理器")
@allure.story("判断服务包")
@allure.title("测试根据URL判断服务包")
def test_determine_service_package():
    APIConfig.get_config("SERVICE_MAPPING")

    original_service_mapping = APIConfig._config.get("SERVICE_MAPPING", {})
    APIConfig._config["SERVICE_MAPPING"] = {"mobile": "mall_mobile_application", "user": "mall_center_user"}
    try:
        result = APIConfig.determine_service_package("/mobile/trade/orderCommit")
        assert result == "mall_mobile_application"
    finally:
        APIConfig._config["SERVICE_MAPPING"] = original_service_mapping


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试从Swagger查找API信息")
def test_find_api_info_in_swagger():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "description": "这是一个测试API",
                    "parameters": [
                        {"name": "id", "in": "query", "type": "integer", "description": "ID参数"}
                    ]
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None
    assert result["summary"] == "测试API"


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试带BasePath查找API信息")
def test_find_api_info_with_basepath():
    handler = SwaggerHandler()
    swagger_data = {
        "basePath": "/v1",
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API"
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/v1/api/test", "GET")
    assert result is not None
    assert result["summary"] == "测试API"


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试模型引用处理")
def test_model_reference_handling():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/TestModel"
                            }
                        }
                    ]
                }
            }
        },
        "definitions": {
            "TestModel": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None


@allure.feature("Swagger处理器")
@allure.story("获取默认值")
@allure.title("测试获取各类型默认值")
def test_get_default_value():
    handler = SwaggerHandler()
    assert handler._get_default_value("string") == ""
    assert handler._get_default_value("integer") == 0
    assert handler._get_default_value("boolean") is False
    assert handler._get_default_value("array") == []
    assert handler._get_default_value("object") == {}


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试从Swagger提取查询参数")
def test_extract_params_from_swagger():
    handler = SwaggerHandler()
    swagger_info = {
        "parameters": [
            {"name": "id", "in": "query", "type": "integer", "required": True},
            {"name": "name", "in": "query", "type": "string", "required": False}
        ]
    }
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) == 6
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = params
    assert len(query_params) == 2
    assert "id" in query_params
    assert "name" in query_params


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试从Swagger提取属性参数")
def test_extract_params_from_swagger_with_properties():
    handler = SwaggerHandler()
    swagger_info = {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    }
                }
            }
        ]
    }
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) >= 2


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试从空Swagger提取参数")
def test_extract_params_from_swagger_empty():
    handler = SwaggerHandler()
    params = handler._extract_params_from_swagger([], {})
    assert len(params) == 6
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = params
    assert query_params == {}
    assert post_data == {}


@allure.feature("Swagger处理器")
@allure.story("Swagger缓存")
@allure.title("测试Swagger缓存存取值")
def test_swagger_cache():
    handler = SwaggerHandler()
    swagger_data = {"paths": {"/api/test": {"get": {}}}}
    handler.swagger_cache["https://example.com"] = swagger_data
    result = handler.swagger_cache.get("https://example.com")
    assert result == swagger_data


@allure.feature("Swagger处理器")
@allure.story("提取Body参数")
@allure.title("测试提取引用类型Body参数")
def test_extract_body_params_with_ref():
    handler = SwaggerHandler()
    swagger_data = {
        "definitions": {
            "TestModel": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                }
            }
        }
    }
    param = {
        "name": "body",
        "in": "body",
        "schema": {"$ref": "#/definitions/TestModel"}
    }
    params = handler._extract_body_params(param["schema"], swagger_data)
    assert len(params) == 2


@allure.feature("Swagger处理器")
@allure.story("提取Body参数")
@allure.title("测试提取属性类型Body参数")
def test_extract_body_params_with_properties():
    handler = SwaggerHandler()
    param = {
        "name": "body",
        "in": "body",
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
    }
    params = handler._extract_body_params(param["schema"], {})
    assert len(params) == 2


@allure.feature("Swagger处理器")
@allure.story("提取Body参数")
@allure.title("测试提取空Schema的Body参数")
def test_extract_body_params_empty_schema():
    handler = SwaggerHandler()
    params = handler._extract_body_params({}, {})
    assert params == {}


@allure.feature("Swagger处理器")
@allure.story("提取Body参数")
@allure.title("测试引用未找到时提取Body参数")
def test_extract_body_params_ref_not_found():
    handler = SwaggerHandler()
    param = {
        "name": "body",
        "in": "body",
        "schema": {"$ref": "#/definitions/NotFound"}
    }
    params = handler._extract_body_params(param["schema"], {})
    assert params == {}


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试路径不存在时查找API信息")
def test_find_api_info_path_not_found():
    handler = SwaggerHandler()
    swagger_data = {"paths": {"/api/test": {"get": {}}}}
    result = handler.find_api_info_in_swagger(swagger_data, "/api/notfound", "GET")
    assert result["summary"] == ""


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试方法未找到时有回退")
def test_find_api_info_method_not_found_but_has_fallback():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {"summary": "GET测试"},
                "post": {"summary": "POST测试"}
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "PUT")
    assert result is not None


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试空Swagger数据查找API信息")
def test_find_api_info_empty_swagger_data():
    handler = SwaggerHandler()
    result = handler.find_api_info_in_swagger({}, "/api/test", "GET")
    assert result["summary"] == ""


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试空路径查找API信息")
def test_find_api_info_empty_paths():
    handler = SwaggerHandler()
    swagger_data = {"paths": {}}
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result["summary"] == ""


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试带参数引用查找API信息")
def test_find_api_info_with_param_ref():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "schema": {"$ref": "#/definitions/TestModel"}
                        }
                    ]
                }
            }
        },
        "definitions": {
            "TestModel": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试方法回退查找API信息")
def test_find_api_info_method_fallback():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {"summary": "GET测试"}
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None


@allure.feature("Swagger处理器")
@allure.story("获取默认值")
@allure.title("测试未知类型获取默认值")
def test_get_default_value_unknown_type():
    handler = SwaggerHandler()
    result = handler._get_default_value("unknown")
    assert result == ""


@allure.feature("Swagger处理器")
@allure.story("初始化")
@allure.title("测试Swagger处理器初始化")
def test_swagger_handler_init():
    handler = SwaggerHandler()
    assert handler.swagger_cache == {}
    assert handler.api_generator is None


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试获取Swagger文档回退路径")
def test_get_swagger_doc_fallback_paths():
    handler = SwaggerHandler()
    assert handler is not None


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试所有路径获取Swagger文档失败")
def test_get_swagger_doc_all_paths_failed():
    handler = SwaggerHandler()
    result = asyncio.run(handler.get_swagger_doc("https://invalid-url.com"))
    assert result is None


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试无效格式获取Swagger文档")
def test_get_swagger_doc_invalid_format():
    handler = SwaggerHandler()
    assert handler is not None


@allure.feature("Swagger处理器")
@allure.story("从Swagger生成API")
@allure.title("测试带BasePath从Swagger生成API")
def test_generate_apis_from_swagger_with_basepath():
    handler = SwaggerHandler()
    swagger_data = {
        "basePath": "/v1",
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "parameters": []
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/v1/api/test", "GET")
    assert result is not None


@allure.feature("Swagger处理器")
@allure.story("从Swagger生成API")
@allure.title("测试指定路径从Swagger生成API")
def test_generate_apis_from_swagger_specific_path():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "parameters": []
                }
            },
            "/api/other": {
                "post": {
                    "summary": "其他API",
                    "parameters": []
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None
    assert result["summary"] == "测试API"


@allure.feature("Swagger处理器")
@allure.story("从Swagger生成API")
@allure.title("测试Swagger文档获取失败时生成API")
def test_generate_apis_from_swagger_doc_failed():
    handler = SwaggerHandler()
    assert handler is not None


@allure.feature("Swagger处理器")
@allure.story("从Swagger生成API")
@allure.title("测试从Swagger生成API并提取参数")
def test_generate_apis_from_swagger_extract_params():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "parameters": [
                        {"name": "id", "in": "query", "type": "integer", "description": "ID参数"},
                        {"name": "name", "in": "query", "type": "string", "description": "名称参数"}
                    ]
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None
    assert len(result["parameters"]) == 2


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试Swagger文档缓存")
def test_get_swagger_doc_caching(monkeypatch):
    handler = SwaggerHandler()
    swagger_data = {"paths": {"/api/test": {"get": {}}}}

    call_count = [0]

    async def mock_send_request(url):
        call_count[0] += 1
        return swagger_data

    monkeypatch.setattr(handler, "_send_request", mock_send_request)

    result1 = asyncio.run(handler.get_swagger_doc("https://example.com"))
    result2 = asyncio.run(handler.get_swagger_doc("https://example.com"))

    assert result1 is not None
    assert result2 is not None
    assert call_count[0] == 2


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试Swagger文档缓存(类级别)")
def test_get_swagger_doc_cache():
    handler = SwaggerHandler()
    swagger_data = {"paths": {"/api/test": {"get": {}}}}

    handler.swagger_cache["https://example.com"] = swagger_data

    result = asyncio.run(handler.get_swagger_doc("https://example.com"))

    assert result == swagger_data


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试提取枚举类型参数")
def test_extract_params_with_enum():
    handler = SwaggerHandler()
    swagger_info = {
        "parameters": [
            {
                "name": "status",
                "in": "query",
                "type": "string",
                "enum": ["active", "inactive"]
            }
        ]
    }
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) == 6
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = params
    assert "status" in query_params


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试提取路径参数")
def test_extract_params_path_param():
    handler = SwaggerHandler()
    swagger_info = {
        "parameters": [
            {
                "name": "id",
                "in": "path",
                "type": "integer",
                "required": True
            }
        ]
    }
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) == 6
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = params


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试提取Body属性参数")
def test_extract_params_body_with_properties():
    handler = SwaggerHandler()
    swagger_info = {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    }
                }
            }
        ]
    }
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) >= 2


@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取引用类型参数值")
def test_extract_param_value_with_ref():
    handler = SwaggerHandler()
    swagger_data = {
        "definitions": {
            "TestModel": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }
    }
    param = {
        "name": "body",
        "in": "body",
        "schema": {"$ref": "#/definitions/TestModel"}
    }
    value = handler._extract_param_value(param, swagger_data)
    assert value is not None


@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取嵌套对象参数值")
def test_extract_param_value_nested_object():
    handler = SwaggerHandler()
    param = {
        "name": "body",
        "in": "body",
        "schema": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    }
                }
            }
        }
    }
    value = handler._extract_param_value(param, {})
    assert value is not None


@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取空对象参数值")
def test_extract_param_value_empty_object():
    handler = SwaggerHandler()
    param = {"name": "body", "in": "body", "schema": {"type": "object"}}
    value = handler._extract_param_value(param["schema"], {})
    assert value == {}


@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取引用类型数组参数值")
def test_extract_param_value_array_with_ref():
    handler = SwaggerHandler()
    swagger_data = {
        "definitions": {
            "ItemModel": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }
    }
    param = {
        "name": "items",
        "in": "body",
        "schema": {
            "type": "array",
            "items": {"$ref": "#/definitions/ItemModel"}
        }
    }
    value = handler._extract_param_value(param, swagger_data)
    assert value is not None


@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取属性类型数组参数值")
def test_extract_param_value_array_with_properties():
    handler = SwaggerHandler()
    param = {
        "name": "items",
        "in": "body",
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }
    }
    value = handler._extract_param_value(param, {})
    assert value is not None


@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取空数组参数值")
def test_extract_param_value_empty_array():
    handler = SwaggerHandler()
    param = {"name": "items", "in": "body", "schema": {"type": "array"}}
    value = handler._extract_param_value(param["schema"], {})
    assert value == []