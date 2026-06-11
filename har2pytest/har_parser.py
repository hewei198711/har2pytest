"""HAR 文件解析器模块。

提供从 HAR（HTTP Archive）文件中提取和解析 API 请求信息的功能。
"""

import json
from typing import Any
from urllib.parse import unquote

from .config import APIConfig
from .logger import logger
from .url_matcher import URLMatcher


class HARParser:
    """HAR 文件解析器类。

    用于从 HAR 文件中提取 API 请求信息，支持过滤无效参数、重复 URL 等功能。
    """

    def __init__(self, base_urls: str = None, kill_urls: str = None):
        """初始化 HAR 解析器。

        Args:
            base_urls: 基础 URL 列表，用于从完整 URL 中提取相对路径（可选）。
            kill_urls: 需要过滤的 URL 关键字列表（可选）。
        """
        self.base_urls = base_urls if base_urls is not None else APIConfig.BASE_URLS()
        self.kill_urls = kill_urls if kill_urls is not None else APIConfig.KILL_URLS()

    def extract_requests_from_har(self, har_file_path: str, filter_duplicate_url: bool = True) -> list[dict[str, Any]]:
        """从 HAR 文件中提取请求信息。

        Args:
            har_file_path: HAR 文件路径。
            filter_duplicate_url: 是否过滤重复的 URL（默认 True）。

        Returns:
            list[dict[str, Any]]: 包含请求信息的字典列表。每个字典包含以下字段：
                - method: HTTP 方法
                - url: 清理后的 URL
                - full_url: 完整的 URL
                - headers: 请求头
                - content_type: 内容类型
                - cookies: Cookie 字典
                - query_params: 查询参数
                - post_data: POST 数据
                - response_status: 响应状态码
                - response_content: 响应内容
                - response_time: 响应时间（毫秒）
                - server_ip: 服务器 IP 地址
        """
        try:
            with open(har_file_path, encoding="utf-8") as f:
                har_data = json.load(f)
        except FileNotFoundError:
            logger.info(f"HAR文件不存在: {har_file_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"HAR文件JSON格式错误: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"读取HAR文件失败: {str(e)}")
            return []

        requests = []
        seen_urls = set()
        entries = har_data.get("log", {}).get("entries", [])

        if not entries:
            logger.info("HAR文件中没有找到请求记录")
            return []

        logger.info(f"开始解析HAR文件，共 {len(entries)} 个请求记录")

        for i, entry in enumerate(entries):
            if entry.get("_resourceType") != "xhr":
                continue

            request = entry.get("request", {})
            response = entry.get("response", {})

            full_url = request.get("url", "")
            should_skip = False
            for kill_url in self.kill_urls:
                if kill_url in full_url:
                    should_skip = True
                    logger.debug(f"过滤URL: {full_url} (包含关键字: {kill_url})")
                    break

            if should_skip:
                continue

            headers = {}
            for header in request.get("headers", []):
                headers[header["name"]] = header["value"]

            # 过滤 headers

            headers = self._filter_headers(headers)

            query_params = {}
            for param in request.get("queryString", []):
                query_params[param["name"]] = (
                    unquote(param["value"]) if isinstance(param["value"], str) else param["value"]
                )

            # 过滤 query参数
            query_params = self._filter_invalid_params(query_params)

            # 获取 POST 数据，过滤无效参数和空值
            post_data = None
            content_type = ""
            if request.get("postData"):
                post_data_text = request["postData"].get("text", "")
                content_type = request["postData"].get("mimeType", "")

                if content_type.startswith("multipart/form-data"):
                    params = request["postData"].get("params", [])
                    post_data = {}
                    for param in params:
                        post_data[param["name"]] = (
                            unquote(param.get("value", ""))
                            if isinstance(param.get("value"), str)
                            else param.get("value", "")
                        )
                    post_data = self._filter_invalid_params(post_data)
                elif content_type.startswith("application/json"):
                    try:
                        post_data = json.loads(post_data_text)
                        post_data = self._filter_invalid_params(post_data)
                    except json.JSONDecodeError:
                        post_data = post_data_text
                else:
                    raise ValueError(f"不支持的Content-Type: {content_type}, URL: {full_url}")

            # 响应内容
            response_content = None
            if response.get("content", {}).get("text"):
                response_text = response["content"]["text"]
                try:
                    response_content = json.loads(response_text)
                except json.JSONDecodeError:
                    response_content = response_text

            # 清理 URL，移除 query 参数
            clean_url = full_url  # 默认值
            if self.base_urls:
                clean_url = URLMatcher.normalize_url(full_url, self.base_urls)
            # 如果没有配置 base_urls，尝试使用 origin header
            else:
                origin = headers.get("origin", headers.get("Origin", ""))
                if origin and full_url.startswith(origin):
                    clean_url = URLMatcher.normalize_url(full_url[len(origin):])
                    logger.debug(f"使用 origin header 作为 base URL: {origin}")

            request_info = {
                "method": request.get("method", "GET"),
                "url": clean_url,
                "full_url": full_url,
                "headers": headers,
                "content_type": content_type,
                "cookies": dict(request.get("cookies", [])),
                "query_params": query_params,
                "post_data": post_data,
                "response_status": response.get("status", 0),
                "response_content": response_content,
                "response_time": entry.get("time", 0),
                "server_ip": entry.get("serverIPAddress", ""),
            }

            # 过滤重复 URL
            if filter_duplicate_url:
                url_key = f"{request_info['method']}:{clean_url}"
                if url_key in seen_urls:
                    continue
                seen_urls.add(url_key)

            requests.append(request_info)

        logger.info(f"解析完成，提取到 {len(requests)} 个有效的API请求")
        return requests

    def _filter_invalid_params(self, data: dict[str, Any]) -> dict[str, Any]:
        """过滤无效参数。

        根据配置中的 INVALID_PARAMS 过滤掉不需要的参数。

        Args:
            data: 原始参数字典。

        Returns:
            dict[str, Any]: 过滤后的参数字典。
        """
        if not isinstance(data, dict):
            logger.warning(f"期望dict类型，实际收到 {type(data)}，跳过过滤")
            return data if data else {}

        filtered_data = {}
        invalid_params = APIConfig.INVALID_PARAMS()
        for key, value in data.items():
            if key not in invalid_params:
                filtered_data[key] = value
            else:
                logger.debug(f"过滤无效参数: {key} = {value}")

        return filtered_data

    def _filter_headers(self, headers: dict[str, str]) -> dict[str, str]:
        """过滤 headers，只保留配置中指定的和必要的 headers。

        Args:
            headers: 原始 headers 字典。

        Returns:
            dict[str, str]: 过滤后的 headers 字典。
        """
        if not isinstance(headers, dict):
            return headers

        headers_to_include = APIConfig.HEADERS_TO_INCLUDE()
        # 如果没有配置 HEADERS_TO_INCLUDE，返回所有 headers
        if not headers_to_include:
            return headers

        # 获取 headers 名称集合（支持字典格式）
        if isinstance(headers_to_include, dict):
            headers_to_include = set(headers_to_include.keys())

        # 基础关键 headers，用于后续处理
        base_required_headers = {"content-type", "content-length", "origin"}
        # 从配置中获取 REQUIRED_HEADERS
        config_required_headers = APIConfig.REQUIRED_HEADERS()
        if isinstance(config_required_headers, dict):
            config_required_headers = set(config_required_headers.keys())
        else:
            config_required_headers = set()
        # 合并所有需要保留的 headers
        required_headers = base_required_headers | config_required_headers
        headers_to_keep = set([h.lower() for h in headers_to_include] + list(required_headers))

        filtered_headers = {}
        for key, value in headers.items():
            if key.lower() in headers_to_keep:
                filtered_headers[key] = value
            else:
                logger.debug(f"过滤 header: {key} = {value}")

        return filtered_headers

    def print_api_summary(self, har_file_path: str):
        """打印 API 请求摘要信息。

        Args:
            har_file_path: HAR 文件路径。
        """
        requests = self.extract_requests_from_har(har_file_path)

        logger.info(f"\nHAR文件: {har_file_path}")
        logger.info(f"共发现 {len(requests)} 个API请求")
        logger.info("-" * 80)

        if not requests:
            logger.info("没有找到有效的API请求")
            return

        success_count = sum(1 for req in requests if 200 <= req["response_status"] < 300)
        error_count = len(requests) - success_count
        avg_time = sum(req["response_time"] for req in requests) / len(requests)

        for i, req in enumerate(requests, 1):
            status = req["response_status"]
            time = req["response_time"]
            url = req["url"][:80]
            method = req["method"]

            logger.info(f"{i:2d}. {method:6s} {status:3d} {time:8.2f}ms {url}")

        logger.info("-" * 80)
        logger.info(f"统计: 成功 {success_count} 个, 失败 {error_count} 个, 平均响应时间 {avg_time:.2f}ms")
