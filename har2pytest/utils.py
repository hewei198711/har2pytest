# coding:utf-8
import re
import json
from typing import Dict, Any, Optional

from .logger import logger


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

