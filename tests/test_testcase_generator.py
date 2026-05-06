"""
测试 testcase_generator.py 模块
"""

import os

import allure

from har2pytest.testcase_generator import TestCaseGenerator


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
        generator = TestCaseGenerator()
        function_name = generator.get_function_name_from_api_file("_user_login.py")
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
    request_info = {"method": "POST", "post_data": {"username": "test", "password": "123456"}}
    params = generator.extract_params_from_har_request(request_info)
    assert params == {"username": "test", "password": "123456"}

    # 测试POST请求带query_params
    request_info = {"method": "POST", "query_params": {"page": 1, "size": 10}}
    params = generator.extract_params_from_har_request(request_info)
    assert params == {"page": 1, "size": 10}

    # 测试GET请求带query_params
    request_info = {"method": "GET", "query_params": {"id": 123}}
    params = generator.extract_params_from_har_request(request_info)
    assert params == {"id": 123}

    # 测试无参数的情况
    request_info = {"method": "GET"}
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
        generator = TestCaseGenerator()
        remarks = generator.get_param_remarks_from_api_file("test_api.py")
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
    generator = TestCaseGenerator()
    remarks = generator.get_param_remarks_from_api_file("nonexistent.py")
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
        generator = TestCaseGenerator()
        remarks = generator.get_param_remarks_from_api_file("invalid_api.py")
        assert remarks == {}
    finally:
        if os.path.exists("invalid_api.py"):
            os.remove("invalid_api.py")
