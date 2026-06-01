# utils/request_wrapper.py
import functools
import json
import os
import time
from typing import Any
from urllib.parse import parse_qs, urlparse

import allure
import requests

from har2pytest.logger import logger

_last_request_response = None


def _value_with_color(value, thresholds):
    """
    根据阈值返回带颜色的HTML文本
    :param value: 数值
    :param thresholds: 阈值字典，如 {'red': 30, 'yellow': 8, 'green': 1}
    :return: HTML格式的带颜色文本
    """
    if value < thresholds.get("green", 0):
        color = "green"
    elif value < thresholds.get("yellow", 0):
        color = "orange"
    else:
        color = "red"

    return f'<span style="color: {color}; font-weight: bold;">{value:.3f}</span>'


def monitor_performance(threshold: float = 8.0):
    """
    性能监控装饰器

    :param threshold: 响应时间阈值(秒)，超过会记录警告
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            response = func(*args, **kwargs)

            elapsed = time.time() - start_time

            thresholds = {"red": 30, "yellow": threshold, "green": 1}
            # 记录性能数据
            if elapsed > threshold:
                logger.warning(f"{args} 接口响应时间超过阈值 ({threshold}s): {elapsed:.3f}s")
                # 添加到 Allure 报告
                allure.attach(
                    f"{args[0]} 响应时间: {_value_with_color(elapsed, thresholds)} s",
                    name="性能监控",
                    attachment_type=allure.attachment_type.HTML,
                )
            return response

        return wrapper

    return decorator


class Client:
    """HTTP客户端封装，集成Allure报告和日志系统"""

    def __init__(
        self,
        base_url: str = "",
        default_timeout: int = 30,
        default_verify: bool = False,
    ):
        self.base_url = base_url
        self.default_timeout = default_timeout
        self.default_verify = default_verify
        self.logger = logger
        self.session = requests.Session()
        self._setup_default_headers()

    def _setup_default_headers(self):
        """初始化默认请求头"""
        self.session.headers.update(
            {
                # 'User-Agent': 'APIClient/1.0',
                # 'Accept': 'application/json',
                # 'Content-Type': 'application/json',
                "channel": "pc",
                # "client": "mall",
                "GW-Client": "test",
            }
        )

    def _log_request(self, method: str, url: str, **kwargs):
        """结构化日志记录请求"""
        log_data = {
            "method": method.upper(),
            "url": url,
            "headers": dict(self.session.headers),
        }

        if "params" in kwargs:
            log_data["params"] = kwargs["params"]
        elif "json" in kwargs:
            log_data["json"] = kwargs["json"]
        elif "data" in kwargs:
            # 检查是否为文件上传请求（MultipartEncoder对象）
            data = kwargs["data"]
            if hasattr(data, "__class__") and "MultipartEncoder" in data.__class__.__name__:
                log_data["data"] = "[文件上传请求 - MultipartEncoder对象]"
            else:
                log_data["data"] = data

        self.logger.info("Request data:", extra={"request": log_data})

    def _log_response(self, response: requests.Response):
        """结构化日志记录响应"""
        try:
            body = response.json() if "json" in response.headers.get("Content-Type", "") else response.text[:500]
        except Exception:
            body = response.text[:500]

        log_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
        }
        self.logger.info("Response data:", extra={"response": log_data})

    def _attach_to_allure(self, response: requests.Response):
        """向Allure添加完整请求/响应信息"""
        # 响应信息
        body = _parse_data(response)

        try:
            # 请求信息
            if response.request.method == "GET":
                parsed_url = urlparse(response.request.url)  # 从response.request获取原始URL
                params = parse_qs(parsed_url.query)  # 解析URL获取查询参数
                if params:
                    allure.attach(
                        json.dumps(
                            {
                                "url": response.request.url,
                                "method": response.request.method,
                                "headers": dict(response.request.headers),
                                "params": params,
                            },
                            indent=2,
                            ensure_ascii=False,
                        ),
                        name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Request body",
                        attachment_type=allure.attachment_type.JSON,
                    )
                else:
                    allure.attach(
                        json.dumps(
                            {
                                "url": response.request.url,
                                "method": response.request.method,
                                "headers": dict(response.request.headers),
                                "params": None,
                            },
                            indent=2,
                            ensure_ascii=False,
                        ),
                        name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Request body",
                        attachment_type=allure.attachment_type.JSON,
                    )
            else:
                allure.attach(
                    json.dumps(
                        {
                            "url": response.request.url,
                            "method": response.request.method,
                            "headers": dict(response.request.headers),
                            "body": _parse_body(response.request),
                        },
                        indent=2,
                        ensure_ascii=False,
                    ),
                    name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Request body",
                    attachment_type=allure.attachment_type.JSON,
                )
        except Exception as e:
            logger.error(f"Add Allure request content err: {str(e)} - {response.request.url}")
        try:
            allure.attach(
                json.dumps(
                    {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "body": body,
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Response data",
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception as e:
            logger.error(f"Add Allure response content err: {str(e)} - {response.request.url} - {response.text}")

    @monitor_performance()
    def request(
        self,
        method: str,
        url: str = "",
        timeout: int | None = None,
        verify: bool | None = None,
        **kwargs,
    ) -> requests.Response:
        """执行HTTP请求"""
        # url = urljoin(self.base_url, url)
        url = f"{self.base_url}{url}"

        # 确定超时和verify设置
        final_timeout = timeout if timeout is not None else self.default_timeout
        final_verify = verify if verify is not None else self.default_verify

        # 记录请求
        self._log_request(method, url, **kwargs)

        try:
            response = self.session.request(method, url, timeout=final_timeout, verify=final_verify, **kwargs)

            # 记录响应
            self._log_response(response)

            self._attach_to_allure(response)
            global _last_request_response
            _last_request_response = response

            # 验证状态码
            response.raise_for_status()

            return response

        except Exception as e:
            self.logger.error(f"Request failed: {str(e)}", exc_info=True)
            allure.attach(
                str(e),
                name="Request Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise

    def get(self, url: str = "", **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url: str = "", **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url: str = "", **kwargs):
        return self.request("PUT", url, **kwargs)


def _parse_body(response) -> Any:
    """解析请求体"""

    if not response.body:
        return None

    # 检查是否为文件上传请求（MultipartEncoder对象）
    if hasattr(response.body, "__class__") and "MultipartEncoder" in response.body.__class__.__name__:
        # 文件上传请求，返回友好的描述信息而不是尝试序列化MultipartEncoder
        return "[文件上传请求 - MultipartEncoder对象]"

    # 根据Content-Type选择解析方式
    content_type = response.headers.get("Content-Type", "")
    # 如果body是字节类型，先解码为字符串
    body = response.body.decode("utf-8") if isinstance(response.body, bytes) else response.body

    if "application/json" in content_type:
        try:
            return json.loads(body)
        except Exception:
            return body

    return body


def _parse_data(response) -> Any:
    """解析响应体"""

    # 根据Content-Type选择解析方式
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            data = response.json()
        except Exception:
            data = response.text
    elif "text/html" in content_type:
        data = response.text

    elif "image/" in content_type:
        data = response.content
    else:
        data = response.text  # 默认处理
    return data


def _attach_to_allure():
    """向Allure添加完整请求/响应信息"""
    # 响应信息
    global _last_request_response
    response = _last_request_response
    body = _parse_data(response)

    try:
        # 请求信息
        if response.request.method == "GET":
            parsed_url = urlparse(response.request.url)  # 从response.request获取原始URL
            params = parse_qs(parsed_url.query)  # 解析URL获取查询参数
            if params:
                allure.attach(
                    json.dumps(
                        {
                            "url": response.request.url,
                            "method": response.request.method,
                            "headers": dict(response.request.headers),
                            "params": params,
                        },
                        indent=2,
                        ensure_ascii=False,
                    ),
                    name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Request body",
                    attachment_type=allure.attachment_type.JSON,
                )
            else:
                allure.attach(
                    json.dumps(
                        {
                            "url": response.request.url,
                            "method": response.request.method,
                            "headers": dict(response.request.headers),
                            "params": None,
                        },
                        indent=2,
                        ensure_ascii=False,
                    ),
                    name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Request body",
                    attachment_type=allure.attachment_type.JSON,
                )
        else:
            allure.attach(
                json.dumps(
                    {
                        "url": response.request.url,
                        "method": response.request.method,
                        "headers": dict(response.request.headers),
                        "body": _parse_body(response.request),
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Request body",
                attachment_type=allure.attachment_type.JSON,
            )
    except Exception as e:
        logger.error(f"Add Allure request content err: {str(e)} - {response.request.url}")
    try:
        allure.attach(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": body,
                },
                indent=2,
                ensure_ascii=False,
            ),
            name=f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Response data",
            attachment_type=allure.attachment_type.JSON,
        )
    except Exception as e:
        logger.error(f"Add Allure response content err: {str(e)} - {response.request.url} - {response.text}")


client = Client(base_url=os.environ["base_url"])
