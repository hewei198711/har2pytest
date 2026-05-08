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
    clean_url = url.lstrip("/")
    url_parts = clean_url.split("/")

    # 如果URL已经是模板格式（包含 {param}），直接提取路径参数
    if "{" in url and "}" in url:
        path_params = {}
        result_parts = []
        for part in url_parts:
            if part.startswith("{") and part.endswith("}"):
                param_name = part[1:-1]
                result_parts.append(param_name)
                path_params[param_name] = ""  # 模板格式，参数值为空
            else:
                result_parts.append(part)
        return url, path_params, result_parts

    # 先尝试从配置的PATH_URLS中匹配
    for path_pattern in APIConfig.PATH_URLS():
        pattern_parts = path_pattern.lstrip("/").split("/")

        if len(url_parts) != len(pattern_parts):
            continue

        matched = True
        result_parts = []
        path_params = {}

        for url_part, pattern_part in zip(url_parts, pattern_parts):
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

    # 检查URL中是否有数字
    has_numeric = any(part.isdigit() for part in url_parts)
    logger.info(f"检查URL: {url}, 是否包含数字: {has_numeric}")

    # 如果有数字且提供了Swagger文档，尝试从Swagger文档中匹配路径模板
    if has_numeric and swagger_data and "paths" in swagger_data:
        paths = swagger_data["paths"]
        logger.info(f"Swagger文档中总共有 {len(paths)} 个路径")

        # 获取Swagger文档的basePath并处理
        base_path = swagger_data.get("basePath", "")
        logger.info(f"Swagger文档的basePath: {base_path}")

        # 使用工具函数处理basePath
        search_url = handle_base_path(url, base_path)
        logger.info(f"去掉basePath后的URL: {search_url}")

        # 重新解析URL
        clean_search_url = search_url.lstrip("/")
        search_url_parts = clean_search_url.split("/")

        # 先过滤出所有带{}的路径，这样可以减少遍历的数量
        swagger_paths_with_params = [path for path in paths.keys() if "{" in path and "}" in path]
        logger.info(f"Swagger文档中有 {len(swagger_paths_with_params)} 个带参数的路径")

        # 遍历带{}的路径
        for swagger_path in swagger_paths_with_params:
            swagger_parts = swagger_path.lstrip("/").split("/")

            # 长度必须相同
            if len(search_url_parts) != len(swagger_parts):
                continue

            matched = True
            result_parts = []
            path_params = {}

            for url_part, swagger_part in zip(search_url_parts, swagger_parts):
                # 如果Swagger路径部分是参数（带{}）
                if swagger_part.startswith("{") and swagger_part.endswith("}"):
                    param_name = swagger_part[1:-1]
                    result_parts.append(param_name)
                    path_params[param_name] = url_part
                else:
                    # 非参数部分必须完全匹配
                    if url_part != swagger_part:
                        matched = False
                        break
                    result_parts.append(url_part)

            if matched:
                logger.info(f"从Swagger文档中匹配到路径模板: {swagger_path}")
                # 将basePath加回到返回的URL中，确保完整路径
                full_path = swagger_path
                if base_path and base_path != "/":
                    full_path = base_path.rstrip("/") + "/" + swagger_path.lstrip("/")
                return full_path, path_params, result_parts
        logger.info("未能从Swagger文档中匹配到路径模板")

    # 如果没有匹配到模板，直接返回原始URL
    return url, {}, url_parts


def extract_function_name(url: str) -> str:
    """
    从URL中提取测试方法函数名
    优先匹配 APIConfig.PATH_URLS 中的路径模板，处理路径参数 {xxx}
    无匹配时，直接将URL路径用下划线连接并清理非法字符（将-替换为_）

    Args:
        url: 原始接口URL，如 /mobile/trade/orderCommit

    Returns:
        str: 生成的函数名片段，如 _mobile_trade_orderCommit

    Example:
        URL: /mobile/trade/orderCommit → 返回 _mobile_trade_orderCommit
        URL: /user/{userId}/info → 返回 _user_userId_info
        URL: /appStore/dis-inventory/settled-scope → 返回 _appStore_dis_inventory_settled_scope
    """
    # 先处理URL中的花括号参数，将 {param} 转换为 param
    processed_url = url
    import re

    # 匹配 {param} 格式的参数
    param_pattern = r"\{([^\}]+)\}"
    processed_url = re.sub(param_pattern, r"\1", processed_url)

    # 直接从URL中提取路径部分，生成函数名
    clean_url = processed_url.lstrip("/")
    url_parts = clean_url.split("/")

    # 先尝试从配置的PATH_URLS中匹配
    for path_pattern in APIConfig.PATH_URLS():
        pattern_parts = path_pattern.lstrip("/").split("/")

        if len(url_parts) != len(pattern_parts):
            continue

        matched = True
        result_parts = []

        for url_part, pattern_part in zip(url_parts, pattern_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                # 如果pattern_part是参数（带{}），使用参数名
                param_name = pattern_part[1:-1]
                # 将参数名中的非法字符替换为下划线
                param_name = re.sub(r"[^a-zA-Z0-9_]", "_", param_name)
                result_parts.append(param_name)
            else:
                # 非参数部分必须完全匹配
                if url_part != pattern_part:
                    matched = False
                    break
                # 将路径部分中的非法字符替换为下划线
                url_part_clean = re.sub(r"[^a-zA-Z0-9_]", "_", url_part)
                result_parts.append(url_part_clean)

        if matched:
            return f"_{'_'.join(result_parts)}"

    # 如果没有匹配到PATH_URLS，直接使用URL路径部分，清理非法字符
    cleaned_parts = [re.sub(r"[^a-zA-Z0-9_]", "_", part) for part in url_parts]
    return f"_{'_'.join(cleaned_parts)}"


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
    seen = []
    unique_values = []
    for value in values:
        key = tuple(value) if isinstance(value, list) else value
        if key not in seen:
            seen.append(key)
            unique_values.append(tuple(value) if isinstance(value, list) else value)
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
    if task_id:
        output_dir = os.path.join(base_output_dir, task_id)
    else:
        output_dir = base_output_dir
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
        headers_match = re.search(r'headers\s*=\s*\{[^}]*\}', content, re.DOTALL)
        if headers_match:
            headers_block = headers_match.group(0)
            # 提取每个header键值对
            header_matches = re.findall(r'"(\w+[-]?\w+)"\s*:\s*("[^"]*"|f"[^"]*")', headers_block)
            for key, value in header_matches:
                headers[key] = value.strip()
    except Exception as e:
        logger.error(f"读取API文件 {api_file} 失败: {str(e)}")

    return headers


def format_dict_for_python(
    data: dict,
    value_formatter: callable = None,
    comments: dict = None
) -> str:
    """
    通用的字典格式化函数，将字典转换为Python代码字符串

    Args:
        data: 要格式化的字典
        value_formatter: 值格式化函数，接受值返回格式化后的字符串
        comments: 注释字典，key为字典key，value为注释内容

    Returns:
        格式化后的Python字典字符串
    """
    if not data:
        return "{}"
    
    if value_formatter is None:
        def value_formatter(v):
            return repr(v)
    
    if comments is None:
        comments = {}
    
    items = []
    for key, value in data.items():
        formatted_value = value_formatter(value)
        comment = comments.get(key, "")
        if comment:
            items.append(f'"{key}": {formatted_value},  # {comment}')
        else:
            items.append(f'"{key}": {formatted_value},')
    
    return "{\n" + "\n".join(items) + "\n}"


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
    
    return format_dict_for_python(headers, header_value_formatter)
