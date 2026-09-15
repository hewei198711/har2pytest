"""测试 har2pytest.testcase_generator 模块中参数化列表、复杂场景、批量三种测试用例模式的生成、参数标准化、描述构建、步骤函数体构建、URL 匹配与模式决策的功能与边界。"""

import asyncio
import json
import logging
import os

import allure
import pytest

from har2pytest.api_metadata import write_api_metadata
from har2pytest.config import APIConfig
from har2pytest.models import APIFileInfo, ParsedRequestInfo
from har2pytest.testcase_generator import TestCaseGenerator
from har2pytest.utils import format_params_for_python, parse_api_file


def _write_api_sidecar(
    api_file,
    *,
    url,
    description="",
    function_name=None,
    method=None,
    param_remarks=None,
    params=None,
    data=None,
    files=None,
    headers=None,
):
    """为手写的 API 模块写同名 ``.api.json`` 元数据。

    parse_api_file 现在只读 ``<module>.api.json``（不再解析 .py 源码/docstring），
    因此每个测试手写的 API 文件都需补一份元数据来表达原断言所需信息：url 必填
    （缺失会让 parse_api_file 抛 ValueError），description 对应原 docstring 第一行，
    data/params/files/headers 对应原模块级赋值，param_remarks 对应原行内 # 备注。

    Returns:
        str: 写出的元数据文件路径。
    """
    return write_api_metadata(
        str(api_file),
        function_name=function_name,
        url=url,
        description=description,
        method=method,
        param_remarks=param_remarks,
        params=params,
        data=data,
        files=files,
        headers=headers,
    )


def _make_har_entry(url, method="GET", headers=None, query_string=None, post_data=None, status=200, time_ms=100):
    """构造单条 HAR entry dict。"""
    request = {"url": url, "method": method, "headers": headers or []}
    if query_string is not None:
        request["queryString"] = query_string
    if post_data is not None:
        request["postData"] = post_data
    return {
        "_resourceType": "xhr",
        "request": request,
        "response": {"status": status, "content": {"text": "{}"}},
        "time": time_ms,
    }


@pytest.fixture
def write_har(tmp_path):
    """工厂 fixture：将 entries 列表写入临时 HAR 文件并返回路径。"""
    def _write(entries, filename="test.har"):
        har_data = {"log": {"entries": entries}}
        har_path = tmp_path / filename
        har_path.write_text(json.dumps(har_data, ensure_ascii=False), encoding="utf-8")
        return har_path
    return _write


# ==================== 格式化参数测试 ====================


@allure.feature("测试用例生成器")
@allure.story("格式化参数")
@allure.title("测试格式化参数为测试用例中的参数字符串")
@pytest.mark.parametrize("params,checks", [
    ({}, ["== {}"]),
    ({"keyword": "TS001", "pageNum": 1}, ["keyword", "TS001", "pageNum", "1"]),
    ({"name": "test<script>", "path": "/api/test"}, ["name", "path"]),
    ({"name": "", "value": None}, ["name", "value"]),
])
def test_format_test_case_params(params, checks):
    result = format_params_for_python(params)
    for check in checks:
        if check.startswith("== "):
            assert result == check[3:]
        else:
            assert check in result


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


# ==================== 从URL提取服务包名测试 ====================


@allure.feature("测试用例生成器")
@allure.story("从URL提取服务包名")
@allure.title("测试从URL中提取服务包名")
def test_extract_service_package_from_url():
    APIConfig.get_config("SERVICE_MAPPING")
    assert APIConfig._config is not None
    original_service_mapping = APIConfig._config.get("SERVICE_MAPPING", {})
    original_lower = dict(APIConfig._service_mapping_lower)
    new_mapping = {"mobile": "mall_mobile_application", "user": "mall_center_user"}
    APIConfig._config["SERVICE_MAPPING"] = new_mapping
    APIConfig._service_mapping_lower = {k.lower(): v for k, v in new_mapping.items()}

    try:
        assert APIConfig.determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"
        assert APIConfig.determine_service_package("/user/123/info") == "mall_center_user"
        assert APIConfig.determine_service_package("") == "apis"
    finally:
        APIConfig._config["SERVICE_MAPPING"] = original_service_mapping
        APIConfig._service_mapping_lower = original_lower


# ==================== 提取参数备注测试 ====================


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

    # 行内 # 备注曾由 parse_api_file 从 .py 反解，现改由 .api.json 元数据提供
    _write_api_sidecar(
        api_file,
        url="/user/login",
        description="用户登录",
        data={"username": "test", "password": "123456"},
        param_remarks={"username": "用户名", "password": "密码"},
    )

    result = parse_api_file(str(api_file))
    remarks = result.param_remarks
    assert remarks.get("username") == "用户名"
    assert remarks.get("password") == "密码"


# ==================== 匹配API文件测试 ====================


@allure.feature("测试用例生成器")
@allure.story("匹配API文件")
@allure.title("测试根据HAR文件匹配API文件")
def test_match_api_files_for_har(tmp_path, write_har):

    har_file = write_har([_make_har_entry("/api/user/login", "POST")])

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

    # URL 匹配依赖 .api.json 元数据（缺元数据的候选文件会被 find_matching_api_file 跳过）
    _write_api_sidecar(api_file, url="/api/user/login", description="用户登录")

    generator = TestCaseGenerator(api_dir=str(api_dir), base_urls=[])
    api_files = asyncio.run(generator.match_api_files_for_har(str(har_file)))

    assert len(api_files) == 1
    assert "user_login.py" in api_files[0]


@allure.feature("测试用例生成器")
@allure.story("匹配API文件-无匹配")
@allure.title("测试HAR文件没有匹配的API文件")
def test_match_api_files_for_har_no_match(tmp_path, write_har):

    har_file = write_har([_make_har_entry("https://example.com/api/nonexistent", time_ms=50)])

    api_dir = tmp_path / "apis"
    api_dir.mkdir()

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_files = asyncio.run(generator.match_api_files_for_har(str(har_file)))

    assert len(api_files) == 0


# ==================== 生成测试用例内容测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试用例内容")
@allure.title("测试生成场景测试用例内容")
def test_generate_scenario_test_content(tmp_path, write_har):

    har_file = write_har([_make_har_entry(
        "/api/user/login", "POST",
        headers=[{"name": "Content-Type", "value": "application/json"}],
        post_data={"mimeType": "application/json", "text": "{}"},
    )])

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

    _write_api_sidecar(api_file, url="/api/user/login", description="用户登录")

    generator = TestCaseGenerator(api_dir=str(api_dir))
    content = generator.generate_scenario_test_content(
        har_file_path=str(har_file),
        api_files=[str(api_file)],
        task_id="test_task",
        target_api_file=str(api_file),
    )

    assert content is not None
    assert "test_user_login" in content
    assert "user_login" in content
    assert "allure" in content


@allure.feature("测试用例生成器")
@allure.story("生成测试用例内容")
@allure.title("测试场景模式生成类级别 headers 属性")
def test_generate_scenario_test_content_with_headers(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)

    api_file = api_dir / "file_upload.py"
    api_file.write_text(
        '''
import os

files = {
    "file": "(binary)",
}

headers = {
    "authorization": f"bearer {os.environ['token']}",
    "GW-Client": "test",
}
def file_upload(files=files, headers=headers):
    """
    文件上传
    /api/upload
    """
    url = "/api/upload"
    return client.post(url=url, headers=headers, data=files)
''',
        encoding="utf-8",
    )

    # 模块级 files/headers 的值现取自 .api.json 元数据（含 f-string 源码片段，
    # 与生成器写入元数据的快照一致），而非解析上面的 .py 模块级赋值
    _write_api_sidecar(
        api_file,
        url="/api/upload",
        description="文件上传",
        files={"file": "(binary)"},
        headers={
            "authorization": 'f"bearer {os.environ[\'token\']}"',
            "GW-Client": "test",
        },
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    content = generator.generate_scenario_test_content(
        har_file_path=None,
        api_files=[str(api_file)],
        task_id=None,
        target_api_file=str(api_file),
    )

    assert content is not None
    # 类级别 headers 属性已生成
    assert "@property" in content
    assert "def headers(self):" in content
    # f-string 安全转换
    assert "os.environ.get('token', '')" in content
    assert '"GW-Client": "test",' in content
    # 步骤调用传 headers=self.headers
    assert "headers=self.headers" in content


@allure.feature("测试用例生成器")
@allure.story("生成场景测试用例")
@allure.title("测试生成场景测试用例")
def test_generate_scenario_testcase(tmp_path, write_har):

    har_file = write_har([_make_har_entry(
        "/api/user/login", "POST",
        headers=[{"name": "Content-Type", "value": "application/json"}],
        post_data={"mimeType": "application/json", "text": "{}"},
    )])

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

    _write_api_sidecar(api_file, url="/api/user/login", description="用户登录")

    output_dir = tmp_path / "output"

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir), base_urls=[])
    result = asyncio.run(
        generator.generate_scenario_testcase(
            har_file_path=str(har_file), target_url="/api/user/login", task_id="test_task"
        )
    )

    assert result is not None
    assert "test_user_login.py" in result
    assert os.path.exists(result)


@allure.feature("测试用例生成器")
@allure.story("提取参数备注-文件不存在")
@allure.title("测试从不存在的API文件提取参数备注")
def test_parse_api_file_param_remarks_not_found():
    # 新语义：无 <module>.api.json 元数据直接抛 ValueError（不再回退解析 .py）
    with pytest.raises(ValueError, match="缺少 API 元数据"):
        parse_api_file("nonexistent.py")


@allure.feature("测试用例生成器")
@allure.story("提取参数备注-无效内容")
@allure.title("测试从无效内容的API文件提取参数备注")
def test_parse_api_file_param_remarks_invalid(tmp_path):
    test_content = """
# coding:utf-8

def test_func():
    pass
"""
    api_file = tmp_path / "invalid_api.py"
    api_file.write_text(test_content, encoding="utf-8")

    # .py 内容不再被解析；元数据仅给必需字段 url，param_remarks 保持为空
    _write_api_sidecar(api_file, url="/invalid/api")

    result = parse_api_file(str(api_file))
    remarks = result.param_remarks
    assert remarks == {}


@allure.feature("测试用例生成器")
@allure.story("获取清理后的函数名")
@allure.title("测试获取清理后的函数名")
def test_parse_api_file_function_name_clean(tmp_path):
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

    api_file = tmp_path / "user_login.py"
    api_file.write_text(test_content, encoding="utf-8")

    _write_api_sidecar(api_file, url="/user/login", description="用户登录")

    result = parse_api_file(str(api_file))
    clean_name = (result.function_name or "").lstrip("_")
    assert clean_name == "user_login"


@allure.feature("测试用例生成器")
@allure.story("获取清理后的函数名-无函数名")
@allure.title("测试从无函数名的文件获取清理后的函数名")
def test_parse_api_file_function_name_no_function(tmp_path):
    test_content = """
# coding:utf-8

data = {
    "username": "test"
}
"""

    api_file = tmp_path / "test_no_func.py"
    api_file.write_text(test_content, encoding="utf-8")

    _write_api_sidecar(api_file, url="/no/func")

    result = parse_api_file(str(api_file))
    clean_name = (result.function_name or "").lstrip("_")
    assert clean_name == "test_no_func"


@allure.feature("测试用例生成器")
@allure.story("获取Headers字符串-直接使用parse_api_file")
@allure.title("测试使用parse_api_file获取Headers")
def test_parse_api_file_headers(tmp_path):
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

    api_file = tmp_path / "test_api.py"
    api_file.write_text(test_content, encoding="utf-8")

    # 模块级 headers 的值现取自 .api.json 元数据，而非解析上面的 .py
    _write_api_sidecar(
        api_file,
        url="/test/api",
        description="测试接口",
        headers={"custom-header": "custom-value"},
    )

    result = parse_api_file(str(api_file))
    headers = result.headers
    assert "custom-header" in headers


# ==================== _parse_state_values 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("解析状态值")
@allure.title("测试解析状态值")
@pytest.mark.parametrize("remark,expected", [
    ("状态 -1：已驳回 0：待审核（默认）1：审核通过", [-1, 0, 1]),
    ("状态(1待审核2待开始3进行中4已结束5已驳回6草稿)", [1, 2, 3, 4, 5, 6]),
    ("普通备注", []),
    ("", []),
    ("Status: 0:Disabled 1:Enabled", [0, 1]),
    ("审核状态 1待审核 2审核通过 3已驳回 4已完成 5已撤销 6完成待受理 7撤销待受理", [1, 2, 3, 4, 5, 6, 7]),
    ("1、商城运营后台平台,2、店铺运营平台或者app服务中心平台", [1, 2]),
    ("排序方式，1.产品编码,2.按当前库存,3.按押货价合计", [1, 2, 3]),
])
def test_parse_state_values(remark, expected):
    generator = TestCaseGenerator()
    assert generator._parse_state_values(remark) == expected


# ==================== _build_param_items_from_api 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("构建参数化项")
@allure.title("测试从API参数构建参数化项")
@pytest.mark.parametrize("api_params,param_remarks,is_batch,expected_len,expected_key,expected_val", [
    ({"keyword": "test", "pageNum": 1, "pageSize": 20}, {"keyword": "关键词"}, None, 1, "keyword", ["test"]),
    ({"keyword": "", "pageNum": 1, "pageSize": 20}, {"keyword": "关键词"}, False, 0, None, None),
    ({"keyword": "", "pageNum": 1, "pageSize": 20}, {"keyword": "关键词"}, True, 1, "keyword", [""]),
    ({"status": 1, "pageNum": 1}, {"status": "状态 -1：已驳回 0：待审核 1：审核通过"}, None, 1, "status", [-1, 0, 1]),
    ({"orderStatusList": [1, 2], "pageNum": 1}, {"orderStatusList": "订单状态 1：待审核 2：已通过"}, None, 1, "orderStatusList", [[1], [2]]),
    ({"orderStatusList": [], "pageNum": 1}, {"orderStatusList": "订单状态"}, False, 0, None, None),
    ({"orderStatusList": [], "pageNum": 1}, {"orderStatusList": "订单状态"}, True, 1, "orderStatusList", [[]]),
])
def test_build_param_items_from_api(api_params, param_remarks, is_batch, expected_len, expected_key, expected_val):
    generator = TestCaseGenerator()
    kwargs = {"is_batch_mode": is_batch} if is_batch is not None else {}
    result = generator._build_param_items_from_api(api_params, param_remarks, **kwargs)
    assert len(result) == expected_len
    if expected_key:
        assert expected_key in result[0]
        assert result[0][expected_key] == expected_val
        if "keyword" in api_params:
            assert "pageNum" in result[0].get("other_params", {})


# ==================== _extract_service_package 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("提取服务包名")
@allure.title("测试从API文件路径提取服务包名")
@pytest.mark.parametrize("path,expected", [
    ("apis/mall_center_user/user_login.py", "mall_center_user"),
    ("apis/mgmt_application/_order_list.py", "mgmt_application"),
    ("apis/login.py", None),
])
def test_extract_service_package(path, expected):
    generator = TestCaseGenerator()
    assert generator._extract_service_package(path) == expected


# ==================== _get_all_api_files 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("获取所有API文件")
@allure.title("测试获取API文件列表")
def test_get_all_api_files(tmp_path):
    # 目录不存在
    generator = TestCaseGenerator(api_dir="nonexistent_dir")
    assert generator._get_all_api_files() == []

    # 目录存在
    api_dir = tmp_path / "apis"
    api_dir.mkdir()
    (api_dir / "user_login.py").write_text("# test", encoding="utf-8")
    (api_dir / "__init__.py").write_text("", encoding="utf-8")
    generator = TestCaseGenerator(api_dir=str(api_dir))
    result = generator._get_all_api_files()
    assert len(result) == 1
    assert "user_login.py" in result[0]


@allure.feature("测试用例生成器")
@allure.story("获取API文件信息")
@allure.title("测试 _get_api_file_info 无实例级第二层缓存")
def test_get_api_file_info_single_cache(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "user_login.py"
    api_file.write_text(
        'params = {"keyword": "test"}\n\ndef user_login(params=params):\n    """\n    用户登录\n    /user/login\n    """\n',
        encoding="utf-8",
    )
    _write_api_sidecar(
        api_file,
        url="/user/login",
        description="用户登录",
        params={"keyword": "test"},
    )
    generator = TestCaseGenerator(api_dir=str(api_dir))
    info = generator._get_api_file_info(str(api_file))
    assert info.function_name == "user_login"
    assert not hasattr(generator, "_api_file_cache"), "应复用 parse_api_file 全局缓存，不建实例级缓存"


# ==================== _generate_test_case_imports 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试用例导入")
@allure.title("测试单函数导入")
@pytest.mark.parametrize("task_id,has_marker", [
    ("test_task", True),
    (None, False),
])
def test_generate_test_case_imports_single(task_id, has_marker):
    generator = TestCaseGenerator(api_dir="apis")
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api", task_id=task_id
    )
    content = "\n".join(result)
    assert "import pytest" in content
    assert "import allure" in content
    assert "from apis.test_service import test_api" in content
    if has_marker:
        assert "@pytest.mark.test_task" in content


@allure.feature("测试用例生成器")
@allure.story("生成测试用例导入")
@allure.title("测试 list_query 模式自动添加 test_list_query 标记")
@pytest.mark.parametrize("task_id,expected_marks", [
    (None, ["@pytest.mark.test_list_query"]),
    ("test_aftersales", ["@pytest.mark.test_aftersales", "@pytest.mark.test_list_query"]),
])
def test_generate_test_case_imports_list_query_mark(task_id, expected_marks):
    generator = TestCaseGenerator(api_dir="apis")
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api",
        task_id=task_id, is_list_query=True,
    )
    content = "\n".join(result)
    for mark in expected_marks:
        assert mark in content, f"缺少标记 {mark}"


@allure.feature("测试用例生成器")
@allure.story("生成测试用例导入")
@allure.title("测试非 list_query 模式不包含 test_list_query 标记")
def test_generate_test_case_imports_without_list_query():
    generator = TestCaseGenerator(api_dir="apis")
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api",
        task_id="test_task", is_list_query=False,
    )
    content = "\n".join(result)
    assert "@pytest.mark.test_task" in content
    assert "@pytest.mark.test_list_query" not in content


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
    _write_api_sidecar(api_file1, url="/api/user/login", description="用户登录")

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
    _write_api_sidecar(api_file2, url="/api/user/info", description="用户信息")

    generator = TestCaseGenerator(api_dir=str(api_dir))
    result = generator._generate_test_case_imports(api_files=[str(api_file1), str(api_file2)])
    content = "\n".join(result)
    assert "user_login" in content
    assert "user_info" in content


# ==================== _generate_test_case_description 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试用例描述")
@allure.title("测试测试用例描述与 headers 属性生成")
@pytest.mark.parametrize("story_name,feature_name,severity,kwargs,checks", [
    ("/api/user/login", "test_service", None, {},
     ["has:Severity.NORMAL", "has:test_service", "has:/api/user/login", "has:class TestClass:",
      "nothas:@allure.description", "nothas:@property", "nothas:def headers(self):"]),
    ("/api/order/create", "order_service", "CRITICAL", {},
     ["has:Severity.CRITICAL"]),
    ("/api/user/login", "user_service", "NORMAL",
     {"api_description": "用户登录", "param_remarks": {"username": "会员账号", "password": "登录密码"}},
     ["has:@allure.description", "has:用户登录", "has:- 接口地址：/api/user/login",
      "has:- username：会员账号", "has:- password：登录密码", "has:class TestClass:"]),
    ("/api/order/list", "order_service", None,
     {"api_headers": {"authorization": "bearer-token-value", "GW-Client": "test"}},
     ["has:@property", "has:def headers(self):",
      'has:"authorization": "bearer-token-value",',
      'has:"GW-Client": "test",']),
])
def test_generate_test_case_description(story_name, feature_name, severity, kwargs, checks):
    generator = TestCaseGenerator()
    call_args = {"severity": severity} if severity else {}
    call_args.update(kwargs)
    result = generator._generate_test_case_description(story_name, feature_name, **call_args)
    content = "\n".join(result)
    for check in checks:
        if check.startswith("has:"):
            assert check[4:] in content, f"Expected '{check[4:]}' in content"
        elif check.startswith("nothas:"):
            assert check[5:] not in content, f"Did not expect '{check[5:]}' in content"


# ==================== _generate_allure_description 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成 allure description")
@allure.title("测试 allure description 生成")
@pytest.mark.parametrize("api_url,api_desc,param_remarks,expected_has,expected_nothas", [
    ("/api/user/login", "用户登录", None, ["用户登录", "- 接口地址：/api/user/login"],
     ["主要参数说明"]),
    ("/api/order/create", "创建订单", {"productId": "产品ID", "quantity": "数量", "remark": ""},
     ["主要参数说明：", "- productId：产品ID", "- quantity：数量", "- remark：# TODO 请填写参数备注"],
     []),
    ("/api/test", "测试接口", None, [],
     ["主要参数说明"]),
])
def test_generate_allure_description(api_url, api_desc, param_remarks, expected_has, expected_nothas):
    generator = TestCaseGenerator()
    result = generator._generate_allure_description(api_url, api_description=api_desc, param_remarks=param_remarks)
    assert result.startswith('@allure.description("""')
    assert result.endswith('""")')
    for text in expected_has:
        assert text in result
    for text in expected_nothas:
        assert text not in result


# ==================== _generate_test_method_definition / assertions / _is_time_param 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成测试方法定义")
@allure.title("测试单/组合参数方法定义")
@pytest.mark.parametrize("param_name,is_combo,title_suffix,expected_in,expected_not_in", [
    ("keyword", False, "关键词", "keyword", None),
    ("startDate,endDate", True, "开始日期-结束日期", "startDate, endDate", None),
])
def test_generate_test_method_definition(param_name, is_combo, title_suffix, expected_in, expected_not_in):
    generator = TestCaseGenerator()
    remarks = {"keyword": "关键词", "startDate": "开始日期", "endDate": "结束日期"}
    result = generator._generate_test_method_definition(
        "列表查询", param_name, remarks, "api_func", 0, is_combo
    )
    content = "\n".join(result)
    assert expected_in in content
    assert "test_0_api_func" in content
    assert title_suffix in content


@allure.feature("测试用例生成器")
@allure.story("生成测试方法断言")
@allure.title("测试断言代码生成（含搜索条件验证分支）")
@pytest.mark.parametrize("func_name,param_var,param_name,should_have_search", [
    ("user_login", "data", None, False),
    ("order_list", "params", "orderNo", True),
    ("order_list", "params", "commitStartTime", False),
    ("order_list", "params", "startDate,endDate", False),
])
def test_generate_test_method_assertions(func_name, param_var, param_name, should_have_search):
    generator = TestCaseGenerator()
    result = generator._generate_test_method_assertions(func_name, param_var, param_name=param_name)
    content = "\n".join(result)
    assert f"{func_name}({param_var}={param_var}, headers=self.headers)" in content
    assert "assert r.status_code == 200" in content
    assert "r.json()" in content
    assert "assert data['code'] == 200" in content
    if should_have_search:
        assert "验证返回数据符合搜索条件" in content
        assert "items = resp_data.get('list', [])" in content
    else:
        assert "验证返回数据符合搜索条件" not in content


@allure.feature("测试用例生成器")
@allure.story("时间类参数判断")
@allure.title("测试时间类参数识别")
@pytest.mark.parametrize("name,expected", [
    ("commitStartTime", True), ("endTime", True), ("createDate", True), ("startTime", True),
    ("orderNo", False), ("pageNum", False), ("keyword", False),
])
def test_is_time_param(name, expected):
    assert TestCaseGenerator._is_time_param(name) == expected


# ==================== _generate_step_function_name 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数名")
@allure.title("测试步骤函数名生成（含去重）")
def test_generate_step_function_name():
    generator = TestCaseGenerator()
    name_counters = {}
    assert generator._generate_step_function_name("user_login", name_counters) == "step_user_login"
    assert generator._generate_step_function_name("user_login", name_counters) == "step_1_user_login"


# ==================== _generate_step_function_body 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数体")
@allure.title("测试生成步骤函数体")
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
    _write_api_sidecar(
        api_file,
        url="/api/user/login",
        description="用户登录",
        data={"username": "test", "password": "123456"},
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "user_login", api_info)
    result = "\n".join(content)
    assert "data =" in result
    assert "username" in result
    assert "user_login(data=data, headers=self.headers)" in result


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
    _write_api_sidecar(
        api_file,
        url="/api/user/list",
        description="用户列表",
        params={"keyword": "test", "pageNum": 1},
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "user_list", api_info)
    result = "\n".join(content)
    assert "params =" in result
    assert "keyword" in result
    assert "user_list(params=params, headers=self.headers)" in result


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
    _write_api_sidecar(api_file, url="/api/health", description="健康检查")

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "health_check", api_info)
    result = "\n".join(content)
    # 无参数时仍传 headers 覆盖模块级默认值
    assert "health_check(headers=self.headers)" in result


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
    _write_api_sidecar(
        api_file,
        url="/api/upload",
        description="文件上传",
        files={"file": "test.png"},
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "upload", api_info)
    result = "\n".join(content)
    assert "files =" in result
    assert "upload(files=files, headers=self.headers)" in result


# ==================== _build_step_headers_arg 测试 ====================


@allure.feature("测试用例生成器")
@allure.story("步骤 headers 差异处理")
@allure.title("测试步骤 headers 差异处理")
@pytest.mark.parametrize("class_headers,step_headers,expected_lines_count,expected_in,expected_not_in", [
    ({"channel": "pc", "authorization": 'f"bearer {os.environ[\'token\']}"'},
     {"channel": "pc", "authorization": 'f"bearer {os.environ[\'token\']}"'},
     0, "headers=self.headers", "**self.headers"),
    ({"channel": "pc", "GW-Client": "test"},
     {"channel": "pc", "GW-Client": "test", "content-type": "application/x-www-form-urlencoded; charset=UTF-8"},
     2, 'headers = {**self.headers, "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}', None),
    ({},
     {"authorization": 'f"bearer {os.environ[\'token\']}"', "content-type": "application/json"},
     2, "os.environ.get('token', '')", "**self.headers"),
])
def test_build_step_headers_arg(class_headers, step_headers, expected_lines_count, expected_in, expected_not_in):
    generator = TestCaseGenerator()
    generator._class_headers = class_headers
    lines, headers_arg = generator._build_step_headers_arg(step_headers)
    assert len(lines) == expected_lines_count
    header_output = "\n".join(lines)
    assert expected_in in (header_output if expected_in not in ("headers=self.headers",) else headers_arg)
    if expected_in == "headers=self.headers":
        assert headers_arg == "headers=self.headers"
    else:
        assert headers_arg == "headers=headers"
    if expected_not_in:
        assert expected_not_in not in header_output


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数体")
@allure.title("测试步骤 API 带额外 content-type 时生成局部 headers")
def test_generate_step_function_body_headers_diff(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "form_post.py"
    api_file.write_text(
        '''
import os

data = {"id": "1"}

headers = {
    "channel": "pc",
    "authorization": f"bearer {os.environ['token']}",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
}
def form_post(data=data, headers=headers):
    """
    表单提交
    /api/form
    """
    url = "/api/form"
    return client.post(url=url, data=data, headers=headers)
''',
        encoding="utf-8",
    )
    # 模块级 data/headers 现取自 .api.json 元数据（headers 存 f-string 源码片段）
    _write_api_sidecar(
        api_file,
        url="/api/form",
        description="表单提交",
        data={"id": "1"},
        headers={
            "channel": "pc",
            "authorization": 'f"bearer {os.environ[\'token\']}"',
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    # 类级别 headers（目标 API）不含 content-type
    generator._class_headers = {"channel": "pc", "authorization": 'f"bearer {os.environ[\'token\']}"'}
    api_info = generator._get_api_file_info(str(api_file))
    content = []
    generator._generate_step_function_body(content, "form_post", api_info)
    result = "\n".join(content)
    # 差异项生成局部覆盖
    assert 'headers = {**self.headers, "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}' in result
    assert "form_post(data=data, headers=headers)" in result


@allure.feature("测试用例生成器")
@allure.story("生成步骤函数体")
@allure.title("测试JSON数组请求体生成 data 字面量")
def test_generate_step_function_body_list_body(tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "behavior_collect.py"
    api_file.write_text(
        '''
import os

data = [{"app_id": "uc-pc", "type": "view"}]

headers = {
    "channel": "pc",
    "authorization": f"bearer {os.environ['token']}",
}
def behavior_collect(data=data, headers=headers):
    """
    行为采集
    /isomer/datacollect/behaviorCollect
    """
    url = "/isomer/datacollect/behaviorCollect"
    return client.post(url=url, json=data, headers=headers)
''',
        encoding="utf-8",
    )
    # API 默认 data 为 JSON 数组：快照进 .api.json 元数据的 data 字段
    _write_api_sidecar(
        api_file,
        url="/isomer/datacollect/behaviorCollect",
        description="行为采集",
        data=[{"app_id": "uc-pc", "type": "view"}],
        headers={
            "channel": "pc",
            "authorization": 'f"bearer {os.environ[\'token\']}"',
        },
    )

    generator = TestCaseGenerator(api_dir=str(api_dir))
    api_info = generator._get_api_file_info(str(api_file))

    # 场景1：HAR post_data 为 list，HAR 数组优先
    content = []
    generator._generate_step_function_body(
        content, "behavior_collect", api_info,
        ParsedRequestInfo(query_params={}, post_data=[{"app_id": "uc-pc", "type": "add_to_cart"}]),
    )
    result = "\n".join(content)
    assert "data = [{'app_id': 'uc-pc', 'type': 'add_to_cart'}]" in result or "data = [{\"app_id\": \"uc-pc\"" in result
    # 无类级别 headers 时生成完整 headers 字面量
    assert "behavior_collect(data=data, headers=headers) as r:" in result

    # 场景2：API 元数据 data 本身为 list，无 HAR 值时直接用 API 默认数组
    # （parse_api_file 只读 .api.json，无需重写 .py 或清理缓存）
    content = []
    generator._generate_step_function_body(content, "behavior_collect", api_info)
    result = "\n".join(content)
    assert "'type': 'view'" in result or '"type": "view"' in result
    assert "behavior_collect(data=data, headers=headers) as r:" in result


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


@pytest.fixture
def pagination_config(monkeypatch):
    """临时把 PAGINATION_PARAMS 设为 pageNum/pageSize（monkeypatch 自动恢复）。"""
    APIConfig.get_config("PAGINATION_PARAMS")  # 确保配置已加载
    # 取局部引用并断言，避免 IDE 把 APIConfig._config 判为 None 类型
    config = APIConfig._config
    assert config is not None
    monkeypatch.setitem(config, "PAGINATION_PARAMS", ["pageNum", "pageSize"])


@allure.feature("测试用例生成器")
@allure.story("标准化参数化")
@allure.title("测试标准化参数化-全部分页参数退化为单条默认项")
def test_normalize_params_all_pagination(pagination_config):
    generator = TestCaseGenerator()
    requests_params = [{"pageNum": 1, "pageSize": 20}, {"pageNum": 2, "pageSize": 20}]
    result = generator.normalize_params_for_parametrization(requests_params)
    # 过滤分页参数后没有有效参数：退化为一条以 pageNum 为变量的默认参数化项
    assert len(result) == 1
    assert list(result[0]) == ["pageNum", "other_params"]
    assert result[0]["pageNum"] == [1, 2]
    assert result[0]["other_params"] == {"pageSize": 20}


@allure.feature("测试用例生成器")
@allure.story("API目录校验")
@allure.title("测试API文件不在api_dir下时报错提示而非生成非法import")
def test_api_file_outside_api_dir_reports_error(tmp_path, caplog):
    api_dir = tmp_path / "apis"
    other_dir = tmp_path / "store_apis" / "mall_store_application"
    other_dir.mkdir(parents=True)
    api_file = other_dir / "appStore_invest.py"
    api_file.write_text("def appStore_invest(data=data, headers=headers):\n    pass\n", encoding="utf-8")
    _write_api_sidecar(
        api_file,
        url="/appStore/invest",
        description="充值",
        function_name="appStore_invest",
        data={"amount": 0},
    )

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path / "output"))
    assert generator._validate_api_dir(str(api_file)) is False
    with caplog.at_level(logging.ERROR):
        content = generator.generate_scenario_test_content(None, [str(api_file)], "t", str(api_file), None)
    assert content is None
    assert any("不在 --api-dir" in record.getMessage() for record in caplog.records)

    caplog.clear()
    with caplog.at_level(logging.ERROR):
        result = asyncio.run(generator.generate_batch_testcases([str(other_dir)], overwrite=True, har_file_path=None))
    assert result["generated"] == 0
    assert result["failed"] == 1
    assert any("--api-dir" in record.getMessage() for record in caplog.records)
    # 多个文件只汇总一条错误，避免刷屏
    assert len([r for r in caplog.records if "--api-dir" in r.getMessage()]) == 1


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试内容")
@allure.title("测试备注含换行符时生成的用例仍合法")
def test_generate_parametrized_content_multiline_remark(tmp_path, monkeypatch):
    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "giftOrder_pageQuery.py"
    api_file.write_text(
        "def giftOrder_pageQuery(data=data, headers=headers):\n    pass\n",
        encoding="utf-8",
    )
    _write_api_sidecar(
        api_file,
        url="/mgmt/activityGift/giftOrder/pageQuery",
        description="分页查询礼物订单活动列表",
        function_name="giftOrder_pageQuery",
        data={"orderStatusList": [], "receiverName": ""},
        param_remarks={
            "orderStatusList": "订单状态集合（参考OrderStatus枚举）：\n1:待支付, 2:待发货",
            "receiverName": "收礼人姓名",
        },
    )

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path / "output"))
    content = generator.generate_parametrized_test_content(None, str(api_file), "test_task")

    # 生成内容通过 validate_python 才会返回，None 说明仍是语法错误
    assert content is not None
    assert "@pytest.mark.test_list_query" in content
    assert "\n1:待支付" not in content
    for line in content.splitlines():
        assert not line.strip().startswith("1:待支付")


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试内容")
@allure.title("测试仅分页参数的列表接口生成单条参数化用例")
def test_generate_parametrized_content_pagination_only(tmp_path, pagination_config):
    """仅有 pageNum/pageSize 的列表接口应生成参数化用例，而不是告警后跳过。"""

    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "cms_activity_getActivityList.py"
    api_file.write_text(
        "def cms_activity_getActivityList(params=params, headers=headers):\n    pass\n",
        encoding="utf-8",
    )
    _write_api_sidecar(
        api_file,
        url="/cms/activity/getActivityList",
        description="活动列表",
        function_name="cms_activity_getActivityList",
        params={"pageNum": 1, "pageSize": 20},
    )

    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "/cms/activity/getActivityList?pageNum=1&pageSize=20",
                        "method": "GET",
                        "headers": [],
                        "queryString": [{"name": "pageNum", "value": "1"}, {"name": "pageSize", "value": "20"}],
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                },
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "/cms/activity/getActivityList?pageNum=3&pageSize=20",
                        "method": "GET",
                        "headers": [],
                        "queryString": [{"name": "pageNum", "value": "3"}, {"name": "pageSize", "value": "20"}],
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

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path / "output"))
    content = generator.generate_parametrized_test_content(str(har_file), str(api_file), "test_task")
    assert content is not None
    assert "@pytest.mark.test_list_query" in content
    assert "pytest.mark.parametrize" in content
    assert '"pageNum"' in content
    assert '"pageSize":' in content


@allure.feature("测试用例生成器")
@allure.story("生成参数化测试内容")
@allure.title("测试batch模式仅分页参数也生成参数化用例")
def test_generate_parametrized_content_pagination_only_batch(tmp_path, pagination_config):
    """无HAR的batch模式：API侧车仅有分页参数时也应生成单条默认参数化用例。"""

    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "cms_advert_getAdvertList.py"
    api_file.write_text(
        "def cms_advert_getAdvertList(params=params, headers=headers):\n    pass\n",
        encoding="utf-8",
    )
    _write_api_sidecar(
        api_file,
        url="/cms/advert/getAdvertList",
        description="广告列表",
        function_name="cms_advert_getAdvertList",
        params={"pageNum": 1, "pageSize": 10},
    )

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(tmp_path / "output"))
    content = generator.generate_parametrized_test_content(None, str(api_file), "test_task")
    assert content is not None
    assert "@pytest.mark.test_list_query" in content
    assert "pytest.mark.parametrize" in content
    assert '"pageNum"' in content
    assert '"pageSize":' in content


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
def test_generate_parametrized_list_testcases_no_match(tmp_path, write_har):

    har_file = write_har([_make_har_entry("/api/user/login", "POST")])

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
def test_generate_parametrized_list_testcases_overwrite(tmp_path, write_har):

    har_file = write_har([_make_har_entry(
        "https://example.com/api/user/list",
        headers=[{"name": "origin", "value": "https://example.com"}],
        query_string=[{"name": "keyword", "value": "test_value"}],
        time_ms=50,
    )])

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
    _write_api_sidecar(
        api_file,
        url="/api/user/list",
        description="用户列表",
        data={"keyword": ""},
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
def test_generate_scenario_testcase_no_match(tmp_path, write_har):

    har_file = write_har([_make_har_entry("/api/user/login", "POST")])

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
def test_generate_scenario_testcase_overwrite(tmp_path, write_har):

    har_file = write_har([_make_har_entry(
        "/api/user/login", "POST",
        headers=[{"name": "Content-Type", "value": "application/json"}],
        post_data={"mimeType": "application/json", "text": "{}"},
    )])

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
    _write_api_sidecar(api_dir / "user_login.py", url="/api/user/login", description="用户登录")

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
def test_generate_parametrized_list_testcases_multi_request(tmp_path, write_har):
    # 创建3条同URL但不同参数的请求
    _origin = [{"name": "origin", "value": "https://example.com"}]
    har_file = write_har([
        _make_har_entry("https://example.com/api/user/list", headers=_origin, query_string=[{"name": "status", "value": "1"}], time_ms=50),
        _make_har_entry("https://example.com/api/user/list", headers=_origin, query_string=[{"name": "status", "value": "2"}], time_ms=60),
        _make_har_entry("https://example.com/api/user/list", headers=_origin, query_string=[{"name": "status", "value": "3"}], time_ms=70),
    ])

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
    _write_api_sidecar(
        api_file,
        url="/api/user/list",
        description="用户列表",
        data={"status": 1},
    )

    output_dir = tmp_path / "output"

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


@allure.feature("测试用例生成器")
@allure.story("批量生成测试用例")
@allure.title("测试批量生成中无参数接口且匹配列表关键词时fallback到场景测试")
def test_generate_batch_no_param_list_keyword_fallback(tmp_path, caplog):
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
    # 模块级 headers 现取自 .api.json 元数据；描述含“列表”用于模式决策
    _write_api_sidecar(
        api_dir / "common_ProductProvenance.py",
        url="/common/ProductProvenance",
        description="获取商品发货信息列表",
        headers={"authorization": 'f"bearer {os.environ[\'token\']}"'},
    )

    output_dir = tmp_path / "output"

    caplog.set_level(logging.INFO)
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
    # 回退场景模式属正常路径：不得出现“没有有效的测试参数”之类的 WARNING
    noise = [
        record
        for record in caplog.records
        if record.levelno >= logging.WARNING and "参数" in record.getMessage()
    ]
    assert noise == []
    # 同时确认日志确实被捕获（INFO 记录“回退场景模式”）
    assert any("回退场景模式" in record.getMessage() for record in caplog.records)


@allure.feature("测试用例生成器")
@allure.story("批量生成")
@allure.title("测试 batch 已存在测试文件时计入 skipped")
def test_generate_batch_skipped_count(tmp_path):
    api_dir = tmp_path / "apis"
    api_dir.mkdir()
    api_file = api_dir / "user_login.py"
    api_file.write_text(
        'params = {"keyword": "test"}\n\ndef user_login(params=params):\n    """\n    用户登录\n    /user/login\n    """\n',
        encoding="utf-8",
    )
    _write_api_sidecar(
        api_file,
        url="/user/login",
        description="用户登录",
        params={"keyword": "test"},
    )

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    (output_dir / "test_user_login.py").write_text("# already exists", encoding="utf-8")

    generator = TestCaseGenerator(api_dir=str(api_dir), output_dir=str(output_dir))
    result = asyncio.run(generator.generate_batch_testcases([str(api_file)], overwrite=False, har_file_path=None))

    assert result["total"] == 1
    assert result["skipped"] == 1
    assert result["generated"] == 0
    assert result["failed"] == 0


@allure.feature("测试用例生成器")
@allure.story("生成参数化列表测试用例")
@allure.title("测试参数化模式下无参数时fallback到场景测试")
def test_generate_parametrized_list_no_param_fallback(tmp_path, write_har):
    har_file = write_har([_make_har_entry("/common/ProductProvenance", time_ms=50)])

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
    _write_api_sidecar(
        api_dir / "common_ProductProvenance.py",
        url="/common/ProductProvenance",
        description="获取商品发货信息列表",
        headers={"authorization": 'f"test {os.environ[\'token\']}"'},
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


@allure.feature("测试用例生成器")
@allure.story("批量生成测试用例")
@allure.title("测试描述含排除关键字时不使用参数化列表模式")
def test_generate_batch_list_query_exclude_keywords(tmp_path, write_har):
    # HAR：/api/order/list 和 /api/order/detail 各两条不同参数的请求
    def _entry(url, name, value):
        return {
            "_resourceType": "xhr",
            "request": {
                "url": url,
                "method": "GET",
                "headers": [],
                "queryString": [{"name": name, "value": value}],
            },
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 50,
        }

    har_file = write_har([
        _entry("https://example.com/api/order/list", "status", "1"),
        _entry("https://example.com/api/order/list", "status", "2"),
        _entry("https://example.com/api/order/detail", "id", "100"),
        _entry("https://example.com/api/order/detail", "id", "200"),
    ])

    api_dir = tmp_path / "apis"
    api_dir.mkdir(parents=True)
    # 描述命中“查询”且不含排除关键字 → 应参数化
    (api_dir / "order_list.py").write_text(
        '''
data = {"status": 1}

def order_list(data=data):
    """
    查询订单列表
    /api/order/list
    """
    url = "/api/order/list"
    return client.get(url=url, params=data)
''',
        encoding="utf-8",
    )
    _write_api_sidecar(
        api_dir / "order_list.py",
        url="/api/order/list",
        description="查询订单列表",
        data={"status": 1},
    )
    # 描述同时命中“查询”和排除关键字“详情” → 应使用场景模式
    (api_dir / "order_detail.py").write_text(
        '''
data = {"id": 100}

def order_detail(data=data):
    """
    查询订单详情
    /api/order/detail
    """
    url = "/api/order/detail"
    return client.get(url=url, params=data)
''',
        encoding="utf-8",
    )
    _write_api_sidecar(
        api_dir / "order_detail.py",
        url="/api/order/detail",
        description="查询订单详情",
        data={"id": 100},
    )

    # 覆盖配置：列表关键字 + 排除关键字
    APIConfig.get_config("LIST_QUERY_KEYWORDS")
    assert APIConfig._config is not None
    orig_kw = APIConfig._config.get("LIST_QUERY_KEYWORDS")
    orig_ex = APIConfig._config.get("LIST_QUERY_EXCLUDE_KEYWORDS")
    APIConfig._config["LIST_QUERY_KEYWORDS"] = ["列表", "查询"]
    APIConfig._config["LIST_QUERY_EXCLUDE_KEYWORDS"] = ["详情"]
    try:
        output_dir = tmp_path / "output"
        generator = TestCaseGenerator(
            api_dir=str(api_dir), output_dir=str(output_dir), base_urls=["https://example.com"]
        )
        result = asyncio.run(
            generator.generate_batch_testcases(
                [str(api_dir)], task_id="test_task", overwrite=True, har_file_path=str(har_file)
            )
        )
        assert result["generated"] == 2

        contents = {}
        for fp in result["generated_files"]:
            with open(fp, encoding="utf-8") as f:
                contents[os.path.basename(fp)] = f.read()

        # 对照组：无排除关键字 → 参数化模式
        assert "pytest.mark.parametrize" in contents["test_order_list.py"]
        # 实验组：含“详情”排除关键字 → 场景模式（无参数化，含步骤函数）
        detail_content = contents["test_order_detail.py"]
        assert "pytest.mark.parametrize" not in detail_content
        assert "step_" in detail_content
    finally:
        APIConfig._config["LIST_QUERY_KEYWORDS"] = orig_kw
        APIConfig._config["LIST_QUERY_EXCLUDE_KEYWORDS"] = orig_ex


# ==================== 异步 / 同步模式测试 ====================


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试 async/sync 模式生成测试方法定义")
@pytest.mark.parametrize("async_mode,expected", [
    (True, "async def test_user_login(self):"),
    (False, "def test_user_login(self):"),
])
def test_scenario_test_method_definition_mode(async_mode, expected, tmp_path):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True)
    (api_dir / "user_login.py").write_text(
        "\ndef user_login(data=data):\n    \"\"\"\n    test\n    /api/login\n    \"\"\"\n    url = \"/api/login\"\n    return client.post(url=url, json=data)\n",
        encoding="utf-8",
    )
    _write_api_sidecar(api_dir / "user_login.py", url="/api/login", description="test")

    generator = TestCaseGenerator(api_dir=str(api_dir), async_mode=async_mode)
    result = generator._generate_scenario_test_method_definition(str(api_dir / "user_login.py"))
    content = "\n".join(result)
    assert expected in content
    if not async_mode:
        assert "async def" not in content


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试 async/sync 模式步骤函数体")
@pytest.mark.parametrize("async_mode,expected_keyword,unexpected_keyword", [
    (True, "async with", None),
    (False, "with", "async with"),
])
def test_step_function_body_mode(async_mode, expected_keyword, unexpected_keyword):
    generator = TestCaseGenerator(api_dir="apis", async_mode=async_mode)
    content = []
    generator._generate_step_function_body(
        content, "user_login", APIFileInfo(data={"name": ""}),
        ParsedRequestInfo(query_params={}, post_data={"name": "test"})
    )
    result = "\n".join(content)
    assert f"{expected_keyword} user_login(data=data, headers=self.headers) as r:" in result
    if unexpected_keyword:
        assert unexpected_keyword not in result


@allure.feature("测试用例生成器")
@allure.story("异步模式")
@allure.title("测试 async/sync 模式导入语句")
@pytest.mark.parametrize("async_mode,should_contain,should_not_contain", [
    (True, "from har2pytest.client import client, async_client", None),
    (False, None, "client.set_client"),
])
def test_imports_mode(async_mode, should_contain, should_not_contain):
    generator = TestCaseGenerator(api_dir="apis", async_mode=async_mode)
    result = generator._generate_test_case_imports(
        service_package="test_service", function_name="test_api"
    )
    content = "\n".join(result)
    if should_contain:
        assert should_contain in content
        assert "client.set_client(async_client)" in content
    if should_not_contain:
        assert should_not_contain not in content
