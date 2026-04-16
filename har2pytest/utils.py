# coding:utf-8
import re
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
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 先尝试从函数文档字符串中提取
        pattern = r'def\s+\w+\s*\([^)]*\):\s*"""\s*(.*?)\s*"""'
        matches = re.findall(pattern, content, re.DOTALL)

        if matches:
            doc_content = matches[0]
            lines = [line.strip() for line in doc_content.split('\n') if line.strip()]
            if len(lines) >= 2:
                api_name = lines[0]
                second_line = lines[-1]
                if second_line.startswith('/'):
                    return api_name, second_line
        
        # 如果从文档字符串中提取失败，尝试从整个文件内容中提取URL
        url_pattern = r'https?://[^\s]+'
        url_matches = re.findall(url_pattern, content)
        if url_matches:
            return "", url_matches[0]

    except Exception as e:
        logger.error(f"读取文件 {filepath} 失败: {str(e)}")

    return None


def format_single_parameter_value(value: Any) -> str:
    """
    格式化单个参数值，用于API文件生成

    将各种类型的参数值格式化为Python代码字符串，支持字符串、布尔值、数字、列表、None等类型

    Args:
        value: 参数值，可以是字符串、布尔值、数字、列表、None等任意类型

    Returns:
        str: 格式化后的参数值字符串，如 '"TS001"'、'True'、'1'、'None'

    Example:
        result = format_single_parameter_value("TS001")
        # 返回 '"TS001"'
        result = format_single_parameter_value(True)
        # 返回 'True'
        result = format_single_parameter_value(1)
        # 返回 '1'
        result = format_single_parameter_value(None)
        # 返回 'None'
    """
    if isinstance(value, str):
        if value.strip().startswith('{') and value.strip().endswith('}'):
            escaped_value = escape_string_for_python(value)
            return f'"{escaped_value}"'
        else:
            escaped_value = escape_string_for_python(value)
            return f'"{escaped_value}"'
    elif isinstance(value, bool):
        return f'{value}'
    elif isinstance(value, (int, float)):
        return f'{value}'
    elif isinstance(value, list):
        return format_list_for_python(value, compact=True)
    elif value is None:
        return 'None'
    else:
        return f'{value}'


def format_list_for_python(lst: list, indent: int = 4, compact: bool = False) -> str:
    """
    格式化列表为Python代码格式，保持None为None而不是null

    将Python列表格式化为代码字符串，支持嵌套列表、字典、字符串、数字、布尔值、None等类型

    Args:
        lst: 要格式化的列表，如 [{"productId": "123"}, "456", None]
        indent: 缩进空格数，默认为4
        compact: 是否使用紧凑格式，默认为False

    Returns:
        str: 格式化后的列表字符串，如 '\n    {"productId": "123"},\n    "456",\n    None,\n]' 或 '[1, 2, 3]'

    Example:
        result = format_list_for_python([{"productId": "123"}, "456", None])
        # 返回 '\n    {"productId": "123"},\n    "456",\n    None,\n]'
        result = format_list_for_python([1, 2, 3], compact=True)
        # 返回 '[1, 2, 3]'
    """
    if not lst:
        return "[]"

    if compact:
        # 紧凑格式
        items = []
        for item in lst:
            if item is None:
                items.append('None')
            elif isinstance(item, bool):
                items.append(str(item))
            elif isinstance(item, (int, float)):
                items.append(str(item))
            elif isinstance(item, str):
                escaped_value = escape_string_for_python(item)
                items.append(f'"{escaped_value}"')
            elif isinstance(item, list):
                items.append(format_list_for_python(item, compact=True))
            elif isinstance(item, dict):
                import json
                dict_str = json.dumps(item, ensure_ascii=False)
                dict_str = dict_str.replace('null', 'None')
                dict_str = dict_str.replace('false', 'False')
                dict_str = dict_str.replace('true', 'True')
                items.append(dict_str)
            else:
                items.append(str(item))
        return '[' + ', '.join(items) + ']'
    else:
        # 缩进格式
        lines = ["["]
        for item in lst:
            if item is None:
                lines.append(f"{' ' * (indent + 4)}None,")
            elif isinstance(item, bool):
                lines.append(f"{' ' * (indent + 4)}{item},")
            elif isinstance(item, (int, float)):
                lines.append(f"{' ' * (indent + 4)}{item},")
            elif isinstance(item, str):
                escaped_value = escape_string_for_python(item)
                lines.append(f"{' ' * (indent + 4)}{escaped_value}",)
            elif isinstance(item, list):
                nested_list = format_list_for_python(item, indent + 4)
                lines.append(f"{' ' * (indent + 4)}{nested_list},")
            elif isinstance(item, dict):
                import json
                dict_str = json.dumps(item, ensure_ascii=False, indent=indent + 4)
                dict_str = dict_str.replace('null', 'None')
                dict_str = dict_str.replace('false', 'False')
                dict_str = dict_str.replace('true', 'True')
                lines.append(f"{' ' * (indent + 4)}{dict_str},")
            else:
                lines.append(f"{' ' * (indent + 4)}{item},")

        lines.append(f"{' ' * indent}]")
        return "\n".join(lines)


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
    value = value.replace('\\', '\\\\')
    
    # 2. 转义 换行、回车、制表符（看不见的特殊字符）
    value = value.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    return value