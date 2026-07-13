"""
HTTP 客户端模块（同步 & 异步）。

提供同步（基于 requests）和异步（基于 aiohttp）的 HTTP 客户端，
集成 Allure 报告和日志系统。
"""

import json
import logging
import os
import time
from typing import Any

import aiohttp
import allure
import requests

from .logger import logger

# ---------------------------------------------------------------------------
# 共享工具函数
# ---------------------------------------------------------------------------


def _value_with_color(value: float, thresholds: dict) -> str:
    """根据阈值返回带颜色的 HTML 文本。"""
    if value < thresholds.get("green", 0):
        color = "green"
    elif value < thresholds.get("yellow", 0):
        color = "orange"
    else:
        color = "red"
    return f'<span style="color: {color}; font-weight: bold;">{value:.3f}</span>'


def _build_request_info(method: str, full_url: str, headers: dict, params, json_data, data, upload_class_name: str | None = None) -> dict:
    """构建请求信息字典（同步/异步共用）。

    Args:
        method: HTTP 方法
        full_url: 完整 URL
        headers: 请求头
        params: 查询参数
        json_data: JSON 数据
        data: 请求体数据
        upload_class_name: 文件上传对象的类名标识（如 "MultipartEncoder" 或 "FormData"）
    """
    request_info = {
        "url": full_url,
        "method": method,
        "headers": headers,
    }
    if params is not None:
        request_info["params"] = params
    if json_data is not None:
        request_info["json"] = json_data
    if data is not None:
        if upload_class_name and hasattr(data, "__class__") and upload_class_name in data.__class__.__name__:
            request_info["data"] = f"[文件上传请求 - {upload_class_name}对象]"
        else:
            request_info["data"] = str(data)[:500]
    return request_info


def _attach_request_response_to_allure(request_info: dict, response_info: dict, exc_val: BaseException | None = None):
    """将请求和响应数据附加到 Allure 报告（同步/异步共用）。

    Args:
        request_info: 请求信息字典
        response_info: 响应信息字典
        exc_val: 异常对象（断言失败时传入）
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 附加请求数据
    try:
        allure.attach(
            json.dumps(request_info, indent=2, ensure_ascii=False),
            name=f"{timestamp} Request data",
            attachment_type=allure.attachment_type.JSON,
        )
    except Exception as e:
        logger.error(f"添加 Allure 请求数据失败: {e}")

    # 附加响应数据
    try:
        allure.attach(
            json.dumps(response_info, indent=2, ensure_ascii=False),
            name=f"{timestamp} Response data",
            attachment_type=allure.attachment_type.JSON,
        )
    except Exception as e:
        logger.error(f"添加 Allure 响应数据失败: {e}")

    # 附加错误信息（仅断言失败时）
    if exc_val is not None:
        try:
            allure.attach(
                str(exc_val),
                name="Assertion Error",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception:
            pass


def _build_log_request_data(method: str, url: str, request_info: dict) -> dict:
    """构建请求日志数据（同步/异步共用）。"""
    log_data = {
        "method": method.upper(),
        "url": url,
        "headers": request_info.get("headers", {}),
    }
    if "params" in request_info:
        log_data["params"] = request_info["params"]
    elif "json" in request_info:
        log_data["json"] = request_info["json"]
    elif "data" in request_info:
        log_data["data"] = request_info["data"]
    return log_data


# ---------------------------------------------------------------------------
# 同步 HTTP 客户端（基于 requests）
# ---------------------------------------------------------------------------


class ResponseContext:
    """同步 HTTP 响应上下文管理器。

    在 __enter__ 中发起请求并记录请求/响应数据，
    在 __exit__ 中：断言失败或 DEBUG 级别时自动将请求/响应数据附加到 Allure 报告。
    """

    def __init__(self, client: "Client", method: str, url: str, **kwargs):
        self._client = client
        self._method = method
        self._url = url
        self._kwargs = dict(kwargs)
        self._response: requests.Response | None = None
        self._request_info: dict = {}
        self._start_time: float | None = None

    def __enter__(self) -> requests.Response:
        """发起 HTTP 请求并返回响应对象。"""
        self._start_time = time.time()
        full_url = f"{self._client.base_url}{self._url}"

        # 提取请求参数
        headers = self._kwargs.pop("headers", {})
        params = self._kwargs.pop("params", None)
        json_data = self._kwargs.pop("json", None)
        data = self._kwargs.pop("data", None)
        timeout = self._kwargs.pop("timeout", None)
        verify = self._kwargs.pop("verify", None)

        # 构建请求信息
        self._request_info = _build_request_info(
            self._method, full_url, headers, params, json_data, data, "MultipartEncoder"
        )

        # 确定超时和 verify
        final_timeout = timeout if timeout is not None else self._client.default_timeout
        final_verify = verify if verify is not None else self._client.default_verify

        # 发起请求
        request_kwargs = {}
        if params is not None:
            request_kwargs["params"] = params
        if json_data is not None:
            request_kwargs["json"] = json_data
        if data is not None:
            request_kwargs["data"] = data
        request_kwargs.update(self._kwargs)

        self._response = self._client.session.request(
            self._method,
            full_url,
            headers=headers,
            timeout=final_timeout,
            verify=final_verify,
            **request_kwargs,
        )

        # 检查响应状态码
        self._response.raise_for_status()

        return self._response

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，处理 Allure 附件。"""
        if exc_type is not None or logger.isEnabledFor(logging.DEBUG):
            try:
                self._attach_to_allure(exc_val)
            except Exception as e:
                logger.error(f"附加 Allure 数据失败: {e}")

        return False  # 不抑制异常

    def _attach_to_allure(self, exc_val: BaseException | None = None):
        """将请求和响应数据附加到 Allure 报告。"""
        if self._response is None:
            return
        body = self._parse_response_body(self._response)

        response_info = {
            "status": self._response.status_code,
            "headers": dict(self._response.headers),
            "body": body,
        }

        _attach_request_response_to_allure(self._request_info, response_info, exc_val)

    @staticmethod
    def _parse_response_body(response: requests.Response) -> Any:
        """解析响应体。"""
        content_type = response.headers.get("Content-Type", "")
        try:
            if "application/json" in content_type:
                return response.json()
            elif "text/html" in content_type:
                return response.text
            elif "image/" in content_type:
                return response.content
            else:
                return response.text[:500]
        except Exception:
            try:
                return response.text[:500]
            except Exception:
                return "[无法读取响应体]"


class Client:
    """同步 HTTP 客户端封装，基于 requests。

    集成 Allure 报告和日志系统，断言失败时自动附加请求/响应数据到 Allure 报告。
    """

    def __init__(self, base_url: str = "", default_timeout: int = 30, default_verify: bool = False):
        self.base_url = base_url
        self.default_timeout = default_timeout
        self.default_verify = default_verify
        self.logger = logger
        self.session = requests.Session()

    def _log_request(self, method: str, url: str, request_info: dict):
        """记录请求日志。"""
        log_data = _build_log_request_data(method, url, request_info)
        self.logger.info(f"Request data: {log_data}")

    def _log_response(self, response: requests.Response):
        """记录响应日志。"""
        try:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                body = response.json()
            else:
                body = response.text[:500]
        except Exception:
            body = "[无法读取响应体]"

        log_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
        }
        self.logger.info(f"Response data: {log_data}")

    def request(self, method: str, url: str = "", **kwargs) -> ResponseContext:
        """创建同步请求上下文管理器。

        Args:
            method: HTTP 请求方法（GET/POST/PUT/DELETE/PATCH等）
            url: 请求 URL 路径
            **kwargs: 请求参数（headers, params, json, data, timeout, verify等）

        Returns:
            ResponseContext: 响应上下文管理器
        """
        return ResponseContext(self, method, url, **kwargs)

    def get(self, url: str = "", **kwargs) -> ResponseContext:
        """创建 GET 请求上下文管理器。"""
        return self.request("GET", url, **kwargs)

    def post(self, url: str = "", **kwargs) -> ResponseContext:
        """创建 POST 请求上下文管理器。"""
        return self.request("POST", url, **kwargs)

    def put(self, url: str = "", **kwargs) -> ResponseContext:
        """创建 PUT 请求上下文管理器。"""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str = "", **kwargs) -> ResponseContext:
        """创建 DELETE 请求上下文管理器。"""
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str = "", **kwargs) -> ResponseContext:
        """创建 PATCH 请求上下文管理器。"""
        return self.request("PATCH", url, **kwargs)


# ---------------------------------------------------------------------------
# 异步 HTTP 客户端（基于 aiohttp）
# ---------------------------------------------------------------------------


class AsyncResponseContext:
    """异步 HTTP 响应上下文管理器。

    在 __aenter__ 中发起实际请求并记录请求/响应数据，
    在 __aexit__ 中：断言失败时自动将请求/响应数据附加到 Allure 报告。
    """

    def __init__(self, client: "AsyncClient", method: str, url: str, **kwargs):
        self._client = client
        self._method = method
        self._url = url
        self._kwargs = dict(kwargs)
        self._response = None
        self._request_info = {}
        self._start_time = None

    async def __aenter__(self):
        """发起 HTTP 请求并返回响应对象。"""
        self._start_time = time.time()
        session = await self._client._get_session()
        full_url = f"{self._client.base_url}{self._url}"

        # 提取请求参数
        headers = self._kwargs.pop("headers", {})
        params = self._kwargs.pop("params", None)
        json_data = self._kwargs.pop("json", None)
        data = self._kwargs.pop("data", None)
        timeout = self._kwargs.pop("timeout", None)

        # 构建请求信息
        self._request_info = _build_request_info(
            self._method, full_url, headers, params, json_data, data, "FormData"
        )

        # 发起请求
        request_kwargs = {}
        if params is not None:
            request_kwargs["params"] = params
        if json_data is not None:
            request_kwargs["json"] = json_data
        if data is not None:
            request_kwargs["data"] = data
        request_kwargs.update(self._kwargs)

        self._response = await session.request(
            self._method,
            full_url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=timeout) if timeout else None,
            **request_kwargs,
        )

        # 检查响应状态码
        try:
            self._response.raise_for_status()
        except Exception:
            if self._response:
                self._response.release()
            raise

        return self._response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，处理 Allure 附件和资源清理。"""
        if exc_type is not None or logger.isEnabledFor(logging.DEBUG):
            try:
                await self._attach_to_allure(exc_val)
            except Exception as e:
                logger.error(f"附加 Allure 数据失败: {e}")

        if self._response:
            self._response.release()

        return False  # 不抑制异常

    async def _attach_to_allure(self, exc_val: BaseException | None = None):
        """将请求和响应数据附加到 Allure 报告。"""
        if self._response is None:
            return

        body = await self._parse_response_body(self._response)

        response_info = {
            "status": self._response.status,
            "headers": dict(self._response.headers),
            "body": body,
        }

        _attach_request_response_to_allure(self._request_info, response_info, exc_val)

    async def _parse_response_body(self, response) -> Any:
        """解析异步响应体。"""
        content_type = response.headers.get("Content-Type", "")
        try:
            if "application/json" in content_type:
                return await response.json()
            elif "text/html" in content_type:
                return await response.text()
            elif "image/" in content_type:
                return await response.read()
            else:
                text = await response.text()
                return text[:500]
        except Exception:
            try:
                text = await response.text()
                return text[:500]
            except Exception:
                return "[无法读取响应体]"


class AsyncClient:
    """异步 HTTP 客户端封装，基于 aiohttp。

    集成 Allure 报告和日志系统，断言失败时自动附加请求/响应数据到 Allure 报告。
    """

    def __init__(self, base_url: str = "", default_timeout: int = 30):
        self.base_url = base_url
        self.default_timeout = default_timeout
        self._session = None
        self.logger = logger

    async def _get_session(self):
        """获取或创建 aiohttp ClientSession。"""

        if self._session is not None and not self._session.closed:
            connector = self._session.connector
            if isinstance(connector, aiohttp.TCPConnector):
                try:
                    loop = getattr(connector, "_loop", None)
                    if loop is not None and not loop.is_closed():
                        return self._session
                except Exception:
                    pass
            else:
                return self._session

        if self._session is not None:
            try:
                await self._session.close()
            except Exception:
                pass
            self._session = None

        headers = {}
        connector = aiohttp.TCPConnector(ssl=False)
        self._session = aiohttp.ClientSession(
            headers=headers,
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.default_timeout),
        )
        return self._session

    async def close(self):
        """关闭 aiohttp 会话。"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    def _log_request(self, method: str, url: str, request_info: dict):
        """记录请求日志。"""
        log_data = _build_log_request_data(method, url, request_info)
        self.logger.info(f"Request data: {log_data}")

    async def _log_response(self, response):
        """记录响应日志。"""
        try:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                body = await response.json()
            else:
                body = await response.text()
                body = body[:500]
        except Exception:
            body = "[无法读取响应体]"

        log_data = {
            "status_code": response.status,
            "headers": dict(response.headers),
            "body": body,
        }
        self.logger.info(f"Response data: {log_data}")

    def request(self, method: str, url: str = "", **kwargs) -> AsyncResponseContext:
        """创建异步请求上下文管理器。"""
        return AsyncResponseContext(self, method, url, **kwargs)

    def get(self, url: str = "", **kwargs) -> AsyncResponseContext:
        """创建 GET 请求上下文管理器。"""
        return self.request("GET", url, **kwargs)

    def post(self, url: str = "", **kwargs) -> AsyncResponseContext:
        """创建 POST 请求上下文管理器。"""
        return self.request("POST", url, **kwargs)

    def put(self, url: str = "", **kwargs) -> AsyncResponseContext:
        """创建 PUT 请求上下文管理器。"""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str = "", **kwargs) -> AsyncResponseContext:
        """创建 DELETE 请求上下文管理器。"""
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str = "", **kwargs) -> AsyncResponseContext:
        """创建 PATCH 请求上下文管理器。"""
        return self.request("PATCH", url, **kwargs)


# ---------------------------------------------------------------------------
# 客户端代理 & 统一文件上传
# ---------------------------------------------------------------------------


class _ClientProxy:
    """客户端代理，支持运行时切换同步/异步客户端。

    生成的 API 文件通过 from har2pytest.client import client 导入此代理。
    异步测试用例可通过 client.set_client(async_client) 切换为异步客户端。
    """

    def __init__(self, default_client):
        self._client = default_client

    def set_client(self, new_client):
        """切换当前客户端实例。

        Args:
            new_client: 新的客户端实例（Client 或 AsyncClient）
        """
        self._client = new_client

    @property
    def is_async(self) -> bool:
        """当前是否使用异步客户端。"""
        return isinstance(self._client, AsyncClient)

    def __getattr__(self, name):
        return getattr(self._client, name)


def build_multipart_data(files: dict, file_key: str) -> tuple[Any, str | None]:
    """构建文件上传数据，自动适配同步/异步客户端。

    Args:
        files: 文件参数字典，包含文件路径和其他表单字段
        file_key: 文件参数的键名

    Returns:
        (data, content_type) 元组。异步模式 content_type 为 None，同步模式为 MultipartEncoder.content_type
    """
    logger.debug(f"[build_multipart_data] 开始构建文件上传数据，文件键: {file_key}, 字段: {list(files.keys())}")

    if client.is_async:
        logger.debug("[build_multipart_data] 当前为异步模式，使用 aiohttp FormData")
        from aiohttp import FormData

        data = FormData()
        for key in files:
            if key == file_key:
                file_path = files[file_key]
                filename = os.path.basename(file_path)
                logger.debug(f"[build_multipart_data] 添加文件字段: {file_key}={file_path} (filename={filename})")
                data.add_field(
                    file_key,
                    open(file_path, "rb"),
                    filename=filename,
                    content_type="text/plain",
                )
            else:
                logger.debug(f"[build_multipart_data] 添加普通字段: {key}={files[key]}")
                data.add_field(key, files[key])
        logger.debug("[build_multipart_data] FormData 构建完成，content_type=None")
        return data, None
    else:
        logger.debug("[build_multipart_data] 当前为同步模式，使用 requests_toolbelt MultipartEncoder")
        from requests_toolbelt import MultipartEncoder

        filename = os.path.basename(files[file_key])
        fields = {}
        for key, value in files.items():
            if key == file_key:
                logger.debug(f"[build_multipart_data] 添加文件字段: {file_key}={value} (filename={filename})")
                fields[file_key] = (filename, open(value, "rb"), "text/plain")
            else:
                logger.debug(f"[build_multipart_data] 添加普通字段: {key}={value}")
                fields[key] = value
        m = MultipartEncoder(fields=fields)
        logger.debug(f"[build_multipart_data] MultipartEncoder 构建完成, content_type: {m.content_type}")
        return m, m.content_type


def build_form_data(data: dict) -> tuple[Any, str | None]:
    """构建 multipart/form-data 表单数据（无文件上传），自动适配同步/异步客户端。

    Args:
        data: 表单字段字典

    Returns:
        (data, content_type) 元组。异步模式 content_type 为 None，同步模式为 MultipartEncoder.content_type
    """
    logger.debug(f"[build_form_data] 开始构建 multipart 表单数据，字段数量: {len(data)}")
    logger.debug(f"[build_form_data] 输入字段: {list(data.keys())}")

    if client.is_async:
        logger.debug("[build_form_data] 当前为异步模式，使用 aiohttp FormData")
        from aiohttp import FormData

        form = FormData()
        for k, v in data.items():
            str_v = str(v)
            logger.debug(f"[build_form_data] 添加字段: {k}={str_v[:200]}{'...' if len(str_v) > 200 else ''}")
            form.add_field(k, str_v)
        logger.debug("[build_form_data] FormData 构建完成，content_type=None")
        return form, None
    else:
        logger.debug("[build_form_data] 当前为同步模式，使用 requests_toolbelt MultipartEncoder")
        from requests_toolbelt import MultipartEncoder

        m = MultipartEncoder(fields=data)
        logger.debug(f"[build_form_data] MultipartEncoder 构建完成, content_type: {m.content_type}")
        return m, m.content_type


# ---------------------------------------------------------------------------
# 全局实例
# ---------------------------------------------------------------------------

client = _ClientProxy(Client(base_url=os.environ.get("base_url", "")))
async_client = AsyncClient(base_url=os.environ.get("base_url", ""))
