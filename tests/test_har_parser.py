"""
测试 har_parser.py 模块
"""

import json
import os

import allure

from har2pytest.har_parser import HARParser


@allure.feature("HAR解析器")
@allure.story("提取请求信息")
def test_extract_requests_from_har():
    """测试从HAR文件提取请求信息"""
    from har2pytest.config import APIConfig

    # 触发配置初始化
    APIConfig.get_config("BASE_URLS")

    # 临时设置 BASE_URLS 配置
    original_base_urls = APIConfig._config.get("BASE_URLS", [])
    APIConfig._config["BASE_URLS"] = ["https://uc-test.perfect99.com/api"]

    # 创建测试HAR文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://uc-test.perfect99.com/api/user/login",
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
        # 恢复原始配置
        APIConfig._config["BASE_URLS"] = original_base_urls

        if os.path.exists("test.har"):
            os.remove("test.har")


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
def test_filter_invalid_params():
    """测试过滤无效参数"""
    from har2pytest.config import APIConfig

    # 触发配置初始化
    APIConfig.get_config("INVALID_PARAMS")

    # 临时设置 INVALID_PARAMS 配置
    original_invalid_params = APIConfig._config.get("INVALID_PARAMS", set())
    APIConfig._config["INVALID_PARAMS"] = {"sign", "timestamp"}

    try:
        parser = HARParser()

        test_data = {
            "username": "test",
            "password": "123456",
            "sign": "test_sign",  # 无效参数
            "timestamp": "1234567890",  # 无效参数
            "file": "test.txt",  # 现在应该保留file参数
        }

        result = parser._filter_invalid_params(test_data)
        assert "username" in result
        assert "password" in result
        assert "sign" not in result
        assert "timestamp" not in result
        assert "file" in result  # 确保file参数被保留
    finally:
        # 恢复原始配置
        APIConfig._config["INVALID_PARAMS"] = original_invalid_params


@allure.feature("HAR解析器")
@allure.story("文件不存在处理")
def test_file_not_found():
    """测试文件不存在的情况"""
    parser = HARParser()
    requests = parser.extract_requests_from_har("nonexistent.har")
    assert len(requests) == 0


@allure.feature("HAR解析器")
@allure.story("无效JSON处理")
def test_invalid_json():
    """测试无效JSON的情况"""
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
def test_filter_headers():
    """测试过滤Headers功能"""
    from har2pytest.config import APIConfig

    # 触发配置初始化
    APIConfig.get_config("HEADERS_TO_INCLUDE")

    # 临时设置 HEADERS_TO_INCLUDE 配置
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
        assert "Origin" in result  # required_headers 中的
        assert "content-length" in result  # required_headers 中的
        assert "X-Requested-With" not in result  # 不在配置中
        assert "User-Agent" not in result  # 不在配置中
    finally:
        # 恢复原始配置
        APIConfig._config["HEADERS_TO_INCLUDE"] = original_headers


@allure.feature("HAR解析器")
@allure.story("过滤Headers-无配置")
def test_filter_headers_no_config():
    """测试没有配置HEADERS_TO_INCLUDE时返回所有headers"""
    from har2pytest.config import APIConfig

    # 触发配置初始化
    APIConfig.get_config("HEADERS_TO_INCLUDE")

    # 临时设置为空列表
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
def test_filter_headers_invalid_input():
    """测试非字典输入时的处理"""
    parser = HARParser()

    result = parser._filter_headers(None)
    assert result is None

    result = parser._filter_headers("invalid")
    assert result == "invalid"


@allure.feature("HAR解析器")
@allure.story("打印API摘要")
def test_print_api_summary():
    """测试打印API摘要功能"""
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
        parser.print_api_summary("test_summary.har")  # 只需验证不报错
    finally:
        if os.path.exists("test_summary.har"):
            os.remove("test_summary.har")


@allure.feature("HAR解析器")
@allure.story("打印API摘要-空请求")
def test_print_api_summary_empty():
    """测试空请求时的摘要打印"""
    test_har = {"log": {"entries": []}}

    with open("test_empty.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        parser.print_api_summary("test_empty.har")  # 只需验证不报错
    finally:
        if os.path.exists("test_empty.har"):
            os.remove("test_empty.har")


@allure.feature("HAR解析器")
@allure.story("Multipart/form-data处理")
def test_multipart_form_data():
    """测试multipart/form-data类型的POST数据解析"""
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
@allure.story("Kill URLs过滤")
def test_kill_urls_filter():
    """测试kill_urls过滤功能"""
    # 使用包含被过滤URL的HAR文件
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
        # 创建带有kill_urls参数的HARParser
        parser = HARParser(kill_urls=["health"])
        requests = parser.extract_requests_from_har("test_kill_urls.har")

        assert len(requests) == 1
        assert "/user/list" in requests[0]["url"]
    finally:
        if os.path.exists("test_kill_urls.har"):
            os.remove("test_kill_urls.har")


@allure.feature("HAR解析器")
@allure.story("重复URL过滤")
def test_duplicate_url_filter():
    """测试重复URL过滤功能"""
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
        # 默认过滤重复URL
        requests = parser.extract_requests_from_har("test_duplicate.har")
        assert len(requests) == 1

        # 不过滤重复URL
        requests = parser.extract_requests_from_har("test_duplicate.har", filter_duplicate_url=False)
        assert len(requests) == 2
    finally:
        if os.path.exists("test_duplicate.har"):
            os.remove("test_duplicate.har")


@allure.feature("HAR解析器")
@allure.story("Origin Header作为base URL")
def test_origin_as_base_url():
    """测试当没有配置base_urls时使用origin header"""
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
        parser = HARParser(base_urls=[])  # 空列表，触发origin header逻辑
        requests = parser.extract_requests_from_har("test_origin.har")

        assert len(requests) == 1
        assert requests[0]["url"] == "/api/user/login"
    finally:
        if os.path.exists("test_origin.har"):
            os.remove("test_origin.har")


@allure.feature("HAR解析器")
@allure.story("响应内容解析")
def test_response_content_parsing():
    """测试响应内容解析"""
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
