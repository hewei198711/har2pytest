import re
from typing import Optional, Tuple, Dict, Any

from .config import APIConfig
from .logger import logger
from .utils import handle_base_path


def get_url_from_api_file(filepath: str) -> tuple | None:
    """
    从API文件中提取URL路径

    从API文件的函数描述中提取接口名称和URL路径，优先从函数描述的最后一行获取URL

    Args:
        filepath: API文件路径，如 "api/mall_mobile_application/_mobile_trade_orderCommit.py"

    Returns:
        Optional[tuple]: 如果成功提取返回(api_name, url)元组，否则返回None
            - api_name: 接口名称，如 "提交订单"
            - url: URL路径，如 "/mobile/trade/orderCommit"

    Example:
        result = get_url_from_api_file("api/mall_mobile_application/_mobile_trade_orderCommit.py")
        # 返回 ("提交订单", "/mobile/trade/orderCommit")
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # 先尝试从函数文档字符串中提取
        pattern = r'def\s+\w+\s*\([^)]*\):\s*"""\s*(.*?)\s*"""'
        matches = re.findall(pattern, content, re.DOTALL)

        if matches:
            doc_content = matches[0]
            lines = [line.strip() for line in doc_content.split("\n") if line.strip()]
            if len(lines) >= 2:
                api_name = lines[0]
                # 从第二行开始查找第一个以 / 开头的行作为 URL
                for line in lines[1:]:
                    if line.startswith("/"):
                        return api_name, line

        # 如果从文档字符串中提取失败，尝试从整个文件内容中提取URL
        url_pattern = r"https?://[^\s]+"
        url_matches = re.findall(url_pattern, content)
        if url_matches:
            return "", url_matches[0]

    except Exception as e:
        logger.error(f"读取文件 {filepath} 失败: {str(e)}")

    return None


def match_url_pattern(url: str, pattern: str) -> Tuple[bool, Dict[str, str]]:
    """
    匹配URL与路径模板，并提取路径参数

    Args:
        url: 实际URL，如 /user/123/info
        pattern: 路径模板，如 /user/{userId}/info

    Returns:
        Tuple[bool, Dict[str, str]]: (是否匹配, 路径参数字典)
            - 如果匹配成功，返回 (True, {"userId": "123"})
            - 如果匹配失败，返回 (False, {})

    Example:
        >>> match_url_pattern("/user/123/info", "/user/{userId}/info")
        (True, {"userId": "123"})
        >>> match_url_pattern("/user/123/info", "/user/{userId}/profile")
        (False, {})
    """
    url_parts = url.lstrip("/").split("/")
    pattern_parts = pattern.lstrip("/").split("/")

    if len(url_parts) != len(pattern_parts):
        return False, {}

    path_params = {}
    for url_part, pattern_part in zip(url_parts, pattern_parts):
        if pattern_part.startswith("{") and pattern_part.endswith("}"):
            param_name = pattern_part[1:-1]
            path_params[param_name] = url_part
        else:
            if url_part != pattern_part:
                return False, {}

    return True, path_params


def match_path_template(url: str, swagger_data: dict[str, Any] = None) -> tuple:
    """
    匹配路径模板

    匹配URL与APIConfig.PATH_URLS中的路径模板，提取路径参数
    如果提供了Swagger文档数据，会尝试从中匹配带{}的路径模板
    如果没有匹配到模板，直接返回原始URL

    Args:
        url: 原始接口URL，如 /mobile/trade/orderCommit 或 /user/123/info
        swagger_data: Swagger文档数据，可选

    Returns:
        tuple: (url_pattern, path_params, result_parts)
            - url_pattern: 匹配的路径模板，如 /user/{userId}/info
            - path_params: 路径参数字典，如 {"userId": "123"}
            - result_parts: 路径部分列表，用于生成函数名

    Example:
        url = "/user/123/info"
        pattern, params, parts = match_path_template(url, swagger_data)
        # 如果Swagger文档中有 /user/{userId}/info 路径，则返回 ("/user/{userId}/info", {"userId": "123"}, ["user", "userId", "info"])
        # 否则返回 ("/user/123/info", {}, ["user", "123", "info"])
    """
    url_parts = url.lstrip("/").split("/")

    # 如果URL已经是模板格式（包含 {param}），直接提取路径参数
    if "{" in url and "}" in url:
        path_params = {}
        result_parts = []
        for part in url_parts:
            if part.startswith("{") and part.endswith("}"):
                param_name = part[1:-1]
                result_parts.append(param_name)
                path_params[param_name] = ""
            else:
                result_parts.append(part)
        return url, path_params, result_parts

    # 先尝试从配置的PATH_URLS中匹配
    for path_pattern in APIConfig.PATH_URLS():
        matched, path_params = match_url_pattern(url, path_pattern)
        if matched:
            pattern_parts = path_pattern.lstrip("/").split("/")
            result_parts = []
            for url_part, pattern_part in zip(url_parts, pattern_parts):
                if pattern_part.startswith("{") and pattern_part.endswith("}"):
                    param_name = pattern_part[1:-1]
                    result_parts.append(param_name)
                else:
                    result_parts.append(url_part)
            return path_pattern, path_params, result_parts

    # 检查URL中是否有数字
    has_numeric = any(part.isdigit() for part in url_parts)
    logger.info(f"检查URL: {url}, 是否包含数字: {has_numeric}")

    # 如果有数字且提供了Swagger文档，尝试从Swagger文档中匹配路径模板
    if has_numeric and swagger_data and "paths" in swagger_data:
        paths = swagger_data["paths"]
        logger.info(f"Swagger文档中总共有 {len(paths)} 个路径")

        base_path = swagger_data.get("basePath", "")
        logger.info(f"Swagger文档的basePath: {base_path}")

        search_url = handle_base_path(url, base_path)
        logger.info(f"去掉basePath后的URL: {search_url}")

        search_url_parts = search_url.lstrip("/").split("/")

        swagger_paths_with_params = [path for path in paths.keys() if "{" in path and "}" in path]
        logger.info(f"Swagger文档中有 {len(swagger_paths_with_params)} 个带参数的路径")

        for swagger_path in swagger_paths_with_params:
            matched, path_params = match_url_pattern(search_url, swagger_path)
            if matched:
                logger.info(f"从Swagger文档中匹配到路径模板: {swagger_path}")
                swagger_parts = swagger_path.lstrip("/").split("/")
                result_parts = []
                for url_part, swagger_part in zip(search_url_parts, swagger_parts):
                    if swagger_part.startswith("{") and swagger_part.endswith("}"):
                        param_name = swagger_part[1:-1]
                        result_parts.append(param_name)
                    else:
                        result_parts.append(url_part)
                full_path = swagger_path
                if base_path and base_path != "/":
                    full_path = base_path.rstrip("/") + "/" + swagger_path.lstrip("/")
                return full_path, path_params, result_parts
        logger.info("未能从Swagger文档中匹配到路径模板")

    return url, {}, url_parts


def find_matching_api_file(
    request_url: str,
    api_files: list[str],
    request_url_map: dict = None,
) -> Optional[str]:
    """
    从API文件列表中查找匹配的API文件

    Args:
        request_url: 请求URL
        api_files: API文件路径列表
        request_url_map: 请求URL到转换后URL的映射

    Returns:
        Optional[str]: 匹配的API文件路径
    """

    # 从request_url_map获取转换后的URL，如果没有则用原始URL
    # 如果提供了Swagger映射表，使用映射后的模板URL（如 /api/user/{userId}/info ）进行匹配
    transformed_url = request_url_map.get(request_url, request_url) if request_url_map else request_url

    # 遍历所有API文件，尝试匹配
    for api_file in api_files:
        result = get_url_from_api_file(api_file)
        if result:
            _, file_url = result # file_url 是API文件中定义的URL模板

            # 三种匹配方式（任一匹配成功即返回）
            # 1. 直接匹配
            # 2. 转换后直接匹配
            # 3. 路径模板匹配（如 /user/123/info 匹配 /user/{userId}/info）
            matched, _ = match_url_pattern(request_url, file_url)
            if (
                request_url == file_url
                or transformed_url == file_url
                or matched
            ):
                return api_file

    return None