"""
HTTP 客户端模块（同步 & 异步）。

提供同步（基于 requests）和异步（基于 aiohttp）的 HTTP 客户端，
集成 Allure 报告和日志系统。
"""

import json
import logging
import mimetypes
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


def _json_default(obj: Any) -> Any:
    """json.dumps 兜底：bytes（图片/二进制响应体）转 base64 摘要，其余转字符串。

    Allure 附件里的请求/响应 dict 可能包含二进制响应体（image/*），
    bytes 无法直接 JSON 序列化；这里转成可读摘要避免附件整体失败。
    """
    import base64

    if isinstance(obj, (bytes, bytearray)):
        raw = bytes(obj)
        if len(raw) > 2000:
            return f"[二进制 {len(raw)} bytes] {base64.b64encode(raw[:2000]).decode('ascii')}..."
        return base64.b64encode(raw).decode("ascii")
    return str(obj)


# 请求体对象上挂载"真实字段摘要"的属性名：Allure/日志据此展示实际发送的参数，
_DATA_FIELDS_ATTR = "_har2pytest_fields"
_DATA_FILES_ATTR = "_har2pytest_files"
# 请求体对象上挂载"已打开的文件句柄列表"的属性名：上下文管理器退出时统一关闭
_OPEN_FILES_ATTR = "_har2pytest_open_files"

# 单字段展示长度上限（避免长文本/二进制撑爆报告）
_DATA_VALUE_LIMIT = 200


def _shorten(value: Any, limit: int = _DATA_VALUE_LIMIT) -> str:
    """把值转成字符串并截断到 limit，超出补省略号。"""
    text = str(value)
    return text[:limit] + ("..." if len(text) > limit else "")


def _guess_content_type(file_path: str) -> str:
    """根据文件扩展名猜测 MIME 类型，无法识别时回退 application/octet-stream。"""
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def _close_attached_files(obj: Any) -> None:
    """关闭挂载在请求体对象上的文件句柄（build_multipart_data 打开的文件）。"""
    open_files = getattr(obj, _OPEN_FILES_ATTR, None)
    if open_files:
        for fh in open_files:
            try:
                fh.close()
            except Exception:
                pass


def _attach_body_summary(obj: Any, fields: dict, files: dict[str, str] | None = None) -> None:
    """把 multipart/表单请求的真实字段挂到 FormData/MultipartEncoder 对象上。

    Args:
        obj: 请求体对象（aiohttp FormData 或 requests_toolbelt MultipartEncoder）
        fields: 普通字段字典（值会截断为字符串）
        files: 文件字段摘要 {key: 文件名}（可选）
    """
    try:
        setattr(
            obj,
            _DATA_FIELDS_ATTR,
            {str(k): _shorten(v) for k, v in fields.items()},
        )
        if files:
            setattr(obj, _DATA_FILES_ATTR, {str(k): str(v) for k, v in files.items()})
    except Exception:  # noqa: BLE001
        # 挂载失败不影响请求本身
        pass


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
        # 优先展示真实字段（build_form_data/build_multipart_data 挂载的 dict 摘要）
        body_fields = getattr(data, _DATA_FIELDS_ATTR, None)
        if isinstance(body_fields, dict):
            request_info["data"] = body_fields
            body_files = getattr(data, _DATA_FILES_ATTR, None)
            if isinstance(body_files, dict):
                request_info["files"] = body_files
        elif upload_class_name and hasattr(data, "__class__") and upload_class_name in data.__class__.__name__:
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

    # 附加请求/响应数据（两段同构，循环收敛）
    for label, info in (("Request", request_info), ("Response", response_info)):
        try:
            allure.attach(
                json.dumps(info, indent=2, ensure_ascii=False, default=_json_default),
                name=f"{timestamp} {label} data",
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception as e:
            logger.error(f"添加 Allure {label} 数据失败: {e}")

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


# ---------------------------------------------------------------------------
# 同步 HTTP 客户端（基于 requests）
# ---------------------------------------------------------------------------


class ResponseContext:
    """同步 HTTP 响应上下文管理器。

    在 __enter__ 中发起请求；在 __exit__ 中：断言失败或 DEBUG 级别时自动将
    请求/响应数据附加到 Allure 报告，并释放响应连接。
    """

    def __init__(self, client: "Client", method: str, url: str, **kwargs):
        self._client = client
        self._method = method
        self._url = url
        self._kwargs = dict(kwargs)
        self._response: requests.Response | None = None
        self._request_info: dict = {}
        self._request_body: Any = None

    def __enter__(self) -> requests.Response:
        """发起 HTTP 请求并返回响应对象。"""
        full_url = f"{self._client.base_url}{self._url}"

        # 提取请求参数
        headers = self._kwargs.pop("headers", {})
        params = self._kwargs.pop("params", None)
        json_data = self._kwargs.pop("json", None)
        data = self._kwargs.pop("data", None)
        timeout = self._kwargs.pop("timeout", None)
        verify = self._kwargs.pop("verify", None)
        raise_for_status = self._kwargs.pop("raise_for_status", None)

        # 保存请求体引用，以便 __exit__ 关闭文件上传句柄
        self._request_body = data

        # 构建请求信息
        self._request_info = _build_request_info(
            self._method, full_url, headers, params, json_data, data, "MultipartEncoder"
        )

        # 确定超时和 verify
        final_timeout = timeout if timeout is not None else self._client.default_timeout
        final_verify = verify if verify is not None else self._client.default_verify
        final_raise = raise_for_status if raise_for_status is not None else self._client.raise_for_status

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

        # 检查响应状态码（raise_for_status 可配置关闭，便于断言/检查 4xx/5xx）
        if final_raise:
            try:
                self._response.raise_for_status()
            except Exception:
                self._response.close()
                raise

        return self._response

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，处理 Allure 附件并释放连接。"""
        if exc_type is not None or logger.isEnabledFor(logging.DEBUG):
            try:
                self._attach_to_allure(exc_val)
            except Exception as e:
                logger.error(f"附加 Allure 数据失败: {e}")

        # 关闭文件上传句柄（build_multipart_data 打开的文件）
        _close_attached_files(self._request_body)

        # 释放连接回 requests 连接池（避免长会话中 4xx/5xx 或未读 body 挂住连接）
        if self._response is not None:
            try:
                self._response.close()
            except Exception:
                pass

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
        """解析响应体（json/text/image；解析失败回退截断文本）。"""
        content_type = response.headers.get("Content-Type", "")
        try:
            if "application/json" in content_type:
                return response.json()
            if "text/html" in content_type:
                return response.text
            if "image/" in content_type:
                return response.content
        except Exception:
            pass
        try:
            return response.text[:500]
        except Exception:
            return "[无法读取响应体]"


class Client:
    """同步 HTTP 客户端封装，基于 requests。

    集成 Allure 报告和日志系统，断言失败时自动附加请求/响应数据到 Allure 报告。
    """

    def __init__(
        self,
        base_url: str = "",
        default_timeout: int = 30,
        default_verify: bool = False,
        raise_for_status: bool = False,
    ):
        self.base_url = base_url
        self.default_timeout = default_timeout
        self.default_verify = default_verify
        self.raise_for_status = raise_for_status
        self.logger = logger
        self.session = requests.Session()

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

    在 __aenter__ 中发起实际请求；在 __aexit__ 中：断言失败或 DEBUG 级别时
    自动将请求/响应数据附加到 Allure 报告，并释放响应连接。
    """

    def __init__(self, client: "AsyncClient", method: str, url: str, **kwargs):
        self._client = client
        self._method = method
        self._url = url
        self._kwargs = dict(kwargs)
        self._response = None
        self._request_info = {}
        self._request_body: Any = None

    async def __aenter__(self):
        """发起 HTTP 请求并返回响应对象。"""
        session = await self._client._get_session()
        full_url = f"{self._client.base_url}{self._url}"

        # 提取请求参数
        headers = self._kwargs.pop("headers", {})
        params = self._kwargs.pop("params", None)
        json_data = self._kwargs.pop("json", None)
        data = self._kwargs.pop("data", None)
        timeout = self._kwargs.pop("timeout", None)
        verify = self._kwargs.pop("verify", None)
        raise_for_status = self._kwargs.pop("raise_for_status", None)

        # 保存请求体引用，以便 __aexit__ 关闭文件上传句柄
        self._request_body = data

        # 构建请求信息
        self._request_info = _build_request_info(
            self._method, full_url, headers, params, json_data, data, "FormData"
        )

        # 确定超时和 verify（aiohttp 用 ssl= 表达，见 _get_session 的 TCPConnector）
        final_timeout = timeout if timeout is not None else self._client.default_timeout
        final_verify = verify if verify is not None else self._client.default_verify
        final_raise = raise_for_status if raise_for_status is not None else self._client.raise_for_status

        # 发起请求（aiohttp/yarl 不接受 None 查询参数值，过滤掉以对齐 requests 行为）
        request_kwargs = {}
        if params is not None:
            request_kwargs["params"] = {k: v for k, v in params.items() if v is not None}
        if json_data is not None:
            request_kwargs["json"] = json_data
        if data is not None:
            request_kwargs["data"] = data
        request_kwargs.update(self._kwargs)

        self._response = await session.request(
            self._method,
            full_url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=final_timeout) if final_timeout else None,
            ssl=final_verify,
            **request_kwargs,
        )

        # 检查响应状态码（raise_for_status 可配置关闭，便于断言/检查 4xx/5xx）
        if final_raise:
            try:
                self._response.raise_for_status()
            except Exception:
                if self._response:
                    await self._response.release()
                raise

        return self._response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，处理 Allure 附件和资源清理。"""
        if exc_type is not None or logger.isEnabledFor(logging.DEBUG):
            try:
                await self._attach_to_allure(exc_val)
            except Exception as e:
                logger.error(f"附加 Allure 数据失败: {e}")

        # 关闭文件上传句柄（build_multipart_data 打开的文件）
        _close_attached_files(self._request_body)

        if self._response:
            await self._response.release()

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
        """解析异步响应体（json/text/image；解析失败回退截断文本）。"""
        content_type = response.headers.get("Content-Type", "")
        try:
            if "application/json" in content_type:
                return await response.json()
            if "text/html" in content_type:
                return await response.text()
            if "image/" in content_type:
                return await response.read()
        except Exception:
            pass
        try:
            text = await response.text()
            return text[:500]
        except Exception:
            return "[无法读取响应体]"


class AsyncClient:
    """异步 HTTP 客户端封装，基于 aiohttp。

    集成 Allure 报告和日志系统，断言失败时自动附加请求/响应数据到 Allure 报告。
    """

    def __init__(self, base_url: str = "", default_timeout: int = 30, raise_for_status: bool = False, default_verify: bool = False):
        self.base_url = base_url
        self.default_timeout = default_timeout
        self.raise_for_status = raise_for_status
        self.default_verify = default_verify
        self._session = None
        self.logger = logger

    async def _get_session(self):
        """获取或创建 aiohttp ClientSession。"""
        if self._session is not None and not self._session.closed:
            return self._session

        # 关闭旧会话（None/已关闭时为 no-op），随后重建
        await self.close()

        connector = aiohttp.TCPConnector(ssl=self.default_verify)
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.default_timeout),
        )
        return self._session

    async def close(self):
        """关闭 aiohttp 会话。"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

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
    logger.debug(f"[build_multipart_data] 文件键: {file_key}, 字段: {list(files.keys())}")

    if client.is_async:
        from aiohttp import FormData

        data = FormData()
        plain_fields = {}
        for key in files:
            if key == file_key:
                file_path = files[file_key]
                filename = os.path.basename(file_path)
                fh = open(file_path, "rb")
                setattr(data, _OPEN_FILES_ATTR, getattr(data, _OPEN_FILES_ATTR, []) + [fh])
                data.add_field(
                    file_key,
                    fh,
                    filename=filename,
                    content_type=_guess_content_type(file_path),
                )
            else:
                data.add_field(key, files[key])
                plain_fields[key] = files[key]
        _attach_body_summary(data, plain_fields, {file_key: filename})
        return data, None
    else:
        from requests_toolbelt import MultipartEncoder

        filename = os.path.basename(files[file_key])
        fields = {}
        plain_fields = {}
        open_files = []
        for key, value in files.items():
            if key == file_key:
                fh = open(value, "rb")
                open_files.append(fh)
                fields[file_key] = (filename, fh, _guess_content_type(value))
            else:
                fields[key] = value
                plain_fields[key] = value
        m = MultipartEncoder(fields=fields)
        if open_files:
            setattr(m, _OPEN_FILES_ATTR, open_files)
        _attach_body_summary(m, plain_fields, {file_key: filename})
        return m, m.content_type


def build_form_data(data: dict) -> tuple[Any, str | None]:
    """构建 multipart/form-data 表单数据（无文件上传），自动适配同步/异步客户端。

    Args:
        data: 表单字段字典

    Returns:
        (data, content_type) 元组。异步模式 content_type 为 None，同步模式为 MultipartEncoder.content_type
    """
    if client.is_async:
        from aiohttp import FormData

        # default_to_multipart=True：纯字符串字段也要编码为真正的 multipart/form-data，
        # 否则 aiohttp 会退化成 application/x-www-form-urlencoded，与同步分支行为不一致
        form = FormData(default_to_multipart=True)
        for k, v in data.items():
            form.add_field(k, str(v))
        _attach_body_summary(form, data)
        return form, None
    else:
        from requests_toolbelt import MultipartEncoder

        m = MultipartEncoder(fields=data)
        _attach_body_summary(m, data)
        return m, m.content_type


# ---------------------------------------------------------------------------
# 全局实例
# ---------------------------------------------------------------------------

client = _ClientProxy(Client(base_url=os.environ.get("base_url", "")))
async_client = AsyncClient(base_url=os.environ.get("base_url", ""))
