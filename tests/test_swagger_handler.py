"""
测试 swagger_updater.py 模块
"""

import allurefrom har2pytest.config import APIConfigfrom har2pytest.swagger_handler import SwaggerHandler@allure.feature("Swagger文档更新器")
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

    test_data = {"paths": {"/test": {"get": {"summary": "test"}}}}
    handler.swagger_cache["http://test.com"] = test_data

    cached_data = handler.swagger_cache.get("http://test.com")
    assert cached_data == test_data
    assert cached_data is not None


@allure.feature("Swagger文档更新器")
@allure.story("提取Body参数-模型引用")
def test_extract_body_params_with_ref():
    """测试从Swagger文档提取Body参数（带模型引用）"""
    handler = SwaggerHandler()

    swagger_data = {
        "definitions": {
            "LoginRequest": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "用户名"},
                    "password": {"type": "string", "description": "密码"},
                },
            }
        }
    }

    schema = {"$ref": "#/definitions/LoginRequest"}
    body_params = handler._extract_body_params(schema, swagger_data)

    assert body_params == {"username": "", "password": ""}


@allure.feature("Swagger文档更新器")
@allure.story("提取Body参数-直接属性")
def test_extract_body_params_with_properties():
    """测试从Swagger文档提取Body参数（直接properties）"""
    handler = SwaggerHandler()

    swagger_data = {}

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
        },
    }
    body_params = handler._extract_body_params(schema, swagger_data)

    assert body_params == {"name": "", "age": 0}


@allure.feature("Swagger文档更新器")
@allure.story("提取Body参数-空schema")
def test_extract_body_params_empty_schema():
    """测试从Swagger文档提取Body参数（空schema）"""
    handler = SwaggerHandler()

    swagger_data = {}
    schema = {}
    body_params = handler._extract_body_params(schema, swagger_data)

    assert body_params == {}


@allure.feature("Swagger文档更新器")
@allure.story("提取Body参数-引用不存在")
def test_extract_body_params_ref_not_found():
    """测试从Swagger文档提取Body参数（引用不存在）"""
    handler = SwaggerHandler()

    swagger_data = {"definitions": {}}

    schema = {"$ref": "#/definitions/NonExistent"}
    body_params = handler._extract_body_params(schema, swagger_data)

    assert body_params == {}


@allure.feature("Swagger文档更新器")
@allure.story("查找API信息-路径不存在")
def test_find_api_info_path_not_found():
    """测试在Swagger文档中查找不存在的路径"""
    updater = SwaggerHandler()

    swagger_data = {"paths": {"/user/login": {"post": {"summary": "登录"}}}}

    api_info = updater.find_api_info_in_swagger(swagger_data, "/nonexistent/path", "GET")

    assert api_info["summary"] == ""
    assert api_info["description"] == ""
    assert api_info["parameters"] == {}


@allure.feature("Swagger文档更新器")
@allure.story("查找API信息-方法不存在但有降级")
def test_find_api_info_method_not_found_but_has_fallback():
    """测试在Swagger文档中查找存在路径但不存在方法，但有降级方法"""
    updater = SwaggerHandler()

    swagger_data = {
        "paths": {
            "/user/login": {
                "post": {"summary": "登录", "description": "用户登录"},
            }
        }
    }

    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "get")

    assert api_info["summary"] == "登录"
    assert api_info["description"] == "用户登录"


@allure.feature("Swagger文档更新器")
@allure.story("查找API信息-空Swagger数据")
def test_find_api_info_empty_swagger_data():
    """测试在空Swagger数据中查找API"""
    updater = SwaggerHandler()

    api_info = updater.find_api_info_in_swagger({}, "/user/login", "POST")
    assert api_info["summary"] == ""
    assert api_info["description"] == ""
    assert api_info["parameters"] == {}


@allure.feature("Swagger文档更新器")
@allure.story("查找API信息-空paths")
def test_find_api_info_empty_paths():
    """测试在空paths中查找API"""
    updater = SwaggerHandler()

    swagger_data = {"paths": {}}
    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")

    assert api_info["summary"] == ""
    assert api_info["description"] == ""
    assert api_info["parameters"] == {}


@allure.feature("Swagger文档更新器")
@allure.story("查找API信息-带$ref参数")
def test_find_api_info_with_param_ref():
    """测试在Swagger文档中查找带$ref引用的API参数"""
    updater = SwaggerHandler()

    swagger_data = {
        "paths": {
            "/user/create": {
                "post": {
                    "summary": "创建用户",
                    "description": "创建新用户",
                    "parameters": [
                        {
                            "name": "user",
                            "in": "body",
                            "schema": {"$ref": "#/definitions/User"},
                        }
                    ],
                }
            }
        },
        "definitions": {
            "User": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "用户名称"},
                    "email": {"type": "string", "description": "用户邮箱"},
                },
            }
        },
    }

    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/create", "POST")

    assert api_info["summary"] == "创建用户"
    assert api_info["description"] == "创建新用户"
    assert api_info["parameters"]["name"] == "用户名称"
    assert api_info["parameters"]["email"] == "用户邮箱"


@allure.feature("Swagger文档更新器")
@allure.story("查找API信息-多种HTTP方法降级")
def test_find_api_info_method_fallback():
    """测试在Swagger文档中查找API时HTTP方法的降级处理"""
    updater = SwaggerHandler()

    swagger_data = {
        "paths": {
            "/user/login": {
                "put": {
                    "summary": "更新登录信息",
                    "description": "更新登录信息",
                    "parameters": [],
                }
            }
        }
    }

    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "post")

    assert api_info["summary"] == "更新登录信息"
    assert api_info["description"] == "更新登录信息"


@allure.feature("Swagger文档更新器")
@allure.story("获取默认值-未知类型")
def test_get_default_value_unknown_type():
    """测试获取未知参数类型的默认值"""
    handler = SwaggerHandler()

    assert handler._get_default_value("unknown_type") == ""
    assert handler._get_default_value("date") == ""
    assert handler._get_default_value("file") == ""


@allure.feature("Swagger文档更新器")
@allure.story("SwaggerHandler初始化")
def test_swagger_handler_init():
    """测试SwaggerHandler初始化"""
    handler = SwaggerHandler()

    assert handler.swagger_cache == {}
    assert handler.api_generator is None


@allure.feature("Swagger文档更新器")
@allure.story("Swagger文档获取-回退路径")
def test_get_swagger_doc_fallback_paths(monkeypatch):
    """测试当swagger-resources失败时，回退到常见路径"""
    handler = SwaggerHandler()

    call_count = [0]

    def mock_send_request(url):
        call_count[0] += 1
        if call_count[0] == 1:
            raise Exception("swagger-resources failed")
        elif call_count[0] == 2:
            return None
        else:
            return {"paths": {"/api/test": {"get": {}}}}

    monkeypatch.setattr(handler, "_send_request", mock_send_request)

    result = handler.get_swagger_doc("https://example.com")

    assert result is not None
    assert "paths" in result
    assert "/api/test" in result["paths"]


@allure.feature("Swagger文档更新器")
@allure.story("Swagger文档获取-所有路径都失败")
def test_get_swagger_doc_all_paths_failed(monkeypatch):
    """测试当所有路径都失败时返回None"""
    handler = SwaggerHandler()

    def mock_send_request(url):
        raise Exception("all paths failed")

    monkeypatch.setattr(handler, "_send_request", mock_send_request)

    result = handler.get_swagger_doc("https://example.com")

    assert result is None


@allure.feature("Swagger文档更新器")
@allure.story("Swagger文档获取-格式不正确")
def test_get_swagger_doc_invalid_format(monkeypatch):
    """测试返回的文档格式不正确（缺少paths字段）"""
    handler = SwaggerHandler()

    call_count = [0]

    def mock_send_request(url):
        call_count[0] += 1
        if call_count[0] == 1:
            raise Exception("swagger-resources failed")
        elif call_count[0] == 2:
            return {"info": {"title": "Test"}}
        else:
            return {"paths": {"/api/test": {"get": {}}}}

    monkeypatch.setattr(handler, "_send_request", mock_send_request)

    result = handler.get_swagger_doc("https://example.com")

    assert result is not None
    assert "paths" in result


@allure.feature("Swagger文档更新器")
@allure.story("从Swagger生成API文件")
def test_generate_apis_from_swagger_with_basepath(tmp_path, monkeypatch):
    """测试从Swagger文档生成API文件（带basePath）"""
    swagger_data = {
        "swagger": "2.0",
        "basePath": "/api/v1",
        "paths": {
            "/users": {
                "get": {
                    "summary": "获取用户列表",
                    "parameters": [
                        {"name": "page", "in": "query", "type": "integer"},
                    ],
                }
            }
        },
    }

    handler = SwaggerHandler()

    monkeypatch.setattr(handler, "get_swagger_doc", lambda url: swagger_data)

    api_generator_mock = type(
        "MockApiGenerator", (), {"generate_api_file": lambda self, req, force, info: str(tmp_path / "api_users.py")}
    )()
    handler.api_generator = api_generator_mock

    result = handler.generate_apis_from_swagger("https://example.com")

    assert len(result) == 1
    assert "api_users.py" in result[0]


@allure.feature("Swagger文档更新器")
@allure.story("从Swagger生成API文件-指定特定路径")
def test_generate_apis_from_swagger_specific_path(tmp_path, monkeypatch):
    """测试从Swagger文档生成指定路径的API文件"""
    swagger_data = {
        "swagger": "2.0",
        "paths": {"/users": {"get": {"summary": "用户列表"}}, "/products": {"get": {"summary": "产品列表"}}},
    }

    handler = SwaggerHandler()

    monkeypatch.setattr(handler, "get_swagger_doc", lambda url: swagger_data)

    api_generator_mock = type(
        "MockApiGenerator", (), {"generate_api_file": lambda self, req, force, info: str(tmp_path / "api_users.py")}
    )()
    handler.api_generator = api_generator_mock

    result = handler.generate_apis_from_swagger("https://example.com", specific_path="/users")

    assert len(result) == 1
    assert "api_users.py" in result[0]


@allure.feature("Swagger文档更新器")
@allure.story("从Swagger生成API文件-获取文档失败")
def test_generate_apis_from_swagger_doc_failed(monkeypatch):
    """测试当无法获取Swagger文档时返回空列表"""
    handler = SwaggerHandler()

    monkeypatch.setattr(handler, "get_swagger_doc", lambda url: None)

    result = handler.generate_apis_from_swagger("https://example.com")

    assert result == []


@allure.feature("Swagger文档更新器")
@allure.story("从Swagger生成API文件-参数提取")
def test_generate_apis_from_swagger_extract_params(tmp_path, monkeypatch):
    """测试从Swagger文档提取参数并生成API文件"""
    swagger_data = {
        "swagger": "2.0",
        "paths": {
            "/users/{userId}": {
                "get": {
                    "summary": "获取用户详情",
                    "parameters": [
                        {"name": "userId", "in": "path", "type": "integer", "description": "用户ID"},
                        {"name": "includeDetails", "in": "query", "type": "boolean"},
                    ],
                }
            }
        },
    }

    handler = SwaggerHandler()

    monkeypatch.setattr(handler, "get_swagger_doc", lambda url: swagger_data)

    captured_request_info = []

    class MockApiGenerator:
        def generate_api_file(self, request_info, force_overwrite, swagger_info):
            captured_request_info.append(request_info)
            return str(tmp_path / "api_users_userId.py")

    handler.api_generator = MockApiGenerator()

    result = handler.generate_apis_from_swagger("https://example.com")

    assert len(result) == 1
    assert len(captured_request_info) == 1

    request_info = captured_request_info[0]

    assert request_info["path_params"] == {"userId": 0}
    assert request_info["query_params"] == {"includeDetails": False}


@allure.feature("Swagger文档更新器")
@allure.story("Swagger数据获取-缓存机制")
def test_get_swagger_doc_caching(monkeypatch):
    """测试Swagger文档获取的缓存机制"""
    handler = SwaggerHandler()

    swagger_data = {"paths": {"/api/test": {"get": {}}}}

    call_count = [0]

    def mock_send_request(url):
        call_count[0] += 1
        # 第一次调用swagger-resources返回空，然后成功获取/v3/api-docs
        if call_count[0] == 1:
            return None  # swagger-resources返回空
        elif call_count[0] == 2:
            return swagger_data  # /v3/api-docs成功
        return None

    monkeypatch.setattr(handler, "_send_request", mock_send_request)

    # 第一次调用 - 应该调用_send_request两次（swagger-resources失败，然后/v3/api-docs成功）
    result1 = handler.get_swagger_doc("https://example.com")

    # 第二次调用相同URL - 应该使用缓存，不调用_send_request
    result2 = handler.get_swagger_doc("https://example.com")

    # 验证第二次调用使用了缓存
    assert call_count[0] == 2  # 第一次调用的两次请求
    assert result1 == swagger_data
    assert result2 == swagger_data


@allure.feature("Swagger文档更新器")
@allure.story("获取Swagger文档-缓存测试")
def test_get_swagger_doc_cache():
    """测试Swagger文档缓存机制"""
    handler = SwaggerHandler()

    test_doc = {"paths": {"/test": {"get": {"summary": "test"}}}}
    handler.swagger_cache["http://cached.com"] = test_doc

    cached_doc = handler.get_swagger_doc("http://cached.com")

    assert cached_doc == test_doc


@allure.feature("Swagger文档更新器")
@allure.story("提取参数-带枚举值")
def test_extract_params_with_enum():
    """测试从Swagger文档提取带枚举值的参数"""
    handler = SwaggerHandler()

    swagger_data = {}
    parameters = [
        {
            "name": "status",
            "in": "query",
            "type": "string",
            "description": "状态",
            "enum": ["active", "inactive"],
        }
    ]

    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
        handler._extract_params_from_swagger(parameters, swagger_data)
    )

    assert query_params == {"status": ""}
    assert has_query_param is True
    assert param_descriptions["status"] == "状态"


@allure.feature("Swagger文档更新器")
@allure.story("提取参数-路径参数处理")
def test_extract_params_path_param():
    """测试从Swagger文档提取路径参数"""
    handler = SwaggerHandler()

    swagger_data = {}
    parameters = [
        {
            "name": "userId",
            "in": "path",
            "type": "integer",
            "description": "用户ID",
            "required": True,
        }
    ]

    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
        handler._extract_params_from_swagger(parameters, swagger_data)
    )

    assert path_params == {"userId": 0}
    assert param_descriptions["userId"] == "用户ID"


@allure.feature("Swagger文档更新器")
@allure.story("提取参数-body参数直接properties")
def test_extract_params_body_with_properties():
    """测试从Swagger文档提取body参数（直接properties）"""
    handler = SwaggerHandler()

    swagger_data = {}
    parameters = [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "ID"},
                    "name": {"type": "string", "description": "名称"},
                },
            },
        }
    ]

    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
        handler._extract_params_from_swagger(parameters, swagger_data)
    )

    assert post_data == {"id": 0, "name": ""}
    assert has_body_param is True
    assert param_descriptions["id"] == "ID"
    assert param_descriptions["name"] == "名称"

@allure.feature("Swagger�ech�f�ehV")
@allure.story("�c�S�Spe<P-$ref_(u�[IN")
def test_extract_param_value_with_ref():
    """KmՋ_extract_param_value�e�lYt$ref_(u"""
    handler = SwaggerHandler()

    swagger_data = {
        "definitions": {
            "User": {
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                }
            }
        }
    }

    prop_info = {"$ref": "#/definitions/User"}
    result = handler._extract_param_value(prop_info, swagger_data)

    assert result == {"id": 0, "name": ""}


@allure.feature("Swagger�ech�f�ehV")
@allure.story("�c�S�Spe<P-L]WY�[a�{|�W")
def test_extract_param_value_nested_object():
    """KmՋ_extract_param_value�e�lYtL]WY�[a�"""
    handler = SwaggerHandler()

    swagger_data = {}
    prop_info = {
        "type": "object",
        "properties": {
            "address": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "street": {"type": "string"},
                }
            },
            "name": {"type": "string"},
        }
    }

    result = handler._extract_param_value(prop_info, swagger_data)

    assert result == {"address": {"city": "", "street": ""}, "name": ""}


@allure.feature("Swagger�ech�f�ehV")
@allure.story("�c�S�Spe<P-zz�[a�")
def test_extract_param_value_empty_object():
    """KmՋ_extract_param_value�e�lYtzz�[a�"""
    handler = SwaggerHandler()

    swagger_data = {}
    prop_info = {"type": "object"}

    result = handler._extract_param_value(prop_info, swagger_data)

    assert result == {}


@allure.feature("Swagger�ech�f�ehV")
@allure.story("�c�S�Spe<P-pe�~{|�W&^$ref")
def test_extract_param_value_array_with_ref():
    """KmՋ_extract_param_value�e�lYt&^$ref�vpe�~"""
    handler = SwaggerHandler()

    swagger_data = {
        "definitions": {
            "Item": {
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                }
            }
        }
    }

    prop_info = {
        "type": "array",
        "items": {"$ref": "#/definitions/Item"}
    }

    result = handler._extract_param_value(prop_info, swagger_data)

    assert result == [{"id": 0, "name": ""}]


@allure.feature("Swagger�ech�f�ehV")
@allure.story("�c�S�Spe<P-pe�~{|�W&^properties")
def test_extract_param_value_array_with_properties():
    """KmՋ_extract_param_value�e�lYt&^properties�vpe�~"""
    handler = SwaggerHandler()

    swagger_data = {}
    prop_info = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            }
        }
    }

    result = handler._extract_param_value(prop_info, swagger_data)

    assert result == [{"id": 0, "name": ""}]


@allure.feature("Swagger�ech�f�ehV")
@allure.story("�c�S�Spe<P-zzpe�~")

@allure.feature("Swagger文档更新器")
@allure.story("提取参数值-空数组")
def test_extract_param_value_empty_array():
    """测试_extract_param_value方法处理空数组"""
    handler = SwaggerHandler()

    swagger_data = {}
    prop_info = {"type": "array"}

    result = handler._extract_param_value(prop_info, swagger_data)

    assert result == []
