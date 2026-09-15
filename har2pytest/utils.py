"""工具函数模块。

提供参数格式化、文件处理等通用工具函数。
"""

import asyncio
import json
import keyword
import os
import re
import sys
from collections.abc import Callable
from dataclasses import replace
from typing import Any

from .api_metadata import VALUE_FIELDS, read_api_metadata
from .logger import logger
from .models import APIFileInfo, ParsedRequestInfo


def format_parameter_value(value: Any) -> str:
    """生成参数值的 Python 代码字符串（递归处理嵌套容器）。

    将 Python 值转换为可在代码中使用的字符串表示：None/True/False 用 Python
    字面量而非 JSON 字面量（null/true/false），中文字符保留，其余类型 repr 兜底。

    Args:
        value: 要格式化的值，可以是任意类型。

    Returns:
        str: 格式化后的字符串，如 '"hello"'、'123'、'None'、'{"a": [1, None]}' 等。
    """
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, list):
        items = [format_parameter_value(item) for item in value]
        return "[" + ", ".join(items) + "]"
    if isinstance(value, dict):
        items = [f"{json.dumps(k, ensure_ascii=False)}: {format_parameter_value(v)}" for k, v in value.items()]
        return "{" + ", ".join(items) + "}"
    return repr(value)


def sanitize_remark(text: Any) -> str:
    """把参数备注/描述规范化为单行文本。

    Swagger 的描述可能包含换行、制表符或续行缩进（如多行枚举说明）。这类文本
    直接写入 ``#`` 注释、docstring 或 ``@allure.title`` 字符串会造成排版错乱，
    甚至生成非法代码（unterminated string literal）。这里把行内空白折叠为单个
    空格并去掉首尾空白；中文全角空格等非 ASCII 字符保持原样。

    Args:
        text: 原始文本；非字符串返回空串。

    Returns:
        str: 单行文本。
    """
    if not isinstance(text, str):
        return ""
    return re.sub(r"[ \t\r\n\f\v]+", " ", text).strip()


def deduplicate_values(values: list[Any]) -> list[Any]:
    """对值列表进行去重处理。

    保持原始顺序，只保留第一次出现的值。

    Args:
        values: 要去重的值列表。

    Returns:
        list[Any]: 去重后的列表。
    """
    unique_values: list[Any] = []
    seen: set[str] = set()
    for value in values:
        # 统一使用 json.dumps 生成 key，避免 raw string 与 JSON 序列化结果碰撞
        key = json.dumps(value, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            unique_values.append(value)
    return unique_values


def get_output_dir(base_output_dir: str) -> str:
    """获取输出目录路径。

    如果目录不存在则创建。

    Args:
        base_output_dir: 基础输出目录。

    Returns:
        str: 输出目录的完整路径。
    """
    os.makedirs(base_output_dir, exist_ok=True)
    return base_output_dir


def write_test_file(filepath: str, content: str):
    """写入 Python 文件（不格式化）。

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
    使用 --no-respect-gitignore，避免输出目录（如 apis/、testcases/）
    位于 .gitignore 时 ruff 跳过全部文件导致格式化被静默忽略。

    Args:
        dir_path: 要格式化的目录路径（必须存在）。
    """
    if not os.path.isdir(dir_path):
        logger.warning(f"格式化目录不存在: {dir_path}")
        return

    logger.info(f"批量格式化目录: {dir_path}")

    async def _run_ruff(args: list[str], task: str) -> None:
        """运行一次 ruff（check --fix / format），失败仅告警不抛出。"""
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "ruff",
                *args,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await proc.wait()
            if proc.returncode != 0:
                logger.warning(f"ruff {task} 返回非零退出码: {proc.returncode}（可能未安装 ruff）")
        except Exception as e:
            logger.warning(f"ruff {task} 执行失败: {e}")

    # 生成代码在 import 前设置 client，E402 为固有结构，忽略避免误报
    await _run_ruff(["check", "--fix", "--ignore", "E402", "--no-respect-gitignore", dir_path], "check --fix")
    await _run_ruff(["format", "--no-respect-gitignore", dir_path], "format")


# ===========================================================================
# API 模块结构化读取（元数据唯一入口）
#
# 生成器产出 .py 的同时会写入 <module>.api.json 元数据（见 api_metadata），
# 描述/URL/参数备注与 params/data/files/headers 的当前值都在其中。
# parse_api_file 只消费元数据：没有元数据或缺少必需字段时直接报错并提示
# 补充（重新生成该 API 文件或手工补 .api.json），不再回退去解析 .py 源码。
# ===========================================================================

# API 文件解析缓存
_API_FILE_CACHE = {}


def clear_api_file_cache():
    """清除 API 文件解析缓存。"""
    _API_FILE_CACHE.clear()


# 模块级赋值可携带的参数/头名称（与 API 元数据 VALUE_FIELDS 单一来源，见 api_metadata）
_API_HEADER_ASSIGN = "headers"
_API_DATA_ASSIGNS = tuple(f for f in VALUE_FIELDS if f != _API_HEADER_ASSIGN)
_API_CURRENT_FIELDS = VALUE_FIELDS


def _normalize_field_value(key: str, current: Any, value: Any) -> Any:
    """当前值字段的统一规则：headers 仅接受 dict（整体合并）；params/data/files 为 dict 时合并、
    非 dict（如 JSON 数组 body）时整体替换。返回要写入的新值。
    """
    if isinstance(value, dict):
        base = current if isinstance(current, dict) else {}
        merged = dict(base)
        merged.update(value)
        return merged
    if key == _API_HEADER_ASSIGN:
        return current  # headers 忽略非 dict 值（保持现状）
    return value  # 其余字段非 dict 整体替换


def _apply_current_field(result: APIFileInfo, key: str, value: Any) -> None:
    """把 headers/params/data/files 的当前值应用到解析结果（规则同 _normalize_field_value）。"""
    if key == _API_HEADER_ASSIGN and not isinstance(value, dict):
        return
    merged = _normalize_field_value(key, getattr(result, key), value)
    setattr(result, key, merged)


def parse_api_file(filepath: str) -> APIFileInfo:
    """从 API 元数据（``<module>.api.json``）读取 API 信息（唯一入口）。

    生成测试用例要求每个 API 文件都带生成时写好的元数据；没有元数据或
    缺少必需字段（url 等）时抛出带提示的 ValueError，**不再回退解析 .py**
    源码/docstring——缺什么就提示补什么（重新生成该 API 文件即可自动补齐）。

    Args:
        filepath: API 文件路径。

    Returns:
        APIFileInfo: 包含 function_name、description、url、param_remarks、
            headers、params、data、files 的数据对象。

    Raises:
        ValueError: 缺少元数据文件或其中缺少必需字段时抛出，附补充提示。
    """
    if filepath in _API_FILE_CACHE:
        return _API_FILE_CACHE[filepath]

    result = APIFileInfo()
    result.function_name = os.path.splitext(os.path.basename(filepath))[0]

    metadata = read_api_metadata(filepath)
    if metadata is None:
        raise ValueError(
            f"缺少 API 元数据文件 {filepath}（应为同名的 .api.json），无法生成测试用例。"
            "请用 har2pytest api/swagger 重新生成该 API 文件（或手工补写 .api.json）后再生成测试用例。"
        )

    url = metadata.get("url")
    if not url:
        raise ValueError(
            f"{filepath} 的 API 元数据缺少必需字段 url，无法用于 URL 匹配/生成测试用例。"
            "请重新生成该 API 文件（--overwrite）以补齐元数据。"
        )
    result.url = url
    result.description = metadata.get("description", "")
    remarks = metadata.get("param_remarks")
    if isinstance(remarks, dict):
        # 历史元数据里的描述可能含换行（Swagger 多行 description），读取时统一压成单行
        result.param_remarks.update({key: sanitize_remark(value) for key, value in remarks.items()})
    # 当前值字段（headers/params/data/files）：仅取元数据中提供的字段
    for key in _API_CURRENT_FIELDS:
        meta_value = metadata.get(key)
        if meta_value is not None:
            _apply_current_field(result, key, meta_value)

    _API_FILE_CACHE[filepath] = replace(result)
    return result


def header_value_formatter(value: Any) -> str:
    """将 headers 值转换为可嵌入 Python 代码的字符串字面量。

    - 普通字符串：用 ``json.dumps`` 转义包装，内部引号/反斜杠/换行不会被破坏；
    - 已是字面量文本（以 ``'``/``"``/``f'``/``f"`` 开头）：原样保留，其中
      ``f'``/``f"`` 里的 ``os.environ[...]`` 转换为 ``os.environ.get(..., '')``，
      避免 import 时因环境变量未设置抛 KeyError。

    Args:
        value: headers 值，可能为普通字符串、f-string 字面量或已带引号的字符串。

    Returns:
        str: 可嵌入 Python 代码的字符串字面量。
    """
    if not isinstance(value, str):
        return repr(value)
    text = value.lstrip()
    if text.startswith(("f'", 'f"')):
        # f-string 字面量文本：仅把 os.environ[索引] 改为 .get，避免误伤其它 [] 下标
        return re.sub(r"os\.environ\[([^\[\]]+)\]", lambda m: f"os.environ.get({m.group(1)}, '')", value)
    if text[:1] in ("'", '"'):
        # 已带引号的字符串字面量，原样保留
        return value
    return json.dumps(value, ensure_ascii=False)


def format_headers_for_python(headers: dict[str, str]) -> str:
    """格式化 headers 字典为 Python 代码字符串。

    Args:
        headers: 请求头字典。

    Returns:
        str: 格式化后的 Python 代码字符串。
    """
    return format_params_for_python(headers, header_value_formatter, inline=False)


def format_params_for_python(
    params: dict,
    value_formatter: Callable | None = None,
    comments: dict | None = None,
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
        # key 用 json.dumps 转义，避免含引号/反斜杠的参数名生成非法代码
        key_literal = json.dumps(key, ensure_ascii=False) if isinstance(key, str) else repr(key)
        if isinstance(value, dict) and value:
            # 递归处理嵌套字典，传递 key_prefix 用于 dotted key 查找（inline 语义透传）
            formatted_value = format_params_for_python(
                value,
                value_formatter,
                comments,
                inline=inline,
                indent=indent + 4,
                key_prefix=full_key,
            )
        else:
            formatted_value = value_formatter(value)
        comment = comments.get(full_key, "")
        if comment:
            # 注释中的换行会导致生成代码断行/语法错误，统一压成单行
            safe_comment = sanitize_remark(comment)
            items.append(f"{indent_str}{key_literal}: {formatted_value},  # {safe_comment}")
        elif comments:
            # 有 comments 字典但无此 key 的描述，添加回退注释
            items.append(f"{indent_str}{key_literal}: {formatted_value},  # TODO: 添加参数说明")
        else:
            items.append(f"{indent_str}{key_literal}: {formatted_value},")

    if inline:
        return "{" + ", ".join(items) + "}"
    # 闭合花括号需要移除一层缩进（4个空格）
    closing_brace_indent = " " * max(0, indent - 4)
    return "{\n" + "\n".join(items) + "\n" + closing_brace_indent + "}"


def merge_request_params(request_info: ParsedRequestInfo) -> dict[str, Any]:
    """合并请求中的 query_params 和 post_data。

    Args:
        request_info: 解析后的请求信息，包含 query_params 和 post_data

    Returns:
        dict: 合并后的参数字典
    """
    params = {}
    if request_info.query_params:
        params.update(request_info.query_params)
    if request_info.post_data:
        if isinstance(request_info.post_data, dict):
            params.update(request_info.post_data)
        else:
            logger.debug(f"post_data不是字典类型，跳过合并: {type(request_info.post_data)}")
    return params


def sanitize_param_name(name: str) -> str:
    """清理参数名，使其可安全用作 Python 标识符。

    - Python 关键字（from、class 等）追加下划线；
    - 其余非标识符字符（如 ``-``、``.``、空格）替换为下划线；
    - 空结果或纯数字开头时加 ``param_`` 前缀，避免生成非法代码。

    Args:
        name: 原始参数名

    Returns:
        安全的 Python 标识符

    Examples:
        >>> sanitize_param_name("from")
        'from_'
        >>> sanitize_param_name("user_id")
        'user_id'
        >>> sanitize_param_name("order-id")
        'order_id'
    """
    if not name:
        return "param_"
    safe = re.sub(r"\W", "_", name)
    if keyword.iskeyword(safe):
        safe += "_"
    if not safe or not (safe[0].isalpha() or safe[0] == "_"):
        safe = "param_" + safe
    return safe
