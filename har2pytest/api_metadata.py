"""API 模块元数据（sidecar）。

背景
----
生成器原先只输出 ``*.py`` 包装模块，下游（URL 匹配、测试用例生成）必须靠
正则/大括号计数从源码文本里反解 url、描述、参数备注等信息——脆弱且随
生成格式漂移。这里在生成 ``*.py`` 的同时落一份结构化元数据
（``<module>.api.json``），把“生成时已经知道”的信息以结构化形式固化下来，
下游（``utils.parse_api_file``）只消费这份元数据，不再解析生成物源码。

元数据保存“生成时确定、手工编辑 .py 时通常不改”的字段（url、描述、
参数备注、method 等），并把 params/data/files/headers 的**当前值**一并
固化（生成时写入模块级赋值的快照）。生成测试用例前请确保每个 API 文件
都有对应的 ``.api.json``；缺失或缺少必需字段时 ``parse_api_file`` 会报错
提示补充（重新生成该 API 文件即可自动补齐）。
"""

from __future__ import annotations

import json
import os
from typing import Any

METADATA_SUFFIX = ".api.json"

# 写入/读取 API 元数据的"当前值"字段（utils 与 api_metadata 共用的单一来源）
VALUE_FIELDS = ("params", "data", "files", "headers")

# HAR 分析得出的常量参数（在超过 50% 请求中值相同的参数）
CONSTANT_PARAMS_FIELD = "constant_params"

# HAR 分析得出的参数枚举值（每个参数的唯一值列表，从所有 HAR 快照收集）
HAR_PARAM_VALUES_FIELD = "har_param_values"

# HAR 分析得出的参数基线值（常量参数 + 首条请求的所有参数值）
HAR_PARAMS_FIELD = "har_params"

# HAR 分析得出的时间参数对（从 HAR 参数基线自行配对，无 Swagger 备注时格式默认 %Y-%m-%d）
HAR_TIME_PAIRS_FIELD = "har_time_pairs"


def metadata_path(py_filepath: str) -> str:
    """返回与 ``py_filepath`` 同名的 API 元数据文件路径。"""
    return os.path.splitext(py_filepath)[0] + METADATA_SUFFIX


def write_api_metadata(
    py_filepath: str,
    *,
    function_name: str | None = None,
    url: str | None = None,
    description: str = "",
    method: str | None = None,
    service_package: str | None = None,
    param_remarks: dict[str, Any] | None = None,
    param_values: dict[str, list[Any]] | None = None,
    time_pairs: dict[str, dict[str, str]] | None = None,
    source: str | None = None,
    params: Any = None,
    data: Any = None,
    files: Any = None,
    headers: dict[str, Any] | None = None,
    constant_params: dict[str, Any] | None = None,
    har_param_values: dict[str, list[Any]] | None = None,
    har_params: dict[str, Any] | None = None,
    har_time_pairs: dict[str, dict[str, str]] | None = None,
) -> str | None:
    """为生成的 API 模块写入 API 元数据文件。

    除 url/描述/备注等规范字段外，一并写入生成时的 params/data/files/headers
    **当前值**快照（与写入 .py 模块级赋值的一致）；下游读取只依赖这份元数据，
    缺失或没有 API 元数据时 parse_api_file 会报错提示补充。

    任何规范字段缺失/为空时该字段从结果中剔除，避免把生成器内部默认值
    （如 "TODO: 添加接口描述"）误当成规范数据。
    """
    payload: dict[str, Any] = {}
    if source:
        payload["source"] = source
    # 规范字段：跳过 None 和空字符串
    safe_values = {
        "function_name": function_name,
        "url": url,
        "description": description,
        "method": method,
        "service_package": service_package,
    }
    for key, value in safe_values.items():
        if value is None or value == "":
            continue
        payload[key] = value
    if param_remarks:
        payload["param_remarks"] = dict(param_remarks)
    if param_values:
        payload["param_values"] = dict(param_values)
    if time_pairs:
        payload["time_pairs"] = dict(time_pairs)
    if constant_params:
        payload[CONSTANT_PARAMS_FIELD] = dict(constant_params)
    if har_param_values:
        payload[HAR_PARAM_VALUES_FIELD] = dict(har_param_values)
    if har_params:
        payload[HAR_PARAMS_FIELD] = dict(har_params)
    if har_time_pairs:
        payload[HAR_TIME_PAIRS_FIELD] = dict(har_time_pairs)
    # 当前值字段：只跳过 None（允许空字典/空列表）
    current_values = {
        "params": params,
        "data": data,
        "files": files,
        "headers": headers,
    }
    for key, value in current_values.items():
        if value is None:
            continue
        payload[key] = value

    meta_file = metadata_path(py_filepath)
    try:
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return meta_file
    except OSError:
        return None


def read_api_metadata(py_filepath: str) -> dict[str, Any] | None:
    """读取 API 元数据；文件缺失或损坏时返回 None（调用方据此报错提示补充）。"""
    meta_file = metadata_path(py_filepath)
    if not os.path.isfile(meta_file):
        return None
    try:
        with open(meta_file, encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    return payload
