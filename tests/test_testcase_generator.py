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
    assert APIConfig._config is not None
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
def test_parse_api_file_param_remarks(tmp_path):
    test_content = '''
# coding:utf-8

data = {
    "username": "test", # 用户名
    "password": "123456" # 密码
}

def user_login(data=data, token=token):
    """
    用户登录
    /user/login
    """
    url = "/user/login"
    headers = {"Authorization": f"bearer {token}"}
    return client.post(url=url, headers=headers, json=data)
'''

    api_file = tmp_path / "test_api.py"
    api_file.write_text(test_content, encoding="utf-8")

    result = parse_api_file(str(api_file))
    remarks = result["param_remarks"]
    assert remarks.get("username") == "用户名"
    assert remarks.get("password") == "密码"


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

    api_file = api_dir / "user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    headers = {}
    return client.post(url=url, headers=headers, json=data)
''')

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=[])
        api_files = asyncio.run(generator.match_api_files_for_har(str(har_file)))

        assert len(api_files) == 1
        assert "user_login.py" in api_files[0]
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

    api_file = api_dir / "user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    headers = {}
    return client.post(url=url, headers=headers, json=data)
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

    api_file = api_dir / "user_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "status": 1,  # 状态
}

def user_list(data=data, token=token):
    """
    用户列表
    /api/user/list
    """
    url = "/api/user/list"
    headers = {}
    return client.get(url=url, headers=headers, params=data)
''')

    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        generated_files = asyncio.run(generator.generate_parametrized_list_testcases(str(har_file), "test_task"))

        assert len(generated_files) == 1
        assert "test_user_list.py" in generated_files[0]
        assert os.path.exists(generated_files[0])

        # 验证生成内容包含参数化数据（2条请求的status值）
        with open(generated_files[0], encoding="utf-8") as f:
            content = f.read()
        assert "pytest.mark.parametrize" in content
        assert "'status'" in content or '"status"' in content
        # 验证2个值都被参数化（而不是被去重为1个）
        assert '"1"' in content or "'1'" in content
        assert '"2"' in content or "'2'" in content
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

    api_file = api_dir / "user_login.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    headers = {}
    return client.post(url=url, headers=headers, json=data)
''')

    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        result = asyncio.run(
            generator.generate_scenario_testcase(
                har_file_path=str(har_file), target_url="/api/user/login", task_id="test_task"
            )
        )

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

def user_login(data=data, token=token):
    """
    用户登录
    /user/login
    """
    url = "/user/login"
    headers = {"Authorization": f"bearer {token}"}
    return client.post(url=url, headers=headers, json=data)
'''

    with open("user_login.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("user_login.py")
        clean_name = result["function_name"].lstrip("_")
        assert clean_name == "user_login"
    finally:
        if os.path.exists("user_login.py"):
            os.remove("user_login.py")


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

def test_api(headers=headers):
    """
    测试接口
    /test/api
    """
    url = "/test/api"
    return client.get(url=url, headers=headers)
'''

    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        result = parse_api_file("test_api.py")
        headers = result["headers"]
        assert "custom-header" in headers
    finally:
        if os.path.exists("test_api.py"):
            os.remove("test_api.py")


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


# ==================== _parse_state_values 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析格式1状态值（冒号分隔）")
def test_parse_state_values_format1():
    generator = TestCaseGenerator()
    result = generator._parse_state_values("状态 -1：已驳回 0：待审核（默认）1：审核通过")
    assert result == [-1, 0, 1]


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析格式2状态值（括号内数字）")
def test_parse_state_values_format2():
    generator = TestCaseGenerator()
    result = generator._parse_state_values("状态(1待审核2待开始3进行中4已结束5已驳回6草稿)")
    assert result == [1, 2, 3, 4, 5, 6]


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析无状态值的备注")
def test_parse_state_values_no_match():
    generator = TestCaseGenerator()
    result = generator._parse_state_values("普通备注")
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析空备注")
def test_parse_state_values_empty():
    generator = TestCaseGenerator()
    result = generator._parse_state_values("")
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析英文冒号格式")
def test_parse_state_values_english_colon():
    generator = TestCaseGenerator()
    result = generator._parse_state_values("Status: 0:Disabled 1:Enabled")
    assert result == [0, 1]


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析数字后直接跟中文（无分隔符）")
def test_parse_state_values_digit_chinese_no_separator():
    """测试数字后直接跟中文的格式，如 1待审核 2审核通过 3已驳回"""
    generator = TestCaseGenerator()
    result = generator._parse_state_values("审核状态 1待审核 2审核通过 3已驳回 4已完成 5已撤销 6完成待受理 7撤销待受理")
    assert result == [1, 2, 3, 4, 5, 6, 7]


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析数字后跟顿号（、）分隔符")
def test_parse_state_values_digit_chinese_comma():
    """测试数字后跟顿号的格式，如 1、商城运营后台平台,2、店铺运营平台"""
    generator = TestCaseGenerator()
    result = generator._parse_state_values("1、商城运营后台平台,2、店铺运营平台或者app服务中心平台")
    assert result == [1, 2]


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析数字后跟点号（.）分隔符")
def test_parse_state_values_digit_dot():
    """测试数字后跟点号的格式，如 1.产品编码,2.按当前库存,3.按押货价合计"""
    generator = TestCaseGenerator()
    result = generator._parse_state_values("排序方式，1.产品编码,2.按当前库存,3.按押货价合计")
    assert result == [1, 2, 3]


# ==================== _build_param_items_from_api 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("构建参数化项")
@allure.title("测试从API参数构建参数化项（基本场景）")
def test_build_param_items_from_api_basic():
    generator = TestCaseGenerator()
    api_params = {"keyword": "test", "pageNum": 1, "pageSize": 20}
    param_remarks = {"keyword": "关键词"}

    result = generator._build_param_items_from_api(api_params, param_remarks)
    assert len(result) == 1
    assert "keyword" in result[0]
    assert result[0]["keyword"] == ["test"]
    assert "pageNum" in result[0]["other_params"]


@allure.feature("测试用例生成器")
@allure.story("构建参数化项")
@allure.title("测试batch模式包含空值参数")
def test_build_param_items_from_api_batch_mode():
    generator = TestCaseGenerator()
    api_params = {"keyword": "", "pageNum": 1, "pageSize": 20}
    param_remarks = {"keyword": "关键词"}

    # 非batch模式：空值被过滤
    result = generator._build_param_items_from_api(api_params, param_remarks, is_batch_mode=False)
    assert len(result) == 0

    # batch模式：空值保留
    result = generator._build_param_items_from_api(api_params, param_remarks, is_batch_mode=True)
    assert len(result) == 1
    assert result[0]["keyword"] == [""]


@allure.feature("测试用例生成器")
@allure.story("构建参数化项")
@allure.title("测试状态参数特殊处理")
def test_build_param_items_from_api_state_param():
    generator = TestCaseGenerator()
    api_params = {"status": 1, "pageNum": 1}
    param_remarks = {"status": "状态 -1：已驳回 0：待审核 1：审核通过"}

    result = generator._build_param_items_from_api(api_params, param_remarks)
    assert len(result) == 1
    assert "status" in result[0]
    assert result[0]["status"] == [-1, 0, 1]


@allure.feature("测试用例生成器")
@allure.story("构建参数化项")
@allure.title("测试状态参数为列表类型")
def test_build_param_items_from_api_state_param_list():
    generator = TestCaseGenerator()
    api_params = {"orderStatusList": [1, 2], "pageNum": 1}
    param_remarks = {"orderStatusList": "订单状态 1：待审核 2：已通过"}

    result = generator._build_param_items_from_api(api_params, param_remarks)
    assert len(result) == 1
    assert "orderStatusList" in result[0]
    assert result[0]["orderStatusList"] == [[1], [2]]


@allure.feature("测试用例生成器")
@allure.story("构建参数化项")
@allure.title("测试空列表参数在batch模式")
def test_build_param_items_from_api_empty_list_batch():
    generator = TestCaseGenerator()
    api_params = {"orderStatusList": [], "pageNum": 1}
    param_remarks = {"orderStatusList": "订单状态"}

    # 非batch模式：空列表被过滤
    result = generator._build_param_items_from_api(api_params, param_remarks, is_batch_mode=False)
    assert len(result) == 0

    # batch模式：空列表保留
    result = generator._build_param_items_from_api(api_params, param_remarks, is_batch_mode=True)
    assert len(result) == 1
    assert result[0]["orderStatusList"] == [[]]


# ==================== _extract_service_package 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("提取服务包名")
@allure.title("测试从API文件路径提取服务包名")
def test_extract_service_package():
    generator = TestCaseGenerator()
    result = generator._extract_service_package("apis\\mall_center_user\\user_login.py")
    assert result == "mall_center_user"


@allure.feature("测试用例生成器")
@allure.story("提取服务包名")
@allure.title("测试从正斜杠路径提取服务包名")
def test_extract_service_package_forward_slash():
    generator = TestCaseGenerator()
    result = generator._extract_service_package("apis/mgmt_application/_order_list.py")
    assert result == "mgmt_application"


@allure.feature("测试用例生成器")
@allure.story("提取服务包名")
@allure.title("测试无子包时返回 None")
def test_extract_service_package_default():
    generator = TestCaseGenerator()
    result = generator._extract_service_package("user_login.py")
    assert result is None


# ==================== _get_all_api_files 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("获取所有API文件")
@allure.title("测试API目录不存在")
def test_get_all_api_files_not_exists():
    generator = TestCaseGenerator(api_dir="nonexistent_dir")
    result = generator._get_all_api_files()
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("获取所有API文件")
@allure.title("测试获取API文件列表")
def test_get_all_api_files(tmp_path):
    api_dir = tmp_path / "apis"
    api_dir.mkdir()
    (api_dir / "user_login.py").write_text("# test", encoding="utf-8")
    (api_dir / "__init__.py").write_text("", encoding="utf-8")

    generator = TestCaseGenerator(api_dir=str(api_dir))
    result = generator._get_all_api_files()
    assert len(result) == 1
    assert "user_login.py" in result[0]


# ==================== _generate_test_case_imports 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试用例导入")
@allure.title("测试单函数导入（含pytest）")
def test_generate_test_case_imports_single():
    generator = TestCaseGenerator(api_dir="apis")
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api", task_id="test_task"
    )
    content = "\n".join(result)
    assert "import pytest" in content
    assert "import allure" in content
    assert "from apis.test_service import test_api" in content
    assert "@pytest.mark.test_task" in content


@allure.feature("测试用例生成器")
@allure.story("生成测试用例导入")
@allure.title("测试单函数导入（不含task_id）")
def test_generate_test_case_imports_without_task_id():
    generator = TestCaseGenerator(api_dir="apis")
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api"
    )
    content = "\n".join(result)
    assert "import pytest" in content
    assert "import allure" in content


@allure.feature("测试用例生成器")
@allure.story("生成测试用例导入")
@allure.title("测试多函数导入")
def test_generate_test_case_imports_multi(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file1 = api_dir / "user_login.py"
    api_file1.write_text(
        '''
def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    return client.post(url=url, json=data)
''',
        encoding="utf-8",
    )

    api_file2 = api_dir / "user_info.py"
    api_file2.write_text(
        '''
def user_info(data=data, token=token):
    """
    用户信息
    /api/user/info
    """
    url = "/api/user/info"
    return client.get(url=url, params=data)
''',
        encoding="utf-8",
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    result = generator._generate_test_case_imports(api_files=[str(api_file1), str(api_file2)])
    content = "\n".join(result)
    assert "user_login" in content
    assert "user_info" in content


# ==================== _generate_test_case_description 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试用例描述")
@allure.title("测试生成测试用例描述")
def test_generate_test_case_description():
    generator = TestCaseGenerator()
    result = generator._generate_test_case_description("/api/user/login", "test_service")
    content = "\n".join(result)
    assert "Severity.NORMAL" in content
    assert "test_service" in content
    assert "/api/user/login" in content
    assert "class TestClass:" in content


@allure.feature("测试用例生成器")
@allure.story("生成测试用例描述")
@allure.title("测试生成CRITICAL级别描述")
def test_generate_test_case_description_critical():
    generator = TestCaseGenerator()
    result = generator._generate_test_case_description("/api/order/create", "order_service", severity="CRITICAL")
    content = "\n".join(result)
    assert "Severity.CRITICAL" in content


# ==================== _generate_test_method_definition 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试方法定义")
@allure.title("测试单参数方法定义")
def test_generate_test_method_definition_single():
    generator = TestCaseGenerator()
    result = generator._generate_test_method_definition(
        "用户列表", "keyword", {"keyword": "关键词"}, "user_list", 0, False
    )
    content = "\n".join(result)
    assert "keyword" in content
    assert "test_0_user_list" in content
    assert "用户列表" in content


@allure.feature("测试用例生成器")
@allure.story("生成测试方法定义")
@allure.title("测试组合参数方法定义")
def test_generate_test_method_definition_combo():
    generator = TestCaseGenerator()
    result = generator._generate_test_method_definition(
        "订单列表",
        "startDate,endDate",
        {"startDate": "开始日期", "endDate": "结束日期"},
        "order_list",
        0,
        True,
    )
    content = "\n".join(result)
    assert "startDate, endDate" in content
    assert "test_0_order_list" in content
    assert "开始日期-结束日期" in content


# ==================== _generate_test_method_assertions 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试方法断言")
@allure.title("测试生成断言代码")
def test_generate_test_method_assertions():
    generator = TestCaseGenerator()
    result = generator._generate_test_method_assertions("user_login", "data")
    content = "\n".join(result)
    assert "user_login(data=data)" in content
    assert "r.status_code == 200" in content
    assert "data = r.json()" in content
    assert "assert data['code'] == 200" in content


# ==================== _generate_step_function_name 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数名")
@allure.title("测试生成步骤函数名（首次）")
def test_generate_step_function_name_first():
    generator = TestCaseGenerator()
    name_counters = {}
    result = generator._generate_step_function_name("user_login", name_counters)
    assert result == "step_user_login"


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数名")
@allure.title("测试生成步骤函数名（重复）")
def test_generate_step_function_name_duplicate():
    generator = TestCaseGenerator()
    name_counters = {}
    # 第一次调用
    name1 = generator._generate_step_function_name("user_login", name_counters)
    assert name1 == "step_user_login"
    # 第二次调用同一函数名
    name2 = generator._generate_step_function_name("user_login", name_counters)
    assert name2 == "step_1_user_login"


# ==================== _generate_step_function_body 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数体")
@allure.title("测试生成data参数的步骤函数体")
def test_generate_step_function_body_data(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "user_login.py"
    api_file.write_text(
        '''
data = {"username": "test", "password": "123456"}

def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    return client.post(url=url, json=data)
''',
        encoding="utf-8",
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "user_login", api_info)
    result = "\n".join(content)
    assert "data =" in result
    assert "username" in result
    assert "user_login(data=data)" in result


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数体")
@allure.title("测试生成params参数的步骤函数体")
def test_generate_step_function_body_params(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "user_list.py"
    api_file.write_text(
        '''
params = {"keyword": "test", "pageNum": 1}

def user_list(params=params, token=token):
    """
    用户列表
    /api/user/list
    """
    url = "/api/user/list"
    return client.get(url=url, params=params)
''',
        encoding="utf-8",
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "user_list", api_info)
    result = "\n".join(content)
    assert "params =" in result
    assert "keyword" in result
    assert "user_list(params=params)" in result


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数体")
@allure.title("测试无参数API的步骤函数体")
def test_generate_step_function_body_no_params(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "health_check.py"
    api_file.write_text(
        '''
def health_check(token=token):
    """
    健康检查
    /api/health
    """
    url = "/api/health"
    return client.get(url=url)
''',
        encoding="utf-8",
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "health_check", api_info)
    result = "\n".join(content)
    assert "health_check()" in result


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数体")
@allure.title("测试文件上传类型的步骤函数体")
def test_generate_step_function_body_files(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "upload.py"
    api_file.write_text(
        '''
files = {"file": "test.png"}

def upload(files=files, token=token):
    """
    文件上传
    /api/upload
    """
    url = "/api/upload"
    return client.post(url=url, files=files)
''',
        encoding="utf-8",
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "upload", api_info)
    result = "\n".join(content)
    assert "files =" in result
    assert "upload(files=files)" in result


# ==================== _generate_parametrize_values 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成参数化值")
@allure.title("测试单参数值生成")
def test_generate_parametrize_values_single():
    generator = TestCaseGenerator()
    result = generator._generate_parametrize_values(["test", "value"], False)
    assert len(result) == 2
    assert '"test"' in result[0]


@allure.feature("测试用例生成器")
@allure.story("生成参数化值")
@allure.title("测试组合参数值生成")
def test_generate_parametrize_values_combo():
    generator = TestCaseGenerator()
    result = generator._generate_parametrize_values([["2026-01-01", "2026-01-31"]], True)
    assert len(result) == 1
    assert "2026-01-01" in result[0]
    assert "2026-01-31" in result[0]


# ==================== _generate_data_dict 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成数据字典")
@allure.title("测试单参数数据字典")
def test_generate_data_dict_single():
    generator = TestCaseGenerator()
    content = []
    generator._generate_data_dict(content, "keyword", {"pageNum": 1}, False, "params")
    result = "\n".join(content)
    assert '"keyword": keyword' in result
    assert '"pageNum": 1' in result


@allure.feature("测试用例生成器")
@allure.story("生成数据字典")
@allure.title("测试组合参数数据字典")
def test_generate_data_dict_combo():
    generator = TestCaseGenerator()
    content = []
    generator._generate_data_dict(content, "startDate,endDate", {"pageNum": 1}, True, "params")
    result = "\n".join(content)
    assert '"startDate": startDate' in result
    assert '"endDate": endDate' in result


# ==================== _generate_parametrize_decorator 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成参数化装饰器")
@allure.title("测试生成参数化装饰器")
def test_generate_parametrize_decorator():
    generator = TestCaseGenerator()
    result = generator._generate_parametrize_decorator("keyword", ["test1", "test2"], False)
    content = "\n".join(result)
    assert "@pytest.mark.parametrize" in content
    assert "keyword" in content
    assert "test1" in content
    assert "test2" in content


# ==================== _generate_test_method_body 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试方法体")
@allure.title("测试生成测试方法体")
def test_generate_test_method_body():
    generator = TestCaseGenerator()
    result = generator._generate_test_method_body("params", "keyword", {"pageNum": 1}, False)
    content = "\n".join(result)
    assert "params = {" in content
    assert '"keyword": keyword' in content
    assert '"pageNum": 1' in content


# ==================== normalize_params_for_parametrization 边缘测试 ====================


@allure.feature("测试用例生成器")
@allure.story("标准化参数化")
@allure.title("测试标准化参数化-全部分页参数")
def test_normalize_params_all_pagination():
    generator = TestCaseGenerator()
    requests_params = [{"pageNum": 1, "pageSize": 20}, {"pageNum": 2, "pageSize": 20}]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 0


@allure.feature("测试用例生成器")
@allure.story("标准化参数化")
@allure.title("测试标准化参数-去重相同值")
def test_normalize_params_dedup():
    generator = TestCaseGenerator()
    requests_params = [
        {"keyword": "test", "pageNum": 1},
        {"keyword": "test", "pageNum": 2},
        {"keyword": "test", "pageNum": 3},
    ]
    result = generator.normalize_params_for_parametrization(requests_params)
    assert len(result) == 1
    assert len(result[0]["keyword"]) == 1
    assert result[0]["keyword"] == ["test"]


# ==================== generate_parametrized_list_testcases 边缘测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成参数化列表测试用例")
@allure.title("测试HAR文件不存在")
def test_generate_parametrized_list_testcases_no_har():
    generator = TestCaseGenerator()
    result = asyncio.run(generator.generate_parametrized_list_testcases("nonexistent.har", "test"))
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("生成参数化列表测试用例")
@allure.title("测试目标URL无匹配")
def test_generate_parametrized_list_testcases_no_match(tmp_path):
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
    (api_dir / "user_login.py").write_text(
        '''
def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    return client.post(url=url, json=data)
''',
        encoding="utf-8",
    )

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=[])
    result = asyncio.run(
        generator.generate_parametrized_list_testcases(str(har_file), "test", target_url="/api/nonexistent")
    )
    assert result == []


@allure.feature("测试用例生成器")
@allure.story("生成参数化列表测试用例")
@allure.title("测试overwrite参数生成的用例包含HAR参数")
def test_generate_parametrized_list_testcases_overwrite(tmp_path):
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
                        "queryString": [{"name": "keyword", "value": "test_value"}],
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

    api_file = api_dir / "user_list.py"
    api_file.write_text(
        '''
data = {"keyword": ""}

def user_list(data=data, token=token):
    """
    用户列表
    /api/user/list
    """
    url = "/api/user/list"
    return client.get(url=url, params=data)
''',
        encoding="utf-8",
    )

    output_dir = tmp_path / "output"

    # 第一次生成
    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
    result1 = asyncio.run(generator.generate_parametrized_list_testcases(str(har_file), "test"))
    assert len(result1) == 1

    # 不覆盖：文件已存在，跳过
    result2 = asyncio.run(generator.generate_parametrized_list_testcases(str(har_file), "test"))
    assert len(result2) == 0

    # 覆盖：强制重新生成
    result3 = asyncio.run(generator.generate_parametrized_list_testcases(str(har_file), "test", overwrite=True))
    assert len(result3) == 1


# ==================== generate_scenario_testcase 边缘测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成场景测试用例")
@allure.title("测试目标URL无匹配")
def test_generate_scenario_testcase_no_match(tmp_path):
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
    (api_dir / "user_login.py").write_text(
        '''
def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    return client.post(url=url, json=data)
''',
        encoding="utf-8",
    )

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=[])
    result = asyncio.run(generator.generate_scenario_testcase(str(har_file), "/api/nonexistent", "test"))
    assert result is None


@allure.feature("测试用例生成器")
@allure.story("生成场景测试用例")
@allure.title("测试场景测试用例覆盖参数")
def test_generate_scenario_testcase_overwrite(tmp_path):
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
    (api_dir / "user_login.py").write_text(
        '''
def user_login(data=data, token=token):
    """
    用户登录
    /api/user/login
    """
    url = "/api/user/login"
    return client.post(url=url, json=data)
''',
        encoding="utf-8",
    )

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
    # 第一次生成
    result1 = asyncio.run(generator.generate_scenario_testcase(str(har_file), "/api/user/login", "test"))
    assert result1 is not None

    # 不覆盖：跳过
    result2 = asyncio.run(generator.generate_scenario_testcase(str(har_file), "/api/user/login", "test"))
    assert result2 is None

    # 覆盖：强制重新生成
    result3 = asyncio.run(
        generator.generate_scenario_testcase(str(har_file), "/api/user/login", "test", overwrite=True)
    )
    assert result3 is not None


@allure.feature("测试用例生成器")
@allure.story("参数化多请求去重")
@allure.title("测试同URL多请求参数化不被去重")
def test_generate_parametrized_list_testcases_multi_request(tmp_path):
    """验证同URL多请求时参数化不会被去重，确保每条请求的参数都被提取。

    这是针对 HARParser 默认 filter_duplicate_url=True 导致同URL请求被去重为1条的回归测试。
    """
    import json

    # 创建3条同URL但不同参数的请求
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
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/list",
                        "method": "GET",
                        "headers": [{"name": "origin", "value": "https://example.com"}],
                        "queryString": [{"name": "status", "value": "3"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 70,
                },
            ]
        }
    }

    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "user_list.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write('''
# coding:utf-8

data = {
    "status": 1,  # 状态
}

def user_list(data=data, token=token):
    """
    用户列表
    /api/user/list
    """
    url = "/api/user/list"
    headers = {}
    return client.get(url=url, headers=headers, params=data)
''')

    output_dir = tmp_path / "output"

    try:
        generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
        generated_files = asyncio.run(generator.generate_parametrized_list_testcases(str(har_file), "test_task"))

        assert len(generated_files) == 1
        filepath = generated_files[0]

        # 验证生成内容包含参数化装饰器，且包含了3个不同的status值
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        assert "pytest.mark.parametrize" in content
        assert "'status'" in content or '"status"' in content
        # 验证3个值都被参数化（而不是被去重为1个）
        assert '"1"' in content or "'1'" in content
        assert '"2"' in content or "'2'" in content
        assert '"3"' in content or "'3'" in content
    finally:
        pass


@allure.feature("测试用例生成器")
@allure.story("批量生成测试用例")
@allure.title("测试批量生成中无参数接口且匹配列表关键词时fallback到场景测试")
def test_generate_batch_no_param_list_keyword_fallback(tmp_path):
    """验证当API描述匹配LIST_QUERY_KEYWORDS但接口无参数时，自动fallback到场景测试。

    修复问题：描述含'列表'但接口无参数导致生成失败。
    """
    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)

    # API描述含'列表'关键词，但是接口无参数（只有headers）
    (api_dir / "common_ProductProvenance.py").write_text(
        '''
import os

from har2pytest.client import client

headers = {
    "authorization": f"bearer {os.environ['token']}",
}


def common_Provenance(headers=headers):
    """
    获取商品发货信息列表
    /common/ProductProvenance
    """

    url = "/common/ProductProvenance"
    return client.get(url=url, headers=headers)
''',
        encoding="utf-8",
    )

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir))
    result = asyncio.run(
        generator.generate_batch_testcases([str(api_dir)], task_id="test_task", overwrite=True, har_file_path=None)
    )

    # 应该成功生成，而不是失败
    assert result["total"] == 1
    assert result["generated"] == 1
    assert result["failed"] == 0
    assert len(result["generated_files"]) == 1
    # 文件应该存在
    assert os.path.exists(result["generated_files"][0])


@allure.feature("测试用例生成器")
@allure.story("生成参数化列表测试用例")
@allure.title("测试参数化模式下无参数时fallback到场景测试")
def test_generate_parametrized_list_no_param_fallback(tmp_path):
    """验证参数化模式下找不到参数时，自动fallback到场景测试。"""
    import json

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "/common/ProductProvenance",
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

    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)

    (api_dir / "common_ProductProvenance.py").write_text(
        '''
import os

from har2pytest.client import client

headers = {
    "authorization": f"test {os.environ['token']}",
}


def common_ProductProvenance(headers=headers):
    """
    获取商品发货信息列表
    /common/ProductProvenance
    """

    url = "/common/ProductProvenance"
    return client.get(url=url, headers=headers)
''',
        encoding="utf-8",
    )

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
    generated_files = asyncio.run(generator.generate_parametrized_list_testcases(str(har_file), "test_task"))

    # 应该成功生成，而不是因为无参数被跳过
    assert len(generated_files) == 1
    filepath = generated_files[0]
    assert os.path.exists(filepath)

    # 验证生成的是场景测试，不是参数化测试
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # 场景测试不含pytest.mark.parametrize，包含步骤函数
    assert "pytest.mark.parametrize" not in content
    assert "step_" in content
    assert "common_ProductProvenance" in content


# ==================== 异步模式测试 ====================


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试异步模式生成 async def 测试方法")
def test_async_mode_scenario_test_method_definition(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    (api_dir / "user_login.py").write_text(
        "\ndef user_login(data=data):\n    \"\"\"\n    test\n    /api/login\n    \"\"\"\n    url = \"/api/login\"\n    return client.post(url=url, json=data)\n",
        encoding="utf-8",
    )
    generator = TestCaseGenerator(api_dir=str(api_dir), async_mode=True)
    result = generator._generate_scenario_test_method_definition(str(api_dir / "user_login.py"))
    content = "\n".join(result)
    assert "async def test_user_login(self):" in content


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试同步模式生成 def 测试方法")
def test_sync_mode_scenario_test_method_definition(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    (api_dir / "user_login.py").write_text(
        "\ndef user_login(data=data):\n    \"\"\"\n    test\n    /api/login\n    \"\"\"\n    url = \"/api/login\"\n    return client.post(url=url, json=data)\n",
        encoding="utf-8",
    )
    generator = TestCaseGenerator(api_dir=str(api_dir), async_mode=False)
    result = generator._generate_scenario_test_method_definition(str(api_dir / "user_login.py"))
    content = "\n".join(result)
    assert "def test_user_login(self):" in content
    assert "async def" not in content


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试异步模式步骤函数体使用 async with")
def test_async_mode_step_function_body():
    generator = TestCaseGenerator(api_dir="apis", async_mode=True)
    content = []
    generator._generate_step_function_body(content, "user_login", {"data": {"name": ""}}, {"query_params": {}, "post_data": {"name": "test"}})
    result = "\n".join(content)
    assert "async with user_login(data=data) as r:" in result


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试同步模式步骤函数体使用 with")
def test_sync_mode_step_function_body():
    generator = TestCaseGenerator(api_dir="apis", async_mode=False)
    content = []
    generator._generate_step_function_body(content, "user_login", {"data": {"name": ""}}, {"query_params": {}, "post_data": {"name": "test"}})
    result = "\n".join(content)
    assert "with user_login(data=data) as r:" in result
    assert "async with" not in result


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试异步模式断言使用 await r.json() 和 r.status")
def test_async_mode_test_method_assertions():
    generator = TestCaseGenerator(api_dir="apis", async_mode=True)
    result = generator._generate_test_method_assertions("user_login", "data")
    content = "\n".join(result)
    assert "async with user_login(data=data) as r:" in content
    assert "assert r.status == 200" in content
    assert "data = await r.json()" in content
    assert "assert data['code'] == 200" in content


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试同步模式断言使用 r.json() 和 r.status_code")
def test_sync_mode_test_method_assertions():
    generator = TestCaseGenerator(api_dir="apis", async_mode=False)
    result = generator._generate_test_method_assertions("user_login", "data")
    content = "\n".join(result)
    assert "with user_login(data=data) as r:" in content
    assert "assert r.status_code == 200" in content
    assert "data = r.json()" in content
    assert "assert data['code'] == 200" in content


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试异步模式导入包含 client.set_client")
def test_async_mode_imports_include_set_client():
    """异步模式测试用例应在导入部分切换 client 为 async_client。"""
    generator = TestCaseGenerator(api_dir="apis", async_mode=True)
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api"
    )
    content = "\n".join(result)
    assert "from har2pytest.client import client, async_client" in content
    assert "client.set_client(async_client)" in content


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试同步模式导入不包含 client.set_client")
def test_sync_mode_imports_exclude_set_client():
    """同步模式测试用例不应切换 client。"""
    generator = TestCaseGenerator(api_dir="apis", async_mode=False)
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api"
    )
    content = "\n".join(result)
    assert "client.set_client" not in content
