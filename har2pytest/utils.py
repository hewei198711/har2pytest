# coding:utf-8
import re
import json
from typing import Dict, Any, Optional

from .logger import logger
from .config import APIConfig


def match_path_template(url: str) -> tuple:
    """
    匹配路径模板

    匹配URL与APIConfig.PATH_URLS中的路径模板，提取路径参数
    如果没有匹配到模板，自动识别路径中的数字参数

    Args:
        url: 原始接口URL，如 /mobile/trade/orderCommit

    Returns:
        tuple: (url_pattern, path_params, result_parts)
            - url_pattern: 匹配的路径模板，如 /user/{userId}/info
            - path_params: 路径参数字典，如 {"userId": "123"}
            - result_parts: 路径部分列表，用于生成函数名

    Example:
        url = "/user/123/info"
        pattern, params, parts = match_path_template(url)
        # 返回 ("/user/{userId}/info", {"userId": "123"}, ["user", "userId", "info"])
    """
    clean_url = url.lstrip("/")
    url_parts = clean_url.split("/")

    # 检查URL是否已经包含花括号参数
    has_braces = any(part.startswith("{") and part.endswith("}") for part in url_parts)

    # 处理已经包含花括号的路径部分
    processed_url_parts = []
    for part in url_parts:
        # 如果部分包含花括号，提取参数名
        if part.startswith("{") and part.endswith("}"):
            processed_url_parts.append(part[1:-1])
        else:
            processed_url_parts.append(part)

    for path_pattern in APIConfig.PATH_URLS():
        pattern_parts = path_pattern.lstrip("/").split("/")

        if len(processed_url_parts) != len(pattern_parts):
            continue

        matched = True
        result_parts = []
        path_params = {}

        for url_part, pattern_part in zip(processed_url_parts, pattern_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                param_name = pattern_part[1:-1]
                result_parts.append(param_name)
                path_params[param_name] = url_part
            else:
                if url_part != pattern_part:
                    matched = False
                    break
                result_parts.append(url_part)

        if matched:
            return path_pattern, path_params, result_parts

    # 如果没有匹配到模板
    result_parts = []
    path_params = {}
    url_pattern_parts = []

    for i, part in enumerate(url_parts):
        # 检查是否是已经包含花括号的参数
        if part.startswith("{") and part.endswith("}"):
            # 提取参数名
            param_name = part[1:-1]
            result_parts.append(param_name)
            path_params[param_name] = ""
            url_pattern_parts.append(part)  # 保留原始的花括号
        # 检查是否是数字
        elif part.isdigit():
            # 生成参数名，如 id, item_id, order_id 等
            if i == len(url_parts) - 1:
                param_name = "id"
            else:
                # 尝试从路径中获取参数名
                if i + 1 < len(url_parts) and url_parts[i + 1].isdigit():
                    param_name = f"param_{i}"
                else:
                    # 尝试使用前一个路径部分作为参数名的一部分
                    if i > 0:
                        param_name = f"{url_parts[i-1]}_id"
                    else:
                        param_name = f"param_{i}"
            result_parts.append(param_name)
            path_params[param_name] = part
            url_pattern_parts.append(f"{{{param_name}}}")
        else:
            result_parts.append(part)
            url_pattern_parts.append(part)

    url_pattern = "/" + "/".join(url_pattern_parts)
    return url_pattern, path_params, result_parts

def extract_function_name(url: str) -> str:
    """
    从URL中提取测试方法函数名
    优先匹配 APIConfig.PATH_URLS 中的路径模板，处理路径参数 {xxx}
    无匹配时，直接将URL路径用下划线连接并清理非法字符

    Args:
        url: 原始接口URL，如 /mobile/trade/orderCommit

    Returns:
        str: 生成的函数名片段，如 _mobile_trade_orderCommit

    Example:
        URL: /mobile/trade/orderCommit → 返回 _mobile_trade_orderCommit
        URL: /user/{userId}/info → 返回 _user_userId_info
    """
    # 先处理URL中的花括号参数，将 {param} 转换为 param
    processed_url = url
    import re
    # 匹配 {param} 格式的参数
    param_pattern = r"\{([^\}]+)\}"
    processed_url = re.sub(param_pattern, r"\1", processed_url)
    
    # 使用辅助方法匹配路径模板
    _, _, result_parts = match_path_template(processed_url)
    return f"_{'_'.join(result_parts)}"

def determine_service_package(url: str) -> str:
    """
    根据URL的第一个字段判断属于哪个微服务包

    Args:
        url: 原始接口URL，如 /mobile/trade/orderCommit

    Returns:
        str: 服务包名称，如 mall_mobile_application

    Example:
        URL: /mobile/trade/orderCommit → 返回 mall_mobile_application
        URL: /member/info → 返回 mall_center_member
    """
    return APIConfig.determine_service_package(url)


def extract_url_from_file(filepath: str) -> Optional[tuple]:
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
        result = extract_url_from_file("api/mall_mobile_application/_mobile_trade_orderCommit.py")
        # 返回 ("提交订单", "/mobile/trade/orderCommit")
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 先尝试从函数文档字符串中提取
        pattern = r'def\s+\w+\s*\([^)]*\):\s*"""\s*(.*?)\s*"""'
        matches = re.findall(pattern, content, re.DOTALL)

        if matches:
            doc_content = matches[0]
            lines = [line.strip() for line in doc_content.split("\n") if line.strip()]
            if len(lines) >= 2:
                api_name = lines[0]
                second_line = lines[-1]
                if second_line.startswith("/"):
                    return api_name, second_line

        # 如果从文档字符串中提取失败，尝试从整个文件内容中提取URL
        url_pattern = r"https?://[^\s]+"
        url_matches = re.findall(url_pattern, content)
        if url_matches:
            return "", url_matches[0]

    except Exception as e:
        logger.error(f"读取文件 {filepath} 失败: {str(e)}")

    return None


def format_parameter_value(value: Any) -> str:
    """
    生成参数值的Python代码字符串

    将参数值生成为可以安全写入Python文件的字符串格式，支持各种数据类型

    Args:
        value: 参数值，可以是字符串、布尔值、数字、列表、字典、None等任意类型

    Returns:
        str: 生成的参数值字符串，如 '"TS001"'、'True'、'1'、'None'、'[1, 2, 3]'

    Example:
        result = format_parameter_value("TS001")
        # 返回 '"TS001"'
        result = format_parameter_value(True)
        # 返回 'True'
        result = format_parameter_value(1)
        # 返回 '1'
        result = format_parameter_value(None)
        # 返回 'None'
        result = format_parameter_value([1, 2, 3])
        # 返回 '[1, 2, 3]'
        result = format_parameter_value({"a": 1, "b": 2})
        # 返回 '{"a": 1, "b": 2}'
    """
    # 使用json.dumps序列化，然后替换为Python语法
    result = json.dumps(value, ensure_ascii=False)
    # 替换 JSON 格式为 Python 格式
    result = result.replace("null", "None")
    result = result.replace("false", "False")
    result = result.replace("true", "True")
    
    return result


def escape_string_for_python(value: str) -> str:
    """
    转义字符串以便在Python代码中使用

    将普通字符串转义为可以安全写入.py文件的字符串，避免生成代码时报错或语法崩溃

    Args:
        value: 需要转义的字符串，如 "Hello\nWorld"

    Returns:
        str: 转义后的字符串，如 "Hello\\nWorld"

    Example:
        result = escape_string_for_python("Hello\nWorld")
        # 返回 "Hello\\nWorld"
        result = escape_string_for_python('He said "Hello"')
        # 返回 'He said "Hello"'
        result = escape_string_for_python("Path: C:\\Users")
        # 返回 "Path: C\\\sers"
    """
    # 1. 转义 反斜杠
    value = value.replace("\\", "\\\\")

    # 2. 转义 换行、回车、制表符（看不见的特殊字符）
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")

    return value

