"""URL 匹配器模块。

提供 URL 匹配、路径参数提取、URL 规范化等功能。
"""

import re
from typing import Any

from .config import APIConfig
from .logger import logger
from .utils import parse_api_file


class URLMatcher:
    """URL 匹配器类。

    提供统一的 URL 匹配、路径参数提取、URL 规范化等功能。
    支持从 Swagger 文档和配置中匹配 URL 模板。
    """

    def __init__(self, swagger_data: dict[str, Any] | None = None):
        """初始化 URL 匹配器。

        Args:
            swagger_data: Swagger 文档数据，用于 URL 模板匹配（可选）。
        """
        self.swagger_data = swagger_data
        # Swagger 路径模板匹配缓存（键为 swagger:url）
        self._swagger_match_cache: dict[str, tuple] = {}
        # URL 信息缓存（get_url_info，键为原始 url）
        self._url_info_cache: dict[str, dict[str, Any]] = {}

    @staticmethod
    def match_url_pattern(url: str, pattern: str) -> tuple[bool, dict[str, str]]:
        """匹配 URL 与路径模板，并提取路径参数。

        Args:
            url: 要匹配的 URL。
            pattern: 路径模板，如 `/user/{id}/info`。

        Returns:
            tuple[bool, dict[str, str]]: 第一个元素表示是否匹配成功，
                第二个元素是提取的路径参数字典。
        """
        url_parts = url.strip("/").split("/")
        pattern_parts = pattern.strip("/").split("/")

        if len(url_parts) != len(pattern_parts):
            return False, {}

        path_params = {}
        for url_part, pattern_part in zip(url_parts, pattern_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                path_params[pattern_part[1:-1]] = url_part
            elif url_part != pattern_part:
                return False, {}

        return True, path_params

    @staticmethod
    def extract_url_template(url: str, patterns: list[str]) -> tuple[str | None, dict[str, str]]:
        """从给定的 URL 模板列表中匹配并提取模板。

        Args:
            url: 要匹配的 URL。
            patterns: URL 模板列表。

        Returns:
            tuple[str | None, dict[str, str]]: 匹配到的模板和提取的路径参数，
                如果未匹配到则返回 (None, {})。
        """
        for pattern in patterns:
            matched, params = URLMatcher.match_url_pattern(url, pattern)
            if matched:
                return pattern, params
        return None, {}

    def match_with_swagger(self, url: str) -> tuple[str | None, dict[str, str], list[str]]:
        """使用 Swagger 文档匹配 URL 模板。

        Args:
            url: 要匹配的 URL。

        Returns:
            tuple[str | None, dict[str, str], list[str]]: 匹配到的完整路径模板、
                提取的路径参数字典、路径部分列表。如果未匹配到则返回 (None, {}, [])。
        """
        cache_key = f"swagger:{url}"
        if cache_key in self._swagger_match_cache:
            return self._swagger_match_cache[cache_key]

        if not self.swagger_data or "paths" not in self.swagger_data:
            return None, {}, []

        base_path = self.swagger_data.get("basePath", "")
        search_url = self.remove_base_path(url, base_path)

        paths = self.swagger_data["paths"]

        # 文档 paths 的键可能已包含 basePath（springfox 常见：basePath=/admin 且键为 /admin/xxx），
        # 也可能不含；两种形态都要尝试，否则"键含 basePath"的文档永远匹配不到模板。
        url_variants = [search_url] if search_url == url else [search_url, url]

        # 先看是否存在“具体路径精确命中”：/mobile/returnOrder/page 这类实际存在的路径
        # 不应被 /mobile/returnOrder/{id} 这类通配模板抢走（否则会生成错误 URL/函数名）
        for variant in url_variants:
            if variant in paths:
                full_path = self._ensure_base_path(variant, base_path)
                result = (full_path, {}, self._extract_path_parts(variant, variant))
                self._swagger_match_cache[cache_key] = result
                return result

        # 获取所有带参数的路径模板
        param_paths = [path for path in paths.keys() if "{" in path and "}" in path]

        for swagger_path in param_paths:
            for variant in url_variants:
                matched, path_params = self.match_url_pattern(variant, swagger_path)
                if matched:
                    full_path = self._ensure_base_path(swagger_path, base_path)
                    result_parts = self._extract_path_parts(variant, swagger_path)
                    result = (full_path, path_params, result_parts)
                    self._swagger_match_cache[cache_key] = result
                    logger.debug(f"从Swagger文档中匹配到路径模板: {swagger_path}")
                    return result

        return None, {}, []

    @staticmethod
    def normalize_url(url: str, base_urls: list[str] | None = None) -> str:
        """规范化 URL。

        移除基础 URL 前缀和查询参数部分，确保 URL 以 `/` 开头。

        Args:
            url: 要规范化的 URL。
            base_urls: 基础 URL 列表，用于移除前缀（可选）。

        Returns:
            str: 规范化后的 URL。
        """
        clean_url = url

        if base_urls:
            for base_url in base_urls:
                if clean_url.startswith(base_url):
                    clean_url = clean_url[len(base_url) :]
                    break

        if "?" in clean_url:
            clean_url = clean_url.split("?")[0]

        # 绝对 URL（含 scheme://host）未匹配任何 base_url 时，只保留 path+query 部分，
        # 避免拼出 "/https://host/..." 这样的垃圾相对路径
        if not clean_url.startswith("/") and "://" in clean_url:
            scheme_sep = clean_url.index("://")
            rest = clean_url[scheme_sep + 3 :]
            slash = rest.find("/")
            clean_url = rest[slash:] if slash != -1 else "/"

        if not clean_url.startswith("/"):
            clean_url = "/" + clean_url

        return clean_url

    @staticmethod
    def generate_function_name(url: str | None) -> str:
        """从 URL 生成函数名。

        将 URL 中的非字母数字字符替换为下划线，并去除前导下划线。

        Args:
            url: URL 字符串，为 None 时返回 "unknown"。

        Returns:
            str: 生成的函数名。
        """
        if url is None:
            return "unknown"
        clean_url = re.sub(r"[{}]", "", url)
        return re.sub(r"[^a-zA-Z0-9_]", "_", clean_url).lstrip("_")

    def get_url_info(self, url: str) -> dict[str, Any]:
        """获取 URL 的完整信息。

        Args:
            url: 要分析的 URL。

        Returns:
            dict[str, Any]: 包含以下字段的字典：
                - original_url: 原始 URL
                - pattern: 匹配到的路径模板
                - path_params: 提取的路径参数
                - function_name: 生成的函数名
                - has_path_params: 是否包含路径参数
        """
        if url in self._url_info_cache:
            return self._url_info_cache[url].copy()

        # 尝试从配置匹配（无论是否含数字：非数字路径参数值也能命中模板）
        path_urls = APIConfig.PATH_URLS()
        pattern, params = self.extract_url_template(url, path_urls)
        if pattern:
            return self._finalize(url, pattern, params)

        # 尝试从Swagger匹配（仅在已加载 swagger_data 时执行；命中即用）
        if self.swagger_data:
            pattern, params, _ = self.match_with_swagger(url)
            if pattern:
                return self._finalize(url, pattern, params)

        # 兜底：无模板命中，原样作为 pattern
        return self._finalize(url, url, {})

    def _finalize(self, url: str, pattern: str, params: dict[str, Any]) -> dict[str, Any]:
        """填充 URL 信息结果、写缓存并返回拷贝。"""
        result = {
            "original_url": url,
            "pattern": pattern,
            "path_params": params,
            "function_name": self.generate_function_name(pattern),
            "has_path_params": bool(params),
        }
        self._url_info_cache[url] = result.copy()
        return result.copy()

    @staticmethod
    def find_matching_api_file(
        request_url: str, api_files: list[str], request_url_map: dict[str, str] | None = None
    ) -> str | None:
        """查找匹配的 API 文件。

        Args:
            request_url: 请求的 URL。
            api_files: API 文件路径列表。
            request_url_map: URL 映射字典，用于转换请求 URL（可选）。

        Returns:
            str | None: 匹配到的 API 文件路径，如果未找到则返回 None。
        """
        transformed_url = request_url_map.get(request_url, request_url) if request_url_map else request_url

        for api_file in api_files:
            try:
                result = parse_api_file(api_file)
            except ValueError:
                # 候选文件缺元数据时无法参与匹配：跳过，交由后续真正读取目标文件时再报错
                continue
            file_url = result.url
            if not file_url:
                continue

            # 直接匹配
            if request_url == file_url or transformed_url == file_url:
                return api_file

            # 双向模式匹配
            matched, _ = URLMatcher.match_url_pattern(request_url, file_url)
            if matched:
                return api_file

            matched, _ = URLMatcher.match_url_pattern(file_url, request_url)
            if matched:
                return api_file

            # URL 标准化匹配
            if URLMatcher.normalize_url(file_url) == URLMatcher.normalize_url(request_url):
                return api_file

        return None

    @staticmethod
    def remove_base_path(url: str, base_path: str) -> str:
        """移除 basePath 前缀。

        Args:
            url: 要处理的 URL。
            base_path: 要移除的基础路径前缀。

        Returns:
            str: 移除前缀后的 URL。
        """
        if not base_path or base_path == "/":
            return url
        if url.startswith(base_path):
            result = url[len(base_path) :]
            return "/" + result if not result.startswith("/") else result
        return url

    @staticmethod
    def _ensure_base_path(path: str, base_path: str) -> str:
        """确保路径带 basePath 前缀（已带则不重复添加）。

        文档 paths 的键可能已包含 basePath，此时不能再拼一次前缀。

        Args:
            path: 路径（可能已含 basePath）。
            base_path: 文档的 basePath。

        Returns:
            str: 带 basePath 前缀的路径。
        """
        if not base_path or base_path == "/":
            return path
        prefix = base_path.rstrip("/")
        if path == prefix or path.startswith(prefix + "/"):
            return path
        return prefix + "/" + path.lstrip("/")

    @staticmethod
    def _extract_path_parts(url: str, pattern: str) -> list[str]:
        """提取路径部分。

        将 URL 和模板进行匹配，提取路径的各个部分。
        如果模板中包含路径参数（如 {id}），则提取参数名；否则提取 URL 中的实际值。

        Args:
            url: URL。
            pattern: 路径模板。

        Returns:
            list[str]: 路径部分列表。
        """
        url_parts = url.strip("/").split("/")
        pattern_parts = pattern.strip("/").split("/")

        result_parts = []
        for url_part, pattern_part in zip(url_parts, pattern_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                result_parts.append(pattern_part[1:-1])
            else:
                result_parts.append(url_part)

        return result_parts
