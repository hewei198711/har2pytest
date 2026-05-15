import json
import os
import re
import subprocess
import sys
from functools import lru_cache
from typing import Any, Callable, Optional

from .logger import logger


def format_parameter_value(value: Any) -> str:
    """生成参数值的Python代码字符串"""
    result = json.dumps(value, ensure_ascii=False)
    result = result.replace("null", "None")
    result = result.replace("false", "False")
    result = result.replace("true", "True")
    return result


def escape_string_for_python(value: str) -> str:
    """转义字符串以便在Python代码中使用"""
    value = value.replace("\\", "\\\\")
    value = value.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return value


def deduplicate_values(values: list[Any]) -> list[Any]:
    """对值列表进行去重处理"""
    unique_values = []
    for value in values:
        key = tuple(value) if isinstance(value, list) else value
        if key not in unique_values:
            unique_values.append(key)
    return unique_values


def format_python_file(filepath: str) -> None:
    """使用ruff格式化Python文件"""
    try:
        ruff_path = os.path.join(os.path.dirname(sys.executable), "ruff")
        subprocess.run([ruff_path, "check", "--fix", filepath], capture_output=True, text=True)
        subprocess.run([ruff_path, "format", filepath], capture_output=True, text=True)
        logger.info(f"使用ruff格式化文件: {filepath}")
    except Exception as e:
        logger.warning(f"格式化文件失败 {filepath}: {str(e)}")


def get_output_dir(base_output_dir: str, task_id: str = None) -> str:
    """获取输出目录路径"""
    output_dir = os.path.join(base_output_dir, task_id) if task_id else base_output_dir
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def write_test_file(filepath: str, content: str):
    """写入Python文件并格式化"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    format_python_file(filepath)


# API文件解析缓存
_API_FILE_CACHE = {}


def parse_api_file(filepath: str) -> dict:
    """从API文件中一次性提取所有信息（带缓存）"""
    if filepath in _API_FILE_CACHE:
        return _API_FILE_CACHE[filepath].copy()
    
    result = {
        "function_name": None,
        "description": "",
        "url": None,
        "param_remarks": {},
        "headers": {}
    }

    try:
        basename = os.path.basename(filepath)
        result["function_name"] = os.path.splitext(basename)[0]
    except Exception as e:
        logger.error(f"从文件路径提取函数名失败 {filepath}: {str(e)}")

    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # 提取描述和URL
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        docstring_url = None
        if docstring_match:
            lines = [line.strip() for line in docstring_match.group(1).split('\n') if line.strip()]
            if lines:
                result["description"] = lines[0]
                for line in lines[1:]:
                    if line.startswith('/'):
                        docstring_url = line
                        break

        # 提取URL
        url_match = re.search(r'url\s*=\s*(f)?["\']([^"\']+)["\']', content)
        if url_match:
            is_fstring = url_match.group(1) == 'f'
            result["url"] = docstring_url if is_fstring else url_match.group(2)

        # 提取参数备注
        for param_type in ["data", "params", "files"]:
            data_match = re.search(rf"{param_type}\s*=\s*\{{[^}}]*\}}", content, re.DOTALL)
            if data_match:
                param_matches = re.findall(r'"(\w+)"\s*:\s*([^#]+)\s*#\s*(.+?)\n', data_match.group(0))
                for param_name, _, remark in param_matches:
                    result["param_remarks"][param_name] = remark.strip()

        # 提取headers
        headers_match = re.search(r"headers\s*=\s*\{[^}]*\}", content, re.DOTALL)
        if headers_match:
            header_matches = re.findall(r'"(\w+[-]?\w+)"\s*:\s*("[^"]*"|f"[^"]*")', headers_match.group(0))
            for key, value in header_matches:
                result["headers"][key] = value.strip()

    except Exception as e:
        logger.error(f"读取API文件 {filepath} 失败: {str(e)}")

    _API_FILE_CACHE[filepath] = result.copy()
    return result


def clear_api_cache():
    """清除API文件解析缓存"""
    _API_FILE_CACHE.clear()


def format_headers_for_python(headers: dict[str, str]) -> str:
    """格式化headers字典为Python代码字符串"""
    def header_value_formatter(value):
        if isinstance(value, str) and value.startswith(('"', 'f"')):
            return value
        return f'"{value}"'
    
    return format_params_for_python(headers, header_value_formatter, inline=False)


def format_params_for_python(
    params: dict,
    value_formatter: Optional[Callable] = None,
    comments: dict = None,
    inline: bool = False,
) -> str:
    """统一的参数格式化函数"""
    if not params:
        return "{}"

    if value_formatter is None:
        value_formatter = repr

    if comments is None:
        comments = {}

    items = []
    for key, value in params.items():
        formatted_value = value_formatter(value)
        comment = comments.get(key, "")
        if comment:
            items.append(f'"{key}": {formatted_value},  # {comment}')
        else:
            items.append(f'"{key}": {formatted_value},')

    if inline:
        return "{" + ", ".join(items) + "}"
    return "{\n" + "\n".join(items) + "\n}"