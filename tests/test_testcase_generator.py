"""
测试 testcase_generator.py 模块
"""

import asyncio
import os

import allure

from har2pytest.config import APIConfig
from har2pytest.testcase_generator import TestCaseGenerator
from har2pytest.utils import format_params_for_python, parse_api_file


@allure.feature("测试用例生成器")
@allure.story("提取函数名")
@allure.title("测试从API文件中提取函数名")
def test_parse_api_file_function_name():
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
        result = parse_api_file("_user_login.py")
        function_name = result["function_name"]
        assert function_name == "_user_login"
    finally:
        if os.path.exists("_user_login.py"):
            os.remove("_user_login.py")


@allure.feature("测试用例生成器")
@allure.story("格式化参数")
@allure.title("测试格式化参数为测试用例中的参数字符串")
def test_format_test_case_params():
    assert format_params_for_python({}) == "{}"

    params = {"keyword": "TS001", "pageNum": 1}
    result = format_params_for_python(params)
    assert "keyword" in result
    assert "TS001" in result
    assert "pageNum" in result
    assert "1" in result


@allure.feature("测试用例生成器")
@allure.story("处理参数到映射")
@allure.title("测试处理参数到映射")
def test_normalize_params_for_parametrization():
    generator = TestCaseGenerator()

    requests_params = [
        {"keyword": "TS001"},
        {"keyword": "TS002"},
        {"keyword": "TS001"},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    assert "keyword" in result[0]
    assert len(result[0]["keyword"]) == 2
    assert "TS001" in result[0]["keyword"]
    assert "TS002" in result[0]["keyword"]

    requests_params = [
        {"startDate": "2026-01-01", "endDate": "2026-01-31"},
        {"startDate": "2026-02-01", "endDate": "2026-02-28"},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    assert any("startDate" in key and "endDate" in key for key in result[0])
    for key in result[0]:
        if "startDate" in key and "endDate" in key:
            assert len(result[0][key]) == 2

    requests_params = [
        {"ids": [1, 2, 3]},
        {"ids": [1, 2, 3]},
        {"ids": [4, 5, 6]},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    assert "ids" in result[0]
    assert len(result[0]["ids"]) == 2

    requests_params = [
        {"orderStatusList": [1, 2], "customerSourceList": [0, 1]},
        {"orderStatusList": [1, 2], "customerSourceList": [0, 1]},
        {"orderStatusList": [3, 4], "customerSourceList": [2, 4]},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    assert any("orderStatusList" in key and "customerSourceList" in key for key in result[0])
    for key in result[0]:
        if "orderStatusList" in key and "customerSourceList" in key:
            assert len(result[0][key]) == 2

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
    assert len(result) == 3

    customer_type_item = next(
        (item for item in result if "customerType" in item and "," not in list(item.keys())[0]), None
    )
    assert customer_type_item is not None
    assert len(customer_type_item["customerType"]) == 4

    creator_card_item = next(
        (item for item in result if "creatorCard" in item and "," not in list(item.keys())[0]), None
    )
    assert creator_card_item is not None
    assert len(creator_card_item["creatorCard"]) == 1

    time_range_item = next(
        (
            item
            for item in result
            if "commitTimeBegin" in list(item.keys())[0] or "commitTimeEnd" in list(item.keys())[0]
        ),
        None,
    )
    assert time_range_item is not None
    param_name = next(iter(time_range_item.keys()))
    assert "commitTimeBegin" in param_name and "commitTimeEnd" in param_name
    assert len(time_range_item[param_name]) == 1


@allure.feature("测试用例生成器")
@allure.story("从URL提取服务包名")
@allure.title("测试从URL中提取服务包名")
def test_extract_service_package_from_url():
    APIConfig.get_config("SERVICE_MAPPING")

    original_service_mapping = APIConfig._config.get("SERVICE_MAPPING", {})
    APIConfig._config["SERVICE_MAPPING"] = {"mobile": "mall_mobile_application", "user": "mall_center_user"}

    try:
        assert APIConfig.determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"
        assert APIConfig.determine_service_package("/user/123/info") == "mall_center_user"
        assert APIConfig.determine_service_package("") == "apis"
    finally:
        APIConfig._config["SERVICE_MAPPING"] = original_service_mapping


@allure.feature("测试用例生成器")
@allure.story("提取参数备注")
@allure.title("测试从API文件中提取参数备注")
def test_parse_api_file_param_remarks():
    test_content = """
# coding:utf-8

data = {
    "username": "test", # 用户名
    "password": "123456" # 密码
}

def _user_login(data=data, access_token=access_token):
    \\\"\\\"\\\"
    用户登录
    /user/login
    \\\"\\\"\\\"
    url = "/user/login"
    headers = {"Authorization": f"bearer {access_token}"}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
"""

    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("test_api.py")
        remarks = result["param_remarks"]
        assert remarks.get("username") == "用户名"
        assert remarks.get("password") == "密码"
    finally:
        if os.path.exists("test_api.py"):
            os.remove("test_api.py")


@allure.feature("测试用例生成器")
@allure.story("匹配API文件")
@allure.title("测试根据HAR文件匹配API文件")
def test_match_api_files_for_har(tmp_path):
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {"url": "/api/user/login", "method": "POST", "headers": []},
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
        api_files = asyncio.run(generator.match_api_files_for_har(str(har_file)))

        assert len(api_files) == 1
        assert "_user_login.py" in api_files[0]
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("匹配API文件-无匹配")
@allure.title("测试HAR文件没有匹配的API文件")
def test_match_api_files_for_har_no_match(tmp_path):
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

    api_dir = tmp_path / "apis"
    api_dir.mkdir()

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir))
        api_files = asyncio.run(generator.match_api_files_for_har(str(har_file)))

        assert len(api_files) == 0
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("生成测试用例内容")
@allure.title("测试生成场景测试用例内容")
def test_generate_scenario_test_content(tmp_path):
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "/api/user/login",
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
        content = generator.generate_scenario_test_content(
            har_file_path=str(har_file),
            api_files=[str(api_file)],
            task_id="test_task",
            target_api_file=str(api_file),
        )

        assert "test_user_login" in content
        assert "user_login" in content
        assert "pytest" in content
        assert "allure" in content
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试用例")
@allure.title("测试生成参数化测试用例")
def test_generate_parametrized_list_testcases(tmp_path):
    import json

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

    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        generated_files = asyncio.run(generator.generate_parametrized_list_testcases(str(har_file), "test_task"))

        assert len(generated_files) == 1
        assert "test_user_list.py" in generated_files[0]
        assert os.path.exists(generated_files[0])
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("生成场景测试用例")
@allure.title("测试生成场景测试用例")
def test_generate_scenario_testcase(tmp_path):
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "/api/user/login",
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

    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        result = asyncio.run(generator.generate_scenario_testcase(
            har_file_path=str(har_file), target_url="/api/user/login", task_id="test_task"
        ))

        assert result is not None
        assert "test_user_login.py" in result
        assert os.path.exists(result)
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("提取参数备注-文件不存在")
@allure.title("测试从不存在的API文件提取参数备注")
def test_parse_api_file_param_remarks_not_found():
    result = parse_api_file("nonexistent.py")
    remarks = result["param_remarks"]
    assert remarks == {}


@allure.feature("测试用例生成器")
@allure.story("提取参数备注-无效内容")
@allure.title("测试从无效内容的API文件提取参数备注")
def test_parse_api_file_param_remarks_invalid():
    test_content = """
# coding:utf-8

def test_func():
    pass
"""
    with open("invalid_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("invalid_api.py")
        remarks = result["param_remarks"]
        assert remarks == {}
    finally:
        if os.path.exists("invalid_api.py"):
            os.remove("invalid_api.py")


@allure.feature("测试用例生成器")
@allure.story("获取清理后的函数名")
@allure.title("测试获取清理后的函数名")
def test_parse_api_file_function_name_clean():
    from har2pytest.utils import parse_api_file

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
        result = parse_api_file("_user_login.py")
        clean_name = result["function_name"].lstrip("_")
        assert clean_name == "user_login"
    finally:
        if os.path.exists("_user_login.py"):
            os.remove("_user_login.py")


@allure.feature("测试用例生成器")
@allure.story("获取清理后的函数名-无函数名")
@allure.title("测试从无函数名的文件获取清理后的函数名")
def test_parse_api_file_function_name_no_function():
    from har2pytest.utils import parse_api_file

    test_content = """
# coding:utf-8

data = {
    "username": "test"
}
"""

    with open("test_no_func.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("test_no_func.py")
        clean_name = result["function_name"].lstrip("_")
        assert clean_name == "test_no_func"
    finally:
        if os.path.exists("test_no_func.py"):
            os.remove("test_no_func.py")


@allure.feature("测试用例生成器")
@allure.story("获取Headers字符串-直接使用parse_api_file")
@allure.title("测试使用parse_api_file获取Headers")
def test_parse_api_file_headers():
    from har2pytest.utils import parse_api_file

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
        result = parse_api_file("_test_api.py")
        headers = result["headers"]
        assert "custom-header" in headers
    finally:
        if os.path.exists("_test_api.py"):
            os.remove("_test_api.py")


@allure.feature("测试用例生成器")
@allure.story("格式化参数-特殊字符")
@allure.title("测试格式化包含特殊字符的参数")
def test_format_test_case_params_special_chars():
    params = {"name": "test<script>", "path": "/api/test"}
    result = format_params_for_python(params)

    assert "name" in result
    assert "path" in result


@allure.feature("测试用例生成器")
@allure.story("格式化参数-空值")
@allure.title("测试格式化空值参数")
def test_format_test_case_params_empty_values():
    params = {"name": "", "value": None}
    result = format_params_for_python(params)

    assert "name" in result
    assert "value" in result