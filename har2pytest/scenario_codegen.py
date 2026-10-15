"""complex_scenario 模式代码生成。

提供复杂场景测试用例的代码生成函数：请求源获取、步骤函数名/体生成、
headers 差异对比、步骤断言等。

所有函数通过 ``render_ctx`` 字典接收 async_mode 相关的预计算常量，
避免依赖 TestCaseGenerator 实例。
"""

from __future__ import annotations

import os
from typing import Any

from .codegen import render_lines
from .logger import logger
from .models import APIFileInfo, ParsedRequestInfo
from .url_matcher import URLMatcher
from .utils import (
    extract_service_package,
    format_parameter_value,
    format_params_for_python,
    header_value_formatter,
    parse_api_file,
    sanitize_remark,
)

# ==================== 请求与信息提取 ====================


def get_requests_from_source(
    har_file_path: str | None,
    api_files: list[str],
    target_api_file: str | None,
    har_parser: Any = None,
    filter_duplicate_url: bool = False,
) -> list[ParsedRequestInfo]:
    """从 HAR 文件或 API 文件获取请求信息。

    优先从 HAR 文件获取，如果 HAR 文件不存在或为空，则从 API 文件构建请求信息。

    Args:
        har_file_path: HAR 文件路径
        api_files: API 文件路径列表
        target_api_file: 目标 API 文件路径
        har_parser: HARParser 实例（可选）
        filter_duplicate_url: 是否过滤重复 URL

    Returns:
        请求信息列表
    """
    if har_file_path and os.path.exists(har_file_path) and har_parser is not None:
        return har_parser.extract_requests_from_har(har_file_path, filter_duplicate_url)

    requests: list[ParsedRequestInfo] = []
    if target_api_file and os.path.exists(target_api_file):
        api_info = parse_api_file(target_api_file)
        if api_info:
            if not api_info.url:
                logger.error(
                    f"API文件 {target_api_file} 元数据缺少 url 字段，跳过构建模拟请求"
                )
                return requests
            request_info = ParsedRequestInfo(
                url=api_info.url,
                method="GET",
                query_params=api_info.params,
                post_data=api_info.data,
                headers=api_info.headers,
            )
            requests.append(request_info)

    return requests


def extract_api_info_for_scenario(
    target_api_file: str | None,
    api_dir: str,
) -> tuple[str | None, str]:
    """从 API 文件提取接口信息（场景模式专用）。

    Args:
        target_api_file: 目标 API 文件路径
        api_dir: API 文件目录路径

    Returns:
        (feature_name, story_name) 元组
    """
    feature_name = ""
    story_name = ""

    if target_api_file:
        feature_name = extract_service_package(target_api_file, api_dir)
        if feature_name is None:
            feature_name = "TODO 未找到对应信息，请检查！"

        result = parse_api_file(target_api_file)
        api_url = result.url
        if api_url:
            story_name = api_url

    return feature_name, story_name


# ==================== 场景测试方法定义 ====================


def gen_scenario_test_method_definition(
    render_ctx: dict[str, Any],
    target_api_file: str,
) -> list[str]:
    """生成场景测试方法定义。

    Args:
        render_ctx: 模板渲染上下文
        target_api_file: 目标 API 文件路径

    Returns:
        测试方法定义代码行列表
    """
    api_info = parse_api_file(target_api_file)
    if not api_info.function_name:
        logger.error(f"API文件 {target_api_file} 缺少 function_name，无法生成步骤方法")
        return []
    api_description = api_info.description or api_info.function_name

    return render_lines(
        "s_test_method_definition.j2",
        title=sanitize_remark(api_description),
        def_prefix=render_ctx["def_prefix"],
        function_name=api_info.function_name,
    )


# ==================== 步骤函数生成 ====================


def gen_scenario_step_functions(
    render_ctx: dict[str, Any],
    content: list[str],
    requests: list[ParsedRequestInfo],
    api_files: list[str],
    class_headers: dict[str, Any] | None = None,
) -> list[str]:
    """生成场景测试步骤函数。

    Args:
        render_ctx: 模板渲染上下文
        content: 内容列表（会被修改）
        requests: 请求信息列表
        api_files: API 文件路径列表
        class_headers: 类级别 headers

    Returns:
        步骤函数名称列表
    """
    step_functions: list[str] = []
    name_counters: dict[str, int] = {}

    for i, request_info in enumerate(requests):
        url = request_info.url
        matched_api_file = URLMatcher.find_matching_api_file(url, api_files)

        if matched_api_file:
            api_info = parse_api_file(matched_api_file)
            api_function_name = api_info.function_name or ""
            api_description = api_info.description
            step_name = gen_step_function_name(api_function_name, name_counters)
            step_functions.append(step_name)

            step_prefix = "        async def " if render_ctx["async_mode"] else "        def "
            content.extend(
                render_lines(
                    "s_step_heading.j2",
                    step_description=api_description or "",
                    step_prefix=step_prefix,
                    step_name=step_name,
                )
            )

            gen_step_function_body(
                render_ctx, content, api_function_name, api_info, request_info, class_headers
            )

            content.extend(
                render_lines(
                    "s_step_asserts.j2",
                    status_attr=f"r.{render_ctx['status_attr']}",
                    json_call=render_ctx["json_call"],
                )
            )

    return step_functions


def gen_step_function_name(api_function_name: str, name_counters: dict[str, int]) -> str:
    """生成步骤函数名称。"""
    if api_function_name not in name_counters:
        name_counters[api_function_name] = 0

    count = name_counters[api_function_name]

    if count == 0:
        step_name = f"step_{api_function_name}"
    else:
        step_name = f"step_{count}_{api_function_name}"

    name_counters[api_function_name] += 1
    return step_name


def gen_step_function_body(
    render_ctx: dict[str, Any],
    content: list[str],
    api_function_name: str,
    api_info: APIFileInfo,
    request_info: ParsedRequestInfo | None = None,
    class_headers: dict[str, Any] | None = None,
) -> None:
    """生成步骤函数体。

    Args:
        render_ctx: 模板渲染上下文
        content: 内容列表（会被修改）
        api_function_name: API 函数名称
        api_info: API 文件信息
        request_info: 解析后的请求信息（来自 HAR 文件，可选）
        class_headers: 类级别 headers
    """
    api_files = api_info.files
    api_data = api_info.data
    api_params = api_info.params

    if request_info:
        har_query = request_info.query_params or {}
        har_post = request_info.post_data or {}
        if isinstance(har_post, list):
            har_values = har_post if har_post else {}
        else:
            har_values = {**har_post, **har_query} if (har_post or har_query) else {}
    else:
        har_values = {}

    is_file_upload = bool(api_files)
    ctx = render_ctx["with_keyword"]

    header_lines, headers_arg = build_step_headers_arg(api_info.headers, class_headers or {})
    if header_lines:
        content.extend(header_lines)

    if is_file_upload:
        har_values_dict = har_values if isinstance(har_values, dict) else {}
        actual_values = {**api_files, **har_values_dict} if har_values_dict else api_files
        files_str = format_params_for_python(actual_values, indent=16)
        content.extend(
            render_lines(
                "s_step_upload.j2",
                files_code=files_str,
                ctx=ctx,
                function_name=api_function_name,
                headers_arg=headers_arg,
            )
        )
    elif api_data:
        if isinstance(api_data, dict) and isinstance(har_values, dict):
            actual_values = {**api_data, **har_values} if har_values else api_data
            data_str = format_params_for_python(actual_values, indent=16)
        elif isinstance(har_values, list):
            data_str = format_parameter_value(har_values)
        else:
            data_str = format_parameter_value(api_data)
        content.extend(
            render_lines(
                "s_step_data.j2",
                data_code=data_str,
                ctx=ctx,
                function_name=api_function_name,
                headers_arg=headers_arg,
            )
        )
    elif api_params:
        har_values_dict = har_values if isinstance(har_values, dict) else {}
        actual_values = {**api_params, **har_values_dict} if har_values_dict else api_params
        params_str = format_params_for_python(actual_values, indent=16)
        content.extend(
            render_lines(
                "s_step_params.j2",
                params_code=params_str,
                ctx=ctx,
                function_name=api_function_name,
                headers_arg=headers_arg,
            )
        )
    else:
        content.extend(
            render_lines(
                "s_step_none.j2",
                ctx=ctx,
                function_name=api_function_name,
                headers_arg=headers_arg,
            )
        )


# ==================== headers 差异对比 ====================


def build_step_headers_arg(
    step_headers: dict[str, Any], class_headers: dict[str, Any] | None = None
) -> tuple[list[str], str]:
    """构建步骤调用的 headers 参数。

    Args:
        step_headers: 步骤对应 API 文件中的 headers 字典
        class_headers: 类级别 headers（差异对比基准）

    Returns:
        (额外的代码行列表, headers 参数字符串)
    """
    class_headers = class_headers or {}
    diff = {k: v for k, v in step_headers.items() if class_headers.get(k) != v}
    if not diff:
        return [], "headers=self.headers"

    if class_headers:
        diff_str = ", ".join(f'"{k}": {header_value_formatter(v)}' for k, v in diff.items())
        line = f"            headers = {{**self.headers, {diff_str}}}"
    else:
        diff_str = ", ".join(f'"{k}": {header_value_formatter(v)}' for k, v in step_headers.items())
        line = f"            headers = {{{diff_str}}}"
    return [line, ""], "headers=headers"
