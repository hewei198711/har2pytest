"""
测试 async_client.py 模块
"""

import logging
from unittest.mock import AsyncMock, MagicMock, patch

import allure
import pytest

from har2pytest.client import AsyncClient, AsyncResponseContext, async_client
from har2pytest.logger import logger


@allure.feature("异步客户端")
@allure.story("初始化")
@allure.title("测试 AsyncClient 初始化")
def test_async_client_init():
    client = AsyncClient(base_url="https://example.com", default_timeout=15)
    assert client.base_url == "https://example.com"
    assert client.default_timeout == 15
    assert client._session is None


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
@allure.story("请求执行")
@allure.title("测试 AsyncResponseContext 成功发起 GET 请求")
@pytest.mark.asyncio
async def test_async_response_context_get_success():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 200, "data": {}})
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()
    mock_response.text = AsyncMock(return_value='{"code": 200, "data": {}}')

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    ctx = client.get("/api/test", params={"key": "value"})
    response = await ctx.__aenter__()

    assert response is mock_response
    mock_session.request.assert_called_once()
    call_args = mock_session.request.call_args
    assert call_args[0][0] == "GET"
    assert call_args[0][1] == "https://example.com/api/test"


@allure.feature("异步客户端")
@allure.story("请求执行")
@allure.title("测试 AsyncResponseContext 成功发起 POST 请求（JSON body）")
@pytest.mark.asyncio
async def test_async_response_context_post_json():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 200})
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()
    mock_response.text = AsyncMock(return_value='{"code": 200}')

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    ctx = client.post("/api/create", json={"name": "test"})
    response = await ctx.__aenter__()

    assert response is mock_response
    mock_session.request.assert_called_once()
    call_args = mock_session.request.call_args
    assert call_args[0][0] == "POST"
    assert call_args[0][1] == "https://example.com/api/create"


@allure.feature("异步客户端")
@allure.story("请求执行")
@allure.title("测试 AsyncResponseContext 使用 async with 语法")
@pytest.mark.asyncio
async def test_async_response_context_async_with():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 200})
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()
    mock_response.text = AsyncMock(return_value='{"code": 200}')

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    async with client.get("/api/test") as r:
        assert r.status == 200
        data = await r.json()
        assert data["code"] == 200

    mock_response.release.assert_called_once()


@allure.feature("异步客户端")
@allure.story("断言失败处理")
@allure.title("测试断言失败时附加 Allure 数据")
@pytest.mark.asyncio
async def test_async_response_context_assertion_failure_attaches_allure():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 500, "msg": "error"})
    mock_response.text = AsyncMock(return_value='{"code": 500, "msg": "error"}')
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    with patch("har2pytest.client.allure.attach") as mock_attach:
        ctx = client.get("/api/test")
        with pytest.raises(AssertionError):
            async with ctx as r:
                data = await r.json()
                assert data["code"] == 200

        # 断言失败时应该附加 Allure 数据
        assert mock_attach.call_count >= 1


@allure.feature("异步客户端")
@allure.story("Allure 数据附加")
@allure.title("测试 DEBUG 级别下断言成功时也附加 Allure 数据")
@pytest.mark.asyncio
async def test_async_response_context_success_attachs_allure_when_debug():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 200})
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()
    mock_response.text = AsyncMock(return_value='{"code": 200}')

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    # 设置 logger 为 DEBUG 级别以触发 Allure 附件
    original_level = logger.level
    logger.setLevel(logging.DEBUG)
    try:
        with patch("har2pytest.client.allure.attach") as mock_attach:
            async with client.get("/api/test") as r:
                assert r.status == 200

            # DEBUG 级别下，断言成功时也会附加 Allure 数据
            assert mock_attach.call_count >= 1
    finally:
        logger.setLevel(original_level)


@allure.feature("异步客户端")
@allure.story("Session管理")
@allure.title("测试 session 复用")
@pytest.mark.asyncio
async def test_async_client_session_reuse():
    client = AsyncClient(base_url="https://example.com")

    session1 = await client._get_session()
    session2 = await client._get_session()

    assert session1 is session2


@allure.feature("异步客户端")
@allure.story("Session管理")
@allure.title("测试 close 关闭 session")
@pytest.mark.asyncio
async def test_async_client_close():
    client = AsyncClient(base_url="https://example.com")

    session = await client._get_session()
    session.close = AsyncMock()

    await client.close()
    session.close.assert_called_once()
    assert client._session is None


@allure.feature("异步客户端")
@allure.story("请求日志")
@allure.title("测试请求日志记录")
def test_async_client_log_request():
    client = AsyncClient(base_url="https://example.com")
    mock_logger = MagicMock()
    client.logger = mock_logger

    request_info = {
        "method": "GET",
        "url": "https://example.com/api/test",
        "headers": {"Authorization": "bearer xxx"},
        "params": {"key": "value"},
    }
    client._log_request("GET", "https://example.com/api/test", request_info)

    mock_logger.info.assert_called_once()
    call_args = mock_logger.info.call_args
    assert "Request data:" in call_args[0][0]


@allure.feature("异步客户端")
@allure.story("全局实例")
@allure.title("测试 async_client 全局实例")
def test_async_client_global_instance():
    assert isinstance(async_client, AsyncClient)
    assert async_client._session is None


@allure.feature("异步客户端")
@allure.story("响应体解析")
@allure.title("测试 _parse_response_body 解析 JSON 响应")
@pytest.mark.asyncio
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
@pytest.mark.asyncio
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
@allure.story("请求信息记录")
@allure.title("测试请求信息包含 params 参数")
@pytest.mark.asyncio
async def test_async_response_context_request_info_params():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 200})
    mock_response.text = AsyncMock(return_value='{"code": 200}')
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    ctx = client.get("/api/test", params={"pageNum": "1"})
    await ctx.__aenter__()

    assert ctx._request_info is not None
    assert "params" in ctx._request_info
    assert ctx._request_info["params"] == {"pageNum": "1"}


@allure.feature("异步客户端")
@allure.story("请求信息记录")
@allure.title("测试请求信息包含 json 参数")
@pytest.mark.asyncio
async def test_async_response_context_request_info_json():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 200})
    mock_response.text = AsyncMock(return_value='{"code": 200}')
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    ctx = client.post("/api/create", json={"name": "test"})
    await ctx.__aenter__()

    assert ctx._request_info is not None
    assert "json" in ctx._request_info
    assert ctx._request_info["json"] == {"name": "test"}


@allure.feature("异步客户端")
@allure.story("请求信息记录")
@allure.title("测试请求信息包含 FormData 参数")
@pytest.mark.asyncio
async def test_async_response_context_request_info_multipart():
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"code": 200})
    mock_response.text = AsyncMock(return_value='{"code": 200}')
    mock_response.raise_for_status = MagicMock()
    mock_response.release = AsyncMock()

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    # 模拟 aiohttp.FormData（异步模式）
    mock_data = MagicMock()
    mock_data.__class__.__name__ = "FormData"

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    ctx = client.post("/api/upload", data=mock_data)
    await ctx.__aenter__()

    assert ctx._request_info is not None
    assert "data" in ctx._request_info
    assert "文件上传请求" in ctx._request_info["data"]


@allure.feature("异步客户端")
@allure.story("异常处理")
@allure.title("测试 HTTP 错误状态码抛出异常")
@pytest.mark.asyncio
async def test_async_response_context_http_error():
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = AsyncMock(return_value={"error": "server error"})
    mock_response.text = AsyncMock(return_value='{"error": "server error"}')
    mock_response.raise_for_status = MagicMock(side_effect=Exception("500 Server Error"))
    mock_response.release = AsyncMock()

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.closed = False
    mock_session.headers = {}

    client = AsyncClient(base_url="https://example.com")
    client._session = mock_session

    ctx = client.get("/api/error")

    with pytest.raises(Exception):
        await ctx.__aenter__()

    mock_response.release.assert_called_once()
