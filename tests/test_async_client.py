"""测试 har2pytest.client 模块中 AsyncClient / AsyncResponseContext 的功能与边界。"""

import logging
from unittest.mock import AsyncMock, MagicMock, patch

import allure
import pytest

from har2pytest.client import AsyncClient, AsyncResponseContext, async_client
from har2pytest.logger import logger


# ==================== Fixtures ====================


@pytest.fixture
def mock_response():
    """构造默认的异步 mock 响应对象（200 OK + JSON）。"""
    resp = AsyncMock()
    resp.status = 200
    resp.headers = {"Content-Type": "application/json"}
    resp.json = AsyncMock(return_value={"code": 200})
    resp.raise_for_status = MagicMock()
    resp.release = AsyncMock()
    resp.text = AsyncMock(return_value='{"code": 200}')
    return resp


@pytest.fixture
def mock_session(mock_response):
    """构造异步 mock session，request 返回 mock_response。"""
    session = AsyncMock()
    session.request = AsyncMock(return_value=mock_response)
    session.closed = False
    session.headers = {}
    return session


@pytest.fixture
def async_client_with_mock(mock_session, mock_response):
    """已注入 mock session 的 AsyncClient，同时返回 (client, mock_response)。"""
    ac = AsyncClient(base_url="https://example.com")
    ac._session = mock_session
    return ac, mock_response


# ==================== 初始化测试 ====================


@allure.story("初始化")
@allure.title("测试 AsyncClient 初始化")
def test_async_client_init():
    client = AsyncClient(base_url="https://example.com", default_timeout=15)
    assert client.base_url == "https://example.com"
    assert client.default_timeout == 15
    assert client._session is None


# ==================== HTTP 方法上下文创建测试 ====================


@allure.feature("异步客户端")
@allure.story("GET请求")
@allure.title("测试 AsyncClient.get 返回 AsyncResponseContext")
def test_async_client_get_returns_context():
    client = AsyncClient(base_url="https://example.com")
    ctx = client.get("/api/test", params={"key": "value"})
    assert isinstance(ctx, AsyncResponseContext)
    assert ctx._method == "GET"
    assert ctx._url == "/api/test"


@allure.feature("异步客户端")
@allure.story("POST请求")
@allure.title("测试 AsyncClient.post 返回 AsyncResponseContext")
def test_async_client_post_returns_context():
    client = AsyncClient(base_url="https://example.com")
    ctx = client.post("/api/test", json={"key": "value"})
    assert isinstance(ctx, AsyncResponseContext)
    assert ctx._method == "POST"
    assert ctx._url == "/api/test"


@allure.feature("异步客户端")
@allure.story("PUT请求")
@allure.title("测试 AsyncClient.put 返回 AsyncResponseContext")
def test_async_client_put_returns_context():
    client = AsyncClient(base_url="https://example.com")
    ctx = client.put("/api/test", json={"key": "value"})
    assert isinstance(ctx, AsyncResponseContext)
    assert ctx._method == "PUT"
    assert ctx._url == "/api/test"


@allure.feature("异步客户端")
@allure.story("DELETE请求")
@allure.title("测试 AsyncClient.delete 返回 AsyncResponseContext")
def test_async_client_delete_returns_context():
    client = AsyncClient(base_url="https://example.com")
    ctx = client.delete("/api/resource/1")
    assert isinstance(ctx, AsyncResponseContext)
    assert ctx._method == "DELETE"
    assert ctx._url == "/api/resource/1"


@allure.feature("异步客户端")
@allure.story("PATCH请求")
@allure.title("测试 AsyncClient.patch 返回 AsyncResponseContext")
def test_async_client_patch_returns_context():
    client = AsyncClient(base_url="https://example.com")
    ctx = client.patch("/api/resource/1", json={"name": "updated"})
    assert isinstance(ctx, AsyncResponseContext)
    assert ctx._method == "PATCH"
    assert ctx._url == "/api/resource/1"


# ==================== 请求执行测试 ====================


@allure.feature("异步客户端")
@allure.story("请求执行")
@allure.title("测试 AsyncResponseContext 成功发起 GET 请求")
async def test_async_response_context_get_success(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    ctx = ac.get("/api/test", params={"key": "value"})
    response = await ctx.__aenter__()

    assert response is mock_resp
    ac._session.request.assert_called_once()
    call_args = ac._session.request.call_args
    assert call_args[0][0] == "GET"
    assert call_args[0][1] == "https://example.com/api/test"


@allure.feature("异步客户端")
@allure.story("请求执行")
@allure.title("测试 AsyncResponseContext 成功发起 POST 请求（JSON body）")
async def test_async_response_context_post_json(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    ctx = ac.post("/api/create", json={"name": "test"})
    response = await ctx.__aenter__()

    assert response is mock_resp
    ac._session.request.assert_called_once()
    call_args = ac._session.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "https://example.com/api/create"


@allure.feature("异步客户端")
@allure.story("请求执行")
@allure.title("测试 AsyncResponseContext 使用 async with 语法")
async def test_async_response_context_async_with(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    async with ac.get("/api/test") as r:
        assert r.status == 200
        data = await r.json()
        assert data["code"] == 200

    mock_resp.release.assert_called_once()


# ==================== 断言失败处理测试 ====================


@allure.feature("异步客户端")
@allure.story("断言失败处理")
@allure.title("测试断言失败时附加 Allure 数据")
async def test_async_response_context_assertion_failure_attaches_allure(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    mock_resp.json = AsyncMock(return_value={"code": 500, "msg": "error"})
    mock_resp.text = AsyncMock(return_value='{"code": 500, "msg": "error"}')

    with patch("har2pytest.client.allure.attach") as mock_attach:
        ctx = ac.get("/api/test")
        with pytest.raises(AssertionError):
            async with ctx as r:
                data = await r.json()
                assert data["code"] == 200

        # 断言失败时应该附加 Allure 数据
        assert mock_attach.call_count >= 1


# ==================== Allure 数据附加测试 ====================


@allure.feature("异步客户端")
@allure.story("Allure 数据附加")
@allure.title("测试 DEBUG 级别下断言成功时也附加 Allure 数据")
async def test_async_response_context_success_attaches_allure_when_debug(async_client_with_mock):
    ac, mock_resp = async_client_with_mock

    # 设置 logger 为 DEBUG 级别以触发 Allure 附件
    original_level = logger.level
    logger.setLevel(logging.DEBUG)
    try:
        with patch("har2pytest.client.allure.attach") as mock_attach:
            async with ac.get("/api/test") as r:
                assert r.status == 200

            # DEBUG 级别下，断言成功时也会附加 Allure 数据
            assert mock_attach.call_count >= 1
    finally:
        logger.setLevel(original_level)


# ==================== Session 管理测试 ====================


@allure.feature("异步客户端")
@allure.story("Session管理")
@allure.title("测试 session 复用")
async def test_async_client_session_reuse():
    client = AsyncClient(base_url="https://example.com")

    session1 = await client._get_session()
    session2 = await client._get_session()

    assert session1 is session2


@allure.feature("异步客户端")
@allure.story("Session管理")
@allure.title("测试 close 关闭 session")
async def test_async_client_close():
    client = AsyncClient(base_url="https://example.com")

    session = await client._get_session()
    session.close = AsyncMock()

    await client.close()
    session.close.assert_called_once()
    assert client._session is None


@allure.feature("异步客户端")
@allure.story("Session管理")
@allure.title("测试旧 session 已关闭时自动重建")
async def test_async_client_session_rebuild_on_closed():
    client = AsyncClient(base_url="https://example.com")

    # 用一个 closed=True 的 mock 模拟已关闭的旧 session
    old_session = MagicMock()
    old_session.closed = True
    old_session.close = AsyncMock()
    client._session = old_session

    new_session = await client._get_session()
    assert new_session is not old_session


# ==================== 全局实例测试 ====================


@allure.feature("异步客户端")
@allure.story("全局实例")
@allure.title("测试 async_client 全局实例")
def test_async_client_global_instance():
    assert isinstance(async_client, AsyncClient)
    assert async_client._session is None


# ==================== 响应体解析测试 ====================


@allure.feature("异步客户端")
@allure.story("响应体解析")
@allure.title("测试 _parse_response_body 解析 JSON 响应")
async def test_parse_response_body_json():
    mock_response = AsyncMock()
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"key": "value"})

    client = AsyncClient(base_url="https://example.com")
    ctx = client.get("/api/test")
    ctx._response = mock_response

    result = await ctx._parse_response_body(mock_response)
    assert result == {"key": "value"}


@allure.feature("异步客户端")
@allure.story("响应体解析")
@allure.title("测试 _parse_response_body 解析 HTML 响应")
async def test_parse_response_body_html():
    mock_response = AsyncMock()
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = AsyncMock(return_value="<html>test</html>")

    client = AsyncClient(base_url="https://example.com")
    ctx = client.get("/api/test")
    ctx._response = mock_response

    result = await ctx._parse_response_body(mock_response)
    assert result == "<html>test</html>"


@allure.feature("异步客户端")
@allure.story("响应体解析")
@allure.title("测试 _parse_response_body 解析 image 响应")
async def test_parse_response_body_image():
    mock_resp = AsyncMock()
    mock_resp.headers = {"Content-Type": "image/png"}
    mock_resp.read = AsyncMock(return_value=b"\x89PNG\r\n")

    client = AsyncClient(base_url="https://example.com")
    ctx = client.get("/api/image")

    result = await ctx._parse_response_body(mock_resp)
    assert result == b"\x89PNG\r\n"


@allure.feature("异步客户端")
@allure.story("响应体解析")
@allure.title("测试 _parse_response_body 解析失败回退截断文本")
async def test_parse_response_body_fallback():
    mock_resp = AsyncMock()
    mock_resp.headers = {"Content-Type": "application/xml"}
    mock_resp.json = AsyncMock(side_effect=Exception("parse error"))
    mock_resp.text = AsyncMock(return_value="<xml>fallback</xml>")

    client = AsyncClient(base_url="https://example.com")
    ctx = client.get("/api/data")

    result = await ctx._parse_response_body(mock_resp)
    assert result == "<xml>fallback</xml>"


# ==================== 请求信息记录测试 ====================


@allure.feature("异步客户端")
@allure.story("请求信息记录")
@allure.title("测试请求信息包含 params 参数")
async def test_async_response_context_request_info_params(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    ctx = ac.get("/api/test", params={"pageNum": "1"})
    await ctx.__aenter__()

    assert ctx._request_info is not None
    assert "params" in ctx._request_info
    assert ctx._request_info["params"] == {"pageNum": "1"}


@allure.feature("异步客户端")
@allure.story("请求信息记录")
@allure.title("测试请求信息包含 json 参数")
async def test_async_response_context_request_info_json(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    ctx = ac.post("/api/create", json={"name": "test"})
    await ctx.__aenter__()

    assert ctx._request_info is not None
    assert "json" in ctx._request_info
    assert ctx._request_info["json"] == {"name": "test"}


@allure.feature("异步客户端")
@allure.story("请求信息记录")
@allure.title("测试请求信息包含 FormData 参数")
async def test_async_response_context_request_info_multipart(async_client_with_mock):
    ac, mock_resp = async_client_with_mock

    # 模拟 aiohttp.FormData（异步模式）
    mock_data = MagicMock()
    mock_data.__class__.__name__ = "FormData"

    ctx = ac.post("/api/upload", data=mock_data)
    await ctx.__aenter__()

    assert ctx._request_info is not None
    assert "data" in ctx._request_info
    assert "文件上传请求" in ctx._request_info["data"]


# ==================== 异常处理测试 ====================


@allure.feature("异步客户端")
@allure.story("异常处理")
@allure.title("测试 HTTP 错误状态码抛出异常")
async def test_async_response_context_http_error(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    mock_resp.status = 500
    mock_resp.json = AsyncMock(return_value={"error": "server error"})
    mock_resp.text = AsyncMock(return_value='{"error": "server error"}')
    mock_resp.raise_for_status = MagicMock(side_effect=Exception("500 Server Error"))
    ac.raise_for_status = True

    ctx = ac.get("/api/error")

    with pytest.raises(Exception):
        await ctx.__aenter__()

    mock_resp.release.assert_called_once()


@allure.feature("异步客户端")
@allure.story("异常处理")
@allure.title("测试默认(False)时可进入并断言 4xx/5xx")
async def test_async_response_context_raise_for_status_disabled(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    mock_resp.status = 500
    mock_resp.json = AsyncMock(return_value={"code": 500})
    mock_resp.text = AsyncMock(return_value='{"code": 500}')
    mock_resp.raise_for_status = MagicMock(side_effect=Exception("500 Server Error"))

    async with ac.get("/api/error") as r:
        assert r.status == 500

    mock_resp.raise_for_status.assert_not_called()


@allure.feature("异步客户端")
@allure.story("异常处理")
@allure.title("测试每请求 raise_for_status 参数覆盖客户端默认值")
async def test_async_response_context_per_request_raise_for_status(async_client_with_mock):
    ac, mock_resp = async_client_with_mock
    mock_resp.status = 500
    mock_resp.raise_for_status = MagicMock(side_effect=Exception("500 Server Error"))

    # 客户端默认 False，但单次请求覆盖为 True
    ctx = ac.get("/api/error", raise_for_status=True)

    with pytest.raises(Exception, match="500 Server Error"):
        await ctx.__aenter__()

    mock_resp.release.assert_called_once()
