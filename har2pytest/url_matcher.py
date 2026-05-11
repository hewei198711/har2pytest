import re
from typing import Any

from .config import APIConfig
from .logger import logger
from .utils import get_url_from_api_file


class URLMatcher:
    """
    URL匹配器类，提供统一的URL匹配、路径参数提取、URL规范化等功能
    """
    
    def __init__(self, swagger_data: dict[str, Any] | None = None):
        """
        初始化URL匹配器
        
        Args:
            swagger_data: Swagger文档数据，可选
        """
        self.swagger_data = swagger_data
        self._path_params_cache = {}
    
    @staticmethod
    def match_url_pattern(url: str, pattern: str) -> tuple[bool, dict[str, str]]:
        """
        匹配URL与路径模板，并提取路径参数
        
        Args:
            url: 实际URL，如 /user/123/info
            pattern: 路径模板，如 /user/{userId}/info
            
        Returns:
            Tuple[bool, Dict[str, str]]: (是否匹配, 路径参数字典)
            
        Example:
            >>> URLMatcher.match_url_pattern("/user/123/info", "/user/{userId}/info")
            (True, {"userId": "123"})
            >>> URLMatcher.match_url_pattern("/user/123/info", "/user/{userId}/profile")
            (False, {})
        """
        # 标准化URL和pattern，移除开头和结尾的斜杠
        url_parts = url.strip('/').split('/')
        pattern_parts = pattern.strip('/').split('/')
        
        if len(url_parts) != len(pattern_parts):
            return False, {}
        
        path_params = {}
        for url_part, pattern_part in zip(url_parts, pattern_parts):
            # 检查是否为路径参数（{param}格式）
            if pattern_part.startswith('{') and pattern_part.endswith('}'):
                param_name = pattern_part[1:-1]
                path_params[param_name] = url_part
            elif url_part != pattern_part:
                return False, {}
        
        return True, path_params
    
    @staticmethod
    def extract_url_template(url: str, patterns: list[str]) -> tuple[str | None, dict[str, str]]:
        """
        从给定的URL模板列表中匹配并提取模板
        
        Args:
            url: 实际URL
            patterns: URL模板列表，如 ["/user/{userId}/info", "/product/{productId}"]
            
        Returns:
            Tuple[Optional[str], Dict[str, str]]: (匹配的模板, 路径参数)
            
        Example:
            >>> URLMatcher.extract_url_template("/user/123/info", ["/user/{userId}/info"])
            ("/user/{userId}/info", {"userId": "123"})
        """
        for pattern in patterns:
            matched, params = URLMatcher.match_url_pattern(url, pattern)
            if matched:
                return pattern, params
        return None, {}
    
    def match_with_swagger(self, url: str) -> tuple[str | None, dict[str, str], list[str]]:
        """
        使用Swagger文档匹配URL模板
        
        Args:
            url: 实际URL
            
        Returns:
            Tuple[Optional[str], Dict[str, str], List[str]]: 
                (URL模板, 路径参数, 路径部分列表)
        """
        if not self.swagger_data or "paths" not in self.swagger_data:
            return None, {}, []
        
        # 获取Swagger文档的basePath并处理
        base_path = self.swagger_data.get("basePath", "")
        search_url = self.remove_base_path(url, base_path)
        
        # 获取所有带参数的路径模板
        paths = self.swagger_data["paths"]
        param_paths = [path for path in paths.keys() if "{" in path and "}" in path]
        
        # 匹配路径模板
        for swagger_path in param_paths:
            matched, path_params = self.match_url_pattern(search_url, swagger_path)
            if matched:
                # 提取路径部分用于函数名生成
                result_parts = self._extract_path_parts(search_url, swagger_path)
                
                # 还原完整URL（包含basePath）
                full_path = self._add_base_path(swagger_path, base_path)
                
                logger.debug(f"从Swagger文档中匹配到路径模板: {swagger_path}")
                return full_path, path_params, result_parts
        
        return None, {}, []
    
    @staticmethod
    def normalize_url(url: str, base_urls: list[str] | None = None) -> str:
        """
        规范化URL，移除base前缀和查询参数
        
        Args:
            url: 原始URL
            base_urls: 需要移除的base URL列表
            
        Returns:
            str: 规范化后的URL
        """
        clean_url = url
        
        # 移除base URL前缀
        if base_urls:
            for base_url in base_urls:
                if clean_url.startswith(base_url):
                    clean_url = clean_url[len(base_url):]
                    break
        
        # 移除查询参数
        if '?' in clean_url:
            clean_url = clean_url.split('?')[0]
        
        # 确保以/开头
        if not clean_url.startswith('/'):
            clean_url = '/' + clean_url
        
        return clean_url
    
    @staticmethod
    def extract_path_params(url: str) -> dict[str, str]:
        """
        从URL中提取路径参数（当URL已经是模板格式时）
        
        Args:
            url: 包含路径参数的URL，如 /user/{userId}/info
            
        Returns:
            Dict[str, str]: 路径参数名称到空值的映射
            
        Example:
            >>> URLMatcher.extract_path_params("/user/{userId}/info")
            {"userId": ""}
        """
        path_params = {}
        parts = url.strip('/').split('/')
        
        for part in parts:
            if part.startswith('{') and part.endswith('}'):
                param_name = part[1:-1]
                path_params[param_name] = ""
        
        return path_params
    
    @staticmethod
    def generate_function_name(url: str | None) -> str:
        """
        从URL生成函数名
        
        Args:
            url: URL路径
            
        Returns:
            str: 生成的函数名
            
        Example:
            >>> URLMatcher.generate_function_name("/mobile/trade/orderCommit")
            "_mobile_trade_orderCommit"
            >>> URLMatcher.generate_function_name("/user/{userId}/info")
            "_user_userId_info"
        """
        if url is None:
            return "_unknown"
        
        # 移除花括号
        clean_url = re.sub(r'[{}]', '', url)
        # 替换非字母数字下划线为下划线
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', clean_url)
        # 移除开头的下划线（如果有）
        clean_name = clean_name.lstrip('_')
        # 添加前缀下划线
        return f"_{clean_name}"
    
    def get_url_info(self, url: str) -> dict[str, Any]:
        """
        获取URL的完整信息（匹配结果、路径参数、函数名等）
        
        Args:
            url: 原始URL
            
        Returns:
            Dict[str, Any]: 包含url, pattern, path_params, function_name等信息
        """
        # 初始化结果
        result = {
            "original_url": url,
            "normalized_url": url,
            "pattern": None,
            "path_params": {},
            "function_name": None,
            "has_path_params": False
        }
        
        # 1. 检查URL是否已经是模板格式
        if '{' in url and '}' in url:
            result["pattern"] = url
            result["path_params"] = self.extract_path_params(url)
            result["has_path_params"] = True
            result["function_name"] = self.generate_function_name(url)
            return result
        
        # 2. 尝试从配置的PATH_URLS匹配
        path_urls = APIConfig.PATH_URLS()
        pattern, params = self.extract_url_template(url, path_urls)
        if pattern:
            result["pattern"] = pattern
            result["path_params"] = params
            result["has_path_params"] = bool(params)
            result["function_name"] = self.generate_function_name(pattern)
            return result
        
        # 3. 尝试从Swagger文档匹配
        if self.swagger_data:
            pattern, params, _ = self.match_with_swagger(url)
            if pattern:
                result["pattern"] = pattern
                result["path_params"] = params
                result["has_path_params"] = bool(params)
                result["function_name"] = self.generate_function_name(pattern)
                return result
        
        # 4. 没有匹配到模板，使用原始URL
        result["normalized_url"] = url
        result["pattern"] = url  # 设置 pattern 为原始URL
        result["function_name"] = self.generate_function_name(url)
        return result
    
    @staticmethod
    def remove_base_path(url: str, base_path: str) -> str:
        """
        移除basePath前缀
        
        Args:
            url: URL路径
            base_path: basePath前缀
            
        Returns:
            str: 移除前缀后的路径
            
        Example:
            >>> URLMatcher.remove_base_path("/appStore/storage/upload", "/appStore")
            "/storage/upload"
        """
        if not base_path or base_path == "/":
            return url
        
        if url.startswith(base_path):
            result = url[len(base_path):]
            if not result.startswith('/'):
                result = '/' + result
            return result
        return url
    
    @staticmethod
    def _add_base_path(path: str, base_path: str) -> str:
        """添加basePath前缀"""
        if not base_path or base_path == "/":
            return path
        
        return base_path.rstrip('/') + '/' + path.lstrip('/')
    
    @staticmethod
    def _extract_path_parts(url: str, pattern: str) -> list[str]:
        """提取路径部分（用于函数名生成）"""
        url_parts = url.strip('/').split('/')
        pattern_parts = pattern.strip('/').split('/')
        
        result_parts = []
        for url_part, pattern_part in zip(url_parts, pattern_parts):
            if pattern_part.startswith('{') and pattern_part.endswith('}'):
                param_name = pattern_part[1:-1]
                result_parts.append(param_name)
            else:
                result_parts.append(url_part)
        
        return result_parts
    
    @staticmethod
    def find_matching_api_file(
        request_url: str, 
        api_files: list[str], 
        request_url_map: dict[str, str] | None = None
    ) -> str | None:
        """
        查找匹配的API文件
        
        Args:
            request_url: 请求URL
            api_files: API文件路径列表
            request_url_map: 请求URL到转换后URL的映射
            
        Returns:
            Optional[str]: 匹配的API文件路径
        """
        
        transformed_url = request_url_map.get(request_url, request_url) if request_url_map else request_url
        
        for api_file in api_files:
            result = get_url_from_api_file(api_file)
            if not result:
                continue
                
            _, file_url = result
            
            # 1. 直接匹配
            if request_url == file_url:
                return api_file
            
            # 2. 转换后匹配
            if transformed_url == file_url:
                return api_file
            
            # 3. 使用URLMatcher进行模板匹配
            matched, _ = URLMatcher.match_url_pattern(request_url, file_url)
            if matched:
                return api_file
        
        return None
