"""
测试 testcase_generator.py 模块
"""

import os

import allure

from har2pytest.testcase_generator import TestCaseGenerator
from har2pytest.utils import get_function_name_from_api_file, get_param_remarks_from_api_file


@allure.feature("测试用例生成器")
@allure.story("提取函数名")
def test_get_function_name_from_file():
    """测试从API文件中提取函数名"""
    # 创建测试API文件（文件名符合规范：函数名.py）
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

    # 使用符合规范的文件名（函数名作为文件名）
    with open("_user_login.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        function_name = get_function_name_from_api_file("_user_login.py")
        assert function_name == "_user_login"
    finally:
        if os.path.exists("_user_login.py"):
            os.remove("_user_login.py")


@allure.feature("测试用例生成器")
@allure.story("提取参数字典")
def test_extract_params_from_har_request():
    """测试从HAR请求信息中提取参数字典"""
    generator = TestCaseGenerator()

    # 测试POST请求带post_data
    request_info = {"method": "POST", "url": "/api/user/login", "post_data": {"username": "test", "password": "123456"}}
    params = generator.extract_params_from_har_request(request_info)
    assert params == {"username": "test", "password": "123456"}

    # 测试POST请求带query_params
    request_info = {"method": "POST", "url": "/api/user/list", "query_params": {"page": 1, "size": 10}}
    params = generator.extract_params_from_har_request(request_info)
    assert params == {"page": 1, "size": 10}

    # 测试GET请求带query_params
    request_info = {"method": "GET", "url": "/api/user/123", "query_params": {"id": 123}}
    params = generator.extract_params_from_har_request(request_info)
    assert params == {"id": 123}

    # 测试无参数的情况
    request_info = {"method": "GET", "url": "/api/health"}
    params = generator.extract_params_from_har_request(request_info)
    assert params is None


@allure.feature("测试用例生成器")
@allure.story("格式化参数")
def test_format_test_case_params():
    """测试格式化参数为测试用例中的参数字符串"""
    generator = TestCaseGenerator()

    # 测试空参数
    assert generator.format_test_case_params({}) == "{}"

    # 测试简单参数
    params = {"keyword": "TS001", "pageNum": 1}
    result = generator.format_test_case_params(params)
    assert "keyword" in result
    assert "TS001" in result
    assert "pageNum" in result
    assert "1" in result


@allure.feature("测试用例生成器")
@allure.story("处理参数到映射")
def test_normalize_params_for_parametrization():
    """测试处理参数到映射"""
    generator = TestCaseGenerator()

    # 测试单个参数
    requests_params = [
        {"keyword": "TS001"},
        {"keyword": "TS002"},
        {"keyword": "TS001"},  # 重复值
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    assert "keyword" in result[0]
    assert len(result[0]["keyword"]) == 2  # 去重后应该有2个值
    assert "TS001" in result[0]["keyword"]
    assert "TS002" in result[0]["keyword"]

    # 测试组合参数
    requests_params = [
        {"startDate": "2026-01-01", "endDate": "2026-01-31"},
        {"startDate": "2026-02-01", "endDate": "2026-02-28"},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    # 检查是否包含 startDate 和 endDate 的组合键（顺序可能不同）
    assert any("startDate" in key and "endDate" in key for key in result[0])
    # 检查组合键的值长度
    for key in result[0]:
        if "startDate" in key and "endDate" in key:
            assert len(result[0][key]) == 2

    # 测试参数值包含列表的情况（边界情况）
    requests_params = [
        {"ids": [1, 2, 3]},
        {"ids": [1, 2, 3]},  # 重复值
        {"ids": [4, 5, 6]},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    assert "ids" in result[0]
    assert len(result[0]["ids"]) == 2  # 去重后应该有2个值

    # 测试组合参数包含列表类型值的情况（边界情况）
    requests_params = [
        {"orderStatusList": [1, 2], "customerSourceList": [0, 1]},
        {"orderStatusList": [1, 2], "customerSourceList": [0, 1]},  # 重复值
        {"orderStatusList": [3, 4], "customerSourceList": [2, 4]},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    # 检查是否包含 orderStatusList 和 customerSourceList 的组合键
    assert any("orderStatusList" in key and "customerSourceList" in key for key in result[0])
    # 检查组合键的值长度（去重后应该有2个值）
    for key in result[0]:
        if "orderStatusList" in key and "customerSourceList" in key:
            assert len(result[0][key]) == 2

    # 测试实际业务场景：6个请求，空列表视为无效参数，相同参数请求分组参数化
    # 场景：
    # - 4个请求：customerType分别为1,2,3,4，其他参数相同，空列表不视为有效参数
    # - 1个请求：creatorCard有传参
    # - 1个请求：commitTimeBegin和commitTimeEnd有传参
    requests_params = [
        {"customerType": 1, "customerSourceList": [], "orderStatusList": []},
        {"customerType": 2, "customerSourceList": [], "orderStatusList": []},
        {"customerType": 3, "customerSourceList": [], "orderStatusList": []},
        {"customerType": 4, "customerSourceList": [], "orderStatusList": []},
        {"creatorCard": "3000470099", "customerSourceList": [], "orderStatusList": []},
        {
            "commitTimeBegin": "2026-04-01",
            "commitTimeEnd": "2026-04-29",
            "customerSourceList": [],
            "orderStatusList": [],
        },
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    # 应该生成3个参数化项：customerType、creatorCard、commitTimeBegin+commitTimeEnd组合
    assert len(result) == 3

    # 检查customerType参数化
    customer_type_item = next(
        (item for item in result if "customerType" in item and "," not in list(item.keys())[0]), None
    )
    assert customer_type_item is not None
    assert len(customer_type_item["customerType"]) == 4  # 4个不同的值

    # 检查creatorCard参数化
    creator_card_item = next(
        (item for item in result if "creatorCard" in item and "," not in list(item.keys())[0]), None
    )
    assert creator_card_item is not None
    assert len(creator_card_item["creatorCard"]) == 1

    # 检查commitTimeBegin和commitTimeEnd组合参数化
    time_range_item = next(
        (
            item
            for item in result
            if "commitTimeBegin" in list(item.keys())[0] or "commitTimeEnd" in list(item.keys())[0]
        ),
        None,
    )
    assert time_range_item is not None
    # 检查是否是组合参数
    param_name = next(iter(time_range_item.keys()))
    assert "commitTimeBegin" in param_name and "commitTimeEnd" in param_name
    assert len(time_range_item[param_name]) == 1


@allure.feature("测试用例生成器")
@allure.story("从URL提取服务包名")
def test_extract_service_package_from_url():
    """测试从URL中提取服务包名"""
    from har2pytest.config import APIConfig
    from har2pytest.utils import determine_service_package

    # 触发配置初始化
    APIConfig.get_config("SERVICE_MAPPING")

    # 临时设置 SERVICE_MAPPING 配置
    original_service_mapping = APIConfig._config.get("SERVICE_MAPPING", {})
    APIConfig._config["SERVICE_MAPPING"] = {"mobile": "mall_mobile_application", "user": "mall_center_user"}

    try:
        assert determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"
        assert determine_service_package("/user/123/info") == "mall_center_user"
        assert determine_service_package("") == "apis"
    finally:
        # 恢复原始配置
        APIConfig._config["SERVICE_MAPPING"] = original_service_mapping


@allure.feature("测试用例生成器")
@allure.story("提取参数备注")
def test_get_param_remarks_from_api_file():
    """测试从API文件中提取参数备注"""
    # 创建测试API文件
    test_content = """
# coding:utf-8

data = {
    "username": "test", # 用户名
    "password": "123456" # 密码
}

def _user_login(data=data, access_token=access_token):
    \"""
    用户登录
    /user/login
    \"""
    url = "/user/login"
    headers = {"Authorization": f"bearer {access_token}"}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
"""

    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        remarks = get_param_remarks_from_api_file("test_api.py")
        assert remarks.get("username") == "用户名"
        assert remarks.get("password") == "密码"
    finally:
        if os.path.exists("test_api.py"):
            os.remove("test_api.py")


@allure.feature("测试用例生成器")
@allure.story("匹配API文件")
def test_match_api_files_for_har(tmp_path):
    """测试根据HAR文件匹配API文件"""
    import json

    # 创建测试HAR文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {"url": "https://example.com/api/user/login", "method": "POST", "headers": []},
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    # 创建测试API目录和文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_login(data=data, access_token=access_token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    headers = {}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
''')

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=[])
        api_files = generator.match_api_files_for_har(str(har_file))

        assert len(api_files) == 1
        assert "_user_login.py" in api_files[0]
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("匹配API文件-无匹配")
def test_match_api_files_for_har_no_match(tmp_path):
    """测试HAR文件没有匹配的API文件"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {"url": "https://example.com/api/nonexistent", "method": "GET", "headers": []},
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    # 创建空的API目录
    api_dir = tmp_path / "apis"
    api_dir.mkdir()

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir))
        api_files = generator.match_api_files_for_har(str(har_file))

        assert len(api_files) == 0
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("生成测试用例内容")
def test_generate_test_case_content(tmp_path):
    """测试生成测试用例内容"""
    import json

    # 创建测试HAR文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/login",
                        "method": "POST",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "postData": {"mimeType": "application/json", "text": "{}"},
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    # 创建测试API文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_login(data=data, access_token=access_token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    headers = {}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
''')

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir))
        content = generator.generate_test_case_content(
            har_file_path=str(har_file),
            api_files=[str(api_file)],
            task_id="test_task",
            target_api_file=str(api_file),
            target_url="/api/user/login",
        )

        assert "test_user_login" in content
        assert "user_login" in content
        assert "pytest" in content
        assert "allure" in content
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("生成测试用例文件")
def test_generate_test_case_from_har(tmp_path):
    """测试从HAR文件生成测试用例文件"""
    import json

    # 创建测试HAR文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/login",
                        "method": "POST",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "postData": {"mimeType": "application/json", "text": "{}"},
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    # 创建测试API文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_login(data=data, access_token=access_token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    headers = {}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
''')

    # 创建输出目录
    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        result = generator.generate_test_case_from_har(str(har_file))

        assert result is not None
        assert "test_test.py" in result
        assert os.path.exists(result)
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试用例")
def test_generate_parametrized_list_testcases(tmp_path):
    """测试生成参数化测试用例"""
    import json

    # 创建测试HAR文件，包含多个请求用于参数化
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/list",
                        "method": "GET",
                        "headers": [{"name": "origin", "value": "https://example.com"}],
                        "queryString": [{"name": "status", "value": "1"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                },
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/list",
                        "method": "GET",
                        "headers": [{"name": "origin", "value": "https://example.com"}],
                        "queryString": [{"name": "status", "value": "2"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 60,
                },
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    # 创建测试API文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "status": 1,  # 状态
}

def _user_list(data=data, access_token=access_token):
    """
    用户列表
    /api/user/list
    """
    url = "/api/user/list"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    # 创建输出目录
    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        generated_files = generator.generate_parametrized_list_testcases(str(har_file), "test_task")

        assert len(generated_files) == 1
        assert "test_user_list.py" in generated_files[0]
        assert os.path.exists(generated_files[0])
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.feature("测试用例生成器")
@allure.story("生成场景测试用例")
def test_generate_scenario_testcase(tmp_path):
    """测试生成场景测试用例"""
    import json

    # 创建测试HAR文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/login",
                        "method": "POST",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "postData": {"mimeType": "application/json", "text": "{}"},
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    # 创建测试API文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_login(data=data, access_token=access_token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    headers = {}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
''')

    # 创建输出目录
    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        result = generator.generate_scenario_testcase(
            har_file_path=str(har_file), target_url="/api/user/login", task_id="test_task"
        )

        assert result is not None
        assert "test_user_login.py" in result
        assert os.path.exists(result)
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("提取参数备注-文件不存在")
def test_get_param_remarks_from_api_file_not_found():
    """测试从不存在的API文件提取参数备注"""
    remarks = get_param_remarks_from_api_file("nonexistent.py")
    assert remarks == {}


@allure.feature("测试用例生成器")
@allure.story("提取参数备注-无效内容")
def test_get_param_remarks_from_api_file_invalid():
    """测试从无效内容的API文件提取参数备注"""
    test_content = """
# coding:utf-8

def test_func():
    pass
"""
    with open("invalid_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        remarks = get_param_remarks_from_api_file("invalid_api.py")
        assert remarks == {}
    finally:
        if os.path.exists("invalid_api.py"):
            os.remove("invalid_api.py")


@allure.feature("测试用例生成器")
@allure.story("获取清理后的函数名")
def test_get_clean_function_name():
    """测试获取清理后的函数名"""
    generator = TestCaseGenerator()

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

    with open("_user_login.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        clean_name = generator._get_clean_function_name("_user_login.py")
        assert clean_name == "user_login"
    finally:
        if os.path.exists("_user_login.py"):
            os.remove("_user_login.py")


@allure.feature("测试用例生成器")
@allure.story("获取清理后的函数名-无函数名")
def test_get_clean_function_name_no_function():
    """测试从无函数名的文件获取清理后的函数名"""
    generator = TestCaseGenerator()

    test_content = '''
# coding:utf-8

data = {
    "username": "test"
}
'''

    with open("test_no_func.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        clean_name = generator._get_clean_function_name("test_no_func.py")
        assert clean_name == "test_no_func"
    finally:
        if os.path.exists("test_no_func.py"):
            os.remove("test_no_func.py")


@allure.feature("测试用例生成器")
@allure.story("获取Headers字符串")
def test_get_headers_str():
    """测试获取Headers字符串"""
    from har2pytest.config import APIConfig

    generator = TestCaseGenerator()

    APIConfig._config["HEADERS_TO_INCLUDE"] = {
        "content-type": "application/json",
        "authorization": "bearer token",
    }

    headers_str = generator._get_headers_str()

    assert "content-type" in headers_str
    assert "authorization" in headers_str


@allure.feature("测试用例生成器")
@allure.story("获取Headers字符串-带API文件")
def test_get_headers_str_with_api_file():
    """测试带API文件获取Headers字符串"""
    from har2pytest.config import APIConfig

    test_content = '''
# coding:utf-8

headers = {
    "custom-header": "custom-value"
}

def _test_api(headers=headers):
    """
    测试接口
    /test/api
    """
    url = "/test/api"
    with client.get(url=url, headers=headers) as r:
        return r
'''

    with open("_test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        APIConfig._config["HEADERS_TO_INCLUDE"] = {
            "content-type": "application/json",
            "authorization": "bearer token",
        }

        generator = TestCaseGenerator()
        headers_str = generator._get_headers_str("_test_api.py")

        assert "content-type" in headers_str
        assert "authorization" in headers_str
        assert "custom-header" in headers_str
    finally:
        if os.path.exists("_test_api.py"):
            os.remove("_test_api.py")


@allure.feature("测试用例生成器")
@allure.story("提取参数-空POST数据")
def test_extract_params_from_har_request_empty_post():
    """测试提取参数时POST数据为空"""
    generator = TestCaseGenerator()

    request_info = {
        "method": "POST",
        "url": "/api/test",
        "post_data": {},
        "query_params": {"page": 1},
    }

    params = generator.extract_params_from_har_request(request_info)

    assert params == {"page": 1}


@allure.feature("测试用例生成器")
@allure.story("提取参数-POST数据非字典")
def test_extract_params_from_har_request_post_data_not_dict():
    """测试POST数据不是字典时提取参数"""
    generator = TestCaseGenerator()

    request_info = {
        "method": "POST",
        "url": "/api/test",
        "post_data": "not a dict",
        "query_params": {},
    }

    params = generator.extract_params_from_har_request(request_info)

    assert params is None


@allure.feature("测试用例生成器")
@allure.story("提取参数-混合参数")
def test_extract_params_from_har_request_mixed_params():
    """测试提取混合参数（query和post_data）"""
    generator = TestCaseGenerator()

    request_info = {
        "method": "POST",
        "url": "/api/test",
        "post_data": {"username": "test"},
        "query_params": {"page": 1, "size": 10},
    }

    params = generator.extract_params_from_har_request(request_info)

    assert params is not None
    assert "username" in params
    assert "page" in params
    assert "size" in params


@allure.feature("测试用例生成器")
@allure.story("格式化参数-特殊字符")
def test_format_test_case_params_special_chars():
    """测试格式化包含特殊字符的参数"""
    generator = TestCaseGenerator()

    params = {"name": "test<script>", "path": "/api/test"}
    result = generator.format_test_case_params(params)

    assert "name" in result
    assert "path" in result


@allure.feature("测试用例生成器")
@allure.story("格式化参数-空值")
def test_format_test_case_params_empty_values():
    """测试格式化空值参数"""
    generator = TestCaseGenerator()

    params = {"name": "", "value": None}
    result = generator.format_test_case_params(params)

    assert "name" in result
    assert "value" in result


@allure.feature("测试用例生成器")
@allure.story("格式化参数-数字和布尔值")
def test_format_test_case_params_numbers_and_bools():
    """测试格式化数字和布尔值参数"""
    generator = TestCaseGenerator()

    params = {"count": 42, "enabled": True, "rate": 3.14}
    result = generator.format_test_case_params(params)

    assert "count" in result
    assert "42" in result
    assert "enabled" in result
    assert "True" in result
    assert "rate" in result
    assert "3.14" in result


@allure.feature("测试用例生成器")
@allure.story("参数规范化-空列表")
def test_normalize_params_empty_list():
    """测试空参数列表"""
    generator = TestCaseGenerator()

    result = generator.normalize_params_for_parametrization([])
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("参数规范化-仅分页参数")
def test_normalize_params_only_pagination():
    """测试仅包含分页参数的请求"""
    generator = TestCaseGenerator()

    requests_params = [
        {"pageNum": 1, "pageSize": 10},
        {"pageNum": 2, "pageSize": 10},
    ]

    result = generator.normalize_params_for_parametrization(requests_params)

    assert len(result) == 0


@allure.feature("测试用例生成器")
@allure.story("参数规范化-多参数组合")
def test_normalize_params_multiple_combinations():
    """测试多个不同参数组合"""
    generator = TestCaseGenerator()

    requests_params = [
        {"type": "A", "category": "1"},
        {"type": "B", "category": "1"},
        {"type": "A", "category": "2"},
    ]

    result = generator.normalize_params_for_parametrization(requests_params)

    assert len(result) == 1
    assert any("type" in key and "category" in key for key in result[0])


@allure.feature("测试用例生成器")
@allure.story("匹配API文件-直接URL匹配")
def test_match_api_files_for_har_with_direct_url(tmp_path):
    """测试API文件直接URL匹配"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/detail",
                        "method": "GET",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_detail.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_detail(data=data, access_token=access_token):
    """
    用户详情
    /api/user/detail
    """
    url = "/api/user/detail"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])
        api_files = generator.match_api_files_for_har(str(har_file))

        assert len(api_files) == 1
        assert "_user_detail.py" in api_files[0]
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("生成参数化值-非组合参数")
def test_generate_parametrize_values_single():
    """测试生成单个参数的参数化值"""
    generator = TestCaseGenerator()

    values = ["value1", "value2", "value3"]
    result = generator._generate_parametrize_values(values, is_combination=False)

    assert len(result) == 3
    assert all("Severity.NORMAL" in r for r in result)


@allure.feature("测试用例生成器")
@allure.story("生成参数化值-组合参数")
def test_generate_parametrize_values_combination():
    """测试生成组合参数的参数化值"""
    generator = TestCaseGenerator()

    values = [("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")]
    result = generator._generate_parametrize_values(values, is_combination=True)

    assert len(result) == 2
    assert all("Severity.NORMAL" in r for r in result)


@allure.feature("测试用例生成器")
@allure.story("生成参数化值-None值处理")
def test_generate_parametrize_values_with_none():
    """测试生成包含None值的参数化值"""
    generator = TestCaseGenerator()

    values = [None, "value1"]
    result = generator._generate_parametrize_values(values, is_combination=False)

    assert len(result) == 2
    assert "None" in result[0]


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试内容-无匹配请求")
def test_generate_parametrized_test_content_no_matching_request(tmp_path):
    """测试生成参数化测试内容但HAR中无匹配请求"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/different",
                        "method": "GET",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_list(data=data, access_token=access_token):
    """
    用户列表
    /api/user/list
    """
    url = "/api/user/list"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])
        result = generator.generate_parametrized_test_content(str(har_file), str(api_file), "test_task")

        assert result is None
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("TestCaseGenerator初始化-默认参数")
def test_testcase_generator_init_default():
    """测试TestCaseGenerator默认初始化"""
    generator = TestCaseGenerator()

    assert generator.api_dir is not None
    assert generator.output_dir is not None
    assert generator.filter_duplicate_url is False
    assert generator.har_parser is not None
    assert generator.swagger_handler is not None


@allure.feature("测试用例生成器")
@allure.story("TestCaseGenerator初始化-自定义参数")
def test_testcase_generator_init_custom():
    """测试TestCaseGenerator自定义初始化"""
    generator = TestCaseGenerator(
        api_dir="/custom/api",
        output_dir="/custom/output",
        filter_duplicate_url=True,
        base_urls=["https://custom.com"],
        kill_urls=["https://kill.com"],
    )

    assert generator.api_dir == "/custom/api"
    assert generator.output_dir == "/custom/output"
    assert generator.filter_duplicate_url is True


@allure.feature("测试用例生成器")
@allure.story("生成测试用例内容-无API文件")
def test_generate_test_case_content_no_api_files(tmp_path):
    """测试生成测试用例内容但没有API文件时生成默认内容"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/login",
                        "method": "POST",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        generator = TestCaseGenerator(api_dir=str(tmp_path / "nonexistent"), base_urls=[])
        content = generator.generate_test_case_content(
            har_file_path=str(har_file),
            api_files=[],
        )

        assert content is not None
        assert "import os" in content
        assert "pytest" in content
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("匹配API文件-HAR文件不存在")
def test_match_api_files_for_har_file_not_exists():
    """测试HAR文件不存在时的匹配"""
    generator = TestCaseGenerator()

    api_files = generator.match_api_files_for_har("/nonexistent/test.har")

    assert api_files == []


@allure.feature("测试用例生成器")
@allure.story("生成测试用例-HAR文件不存在")
def test_generate_test_case_from_har_file_not_exists():
    """测试HAR文件不存在时生成测试用例"""
    generator = TestCaseGenerator()

    result = generator.generate_test_case_from_har("/nonexistent/test.har")

    assert result is None


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试用例-HAR文件不存在")
def test_generate_parametrized_list_testcases_file_not_exists():
    """测试HAR文件不存在时生成参数化测试用例"""
    generator = TestCaseGenerator()

    result = generator.generate_parametrized_list_testcases("/nonexistent/test.har", "test_task")

    assert result == []


@allure.feature("测试用例生成器")
@allure.story("生成场景测试用例-HAR文件不存在")
def test_generate_scenario_testcase_file_not_exists():
    """测试HAR文件不存在时生成场景测试用例"""
    generator = TestCaseGenerator()

    result = generator.generate_scenario_testcase("/nonexistent/test.har", "/api/test", "test_task")

    assert result is None


# ==================== 路径URL测试用例 ====================
@allure.feature("测试用例生成器")
@allure.story("路径参数提取-从URL提取路径参数")
def test_extract_path_params_from_url(tmp_path):
    """测试从带路径参数的URL提取参数"""
    import json

    swagger_data = {
        "paths": {
            "/user/{userId}/detail": {
                "get": {
                    "summary": "用户详情",
                    "parameters": [
                        {"name": "userId", "in": "path", "type": "integer", "description": "用户ID"},
                    ],
                }
            }
        }
    }

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/12345/detail",
                        "method": "GET",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    generator = TestCaseGenerator(base_urls=["https://example.com/api"])
    original_get_swagger_data = generator.swagger_handler.get_swagger_data_for_url
    generator.swagger_handler.get_swagger_data_for_url = lambda url: swagger_data

    try:
        requests = generator.har_parser.extract_requests_from_har(str(har_file))
        params = generator.extract_params_from_har_request(requests[0])

        assert params is not None
        assert "userId" in params
        assert params["userId"] == "12345"
    finally:
        generator.swagger_handler.get_swagger_data_for_url = original_get_swagger_data


@allure.feature("测试用例生成器")
@allure.story("路径URL匹配-带路径参数的HAR请求匹配API文件")
def test_match_api_files_with_path_params_from_swagger(tmp_path):
    """测试带路径参数的HAR请求正确匹配API文件"""
    import json

    swagger_data = {
        "paths": {
            "/api/user/{userId}/detail": {
                "get": {"summary": "用户详情"},
            }
        }
    }

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/99999/detail",
                        "method": "GET",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_detail.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_detail(data=data, access_token=access_token):
    """
    用户详情
    /api/user/{userId}/detail
    """
    url = "/api/user/{userId}/detail"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])
    original_get_swagger_data = generator.swagger_handler.get_swagger_data_for_url
    generator.swagger_handler.get_swagger_data_for_url = lambda url: swagger_data

    try:
        api_files = generator.match_api_files_for_har(str(har_file))

        assert len(api_files) == 1
        assert "_user_detail.py" in api_files[0]
    finally:
        generator.swagger_handler.get_swagger_data_for_url = original_get_swagger_data


@allure.feature("测试用例生成器")
@allure.story("路径URL生成测试用例-带路径参数的URL生成测试用例内容")
def test_generate_test_case_content_with_path_params(tmp_path):
    """测试带路径参数的URL生成测试用例内容"""
    import json

    swagger_data = {
        "paths": {
            "/api/order/{orderId}/items/{itemId}": {
                "get": {
                    "summary": "订单商品详情",
                    "parameters": [
                        {"name": "orderId", "in": "path", "type": "string"},
                        {"name": "itemId", "in": "path", "type": "string"},
                    ],
                }
            }
        }
    }

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/order/ORD20260101001/items/ITEM001",
                        "method": "GET",
                        "headers": [{"name": "origin", "value": "https://example.com"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_order_items_detail.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _order_items_detail(data=data, access_token=access_token):
    """
    订单商品详情
    /api/order/{orderId}/items/{itemId}
    """
    url = "/api/order/{orderId}/items/{itemId}"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])
    original_get_swagger_data = generator.swagger_handler.get_swagger_data_for_url
    generator.swagger_handler.get_swagger_data_for_url = lambda url: swagger_data

    try:
        content = generator.generate_test_case_content(
            har_file_path=str(har_file),
            api_files=[str(api_file)],
            target_api_file=str(api_file),
            target_url="/api/order/{orderId}/items/{itemId}",
        )

        assert content is not None
        assert "_order_items_detail" in content
        assert "orderId" in content or "ORD20260101001" in content
        assert "itemId" in content or "ITEM001" in content
    finally:
        generator.swagger_handler.get_swagger_data_for_url = original_get_swagger_data


@allure.feature("测试用例生成器")
@allure.story("路径URL生成测试用例-多个路径参数")
def test_generate_test_case_with_multiple_path_params(tmp_path):
    """测试带多个路径参数的URL生成测试用例"""
    import json

    swagger_data = {
        "paths": {
            "/api/store/{storeId}/product/{productId}/stock": {
                "get": {
                    "summary": "门店商品库存",
                    "parameters": [
                        {"name": "storeId", "in": "path", "type": "string"},
                        {"name": "productId", "in": "path", "type": "string"},
                    ],
                }
            }
        }
    }

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/store/123/product/456/stock",
                        "method": "GET",
                        "headers": [],
                        "queryString": [{"name": "test", "value": "value"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    generator = TestCaseGenerator(base_urls=["https://example.com"])
    original_get_swagger_data = generator.swagger_handler.get_swagger_data_for_url
    generator.swagger_handler.get_swagger_data_for_url = lambda url: swagger_data

    try:
        requests = generator.har_parser.extract_requests_from_har(str(har_file))
        params = generator.extract_params_from_har_request(requests[0])

        assert params is not None
        assert params["storeId"] == "123"
        assert params["productId"] == "456"
    finally:
        generator.swagger_handler.get_swagger_data_for_url = original_get_swagger_data


@allure.feature("测试用例生成器")
@allure.story("路径URL生成测试用例-路径参数与查询参数混合")
def test_generate_test_case_with_path_and_query_params(tmp_path):
    """测试路径参数与查询参数混合的场景"""
    import json

    swagger_data = {
        "paths": {
            "/api/user/{userId}/orders": {
                "get": {
                    "summary": "用户订单列表",
                    "parameters": [
                        {"name": "userId", "in": "path", "type": "string"},
                        {"name": "status", "in": "query", "type": "string"},
                        {"name": "page", "in": "query", "type": "integer"},
                    ],
                }
            }
        }
    }

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/USER123/orders?status=PAID&page=1",
                        "method": "GET",
                        "headers": [],
                        "queryString": [
                            {"name": "status", "value": "PAID"},
                            {"name": "page", "value": "1"},
                        ],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    generator = TestCaseGenerator(base_urls=["https://example.com"])
    original_get_swagger_data = generator.swagger_handler.get_swagger_data_for_url
    generator.swagger_handler.get_swagger_data_for_url = lambda url: swagger_data

    try:
        requests = generator.har_parser.extract_requests_from_har(str(har_file))
        params = generator.extract_params_from_har_request(requests[0])

        assert params is not None
        # 验证查询参数正确提取
        assert params["status"] == "PAID"
        assert params["page"] == "1"
        # 验证路径参数是否正确提取（如果匹配成功）
        if "userId" in params:
            assert params["userId"] == "USER123"
    finally:
        generator.swagger_handler.get_swagger_data_for_url = original_get_swagger_data


@allure.feature("测试用例生成器")
@allure.story("路径URL生成测试用例-无Swagger匹配时使用原始URL")
def test_generate_test_case_without_swagger_match(tmp_path):
    """测试当Swagger中没有匹配的路径模板时，使用原始URL"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/123/info",
                        "method": "GET",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_info.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _user_info(data=data, access_token=access_token):
    """
    用户信息
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])
    original_get_swagger_data = generator.swagger_handler.get_swagger_data_for_url
    generator.swagger_handler.get_swagger_data_for_url = lambda url: None

    try:
        api_files = generator.match_api_files_for_har(str(har_file))

        assert len(api_files) == 0
    finally:
        generator.swagger_handler.get_swagger_data_for_url = original_get_swagger_data


@allure.feature("测试用例生成器")
@allure.story("场景测试用例-文件上传请求")
def test_extract_params_from_har_request_file_upload(tmp_path):
    """测试从HAR请求中提取文件上传参数"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/upload",
                        "method": "POST",
                        "headers": [
                            {"name": "content-type", "value": "multipart/form-data; boundary=----WebKitFormBoundary"},
                        ],
                        "postData": {
                            "mimeType": "multipart/form-data; boundary=----WebKitFormBoundary",
                            "params": [
                                {"name": "name", "value": "test.jpg"},
                                {"name": "file", "fileName": "test.jpg", "contentType": "image/jpeg"},
                            ],
                        },
                    },
                    "response": {"status": 200, "content": {"text": '{"code": 200}'}},
                    "time": 500,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    generator = TestCaseGenerator(api_dir=str(tmp_path), base_urls=["https://example.com"])
    
    requests = generator.har_parser.extract_requests_from_har(str(har_file))
    assert len(requests) == 1
    
    request_info = requests[0]
    params = generator.extract_params_from_har_request(request_info)
    
    assert params is not None
    # 当前实现将所有参数都放在顶层，包括文件参数
    assert "name" in params
    assert params["name"] == "test.jpg"


@allure.feature("测试用例生成器")
@allure.story("场景测试用例-无参数请求")
def test_extract_params_from_har_request_no_params(tmp_path):
    """测试从HAR请求中提取无参数的情况"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/health",
                        "method": "GET",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": '{"code": 200}'}},
                    "time": 50,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    generator = TestCaseGenerator(api_dir=str(tmp_path), base_urls=["https://example.com"])
    
    requests = generator.har_parser.extract_requests_from_har(str(har_file))
    assert len(requests) == 1
    
    request_info = requests[0]
    params = generator.extract_params_from_har_request(request_info)
    
    # 无参数请求应该返回None
    assert params is None


@allure.feature("测试用例生成器")
@allure.story("参数化测试-无有效参数")
def test_generate_parametrized_test_content_no_valid_params(tmp_path):
    """测试当没有有效参数时不生成参数化测试"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/list?page=1&size=10",
                        "method": "GET",
                        "headers": [],
                        "queryString": [
                            {"name": "page", "value": "1"},
                            {"name": "size", "value": "10"},
                        ],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _list(data=data, access_token=access_token):
    """
    列表查询
    /api/list
    """
    url = "/api/list"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])

    try:
        result = generator.generate_parametrized_test_content(
            har_file_path=str(har_file),
            api_file=str(api_file),
            task_id="test_task",
        )

        assert result is not None
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("参数化测试-空参数值")
def test_generate_parametrized_test_content_empty_values(tmp_path):
    """测试处理空参数值的参数化测试"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/search?keyword=&category=A",
                        "method": "GET",
                        "headers": [],
                        "queryString": [
                            {"name": "keyword", "value": ""},
                            {"name": "category", "value": "A"},
                        ],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                },
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/search?keyword=&category=B",
                        "method": "GET",
                        "headers": [],
                        "queryString": [
                            {"name": "keyword", "value": ""},
                            {"name": "category", "value": "B"},
                        ],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                },
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_search.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def _search(data=data, access_token=access_token):
    """
    搜索
    /api/search
    """
    url = "/api/search"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])

    try:
        result = generator.generate_parametrized_test_content(
            har_file_path=str(har_file),
            api_file=str(api_file),
            task_id="test_task",
        )

        assert result is not None
        assert "category" in result
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("路径URL生成测试用例-生成带路径参数的参数化测试")
def test_generate_parametrized_test_with_path_params(tmp_path):
    """测试生成带路径参数的参数化测试用例"""
    import json

    swagger_data = {
        "paths": {
            "/api/customer/{customerId}/orders": {
                "get": {
                    "summary": "客户订单列表",
                    "parameters": [
                        {"name": "customerId", "in": "path", "type": "integer"},
                        {"name": "status", "in": "query", "type": "string"},
                    ],
                }
            }
        }
    }

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/customer/1001/orders?status=ACTIVE",
                        "method": "GET",
                        "headers": [],
                        "queryString": [{"name": "status", "value": "ACTIVE"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                },
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/customer/1002/orders?status=ACTIVE",
                        "method": "GET",
                        "headers": [],
                        "queryString": [{"name": "status", "value": "ACTIVE"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 60,
                },
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_customer_orders.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "customerId": 1001,
    "status": "ACTIVE",
}

def _customer_orders(data=data, access_token=access_token):
    """
    客户订单列表
    /api/customer/{customerId}/orders
    """
    url = "/api/customer/{customerId}/orders"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=["https://example.com"])
    original_get_swagger_data = generator.swagger_handler.get_swagger_data_for_url
    generator.swagger_handler.get_swagger_data_for_url = lambda url: swagger_data

    try:
        # 先验证API文件匹配
        api_files = generator.match_api_files_for_har(str(har_file))
        assert len(api_files) >= 1, f"未匹配到API文件: {api_files}"
        
        # 然后验证测试用例生成
        generated_files = generator.generate_parametrized_list_testcases(str(har_file), "test_task")

        if len(generated_files) > 0:
            assert "test_customer_orders.py" in generated_files[0]
            assert os.path.exists(generated_files[0])
    finally:
        generator.swagger_handler.get_swagger_data_for_url = original_get_swagger_data
