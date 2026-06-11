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
def test_parse_api_file_function_name():
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
        result = parse_api_file("_user_login.py")
        function_name = result["function_name"]
        assert function_name == "_user_login"
    finally:
        if os.path.exists("_user_login.py"):
            os.remove("_user_login.py")


@allure.feature("测试用例生成器")
@allure.story("格式化参数")
def test_format_test_case_params():
    """测试格式化参数为测试用例中的参数字符串"""
    # 测试空参数
    assert format_params_for_python({}) == "{}"

    # 测试简单参数
    params = {"keyword": "TS001", "pageNum": 1}
    result = format_params_for_python(params)
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


@allure.feature("测试用例生成器")
@allure.story("提取参数备注")
def test_parse_api_file_param_remarks():
    """测试从API文件中提取参数备注"""
    # 创建测试API文件
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
def test_match_api_files_for_har(tmp_path):
    """测试根据HAR文件匹配API文件"""
    import json

    # 创建测试HAR文件
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
def test_generate_scenario_test_content(tmp_path):
    """测试生成场景测试用例内容"""
    import json

    # 创建测试HAR文件
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
def test_parse_api_file_param_remarks_not_found():
    """测试从不存在的API文件提取参数备注"""
    result = parse_api_file("nonexistent.py")
    remarks = result["param_remarks"]
    assert remarks == {}


@allure.feature("测试用例生成器")
@allure.story("提取参数备注-无效内容")
def test_parse_api_file_param_remarks_invalid():
    """测试从无效内容的API文件提取参数备注"""
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
def test_parse_api_file_function_name_clean():
    """测试获取清理后的函数名"""
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
def test_parse_api_file_function_name_no_function():
    """测试从无函数名的文件获取清理后的函数名"""
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
def test_parse_api_file_headers():
    """测试使用parse_api_file获取Headers"""
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
def test_format_test_case_params_special_chars():
    """测试格式化包含特殊字符的参数"""
    params = {"name": "test<script>", "path": "/api/test"}
    result = format_params_for_python(params)

    assert "name" in result
    assert "path" in result


@allure.feature("测试用例生成器")
@allure.story("格式化参数-空值")
def test_format_test_case_params_empty_values():
    """测试格式化空值参数"""
    params = {"name": "", "value": None}
    result = format_params_for_python(params)

    assert "name" in result
    assert "value" in result


@allure.feature("测试用例生成器")
@allure.story("格式化参数-数字和布尔值")
def test_format_test_case_params_numbers_and_bools():
    """测试格式化数字和布尔值参数"""
    params = {"count": 42, "enabled": True, "rate": 3.14}
    result = format_params_for_python(params)

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
    assert '"value1"' in result
    assert '"value2"' in result
    assert '"value3"' in result


@allure.feature("测试用例生成器")
@allure.story("生成参数化值-组合参数")
def test_generate_parametrize_values_combination():
    """测试生成组合参数的参数化值"""
    generator = TestCaseGenerator()

    values = [("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")]
    result = generator._generate_parametrize_values(values, is_combination=True)

    assert len(result) == 2
    assert '("2026-01-01", "2026-01-31")' in result
    assert '("2026-02-01", "2026-02-28")' in result


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
@allure.story("匹配API文件-HAR文件不存在")
def test_match_api_files_for_har_file_not_exists():
    """测试HAR文件不存在时的匹配"""
    generator = TestCaseGenerator()

    api_files = generator.match_api_files_for_har("/nonexistent/test.har")

    assert api_files == []


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试用例-HAR文件不存在")


@allure.feature("测试用例生成器")
@allure.story("生成场景测试用例-HAR文件不存在")
def test_generate_scenario_testcase_file_not_exists():
    """测试HAR文件不存在时生成场景测试用例"""
    generator = TestCaseGenerator()

    result = generator.generate_scenario_testcase("/nonexistent/test.har", "/api/test", "test_task")

    assert result is None


# ==================== 路径URL测试用例 ====================
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
    original_swagger_doc_urls = APIConfig.SWAGGER_DOC_URLS
    original_default_api_dir = APIConfig.DEFAULT_API_DIR
    APIConfig.SWAGGER_DOC_URLS = lambda: {"mall_center_user": "https://example.com/swagger"}
    APIConfig.DEFAULT_API_DIR = lambda: "apis"
    original_get_swagger_doc = generator.swagger_handler.get_swagger_doc
    async def _mock_get(url): return swagger_data
    generator.swagger_handler.get_swagger_doc = _mock_get

    try:
        api_files = generator.match_api_files_for_har(str(har_file))

        assert len(api_files) == 1
        assert "_user_detail.py" in api_files[0]
    finally:
        APIConfig.SWAGGER_DOC_URLS = original_swagger_doc_urls
        APIConfig.DEFAULT_API_DIR = original_default_api_dir
        generator.swagger_handler.get_swagger_doc = original_get_swagger_doc


@allure.feature("测试用例生成器")
@allure.story("路径URL生成测试用例-带路径参数的URL生成测试用例内容")
def test_generate_scenario_test_content_with_path_params(tmp_path):
    """测试带路径参数的URL生成场景测试用例内容"""
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
    original_swagger_doc_urls = APIConfig.SWAGGER_DOC_URLS
    original_default_api_dir = APIConfig.DEFAULT_API_DIR
    APIConfig.SWAGGER_DOC_URLS = lambda: {"mall_center_user": "https://example.com/swagger"}
    APIConfig.DEFAULT_API_DIR = lambda: "apis"
    original_get_swagger_doc = generator.swagger_handler.get_swagger_doc
    async def _mock_get(url): return swagger_data
    generator.swagger_handler.get_swagger_doc = _mock_get

    try:
        content = generator.generate_scenario_test_content(
            har_file_path=str(har_file),
            api_files=[str(api_file)],
            target_api_file=str(api_file),
        )

        assert content is not None
        assert "_order_items_detail" in content
        assert "orderId" in content or "ORD20260101001" in content
        assert "itemId" in content or "ITEM001" in content
    finally:
        APIConfig.SWAGGER_DOC_URLS = original_swagger_doc_urls
        APIConfig.DEFAULT_API_DIR = original_default_api_dir
        generator.swagger_handler.get_swagger_doc = original_get_swagger_doc


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
    original_swagger_doc_urls = APIConfig.SWAGGER_DOC_URLS
    original_default_api_dir = APIConfig.DEFAULT_API_DIR
    APIConfig.SWAGGER_DOC_URLS = lambda: {"apis": "https://example.com/swagger"}
    APIConfig.DEFAULT_API_DIR = lambda: "apis"
    original_get_swagger_doc = generator.swagger_handler.get_swagger_doc
    async def _mock_get(url): return swagger_data
    generator.swagger_handler.get_swagger_doc = _mock_get

    try:
        requests = generator.har_parser.extract_requests_from_har(str(har_file))
        # 直接合并 query_params 和 post_data
        params = {}
        params.update(requests[0].get("query_params") or {})
        if requests[0].get("post_data"):
            params.update(requests[0]["post_data"])

        assert params is not None
        # 验证查询参数正确提取
        assert params["status"] == "PAID"
        assert params["page"] == "1"
        # 验证路径参数是否正确提取（如果匹配成功）
        if "userId" in params:
            assert params["userId"] == "USER123"
    finally:
        APIConfig.SWAGGER_DOC_URLS = original_swagger_doc_urls
        APIConfig.DEFAULT_API_DIR = original_default_api_dir
        generator.swagger_handler.get_swagger_doc = original_get_swagger_doc


@allure.feature("测试用例生成器")
@allure.story("路径URL生成测试用例-无Swagger匹配时使用原始URL")
def test_generate_test_case_without_swagger_match(tmp_path):
    """测试当Swagger中没有匹配的路径模板时，仍然可以使用路径参数模式匹配"""
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
    original_swagger_doc_urls = APIConfig.SWAGGER_DOC_URLS
    original_default_api_dir = APIConfig.DEFAULT_API_DIR
    APIConfig.SWAGGER_DOC_URLS = lambda: {"apis": "https://example.com/swagger"}
    APIConfig.DEFAULT_API_DIR = lambda: "apis"
    original_get_swagger_doc = generator.swagger_handler.get_swagger_doc
    async def _mock_get_none(url): return None
    generator.swagger_handler.get_swagger_doc = _mock_get_none

    try:
        api_files = generator.match_api_files_for_har(str(har_file))

        # 即使没有Swagger数据，也应该能通过路径参数模式匹配找到API文件
        assert len(api_files) == 1
        assert str(api_file) in api_files[0]
    finally:
        APIConfig.SWAGGER_DOC_URLS = original_swagger_doc_urls
        APIConfig.DEFAULT_API_DIR = original_default_api_dir
        generator.swagger_handler.get_swagger_doc = original_get_swagger_doc


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
    original_swagger_doc_urls = APIConfig.SWAGGER_DOC_URLS
    original_default_api_dir = APIConfig.DEFAULT_API_DIR
    APIConfig.SWAGGER_DOC_URLS = lambda: {"apis": "https://example.com/swagger"}
    APIConfig.DEFAULT_API_DIR = lambda: "apis"
    original_get_swagger_doc = generator.swagger_handler.get_swagger_doc
    async def _mock_get(url): return swagger_data
    generator.swagger_handler.get_swagger_doc = _mock_get

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
        APIConfig.SWAGGER_DOC_URLS = original_swagger_doc_urls
        APIConfig.DEFAULT_API_DIR = original_default_api_dir
        generator.swagger_handler.get_swagger_doc = original_get_swagger_doc



@allure.feature("测试用例生成器")
@allure.story("API目录不存在")
def test_get_all_api_files_dir_not_exists(tmp_path):
    """测试当API目录不存在时_get_all_api_files返回空列表"""
    non_existent_dir = tmp_path / "non_existent_dir"
    generator = TestCaseGenerator(api_dir=str(non_existent_dir))
    result = generator._get_all_api_files()
    assert result == []





@allure.feature("测试用例生成器")
@allure.story("匹配API文件-HAR文件不存在")
def test_match_api_files_for_har_not_exists(tmp_path):
    """测试当HAR文件不存在时返回空列表"""
    generator = TestCaseGenerator()
    non_existent = tmp_path / "non_existent.har"
    result = generator.match_api_files_for_har(str(non_existent))
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("匹配API文件-空HAR文件")
def test_match_api_files_for_har_empty(tmp_path):
    """测试当HAR文件为空时返回空列表"""
    import json
    
    empty_har = {"log": {"entries": []}}
    har_file = tmp_path / "empty.har"
    with open(har_file, "w") as f:
        json.dump(empty_har, f)
    
    generator = TestCaseGenerator()
    result = generator.match_api_files_for_har(str(har_file))
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试用例-文件不存在")
def test_generate_parametrized_list_testcases_file_not_exists(tmp_path):
    """测试当HAR文件不存在时返回空列表"""
    generator = TestCaseGenerator(output_dir=str(tmp_path))
    non_existent = tmp_path / "non_existent.har"
    result = generator.generate_parametrized_list_testcases(str(non_existent), "test_task")
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("解析状态参数")
def test_parse_state_values():
    """测试从参数备注中解析状态值"""
    generator = TestCaseGenerator()

    # 测试中文冒号
    remark = "状态 -1：已驳回 0：待审核（默认）1：审核通过"
    result = generator._parse_state_values(remark)
    assert result == [-1, 0, 1]

    # 测试英文冒号
    remark = "状态 -1:已驳回 0:待审核（默认）1:审核通过"
    result = generator._parse_state_values(remark)
    assert result == [-1, 0, 1]

    # 测试没有状态字段的备注
    remark = "用户ID"
    result = generator._parse_state_values(remark)
    assert result == []

    # 测试空备注
    remark = ""
    result = generator._parse_state_values(remark)
    assert result == []

    # 测试负数状态
    remark = "状态 -2：已删除 -1：已驳回 0：待审核 1：审核通过"
    result = generator._parse_state_values(remark)
    assert result == [-2, -1, 0, 1]


@allure.feature("测试用例生成器")
@allure.story("参数化-状态参数使用HAR原始值")
def test_normalize_params_with_state_param():
    """测试参数化时状态参数使用HAR原始值去重，不解析API备注中的状态枚举。"""
    generator = TestCaseGenerator()

    requests_params = [
        {"status": "0", "pageNum": "1", "pageSize": "10"},
        {"status": "1", "pageNum": "1", "pageSize": "10"},
    ]

    result = generator.normalize_params_for_parametrization(requests_params)

    # parametrized_list 模式使用 HAR 原始值，不展开状态枚举
    assert len(result) == 1
    assert "status" in result[0]
    assert result[0]["status"] == ["0", "1"]
    assert result[0]["other_params"] == {"pageNum": "1", "pageSize": "10"}


# ==================== 三种模式单元测试 ====================


@allure.feature("测试用例生成器")
@allure.story("parametrized_list 模式 - API自定义headers")
def test_parametrized_list_with_custom_headers(tmp_path):
    """测试 parametrized_list 模式使用 API 文件中的自定义 headers。

    验证点：_generate_test_class_setup(api_file) 正确从 API 文件提取自定义 headers。
    """
    import json

    # 创建测试HAR文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/order/list",
                        "method": "GET",
                        "headers": [{"name": "origin", "value": "https://example.com"}],
                        "queryString": [{"name": "status", "value": "1"}],
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

    # 创建带自定义 headers 的 API 文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_order_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

headers = {
    "channel": "mobile",
    "client": "op",
    "platform": "ios",
}

data = {
    "status": 1,  # 状态
}

def _order_list(data=data, access_token=access_token):
    """
    订单列表
    /api/order/list
    """
    url = "/api/order/list"
    headers = {"Authorization": f"bearer {access_token}"}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=["https://example.com"])

    # 生成 parametrized 测试内容
    content = generator.generate_parametrized_test_content(str(har_file), str(api_file), "test_task")

    assert content is not None, "生成内容不应为 None"

    # 验证自定义 headers 出现在输出中（而非默认 headers）
    assert '"channel": "mobile"' in content, "应包含 API 文件中的 channel header"
    assert '"platform": "ios"' in content, "应包含 API 文件中的 platform header"
    # 不应包含默认 headers（pc、authorization）
    assert '"channel": "pc"' not in content, "不应包含默认 channel header"

    # 验证参数化测试方法生成正确
    assert "@pytest.mark.parametrize" in content
    assert "def test_0_order_list(self, status):" in content


@allure.feature("测试用例生成器")
@allure.story("parametrized_list 模式 - HAR无参数时返回None")
def test_parametrized_list_har_no_params_returns_none(tmp_path):
    """测试 parametrized_list 模式，HAR 文件存在但无匹配参数时返回 None。

    验证点：非 batch 模式下，HAR 无参数不会回退到 API 文件读取参数。
    """
    import json

    # 创建 HAR 文件（URL 与 API 文件不匹配）
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/other/endpoint",
                        "method": "GET",
                        "headers": [],
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

    # 创建 API 文件（虽然 API 文件有参数，但 HAR 中没有匹配请求）
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "page": "1",
    "page_size": "20",
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

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])

    # HAR 存在但 URL 不匹配，不应回退到 API 文件参数
    result = generator.generate_parametrized_test_content(str(har_file), str(api_file), "test_task")

    assert result is None, "HAR 无匹配参数时不应回退到 API 文件，应返回 None"


@allure.feature("测试用例生成器")
@allure.story("complex_scenario 模式 - 请求顺序保持")
def test_scenario_preserves_request_order(tmp_path):
    """测试 complex_scenario 模式保持 HAR 请求顺序。

    验证点：步骤函数按照 HAR 中的请求顺序生成。
    """
    import json

    # 创建包含多步骤的 HAR 文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/login",
                        "method": "POST",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "postData": {"mimeType": "application/json", "text": '{"username":"test"}'},
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                },
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/product/list",
                        "method": "GET",
                        "headers": [],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 80,
                },
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/order/create",
                        "method": "POST",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "postData": {"mimeType": "application/json", "text": '{"product_id":"P001"}'},
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 120,
                },
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    # 创建对应的 API 文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_files = []
    for name, url, method in [
        ("_user_login.py", "/api/user/login", "POST"),
        ("_product_list.py", "/api/product/list", "GET"),
        ("_order_create.py", "/api/order/create", "POST"),
    ]:
        api_file = api_dir / name
        with open(api_file, "w", encoding="utf-8") as f:
            f.write(f'''
# coding:utf-8

def {name.replace(".py", "")}(data=data, access_token=access_token):
    """
    {name.replace(".py", "").lstrip("_")}
    {url}
    """
    url = "{url}"
    headers = {{}}
    with client.{method.lower()}(url=url, headers=headers, json=data) as r:
        return r
''')
        api_files.append(str(api_file))

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=["https://example.com"])

    content = generator.generate_scenario_test_content(str(har_file), api_files, "test_task", api_files[0])

    assert content is not None

    # 验证步骤函数顺序 = HAR 请求顺序
    step_login_idx = content.find("def step_user_login():")
    step_list_idx = content.find("def step_product_list():")
    step_create_idx = content.find("def step_order_create():")

    assert step_login_idx != -1, "应生成 user_login 步骤函数"
    assert step_list_idx != -1, "应生成 product_list 步骤函数"
    assert step_create_idx != -1, "应生成 order_create 步骤函数"

    # 验证顺序：login → list → create
    assert step_login_idx < step_list_idx, "login 应在 list 之前"
    assert step_list_idx < step_create_idx, "list 应在 create 之前"

    # 验证步骤调用顺序
    call_section = content[content.find("# 执行所有测试步骤"):]
    call_login = call_section.find("step_user_login()")
    call_list = call_section.find("step_product_list()")
    call_create = call_section.find("step_order_create()")
    assert call_login < call_list < call_create, "步骤调用顺序应与 HAR 请求顺序一致"


@allure.feature("测试用例生成器")
@allure.story("complex_scenario 模式 - 无HAR从API文件生成")
def test_scenario_without_har_from_api_file(tmp_path):
    """测试 complex_scenario 模式无 HAR 文件时从 API 文件构建。

    验证点：_get_requests_from_source 在无 HAR 时正确从 API 文件构建请求信息。
    """
    # 创建 API 文件（包含 params 和 data）
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

params = {
    "from": "mobile",
}

data = {
    "username": "test",
    "password": "123456",
}

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

    generator = TestCaseGenerator(api_dir=str(api_dir))

    # 无 HAR 文件，从 API 文件生成场景测试内容
    content = generator.generate_scenario_test_content(
        har_file_path=None,
        api_files=[str(api_file)],
        task_id="test_task",
        target_api_file=str(api_file),
    )

    assert content is not None
    assert "test_user_login" in content
    assert "step_user_login" in content
    assert "data = " in content or '"username": "test"' in content


@allure.feature("测试用例生成器")
@allure.story("batch 模式 - 列表接口参数化生成")
def test_batch_list_mode(tmp_path):
    """测试 batch 模式生成列表查询参数化测试。

    验证点：API 描述含"列表"时，按 parametrized_list 模式生成。
    """
    # 创建 API 文件（描述包含"列表"）
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_product_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "page": "1",  # 页码
    "page_size": "20",  # 每页数量
    "status": 1,  # 状态 0：下架 1：上架
}

def _product_list(data=data, access_token=access_token):
    """
    商品列表
    /api/product/list
    """
    url = "/api/product/list"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir))

    result = asyncio.run(generator.generate_batch_testcases([str(api_dir)], "test_batch"))

    assert result["total"] == 1
    assert result["generated"] == 1
    assert result["skipped"] == 0
    assert result["failed"] == 0
    assert len(result["generated_files"]) == 1

    # 验证生成的内容是 parametrized_list 模式
    generated_file = result["generated_files"][0]
    with open(generated_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "import pytest" in content, "列表模式应导入 pytest"
    assert "@pytest.mark.parametrize" in content, "列表模式应包含 parametrize 装饰器"
    assert "status" in content or "page" in content, "应包含 API 文件中的参数"


@allure.feature("测试用例生成器")
@allure.story("batch 模式 - 场景接口流程生成")
def test_batch_scenario_mode(tmp_path):
    """测试 batch 模式生成场景流程测试。

    验证点：API 描述不含"列表"时，按 complex_scenario 模式生成。
    """
    # 创建 API 文件（描述不含"列表"）
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_submit_order.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "product_id": "P001",
    "quantity": 1,
}

def _submit_order(data=data, access_token=access_token):
    """
    提交订单
    /api/order/submit
    """
    url = "/api/order/submit"
    headers = {}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
''')

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir))

    result = asyncio.run(generator.generate_batch_testcases([str(api_dir)], "test_batch"))

    assert result["total"] == 1
    assert result["generated"] == 1
    assert result["failed"] == 0

    # 验证生成的内容是 complex_scenario 模式
    generated_file = result["generated_files"][0]
    with open(generated_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "import pytest" not in content, "场景模式不应导入 pytest"
    assert "def test_submit_order(self):" in content, "应包含测试方法定义"
    assert "test_data = {}" in content, "场景模式应包含 test_data 字典"


@allure.feature("测试用例生成器")
@allure.story("batch 模式 - 已存在文件跳过")
def test_batch_skip_existing(tmp_path):
    """测试 batch 模式跳过已存在的测试文件。

    验证点：get_output_dir(task_id) 会创建 task_id 子目录，预创建文件需放在子目录中。
    """
    # 创建 API 文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "_product_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "status": 1,
}

def _product_list(data=data, access_token=access_token):
    """
    商品列表
    /api/product/list
    """
    url = "/api/product/list"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)

    # 预创建测试文件，放在 task_id 子目录中（get_output_dir 逻辑）
    task_subdir = output_dir / "test_batch"
    task_subdir.mkdir(parents=True)
    existing_file = task_subdir / "test_product_list.py"
    with open(existing_file, "w", encoding="utf-8") as f:
        f.write("# existing content")

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir))

    result = asyncio.run(generator.generate_batch_testcases([str(api_dir)], "test_batch"))

    assert result["skipped"] == 1, "已存在的文件应被跳过"
    assert result["generated"] == 0, "不应生成新文件"


@allure.feature("测试用例生成器")
@allure.story("batch 模式 - 不存在的路径被忽略")
def test_batch_skip_non_existent_path(tmp_path):
    """测试 batch 模式忽略不存在的路径。

    验证点：不存在的文件路径不会计入 total/failed。
    """
    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(tmp_path), output_dir=str(output_dir))

    non_existent = tmp_path / "non_existent.py"
    result = asyncio.run(generator.generate_batch_testcases([str(non_existent)], "test_batch"))

    assert result["total"] == 0, "不存在的路径不计入 total"
    assert result["failed"] == 0


@allure.feature("测试用例生成器")
@allure.story("batch 模式 - 目录展开")
def test_batch_expand_directory(tmp_path):
    """测试 batch 模式展开目录输入。"""
    # 创建多个 API 文件
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    for name in ["_api_one.py", "_api_two.py"]:
        with open(api_dir / name, "w", encoding="utf-8") as f:
            f.write(f'''
# coding:utf-8

def {name.replace(".py", "")}(data=data, access_token=access_token):
    """
    {name.replace(".py", "").lstrip("_")}
    /api/{name.replace(".py", "").lstrip("_")}
    """
    url = "/api/{name.replace(".py", "").lstrip("_")}"
    headers = {{}}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
''')

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path))

    result = asyncio.run(generator.generate_batch_testcases([str(api_dir)], "test_batch"))

    assert result["total"] == 2
    assert result["generated"] == 2


@allure.feature("测试用例生成器")
@allure.story("_build_param_items_from_api - batch模式包含空值")
def test_build_param_items_from_api_batch_includes_empty(tmp_path):
    """测试 _build_param_items_from_api 在 batch 模式下包含空值参数。

    验证点：is_batch_mode=True 时空字符串和 None 也生成参数化项。
    """
    generator = TestCaseGenerator()

    api_params = {
        "keyword": "",
        "category": "A",
        "tag": None,
        "pageNum": "1",
    }

    param_remarks = {}

    result = generator._build_param_items_from_api(api_params, param_remarks, is_batch_mode=True)

    # 应过滤掉 pageNum（分页参数），包含 keyword=""、category="A"、tag=None
    param_names = [next(k for k in item if k != "other_params") for item in result]

    assert "category" in param_names, "有效参数应包含"
    assert "keyword" in param_names, "batch 模式下空字符串应包含"
    assert "tag" in param_names, "batch 模式下 None 应包含"
    assert "pageNum" not in param_names, "分页参数应被过滤"


@allure.feature("测试用例生成器")
@allure.story("_build_param_items_from_api - 非batch模式过滤空值")
def test_build_param_items_from_api_non_batch_filters_empty(tmp_path):
    """测试 _build_param_items_from_api 在非 batch 模式下过滤空值。

    验证点：is_batch_mode=False 时空字符串和 None 被过滤。
    """
    generator = TestCaseGenerator()

    api_params = {
        "keyword": "",
        "category": "A",
        "tag": None,
    }

    param_remarks = {}

    result = generator._build_param_items_from_api(api_params, param_remarks, is_batch_mode=False)

    param_names = [next(k for k in item if k != "other_params") for item in result]

    assert "category" in param_names, "有效参数应包含"
    assert "keyword" not in param_names, "非 batch 模式下空字符串应过滤"
    assert "tag" not in param_names, "非 batch 模式下 None 应过滤"


@allure.feature("测试用例生成器")
@allure.story("_build_param_items_from_api - 状态参数处理")
def test_build_param_items_from_api_with_state_params(tmp_path):
    """测试 _build_param_items_from_api 处理状态参数。

    验证点：状态参数从备注解析并展开为多个值。
    """
    generator = TestCaseGenerator()

    api_params = {
        "status": 1,
    }

    param_remarks = {
        "status": "状态 0：待审核 1：审核通过 2：审核驳回",
    }

    result = generator._build_param_items_from_api(api_params, param_remarks, is_batch_mode=True)

    # 只有 status 参数，应展开为 [0, 1, 2]
    assert len(result) == 1
    status_item = result[0]
    assert "status" in status_item
    assert status_item["status"] == [0, 1, 2], "状态参数应从备注解析为值列表"


@allure.feature("测试用例生成器")
@allure.story("_build_param_items_from_api - 空参数列表")
def test_build_param_items_from_api_empty_params(tmp_path):
    """测试 _build_param_items_from_api 处理空参数列表。"""
    generator = TestCaseGenerator()

    result = generator._build_param_items_from_api({}, {}, is_batch_mode=True)
    assert result == []

    result = generator._build_param_items_from_api({}, {}, is_batch_mode=False)
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("_build_param_items_from_api - 全部分页参数")
def test_build_param_items_from_api_only_pagination(tmp_path):
    """测试 _build_param_items_from_api 过滤全部分页参数。"""
    generator = TestCaseGenerator()

    api_params = {
        "pageNum": "1",
        "pageSize": "20",
    }

    result = generator._build_param_items_from_api(api_params, {}, is_batch_mode=True)
    assert result == [], "全部分页参数应返回空列表"


@allure.feature("测试用例生成器")
@allure.story("_build_param_items_from_api - 混合分页和非分页参数")
def test_build_param_items_from_api_mixed_pagination(tmp_path):
    """测试 _build_param_items_from_api 混合分页和非分页参数。"""
    generator = TestCaseGenerator()

    api_params = {
        "pageNum": "1",
        "pageSize": "20",
        "status": "1",
    }

    result = generator._build_param_items_from_api(api_params, {}, is_batch_mode=True)
    assert len(result) == 1, "只有非分页参数应保留"
    param_name = next(k for k in result[0] if k != "other_params")
    assert param_name == "status", "非分页参数 status 应保留"
