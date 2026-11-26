"""测试 har2pytest.swagger_handler 模块中 Swagger 文档获取与合并、API 信息查找、参数提取与默认值、嵌套描述递归提取、URL 清洗与 $ref 解析的功能与边界。"""

import asyncio

import allure
import pytest

from har2pytest.swagger_handler import SwaggerHandler

# ==================== 查找API信息测试 ====================


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
                    "parameters": [{"name": "id", "in": "query", "type": "integer", "description": "ID参数"}],
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None
    assert result.summary == "测试API"


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试header参数不进入parameters")
def test_find_api_info_header_param_excluded():
    """in: header 参数（如 Authorization）不应被收进 parameters，
    否则会以默认值空串写入 api.json 的 params，导致生成的测试用例
    向无 params 参数的 API 函数传参（TypeError）。"""
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "parameters": [
                        {"name": "Authorization", "in": "header", "type": "string", "description": "令牌"},
                        {"name": "id", "in": "query", "type": "string", "description": "ID参数"},
                    ],
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result.parameters == {"id": "ID参数"}
    assert "Authorization" not in result.param_defaults


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试formData文件参数进入参数说明与默认值")
def test_find_api_info_form_data_param_included():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/demo/upload": {
                "post": {
                    "summary": "上传附件",
                    "consumes": ["multipart/form-data"],
                    "parameters": [
                        {"name": "Authorization", "in": "header", "type": "string", "description": "令牌"},
                        {"name": "file", "in": "formData", "type": "file", "description": "附件文件"},
                    ],
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/demo/upload", "POST")
    # formData 参数的描述被收进 parameters，header 参数仍被忽略
    assert result.parameters == {"file": "附件文件"}
    assert result.param_defaults == {"file": "(binary)"}


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试带BasePath查找API信息")
def test_find_api_info_with_basepath():
    handler = SwaggerHandler()
    swagger_data = {"basePath": "/v1", "paths": {"/api/test": {"get": {"summary": "测试API"}}}}
    result = handler.find_api_info_in_swagger(swagger_data, "/v1/api/test", "GET")
    assert result is not None
    assert result.summary == "测试API"


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
                    "parameters": [{"name": "body", "in": "body", "schema": {"$ref": "#/definitions/TestModel"}}],
                }
            }
        },
        "definitions": {
            "TestModel": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "姓名"},
                    "age": {"type": "integer", "description": "年龄"},
                },
            }
        },
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result.summary == "测试API"
    # body schema 的属性描述经 $ref 递归提取进 result.parameters
    assert result.parameters == {"name": "姓名", "age": "年龄"}


# ==================== 获取默认值测试 ====================


@pytest.mark.parametrize("type_name,param_name,expected", [
    pytest.param("string", None, "", id="string默认空串"),
    pytest.param("integer", None, None, id="integer默认None"),
    pytest.param("boolean", None, None, id="boolean默认None"),
    pytest.param("array", None, [], id="array默认空列表"),
    pytest.param("object", None, {}, id="object默认空字典"),
    # 分页参数特殊默认值
    pytest.param("integer", "pageNum", 1, id="分页pageNum默认1"),
    pytest.param("integer", "pageSize", 10, id="分页pageSize默认10"),
    pytest.param("unknown", None, "", id="未知类型默认空串"),
    pytest.param("integer", "someField", None, id="非分页参数名integer返回None"),
])
@allure.feature("Swagger处理器")
@allure.story("获取默认值")
@allure.title("测试获取各类型默认值")
def test_get_default_value_forms(type_name, param_name, expected):
    handler = SwaggerHandler()
    if param_name is None:
        assert handler._get_default_value(type_name) == expected
    else:
        assert handler._get_default_value(type_name, param_name) == expected


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试从Swagger提取查询参数")
def test_extract_params_from_swagger():
    handler = SwaggerHandler()
    swagger_info = {
        "parameters": [
            {"name": "id", "in": "query", "type": "integer", "required": True},
            {"name": "name", "in": "query", "type": "string", "required": False},
        ]
    }
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) == 6
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = params
    assert len(query_params) == 2
    assert "id" in query_params
    assert "name" in query_params


# ==================== 提取参数测试 ====================


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
                "schema": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}},
            }
        ]
    }
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) >= 2


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试多行参数描述压成单行")
def test_extract_params_from_swagger_multiline_description():
    handler = SwaggerHandler()
    swagger_data = {
        "definitions": {
            "GiftOrderQueryReqDTO": {
                "type": "object",
                "properties": {
                    "orderStatusList": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "订单状态集合（参考OrderStatus枚举）：\n1:待支付, 2:待发货",
                    }
                },
            }
        }
    }
    parameters = [
        {"name": "body", "in": "body", "schema": {"$ref": "#/definitions/GiftOrderQueryReqDTO"}},
        {"name": "pageNum", "in": "query", "type": "integer", "description": "分页页码\n（默认1）"},
    ]
    param_descriptions = handler._extract_params_from_swagger(parameters, swagger_data)[5]

    assert param_descriptions["orderStatusList"] == "订单状态集合（参考OrderStatus枚举）： 1:待支付, 2:待发货"
    assert param_descriptions["pageNum"] == "分页页码 （默认1）"
    assert all("\n" not in value for value in param_descriptions.values())


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
@allure.story("从Swagger提取参数")
@allure.title("测试提取formData表单与文件参数")
def test_extract_params_from_swagger_form_data():
    handler = SwaggerHandler()
    parameters = [
        {"name": "file", "in": "formData", "type": "file", "description": "附件文件"},
        {"name": "remark", "in": "formData", "type": "string", "description": "备注"},
        {"name": "count", "in": "formData", "type": "integer", "description": "数量"},
    ]
    query_params, post_data, _, has_body_param, path_params, descriptions = handler._extract_params_from_swagger(
        parameters, {}
    )
    # 表单参数归入请求体；file 类型填 (binary) 占位，与 HAR 路径
    # _find_file_upload_key 的约定一致，其余类型走常规默认值
    assert post_data == {"file": "(binary)", "remark": "", "count": None}
    assert has_body_param is True
    assert query_params == {}
    assert path_params == {}
    assert descriptions == {"file": "附件文件", "remark": "备注", "count": "数量"}


@allure.feature("Swagger处理器")
@allure.story("提取Body参数")
@allure.title("测试提取引用类型Body参数")
def test_extract_body_params_with_ref():
    handler = SwaggerHandler()
    swagger_data = {
        "definitions": {
            "TestModel": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}
        }
    }
    param = {"name": "body", "in": "body", "schema": {"$ref": "#/definitions/TestModel"}}
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
        "schema": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}},
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
    param = {"name": "body", "in": "body", "schema": {"$ref": "#/definitions/NotFound"}}
    params = handler._extract_body_params(param["schema"], {})
    assert params == {}


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试裸类型Body参数兜底提取默认值与说明")
def test_extract_params_from_swagger_bare_type_body():
    handler = SwaggerHandler()
    parameters = [
        {"name": "orderNo", "in": "body", "description": "订单号", "schema": {"type": "string"}},
        {"name": "remarks", "in": "query", "type": "string", "description": "备注"},
    ]
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
        handler._extract_params_from_swagger(parameters, {})
    )
    assert has_body_param is True
    assert has_query_param is True
    assert post_data == {"orderNo": ""}
    assert query_params == {"remarks": ""}
    assert param_descriptions == {"orderNo": "订单号", "remarks": "备注"}


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试裸类型Body参数按类型取默认值")
def test_extract_params_from_swagger_bare_type_body_default_value():
    handler = SwaggerHandler()
    parameters = [{"name": "count", "in": "body", "schema": {"type": "integer"}}]
    _, post_data, _, has_body_param, _, _ = handler._extract_params_from_swagger(parameters, {})
    assert has_body_param is True
    assert post_data == {"count": None}


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试裸类型Body参数查找API信息补齐说明与默认值")
def test_find_api_info_in_swagger_bare_type_body():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/mgmt/order/demoAction": {
                "post": {
                    "summary": "取消订单",
                    "parameters": [
                        {"name": "orderNo", "in": "body", "description": "订单号", "schema": {"type": "string"}},
                        {"name": "remarks", "in": "query", "type": "string", "description": "备注"},
                    ],
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/mgmt/order/demoAction", "POST")
    assert result.summary == "取消订单"
    assert result.parameters == {"orderNo": "订单号", "remarks": "备注"}
    assert result.param_defaults["orderNo"] == ""
    assert result.param_defaults["remarks"] == ""


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试顶层数组Body提取元素备注与类型感知默认值")
def test_find_api_info_in_swagger_top_level_array_body():
    handler = SwaggerHandler()
    swagger_data = {
        "definitions": {
            "DemoItem": {
                "type": "object",
                "properties": {
                    "demoCode": {"type": "string", "description": "演示编码"},
                    "demoCount": {"type": "integer", "description": "演示数量"},
                },
            }
        },
        "paths": {
            "/mgmt/demo/demoBatchAction": {
                "post": {
                    "summary": "演示批量操作",
                    "parameters": [
                        {
                            "name": "itemList",
                            "in": "body",
                            "description": "itemList",
                            "required": True,
                            "schema": {"type": "array", "items": {"$ref": "#/definitions/DemoItem"}},
                        }
                    ],
                }
            }
        },
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/mgmt/demo/demoBatchAction", "POST")
    # 元素字段备注展开为顶层键；参数名自身不再产生噪声备注
    assert result.parameters == {"demoCode": "演示编码", "demoCount": "演示数量"}
    # 类型感知默认值：字符串 ""、整型 None
    assert result.param_defaults == {"demoCode": "", "demoCount": None}


@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试标量数组Body保留参数名兜底备注")
def test_find_api_info_in_swagger_scalar_array_body_fallback():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/mgmt/demo/demoCodeList": {
                "post": {
                    "summary": "演示编码列表",
                    "parameters": [
                        {
                            "name": "codeList",
                            "in": "body",
                            "description": "演示编码列表",
                            "schema": {"type": "array", "items": {"type": "string"}},
                        }
                    ],
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/mgmt/demo/demoCodeList", "POST")
    # 无模型可展开的标量数组：兜底备注保留
    assert result.parameters == {"codeList": "演示编码列表"}
    assert "codeList" not in result.param_defaults


# ==================== 提取Body参数测试 ====================


@pytest.mark.parametrize("swagger_data,url,method", [
    pytest.param({"paths": {"/api/test": {"get": {}}}}, "/api/notfound", "GET", id="路径不存在"),
    # 路径存在但方法缺失时：不抛错，返回空 SwaggerInfo（无 summary/description）
    pytest.param({"paths": {"/api/test": {"get": {"summary": "GET测试"}, "post": {"summary": "POST测试"}}}}, "/api/test", "PUT", id="方法未找到"),
    pytest.param({}, "/api/test", "GET", id="空Swagger数据"),
    pytest.param({"paths": {}}, "/api/test", "GET", id="空路径"),
])
@allure.feature("Swagger处理器")
@allure.story("从Swagger查找API信息")
@allure.title("测试未命中时查找API信息返回空信息")
def test_find_api_info_not_found_forms(swagger_data, url, method):
    handler = SwaggerHandler()
    result = handler.find_api_info_in_swagger(swagger_data, url, method)
    assert result.summary == ""
    assert result.description == ""


# ==================== 初始化测试 ====================


@allure.feature("Swagger处理器")
@allure.story("初始化")
@allure.title("测试Swagger处理器初始化")
def test_swagger_handler_init():
    handler = SwaggerHandler()
    assert handler.swagger_cache == {}


# ==================== 获取Swagger文档测试 ====================


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试所有路径获取Swagger文档失败")
def test_get_swagger_doc_all_paths_failed(monkeypatch):
    async def mock_send_request(url):
        raise Exception("Connection failed")

    handler = SwaggerHandler()
    monkeypatch.setattr(handler, "_send_request", mock_send_request)
    result = asyncio.run(handler.get_swagger_doc("https://invalid-url.com"))
    assert result is None


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试通过 swagger-resources 发现文档路径并成功获取")
def test_get_swagger_doc_via_swagger_resources(monkeypatch):
    calls = []

    async def mock_send_request(url):
        calls.append(url)
        if url.endswith("/swagger-resources"):
            return [{"location": "/actual/api-docs"}]
        return {"paths": {"/api/test": {"get": {}}}}

    handler = SwaggerHandler()
    monkeypatch.setattr(handler, "_send_request", mock_send_request)
    result = asyncio.run(handler.get_swagger_doc("https://example.com"))
    assert result is not None
    assert "paths" in result
    assert any("actual/api-docs" in u for u in calls)


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试遍历并合并 swagger-resources 的全部分组")
def test_get_swagger_doc_merges_all_groups(monkeypatch):
    calls = []
    docs = {
        "https://example.com/admin/v2/api-docs?group=ApiV_1": {
            "swagger": "2.0",
            "basePath": "/admin",
            "tags": [{"name": "comm"}],
            "paths": {"/admin/comm/coupon": {"get": {"summary": "优惠券列表"}}},
            "definitions": {"Coupon": {"type": "object", "properties": {"id": {"type": "integer"}}}},
        },
        "https://example.com/admin/v2/api-docs?group=ApiV_2": {
            "swagger": "2.0",
            "basePath": "/admin",
            "tags": [{"name": "activity"}],
            "paths": {
                "/admin/activity/activity": {"get": {"summary": "活动列表"}},
                # 与第一个分组重复的 path+method：保留首次出现的定义
                "/admin/comm/coupon": {"get": {"summary": "重复的优惠券列表"}, "post": {"summary": "新增优惠券"}},
            },
            "definitions": {
                "Activity": {"type": "object", "properties": {"id": {"type": "integer"}}},
                "Coupon": {"type": "object", "properties": {"stale": {"type": "string"}}},
            },
        },
    }

    async def mock_send_request(url):
        calls.append(url)
        if url.endswith("/swagger-resources"):
            return [
                {"name": "ApiV_1", "location": "/v2/api-docs?group=ApiV_1"},
                {"name": "ApiV_2", "location": "/v2/api-docs?group=ApiV_2"},
            ]
        return docs[url]

    handler = SwaggerHandler()
    monkeypatch.setattr(handler, "_send_request", mock_send_request)
    result = asyncio.run(handler.get_swagger_doc("https://example.com/admin/doc.html#/"))

    assert result is not None
    # 两个分组的路径都拿到
    assert set(result["paths"]) == {"/admin/comm/coupon", "/admin/activity/activity"}
    # 同 path 的不同 method 合并
    assert set(result["paths"]["/admin/comm/coupon"]) == {"get", "post"}
    # 重复的 path+method 保留首次出现
    assert result["paths"]["/admin/comm/coupon"]["get"]["summary"] == "优惠券列表"
    # definitions 取并集，重名保留首次出现的定义
    assert set(result["definitions"]) == {"Coupon", "Activity"}
    assert "id" in result["definitions"]["Coupon"]["properties"]
    # tags 合并，顶层字段取首个分组
    assert [t["name"] for t in result["tags"]] == ["comm", "activity"]
    assert result["basePath"] == "/admin"
    # 两个分组文档都被请求过
    assert sum(1 for u in calls if "api-docs?group=" in u) == 2


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试部分分组获取失败时仍合并其余分组")
def test_get_swagger_doc_group_failure_keeps_others(monkeypatch):
    async def mock_send_request(url):
        if url.endswith("/swagger-resources"):
            return [
                {"name": "ApiV_1", "location": "/v2/api-docs?group=ApiV_1"},
                {"name": "broken", "location": "/v2/api-docs?group=broken"},
                {"name": "ApiV_2", "location": "/v2/api-docs?group=ApiV_2"},
            ]
        if url.endswith("group=broken"):
            raise Exception("500 Server Error")
        group = url.rsplit("=", 1)[-1]
        return {"paths": {f"/{group}/list": {"get": {"summary": group}}}}

    handler = SwaggerHandler()
    monkeypatch.setattr(handler, "_send_request", mock_send_request)
    result = asyncio.run(handler.get_swagger_doc("https://example.com"))

    assert result is not None
    assert set(result["paths"]) == {"/ApiV_1/list", "/ApiV_2/list"}
    # 没有任何分组携带 tags/definitions 时不留空键
    assert "tags" not in result
    assert "definitions" not in result


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试 swagger-resources 为空列表时回退到常见路径")
def test_get_swagger_doc_empty_resources_fallback(monkeypatch):
    async def mock_send_request(url):
        if url.endswith("/swagger-resources"):
            return []
        return {"paths": {"/api/test": {"get": {}}}}

    handler = SwaggerHandler()
    monkeypatch.setattr(handler, "_send_request", mock_send_request)
    result = asyncio.run(handler.get_swagger_doc("https://example.com"))
    assert result is not None
    assert "/api/test" in result["paths"]


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试 swagger-resources 失败后回退到常见路径")
def test_get_swagger_doc_fallback_paths(monkeypatch):
    async def mock_send_request(url):
        if url.endswith("/swagger-resources"):
            raise Exception("no resources")
        return {"paths": {"/api/test": {"get": {}}}}

    handler = SwaggerHandler()
    monkeypatch.setattr(handler, "_send_request", mock_send_request)
    result = asyncio.run(handler.get_swagger_doc("https://example.com"))
    assert result is not None
    assert "paths" in result


@allure.feature("Swagger处理器")
@allure.story("从Swagger生成API")
@allure.title("测试从Swagger生成API并提取参数")
def test_find_api_info_in_swagger_extract_params():
    handler = SwaggerHandler()
    swagger_data = {
        "paths": {
            "/api/test": {
                "get": {
                    "summary": "测试API",
                    "parameters": [
                        {"name": "id", "in": "query", "type": "integer", "description": "ID参数"},
                        {"name": "name", "in": "query", "type": "string", "description": "名称参数"},
                    ],
                }
            }
        }
    }
    result = handler.find_api_info_in_swagger(swagger_data, "/api/test", "GET")
    assert result is not None
    assert len(result.parameters) == 2


# ==================== 从Swagger生成API测试 ====================


@allure.feature("Swagger处理器")
@allure.story("获取Swagger文档")
@allure.title("测试Swagger文档缓存命中与首次获取")
def test_get_swagger_doc_caching(monkeypatch):
    handler = SwaggerHandler()
    swagger_data = {"paths": {"/api/test": {"get": {}}}}

    call_count = [0]

    async def mock_send_request(url):
        call_count[0] += 1
        return swagger_data

    monkeypatch.setattr(handler, "_send_request", mock_send_request)

    # 预填缓存：直接命中，不发任何网络请求
    handler.swagger_cache["https://cached.com"] = swagger_data
    result_cached = asyncio.run(handler.get_swagger_doc("https://cached.com"))
    assert result_cached == swagger_data
    assert call_count[0] == 0

    # 首次获取：探测 swagger-resources + 常见路径，至少发 1 次请求
    result1 = asyncio.run(handler.get_swagger_doc("https://example.com"))
    calls_after_first = call_count[0]
    assert calls_after_first >= 1
    assert result1 is not None

    # 第二次调用命中缓存，不再发起请求
    result2 = asyncio.run(handler.get_swagger_doc("https://example.com"))
    assert call_count[0] == calls_after_first
    assert result2 is not None


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试提取枚举类型参数")
def test_extract_params_with_enum():
    handler = SwaggerHandler()
    swagger_info = {"parameters": [{"name": "status", "in": "query", "type": "string", "enum": ["active", "inactive"]}]}
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) == 6
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = params
    assert "status" in query_params


# ==================== 提取参数值测试 ====================


@allure.feature("Swagger处理器")
@allure.story("从Swagger提取参数")
@allure.title("测试提取路径参数")
def test_extract_params_path_param():
    handler = SwaggerHandler()
    swagger_info = {"parameters": [{"name": "id", "in": "path", "type": "integer", "required": True}]}
    params = handler._extract_params_from_swagger(swagger_info["parameters"], {})
    assert len(params) == 6
    query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = params
    # path 参数进入 path_params（默认值按 integer=None），不落入 query
    assert path_params == {"id": None}
    assert query_params == {}
    assert has_query_param is False


@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取引用类型参数值")
def test_extract_param_value_with_ref():
    handler = SwaggerHandler()
    swagger_data = {"definitions": {"TestModel": {"type": "object", "properties": {"name": {"type": "string"}}}}}
    param = {"name": "body", "in": "body", "schema": {"$ref": "#/definitions/TestModel"}}
    value = handler._extract_param_value(param["schema"], swagger_data)
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
                "user": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}
            },
        },
    }
    value = handler._extract_param_value(param["schema"], {})
    assert isinstance(value, dict)


@pytest.mark.parametrize("schema,expected", [
    pytest.param({"type": "object"}, {}, id="空对象参数值"),
    pytest.param({"type": "array"}, [], id="空数组参数值"),
])
@allure.feature("Swagger处理器")
@allure.story("提取参数值")
@allure.title("测试提取空容器参数值")
def test_extract_param_value_empty_container_forms(schema, expected):
    handler = SwaggerHandler()
    value = handler._extract_param_value(schema, {})
    assert value == expected


# ==================== 清洗Swagger URL测试 ====================


class TestCleanSwaggerUrl:
    @pytest.mark.parametrize("url,expected", [
        pytest.param("https://example.com/doc.html", "https://example.com", id="移除doc_html后缀"),
        pytest.param("https://example.com/index.html", "https://example.com", id="移除index_html后缀"),
        pytest.param("https://example.com/swagger-ui.html", "https://example.com", id="移除swagger_ui_html后缀"),
        pytest.param("https://example.com/doc.html#/user/getUserById", "https://example.com", id="移除URL_fragment"),
        pytest.param("https://example.com/", "https://example.com", id="移除末尾斜杠"),
        pytest.param("https://example.com/api", "https://example.com/api", id="干净的URL不变化"),
        pytest.param("https://example.com/doc.html#/order/list", "https://example.com", id="带fragment和doc_html的URL"),
    ])
    @allure.feature("Swagger处理器")
    @allure.story("清洗Swagger URL")
    @allure.title("测试清洗Swagger URL各形态")
    def test_clean_swagger_url_forms(self, url, expected):
        assert SwaggerHandler._clean_swagger_url(url) == expected


# ==================== 提取参数值边缘测试 ====================


class TestExtractParamValueEdge:
    @pytest.mark.parametrize("schema,expected", [
        pytest.param({}, "", id="无type的默认返回值"),
        pytest.param({"type": "number"}, None, id="number类型"),
        pytest.param({"type": "float"}, None, id="float类型"),
        pytest.param({"type": "int"}, None, id="int类型"),
        pytest.param({"type": "boolean"}, None, id="boolean类型"),
    ])
    @allure.feature("Swagger处理器")
    @allure.story("提取参数值-边缘")
    @allure.title("测试标量类型参数值各形态")
    def test_scalar_type_forms(self, schema, expected):
        handler = SwaggerHandler()
        value = handler._extract_param_value(schema, {})
        assert value == expected

    @allure.feature("Swagger处理器")
    @allure.story("提取参数值-边缘")
    @allure.title("测试object类型带$ref")
    def test_object_with_ref(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "Address": {"type": "object", "properties": {"city": {"type": "string"}, "street": {"type": "string"}}}
            }
        }
        value = handler._extract_param_value({"$ref": "#/definitions/Address"}, swagger_data)
        assert isinstance(value, dict)
        assert "city" in value

    @pytest.mark.parametrize("schema,swagger_data", [
        pytest.param({"type": "array", "items": {"$ref": "#/definitions/Tag"}}, {"definitions": {"Tag": {"type": "object", "properties": {"name": {"type": "string"}}}}}, id="array类型带ref_items"),
        pytest.param({"type": "array", "items": {"type": "object", "properties": {"key": {"type": "string"}}}}, {}, id="array类型带properties_items"),
    ])
    @allure.feature("Swagger处理器")
    @allure.story("提取参数值-边缘")
    @allure.title("测试array类型带items时提取单元素列表")
    def test_array_with_items_forms(self, schema, swagger_data):
        handler = SwaggerHandler()
        value = handler._extract_param_value(schema, swagger_data)
        assert isinstance(value, list)
        assert len(value) == 1


# ==================== 提取嵌套描述测试 ====================


class TestExtractNestedDescriptions:
    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试提取引用类型的嵌套描述")
    def test_extract_nested_desc_with_ref(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "UserInfo": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "用户名称"},
                        "age": {"type": "integer", "description": "用户年龄"},
                    },
                }
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions({"$ref": "#/definitions/UserInfo"}, swagger_data, descriptions)
        assert "name" in descriptions
        assert descriptions["name"] == "用户名称"
        assert "age" in descriptions
        assert descriptions["age"] == "用户年龄"

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试提取properties类型的嵌套描述")
    def test_extract_nested_desc_with_properties(self):
        handler = SwaggerHandler()
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "ID"},
                "name": {"type": "string", "description": "名称"},
            },
        }
        descriptions = {}
        handler._extract_nested_descriptions(schema, {}, descriptions)
        assert "id" in descriptions
        assert descriptions["id"] == "ID"
        assert "name" in descriptions
        assert descriptions["name"] == "名称"

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试提取嵌套对象描述（带父级键）")
    def test_extract_nested_desc_with_parent_key(self):
        handler = SwaggerHandler()
        schema = {
            "type": "object",
            "properties": {
                "user": {"type": "object", "properties": {"name": {"type": "string", "description": "用户名"}}}
            },
        }
        descriptions = {}
        handler._extract_nested_descriptions(schema, {}, descriptions)
        assert "user" not in descriptions  # user本身没有description
        assert "user.name" in descriptions
        assert descriptions["user.name"] == "用户名"

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试提取数组嵌套描述")
    def test_extract_nested_desc_with_array(self):
        handler = SwaggerHandler()
        schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {"type": "object", "properties": {"id": {"type": "integer", "description": "项目ID"}}},
                }
            },
        }
        descriptions = {}
        handler._extract_nested_descriptions(schema, {}, descriptions)
        assert "items.id" in descriptions
        assert descriptions["items.id"] == "项目ID"

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试顶层数组Body引用模型的元素描述提取")
    def test_extract_nested_desc_top_level_array_with_ref(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "DemoItem": {
                    "type": "object",
                    "properties": {
                        "demoCode": {"type": "string", "description": "演示编码"},
                        "demoCount": {"type": "integer", "description": "演示数量"},
                    },
                }
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions(
            {"type": "array", "items": {"$ref": "#/definitions/DemoItem"}}, swagger_data, descriptions
        )
        assert descriptions == {"demoCode": "演示编码", "demoCount": "演示数量"}

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试顶层数组Body内联模型的元素描述提取")
    def test_extract_nested_desc_top_level_array_inline_properties(self):
        handler = SwaggerHandler()
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"demoName": {"type": "string", "description": "演示名称"}},
            },
        }
        descriptions = {}
        handler._extract_nested_descriptions(schema, {}, descriptions)
        assert descriptions == {"demoName": "演示名称"}

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试顶层标量数组无描述可提取")
    def test_extract_nested_desc_top_level_scalar_array(self):
        handler = SwaggerHandler()
        descriptions = {}
        handler._extract_nested_descriptions({"type": "array", "items": {"type": "string"}}, {}, descriptions)
        assert descriptions == {}

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试顶层数组Body自引用模型防环")
    def test_extract_nested_desc_top_level_array_self_ref(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "DemoNode": {
                    "type": "object",
                    "properties": {
                        "demoName": {"type": "string", "description": "演示名称"},
                        "children": {"type": "array", "items": {"$ref": "#/definitions/DemoNode"}},
                    },
                }
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions(
            {"type": "array", "items": {"$ref": "#/definitions/DemoNode"}}, swagger_data, descriptions
        )
        # 自引用环在 children 分支停止，首层字段正常提取
        assert descriptions == {"demoName": "演示名称"}

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试提取嵌套引用描述（含父级键）")
    def test_extract_nested_desc_with_ref_and_parent_key(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "Address": {"type": "object", "properties": {"city": {"type": "string", "description": "城市"}}}
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions({"$ref": "#/definitions/Address"}, swagger_data, descriptions, "address")
        assert "address.city" in descriptions
        assert descriptions["address.city"] == "城市"

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试空schema")
    def test_extract_nested_desc_empty_schema(self):
        handler = SwaggerHandler()
        descriptions = {}
        handler._extract_nested_descriptions({}, {}, descriptions)
        assert descriptions == {}

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试引用未找到")
    def test_extract_nested_desc_ref_not_found(self):
        handler = SwaggerHandler()
        descriptions = {}
        handler._extract_nested_descriptions({"$ref": "#/definitions/NotFound"}, {}, descriptions)
        assert descriptions == {}

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试自引用模型（数组指向自身）不无限递归")
    def test_extract_nested_desc_self_ref_array(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "MsgType": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "类型ID"},
                        "name": {"type": "string", "description": "类型名称"},
                        "children": {
                            "type": "array",
                            "description": "子类型列表",
                            "items": {"$ref": "#/definitions/MsgType"},
                        },
                    },
                }
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions({"$ref": "#/definitions/MsgType"}, swagger_data, descriptions)
        assert descriptions["id"] == "类型ID"
        assert descriptions["name"] == "类型名称"
        assert descriptions["children"] == "子类型列表"
        # 自引用环在第一处重复 $ref 被截断，不再展开第二层 children
        assert "children.id" not in descriptions

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试互相引用模型不无限递归")
    def test_extract_nested_desc_cross_ref_cycle(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "A": {
                    "type": "object",
                    "properties": {
                        "aName": {"type": "string", "description": "A名称"},
                        "b": {"$ref": "#/definitions/B"},
                    },
                },
                "B": {
                    "type": "object",
                    "properties": {
                        "bName": {"type": "string", "description": "B名称"},
                        "a": {"$ref": "#/definitions/A"},
                    },
                },
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions({"$ref": "#/definitions/A"}, swagger_data, descriptions)
        assert descriptions["aName"] == "A名称"
        assert descriptions["b.bName"] == "B名称"
        # 回到 A 的引用在 b.a 处被截断
        assert "b.a.aName" not in descriptions

    @allure.feature("Swagger处理器")
    @allure.story("提取嵌套描述")
    @allure.title("测试兄弟节点引用同一模型时各自完整展开")
    def test_extract_nested_desc_sibling_refs(self):
        handler = SwaggerHandler()
        swagger_data = {
            "definitions": {
                "Addr": {"type": "object", "properties": {"city": {"type": "string", "description": "城市"}}},
                "User": {
                    "type": "object",
                    "properties": {
                        "home": {"$ref": "#/definitions/Addr"},
                        "office": {"$ref": "#/definitions/Addr"},
                    },
                },
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions({"$ref": "#/definitions/User"}, swagger_data, descriptions)
        assert descriptions["home.city"] == "城市"
        assert descriptions["office.city"] == "城市"


# ==================== OpenAPI 3 components/schemas 测试 ====================


class TestOpenAPI3ComponentsSchemas:
    @allure.feature("Swagger处理器")
    @allure.story("OpenAPI3 components/schemas")
    @allure.title("测试 $ref 解析到 components/schemas")
    def test_resolve_schema_ref_components(self):
        handler = SwaggerHandler()
        swagger_data = {
            "components": {"schemas": {"TestModel": {"type": "object", "properties": {"name": {"type": "string"}}}}}
        }
        result = handler._resolve_schema_ref("#/components/schemas/TestModel", swagger_data)
        assert result is not None
        assert "name" in result["properties"]

    @allure.feature("Swagger处理器")
    @allure.story("OpenAPI3 components/schemas")
    @allure.title("测试 $ref 解析到 definitions(v2 兼容)")
    def test_resolve_schema_ref_definitions(self):
        handler = SwaggerHandler()
        swagger_data = {"definitions": {"TestModel": {"type": "object", "properties": {"name": {"type": "string"}}}}}
        result = handler._resolve_schema_ref("#/definitions/TestModel", swagger_data)
        assert result is not None
        assert "name" in result["properties"]

    @allure.feature("Swagger处理器")
    @allure.story("OpenAPI3 components/schemas")
    @allure.title("测试 $ref 带文件前缀解析")
    def test_resolve_schema_ref_file_prefix(self):
        handler = SwaggerHandler()
        swagger_data = {
            "components": {"schemas": {"TestModel": {"type": "object", "properties": {"name": {"type": "string"}}}}}
        }
        result = handler._resolve_schema_ref("Model.yaml#/components/schemas/TestModel", swagger_data)
        assert result is not None
        assert "name" in result["properties"]

    @allure.feature("Swagger处理器")
    @allure.story("OpenAPI3 components/schemas")
    @allure.title("测试 components/schemas 提取 body 默认值")
    def test_extract_body_params_components(self):
        handler = SwaggerHandler()
        swagger_data = {
            "components": {
                "schemas": {"TestModel": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}}
            }
        }
        schema = {"$ref": "#/components/schemas/TestModel"}
        params = handler._extract_body_params(schema, swagger_data)
        assert params == {"name": "", "age": None}

    @allure.feature("Swagger处理器")
    @allure.story("OpenAPI3 components/schemas")
    @allure.title("测试 components/schemas 提取嵌套描述")
    def test_extract_nested_desc_components(self):
        handler = SwaggerHandler()
        swagger_data = {
            "components": {
                "schemas": {
                    "UserInfo": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "用户名称"},
                            "age": {"type": "integer", "description": "用户年龄"},
                        },
                    }
                }
            }
        }
        descriptions = {}
        handler._extract_nested_descriptions({"$ref": "#/components/schemas/UserInfo"}, swagger_data, descriptions)
        assert descriptions == {"name": "用户名称", "age": "用户年龄"}


# ==================== close 方法测试 ====================


@allure.feature("Swagger处理器")
@allure.story("会话关闭")
@allure.title("测试未创建会话时 close 不报错")
async def test_close_without_session():
    handler = SwaggerHandler()
    assert handler._session is None
    await handler.close()
    assert handler._session is None


@allure.feature("Swagger处理器")
@allure.story("会话关闭")
@allure.title("测试 close 关闭已有会话并置空")
async def test_close_with_session():
    handler = SwaggerHandler()
    session = await handler._get_session()
    assert session is not None
    assert not session.closed
    await handler.close()
    assert handler._session is None
    assert session.closed


@allure.feature("Swagger处理器")
@allure.story("会话关闭")
@allure.title("测试重复 close 不报错")
async def test_close_idempotent():
    handler = SwaggerHandler()
    await handler._get_session()
    await handler.close()
    await handler.close()
    assert handler._session is None
