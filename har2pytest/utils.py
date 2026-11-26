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
    DB_PARAMS_FIELD,
    FIELD_MAP_FIELD,
    HAR_PARAM_VALUES_FIELD,
    HAR_PARAMS_FIELD,
    HAR_TIME_PAIRS_FIELD,
    SINGLE_TIME_PARAMS_FIELD,
    VALUE_FIELDS,
    VALUE_PAIRS_FIELD,
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


# 人工校验保护标记：测试文件中出现该注释行时，--overwrite 也不覆盖该文件
MANUAL_KEEP_MARKER = "# har2pytest: keep"


def is_manually_kept(filepath: str) -> bool:
    """判断测试文件是否带人工保护标记（MANUAL_KEEP_MARKER）。

    文件中任意一行以标记注释开头（允许标记后附加说明文字）即视为
    已人工校验，生成器在 --overwrite 模式下也应跳过覆盖。
    读取失败按未保护处理，避免阻塞正常生成。

    Args:
        filepath: 测试文件路径。

    Returns:
        bool: 文件带保护标记时返回 True。
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            return any(line.strip().startswith(MANUAL_KEEP_MARKER) for line in f)
    except OSError:
        return False


async def format_directory(dir_path: str) -> None:
    """异步批量格式化指定目录下的所有 Python 文件。

    对整个目录运行 ruff check --fix 和 ruff format，
    比逐个文件格式化效率更高。
    使用 --no-respect-gitignore，避免输出目录（如 apis/、testcases/）
    位于 .gitignore 时 ruff 跳过全部文件导致格式化被静默忽略。
    带人工保护标记（MANUAL_KEEP_MARKER）的文件会被排除，
    避免 --fix/format 静默改动已人工校验的内容。

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

    # 人工保护文件不参与格式化：--fix 可能删改 import、format 可能重排代码，
    # 都会破坏已人工校验的形态，故显式排除。
    # 必须用绝对路径（正斜杠）：ruff 的含分隔符 exclude 模式按 cwd 相对路径匹配，
    # 相对目标目录的路径在 cwd 不同时不会命中（实测验证）
    kept_abs_paths = [
        os.path.abspath(os.path.join(root, file)).replace(os.sep, "/")
        for root, _, files in os.walk(dir_path)
        for file in files
        if file.endswith(".py") and is_manually_kept(os.path.join(root, file))
    ]
    exclude_args = ["--exclude", ",".join(kept_abs_paths)] if kept_abs_paths else []

    # 生成代码在 import 前设置 client，E402 为固有结构，忽略避免误报
    await _run_ruff(
        ["check", "--fix", "--ignore", "E402", "--no-respect-gitignore", *exclude_args, dir_path], "check --fix"
    )
    await _run_ruff(["format", "--no-respect-gitignore", *exclude_args, dir_path], "format")


def parse_state_values(remark: str) -> list[int] | list[str]:
    """从参数备注中解析参数化取值。

    支持内置 6 种提取模式，并可通过配置 STATE_VALUE_PATTERNS 扩展。
    所有模式统一遍历，首个匹配成功即返回。

    Args:
        remark: 参数备注字符串

    Returns:
        参数化取值列表（整数或字符串）
    """
    # 箭头/连字符模式：段首数字后跟箭头或连字符（如 1->描述、1→描述、-5->待收礼、11-签约购）
    # 不再独立早返预检查：连字符枚举常与点号编号混排（如 "0. 立即购买;…;11-签约购"），
    # 早返会阻断模式0 丢失前项；改为在模式0 分支内条件伴生合并（见下方注释）。
    # 注意：不能给模式0 加“冒号/点号后不跟数字”守卫，会误杀“枚举：版本号描述”
    # 合法形态（如 "1：2.0；2：3.0；3：4.0"，全量语料实测丢值 147 处）
    arrow_pattern = r"(?<!\w)(-?\d+)\s*[-\u2192>]"

    # 模式0：段首数字后跟标点分隔符
    int_punct_pattern = r"(?<!\w)(-?\d+)\s*[:：、。.]"
    # 模式0 伴生形态：顿号/逗号后接“数字+空白+中文描述”的混排尾项
    # （如 "10、演示加购 20、演示立即购买、30 演示提交订单" 的 30）。
    # 仅在模式0已有命中时合并取数：独立成模式会因首中即返丢失前项，
    # 无条件合并会在模式0空命中时阻断括号/单数字兜底模式丢失首项
    int_list_tail_pattern = r"(?<=[、,，])\s*(-?\d+)(?=\s+[\u4e00-\u9fff])"
    # 纯大写 token 顿号/逗号列表（如 "APP 、PC、DEMO_PROGRAM"）：
    # 须≥2 个分隔命中才生效（排除“用户ID”类单词尾粘连），再补末尾 token（含“等”/右括号收尾）；
    # 后行排除中文/词字符/斜杠粘连（"会员ID"、"1/PC" 不是独立枚举 token）
    str_list_pattern = r"(?<![A-Za-z0-9_\u4e00-\u9fff/])([A-Z][A-Z0-9_]+)(?=\s*[、,，])"
    str_list_tail_pattern = r"([A-Z][A-Z0-9_]+)\s*[等)）]?\s*$"

    # 内置匹配模式：(类型, 正则)
    # 注意：模式 0/4 添加 (?<!\w) 负向后行断言，避免匹配嵌入单词中的数字（如 "H5、APP" 中的 5）
    # 注意：模式 5 使用 (?<![a-zA-Z0-9_]) 而非 (?<!\w)，因为 Python 3 的 \w 匹配中文字符
    # 注意：箭头模式（原 index 1）已单独提取，此处不再包含
    builtin_patterns = [
        ("int", int_punct_pattern),  # 匹配段首数字后跟冒号、顿号或点号（如 1.产品编码）
        ("str", r"(\w+)\s*->"),  # 匹配文本后跟箭头（如 health->上海健康 ev->企业微信）
        ("str_list", str_list_pattern),  # 纯大写 token 顿号/逗号列表（≥2 命中 + 末尾 token 补全）
        ("bracket_int", r"\((.*?)\)"),  # 匹配括号内的连续数字（仅限独立数字，如 (1,2,3)、(1:正常 0:禁用)）
        ("int", r"(?<!\w)(\d+)(?=[\u4e00-\u9fff])"),  # 匹配段首数字后直接跟中文（如 1待审核 2审核通过）
        # 数字与小写英文缩写无分隔符粘连的紧凑枚举（如 1app2pc4小程序）：
        # 无对应正则，循环内 chain_int 分支用链中/链尾两条子模式合并取数；
        # 必须位于单数字兜底模式之前，否则兜底只命中段首数字提前返回
        ("chain_int", None),
        ("int", r"(?<![a-zA-Z0-9_])(\d)(?![\d.])"),  # 匹配嵌在中文中的单个数字（如 转赠方式1指定2扫码）；排除小数点形式（如 "类型为2.shortLink" 引用其他参数取值）
    ]

    # 合并配置扩展模式
    all_patterns = list(builtin_patterns)
    for pattern_config in APIConfig.STATE_VALUE_PATTERNS():
        if isinstance(pattern_config, str):
            all_patterns.append(("int", pattern_config))
        elif isinstance(pattern_config, dict):
            all_patterns.append((pattern_config.get("type", "int"), pattern_config.get("regex", "")))

    # 统一遍历，首个匹配成功即返回
    for pattern_type, pattern in all_patterns:
        # 数字-英文缩写粘连枚举（如 1app2pc4小程序）特殊分支：链中数字
        # （数字后跟字母组再跟数字，如 1app 的 1、2pc 的 2）与链尾数字
        # （前有“数字+字母组”、后跟中文或结尾，如 4小程序 的 4）合并保序。
        # 全量语料量化：仅 3 个平台类备注词干 18 处命中且全部正确；
        # base64/mp4 等词内数字因形态不满足两条子模式而不受影响
        if pattern_type == "chain_int":
            mids = re.findall(r"(\d+)(?=[a-z]+\d)", remark)
            tails = re.findall(r"\d[a-z]+(\d+)(?=[\u4e00-\u9fff]|$)", remark)
            values = [int(v) for v in dict.fromkeys([*mids, *tails])]
            if values:
                return values
            continue

        if not pattern:
            continue

        if pattern_type == "bracket_int":
            m = re.search(pattern, remark)
            if m:
                # 只取独立数字：跳过紧贴字母/数字的位数，避免 "(base64转码后的path)" 提出 [64]
                numbers = re.findall(r"(?<![A-Za-z0-9])-?\d+(?![0-9])", m.group(1))
                if numbers:
                    return list(dict.fromkeys(int(n) for n in numbers))
            continue

        if pattern_type == "str_list":
            hits = re.findall(pattern, remark)
            if len(hits) >= 2:
                tail = re.search(str_list_tail_pattern, remark)
                values = list(hits)
                if tail and tail.group(1) not in values:
                    values.append(tail.group(1))
                return list(dict.fromkeys(values))
            continue

        matches = re.findall(pattern, remark)
        # 模式0 与混排尾项/箭头连字符模式条件伴生合并：
        # 已有命中→按备注位置序收集三种模式的取值并集（保证备注自然顺序，避免排序噪音）；
        # 空命中→维持旧箭头预检查早返语义（如 "1->1:3押货 2->85折押货" 取 [1,2]），
        # 且不得阻断后续括号/单数字兜底模式（否则丢首项）
        if pattern == int_punct_pattern:
            if matches:
                pairs = [(m.start(), m.group(1)) for m in re.finditer(pattern, remark)]
                pairs += [(m.start(), m.group(1)) for m in re.finditer(int_list_tail_pattern, remark)]
                pairs += [(m.start(), m.group(1)) for m in re.finditer(arrow_pattern, remark)]
                pairs.sort(key=lambda x: x[0])
                matches = list(dict.fromkeys(v for _, v in pairs))
            else:
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
        参数枚举值字典（如 {"getType": [1,2,3], "platform": [1,2,3]}）
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
    for param_name, remark in param_remarks.items():
        if not APIConfig.is_time_param(param_name):
            # 名称闸门不命中时按备注时间语义放行（复用 epoch 迁移的同套
            # 判定）：createBegin/createEnd 这类"词干+Begin/End 后缀"命名
            # 不含任何关键字，但备注"下单开始/结束时间"语义明确；后续剥离
            # 只保留双侧齐全的组，金额/号码类参数（备注无时间语义）不受影响
            if not _EPOCH_TIME_REMARK_PATTERN.search(remark):
                continue
        name_lower = param_name.lower()
        # 尝试剥离时间对后缀（后缀与配对侧由 TIME_PAIR_SUFFIXES 配置驱动，
        # 字典保序：先 end 类后缀避免 startswith 误匹配；默认内置 begin/min
        # 与 start 同侧、max 与 end 同侧，覆盖 commitDateBegin/End、
        # createTimeMin/Max 这类命名惯例；名称闸门/备注语义已过滤非时间
        # 参数，剥离后仍只保留双侧齐全的组）
        for suffix, pair_type in APIConfig.TIME_PAIR_SUFFIXES().items():
            if name_lower.endswith(suffix):
                base = param_name[:len(param_name) - len(suffix)]
                groups.setdefault(base, {})[pair_type] = param_name
                break
        else:
            # 后缀未命中时尝试剥离 start/end/begin 前缀（startDemoTime/endDemoTime
            # 及 beginFinishCheckTime/endFinishCheckTime 形态）；begin 与 start
            # 同为开始语义；前置 is_time_param 闸门已过滤非时间参数，前缀剥离
            # 不会误伤 endpoint 类命名
            for prefix in ("end", "start", "begin"):
                if name_lower.startswith(prefix):
                    base = param_name[len(prefix):]
                    pair_type = "end" if prefix == "end" else "start"
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


def build_value_pairs(
    api_params: dict[str, Any],
    time_pairs: dict[str, dict[str, str]] | None = None,
) -> dict[str, dict[str, str]]:
    """从参数声明中识别数值范围对（非时间的 Start/End 配对参数）。

    与 build_time_pairs 的名称形态剥离同惯例，但闸门换成类型判据：
    仅当 start/end 双侧齐全、词干相同且两侧声明值均为数值标量
    （None/int/float；Swagger 类型感知默认值中数值参数落 None，字符串
    落 ""、数组落 []，故 None 即数值声明）才配对。已被 time_pairs
    配对的成员排除（时间对机制优先）。产出的元数据供测试生成侧
    合并区间组合用例，基线由 test_0 收集响应 min/max 动态提供。

    Args:
        api_params: 参数声明字典（参数名 -> 类型感知默认值）
        time_pairs: build_time_pairs 产出的时间对元数据（可为 None）

    Returns:
        数值对元数据字典（如 {"monthExchangeAmt": {"start":
        "monthExchangeAmtStart", "end": "monthExchangeAmtEnd"}}）
    """
    paired_members: set[str] = set()
    for info in (time_pairs or {}).values():
        paired_members.add(info["start"])
        paired_members.add(info["end"])

    def is_numeric_scalar(value: Any) -> bool:
        # bool 是 int 子类须排除；None 为数值参数的类型感知默认值
        return value is None or (isinstance(value, (int, float)) and not isinstance(value, bool))

    groups: dict[str, dict[str, str]] = {}
    for param_name, value in api_params.items():
        if param_name in paired_members or not is_numeric_scalar(value):
            continue
        name_lower = param_name.lower()
        # 后缀剥离与 build_time_pairs 同惯例（先 end 后 start/begin）；
        # 类型闸门已排除字符串/数组参数，不会误伤 endpoint 类命名
        for suffix in ("end", "start", "begin"):
            if name_lower.endswith(suffix):
                base = param_name[:len(param_name) - len(suffix)]
                pair_type = "end" if suffix == "end" else "start"
                groups.setdefault(base, {})[pair_type] = param_name
                break

    value_pairs: dict[str, dict[str, str]] = {}
    for base, params in groups.items():
        if "start" in params and "end" in params:
            value_pairs[base] = {"start": params["start"], "end": params["end"]}
    return value_pairs


# epoch 时间戳格式标记：integer(int64) 声明 + 备注时间语义的 Start/End
# 配对迁入 time_pairs 后使用的 format 值（毫秒/秒，Java int64 惯例为毫秒）
EPOCH_MS_FORMAT = "epoch_ms"
EPOCH_S_FORMAT = "epoch_s"

# epoch 时间对识别：备注时间语义匹配（中文关键字子串命中即可；英文
# date/time 用整词匹配，避免误伤 candidate/update 等单词内部的 "date"）
_EPOCH_TIME_REMARK_PATTERN = re.compile(r"时间|日期|\b(?:date|time)\b", re.IGNORECASE)


def build_epoch_time_pairs(
    value_pairs: dict[str, dict[str, str]],
    param_remarks: dict[str, str],
) -> dict[str, dict[str, str]]:
    """从数值对中识别时间戳语义对并迁移为 epoch 时间对。

    Swagger 中以 integer(int64) 声明的毫秒/秒时间戳参数（如 createBegin/
    createEnd，备注"下单开始时间/结束时间"）会被 build_value_pairs 按
    数值标量判据捕获为数值对，但这类参数本质是时间对，应迁入 time_pairs
    走 datetime 动态取值链路（list_query_data 注入动态时间戳表达式），
    而非数值对 min/max 聚合链路（基线 None，不生成时间参数值）。

    格式判定：start 备注含"秒时间戳"取 epoch_s（秒级），否则默认
    epoch_ms（毫秒级）。

    Args:
        value_pairs: build_value_pairs 产出的数值对元数据
        param_remarks: 参数备注字典

    Returns:
        epoch 时间对元数据（如 {"create": {"start": "createBegin",
        "end": "createEnd", "format": "epoch_ms"}}）
    """
    epoch_pairs: dict[str, dict[str, str]] = {}
    for base, info in value_pairs.items():
        remark = param_remarks.get(info["start"], "")
        if not _EPOCH_TIME_REMARK_PATTERN.search(remark):
            continue
        fmt = EPOCH_S_FORMAT if "秒时间戳" in remark else EPOCH_MS_FORMAT
        epoch_pairs[base] = {
            "start": info["start"],
            "end": info["end"],
            "format": fmt,
        }
    return epoch_pairs


# 裸日期格式 token（无括号包裹，如 "开始业绩月份yyyyMM 202104"）：
# 年份 token 必须存在（排除散文偶合）；大小写不敏感匹配后由
# _normalize_bare_date_tokens 归一，前后行断言只排除 ASCII 字母/数字粘连
# （中文紧邻如 "月份yyyyMM" 仍须命中，故不用 \b）
_BARE_DATE_FORMAT_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:yyyy|yy)(?:[-/年.]?(?:MM|dd))*(?:[ T]?(?:HH|mm)(?::(?:mm|ss))*)?(?![A-Za-z0-9])",
    re.IGNORECASE,
)


def _normalize_bare_date_tokens(tok: str) -> str:
    """归一裸日期 token 的大小写变体（YYYY/yyyy、DD/dd、hh/HH）。

    小写 mm 按位置消歧：HH 之前为月份（MM）、之后为分钟（mm），
    如 "yyyy-mm" → "yyyy-MM"、"yyyy-mm-dd hh:mm:ss" 月/分各归其位。
    """
    hour = re.search(r"hh", tok, re.IGNORECASE)

    def repl(m: re.Match) -> str:
        t = m.group(0).lower()
        if t == "mm":
            return "mm" if hour and m.start() > hour.start() else "MM"
        return "HH" if t == "hh" else t

    return re.sub(r"(?i)yyyy|yy|mm|dd|hh|ss", repl, tok)


def extract_explicit_date_format(remark: str) -> str | None:
    """从参数备注中提取显式日期格式并转换为 strftime 格式。

    优先取括号内的 yyyy/MM/dd 等格式；括号缺失或内容无日期 token 时
    回落搜索裸格式 token（如 "开始业绩月份yyyyMM 202104"）。与
    _extract_date_format_from_remark 的区别：未识别到任何日期 token 时
    返回 None（不回落默认格式），供单时间参数的双条件识别使用。

    Args:
        remark: 参数备注文本（如 "领取时间开始时间(yyyy-MM-dd)"）

    Returns:
        strftime 格式字符串（如 "%Y-%m-%d"）；未识别到日期格式时返回 None
    """
    match = re.search(r"[\(\uff08]([^\)\uff09]+)[\)\uff09]", remark)
    if match:
        fmt = match.group(1)
        # Java 风格日期格式 → Python strftime
        fmt = (
            fmt.replace("yyyy", "%Y")
            .replace("yy", "%y")
            .replace("MM", "%m")
            .replace("dd", "%d")
            .replace("HH", "%H")
            .replace("mm", "%M")
            .replace("ss", "%S")
        )
        # 括号内容不含任何日期 token（如 "含"）时视为未识别，继续尝试裸 token
        if "%" in fmt:
            return fmt
    bare = _BARE_DATE_FORMAT_PATTERN.search(remark)
    if bare:
        tok = _normalize_bare_date_tokens(bare.group(0))
        return (
            tok.replace("yyyy", "%Y")
            .replace("yy", "%y")
            .replace("MM", "%m")
            .replace("dd", "%d")
            .replace("HH", "%H")
            .replace("mm", "%M")
            .replace("ss", "%S")
        )
    return None


def _extract_date_format_from_remark(remark: str) -> str:
    """从参数备注中提取日期格式（配对路径专用，无 token 时回落默认格式）。

    包装 extract_explicit_date_format：未识别到日期格式时默认
    "%Y-%m-%d"（纯日期）。带时分的完整格式须由备注显式声明
    （如 "yyyy-MM-dd HH:mm:ss"）。
    """
    fmt = extract_explicit_date_format(remark)
    return fmt if fmt is not None else "%Y-%m-%d"


# 单时间参数候选关键字（独立于 TIME_PARAMS 闸门：全量语料量化证实
# "orderdate" 子串会误命中 demoLimitOrderDate（演示限制开关，枚举 [0,1,2]）
# 等非时间参数，不能扩全局闸门；此处用候选关键字 + 备注显式格式 token
# 双条件识别，消费侧由落盘的 single_time_params 元数据驱动）
_SINGLE_TIME_KEYWORDS = ("orderdate", "achievementmonth", "contrastdate")


def build_single_time_params(
    param_remarks: dict[str, str],
    time_pairs: dict[str, dict[str, str]] | None = None,
) -> dict[str, dict[str, Any]]:
    """从参数备注中识别单时间参数（一个参数自身承载时间，无 start/end 伴生）。

    双条件：参数名命中候选关键字 + 备注含显式日期格式 token；已被
    time_pairs 配对的 start/end 成员排除（配对机制优先）。备注含"逗号"
    声明时间段用逗号分隔，消费侧注入"当年起点,今天"区间，否则注入当前单值。

    Args:
        param_remarks: 参数备注字典
        time_pairs: build_time_pairs 产出的时间对元数据（可为 None）

    Returns:
        单时间参数元数据字典（如 {"orderDate": {"format": "%Y-%m-%d",
        "range": True}}）；无命中时返回空字典
    """
    paired_members: set[str] = set()
    for info in (time_pairs or {}).values():
        paired_members.add(info["start"])
        paired_members.add(info["end"])
    result: dict[str, dict[str, Any]] = {}
    for name, remark in param_remarks.items():
        name_lower = name.lower()
        if not any(k in name_lower for k in _SINGLE_TIME_KEYWORDS):
            continue
        if name in paired_members:
            continue
        fmt = extract_explicit_date_format(remark or "")
        if fmt is None:
            continue
        result[name] = {"format": fmt, "range": "逗号" in (remark or "")}
    return result


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
    # 读取单时间参数元数据（single_time_params，生成侧双条件识别后落盘）
    stp = metadata.get(SINGLE_TIME_PARAMS_FIELD)
    if isinstance(stp, dict):
        result.single_time_params.update(stp)
    # 读取数值范围对元数据（value_pairs，生成侧按参数声明类型识别后落盘）
    vp = metadata.get(VALUE_PAIRS_FIELD)
    if isinstance(vp, dict):
        result.value_pairs.update(vp)
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
    # 读取数据库参数示例值（api 生成阶段按 DB_CONFIG.api_table_map 探测）
    dbp = metadata.get(DB_PARAMS_FIELD)
    if isinstance(dbp, dict):
        result.db_params = dict(dbp)
    # 读取参数名到响应字段名的显式映射（field_map，手工补充的接口语义）；
    # 键值都压成字符串，避免手工 JSON 里混入非字符串值污染下游匹配
    fm = metadata.get(FIELD_MAP_FIELD)
    if isinstance(fm, dict):
        result.field_map.update({str(k): str(v) for k, v in fm.items()})
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
