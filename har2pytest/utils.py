"""工具函数模块。

提供参数格式化、文件处理等通用工具函数。
"""

import asyncio
import json
import os
import re
import sys
from collections.abc import Callable
from typing import Any

from .logger import logger


def format_parameter_value(value: Any) -> str:
    """生成参数值的 Python 代码字符串。

    将 Python 值转换为可在代码中使用的字符串表示。

    Args:
        value: 要格式化的值，可以是任意类型。

    Returns:
        str: 格式化后的字符串，如 '"hello"'、'123'、'None' 等。
    """
    result = json.dumps(value, ensure_ascii=False)
    result = result.replace("null", "None")
    result = result.replace("false", "False")
    result = result.replace("true", "True")
    return result


def deduplicate_values(values: list[Any]) -> list[Any]:
    """对值列表进行去重处理。

    保持原始顺序，只保留第一次出现的值。

    Args:
        values: 要去重的值列表。

    Returns:
        list[Any]: 去重后的列表。
    """
    unique_values = []
    seen = set()
    for value in values:
        key = json.dumps(value, sort_keys=True, ensure_ascii=False) if isinstance(value, (list, dict)) else value
        if key not in seen:
            seen.add(key)
            unique_values.append(value)
    return unique_values


def get_output_dir(base_output_dir: str, task_id: str = None) -> str:
    """获取输出目录路径。

    如果目录不存在则创建。

    Args:
        base_output_dir: 基础输出目录。
        task_id: 任务 ID，用于创建子目录（可选）。

    Returns:
        str: 输出目录的完整路径。
    """
    output_dir = os.path.join(base_output_dir, task_id) if task_id else base_output_dir
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


async def write_test_file(filepath: str, content: str):
    """异步写入 Python 文件（不格式化）。

    仅将内容写入文件，不进行 ruff 格式化。
    批量格式化应在所有文件生成后调用 format_directory()。

    Args:
        filepath: 文件路径。
        content: 文件内容。
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


async def format_directory(dir_path: str) -> None:
    """异步批量格式化指定目录下的所有 Python 文件。

    对整个目录运行 ruff check --fix 和 ruff format，
    比逐个文件格式化效率更高。

    Args:
        dir_path: 要格式化的目录路径（必须存在）。
    """
    if not os.path.isdir(dir_path):
        logger.warning(f"格式化目录不存在: {dir_path}")
        return

    logger.info(f"批量格式化目录: {dir_path}")
    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "ruff", "check", "--fix", dir_path,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()
    except Exception:
        pass  # check --fix 可能没有要修复的问题

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "ruff", "format", dir_path,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()
    except Exception as e:
        logger.warning(f"ruff 格式化失败: {e}")


# API文件解析缓存
_API_FILE_CACHE = {}


def parse_api_file(filepath: str) -> dict:
    """从 API 文件中提取所有信息。

    提取函数名、描述、URL、参数备注、请求头和参数值等信息。
    结果会被缓存以提高性能。

    Args:
        filepath: API 文件路径。

    Returns:
        dict: 包含以下字段的字典：
            - function_name: 函数名
            - description: 接口描述
            - url: 接口 URL
            - param_remarks: 参数备注字典
            - headers: 请求头字典
            - params: 参数值字典
            - data: data参数字典
            - files: files参数字典
    """
    if filepath in _API_FILE_CACHE:
        return _API_FILE_CACHE[filepath].copy()

    result = {
        "function_name": None,
        "description": "",
        "url": None,
        "param_remarks": {},
        "headers": {},
        "params": {},
        "data": {},
        "files": {},
    }

    try:
        basename = os.path.basename(filepath)
        result["function_name"] = os.path.splitext(basename)[0]
    except Exception as e:
        logger.error(f"从文件路径提取函数名失败 {filepath}: {str(e)}")

    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # 提取描述和URL（仅支持双引号的docstring）
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            # 获取第一个非空的捕获组
            docstring_content = docstring_match.group(1)
            lines = [line.strip() for line in docstring_content.split("\n") if line.strip()]
            if lines:
                result["description"] = lines[0]
                result["url"]  = lines[1]

        # 提取参数值和备注（params、data 和 files）
        for param_type in ["params", "data", "files"]:
            # 使用括号计数法正确提取嵌套字典（避免正则 {.*?} 在嵌套结构时截断）
            param_start = content.find(f"{param_type} = {{")
            if param_start != -1:
                brace_start = content.find("{", param_start)
                if brace_start != -1:
                    brace_count = 1
                    brace_end = brace_start + 1
                    while brace_count > 0 and brace_end < len(content):
                        if content[brace_end] == "{":
                            brace_count += 1
                        elif content[brace_end] == "}":
                            brace_count -= 1
                        brace_end += 1
                    dict_str = content[param_start:brace_end]
                else:
                    continue

                # 提取参数备注（支持嵌套 dict，使用 dotted key 如 "payDTO.accountName"）
                lines = dict_str.split("\n")
                parent_keys = []
                for line in lines:
                    stripped = line.strip()
                    # 检测进入嵌套 dict： "key": {
                    enter_match = re.match(r'"(\w+)"\s*:\s*\{', stripped)
                    if enter_match:
                        parent_keys.append(enter_match.group(1))
                        continue
                    # 检测退出嵌套 dict： } 或 },
                    if re.match(r'^\}\s*,?\s*$', stripped):
                        if parent_keys:
                            parent_keys.pop()
                        continue
                    # 匹配 key-value-comment 格式
                    comment_match = re.match(r'"(\w+)"\s*:\s*[^#]*#\s*(.+)$', stripped)
                    if comment_match:
                        key_name = comment_match.group(1)
                        remark = comment_match.group(2).strip()
                        full_key = ".".join(parent_keys + [key_name]) if parent_keys else key_name
                        result["param_remarks"][full_key] = remark
                
                # 移除行尾注释后解析字典值
                try:
                    # 移除变量名赋值部分，只保留字典内容
                    dict_str = dict_str.replace(f"{param_type} = ", "")
                    lines = dict_str.split("\n")
                    cleaned_lines = []
                    for line in lines:
                        if "#" in line:
                            line = line.split("#")[0]
                        cleaned_lines.append(line)
                    dict_str = "\n".join(cleaned_lines)

                    params_dict = eval(dict_str)
                    if isinstance(params_dict, dict):
                        result[param_type].update(params_dict)
                    break # API文件只会有第一个参数类型
                except Exception as e:
                    logger.error(f"解析 {param_type} 字典失败: {str(e)}")

        # 提取headers
        # 先定位 headers 字典范围，再提取键值对
        headers_start = content.find("headers = {")
        if headers_start != -1:
            # 找到 headers 字典的结束位置（正确处理嵌套的大括号）
            headers_start += len("headers = {")
            brace_count = 1
            headers_end = headers_start
            while brace_count > 0 and headers_end < len(content):
                if content[headers_end] == "{":
                    brace_count += 1
                elif content[headers_end] == "}":
                    brace_count -= 1
                headers_end += 1
            
            headers_content = "{" + content[headers_start:headers_end]
            
            header_pattern = r'"(\w+[-]?\w+)"\s*:\s*(f"[^"]*"|f\'[^\']*\'|"[^"]*"|\'[^\']*\')'
            for key, value in re.findall(header_pattern, headers_content):
                if value.startswith('f"') or value.startswith("f'"):
                    result["headers"][key] = value
                else:
                    result["headers"][key] = value.strip('"').strip("'")

    except Exception as e:
        logger.error(f"读取API文件 {filepath} 失败: {str(e)}")

    _API_FILE_CACHE[filepath] = result.copy()
    return result


def format_headers_for_python(headers: dict[str, str]) -> str:
    """格式化 headers 字典为 Python 代码字符串。

    Args:
        headers: 请求头字典。

    Returns:
        str: 格式化后的 Python 代码字符串。
    """

    def header_value_formatter(value):
        if isinstance(value, str) and value.startswith(('"', 'f"')):
            return value
        return f'"{value}"'

    return format_params_for_python(headers, header_value_formatter, inline=False)


def format_params_for_python(
    params: dict,
    value_formatter: Callable | None = None,
    comments: dict = None,
    inline: bool = False,
    indent: int = 4,
    key_prefix: str = "",
) -> str:
    """统一的参数格式化函数。

    将参数字典格式化为 Python 代码字符串，支持添加注释和内联格式。
    递归处理嵌套字典，使用 dotted key 查找注释。

    Args:
        params: 参数字典。
        value_formatter: 值格式化函数，默认使用 repr。
        comments: 参数注释字典，键为参数名（支持 dotted key 如 "payDTO.accountName"），值为注释内容。
        inline: 是否使用内联格式（单行）。
        indent: 缩进空格数，默认为 4。
        key_prefix: 嵌套字典的 key 前缀（用于 dotted key 查找）。

    Returns:
        str: 格式化后的 Python 代码字符串。
    """
    if not params:
        return "{}"

    if value_formatter is None:
        value_formatter = repr

    if comments is None:
        comments = {}

    indent_str = " " * indent
    items = []
    for key, value in params.items():
        full_key = f"{key_prefix}.{key}" if key_prefix else key
        if isinstance(value, dict) and value:
            # 递归处理嵌套字典，传递 key_prefix 用于 dotted key 查找
            formatted_value = format_params_for_python(
                value, value_formatter, comments,
                inline=False, indent=indent + 4, key_prefix=full_key,
            )
        else:
            formatted_value = value_formatter(value)
        comment = comments.get(full_key, "")
        if comment:
            # 将注释中的换行符替换为空格，避免语法错误
            safe_comment = comment.replace('\n', ' ').replace('\r', ' ')
            items.append(f'{indent_str}"{key}": {formatted_value},  # {safe_comment}')
        elif comments:
            # 有 comments 字典但无此 key 的描述，添加回退注释
            items.append(f'{indent_str}"{key}": {formatted_value},  # TODO: 添加参数说明')
        else:
            items.append(f'{indent_str}"{key}": {formatted_value},')

    if inline:
        return "{" + ", ".join(items) + "}"
    # 闭合花括号需要移除一层缩进（4个空格）
    closing_brace_indent = " " * max(0, indent - 4)
    return "{\n" + "\n".join(items) + "\n" + closing_brace_indent + "}"


def merge_request_params(request_info: dict[str, Any]) -> dict[str, Any]:
    """合并请求中的 query_params 和 post_data。
    
    Args:
        request_info: 请求信息字典，包含 query_params 和 post_data
        
    Returns:
        dict: 合并后的参数字典
    """
    params = {}
    if request_info.get("query_params"):
        params.update(request_info["query_params"])
    if request_info.get("post_data"):
        if isinstance(request_info["post_data"], dict):
            params.update(request_info["post_data"])
        else:
            logger.debug(f"post_data不是字典类型，跳过合并: {type(request_info['post_data'])}")
    return params