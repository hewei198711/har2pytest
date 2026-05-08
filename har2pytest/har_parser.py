import json
from typing import Any
from urllib.parse import unquote

from .config import APIConfig
from .logger import logger


class HARParser:
    """HAR文件解析器类"""

    def __init__(self, base_urls: str = None, kill_urls: str = None):
        """
        初始化HAR解析器
        """
        self.base_urls = base_urls if base_urls is not None else APIConfig.BASE_URLS()
        self.kill_urls = kill_urls if kill_urls is not None else APIConfig.KILL_URLS()

    def extract_requests_from_har(self, har_file_path: str, filter_duplicate_url: bool = True) -> list[dict[str, Any]]:
        """
        从HAR文件中提取请求信息
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
                query_params[param["name"]] = unquote(param["value"]) if isinstance(param["value"], str) else param["value"]

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
                        post_data[param["name"]] = unquote(param.get("value", "")) if isinstance(param.get("value"), str) else param.get("value", "")
                    post_data = self._filter_invalid_params(post_data)
                elif content_type.startswith("application/json"):
                    try:
                        post_data = json.loads(post_data_text)
                        post_data = self._filter_invalid_params(post_data)
                    except json.JSONDecodeError:
                        post_data = post_data_text
                else:
                    raise Exception(f"{full_url} 不支持的Content-Type: {content_type}, 请检查")

            # 响应内容
            response_content = None
            if response.get("content", {}).get("text"):
                response_text = response["content"]["text"]
                try:
                    response_content = json.loads(response_text)
                except json.JSONDecodeError:
                    response_content = response_text

            # 清理 URL，移除 query 参数
            clean_url = full_url
            # 如果配置了 base_urls，尝试匹配并移除前缀
            if self.base_urls:
                for base_url in self.base_urls:
                    if full_url.startswith(base_url):
                        clean_url = full_url[len(base_url) :]
                        break
            else:
                # 如果没有配置 base_urls，尝试从 headers 中获取 origin
                origin = headers.get("origin", headers.get("Origin", ""))
                if origin and full_url.startswith(origin):
                    clean_url = full_url[len(origin) :]
                    logger.debug(f"使用 origin header 作为 base URL: {origin}")

            if "?" in clean_url:
                clean_url = clean_url.split("?")[0]

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
        """
        过滤无效参数
        """
        if not isinstance(data, dict):
            return data

        filtered_data = {}
        for key, value in data.items():
            if key not in APIConfig.INVALID_PARAMS():
                filtered_data[key] = value
            else:
                logger.debug(f"过滤无效参数: {key} = {value}")

        return filtered_data

    def _filter_headers(self, headers: dict[str, str]) -> dict[str, str]:
        """
        过滤 headers，只保留配置中指定的和必要的 headers

        Args:
            headers: 原始 headers 字典

        Returns:
            Dict[str, str]: 过滤后的 headers 字典
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
        """
        打印API请求摘要信息
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
