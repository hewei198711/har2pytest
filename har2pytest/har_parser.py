"""HAR 文件解析器模块。

提供从 HAR（HTTP Archive）文件中提取和解析 API 请求信息的功能。
"""

import json
from typing import Any
from urllib.parse import parse_qs, unquote

from .config import APIConfig
from .logger import logger
from .models import ParsedRequestInfo
from .url_matcher import URLMatcher


class HARParser:
    """HAR 文件解析器类。

    用于从 HAR 文件中提取 API 请求信息，支持过滤无效参数、重复 URL 等功能。
    """

    def __init__(self, base_urls: list[str] | None = None, kill_urls: list[str] | None = None):
        """初始化 HAR 解析器。

        Args:
            base_urls: 基础 URL 列表，用于从完整 URL 中提取相对路径（可选）。
            kill_urls: 需要过滤的 URL 关键字列表（可选）。
        """
        self.base_urls = base_urls if base_urls is not None else APIConfig.BASE_URLS()
        self.kill_urls = kill_urls if kill_urls is not None else APIConfig.KILL_URLS()

    def extract_requests_from_har(self, har_file_path: str, filter_duplicate_url: bool = True) -> list[ParsedRequestInfo]:
        """从 HAR 文件中提取请求信息。

        Args:
            har_file_path: HAR 文件路径。
            filter_duplicate_url: 是否过滤重复的 URL（默认 True）。

        Returns:
            list[ParsedRequestInfo]: 解析后的请求信息列表，包含请求头、参数、响应等字段。
        """
        entries = self._load_entries(har_file_path)
        if not entries:
            return []

        logger.info(f"开始解析HAR文件，共 {len(entries)} 个请求记录")

        requests: list[ParsedRequestInfo] = []
        seen_urls: set[str] = set()
        for entry in entries:
            request_info = self._parse_entry(entry)
            if request_info is None:
                continue
            # 过滤重复 URL（同 method+clean_url 只保留第一个）
            if filter_duplicate_url:
                url_key = f"{request_info.method}:{request_info.url}"
                if url_key in seen_urls:
                    continue
                seen_urls.add(url_key)
            requests.append(request_info)

        logger.info(f"解析完成，提取到 {len(requests)} 个有效的API请求")
        return requests

    @staticmethod
    def _load_entries(har_file_path: str) -> list[dict[str, Any]]:
        """读取 HAR 文件并返回 log.entries（文件缺失/损坏/无记录时返回空列表）。"""
        try:
            with open(har_file_path, encoding="utf-8") as f:
                har_data = json.load(f)
        except FileNotFoundError:
            logger.warning(f"HAR文件不存在: {har_file_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"HAR文件JSON格式错误: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"读取HAR文件失败: {str(e)}")
            return []

        entries = har_data.get("log", {}).get("entries", [])
        if not entries:
            logger.info("HAR文件中没有找到请求记录")
        return entries

    @staticmethod
    def _name_value_to_dict(pairs: list[dict[str, Any]], url_decode: bool = False) -> dict[str, str]:
        """把 HAR 的 {name, value} 键值对列表转成字典。

        Args:
            pairs: 键值对列表，如 headers / queryString / postData.params。
            url_decode: 是否对字符串值做 URL 解码（queryString/表单参数为 True）。
        """
        result = {}
        for item in pairs:
            value = item.get("value", "")
            name = item.get("name", "")
            if url_decode and isinstance(value, str):
                value = unquote(value)
            result[name] = value
        return result

    def _parse_entry(self, entry: dict[str, Any]) -> ParsedRequestInfo | None:
        """解析单条 HAR entry；应跳过的请求返回 None。"""
        # 跳过非 XHR 请求（图片、CSS、JS 等），兼容无 _resourceType 字段的 HAR
        resource_type = entry.get("_resourceType", "xhr")
        if resource_type not in ("xhr", "fetch"):
            return None

        request = entry.get("request", {})
        response = entry.get("response", {})
        full_url = request.get("url", "")

        # 过滤 URL（含 kill 关键字）
        matched_kill = next((k for k in self.kill_urls if k in full_url), None)
        if matched_kill is not None:
            logger.debug(f"过滤URL: {full_url} (包含关键字: {matched_kill})")
            return None

        headers = self._name_value_to_dict(request.get("headers", []))
        # 保存 origin 用于 URL 规范化（大小写不敏感查找，不出现在最终文件中）
        raw_origin = next((v for k, v in headers.items() if k.lower() == "origin"), "")

        # 过滤 headers
        headers = self._filter_headers(headers)

        # query 参数：解码并过滤无效参数
        query_params = self._name_value_to_dict(request.get("queryString", []), url_decode=True)
        query_params = self._filter_invalid_params(query_params)

        # POST 数据：按 Content-Type 分支解析，过滤无效参数和空值
        post_data: Any = None
        content_type = ""
        post_data_text = ""
        if request.get("postData"):
            post_data_text = request["postData"].get("text", "")
            content_type = request["postData"].get("mimeType", "")

            if content_type.startswith("multipart/form-data"):
                params = request["postData"].get("params", [])
                post_data = self._name_value_to_dict(params, url_decode=True)
                post_data = self._filter_invalid_params(post_data)
            elif content_type.startswith("application/json"):
                post_data = self._filter_invalid_params(self._try_json_loads(post_data_text))
            elif content_type.startswith("application/x-www-form-urlencoded"):
                if post_data_text:
                    parsed = parse_qs(post_data_text)
                    # parse_qs 返回 {key: [value, ...]}，取每个 key 的最后一个值
                    post_data = {k: v[-1] for k, v in parsed.items()}
                else:
                    # 部分 HAR 只提供结构化 params（无 text），回退避免丢参数
                    post_data = self._name_value_to_dict(request["postData"].get("params", []), url_decode=True)
                post_data = self._filter_invalid_params(post_data)
            else:
                logger.warning(f"不支持的Content-Type: {content_type}, URL: {full_url}，跳过该请求")
                return None

        # 响应内容
        response_content: Any = None
        response_text = response.get("content", {}).get("text")
        if response_text:
            response_content = self._try_json_loads(response_text)

        return ParsedRequestInfo(
            method=request.get("method", "GET"),
            url=self._normalize_url(full_url, raw_origin),
            full_url=full_url,
            headers=headers,
            content_type=content_type,
            cookies=self._name_value_to_dict(request.get("cookies", [])),
            query_params=query_params,
            post_data=post_data,
            response_status=response.get("status", 0),
            response_content=response_content,
            response_time=entry.get("time", 0),
            server_ip=entry.get("serverIPAddress", ""),
        )

    def _normalize_url(self, full_url: str, origin: str) -> str:
        """清理 URL：优先移除 base_urls 前缀，其次 origin 前缀；无则仅去 query 并保证以 / 开头。"""
        if self.base_urls:
            return URLMatcher.normalize_url(full_url, self.base_urls)
        if origin and full_url.startswith(origin):
            logger.debug(f"使用 origin header 作为 base URL: {origin}")
            return URLMatcher.normalize_url(full_url, [origin])
        # 无 base_urls 也无 origin，仍需去掉查询参数
        return URLMatcher.normalize_url(full_url)

    @staticmethod
    def _try_json_loads(text: str) -> Any:
        """尝试按 JSON 解析；解析失败时原样返回文本。"""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text

    def _filter_invalid_params(self, data: Any, invalid_params: set[str] | None = None) -> Any:
        """递归过滤无效参数。

        对 dict 逐层过滤 key（含嵌套 dict/list 内的字段），
        对 list 递归每个元素，其余标量原样返回。

        Args:
            data: 原始参数（dict、list 或其他类型）。
            invalid_params: 需要过滤的参数名集合（缺省时从配置读取）。

        Returns:
            过滤后的数据，保持与输入相同的结构化类型。
        """
        if invalid_params is None:
            invalid_params = APIConfig.INVALID_PARAMS() or set()

        if isinstance(data, dict):
            filtered_data: dict[str, Any] = {}
            for key, value in data.items():
                if key in invalid_params:
                    logger.debug(f"过滤无效参数: {key} = {value}")
                else:
                    filtered_data[key] = self._filter_invalid_params(value, invalid_params)
            return filtered_data

        if isinstance(data, list):
            return [self._filter_invalid_params(item, invalid_params) for item in data]

        # 标量（字符串/数字/布尔/None）原样保留
        return data

    def _filter_headers(self, headers: dict[str, str]) -> dict[str, str]:
        """过滤 headers，只保留配置指定的与下游必需的头（头名大小写不敏感）。

        Args:
            headers: 原始 headers 字典。

        Returns:
            dict[str, str]: 过滤后的 headers 字典。
        """
        include = APIConfig.HEADERS_TO_INCLUDE()
        # content-type/content-length 是请求体元数据，下游据此判定 json/multipart/空 body，
        # 即使未配置在白名单中也强制保留；REQUIRED_HEADERS 的键同样确保不被滤掉
        keep = {"content-type", "content-length"}
        for cfg in (include, APIConfig.REQUIRED_HEADERS()):
            if cfg:
                keys = cfg.keys() if isinstance(cfg, dict) else cfg
                keep.update(k.lower() for k in keys)
        return {k: v for k, v in headers.items() if k.lower() in keep}

    def print_api_summary(self, har_file_path: str) -> None:
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

        success_count = sum(1 for req in requests if 200 <= req.response_status < 300)
        error_count = len(requests) - success_count
        avg_time = sum(req.response_time for req in requests) / len(requests)

        for i, req in enumerate(requests, 1):
            status = req.response_status
            time = req.response_time
            url = req.url[:80]
            method = req.method

            logger.info(f"{i:2d}. {method:6s} {status:3d} {time:8.2f}ms {url}")

        logger.info("-" * 80)
        logger.info(f"统计: 成功 {success_count} 个, 失败 {error_count} 个, 平均响应时间 {avg_time:.2f}ms")
