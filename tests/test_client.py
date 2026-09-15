"""
测试 client.py 模块（同步 Client 和 ResponseContext）
"""

import logging
from unittest.mock import MagicMock, patch

import allure
import pytest
import requests

from har2pytest.client import (
    _DATA_FIELDS_ATTR,
    _DATA_FILES_ATTR,
    Client,
    ResponseContext,
    _build_request_info,
    _guess_content_type,
    _json_default,
    _shorten,
    build_form_data,
    build_multipart_data,
    client,
)
from har2pytest.logger import logger

# ==================== Fixtures ====================


@pytest.fixture
def mock_response():
    """构造默认的同步 mock 响应对象（200 OK + JSON）。"""
    resp = MagicMock(spec=requests.Response)
    resp.status_code = 200
    resp.headers = {"Content-Type": "application/json"}
    resp.json.return_value = {"code": 200}
    resp.raise_for_status = MagicMock()
    return resp


@pytest.fixture
def mock_session(mock_response):
    """构造同步 mock session，request 返回 mock_response。"""
    session = MagicMock()
    session.request.return_value = mock_response
    return session


@pytest.fixture
def client_with_mock(mock_session):
    """已注入 mock session 的 Client，同时返回 (client, mock_response)。"""
    mock_response = mock_session.request.return_value
    ac = Client(base_url="https://example.com")
    ac.session = mock_session
    return ac, mock_response


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


@allure.feature("同步客户端")
@allure.story("请求方法")
@allure.title("测试 Client.delete 返回 ResponseContext")
def test_client_delete_returns_context():
    c = Client(base_url="https://example.com")
    ctx = c.delete("/api/remove")
    assert isinstance(ctx, ResponseContext)
    assert ctx._method == "DELETE"
    assert ctx._url == "/api/remove"


@allure.feature("同步客户端")
@allure.story("请求方法")
@allure.title("测试 Client.patch 返回 ResponseContext")
def test_client_patch_returns_context():
    c = Client(base_url="https://example.com")
    ctx = c.patch("/api/update", json={"field": "value"})
    assert isinstance(ctx, ResponseContext)
    assert ctx._method == "PATCH"
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
    assert ctx._request_info == {}


# ==================== ResponseContext.__enter__ 测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__enter__ GET 请求成功")
def test_response_context_enter_get_success(client_with_mock, mock_session):
    c, mock_response = client_with_mock
    ctx = c.get("/api/test", params={"key": "value"})
    response = ctx.__enter__()

    assert response is mock_response
    mock_session.request.assert_called_once()
    call_args = mock_session.request.call_args
    assert call_args[0][0] == "GET"
    assert call_args[0][1] == "https://example.com/api/test"


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__enter__ POST JSON 请求")
def test_response_context_enter_post_json(client_with_mock, mock_session):
    c, mock_response = client_with_mock
    ctx = c.post("/api/create", json={"name": "test"})
    response = ctx.__enter__()

    assert response is mock_response
    mock_session.request.assert_called_once()


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__enter__ 带自定义 timeout 和 verify")
def test_response_context_enter_custom_timeout_verify(client_with_mock, mock_session):
    c, _ = client_with_mock
    c.default_timeout = 30
    c.default_verify = False
    ctx = c.get("/api/test", timeout=10, verify=True)
    ctx.__enter__()

    call_kwargs = mock_session.request.call_args[1]
    assert call_kwargs["timeout"] == 10
    assert call_kwargs["verify"] is True


# ==================== ResponseContext.__exit__ 测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__exit__ 正常退出不附加 Allure")
def test_response_context_exit_success_no_attach(client_with_mock):
    c, _ = client_with_mock

    with patch("har2pytest.client.allure.attach") as mock_attach:
        with c.get("/api/test") as r:
            assert r.status_code == 200

        # 正常退出不附加 Allure 数据（非 DEBUG 级别且无异常）
        mock_attach.assert_not_called()


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__exit__ 关闭挂载的文件句柄")
def test_response_context_exit_closes_files(client_with_mock):
    c, _ = client_with_mock
    mock_fh = MagicMock()
    mock_body = MagicMock()
    mock_body._har2pytest_open_files = [mock_fh]

    ctx = c.post("/api/upload", data=mock_body)
    ctx.__enter__()
    ctx.__exit__(None, None, None)

    mock_fh.close.assert_called_once()


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__exit__ 异常时附加 Allure")
def test_response_context_exit_exception_attaches_allure(client_with_mock):
    c, mock_response = client_with_mock
    mock_response.status_code = 500
    mock_response.json.return_value = {"code": 500, "msg": "error"}

    with patch("har2pytest.client.allure.attach") as mock_attach:
        try:
            with c.get("/api/test"):
                raise AssertionError("test failure")
        except AssertionError:
            pass

        # 异常时应该附加 Allure 数据
        assert mock_attach.call_count >= 1


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 ResponseContext.__exit__ DEBUG 级别附加 Allure")
def test_response_context_exit_debug_attaches_allure(client_with_mock):
    c, _ = client_with_mock

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
def test_response_context_request_info_params(client_with_mock):
    c, _ = client_with_mock
    ctx = c.get("/api/test", params={"pageNum": "1"})
    ctx.__enter__()

    assert ctx._request_info is not None
    assert "params" in ctx._request_info
    assert ctx._request_info["params"] == {"pageNum": "1"}


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试请求信息包含 json 参数")
def test_response_context_request_info_json(client_with_mock):
    c, _ = client_with_mock
    ctx = c.post("/api/create", json={"name": "test"})
    ctx.__enter__()

    assert ctx._request_info is not None
    assert "json" in ctx._request_info
    assert ctx._request_info["json"] == {"name": "test"}


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试请求信息包含 MultipartEncoder data 参数")
def test_response_context_request_info_multipart(client_with_mock):
    c, _ = client_with_mock
    mock_encoder = MagicMock()
    mock_encoder.__class__.__name__ = "MultipartEncoder"
    ctx = c.post("/api/upload", data=mock_encoder)
    ctx.__enter__()

    assert ctx._request_info is not None
    assert "data" in ctx._request_info
    assert "文件上传请求" in ctx._request_info["data"]


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试请求信息包含 _DATA_FIELDS_ATTR 挂载字段和文件信息")
def test_response_context_request_info_data_fields_attr(client_with_mock):
    c, _ = client_with_mock
    mock_data = MagicMock()
    setattr(mock_data, _DATA_FIELDS_ATTR, {"key": "value"})
    setattr(mock_data, _DATA_FILES_ATTR, {"file": "test.png"})

    ctx = c.post("/api/upload", data=mock_data)
    ctx.__enter__()

    assert ctx._request_info["data"] == {"key": "value"}
    assert ctx._request_info["files"] == {"file": "test.png"}


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


@allure.feature("同步客户端")
@allure.story("响应体解析")
@allure.title("测试解析全部失败时回退到 [无法读取响应体]")
def test_parse_response_body_total_failure():
    class _NoTextMock(MagicMock):
        @property
        def text(self):
            raise RuntimeError("no text")

    mock_response = _NoTextMock()
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = MagicMock(side_effect=ValueError("invalid json"))

    result = ResponseContext._parse_response_body(mock_response)
    assert result == "[无法读取响应体]"


# ==================== 工具函数测试 ====================


@allure.feature("同步客户端")
@allure.story("工具函数")
@allure.title("测试 _shorten 截断长值")
def test_shorten_truncation():
    assert _shorten("abc") == "abc"
    assert _shorten("a" * 300) == "a" * 200 + "..."


@allure.feature("同步客户端")
@allure.story("工具函数")
@allure.title("测试 _json_default bytes 转 base64")
def test_json_default_bytes():
    import base64

    result = _json_default(b"\x89PNG")
    assert result == base64.b64encode(b"\x89PNG").decode("ascii")

    long_bytes = b"x" * 3000
    result_long = _json_default(long_bytes)
    assert "[二进制 3000 bytes]" in result_long
    assert result_long.endswith("...")


@allure.feature("同步客户端")
@allure.story("工具函数")
@allure.title("测试 _json_default 非 bytes 回退 str")
def test_json_default_fallback():
    assert _json_default(42) == "42"
    assert _json_default(None) == "None"


@allure.feature("同步客户端")
@allure.story("工具函数")
@allure.title("测试 _guess_content_type 猜测 MIME 类型")
def test_guess_content_type():
    assert _guess_content_type("photo.png") == "image/png"
    assert _guess_content_type("doc.pdf") == "application/pdf"
    assert _guess_content_type("unknown.xyz") == "application/octet-stream"


# ==================== 全局实例测试 ====================


@allure.feature("同步客户端")
@allure.story("全局实例")
@allure.title("测试 client 全局实例为 _ClientProxy 且默认同步")
def test_client_global_instance():
    from har2pytest.client import _ClientProxy

    assert isinstance(client, _ClientProxy)
    assert client.is_async is False


@allure.feature("同步客户端")
@allure.story("全局实例")
@allure.title("测试 _ClientProxy 切换同步/异步客户端")
def test_client_proxy_set_client():
    from har2pytest.client import AsyncClient, Client, _ClientProxy

    proxy = _ClientProxy(Client(base_url=""))
    assert proxy.is_async is False

    proxy.set_client(AsyncClient(base_url=""))
    assert proxy.is_async is True

    # 恢复同步
    proxy.set_client(Client(base_url=""))
    assert proxy.is_async is False


# ==================== HTTP 错误测试 ====================


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试 HTTP 错误状态码在 raise_for_status=True 时抛出异常")
def test_response_context_http_error(client_with_mock):
    c, mock_response = client_with_mock
    c.raise_for_status = True
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "server error"}
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    ctx = c.get("/api/error")
    with pytest.raises(requests.HTTPError):
        ctx.__enter__()


# ==================== _attach_to_allure 测试 ====================


@allure.feature("同步客户端")
@allure.story("Allure附件")
@allure.title("测试 _attach_to_allure 附加请求和响应数据")
def test_attach_to_allure(client_with_mock):
    c, _ = client_with_mock
    ctx = c.get("/api/test")
    ctx.__enter__()

    with patch("har2pytest.client.allure.attach") as mock_attach:
        ctx._attach_to_allure()
        # 应该附加请求和响应数据（至少2次）
        assert mock_attach.call_count >= 2


@allure.feature("同步客户端")
@allure.story("Allure附件")
@allure.title("测试 _attach_to_allure 附加断言错误")
def test_attach_to_allure_with_exception(client_with_mock):
    c, mock_response = client_with_mock
    mock_response.json.return_value = {"code": 500}
    ctx = c.get("/api/test")
    ctx.__enter__()

    with patch("har2pytest.client.allure.attach") as mock_attach:
        ctx._attach_to_allure(AssertionError("assertion failed"))
        # 应该附加请求、响应和错误信息（至少3次）
        assert mock_attach.call_count >= 3


@allure.feature("同步客户端")
@allure.story("ResponseContext")
@allure.title("测试默认(False)与单请求开关下可进入并断言 4xx/5xx")
def test_response_context_raise_for_status_disabled(client_with_mock, mock_session):
    c, mock_response = client_with_mock
    mock_response.status_code = 500
    mock_response.json.return_value = {"code": 500}
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")

    # 默认 raise_for_status=False：可直接进入并断言
    with c.get("/api/error") as r:
        assert r.status_code == 500
    mock_response.raise_for_status.assert_not_called()

    # 客户端级开启 True → 入口抛错
    mock_response.raise_for_status.reset_mock()
    c_true = Client(base_url="https://example.com", raise_for_status=True)
    c_true.session = mock_session
    with pytest.raises(requests.HTTPError):
        c_true.get("/api/error").__enter__()

    # 单请求级覆盖：默认 False 的客户端上开启 True 也会抛错
    mock_response.raise_for_status.reset_mock()
    c2 = Client(base_url="https://example.com")
    c2.session = mock_session
    with pytest.raises(requests.HTTPError):
        c2.get("/api/error", raise_for_status=True).__enter__()


@allure.feature("同步客户端")
@allure.story("请求信息记录")
@allure.title("测试 multipart 表单在请求信息中展示真实字段")
def test_request_info_shows_multipart_fields():
    # 默认全局 client 为同步，build_form_data 走 MultipartEncoder 分支
    m, content_type = build_form_data({"orderNo": "SG001", "remarks": "111"})

    info = _build_request_info(
        "POST", "https://example.com/api/order/cancel", {"content-type": content_type or "multipart/form-data"},
        None, None, m,
    )
    assert info["data"] == {"orderNo": "SG001", "remarks": "111"}
    assert "文件上传请求" not in str(info["data"])


# ==================== build_multipart_data 测试 ====================


@allure.feature("同步客户端")
@allure.story("文件上传")
@allure.title("测试 build_multipart_data 同步分支返回 MultipartEncoder")
def test_build_multipart_data_sync(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    result, content_type = build_multipart_data(
        {"file": str(test_file), "name": "test"}, "file",
    )
    assert content_type is not None
    assert "multipart/form-data" in content_type
    assert hasattr(result, "_har2pytest_open_files")
    for fh in result._har2pytest_open_files:
        fh.close()
