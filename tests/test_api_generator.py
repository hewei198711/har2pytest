"""测试 api_generator.py 模块 - APIGenerator 类"""

import os

import allure
import pytest

from har2pytest.api_generator import APIGenerator


@allure.feature("API生成器")
@allure.story("初始化")
@allure.title("测试默认输出目录初始化")
def test_init_default_output_dir():
    generator = APIGenerator()
    assert generator.output_dir is not None
    assert generator.swagger_handler is not None
    assert generator.url_matcher is not None


@allure.feature("API生成器")
@allure.story("初始化")
@allure.title("测试自定义输出目录初始化")
def test_init_custom_output_dir(tmp_path):
    custom_dir = str(tmp_path / "custom_api")
    generator = APIGenerator(output_dir=custom_dir)
    assert generator.output_dir == custom_dir


@allure.feature("API生成器")
@allure.story("检查API是否存在")
@allure.title("测试API文件不存在")
def test_check_api_exists_not_found(monkeypatch, tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path))
    assert not generator.check_api_exists("/api/test_endpoint", "test_service")


@allure.feature("API生成器")
@allure.story("检查API是否存在")
@allure.title("测试根目录下API文件存在")
def test_check_api_exists_root_dir(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path))
    func_name = "_api_test_endpoint"
    file_path = os.path.join(str(tmp_path), f"{func_name}.py")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# test")
    assert generator.check_api_exists("/api/test_endpoint", "apis")


@allure.feature("API生成器")
@allure.story("检查API是否存在")
@allure.title("测试服务包目录下API文件存在")
def test_check_api_exists_service_package_dir(tmp_path):
    generator = APIGenerator(output_dir=str(tmp_path))
    func_name = "_api_test_endpoint"
    package_dir = os.path.join(str(tmp_path), "test_service")
    os.makedirs(package_dir, exist_ok=True)
    with open(os.path.join(package_dir, f"{func_name}.py"), "w", encoding="utf-8") as f:
        f.write("# test")
    assert generator.check_api_exists("/api/test_endpoint", "test_service")


@allure.feature("API生成器")
@allure.story("解析请求信息")
@allure.title("测试解析GET请求信息")
def test_parse_request_info_get():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {"id": 1},
        "post_data": {},
        "headers": {"Authorization": "Bearer token"}
    }
    result = generator._parse_request_info(request_info)
    assert result["method"] == "GET"
    assert result["query_params"] == {"id": 1}
    assert "Authorization" in result["headers"]


@allure.feature("API生成器")
@allure.story("解析请求信息")
@allure.title("测试解析POST请求信息")
def test_parse_request_info_post():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "POST",
        "url": "/api/create",
        "query_params": {},
        "post_data": {"name": "test"},
        "headers": {"content-type": "application/json"}
    }
    result = generator._parse_request_info(request_info)
    assert result["method"] == "POST"
    assert result["post_data"] == {"name": "test"}


@allure.feature("API生成器")
@allure.story("解析请求信息")
@allure.title("测试解析文件上传请求信息")
def test_parse_request_info_file_upload():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "POST",
        "url": "/api/upload",
        "query_params": {},
        "post_data": {"file": "@test.txt"},
        "headers": {"content-type": "multipart/form-data"}
    }
    result = generator._parse_request_info(request_info)
    assert result["is_file_upload"] is True

    # 测试 multipart/form-data 但没有实际文件参数 -> 不是文件上传，使用 data=
    request_info2 = {
        "method": "POST",
        "url": "/api/form",
        "query_params": {},
        "post_data": {"orderNo": "SG001", "remarks": "test"},
        "headers": {"content-type": "multipart/form-data"}
    }
    result2 = generator._parse_request_info(request_info2)
    assert result2["is_file_upload"] is False
    assert result2["is_json_content"] is False

    # 测试 HAR 中文件上传的 (binary) 占位符 -> 应是文件上传
    request_info3 = {
        "method": "POST",
        "url": "/api/storage/upload",
        "query_params": {},
        "post_data": {"storageType": "PublicCloud", "clientKey": "mall-center-product", "file": "(binary)"},
        "headers": {"content-type": "multipart/form-data; boundary=----WebKitFormBoundary33zTNLfGBAtCpQkw"}
    }
    result3 = generator._parse_request_info(request_info3)
    assert result3["is_file_upload"] is True
    assert result3["is_json_content"] is False




@allure.feature("API生成器")
@allure.story("解析请求信息")
@allure.title("测试解析urlencoded请求信息")
def test_parse_request_info_urlencoded():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "POST",
        "url": "/api/submit",
        "query_params": {},
        "post_data": {},
        "headers": {"content-length": "0"}
    }
    result = generator._parse_request_info(request_info)
    assert result["is_need_urlencode"] is True


@allure.feature("API生成器")
@allure.story("解析请求信息")
@allure.title("测试请求信息默认补充headers")
def test_parse_request_info_default_headers():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {},
        "post_data": {},
        "headers": {}
    }
    result = generator._parse_request_info(request_info)
    assert len(result["headers"]) > 0


@allure.feature("API生成器")
@allure.story("生成导入语句")
@allure.title("测试生成普通请求的导入语句")
def test_generate_imports_normal():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "is_file_upload": False,
        "is_need_urlencode": False
    }
    imports = generator._generate_imports(parsed_info)
    assert "import os" in imports
    assert "from util.client import client" in imports


@allure.feature("API生成器")
@allure.story("生成导入语句")
@allure.title("测试生成文件上传的导入语句")
def test_generate_imports_file_upload():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "is_file_upload": True,
        "is_need_urlencode": False
    }
    imports = generator._generate_imports(parsed_info)
    assert "from requests_toolbelt import MultipartEncoder" in imports


@allure.feature("API生成器")
@allure.story("生成导入语句")
@allure.title("测试生成urlencoded的导入语句")
def test_generate_imports_urlencoded():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "is_file_upload": False,
        "is_need_urlencode": True
    }
    imports = generator._generate_imports(parsed_info)
    assert "from urllib.parse import urlencode" in imports


@allure.feature("API生成器")
@allure.story("生成参数字符串")
@allure.title("测试生成参数字符串")
def test_generate_params_string():
    generator = APIGenerator(output_dir="test_output")
    params = {"keyword": "TS001", "pageNum": 1}
    result = generator._generate_params_string(params)
    assert "keyword" in result
    assert "pageNum" in result


@allure.feature("API生成器")
@allure.story("生成参数字符串")
@allure.title("测试空参数字典生成")
def test_generate_params_string_empty():
    generator = APIGenerator(output_dir="test_output")
    result = generator._generate_params_string({})
    assert result == "{}"


@allure.feature("API生成器")
@allure.story("生成参数字符串")
@allure.title("测试带Swagger描述的参数字符串")
def test_generate_params_string_with_swagger_info():
    generator = APIGenerator(output_dir="test_output")
    params = {"id": 1}
    swagger_info = {"parameters": {"id": "用户ID"}, "description": "", "summary": ""}
    result = generator._generate_params_string(params, swagger_info)
    assert "id" in result


@allure.feature("API生成器")
@allure.story("处理参数")
@allure.title("测试处理GET请求参数")
def test_process_parameters_get():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "GET",
        "path_params": {},
        "query_params": {"id": 1},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "headers": {"Authorization": "Bearer token"}
    }
    result = generator._process_parameters(parsed_info)
    assert any("params =" in line for line in result)
    assert any("headers =" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理参数")
@allure.title("测试处理POST请求参数")
def test_process_parameters_post():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "POST",
        "path_params": {},
        "query_params": {},
        "post_data": {"name": "test"},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "headers": {"content-type": "application/json"}
    }
    result = generator._process_parameters(parsed_info)
    assert any("data =" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理参数")
@allure.title("测试处理urlencoded POST参数")
def test_process_parameters_urlencoded():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "POST",
        "path_params": {},
        "query_params": {"key": "value"},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": True,
        "headers": {"content-type": "application/x-www-form-urlencoded"}
    }
    result = generator._process_parameters(parsed_info)
    assert any("content-Type" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理参数")
@allure.title("测试处理路径参数")
def test_process_parameters_path_params():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "GET",
        "path_params": {"id": "123"},
        "query_params": {},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "headers": {}
    }
    result = generator._process_parameters(parsed_info)
    assert any("params =" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理GET方法")
def test_handle_http_method_get():
    generator = APIGenerator(output_dir="test_output")
    result = generator._handle_http_method("GET", "params", {}, {"id": 1}, False)
    assert any("client.get" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理无参数GET方法")
def test_handle_http_method_get_no_params():
    generator = APIGenerator(output_dir="test_output")
    result = generator._handle_http_method("GET", None, {}, {}, False)
    assert any("client.get" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理POST JSON方法")
def test_handle_http_method_post_json():
    generator = APIGenerator(output_dir="test_output")
    result = generator._handle_http_method("POST", "data", {}, {}, False, is_json_content=True)
    assert any("json=data" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理POST urlencoded方法")
def test_handle_http_method_post_urlencoded():
    generator = APIGenerator(output_dir="test_output")
    result = generator._handle_http_method("POST", "data", {}, {}, True)
    assert any("urlencode" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理POST data方法（非JSON非urlencode）")
def test_handle_http_method_post_data():
    generator = APIGenerator(output_dir="test_output")
    result = generator._handle_http_method("POST", "data", {}, {}, False, is_json_content=False)
    assert any("data=data" in line for line in result)
    assert not any("json=data" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理无参数POST方法")
def test_handle_http_method_post_no_params():
    generator = APIGenerator(output_dir="test_output")
    result = generator._handle_http_method("POST", None, {}, {}, False)
    assert any("client.post" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理带路径参数的POST方法")
def test_handle_http_method_post_path_params():
    generator = APIGenerator(output_dir="test_output")
    result = generator._handle_http_method("POST", "params", {"id": "1"}, {}, False)
    assert any("client.post" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理HTTP方法")
@allure.title("测试处理不支持的HTTP方法")
def test_handle_http_method_unsupported():
    generator = APIGenerator(output_dir="test_output")
    with pytest.raises(ValueError, match="不支持的HTTP方法"):
        generator._handle_http_method("DELETE", None, {}, {}, False)


@allure.feature("API生成器")
@allure.story("处理文件上传")
@allure.title("测试处理文件上传")
def test_handle_file_upload():
    generator = APIGenerator(output_dir="test_output")
    post_data = {"file": "(binary)", "description": "test file"}
    result = generator._handle_file_upload(post_data)
    assert any("MultipartEncoder" in line for line in result)


@allure.feature("API生成器")
@allure.story("处理文件上传")
@allure.title("测试文件上传缺少file字段")
def test_handle_file_upload_no_file_key():
    generator = APIGenerator(output_dir="test_output")
    with pytest.raises(ValueError, match="未找到文件参数"):
        generator._handle_file_upload({"name": "test"})


@allure.feature("API生成器")
@allure.story("处理文件上传")
@allure.title("测试文件上传参数非字典")
def test_handle_file_upload_not_dict():
    generator = APIGenerator(output_dir="test_output")
    with pytest.raises(ValueError, match="文件上传参数格式错误"):
        generator._handle_file_upload("not a dict")


@allure.feature("API生成器")
@allure.story("生成函数定义")
@allure.title("测试生成GET函数定义")
def test_generate_function_definition_get():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {"id": 1},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "path_params": {},
        "url_pattern": "/api/test",
        "headers": {}
    }
    swagger_info = {"summary": "测试API", "description": "", "parameters": {}}
    result = generator._generate_function_definition(parsed_info, "_api_test", swagger_info)
    assert any("def _api_test" in line for line in result)


@allure.feature("API生成器")
@allure.story("生成函数定义")
@allure.title("测试生成POST函数定义")
def test_generate_function_definition_post():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "POST",
        "url": "/api/create",
        "query_params": {},
        "post_data": {"name": "test"},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "path_params": {},
        "url_pattern": "/api/create",
        "headers": {}
    }
    swagger_info = {"description": "创建接口", "parameters": {}, "summary": ""}
    result = generator._generate_function_definition(parsed_info, "_api_create", swagger_info)
    assert any("def _api_create" in line for line in result)


@allure.feature("API生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带路径参数的函数定义")
def test_generate_function_definition_with_path_params():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "GET",
        "url": "/api/user/123",
        "query_params": {},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "path_params": {"id": "123"},
        "url_pattern": "/api/user/{id}",
        "headers": {}
    }
    swagger_info = {"summary": "用户详情", "description": "", "parameters": {}}
    result = generator._generate_function_definition(parsed_info, "_api_user_detail", swagger_info)
    assert any("url = f" in line for line in result)


@allure.feature("API生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带摘要的函数定义")
def test_generate_function_definition_with_summary():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "path_params": {},
        "url_pattern": "/api/test",
        "headers": {}
    }
    swagger_info = {"summary": "获取用户列表", "description": "", "parameters": {}}
    result = generator._generate_function_definition(parsed_info, "_api_users", swagger_info)
    assert "获取用户列表" in "\n".join(result)


@allure.feature("API生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带描述的函数定义")
def test_generate_function_definition_with_description():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "path_params": {},
        "url_pattern": "/api/test",
        "headers": {}
    }
    swagger_info = {"summary": "", "description": "获取用户信息", "parameters": {}}
    result = generator._generate_function_definition(parsed_info, "_api_users", swagger_info)
    assert "获取用户信息" in "\n".join(result)


@allure.feature("API生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带参数说明的函数定义")
def test_generate_function_definition_with_parameters():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {"id": 1},
        "post_data": {},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "path_params": {},
        "url_pattern": "/api/test",
        "headers": {}
    }
    swagger_info = {"summary": "测试", "description": "", "parameters": {"id": "用户ID"}}
    result = generator._generate_function_definition(parsed_info, "_api_test", swagger_info)
    content = "\n".join(result)
    assert "用户ID" in content


@allure.feature("API生成器")
@allure.story("生成函数定义")
@allure.title("测试生成带参数的函数签名")
def test_generate_function_definition_with_params():
    generator = APIGenerator(output_dir="test_output")
    parsed_info = {
        "method": "POST",
        "url": "/api/create",
        "query_params": {},
        "post_data": {"name": "test"},
        "is_file_upload": False,
        "is_need_urlencode": False,
        "path_params": {},
        "url_pattern": "/api/create",
        "headers": {}
    }
    swagger_info = {"summary": "", "description": "", "parameters": {}}
    result = generator._generate_function_definition(parsed_info, "_api_create", swagger_info)
    content = "\n".join(result)
    assert "def _api_create(data=data, headers=headers)" in content


@allure.feature("API生成器")
@allure.story("生成文件内容")
@allure.title("测试生成GET请求的完整文件内容")
def test_generate_file_content_get():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {"id": 1},
        "post_data": {},
        "headers": {"Authorization": "Bearer token"}
    }
    content = generator.generate_file_content(request_info, "_api_test")
    assert "import os" in content
    assert "def _api_test" in content
    assert "client.get" in content


@allure.feature("API生成器")
@allure.story("生成文件内容")
@allure.title("测试生成POST请求的完整文件内容")
def test_generate_file_content_post():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "POST",
        "url": "/api/create",
        "query_params": {},
        "post_data": {"name": "test"},
        "headers": {"content-type": "application/json"}
    }
    content = generator.generate_file_content(request_info, "_api_create")
    assert "import os" in content
    assert "def _api_create" in content
    assert "client.post" in content


@allure.feature("API生成器")
@allure.story("生成文件内容")
@allure.title("测试带Swagger信息生成文件内容")
def test_generate_file_content_with_swagger_info():
    generator = APIGenerator(output_dir="test_output")
    request_info = {
        "method": "GET",
        "url": "/api/test",
        "query_params": {"id": 1},
        "post_data": {},
        "headers": {}
    }
    swagger_info = {"summary": "获取用户", "description": "", "parameters": {"id": "用户ID"}}
    content = generator.generate_file_content(request_info, "_api_test", swagger_info)
    assert "获取用户" in content


@allure.feature("API生成器")
@allure.story("生成索引文件")
@allure.title("测试生成索引文件")
def test_generate_index_file(tmp_path):
    output_dir = str(tmp_path / "api")
    generator = APIGenerator(output_dir=output_dir)

    service_dir = os.path.join(output_dir, "test_service")
    os.makedirs(service_dir, exist_ok=True)
    test_file = os.path.join(service_dir, "_api_test.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# test")

    generator.generate_index_file([test_file])

    init_file = os.path.join(service_dir, "__init__.py")
    assert os.path.exists(init_file)
    with open(init_file, encoding="utf-8") as f:
        content = f.read()
    assert "from ._api_test import _api_test" in content


@allure.feature("API生成器")
@allure.story("生成索引文件")
@allure.title("测试生成主目录索引文件")
def test_generate_index_file_main_init(tmp_path):
    output_dir = str(tmp_path / "api")
    generator = APIGenerator(output_dir=output_dir)

    service_dir = os.path.join(output_dir, "test_service")
    os.makedirs(service_dir, exist_ok=True)
    test_file = os.path.join(service_dir, "_api_test.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# test")

    generator.generate_index_file([test_file])

    main_init = os.path.join(output_dir, "__init__.py")
    assert os.path.exists(main_init)


@allure.feature("API生成器")
@allure.story("生成索引文件")
@allure.title("测试重复导入不会重复添加")
def test_generate_index_file_duplicate_no_append(tmp_path):
    output_dir = str(tmp_path / "api")
    generator = APIGenerator(output_dir=output_dir)

    service_dir = os.path.join(output_dir, "test_service")
    os.makedirs(service_dir, exist_ok=True)
    test_file = os.path.join(service_dir, "_api_test.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# test")

    generator.generate_index_file([test_file])
    generator.generate_index_file([test_file])

    init_file = os.path.join(service_dir, "__init__.py")
    with open(init_file, encoding="utf-8") as f:
        content = f.read()
    assert content.count("from ._api_test import _api_test") == 1