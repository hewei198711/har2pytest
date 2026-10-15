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

from .api_metadata import (
    CONSTANT_PARAMS_FIELD,
    HAR_PARAM_VALUES_FIELD,
    HAR_PARAMS_FIELD,
    HAR_TIME_PAIRS_FIELD,
    VALUE_FIELDS,
    read_api_metadata,
)
from .config import APIConfig
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


def write_test_file(filepath: str, content: str) -> None:
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


def parse_state_values(remark: str) -> list[int] | list[str]:
    """从参数备注中解析参数化取值。

    支持内置 5 种提取模式，并可通过配置 STATE_VALUE_PATTERNS 扩展。
    所有模式统一遍历，首个匹配成功即返回。

    Args:
        remark: 参数备注字符串

    Returns:
        参数化取值列表（整数或字符串）
    """
    # 箭头模式单独提取：用于优先预检查，避免被冒号模式误匹配
    # 例如 "经营模式 1->1:3押货 2->85折押货" 应解析为 [1, 2] 而非被冒号模式匹配到 [1]
    arrow_pattern = r"(?<!\w)(-?\d+)\s*[-\u2192>]"  # 匹配段首数字后跟箭头或破折号（如 1->描述、1→描述、-5->待收礼）

    # 内置匹配模式：(类型, 正则)
    # 注意：模式 0/4 添加 (?<!\w) 负向后行断言，避免匹配嵌入单词中的数字（如 "H5、APP" 中的 5）
    # 注意：模式 5 使用 (?<![a-zA-Z0-9_]) 而非 (?<!\w)，因为 Python 3 的 \w 匹配中文字符
    # 注意：箭头模式（原 index 1）已单独提取，此处不再包含
    builtin_patterns = [
        ("int", r"(?<!\w)(-?\d+)\s*[:\uff1a\u3001\u3002.]"),  # 匹配段首数字后跟冒号、顿号或点号（如 1.产品编码）
        ("str", r"(\w+)\s*->"),  # 匹配文本后跟箭头（如 health->上海健康 ev->企业微信）
        ("bracket_int", r"\((.*?)\)"),  # 匹配括号内的连续数字
        ("int", r"(?<!\w)(\d+)(?=[\u4e00-\u9fff])"),  # 匹配段首数字后直接跟中文（如 1待审核 2审核通过）
        ("int", r"(?<![a-zA-Z0-9_])(\d)(?!\d)"),  # 匹配嵌在中文中的单个数字（如 转赠方式1指定2扫码）
    ]

    # 合并配置扩展模式
    all_patterns = list(builtin_patterns)
    for pattern_config in APIConfig.STATE_VALUE_PATTERNS():
        if isinstance(pattern_config, str):
            all_patterns.append(("int", pattern_config))
        elif isinstance(pattern_config, dict):
            all_patterns.append((pattern_config.get("type", "int"), pattern_config.get("regex", "")))

    # 箭头格式优先预检查
    arrow_matches = re.findall(arrow_pattern, remark)
    if arrow_matches:
        arrow_values = []
        for m in arrow_matches:
            try:
                arrow_values.append(int(m))
            except ValueError:
                pass
        if arrow_values:
            return list(dict.fromkeys(arrow_values))

    # 统一遍历，首个匹配成功即返回
    for pattern_type, pattern in all_patterns:
        if not pattern:
            continue

        if pattern_type == "bracket_int":
            m = re.search(pattern, remark)
            if m:
                numbers = re.findall(r"-?\d+", m.group(1))
                if numbers:
                    return list(dict.fromkeys(int(n) for n in numbers))
            continue

        matches = re.findall(pattern, remark)
        if not matches:
            continue

        if pattern_type == "str":
            text_matches = [m for m in matches if not m.isdigit()]
            if text_matches:
                return list(dict.fromkeys(text_matches))
        else:
            values = []
            for match in matches:
                try:
                    values.append(int(match))
                except ValueError:
                    pass
            if values:
                return list(dict.fromkeys(values))

    return []


def build_param_values(param_remarks: dict[str, str]) -> dict[str, list[Any]]:
    """从参数备注字典中解析所有参数的枚举值。

    Args:
        param_remarks: 参数备注字典

    Returns:
        参数枚举值字典（如 {"getType": [1,2,3], "platform": [1,2,4]}）
    """
    param_values: dict[str, list[Any]] = {}
    for param_name, remark in param_remarks.items():
        values = parse_state_values(remark)
        if values:
            param_values[param_name] = values
    return param_values


def build_time_pairs(param_remarks: dict[str, str]) -> dict[str, dict[str, str]]:
    """从参数备注字典中识别时间参数对并提取元数据。

    通过 TIME_PARAMS 配置关键字检测时间参数，按基础名分组后配对
    start/end 参数，并从备注中提取日期格式。

    Args:
        param_remarks: 参数备注字典

    Returns:
        时间对元数据字典（如 {"getTime": {"start": "getTimeStartTime",
        "end": "getTimeEndTime", "format": "yyyy-MM-dd"}}）
    """
    # 按基础名分组：base -> {"start": param_name, "end": param_name}
    groups: dict[str, dict[str, str]] = {}
    for param_name in param_remarks:
        if not APIConfig.is_time_param(param_name):
            continue
        name_lower = param_name.lower()
        # 尝试剥离 end/start 后缀（先 end 后 start，避免 startswith 误匹配）
        for suffix in ("endtime", "starttime", "end", "start"):
            if name_lower.endswith(suffix):
                base = param_name[:len(param_name) - len(suffix)]
                pair_type = "end" if suffix in ("endtime", "end") else "start"
                groups.setdefault(base, {})[pair_type] = param_name
                break

    # 只保留同时有 start 和 end 的配对，提取日期格式
    time_pairs: dict[str, dict[str, str]] = {}
    for base, params in groups.items():
        if "start" in params and "end" in params:
            start_remark = param_remarks.get(params["start"], "")
            fmt = _extract_date_format_from_remark(start_remark)
            time_pairs[base] = {
                "start": params["start"],
                "end": params["end"],
                "format": fmt,
            }
    return time_pairs


def _extract_date_format_from_remark(remark: str) -> str:
    """从参数备注中提取日期格式（括号内的 yyyy/MM/dd 等）并转换为 strftime 格式。

    Args:
        remark: 参数备注文本（如 "领取时间开始时间(yyyy-MM-dd)"）

    Returns:
        strftime 格式字符串（如 "%Y-%m-%d"）；未找到时默认 "%Y-%m-%d"
    """
    match = re.search(r"[\(\uff08]([^\)\uff09]+)[\)\uff09]", remark)
    if not match:
        return "%Y-%m-%d"
    fmt = match.group(1)
    # Java 风格日期格式 → Python strftime
    fmt = fmt.replace("yyyy", "%Y").replace("yy", "%y")
    fmt = fmt.replace("MM", "%m").replace("dd", "%d")
    fmt = fmt.replace("HH", "%H").replace("mm", "%M").replace("ss", "%S")
    return fmt


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


def clear_api_file_cache() -> None:
    """清除 API 文件解析缓存。"""
    _API_FILE_CACHE.clear()


# headers 字段名（用于区分合并策略：headers 仅接受 dict 整体合并，其余字段非 dict 时整体替换）
_API_HEADER_ASSIGN = "headers"
_API_CURRENT_FIELDS = VALUE_FIELDS


def _normalize_field_value(current: Any, value: Any) -> Any:
    """当前值字段的统一规则：dict 时合并、非 dict 时整体替换。返回要写入的新值。

    注意：headers 非 dict 值的过滤由调用方 _apply_current_field 提前处理，此处不再重复判断。
    """
    if isinstance(value, dict):
        base = current if isinstance(current, dict) else {}
        merged = dict(base)
        merged.update(value)
        return merged
    return value  # 非 dict 整体替换


def _apply_current_field(result: APIFileInfo, key: str, value: Any) -> None:
    """把 headers/params/data/files 的当前值应用到解析结果（规则同 _normalize_field_value）。"""
    if key == _API_HEADER_ASSIGN and not isinstance(value, dict):
        return
    merged = _normalize_field_value(getattr(result, key), value)
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
    # 读取参数枚举值（param_values）
    param_vals = metadata.get("param_values")
    if isinstance(param_vals, dict):
        result.param_values.update(param_vals)
    # 读取时间参数对元数据（time_pairs）；HAR 派生元数据（har_time_pairs）只
    # 补齐 time_pairs 中不存在的基础名（Swagger 备注提取的格式更准确，优先）
    time_pairs_data = metadata.get("time_pairs")
    if isinstance(time_pairs_data, dict):
        result.time_pairs.update(time_pairs_data)
    har_time_pairs_data = metadata.get(HAR_TIME_PAIRS_FIELD)
    if isinstance(har_time_pairs_data, dict):
        for base, info in har_time_pairs_data.items():
            if base not in result.time_pairs and isinstance(info, dict):
                result.time_pairs[base] = info
    # 读取常量参数
    cp = metadata.get(CONSTANT_PARAMS_FIELD)
    if isinstance(cp, dict):
        result.constant_params = dict(cp)
    # 读取 HAR 参数枚举值
    hpv = metadata.get(HAR_PARAM_VALUES_FIELD)
    if isinstance(hpv, dict):
        result.har_param_values.update(hpv)
    # 读取 HAR 参数基线值
    hp = metadata.get(HAR_PARAMS_FIELD)
    if isinstance(hp, dict):
        result.har_params.update(hp)
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
    return format_params_for_python(headers, header_value_formatter)


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

    # inline 模式不加缩进，多行模式按 indent 参数缩进
    indent_str = "" if inline else " " * indent
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
        return "{" + " ".join(items) + "}"
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
    # 纯数字或下划线开头时加 param_ 前缀，确保为合法标识符
    if not (safe[0].isalpha() or safe[0] == "_"):
        safe = "param_" + safe
    return safe


def extract_service_package(api_file: str, api_dir: str) -> str | None:
    """从 API 文件路径中提取服务包名称。

    Args:
        api_file: API 文件路径
        api_dir: API 目录根路径

    Returns:
        相对 api_dir 的首段目录名（服务包名）；文件直接位于 api_dir 下
        或路径无法相对化时返回 None。
    """
    try:
        rel_path = os.path.relpath(api_file, api_dir)
    except ValueError:
        return None
    module_path = rel_path.removesuffix(".py").replace("\\", "/")
    parts = module_path.split("/")
    if len(parts) > 1:
        return parts[0]
    return None
