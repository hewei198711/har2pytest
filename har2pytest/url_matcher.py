import re
from functools import lru_cache
from typing import Any, Optional

from .config import APIConfig
from .logger import logger


class URLMatcher:
    """
    URL匹配器类，提供统一的URL匹配、路径参数提取、URL规范化等功能
    """
    
    def __init__(self, swagger_data: dict[str, Any] | None = None):
        """初始化URL匹配器"""
        self.swagger_data = swagger_data
        self._path_params_cache = {}
        # 缓存匹配结果
        self._match_cache = {}
    
    def _has_numeric_path_segment(self, url: str) -> bool:
        """检查URL中是否包含数字路径参数"""
        return bool(re.search(r'\/(\d+)\/', url))
    
    @staticmethod
    def match_url_pattern(url: str, pattern: str) -> tuple[bool, dict[str, str]]:
        """匹配URL与路径模板，并提取路径参数"""
        url_parts = url.strip('/').split('/')
        pattern_parts = pattern.strip('/').split('/')
        
        if len(url_parts) != len(pattern_parts):
            return False, {}
        
        path_params = {}
        for url_part, pattern_part in zip(url_parts, pattern_parts):
            if pattern_part.startswith('{') and pattern_part.endswith('}'):
                path_params[pattern_part[1:-1]] = url_part
            elif url_part != pattern_part:
                return False, {}
        
        return True, path_params
    
    @staticmethod
    def extract_url_template(url: str, patterns: list[str]) -> tuple[Optional[str], dict[str, str]]:
        """从给定的URL模板列表中匹配并提取模板"""
        for pattern in patterns:
            matched, params = URLMatcher.match_url_pattern(url, pattern)
            if matched:
                return pattern, params
        return None, {}
    
    def match_with_swagger(self, url: str) -> tuple[Optional[str], dict[str, str], list[str]]:
        """使用Swagger文档匹配URL模板"""
        cache_key = f"swagger:{url}"
        if cache_key in self._match_cache:
            return self._match_cache[cache_key]
        
        if not self.swagger_data or "paths" not in self.swagger_data:
            return None, {}, []
        
        base_path = self.swagger_data.get("basePath", "")
        search_url = self._remove_base_path(url, base_path)
        
        # 获取所有带参数的路径模板
        paths = self.swagger_data["paths"]
        param_paths = [path for path in paths.keys() if "{" in path and "}" in path]
        
        for swagger_path in param_paths:
            matched, path_params = self.match_url_pattern(search_url, swagger_path)
            if matched:
                full_path = self._add_base_path(swagger_path, base_path)
                result_parts = self._extract_path_parts(search_url, swagger_path)
                result = (full_path, path_params, result_parts)
                self._match_cache[cache_key] = result
                logger.debug(f"从Swagger文档中匹配到路径模板: {swagger_path}")
                return result
        
        return None, {}, []
    
    @staticmethod
    def normalize_url(url: str, base_urls: list[str] | None = None) -> str:
        """规范化URL"""
        clean_url = url
        
        if base_urls:
            for base_url in base_urls:
                if clean_url.startswith(base_url):
                    clean_url = clean_url[len(base_url):]
                    break
        
        if '?' in clean_url:
            clean_url = clean_url.split('?')[0]
        
        if not clean_url.startswith('/'):
            clean_url = '/' + clean_url
        
        return clean_url
    
    @staticmethod
    def generate_function_name(url: str | None) -> str:
        """从URL生成函数名"""
        if url is None:
            return "_unknown"
        clean_url = re.sub(r'[{}]', '', url)
        return re.sub(r'[^a-zA-Z0-9_]', '_', clean_url)
    
    def get_url_info(self, url: str) -> dict[str, Any]:
        """获取URL的完整信息"""
        cache_key = f"info:{url}"
        if cache_key in self._match_cache:
            return self._match_cache[cache_key].copy()
        
        result = {
            "original_url": url,
            "pattern": None,
            "path_params": {},
            "function_name": None,
            "has_path_params": False
        }
        
        has_braces = '{' in url and '}' in url
        has_numeric = self._has_numeric_path_segment(url)
        
        if has_numeric or has_braces:
            # 尝试从配置匹配
            path_urls = APIConfig.PATH_URLS()
            pattern, params = self.extract_url_template(url, path_urls)
            if pattern:
                result["pattern"] = pattern
                result["path_params"] = params
                result["has_path_params"] = bool(params)
                result["function_name"] = self.generate_function_name(pattern)
                self._match_cache[cache_key] = result.copy()
                return result
            
            # 尝试从Swagger匹配
            if self.swagger_data:
                pattern, params, _ = self.match_with_swagger(url)
                if pattern:
                    result["pattern"] = pattern
                    result["path_params"] = params
                    result["has_path_params"] = bool(params)
                    result["function_name"] = self.generate_function_name(pattern)
                    self._match_cache[cache_key] = result.copy()
                    return result
        
        result["pattern"] = url
        result["function_name"] = self.generate_function_name(url)
        self._match_cache[cache_key] = result.copy()
        return result
    
    @staticmethod
    def find_matching_api_file(
        request_url: str, 
        api_files: list[str], 
        request_url_map: dict[str, str] | None = None
    ) -> Optional[str]:
        """查找匹配的API文件"""
        transformed_url = request_url_map.get(request_url, request_url) if request_url_map else request_url
        
        for api_file in api_files:
            from .utils import parse_api_file
            result = parse_api_file(api_file)
            file_url = result.get("url")
            if not file_url:
                continue
            
            if request_url == file_url or transformed_url == file_url:
                return api_file
            
            matched, _ = URLMatcher.match_url_pattern(request_url, file_url)
            if matched:
                return api_file
        
        return None
    
    @staticmethod
    def _remove_base_path(url: str, base_path: str) -> str:
        """移除basePath前缀"""
        if not base_path or base_path == "/":
            return url
        if url.startswith(base_path):
            result = url[len(base_path):]
            return '/' + result if not result.startswith('/') else result
        return url
    
    @staticmethod
    def _add_base_path(path: str, base_path: str) -> str:
        """添加basePath前缀"""
        if not base_path or base_path == "/":
            return path
        return base_path.rstrip('/') + '/' + path.lstrip('/')
    
    @staticmethod
    def _extract_path_parts(url: str, pattern: str) -> list[str]:
        """提取路径部分"""
        url_parts = url.strip('/').split('/')
        pattern_parts = pattern.strip('/').split('/')
        
        result_parts = []
        for url_part, pattern_part in zip(url_parts, pattern_parts):
            if pattern_part.startswith('{') and pattern_part.endswith('}'):
                result_parts.append(pattern_part[1:-1])
            else:
                result_parts.append(url_part)
        
        return result_parts