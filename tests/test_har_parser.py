"""
测试 har_parser.py 模块
"""

import json
import logging
import os

import allure

from har2pytest.har_parser import HARParser


@allure.feature("HAR解析器")
@allure.story("提取请求信息")
@allure.title("测试从HAR文件提取请求信息")
def test_extract_requests_from_har():
    from har2pytest.config import APIConfig

    APIConfig.get_config("BASE_URLS")

    original_base_urls = APIConfig._config.get("BASE_URLS", [])
    APIConfig._config["BASE_URLS"] = ["https://taobao.com/api"]

    test_har = {
        "log": {
            "entries": [
                {
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
                }
            ]
        }
    }

    with open("test.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test.har")

        assert len(requests) == 1
        assert requests[0]["method"] == "POST"
        assert requests[0]["url"] == "/user/login"
        assert requests[0]["response_status"] == 200
    finally:
        APIConfig._config["BASE_URLS"] = original_base_urls

        if os.path.exists("test.har"):
            os.remove("test.har")


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
@allure.title("测试过滤无效参数")
def test_filter_invalid_params():
    from har2pytest.config import APIConfig

    APIConfig.get_config("INVALID_PARAMS")

    original_invalid_params = APIConfig._config.get("INVALID_PARAMS", set())
    APIConfig._config["INVALID_PARAMS"] = {"sign", "timestamp"}

    try:
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
    finally:
        APIConfig._config["INVALID_PARAMS"] = original_invalid_params


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
def test_invalid_json():
    with open("invalid.har", "w", encoding="utf-8") as f:
        f.write("invalid json")

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("invalid.har")
        assert len(requests) == 0
    finally:
        if os.path.exists("invalid.har"):
            os.remove("invalid.har")


@allure.feature("HAR解析器")
@allure.story("过滤Headers")
@allure.title("测试过滤Headers功能")
def test_filter_headers():
    from har2pytest.config import APIConfig

    APIConfig.get_config("HEADERS_TO_INCLUDE")

    original_headers = APIConfig._config.get("HEADERS_TO_INCLUDE", [])
    APIConfig._config["HEADERS_TO_INCLUDE"] = ["content-type", "authorization"]

    try:
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
    finally:
        APIConfig._config["HEADERS_TO_INCLUDE"] = original_headers


@allure.feature("HAR解析器")
@allure.story("过滤Headers-无配置")
@allure.title("测试没有配置HEADERS_TO_INCLUDE时返回所有headers")
def test_filter_headers_no_config():
    from har2pytest.config import APIConfig

    APIConfig.get_config("HEADERS_TO_INCLUDE")

    original_headers = APIConfig._config.get("HEADERS_TO_INCLUDE", [])
    APIConfig._config["HEADERS_TO_INCLUDE"] = []

    try:
        parser = HARParser()

        test_headers = {"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}

        result = parser._filter_headers(test_headers)
        assert result == test_headers
    finally:
        APIConfig._config["HEADERS_TO_INCLUDE"] = original_headers


@allure.feature("HAR解析器")
@allure.story("过滤Headers-非字典输入")
@allure.title("测试非字典输入时的处理")
def test_filter_headers_invalid_input():
    parser = HARParser()

    result = parser._filter_headers(None)
    assert result is None

    result = parser._filter_headers("invalid")
    assert result == "invalid"


@allure.feature("HAR解析器")
@allure.story("打印API摘要")
@allure.title("测试打印API摘要功能")
def test_print_api_summary(caplog):
    caplog.set_level(logging.INFO)
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {"url": "https://example.com/api/user/login", "method": "POST", "headers": []},
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                    "serverIPAddress": "127.0.0.1",
                }
            ]
        }
    }

    with open("test_summary.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        parser.print_api_summary("test_summary.har")
        log_output = "\n".join([r.message for r in caplog.records])
        assert "共发现" in log_output or "个API请求" in log_output
    finally:
        if os.path.exists("test_summary.har"):
            os.remove("test_summary.har")


@allure.feature("HAR解析器")
@allure.story("打印API摘要-空请求")
@allure.title("测试空请求时的摘要打印")
def test_print_api_summary_empty(caplog):
    caplog.set_level(logging.INFO)
    test_har = {"log": {"entries": []}}

    with open("test_empty.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        parser.print_api_summary("test_empty.har")
        log_output = "\n".join([r.message for r in caplog.records])
        assert "共发现" in log_output or "没有找到" in log_output
    finally:
        if os.path.exists("test_empty.har"):
            os.remove("test_empty.har")


@allure.feature("HAR解析器")
@allure.story("Multipart/form-data处理")
@allure.title("测试multipart/form-data类型的POST数据解析")
def test_multipart_form_data():
    test_har = {
        "log": {
            "entries": [
                {
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
                }
            ]
        }
    }

    with open("test_multipart.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test_multipart.har")

        assert len(requests) == 1
        assert requests[0]["post_data"] == {"file": "test.txt", "name": "test"}
    finally:
        if os.path.exists("test_multipart.har"):
            os.remove("test_multipart.har")


@allure.feature("HAR解析器")
@allure.story("application/x-www-form-urlencoded处理")
@allure.title("测试application/x-www-form-urlencoded类型的POST数据解析")
def test_form_urlencoded_data():
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/login",
                        "method": "POST",
                        "headers": [
                            {"name": "Content-Type", "value": "application/x-www-form-urlencoded"}
                        ],
                        "postData": {
                            "mimeType": "application/x-www-form-urlencoded",
                            "text": "username=testuser&password=123456&remember=true",
                        },
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    with open("test_form_urlencoded.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test_form_urlencoded.har")

        assert len(requests) == 1
        assert requests[0]["post_data"] == {"username": "testuser", "password": "123456", "remember": "true"}
    finally:
        if os.path.exists("test_form_urlencoded.har"):
            os.remove("test_form_urlencoded.har")


@allure.feature("HAR解析器")
@allure.story("application/x-www-form-urlencoded处理")
@allure.title("测试urlencoded带URL编码字符的解析")
def test_form_urlencoded_with_encoded_chars():
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/search",
                        "method": "POST",
                        "headers": [
                            {"name": "Content-Type", "value": "application/x-www-form-urlencoded"}
                        ],
                        "postData": {
                            "mimeType": "application/x-www-form-urlencoded",
                            "text": "keyword=%E6%B5%8B%E8%AF%95&page=1&size=10",
                        },
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    with open("test_form_urlencoded2.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test_form_urlencoded2.har")

        assert len(requests) == 1
        assert requests[0]["post_data"] == {"keyword": "测试", "page": "1", "size": "10"}
    finally:
        if os.path.exists("test_form_urlencoded2.har"):
            os.remove("test_form_urlencoded2.har")


@allure.feature("HAR解析器")
@allure.story("application/x-www-form-urlencoded处理")
@allure.title("测试urlencoded空数据的解析")
def test_form_urlencoded_empty():
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/submit",
                        "method": "POST",
                        "headers": [
                            {"name": "Content-Type", "value": "application/x-www-form-urlencoded"}
                        ],
                        "postData": {
                            "mimeType": "application/x-www-form-urlencoded",
                            "text": "",
                        },
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    with open("test_form_urlencoded3.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test_form_urlencoded3.har")

        assert len(requests) == 1
        assert requests[0]["post_data"] == {}
    finally:
        if os.path.exists("test_form_urlencoded3.har"):
            os.remove("test_form_urlencoded3.har")


@allure.feature("HAR解析器")
@allure.story("Kill URLs过滤")
@allure.title("测试kill_urls过滤功能")
def test_kill_urls_filter():
    test_har = {
        "log": {
            "entries": [
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
            ]
        }
    }

    with open("test_kill_urls.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser(kill_urls=["health"])
        requests = parser.extract_requests_from_har("test_kill_urls.har")

        assert len(requests) == 1
        assert "/user/list" in requests[0]["url"]
    finally:
        if os.path.exists("test_kill_urls.har"):
            os.remove("test_kill_urls.har")


@allure.feature("HAR解析器")
@allure.story("重复URL过滤")
@allure.title("测试重复URL过滤功能")
def test_duplicate_url_filter():
    test_har = {
        "log": {
            "entries": [
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
            ]
        }
    }

    with open("test_duplicate.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test_duplicate.har")
        assert len(requests) == 1

        requests = parser.extract_requests_from_har("test_duplicate.har", filter_duplicate_url=False)
        assert len(requests) == 2
    finally:
        if os.path.exists("test_duplicate.har"):
            os.remove("test_duplicate.har")


@allure.feature("HAR解析器")
@allure.story("Origin Header作为base URL")
@allure.title("测试当没有配置base_urls时使用origin header")
def test_origin_as_base_url():
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/login",
                        "method": "POST",
                        "headers": [{"name": "origin", "value": "https://example.com"}],
                        "postData": {"mimeType": "application/json", "text": "{}"},
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    with open("test_origin.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser(base_urls=[])
        requests = parser.extract_requests_from_har("test_origin.har")

        assert len(requests) == 1
        assert requests[0]["url"] == "/api/user/login"
    finally:
        if os.path.exists("test_origin.har"):
            os.remove("test_origin.har")


@allure.feature("HAR解析器")
@allure.story("响应内容解析")
@allure.title("测试响应内容解析")
def test_response_content_parsing():
    test_har = {
        "log": {
            "entries": [
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
            ]
        }
    }

    with open("test_response.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test_response.har")

        assert len(requests) == 2
        assert requests[0]["response_content"] == {"code": 0, "data": "success"}
        assert requests[1]["response_content"] == "plain text response"
    finally:
        if os.path.exists("test_response.har"):
            os.remove("test_response.har")