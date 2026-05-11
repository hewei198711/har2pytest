import json
import os
import re
import subprocess
import sys
from typing import Any

from .config import APIConfig
from .logger import logger


def handle_base_path(url: str, base_path: str) -> str:
    """
    处理URL中的basePath前缀

    如果URL包含basePath前缀，将其移除，并确保结果以"/"开头

    Args:
        url: 原始URL，如 /appStore/store/xxx
        base_path: Swagger文档中的basePath，如 /appStore

    Returns:
        str: 移除basePath前缀后的URL，如 /store/xxx

    Example:
        handle_base_path("/appStore/store/xxx", "/appStore")  # 返回 "/store/xxx"
        handle_base_path("/appStore/store/xxx", "/")  # 返回 "/appStore/store/xxx"
        handle_base_path("/appStore/store/xxx", "")  # 返回 "/appStore/store/xxx"
    """
    if not base_path or base_path == "/":
        return url

    # 尝试去掉basePath前缀
    if url.startswith(base_path):
        result = url[len(base_path) :]
        if not result.startswith("/"):
            result = "/" + result
        return result
    return url


def extract_function_name(url: str) -> str:
    """
    从URL中提取测试方法函数名

    将URL路径转换为合法的Python函数名格式，去除花括号参数标记，
    将所有非字母数字下划线的字符替换为下划线。

    Args:
        url: 原始接口URL，如 /mobile/trade/orderCommit

    Returns:
        str: 生成的函数名片段，如 _mobile_trade_orderCommit

    Example:
        URL: /mobile/trade/orderCommit → 返回 _mobile_trade_orderCommit
        URL: /user/{userId}/info → 返回 _user_userId_info
        URL: /appStore/dis-inventory/settled-scope → 返回 _appStore_dis_inventory_settled_scope
    """

    if "{" in url and "}" in url:
        url = re.sub(r"\{|\}", "", url)
    
    # 直接将所有非字母数字下划线的字符替换为下划线
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", url)
    
    return cleaned


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


def deduplicate_values(values: list[Any]) -> list[Any]:
    """
    对值列表进行去重处理，支持列表类型值

    将不可哈希的值（list）转为可哈希的tuple进行去重，然后返回去重后的列表
    如果元素是列表，则转换为元组后返回；否则直接返回原值

    Args:
        values: 需要去重的值列表，可以包含任意类型，包括嵌套列表

    Returns:
        List[Any]: 去重后的值列表，列表类型的元素会被转换为元组

    Example:
        result = deduplicate_values([1, 2, 3, 2, 1])
        # 返回 [1, 2, 3]
        result = deduplicate_values([[1, 2], [3, 4], [1, 2]])
        # 返回 [(1, 2), (3, 4)]
        result = deduplicate_values(["a", "b", "a"])
        # 返回 ["a", "b"]
    """
    unique_values = []
    for value in values:
        key = tuple(value) if isinstance(value, list) else value
        if key not in unique_values:
            unique_values.append(key)
    return unique_values


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


def format_python_file(filepath: str) -> None:
    """
    使用ruff格式化Python文件

    先执行 ruff check --fix 修复代码问题，再执行 ruff format 格式化代码

    Args:
        filepath: 要格式化的Python文件路径
    """
    try:
        ruff_path = os.path.join(os.path.dirname(sys.executable), "ruff")
        subprocess.run([ruff_path, "check", "--fix", filepath], capture_output=True, text=True)
        subprocess.run([ruff_path, "format", filepath], capture_output=True, text=True)
        logger.info(f"使用ruff格式化文件: {filepath}")
    except Exception as e:
        logger.warning(f"格式化文件失败 {filepath}: {str(e)}")


def get_output_dir(base_output_dir: str, task_id: str = None) -> str:
    """
    获取输出目录路径

    :param base_output_dir: 基础输出目录
    :param task_id: 任务ID，如果提供则创建子目录 {base_output_dir}/{task_id}
    :return: 输出目录路径
    """
    output_dir = os.path.join(base_output_dir, task_id) if task_id else base_output_dir
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def write_test_file(filepath: str, content: str):
    """
    写入Python文件并格式化

    用于生成API文件和测试用例文件

    :param filepath: 文件路径
    :param content: 文件内容
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    format_python_file(filepath)


def get_function_name_from_api_file(filepath: str) -> str | None:
    """
    从API文件路径中提取函数名

    由于API文件名就是函数名（如 _user_mgmt_order_page.py），
    直接从文件名提取，无需读取文件内容

    Args:
        filepath: API文件路径

    Returns:
        Optional[str]: 函数名，如果提取失败返回None

    Example:
        result = get_function_name_from_api_file("apis/_user_login.py")
        # 返回 "_user_login"
    """
    try:
        basename = os.path.basename(filepath)
        function_name = os.path.splitext(basename)[0]
        return function_name
    except Exception as e:
        logger.error(f"从文件路径提取函数名失败 {filepath}: {str(e)}")
        return None


def get_param_remarks_from_api_file(api_file: str) -> dict[str, str]:
    """
    从API文件中提取参数备注

    Args:
        api_file: API文件路径

    Returns:
        dict[str, str]: 参数名到备注的映射字典

    Example:
        result = get_param_remarks_from_api_file("apis/_user_login.py")
        # 返回 {"username": "用户名", "password": "密码"}
    """
    param_remarks = {}
    try:
        with open(api_file, encoding="utf-8") as f:
            content = f.read()

        # 查找data字典定义
        data_match = re.search(r"data\s*=\s*\{[^}]*\}", content, re.DOTALL)
        if data_match:
            data_block = data_match.group(0)
            # 提取每个参数和备注
            param_matches = re.findall(r'"(\w+)"\s*:\s*([^#]+)\s*#\s*(.+?)\n', data_block)
            for param_name, _, remark in param_matches:
                # 提取备注中的参数名称
                # 例如："兑换流水号" 或 "顾客手机号"
                param_remarks[param_name] = remark.strip()
    except Exception as e:
        logger.error(f"读取API文件 {api_file} 失败: {str(e)}")

    return param_remarks


def get_headers_from_api_file(api_file: str) -> dict[str, str]:
    """
    从API文件中提取headers配置

    Args:
        api_file: API文件路径

    Returns:
        dict[str, str]: headers配置字典

    Example:
        result = get_headers_from_api_file("apis/_user_login.py")
        # 返回 {"channel": "pc", "content-type": "application/json"}
    """
    headers = {}
    try:
        with open(api_file, encoding="utf-8") as f:
            content = f.read()

        # 查找headers字典定义
        headers_match = re.search(r"headers\s*=\s*\{[^}]*\}", content, re.DOTALL)
        if headers_match:
            headers_block = headers_match.group(0)
            # 提取每个header键值对
            header_matches = re.findall(r'"(\w+[-]?\w+)"\s*:\s*("[^"]*"|f"[^"]*")', headers_block)
            for key, value in header_matches:
                headers[key] = value.strip()
    except Exception as e:
        logger.error(f"读取API文件 {api_file} 失败: {str(e)}")

    return headers


def format_headers_for_python(headers: dict[str, str]) -> str:
    """
    格式化headers字典为Python代码字符串

    处理f-string格式的值，确保生成正确的Python代码。
    生成单行格式，由ruff等格式化工具处理最终格式。

    Args:
        headers: headers字典

    Returns:
        格式化后的headers字符串
    """

    def header_value_formatter(value):
        # 值已经是带引号的字符串（包括 f-string）
        if isinstance(value, str) and value.startswith(('"', 'f"')):
            return value
        # 添加引号
        return f'"{value}"'

    return format_params_for_python(headers, header_value_formatter, inline=False)


def format_params_for_python(
    params: dict,
    value_formatter: callable = None,
    comments: dict = None,
    inline: bool = False,
) -> str:
    """
    统一的参数格式化函数

    Args:
        params: 参数字典
        value_formatter: 值格式化函数
        comments: 注释字典
        inline: 是否单行输出

    Returns:
        str: 格式化后的Python代码字符串
    """
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
    else:
        return "{\n" + "\n".join(items) + "\n}"
