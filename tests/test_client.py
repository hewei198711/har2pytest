"""
测试 client.py 模块（同步 Client 和 ResponseContext）
"""

import logging
from unittest.mock import MagicMock, patch

import allure
import pytest
import requests

from har2pytest.client import Client, ResponseContext, _value_with_color, client
from har2pytest.logger import logger


# ==================== _value_with_color 测试 ====================


@allure.feature("共享工具函数")
@allure.story("性能监控颜色")
@allure.title("测试性能值绿色（低于green阈值）")
def test_value_with_color_green():
    thresholds = {"green": 5, "yellow": 10}
    result = _value_with_color(2.0, thresholds)
    assert "green" in result
    assert "2.000" in result


@allure.feature("共享工具函数")
@allure.story("性能监控颜色")
@allure.title("测试性能值橙色（低于yellow阈值）")
def test_value_with_color_yellow():
    thresholds = {"green": 5, "yellow": 10}
    result = _value_with_color(7.0, thresholds)
    assert "orange" in result


@allure.feature("共享工具函数")
@allure.story("性能监控颜色")
@allure.title("测试性能值红色（超过阈值）")
def test_value_with_color_red():
    thresholds = {"green": 5, "yellow": 10}
    result = _value_with_color(15.0, thresholds)
    assert "red" in result


# ==================== Client 初始化测试 ====================


@allure.feature("同步客户端")
@allure.story("初始化")
@allure.title("测试 Client 默认初始化")
def test_client_init_default():
    c = Client()
    assert c.base_url == ""
    assert c.default_timeout == 30
    assert c.default_verify is False
    assert isinstance(c.session, requests.Session)


@allure.feature("同步客户端")
@allure.story("初始化")
@allure.title("测试 Client 自定义参数初始化")
def test_client_init_custom():
    c = Client(base_url="https://api.example.com", default_timeout=60, default_verify=True)
    assert c.base_url == "https://api.example.com"
    assert c.default_timeout == 60
    assert c.default_verify is True


# ==================== Client 请求方法测试 ====================


@allure.feature("同步客户端")
@allure.story("请求方法")
@allure.title("测试 Client.get 返回 ResponseContext")
def test_client_get_returns_context():
    c = Client(base_url="https://example.com")
    ctx = c.get("/api/test", params={"key": "value"})
    assert isinstance(ctx, ResponseContext)
    assert ctx._method == "GET"
    assert ctx._url == "/api/test"


@allure.feature("同步客户端")
@allure.story("请求方法")
@allure.title("测试 Client.post 返回 ResponseContext")
def test_client_post_returns_context():
    c = Client(base_url="https://example.com")
    ctx = c.post("/api/create", json={"name": "test"})
    assert isinstance(ctx, ResponseContext)
    assert ctx._method == "POST"
    assert ctx._url == "/api/create"


@allure.feature("同步客户端")
@allure.story("请求方法")
@allure.title("测试 Client.put 返回 ResponseContext")
def test_client_put_returns_context():
    c = Client(base_url="https://example.com")
    ctx = c.put("/api/update", json={"name": "test"})
    assert isinstance(ctx, ResponseContext)
    assert ctx._method == "PUT"
    assert ctx._url == "/api/update"


# ==================== ResponseContext 初始化测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext 初始化")
def test_response_context_init():
    c = Client(base_url="https://example.com")
    ctx = ResponseContext(c, "GET", "/api/test", params={"key": "value"})
    assert ctx._client is c
    assert ctx._method == "GET"
    assert ctx._url == "/api/test"
    assert ctx._response is None
    assert ctx._request_info is None


# ==================== ResponseContext.__enter__ 测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__enter__ GET 请求成功")
def test_response_context_enter_get_success():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200, "data": {}}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.get("/api/test", params={"key": "value"})
    response = ctx.__enter__()

    assert response is mock_response
    mock_session.request.assert_called_once()
    call_args = mock_session.request.call_args
    assert call_args[0][0] == "GET"
    assert "https://example.com/api/test" in str(call_args)


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__enter__ POST JSON 请求")
def test_response_context_enter_post_json():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.post("/api/create", json={"name": "test"})
    response = ctx.__enter__()

    assert response is mock_response
    mock_session.request.assert_called_once()


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__enter__ 带自定义 timeout 和 verify")
def test_response_context_enter_custom_timeout_verify():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com", default_timeout=30, default_verify=False)
    c.session = mock_session

    ctx = c.get("/api/test", timeout=10, verify=True)
    ctx.__enter__()

    call_kwargs = mock_session.request.call_args[1]
    assert call_kwargs["timeout"] == 10
    assert call_kwargs["verify"] is True


# ==================== ResponseContext.__exit__ 测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__exit__ 正常退出不附加 Allure")
def test_response_context_exit_success_no_attach():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    with patch("har2pytest.client.allure.attach") as mock_attach:
        with c.get("/api/test") as r:
            assert r.status_code == 200

        # 正常退出不附加 Allure 数据（非 DEBUG 级别且无异常）
        mock_attach.assert_not_called()


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__exit__ 异常时附加 Allure")
def test_response_context_exit_exception_attaches_allure():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 500
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 500, "msg": "error"}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    with patch("har2pytest.client.allure.attach") as mock_attach:
        try:
            with c.get("/api/test") as r:
                raise AssertionError("test failure")
        except AssertionError:
            pass

        # 异常时应该附加 Allure 数据
        assert mock_attach.call_count >= 1


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__exit__ DEBUG 级别附加 Allure")
def test_response_context_exit_debug_attaches_allure():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    original_level = logger.level
    logger.setLevel(logging.DEBUG)
    try:
        with patch("har2pytest.client.allure.attach") as mock_attach:
            with c.get("/api/test") as r:
                assert r.status_code == 200

            # DEBUG 级别下应该附加 Allure 数据
            assert mock_attach.call_count >= 1
    finally:
        logger.setLevel(original_level)


# ==================== ResponseContext 请求信息测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试请求信息包含 params 参数")
def test_response_context_request_info_params():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.get("/api/test", params={"pageNum": "1"})
    ctx.__enter__()

    assert ctx._request_info is not None
    assert "params" in ctx._request_info
    assert ctx._request_info["params"] == {"pageNum": "1"}


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试请求信息包含 json 参数")
def test_response_context_request_info_json():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.post("/api/create", json={"name": "test"})
    ctx.__enter__()

    assert ctx._request_info is not None
    assert "json" in ctx._request_info
    assert ctx._request_info["json"] == {"name": "test"}


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试请求信息包含 MultipartEncoder data 参数")
def test_response_context_request_info_multipart():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    mock_encoder = MagicMock()
    mock_encoder.__class__.__name__ = "MultipartEncoder"

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.post("/api/upload", data=mock_encoder)
    ctx.__enter__()

    assert ctx._request_info is not None
    assert "data" in ctx._request_info
    assert "文件上传请求" in ctx._request_info["data"]


# ==================== _parse_response_body 测试 ====================


@allure.feature("同步客户端")
@allure.story("响应体解析")
@allure.title("测试解析 JSON 响应体")
def test_parse_response_body_json():
    mock_response = MagicMock(spec=requests.Response)
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"key": "value"}

    result = ResponseContext._parse_response_body(mock_response)
    assert result == {"key": "value"}


@allure.feature("同步客户端")
@allure.story("响应体解析")
@allure.title("测试解析 HTML 响应体")
def test_parse_response_body_html():
    mock_response = MagicMock(spec=requests.Response)
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "<html>test</html>"

    result = ResponseContext._parse_response_body(mock_response)
    assert result == "<html>test</html>"


@allure.feature("同步客户端")
@allure.story("响应体解析")
@allure.title("测试解析图片响应体")
def test_parse_response_body_image():
    mock_response = MagicMock(spec=requests.Response)
    mock_response.headers = {"Content-Type": "image/png"}
    mock_response.content = b"\x89PNG"

    result = ResponseContext._parse_response_body(mock_response)
    assert result == b"\x89PNG"


@allure.feature("同步客户端")
@allure.story("响应体解析")
@allure.title("测试解析未知类型响应体")
def test_parse_response_body_unknown():
    mock_response = MagicMock(spec=requests.Response)
    mock_response.headers = {"Content-Type": "application/octet-stream"}
    mock_response.text = "binary data" * 100

    result = ResponseContext._parse_response_body(mock_response)
    assert len(result) <= 500


@allure.feature("同步客户端")
@allure.story("响应体解析")
@allure.title("测试解析异常时回退到 text")
def test_parse_response_body_fallback():
    mock_response = MagicMock(spec=requests.Response)
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.side_effect = ValueError("invalid json")
    mock_response.text = "fallback text"

    result = ResponseContext._parse_response_body(mock_response)
    assert result == "fallback text"


# ==================== 日志方法测试 ====================


@allure.feature("同步客户端")
@allure.story("日志")
@allure.title("测试 _log_request 记录请求日志")
def test_client_log_request():
    c = Client(base_url="https://example.com")
    mock_logger = MagicMock()
    c.logger = mock_logger

    request_info = {
        "method": "GET",
        "url": "https://example.com/api/test",
        "headers": {"Authorization": "bearer xxx"},
        "params": {"key": "value"},
    }
    c._log_request("GET", "https://example.com/api/test", request_info)

    mock_logger.info.assert_called_once()


@allure.feature("同步客户端")
@allure.story("日志")
@allure.title("测试 _log_request 记录带 json 的请求日志")
def test_client_log_request_with_json():
    c = Client(base_url="https://example.com")
    mock_logger = MagicMock()
    c.logger = mock_logger

    request_info = {
        "method": "POST",
        "url": "https://example.com/api/create",
        "headers": {},
        "json": {"name": "test"},
    }
    c._log_request("POST", "https://example.com/api/create", request_info)

    mock_logger.info.assert_called_once()


@allure.feature("同步客户端")
@allure.story("日志")
@allure.title("测试 _log_request 记录带 data 的请求日志")
def test_client_log_request_with_data():
    c = Client(base_url="https://example.com")
    mock_logger = MagicMock()
    c.logger = mock_logger

    request_info = {
        "method": "POST",
        "url": "https://example.com/api/create",
        "headers": {},
        "data": "key=value",
    }
    c._log_request("POST", "https://example.com/api/create", request_info)

    mock_logger.info.assert_called_once()


@allure.feature("同步客户端")
@allure.story("日志")
@allure.title("测试 _log_response 记录 JSON 响应日志")
def test_client_log_response_json():
    c = Client(base_url="https://example.com")
    mock_logger = MagicMock()
    c.logger = mock_logger

    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200}

    c._log_response(mock_response)
    mock_logger.info.assert_called_once()


@allure.feature("同步客户端")
@allure.story("日志")
@allure.title("测试 _log_response 记录非 JSON 响应日志")
def test_client_log_response_non_json():
    c = Client(base_url="https://example.com")
    mock_logger = MagicMock()
    c.logger = mock_logger

    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "<html>ok</html>"

    c._log_response(mock_response)
    mock_logger.info.assert_called_once()


@allure.feature("同步客户端")
@allure.story("日志")
@allure.title("测试 _log_response 异常时回退")
def test_client_log_response_exception():
    c = Client(base_url="https://example.com")
    mock_logger = MagicMock()
    c.logger = mock_logger

    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 500
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.side_effect = ValueError("bad json")
    mock_response.text = "error"

    c._log_response(mock_response)
    mock_logger.info.assert_called_once()


# ==================== 全局实例测试 ====================


@allure.feature("同步客户端")
@allure.story("全局实例")
@allure.title("测试 client 全局实例")
def test_client_global_instance():
    assert isinstance(client, Client)


# ==================== HTTP 错误测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 HTTP 错误状态码抛出异常")
def test_response_context_http_error():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 500
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"error": "server error"}
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.get("/api/error")
    with pytest.raises(requests.HTTPError):
        ctx.__enter__()


# ==================== _attach_to_allure 测试 ====================


@allure.feature("同步客户端")
@allure.story("Allure附件")
@allure.title("测试 _attach_to_allure 附加请求和响应数据")
def test_attach_to_allure():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 200, "data": {}}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.get("/api/test")
    ctx.__enter__()

    with patch("har2pytest.client.allure.attach") as mock_attach:
        ctx._attach_to_allure()
        # 应该附加请求和响应数据（至少2次）
        assert mock_attach.call_count >= 2


@allure.feature("同步客户端")
@allure.story("Allure附件")
@allure.title("测试 _attach_to_allure 附加断言错误")
def test_attach_to_allure_with_exception():
    mock_session = MagicMock()
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json.return_value = {"code": 500}
    mock_response.raise_for_status = MagicMock()
    mock_session.request.return_value = mock_response

    c = Client(base_url="https://example.com")
    c.session = mock_session

    ctx = c.get("/api/test")
    ctx.__enter__()

    with patch("har2pytest.client.allure.attach") as mock_attach:
        ctx._attach_to_allure(AssertionError("assertion failed"))
        # 应该附加请求、响应和错误信息（至少3次）
        assert mock_attach.call_count >= 3
