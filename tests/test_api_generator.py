"""测试 api_generator.py 模块 - APIGenerator 类"""

import asyncio
import json
import logging
import os

import allure
import pytest

from har2pytest.api_generator import APIGenerator
from har2pytest.config import APIConfig
from har2pytest.models import ParsedRequestInfo, SwaggerInfo


@pytest.fixture(scope="session")
def generator() -> APIGenerator:
    """会话级共享 APIGenerator，供只做字符串生成的测试复用（避免逐个构造）。"""
    return APIGenerator(output_dir="test_output")


@pytest.fixture
def use_test_config(monkeypatch):
    """使用测试配置文件，避免依赖生产环境配置。"""
    test_config = str(os.path.join(os.path.dirname(__file__), "har2pytest_config_test.json"))
    monkeypatch.setenv("HAR2PYTEST_CONFIG", test_config)
    APIConfig._config = None  # 重置配置缓存
    yield
    APIConfig._config = None  # 测试后也重置，避免影响其他测试


# ==================== 初始化测试 ====================


@allure.feature("API 生成器")
@allure.story("初始化")
@allure.title("测试默认输出目录初始化")
def test_init_default_output_dir():
    generator = APIGenerator()
    assert generator.output_dir is not None
    assert generator.swagger_handler is not None
    assert generator.url_matcher is not None


@allure.feature("API 生成器")
@allure.story("初始化")
@allure.title("测试自定义输出目录初始化")
def test_init_custom_output_dir(tmp_path):
    custom_dir = str(tmp_path / "custom_api")
    generator = APIGenerator(output_dir=custom_dir)
    assert generator.output_dir == custom_dir


# ==================== 检查 API 是否存在测试 ====================
@allure.title("测试 API 文件不存在")
def test_check_api_exists_not_found(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path))
    assert not generator.check_api_exists("/api/test_endpoint", "test_service")


@allure.feature("API 生成器")
@allure.story("检查 API 是否存在")
@allure.title("测试根目录下 API 文件存在")
def test_check_api_exists_root_dir(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path))
    func_name = "api_test_endpoint"
    file_path = os.path.join(str(tmp_path), f"{func_name}.py")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# test")
    assert generator.check_api_exists("/api/test_endpoint", "apis")


@allure.feature("API 生成器")
@allure.story("检查 API 是否存在")
@allure.title("测试服务包目录下 API 文件存在")
def test_check_api_exists_service_package_dir(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path))
    func_name = "api_test_endpoint"
    package_dir = os.path.join(str(tmp_path), "test_service")
    os.makedirs(package_dir, exist_ok=True)
    with open(os.path.join(package_dir, f"{func_name}.py"), "w", encoding="utf-8") as f:
        f.write("# test")
    assert generator.check_api_exists("/api/test_endpoint", "test_service")


# ==================== 解析请求信息测试 ====================


@allure.feature("API 生成器")
@allure.story("解析请求信息")
@allure.title("测试解析GET请求信息")
def test_parse_request_info_get(generator, monkeypatch):
    # 隔离 REQUIRED_HEADERS：避免运行目录下配置（含大小写不敏感覆盖的 authorization）
    # 改变本用例传入头，聚焦验证 GET 基础字段解析
    monkeypatch.setattr(APIConfig, "REQUIRED_HEADERS", classmethod(lambda cls: {}))

    request_info = ParsedRequestInfo(
        method="GET",
        url="/api/test",
        query_params={"id": 1},
        post_data={},
        headers={"Authorization": "Bearer token"},
    )
    result = generator._parse_request_info(request_info)
    assert result.method == "GET"
    assert result.query_params == {"id": 1}
    assert "Authorization" in result.headers


@allure.feature("API 生成器")
@allure.story("解析请求信息")
@allure.title("测试解析POST请求信息")
def test_parse_request_info_post(generator):
    request_info = ParsedRequestInfo(
        method="POST",
        url="/api/create",
        query_params={},
        post_data={"name": "test"},
        headers={"content-type": "application/json"},
    )
    result = generator._parse_request_info(request_info)
    assert result.method == "POST"
    assert result.post_data == {"name": "test"}


@allure.feature("API 生成器")
@allure.story("解析请求信息")
@allure.title("测试解析文件上传请求信息")
def test_parse_request_info_file_upload(generator):
    request_info = ParsedRequestInfo(
        method="POST",
        url="/api/upload",
        query_params={},
        post_data={"file": "@test.txt"},
        headers={"content-type": "multipart/form-data"},
    )
    result = generator._parse_request_info(request_info)
    assert result.is_file_upload is True

    # 测试 multipart/form-data 但没有实际文件参数 -> 不是文件上传，使用 data=
    request_info2 = ParsedRequestInfo(
        method="POST",
        url="/api/form",
        query_params={},
        post_data={"orderNo": "SG001", "remarks": "test"},
        headers={"content-type": "multipart/form-data"},
    )
    result2 = generator._parse_request_info(request_info2)
    assert result2.is_file_upload is False
    assert result2.is_json_content is False

    # 测试 HAR 中文件上传的 (binary) 占位符 -> 应是文件上传
    request_info3 = ParsedRequestInfo(
        method="POST",
        url="/api/storage/upload",
        query_params={},
        post_data={"storageType": "PublicCloud", "clientKey": "mall-center-product", "file": "(binary)"},
        headers={"content-type": "multipart/form-data; boundary=----WebKitFormBoundary33zTNLfGBAtCpQkw"},
    )
    result3 = generator._parse_request_info(request_info3)
    assert result3.is_file_upload is True
    assert result3.is_json_content is False


# ==================== 解析请求信息测试 ====================


@allure.feature("API 生成器")
@allure.story("解析请求信息")
@allure.title("测试解析urlencoded请求信息")
def test_parse_request_info_urlencoded_empty_body(generator):
    request_info = ParsedRequestInfo(
        method="POST",
        url="/api/submit",
        query_params={},
        post_data={},
        headers={"content-length": "0"},
    )
    result = generator._parse_request_info(request_info)
    assert result.is_need_urlencode is True


@allure.feature("API 生成器")
@allure.story("解析请求信息")
@allure.title("测试POST空JSON body带query参数时判定为urlencode")
@allure.description(
    "POST 接口 body 为空 JSON（{}）但 URL 带 query 参数（如 ?orderNo=xxx）时，"
    "应按 application/x-www-form-urlencoded 处理（query 参数作为表单数据 urlencode 传参）。"
)
def test_parse_request_info_post_empty_json_body_with_query_urlencode(generator):
    request_info = ParsedRequestInfo(
        method="POST",
        url="/mobile/web/order/as/upgradeOrderVerify",
        query_params={"orderNo": "SG014000260817001801"},
        post_data={},
        headers={"content-type": "application/json;charset=UTF-8", "content-length": "2"},
    )
    result = generator._parse_request_info(request_info)
    assert result.is_need_urlencode is True


@allure.feature("API 生成器")
@allure.story("解析请求信息")
@allure.title("测试请求信息默认补充headers")
def test_parse_request_info_default_headers(generator):
    request_info = ParsedRequestInfo(method="GET", url="/api/test", query_params={}, post_data={}, headers={})
    result = generator._parse_request_info(request_info)
    assert len(result.headers) > 0


@allure.feature("API 生成器")
@allure.story("生成导入语句")
@allure.title("测试生成urlencoded的导入语句")
def test_generate_imports_urlencoded(generator):
    parsed_info = ParsedRequestInfo(is_file_upload=False, is_need_urlencode=True)
    imports = generator._generate_imports(parsed_info)
    assert "from urllib.parse import urlencode" in imports


# ==================== 生成参数字符串测试 ====================


@allure.feature("API 生成器")
@allure.story("生成参数字符串")
@allure.title("测试生成参数字符串")
def test_generate_params_string(generator):
    params = {"keyword": "TS001", "pageNum": 1}
    result = generator._generate_params_string(params)
    assert "keyword" in result
    assert "pageNum" in result


@allure.feature("API 生成器")
@allure.story("生成参数字符串")
@allure.title("测试空参数字典生成")
def test_generate_params_string_empty(generator):
    result = generator._generate_params_string({})
    assert result == "{}"


@allure.feature("API 生成器")
@allure.story("生成参数字符串")
@allure.title("测试带Swagger描述的参数字符串")
def test_generate_params_string_with_swagger_info(generator):
    params = {"id": 1}
    swagger_info = SwaggerInfo(parameters={"id": "用户ID"})
    result = generator._generate_params_string(params, swagger_info)
    assert "id" in result


@allure.feature("API 生成器")
@allure.story("生成参数字符串")
@allure.title("测试JSON数组请求体（list）直接生成Python字面量而非dict格式化")
def test_generate_params_string_list_body(generator):
    params = [{"action": "click", "timestamp": 123}, {"action": "view"}]
    result = generator._generate_params_string(params)
    assert result.startswith("[")
    assert '"action": "click"' in result
    assert '"timestamp": 123' in result
    # 空列表处理
    assert generator._generate_params_string([]) == "[]"


# ==================== 处理参数测试 ====================


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试 PUT 带 JSON body 时识别为 JSON 请求（回归：请求体分类仅在 POST 分支生效）")
def test_parse_request_info_put_json_body(generator):
    request_info = ParsedRequestInfo(
        method="PUT",
        url="/role",
        query_params={},
        post_data={"name": "管理员"},
        headers={"content-type": "application/json"},
    )
    result = generator._parse_request_info(request_info)
    assert result.is_json_content is True

    body = generator._handle_http_method("PUT", "data", {}, {}, False, is_json_content=result.is_json_content)
    assert any("client.put(url=url, json=data" in line for line in body)


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试非 POST 写方法 query 参数走 params（回归：DELETE/PUT query 属于 URL 语义）")
def test_parse_request_info_delete_query_only(generator):
    request_info = ParsedRequestInfo(
        method="DELETE",
        url="/role",
        query_params={"roleId": "1"},
        post_data={},
        headers={},
    )
    parsed = generator._parse_request_info(request_info)
    assert parsed.is_need_urlencode is False

    param_name, param_data = generator._determine_param_info(parsed)
    assert param_name == "params"
    assert param_data == {"roleId": "1"}


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试 REQUIRED_HEADERS 大小写不敏感覆盖，不产生重复头")
def test_parse_request_info_required_headers_case_insensitive(monkeypatch):
    # 临时替换 REQUIRED_HEADERS 为测试值，避免直接访问 _config 私有属性
    monkeypatch.setattr(APIConfig, "REQUIRED_HEADERS", classmethod(lambda cls: {"GW-Client": "test"}))
    generator = APIGenerator(output_dir="test_output")
    request_info = ParsedRequestInfo(
        method="POST",
        url="/mgmt/order/cancel",
        query_params={},
        post_data={},
        headers={"channel": "pc", "gw-client": "op_pc"},
    )
    result = generator._parse_request_info(request_info)
    lower_keys = {k.lower() for k in result.headers}
    # 同义大小写头只保留一份（配置的规范键 GW-Client，值取配置 test）
    assert len([k for k in result.headers if k.lower() == "gw-client"]) == 1
    assert "gw-client" not in result.headers
    assert result.headers["GW-Client"] == "test"
    assert lower_keys == {"channel", "gw-client"}


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试处理GET请求参数")
def test_process_parameters_get(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        path_params={},
        query_params={"id": 1},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=False,
        headers={"Authorization": "Bearer token"},
    )
    result = generator._process_parameters(parsed_info)
    assert any("params =" in line for line in result)
    assert any("headers =" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试处理POST请求参数")
def test_process_parameters_post(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        path_params={},
        query_params={},
        post_data={"name": "test"},
        is_file_upload=False,
        is_need_urlencode=False,
        headers={"content-type": "application/json"},
    )
    result = generator._process_parameters(parsed_info)
    assert any("data =" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试处理urlencoded POST参数")
def test_process_parameters_urlencoded(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        path_params={},
        query_params={"key": "value"},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=True,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    result = generator._process_parameters(parsed_info)
    assert any("content-type" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试处理路径参数")
def test_process_parameters_path_params(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        path_params={"id": "123"},
        query_params={},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=False,
        headers={},
    )
    result = generator._process_parameters(parsed_info)
    assert any("params =" in line for line in result)


# ==================== 处理 HTTP 方法测试 ====================


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理GET方法")
def test_handle_http_method_get(generator):
    result = generator._handle_http_method("GET", "params", {}, {"id": 1}, False)
    assert any("client.get" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理无参数GET方法")
def test_handle_http_method_get_no_params(generator):
    result = generator._handle_http_method("GET", None, {}, {}, False)
    assert any("client.get" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理POST JSON方法")
def test_handle_http_method_post_json(generator):
    result = generator._handle_http_method("POST", "data", {}, {}, False, is_json_content=True)
    assert any("json=data" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理POST urlencoded方法")
def test_handle_http_method_post_urlencoded(generator):
    result = generator._handle_http_method("POST", "data", {}, {}, True)
    assert any("urlencode" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理POST data方法（非JSON非urlencode）")
def test_handle_http_method_post_data(generator):
    result = generator._handle_http_method("POST", "data", {}, {}, False, is_json_content=False)
    assert any("data=data" in line for line in result)
    assert not any("json=data" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理无参数POST方法")
def test_handle_http_method_post_no_params(generator):
    result = generator._handle_http_method("POST", None, {}, {}, False)
    assert any("client.post" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理带路径参数的POST方法")
def test_handle_http_method_post_path_params(generator):
    result = generator._handle_http_method("POST", "params", {"id": "1"}, {}, False)
    assert any("client.post" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理不支持的HTTP方法")
def test_handle_http_method_unsupported(generator):
    with pytest.raises(ValueError, match="不支持的HTTP方法"):
        generator._handle_http_method("HEAD", None, {}, {}, False)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试 PUT/PATCH/DELETE 生成对应 client 调用")
@pytest.mark.parametrize("method,expected", [("PUT", "client.put"), ("PATCH", "client.patch"), ("DELETE", "client.delete")])
def test_handle_http_method_body_methods(generator, method, expected):
    result = generator._handle_http_method(method, "data", {}, {}, False, is_json_content=True)
    assert any(f"{expected}(url=url, json=data" in line for line in result)


@allure.feature("API 生成器")
@allure.story("处理HTTP方法")
@allure.title("测试 DELETE 无请求体时只传 url")
def test_handle_http_method_delete_without_body(generator):
    result = generator._handle_http_method("DELETE", None, {}, {}, False)
    assert any("client.delete(url=url, headers=headers)" in line for line in result)


# ==================== 处理文件上传测试 ====================


@allure.feature("API 生成器")
@allure.story("处理文件上传")
@allure.title("测试文件上传缺少file字段")
def test_handle_file_upload_no_file_key(generator):
    with pytest.raises(ValueError, match="未找到文件参数"):
        generator._handle_file_upload({"name": "test"})


@allure.feature("API 生成器")
@allure.story("处理文件上传")
@allure.title("测试文件上传参数非字典")
def test_handle_file_upload_not_dict(generator):
    with pytest.raises(ValueError, match="文件上传参数格式错误"):
        generator._handle_file_upload("not a dict")


# ==================== 生成函数定义测试 ====================


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试生成GET函数定义")
def test_generate_function_definition_get(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        url="/api/test",
        query_params={"id": 1},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={},
        url_pattern="/api/test",
        headers={},
    )
    swagger_info = SwaggerInfo(summary="测试 API")
    result = generator._generate_function_definition(parsed_info, "api_test", swagger_info)
    assert any("def api_test" in line for line in result)


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试生成POST函数定义")
def test_generate_function_definition_post(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        url="/api/create",
        query_params={},
        post_data={"name": "test"},
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={},
        url_pattern="/api/create",
        headers={},
    )
    swagger_info = SwaggerInfo(description="创建接口")
    result = generator._generate_function_definition(parsed_info, "api_create", swagger_info)
    assert any("def api_create" in line for line in result)


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带路径参数的函数定义")
def test_generate_function_definition_with_path_params(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        url="/api/user/123",
        query_params={},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={"id": "123"},
        url_pattern="/api/user/{id}",
        headers={},
    )
    swagger_info = SwaggerInfo(summary="用户详情")
    result = generator._generate_function_definition(parsed_info, "_api_user_detail", swagger_info)
    assert any("url = f" in line for line in result)


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带摘要的函数定义")
def test_generate_function_definition_with_summary(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        url="/api/test",
        query_params={},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={},
        url_pattern="/api/test",
        headers={},
    )
    swagger_info = SwaggerInfo(summary="获取用户列表")
    result = generator._generate_function_definition(parsed_info, "_api_users", swagger_info)
    assert "获取用户列表" in "\n".join(result)


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带描述的函数定义")
def test_generate_function_definition_with_description(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        url="/api/test",
        query_params={},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={},
        url_pattern="/api/test",
        headers={},
    )
    swagger_info = SwaggerInfo(description="获取用户信息")
    result = generator._generate_function_definition(parsed_info, "_api_users", swagger_info)
    assert "获取用户信息" in "\n".join(result)


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带参数说明的函数定义")
def test_generate_function_definition_with_parameters(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        url="/api/test",
        query_params={"id": 1},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={},
        url_pattern="/api/test",
        headers={},
    )
    swagger_info = SwaggerInfo(summary="测试", parameters={"id": "用户ID"})
    result = generator._generate_function_definition(parsed_info, "api_test", swagger_info)
    content = "\n".join(result)
    assert "用户ID" in content


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带参数的函数签名")
def test_generate_function_definition_with_params(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        url="/api/create",
        query_params={},
        post_data={"name": "test"},
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={},
        url_pattern="/api/create",
        headers={},
    )
    swagger_info = SwaggerInfo()
    result = generator._generate_function_definition(parsed_info, "api_create", swagger_info)
    content = "\n".join(result)
    assert "def api_create(data=data, headers=headers)" in content


# ==================== 生成文件内容测试 ====================


@allure.feature("API 生成器")
@allure.story("生成文件内容")
@allure.title("测试生成GET请求的完整文件内容")
def test_generate_file_content_get(generator):
    request_info = ParsedRequestInfo(
        method="GET",
        url="/api/test",
        query_params={"id": 1},
        post_data={},
        headers={"Authorization": "Bearer token"},
    )
    content = generator.generate_file_content(request_info, "api_test")
    assert "import os" in content  # headers 模板使用 os.environ，始终需要 import os
    assert "def api_test" in content
    assert "client.get" in content


@allure.feature("API 生成器")
@allure.story("生成文件内容")
@allure.title("测试生成POST请求的完整文件内容")
def test_generate_file_content_post(generator):
    request_info = ParsedRequestInfo(
        method="POST",
        url="/api/create",
        query_params={},
        post_data={"name": "test"},
        headers={"content-type": "application/json"},
    )
    content = generator.generate_file_content(request_info, "api_create")
    assert "import os" in content  # headers 模板使用 os.environ，始终需要 import os
    assert "def api_create" in content
    assert "client.post" in content


@allure.feature("API 生成器")
@allure.story("生成文件内容")
@allure.title("测试带Swagger信息生成文件内容")
def test_generate_file_content_with_swagger_info(generator):
    request_info = ParsedRequestInfo(method="GET", url="/api/test", query_params={"id": 1}, post_data={}, headers={})
    swagger_info = SwaggerInfo(summary="获取用户", parameters={"id": "用户ID"})
    content = generator.generate_file_content(request_info, "api_test", swagger_info)
    assert "获取用户" in content


# ==================== 生成索引文件测试 ====================


@allure.feature("API 生成器")
@allure.story("生成索引文件")
@allure.title("测试生成索引文件")
def test_generate_index_file(tmp_path):
    output_dir = str(tmp_path / "api")
    generator = APIGenerator(output_dir=output_dir)

    service_dir = os.path.join(output_dir, "test_service")
    os.makedirs(service_dir, exist_ok=True)
    test_file = os.path.join(service_dir, "api_test.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# test")

    generator.generate_index_file([test_file])

    init_file = os.path.join(service_dir, "__init__.py")
    assert os.path.exists(init_file)
    with open(init_file, encoding="utf-8") as f:
        content = f.read()
    assert "from .api_test import api_test" in content


@allure.feature("API 生成器")
@allure.story("生成索引文件")
@allure.title("测试生成主目录索引文件")
def test_generate_index_file_main_init(tmp_path):
    output_dir = str(tmp_path / "api")
    generator = APIGenerator(output_dir=output_dir)

    service_dir = os.path.join(output_dir, "test_service")
    os.makedirs(service_dir, exist_ok=True)
    test_file = os.path.join(service_dir, "api_test.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# test")

    generator.generate_index_file([test_file])

    main_init = os.path.join(output_dir, "__init__.py")
    assert os.path.exists(main_init)


@allure.feature("API 生成器")
@allure.story("生成索引文件")
@allure.title("测试重复导入不会重复添加")
def test_generate_index_file_duplicate_no_append(tmp_path):
    output_dir = str(tmp_path / "api")
    generator = APIGenerator(output_dir=output_dir)

    service_dir = os.path.join(output_dir, "test_service")
    os.makedirs(service_dir, exist_ok=True)
    test_file = os.path.join(service_dir, "api_test.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# test")

    generator.generate_index_file([test_file])
    generator.generate_index_file([test_file])

    init_file = os.path.join(service_dir, "__init__.py")
    with open(init_file, encoding="utf-8") as f:
        content = f.read()
    assert content.count("from .api_test import api_test") == 1


# ==================== 统一客户端模式测试 ====================


@allure.feature("API 生成器")
@allure.story("统一客户端模式")
@allure.title("测试统一模式始终生成 client 导入，不区分同步/异步")
def test_unified_mode_generate_imports(generator):
    parsed_info = ParsedRequestInfo(is_file_upload=False, is_need_urlencode=False)
    imports = generator._generate_imports(parsed_info)
    assert "import os" in imports
    assert "from har2pytest.client import client" in imports
    assert "async_client" not in "".join(imports)


@allure.feature("API 生成器")
@allure.story("统一客户端模式")
@allure.title("测试文件上传导入 client 和 build_multipart_data，运行时自动适配同步/异步")
def test_unified_mode_file_upload_imports(generator):
    parsed_info = ParsedRequestInfo(is_file_upload=True, is_need_urlencode=False)
    imports = generator._generate_imports(parsed_info)
    assert "from har2pytest.client import client, build_multipart_data" in imports


@allure.feature("API 生成器")
@allure.story("统一客户端模式")
@allure.title("测试文件上传代码调用 build_multipart_data 自动适配同步/异步客户端")
def test_unified_mode_handle_file_upload(generator):
    post_data = {"file": "(binary)", "description": "test file"}
    result = generator._handle_file_upload(post_data)
    content = "\n".join(result)
    assert "build_multipart_data" in content


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试urlencoded空body接口生成data占位")
@allure.description(
    "content-length=0 的空 body POST 接口（HAR 无参数）应生成 data = {} 占位，"
    "保证 data = urlencode(data) 不会引用未定义变量（修复 UnboundLocalError）。"
)
def test_process_parameters_urlencoded_empty_body_placeholder(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        path_params={},
        query_params={},
        post_data=None,
        is_file_upload=False,
        is_need_urlencode=True,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    result = generator._process_parameters(parsed_info)
    content = "\n".join(result)
    assert "data = {}" in content
    assert "content-type" in content


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试urlencoded空body接口生成data参数与urlencode分支")
def test_generate_function_definition_urlencoded_empty_body(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        url="/api/empty",
        query_params={},
        post_data=None,
        is_file_upload=False,
        is_need_urlencode=True,
        path_params={},
        url_pattern="/api/empty",
        headers={},
    )
    # swagger 参数说明（如 Authorization）不应污染 param_name，也不应丢失
    swagger_info = SwaggerInfo(parameters={"Authorization": "令牌"})
    result = generator._generate_function_definition(parsed_info, "api_empty", swagger_info)
    content = "\n".join(result)
    assert "def api_empty(data=data, headers=headers)" in content
    assert "data = urlencode(data)" in content
    assert "- Authorization: 令牌" in content


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试swagger参数说明不污染无body接口的param_name")
@allure.description(
    "回归测试：docstring 参数说明循环不应覆盖 param_name，否则无 body 接口会误走 data 分支生成引用未定义变量的坏代码。"
)
def test_generate_function_definition_swagger_params_no_leak(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        url="/api/noop",
        query_params={},
        post_data=None,
        is_file_upload=False,
        is_need_urlencode=False,
        path_params={},
        url_pattern="/api/noop",
        headers={},
    )
    swagger_info = SwaggerInfo(parameters={"Authorization": "令牌"})
    result = generator._generate_function_definition(parsed_info, "api_noop", swagger_info)
    content = "\n".join(result)
    # 无 body 接口不应有 data 参数和 data 相关代码
    assert "def api_noop(headers=headers)" in content
    assert "client.post(url=url, headers=headers)" in content
    assert "urlencode(data)" not in content


# ==================== 参数确定逻辑测试 ====================


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试POST空body带query参数时参数并入data")
@allure.description(
    "POST 接口 body 为空 JSON（{}）但 URL 带 query 参数（如 ?orderNo=xxx）时，"
    "参数应并入 data 生成，避免函数签名和调用完全丢失参数。"
)
def test_determine_param_info_post_empty_body_with_query(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        url="/mobile/web/order/as/upgradeOrderVerify",
        query_params={"orderNo": "SG014000260817001801"},
        post_data={},
        is_need_urlencode=True,
        headers={"content-type": "application/json"},
    )
    param_name, param_data = generator._determine_param_info(parsed_info)
    assert param_name == "data"
    assert param_data == {"orderNo": "SG014000260817001801"}


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试POST空body带query参数时生成urlencode传参")
@allure.description(
    "POST 接口 body 为空 JSON（{}）但 URL 带 query 参数时，应生成 data 参数、urlencode 编码"
    "和 client.post(data=data) 调用（application/x-www-form-urlencoded 传参）。"
)
def test_generate_function_definition_post_query_as_data(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        url="/mobile/web/order/as/upgradeOrderVerify",
        query_params={"orderNo": "SG014000260817001801"},
        post_data={},
        is_file_upload=False,
        is_need_urlencode=True,
        is_json_content=False,
        path_params={},
        url_pattern="/mobile/web/order/as/upgradeOrderVerify",
        headers={"content-type": "application/json"},
    )
    swagger_info = SwaggerInfo(parameters={"orderNo": "orderNo"})
    # 端到端验证：文件内容 = 参数定义(_process_parameters) + 函数定义(_generate_function_definition)
    content = generator.generate_file_content(parsed_info, "api_verify", swagger_info, parsed_info)
    assert "def api_verify(data=data, headers=headers)" in content
    assert '"orderNo": "SG014000260817001801"' in content
    assert "from urllib.parse import urlencode" in content
    assert "data = urlencode(data) # application/x-www-form-urlencoded传参需要特殊处理" in content
    assert "client.post(url=url, data=data, headers=headers)" in content


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试POST body与query参数合并")
@allure.description(
    "POST 接口 body 为 dict 且 URL 带 query 参数时，两者应合并进 data（post 覆盖同名 query），避免 URL query 参数丢失。"
)
def test_determine_param_info_post_merge_body_and_query(generator):
    parsed_info = ParsedRequestInfo(
        method="POST",
        url="/api/create",
        query_params={"source": "pc", "page": "1"},
        post_data={"name": "test"},
        headers={},
    )
    param_name, param_data = generator._determine_param_info(parsed_info)
    assert param_name == "data"
    assert param_data == {"source": "pc", "page": "1", "name": "test"}


# ==================== 端到端生成测试 ====================


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 generate_api_file 写入 .py 与 API 元数据 .api.json")
def test_generate_api_file_writes_sidecar(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="GET",
        url="/api/hello",
        query_params={"id": 1},
        post_data={},
        headers={},
    )

    filepath = asyncio.run(generator.generate_api_file(request_info))

    assert filepath is not None
    assert os.path.isfile(filepath)
    assert filepath.endswith("api_hello.py")

    sidecar = filepath[: -len(".py")] + ".api.json"
    assert os.path.isfile(sidecar)
    with open(sidecar, encoding="utf-8") as f:
        data = json.load(f)
    assert data["url"] == "/api/hello"
    assert data["method"] == "GET"
    assert data["function_name"] == "api_hello"
    # 当前值字段随生成固化：GET query 参数进入 params，headers 一并快照
    assert data["params"] == {"id": 1}
    assert isinstance(data.get("headers"), dict)


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试同路径多方法按方法后缀生成不同文件（首个用原名，其余加后缀并告警）")
def test_generate_apis_from_swagger_same_path_multi_method(tmp_path, monkeypatch, caplog, use_test_config):
    output_dir = tmp_path / "apis"
    generator = APIGenerator(output_dir=str(output_dir))
    doc = {
        "swagger": "2.0",
        "basePath": "/member",
        "paths": {
            "/purchaseExchangeOrder/returnInfo": {
                "get": {"summary": "退货信息", "parameters": [], "responses": {}},
                "post": {"summary": "提交退货信息", "parameters": [], "responses": {}},
            },
            "/role": {
                "post": {"summary": "新增角色", "parameters": [], "responses": {}},
                "put": {"summary": "更新角色", "parameters": [], "responses": {}},
                # HEAD 不在支持范围内，应被跳过而不是报错
                "head": {"summary": "探测", "parameters": [], "responses": {}},
            },
        },
    }

    async def fake_get_swagger_doc(url):
        return doc

    monkeypatch.setattr(generator.swagger_handler, "get_swagger_doc", fake_get_swagger_doc)
    with caplog.at_level(logging.INFO):
        files = asyncio.run(
            generator.generate_apis_from_swagger("https://example.com/member/doc.html", force_overwrite=True, service_package="order_application")
        )

    names = sorted(os.path.basename(f) for f in files)
    assert names == [
        "member_purchaseExchangeOrder_returnInfo.py",
        "member_purchaseExchangeOrder_returnInfo_post.py",
        "member_role.py",
        "member_role_put.py",
    ]
    # 首个 method 用原名，内容确定（GET/POST）
    with open(output_dir / "order_application" / "member_purchaseExchangeOrder_returnInfo.py", encoding="utf-8") as f:
        plain = f.read()
    assert "client.get(" in plain
    with open(output_dir / "order_application" / "member_purchaseExchangeOrder_returnInfo_post.py", encoding="utf-8") as f:
        suffixed = f.read()
    assert "client.post(" in suffixed
    with open(output_dir / "order_application" / "member_role_put.py", encoding="utf-8") as f:
        put_content = f.read()
    assert "client.put(" in put_content
    assert any("改用方法后缀生成" in record.getMessage() for record in caplog.records)
    assert any("跳过不支持的HTTP方法: HEAD" in record.getMessage() for record in caplog.records)


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试裸类型Body参数不丢失且不误走urlencode")
def test_generate_apis_from_swagger_bare_type_body(tmp_path, monkeypatch):
    output_dir = tmp_path / "apis"
    generator = APIGenerator(output_dir=str(output_dir))
    doc = {
        "swagger": "2.0",
        "paths": {
            "/mgmt/order/cancelOrder": {
                "post": {
                    "summary": "取消订单",
                    "parameters": [
                        {"name": "orderNo", "in": "body", "description": "订单号", "schema": {"type": "string"}},
                        {"name": "remarks", "in": "query", "type": "string", "description": "备注"},
                    ],
                }
            }
        },
    }

    async def fake_get_swagger_doc(url):
        return doc

    monkeypatch.setattr(generator.swagger_handler, "get_swagger_doc", fake_get_swagger_doc)
    files = asyncio.run(
        generator.generate_apis_from_swagger("https://example.com/member/doc.html", force_overwrite=True, service_package="member")
    )

    assert len(files) == 1
    filepath = files[0]
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    # 裸类型 body 参数 orderNo 不得丢失，且不得误判为 urlencode
    assert '"orderNo": ""' in content
    assert "urlencode" not in content
    assert "client.post(url=url, json=data" in content
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["data"] == {"remarks": "", "orderNo": ""}
    assert meta["param_remarks"] == {"orderNo": "订单号", "remarks": "备注"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 PUT 请求生成 client.put 调用与元数据")
def test_generate_api_file_put_method(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="PUT",
        url="/role",
        query_params={},
        post_data={"name": "管理员"},
        headers={"content-type": "application/json"},
    )

    filepath = asyncio.run(generator.generate_api_file(request_info))

    assert filepath is not None
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    assert "client.put(" in content
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        data = json.load(f)
    assert data["method"] == "PUT"
    assert data["data"] == {"name": "管理员"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 HAR 场景 POST body 接口 har_params 记录 data 实际值")
def test_generate_api_file_har_post_body_har_params(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="POST",
        url="/mgmt/order/cancelOrder",
        query_params={"remarks": "111"},
        post_data={"orderNo": "SG002000260616000137"},
        headers={"content-type": "application/json"},
    )

    filepath = asyncio.run(
        generator.generate_api_file(
            request_info,
            constant_params={"orderNo": "SG002000260616000137"},
        )
    )

    assert filepath is not None
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    # POST 的实际请求参数落在 data（query 先、body 覆盖同名），har_params 应记录该基线
    assert meta["har_params"] == {"remarks": "111", "orderNo": "SG002000260616000137"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 HAR 场景 GET 接口 har_params 记录 params 实际值")
def test_generate_api_file_har_get_har_params(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="GET",
        url="/seckill/product/api/getStockInfo",
        query_params={"serialNo": "TS001"},
    )

    filepath = asyncio.run(
        generator.generate_api_file(
            request_info,
            constant_params={"serialNo": "TS001"},
        )
    )

    assert filepath is not None
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["har_params"] == {"serialNo": "TS001"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 HAR 场景 POST body 带路径参数时 har_params 合并两键")
def test_generate_api_file_har_post_body_with_path_har_params(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="POST",
        url="/mgmt/order/orderInfo/SG002",
        post_data={"remarks": "111"},
        headers={"content-type": "application/json"},
        path_params={"orderNo": "SG002"},
    )
    # 自包含 swagger_info：避免依赖真实 Swagger 文档（删除后 URL 模板匹配
    # 无法提取路径参数，导致 har_params 合并断言受环境耦合影响）
    swagger_info = SwaggerInfo(
        parameters={"remarks": "备注", "orderNo": "订单号"},
        param_defaults={"remarks": "", "orderNo": ""},
    )

    filepath = asyncio.run(
        generator.generate_api_file(
            request_info,
            swagger_info=swagger_info,
            constant_params={"remarks": "111"},
        )
    )

    assert filepath is not None
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    # POST + 路径参数时 params（路径实际值）与 data（body 实际值）两键并存，合并收录
    assert meta["har_params"] == {"orderNo": "SG002", "remarks": "111"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 HAR 场景 har_params 补齐 har_param_values 中缺失的单参数键")
def test_generate_api_file_har_params_backfill_missing_keys(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="GET",
        url="/mgmt/order/orderList",
        query_params={"header": "1", "pageNum": "1"},
    )
    swagger_info = SwaggerInfo(
        parameters={"header": "表头", "orderNo": "订单号"},
        param_defaults={"header": "", "orderNo": ""},
    )

    filepath = asyncio.run(
        generator.generate_api_file(
            request_info,
            swagger_info=swagger_info,
            constant_params={"header": "1"},
            har_param_values={"orderNo": ["GH001"], "header,orderTypes": [["1", "2"]]},
        )
    )

    assert filepath is not None
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    # orderNo 不在首条请求基线（query_params），应补齐 ""；组合键不补
    assert meta["har_params"] == {"header": "1", "pageNum": "1", "orderNo": ""}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 HAR 场景从参数基线配对时间对写入 har_time_pairs")
def test_generate_api_file_har_time_pairs(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="GET",
        url="/mgmt/order/orderList",
        query_params={"pageNum": "1", "commitStartTime": "2026-06-01", "commitEndTime": "2026-06-30"},
    )
    swagger_info = SwaggerInfo(
        parameters={"pageNum": "页码", "commitStartTime": "提交开始时间", "commitEndTime": "提交结束时间"},
        param_defaults={"pageNum": "", "commitStartTime": "", "commitEndTime": ""},
    )

    filepath = asyncio.run(
        generator.generate_api_file(
            request_info,
            swagger_info=swagger_info,
            constant_params={"pageNum": "1"},
        )
    )

    assert filepath is not None
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    # 无 Swagger 备注可提取格式，默认 %Y-%m-%d；按基础名 commit 配对 start/end
    assert meta["har_time_pairs"] == {
        "commit": {"start": "commitStartTime", "end": "commitEndTime", "format": "%Y-%m-%d"},
    }


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试非 HAR 场景不写 har_params 字段")
def test_generate_api_file_non_har_no_har_params(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="GET",
        url="/mgmt/order/orderList",
        query_params={"pageNum": 1},
    )

    filepath = asyncio.run(generator.generate_api_file(request_info))

    assert filepath is not None
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    assert "har_params" not in meta


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 paths 已含 basePath 时不重复拼接（springfox basePath=/member 且 paths=/member/xxx）")
def test_generate_apis_from_swagger_basepath_not_duplicated(tmp_path, monkeypatch, use_test_config):
    output_dir = tmp_path / "apis"
    generator = APIGenerator(output_dir=str(output_dir))
    doc = {
        "swagger": "2.0",
        "basePath": "/member",
        "paths": {
            "/member/activity/ActivityWithOutEnding": {
                "get": {"summary": "查看所有活动", "parameters": [], "responses": {}},
            }
        },
    }

    async def fake_get_swagger_doc(url):
        return doc

    monkeypatch.setattr(generator.swagger_handler, "get_swagger_doc", fake_get_swagger_doc)
    files = asyncio.run(generator.generate_apis_from_swagger("https://example.com/member/doc.html", force_overwrite=True, service_package="member"))

    assert len(files) == 1
    with open(files[0], encoding="utf-8") as f:
        content = f.read()
    assert 'url = "/member/activity/ActivityWithOutEnding"' in content
    assert "/member/member/" not in content
    # 文件名同理不带重复前缀
    assert os.path.basename(files[0]) == "member_activity_ActivityWithOutEnding.py"


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 --path 指定含 basePath 的路径也能命中")
def test_generate_apis_from_swagger_specific_path_with_basepath(tmp_path, monkeypatch, use_test_config):
    output_dir = tmp_path / "apis"
    generator = APIGenerator(output_dir=str(output_dir))
    doc = {
        "swagger": "2.0",
        "basePath": "/member",
        "paths": {
            "/member/comm/coupon": {"get": {"summary": "优惠券列表", "parameters": [], "responses": {}}},
            "/member/activity/activity": {"get": {"summary": "活动列表", "parameters": [], "responses": {}}},
        },
    }

    async def fake_get_swagger_doc(url):
        return doc

    monkeypatch.setattr(generator.swagger_handler, "get_swagger_doc", fake_get_swagger_doc)
    files = asyncio.run(
        generator.generate_apis_from_swagger(
            "https://example.com/member/doc.html", force_overwrite=True, specific_path="/member/comm/coupon", service_package="member"
        )
    )

    assert len(files) == 1
    assert os.path.basename(files[0]) == "member_comm_coupon.py"


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 PATCH 请求生成 client.patch 调用与元数据")
def test_generate_api_file_patch_method(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="PATCH",
        url="/api/resource",
        query_params={},
        post_data={"update": "value"},
        headers={"content-type": "application/json"},
    )

    filepath = asyncio.run(generator.generate_api_file(request_info))

    assert filepath is not None
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    assert "client.patch(" in content
    assert "json=data" in content
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["method"] == "PATCH"
    assert meta["data"] == {"update": "value"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 generate_api_file 文件上传端到端生成")
def test_generate_api_file_upload_e2e(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="POST",
        url="/api/storage/upload",
        query_params={},
        post_data={"storageType": "PublicCloud", "file": "(binary)"},
        headers={"content-type": "multipart/form-data"},
    )

    filepath = asyncio.run(generator.generate_api_file(request_info))

    assert filepath is not None
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    assert "build_multipart_data" in content
    assert "from har2pytest.client import client, build_multipart_data" in content
    assert "client.post(" in content
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["method"] == "POST"
    assert meta["files"] == {"storageType": "PublicCloud", "file": "(binary)"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 generate_api_file urlencoded 端到端生成")
def test_generate_api_file_urlencoded_e2e(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    request_info = ParsedRequestInfo(
        method="POST",
        url="/api/submit",
        query_params={"key": "value"},
        post_data={},
        headers={"content-length": "0"},
    )

    filepath = asyncio.run(generator.generate_api_file(request_info))

    assert filepath is not None
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    assert "from urllib.parse import urlencode" in content
    assert "data = urlencode(data)" in content
    assert "client.post(url=url, data=data, headers=headers)" in content
    with open(filepath[: -len(".py")] + ".api.json", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["method"] == "POST"
    assert meta["data"] == {"key": "value"}


@allure.feature("API 生成器")
@allure.story("端到端生成")
@allure.title("测试 generate_apis_from_swagger 无 paths 空文档返回空列表")
def test_generate_apis_from_swagger_empty_doc(tmp_path, monkeypatch):
    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    doc = {"swagger": "2.0", "basePath": "/api"}

    async def fake_get_swagger_doc(url):
        return doc

    monkeypatch.setattr(generator.swagger_handler, "get_swagger_doc", fake_get_swagger_doc)
    files = asyncio.run(generator.generate_apis_from_swagger("https://example.com/doc.html", force_overwrite=True))

    assert files == []


# ==================== 静态方法与辅助函数测试 ====================


@allure.feature("API 生成器")
@allure.story("静态方法")
@allure.title("测试 _build_full_path 拼接与去重逻辑")
@pytest.mark.parametrize(
    "path,base_path,expected",
    [
        ("/role", "/api", "/api/role"),
        ("/api/role", "/api", "/api/role"),
        ("/role", "", "/role"),
        ("/role", "/", "/role"),
    ],
)
def test_build_full_path(generator, path, base_path, expected):
    assert APIGenerator._build_full_path(path, base_path) == expected


@allure.feature("API 生成器")
@allure.story("处理文件上传")
@allure.title("测试 _handle_multipart_form 无文件上传的 multipart 表单")
def test_handle_multipart_form(generator):
    result = generator._handle_multipart_form()
    content = "\n".join(result)
    assert "data" in content


@allure.feature("API 生成器")
@allure.story("处理参数")
@allure.title("测试 _module_value_snapshot 参数快照")
def test_module_value_snapshot(generator):
    parsed_info = ParsedRequestInfo(
        method="GET",
        url="/api/test",
        query_params={"id": 1},
        post_data={},
        headers={"Authorization": "Bearer token"},
    )
    snapshot = generator._module_value_snapshot(parsed_info)
    assert snapshot["params"] == {"id": 1}
    assert "headers" in snapshot


@allure.feature("API 生成器")
@allure.story("生成函数定义")
@allure.title("测试 _docstring_first_line 缺省返回 TODO 占位")
def test_docstring_first_line_default(generator):
    swagger_info = SwaggerInfo()
    result = generator._docstring_first_line(swagger_info)
    assert result == "TODO: 添加接口描述"
