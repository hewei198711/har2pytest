"""测试 har2pytest.har_parser 模块中 HAR 文件解析、请求过滤、参数清洗与 API 摘要输出的功能与边界。"""

import json
import logging

import allure
import pytest

from har2pytest.config import APIConfig
from har2pytest.har_parser import HARParser

# ==================== Fixtures ====================


@pytest.fixture(autouse=True)
def _restore_config():
    """每个测试前后自动保存/恢复 APIConfig 配置，确保测试间隔离。"""
    APIConfig._config = APIConfig._load_config()  # 确保配置已加载
    original = APIConfig._config
    yield
    APIConfig._config = original


@pytest.fixture
def write_har(tmp_path):
    """工厂 fixture：将 entries 列表写入临时 HAR 文件并返回路径。"""
    def _write(entries, filename="test.har"):
        har_data = {"log": {"entries": entries}}
        har_path = tmp_path / filename
        har_path.write_text(json.dumps(har_data, ensure_ascii=False), encoding="utf-8")
        return har_path
    return _write


# ==================== HAR 解析测试 ====================


@allure.feature("HAR解析器")
@allure.story("提取请求信息")
@allure.title("测试从HAR文件提取请求信息")
def test_extract_requests_from_har(write_har):
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["BASE_URLS"] = ["https://taobao.com/api"]

    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://taobao.com/api/user/login",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/json"}],
            "postData": {
                "mimeType": "application/json",
                "text": '{"username": "test", "password": "123456"}',
            },
        },
        "response": {"status": 200, "content": {"text": '{"code": 0, "message": "success"}'}},
        "time": 100,
    }])

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert requests[0].url == "/user/login"
    assert requests[0].response_status == 200


@allure.feature("HAR解析器")
@allure.story("提取请求信息")
@allure.title("测试提取 cookies")
def test_extract_cookies(write_har):
    har_path = write_har([{
        "request": {
            "url": "https://example.com/api/user",
            "method": "GET",
            "headers": [],
            "queryString": [],
            "cookies": [{"name": "sid", "value": "abc123"}],
        },
        "response": {"status": 200, "content": {"text": "{}"}},
    }], filename="cookies.har")
    parser = HARParser(base_urls=["https://example.com"], kill_urls=[])
    requests = parser.extract_requests_from_har(str(har_path))
    assert len(requests) == 1
    assert requests[0].cookies == {"sid": "abc123"}


@allure.feature("HAR解析器")
@allure.story("提取请求信息")
@allure.title("测试缺失 _resourceType 时默认按 xhr 保留")
def test_missing_resource_type_defaults_to_xhr(write_har):
    har_path = write_har([{
        "request": {
            "url": "https://example.com/api/user",
            "method": "GET",
            "headers": [],
            "queryString": [],
        },
        "response": {"status": 200, "content": {"text": "{}"}},
    }], filename="no_restype.har")
    parser = HARParser(base_urls=["https://example.com"], kill_urls=[])
    requests = parser.extract_requests_from_har(str(har_path))
    assert len(requests) == 1


@allure.feature("HAR解析器")
@allure.story("过滤非 API 请求")
@allure.title("测试非 xhr/fetch 资源被跳过")
def test_filter_non_api_resource_type(write_har):
    har_path = write_har([
        {"_resourceType": "image", "request": {"url": "https://example.com/a.png", "method": "GET", "headers": [], "queryString": []}},
        {"_resourceType": "xhr", "request": {"url": "https://example.com/api/list", "method": "GET", "headers": [], "queryString": []}},
    ], filename="res.har")
    parser = HARParser(base_urls=["https://example.com"], kill_urls=[])
    requests = parser.extract_requests_from_har(str(har_path))
    assert len(requests) == 1
    assert requests[0].url == "/api/list"


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
@allure.title("测试过滤无效参数")
def test_filter_invalid_params():
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["INVALID_PARAMS"] = {"sign", "timestamp"}
    parser = HARParser()

    test_data = {
        "username": "test",
        "password": "123456",
        "sign": "test_sign",
        "timestamp": "1234567890",
        "file": "test.txt",
    }

    result = parser._filter_invalid_params(test_data)
    assert "username" in result
    assert "password" in result
    assert "sign" not in result
    assert "timestamp" not in result
    assert "file" in result


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
@allure.title("测试过滤JSON数组body中的无效参数")
def test_filter_invalid_params_list():
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["INVALID_PARAMS"] = {"sign", "timestamp"}
    parser = HARParser()

    test_data = [
        {"productId": 1, "sign": "abc"},
        {"productId": 2, "sign": "def", "timestamp": "123"},
    ]

    result = parser._filter_invalid_params(test_data)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == {"productId": 1}
    assert result[1] == {"productId": 2}


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
@allure.title("测试过滤空列表")
def test_filter_invalid_params_empty_list():
    parser = HARParser()
    result = parser._filter_invalid_params([])
    assert result == []


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
@allure.title("测试过滤混合类型列表")
def test_filter_invalid_params_mixed_list():
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["INVALID_PARAMS"] = {"sign"}
    parser = HARParser()

    test_data = [
        {"id": 1, "sign": "x"},
        "plain_string",
        42,
        [{"inner": 1, "sign": "y"}],
    ]

    result = parser._filter_invalid_params(test_data)
    assert isinstance(result, list)
    assert len(result) == 4
    assert result[0] == {"id": 1}
    assert result[1] == "plain_string"
    assert result[2] == 42
    assert result[3] == [{"inner": 1}]


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
@allure.title("测试过滤嵌套 dict 中的无效参数")
def test_filter_invalid_params_nested_dict():
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["INVALID_PARAMS"] = {"sign", "token"}
    parser = HARParser()
    test_data = {
        "order": {
            "sign": "x",
            "items": [
                {"sku": "A", "token": "t1"},
                {"sku": "B"},
            ],
            "meta": {"token": "nested"},
        }
    }
    result = parser._filter_invalid_params(test_data)
    assert result == {"order": {"items": [{"sku": "A"}, {"sku": "B"}], "meta": {}}}


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
@allure.title("测试非容器标量原样保留")
def test_filter_invalid_params_scalar_preserved():
    parser = HARParser()
    assert parser._filter_invalid_params(None) is None
    assert parser._filter_invalid_params(0) == 0
    assert parser._filter_invalid_params("") == ""


@allure.feature("HAR解析器")
@allure.story("文件不存在处理")
@allure.title("测试文件不存在的情况")
def test_file_not_found():
    parser = HARParser()
    requests = parser.extract_requests_from_har("nonexistent.har")
    assert len(requests) == 0


@allure.feature("HAR解析器")
@allure.story("无效JSON处理")
@allure.title("测试无效JSON的情况")
def test_invalid_json(tmp_path):
    invalid_path = tmp_path / "invalid.har"
    invalid_path.write_text("invalid json", encoding="utf-8")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(invalid_path))
    assert len(requests) == 0


@allure.feature("HAR解析器")
@allure.story("过滤Headers")
@allure.title("测试过滤Headers功能")
def test_filter_headers():
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["HEADERS_TO_INCLUDE"] = {"content-type": "", "authorization": ""}
    parser = HARParser()

    test_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token123",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://example.com",
        "User-Agent": "test-agent",
        "content-length": "100",
    }

    result = parser._filter_headers(test_headers)
    assert "Content-Type" in result
    assert "Authorization" in result
    assert "content-length" in result
    assert "Origin" not in result
    assert "X-Requested-With" not in result
    assert "User-Agent" not in result


@allure.feature("HAR解析器")
@allure.story("过滤Headers-无配置")
@allure.title("测试没有配置HEADERS_TO_INCLUDE时返回所有headers")
def test_filter_headers_no_config():
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["HEADERS_TO_INCLUDE"] = {}
    parser = HARParser()

    test_headers = {"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}
    result = parser._filter_headers(test_headers)
    assert result == test_headers


@allure.feature("HAR解析器")
@allure.story("过滤Headers")
@allure.title("测试 REQUIRED_HEADERS 大小写不敏感(必需头不被误滤)")
def test_filter_headers_required_case_insensitive():
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["HEADERS_TO_INCLUDE"] = {"channel": ""}
    APIConfig._config["REQUIRED_HEADERS"] = {"Authorization": "x"}
    parser = HARParser()
    test_headers = {"channel": "pc", "Authorization": "Bearer t", "X-Other": "x"}
    result = parser._filter_headers(test_headers)
    assert "channel" in result
    assert "Authorization" in result
    assert "X-Other" not in result


@allure.feature("HAR解析器")
@allure.story("打印API摘要")
@allure.title("测试打印API摘要功能")
def test_print_api_summary(write_har, caplog):
    caplog.set_level(logging.INFO)
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {"url": "https://example.com/api/user/login", "method": "POST", "headers": []},
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 100,
        "serverIPAddress": "127.0.0.1",
    }], filename="test_summary.har")

    parser = HARParser()
    parser.print_api_summary(str(har_path))
    log_output = "\n".join([r.message for r in caplog.records])
    assert "共发现" in log_output or "个API请求" in log_output


@allure.feature("HAR解析器")
@allure.story("打印API摘要-空请求")
@allure.title("测试空请求时的摘要打印")
def test_print_api_summary_empty(write_har, caplog):
    caplog.set_level(logging.INFO)
    har_path = write_har([], filename="test_empty.har")

    parser = HARParser()
    parser.print_api_summary(str(har_path))
    log_output = "\n".join([r.message for r in caplog.records])
    assert "共发现" in log_output or "没有找到" in log_output


@allure.feature("HAR解析器")
@allure.story("Multipart/form-data处理")
@allure.title("测试multipart/form-data类型的POST数据解析")
def test_multipart_form_data(write_har):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/upload",
            "method": "POST",
            "headers": [
                {"name": "Content-Type", "value": "multipart/form-data; boundary=----WebKitFormBoundary"}
            ],
            "postData": {
                "mimeType": "multipart/form-data",
                "params": [{"name": "file", "value": "test.txt"}, {"name": "name", "value": "test"}],
            },
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 100,
    }], filename="test_multipart.har")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].post_data == {"file": "test.txt", "name": "test"}


@allure.feature("HAR解析器")
@allure.story("application/x-www-form-urlencoded处理")
@allure.title("测试application/x-www-form-urlencoded类型的POST数据解析")
def test_form_urlencoded_data(write_har):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/login",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/x-www-form-urlencoded"}],
            "postData": {
                "mimeType": "application/x-www-form-urlencoded",
                "text": "username=testuser&password=123456&remember=true",
            },
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 100,
    }], filename="test_form_urlencoded.har")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].post_data == {"username": "testuser", "password": "123456", "remember": "true"}


@allure.feature("HAR解析器")
@allure.story("application/x-www-form-urlencoded处理")
@allure.title("测试urlencoded带URL编码字符的解析")
def test_form_urlencoded_with_encoded_chars(write_har):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/search",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/x-www-form-urlencoded"}],
            "postData": {
                "mimeType": "application/x-www-form-urlencoded",
                "text": "keyword=%E6%B5%8B%E8%AF%95&page=1&size=10",
            },
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 50,
    }], filename="test_form_urlencoded2.har")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].post_data == {"keyword": "测试", "page": "1", "size": "10"}


@allure.feature("HAR解析器")
@allure.story("application/x-www-form-urlencoded处理")
@allure.title("测试urlencoded空数据的解析")
def test_form_urlencoded_empty(write_har):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/submit",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/x-www-form-urlencoded"}],
            "postData": {
                "mimeType": "application/x-www-form-urlencoded",
                "text": "",
            },
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 50,
    }], filename="test_form_urlencoded3.har")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].post_data == {}


@allure.feature("HAR解析器")
@allure.story("application/x-www-form-urlencoded处理")
@allure.title("测试urlencoded仅有params无text时回退结构化解析")
@allure.description("部分 HAR 导出只提供 postData.params（无 text），应回退结构化解析而不丢参数")
def test_form_urlencoded_params_only(write_har):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/form",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/x-www-form-urlencoded"}],
            "postData": {
                "mimeType": "application/x-www-form-urlencoded",
                "params": [
                    {"name": "username", "value": "testuser"},
                    {"name": "password", "value": "123456"},
                ],
            },
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 50,
    }], filename="test_form_urlencoded_params_only.har")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].post_data == {"username": "testuser", "password": "123456"}


@allure.feature("HAR解析器")
@allure.story("kill_urls过滤")
@allure.title("测试kill_urls过滤功能")
def test_kill_urls_filter(write_har):
    har_path = write_har([
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/health", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 50,
        },
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/user/list", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 100,
        },
    ], filename="test_kill_urls.har")

    parser = HARParser(kill_urls=["health"])
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert "/user/list" in requests[0].url


@allure.feature("HAR解析器")
@allure.story("重复URL过滤")
@allure.title("测试重复URL过滤功能")
def test_duplicate_url_filter(write_har):
    har_path = write_har([
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/user/list", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 100,
        },
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/user/list", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 150,
        },
    ], filename="test_duplicate.har")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))
    assert len(requests) == 1

    requests = parser.extract_requests_from_har(str(har_path), filter_duplicate_url=False)
    assert len(requests) == 2


@allure.feature("HAR解析器")
@allure.story("Origin Header作为base URL")
@allure.title("测试当没有配置base_urls时使用origin header")
def test_origin_as_base_url(write_har):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/user/login",
            "method": "POST",
            "headers": [{"name": "origin", "value": "https://example.com"}],
            "postData": {"mimeType": "application/json", "text": "{}"},
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 100,
    }], filename="test_origin.har")

    parser = HARParser(base_urls=[])
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].url == "/api/user/login"


@allure.feature("HAR解析器")
@allure.story("响应内容解析")
@allure.title("测试响应内容解析")
def test_response_content_parsing(write_har):
    har_path = write_har([
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/test", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": '{"code": 0, "data": "success"}'}},
            "time": 50,
        },
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/text", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "plain text response"}},
            "time": 30,
        },
    ], filename="test_response.har")

    parser = HARParser()
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 2
    assert requests[0].response_content == {"code": 0, "data": "success"}
    assert requests[1].response_content == "plain text response"


# ==================== 边界与遗漏场景测试 ====================


@allure.feature("HAR解析器")
@allure.story("不支持的Content-Type")
@allure.title("测试不支持的 Content-Type 时跳过该请求")
def test_unsupported_content_type_skipped(write_har):
    har_path = write_har([
        {
            "_resourceType": "xhr",
            "request": {
                "url": "https://example.com/api/data",
                "method": "POST",
                "headers": [{"name": "Content-Type", "value": "text/xml"}],
                "postData": {"mimeType": "text/xml", "text": "<data>test</data>"},
            },
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 50,
        },
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/list", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 30,
        },
    ])

    parser = HARParser(base_urls=["https://example.com"], kill_urls=[])
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].url == "/api/list"


@allure.feature("HAR解析器")
@allure.story("URL规范化")
@allure.title("测试无 base_urls 且无 origin 时 URL 仍去掉查询参数")
def test_normalize_url_no_base_no_origin(write_har):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/search?keyword=test&page=1",
            "method": "GET",
            "headers": [],
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 30,
    }])

    parser = HARParser(base_urls=[], kill_urls=[])
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert "?" not in requests[0].url
    assert requests[0].url.startswith("/")


@allure.feature("HAR解析器")
@allure.story("打印API摘要")
@allure.title("测试 print_api_summary 完整统计输出")
def test_print_api_summary_statistics(write_har, caplog):
    caplog.set_level(logging.INFO)
    har_path = write_har([
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/ok", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 100,
        },
        {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/fail", "method": "GET", "headers": []},
            "response": {"status": 500, "content": {"text": "{}"}},
            "time": 200,
        },
    ], filename="test_stats.har")

    parser = HARParser()
    parser.print_api_summary(str(har_path))
    log_output = "\n".join(r.message for r in caplog.records)

    assert "共发现 2 个API请求" in log_output
    assert "成功 1 个" in log_output
    assert "失败 1 个" in log_output
    assert "平均响应时间" in log_output


@allure.feature("HAR解析器")
@allure.story("queryString解析")
@allure.title("测试 queryString 解析并过滤无效参数")
def test_query_string_parsing_and_filtering(write_har):
    from har2pytest.config import APIConfig

    assert APIConfig._config is not None
    APIConfig._config["INVALID_PARAMS"] = {"sign"}

    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/search",
            "method": "GET",
            "headers": [],
            "queryString": [
                {"name": "keyword", "value": "%E6%B5%8B%E8%AF%95"},
                {"name": "sign", "value": "abc123"},
                {"name": "page", "value": "1"},
            ],
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 30,
    }])

    parser = HARParser(base_urls=["https://example.com"], kill_urls=[])
    requests = parser.extract_requests_from_har(str(har_path))

    assert len(requests) == 1
    assert requests[0].query_params == {"keyword": "测试", "page": "1"}
    assert "sign" not in requests[0].query_params
