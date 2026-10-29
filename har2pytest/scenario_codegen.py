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
from .config import APIConfig
from .logger import logger
from .models import APIFileInfo, ParsedRequestInfo
from .step_values import (
    StepValueContext,
    _path_segments,
    build_scenario_value_plan,
    collect_append_path,
    collect_file_field,
    find_collect_config,
    make_step_key,
    render_param_dict_code,
    render_test_data_init,
)
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
    if not (target_api_file and os.path.exists(target_api_file)):
        return requests
    api_info = parse_api_file(target_api_file)
    if not api_info:
        return requests
    if not api_info.url:
        logger.error(
            f"API文件 {target_api_file} 元数据缺少 url 字段，跳过构建模拟请求"
        )
        return requests
    requests.append(
        ParsedRequestInfo(
            url=api_info.url,
            method="GET",
            query_params=api_info.params,
            post_data=api_info.data,
            headers=api_info.headers,
        )
    )
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
) -> list[dict]:
    """生成场景测试步骤函数。

    先匹配 API 文件并分配步骤名，再分析步骤取值计划（哪些参数取前序
    步骤响应、哪些提升为用例级 test_data），最后生成各步骤函数。

    响应收集接口（COLLECT_RESPONSE_APIS 配置命中）的多次调用合并为一个
    带循环形参的步骤函数：每次调用响应片段追加进 test_data 收集列表，
    执行段以 for 循环逐文件调用。

    Args:
        render_ctx: 模板渲染上下文
        content: 内容列表（会被修改）
        requests: 请求信息列表
        api_files: API 文件路径列表
        class_headers: 类级别 headers

    Returns:
        执行条目列表（每项 {"name": 步骤函数名, "collect": 收集配置或 None}）
    """
    step_calls: list[dict] = []
    name_counters: dict[str, int] = {}
    track_enabled = APIConfig.TRACK_PARAM_SOURCES()

    # 第一遍：匹配 API 文件并分配步骤名（步骤名确定后才能构建取值计划）
    matched: list[tuple[str, APIFileInfo, ParsedRequestInfo]] = []
    step_keys: list[str] = []
    used_keys: set[str] = set()
    function_step_keys: dict[str, str] = {}  # API 函数名 → 步骤键（同一 API 多次调用复用同一键）
    collect_step_names: dict[str, str] = {}  # collect_key → 步骤名（同接口多次调用合并）
    for request_info in requests:
        matched_api_file = URLMatcher.find_matching_api_file(request_info.url, api_files)
        if not matched_api_file:
            # 静默跳过会让产物少步骤，这里必须告知原因（常见：缺 API 文件或缺同名 .api.json 元数据）
            logger.warning(
                f"HAR 请求未匹配到可用的 API 文件，步骤已跳过: {request_info.method} {request_info.url}；"
                "若对应 API 文件已存在，请确认其同名 .api.json 元数据齐全"
                "（可用 har2pytest api <har> --overwrite 重新生成）"
            )
            continue
        api_info = parse_api_file(matched_api_file)
        # 从 API 文件 URL 模板提取路径参数（如 /orderInfo/{orderNo} → orderNo），
        # 使取值分析能把第一个步骤的路径参数提升为用例级 test_data 值
        if api_info.url:
            _, path_params = URLMatcher.match_url_pattern(request_info.url, api_info.url)
            if path_params:
                request_info.path_params = path_params
        collect_cfg = find_collect_config(request_info.url) if track_enabled else None
        if collect_cfg is not None and collect_cfg["collect_key"] in collect_step_names:
            # 同接口再次调用：复用步骤名，不新增执行条目（循环体逐文件执行）
            step_name = collect_step_names[collect_cfg["collect_key"]]
        else:
            step_name = gen_step_function_name(api_info.function_name or "", name_counters)
            if collect_cfg is not None:
                collect_step_names[collect_cfg["collect_key"]] = step_name
            step_calls.append({"name": step_name, "collect": collect_cfg})
        # 同一 API 函数多次调用时复用同一键，不同 API 函数间保证键唯一
        func_name = api_info.function_name or ""
        if func_name in function_step_keys:
            step_keys.append(function_step_keys[func_name])
        else:
            key = make_step_key(func_name, used_keys)
            function_step_keys[func_name] = key
            step_keys.append(key)
        matched.append((step_name, api_info, request_info))

    # 分析步骤取值计划，并在第一个步骤函数前插入 test_data 初始化
    value_plan = build_scenario_value_plan(
        [item[2] for item in matched], step_keys
    )
    if track_enabled:
        content.extend(render_test_data_init(value_plan, indent=8))

    # JSON 字符串子集投影的产物需要 json.dumps 重组渲染，头部补充 import json
    if any(
        src.kind == "json_projection"
        for step_ctx in value_plan.steps
        for src in step_ctx.param_sources.values()
    ):
        os_import_idx = next(
            (i for i, line in enumerate(content) if line == "import os"), 0
        )
        content.insert(os_import_idx + 1, "import json")

    # 步骤函数是测试方法内的嵌套函数，比方法定义多一级缩进
    step_prefix = "    " + render_ctx["def_prefix"]

    # 第二遍：生成步骤函数（heading + 函数体 + 断言与响应存储）；
    # 响应收集接口的重复调用只渲染一次函数定义（循环执行）
    rendered_collect: set[str] = set()
    for (step_name, api_info, request_info), step_ctx in zip(matched, value_plan.steps):
        collect_cfg = step_ctx.collect
        if collect_cfg is not None:
            collect_key = collect_cfg["collect_key"]
            if collect_key in rendered_collect:
                continue
            rendered_collect.add(collect_key)
        api_function_name = api_info.function_name or ""
        # 响应收集接口的步骤函数带文件形参（执行段 for 循环逐文件传入）
        if collect_cfg is not None:
            step_params = collect_file_field(collect_cfg)
        else:
            step_params = ""
        content.extend(
            render_lines(
                "s_step_heading.j2",
                step_description=api_info.description or "",
                step_prefix=step_prefix,
                step_name=step_name,
                step_params=step_params,
            )
        )

        gen_step_function_body(
            render_ctx, content, api_function_name, api_info, request_info,
            class_headers, value_ctx=step_ctx, collect_cfg=collect_cfg,
        )

        if collect_cfg is not None:
            # 响应收集接口：断言后把响应片段追加进 test_data 收集列表
            append_path = collect_append_path(collect_cfg)
            store_line = f"test_data[{collect_key!r}].append(data{_path_segments(tuple(append_path))})"
            code_assert = False
        else:
            # 断言后存储本步骤响应供后续步骤引用；未被引用的响应不存储
            # （避免无用响应常驻 test_data），关闭取值跟踪时保持旧输出
            if track_enabled and step_ctx.store_response:
                store_line = f"test_data[{step_ctx.step_key!r}] = data['data']"
            else:
                store_line = ""
            code_assert = True
        content.extend(
            render_lines(
                "s_step_asserts.j2",
                status_attr=f"r.{render_ctx['status_attr']}",
                json_call=render_ctx["json_call"],
                code_assert=code_assert,
                step_store_line=store_line,
            )
        )

    return step_calls


def gen_step_function_name(api_function_name: str, name_counters: dict[str, int]) -> str:
    """生成步骤函数名称（同一 API 函数第二次起加计数前缀）。"""
    count = name_counters.get(api_function_name, 0)
    name_counters[api_function_name] = count + 1
    if count == 0:
        return f"step_{api_function_name}"
    return f"step_{count}_{api_function_name}"


def _format_step_payload(
    actual_values: dict[str, Any],
    value_ctx: StepValueContext | None,
) -> str:
    """渲染步骤参数字典：有取值来源时按 test_data 引用渲染，否则普通格式化。"""
    if value_ctx is not None and value_ctx.param_sources:
        return render_param_dict_code(actual_values, value_ctx.param_sources, indent=16)
    return format_params_for_python(actual_values, indent=16)


def gen_step_function_body(
    render_ctx: dict[str, Any],
    content: list[str],
    api_function_name: str,
    api_info: APIFileInfo,
    request_info: ParsedRequestInfo | None = None,
    class_headers: dict[str, Any] | None = None,
    value_ctx: StepValueContext | None = None,
    collect_cfg: dict | None = None,
) -> None:
    """生成步骤函数体。

    Args:
        render_ctx: 模板渲染上下文
        content: 内容列表（会被修改）
        api_function_name: API 函数名称
        api_info: API 文件信息
        request_info: 解析后的请求信息（来自 HAR 文件，可选）
        class_headers: 类级别 headers
        value_ctx: 步骤取值上下文（有取值来源时参数改用 test_data 引用）
        collect_cfg: 响应收集配置（命中 COLLECT_RESPONSE_APIS 时非 None，
            文件字段渲染为循环形参引用，其余表单字段仍按取值来源渲染）
    """
    api_files = api_info.files
    api_data = api_info.data
    api_params = api_info.params

    # HAR 实际请求参数（complex_scenario 以 HAR 键为准）：
    # 路径参数属 params 渠道（URL f-string 引用），query 并入 body 渠道避免丢失
    har_path: dict[str, Any]
    har_query: dict[str, Any]
    har_post: Any
    if request_info:
        har_path = request_info.path_params or {}
        har_query = request_info.query_params or {}
        har_post = request_info.post_data or {}
    else:
        har_path = {}
        har_query = {}
        har_post = {}

    header_lines, headers_arg = build_step_headers_arg(api_info.headers, class_headers or {})
    if header_lines:
        content.extend(header_lines)

    # 渠道由 API 文件声明决定（与 API 函数签名一致）；载荷键以 HAR 实际请求参数为准，
    # HAR 未传的 Swagger 声明键不渲染（仅 complex_scenario 传 request_info 时生效，
    # list_query/batch 等无 HAR 场景仍渲染 API 默认值）
    if api_files:
        # 文件上传：HAR 表单字段为准；HAR 无字段时回退 API 默认 files；
        # 与 data/params 渠道一致，应用取值来源（test_data 引用）渲染
        files_payload = api_files
        if request_info is not None and isinstance(har_post, dict) and har_post:
            files_payload = har_post
        if collect_cfg is not None:
            # 响应收集接口：文件字段改由循环形参提供
            # （执行段以 for file in test_data['files'] 逐文件调用），
            # 其余表单字段仍按取值来源渲染（如 test_data['storageType']）
            file_field = collect_file_field(collect_cfg)
            collect_files_payload = dict(files_payload)
            collect_files_payload.pop(file_field, None)
            files_str = render_param_dict_code(
                collect_files_payload,
                value_ctx.param_sources if value_ctx is not None else {},
                indent=16,
                extra_items={file_field: file_field},
            )
        else:
            files_str = _format_step_payload(files_payload, value_ctx)
        template, code_kwargs = "s_step_upload.j2", {"files_code": files_str}
    elif api_data:
        if isinstance(har_post, list):
            data_str = format_parameter_value(har_post)
        elif request_info is not None and isinstance(har_post, dict):
            # 以 HAR 键为准：body 与 query 合并（post 覆盖同名 query），
            # 空 body 渲染空字典而非 Swagger 默认值
            data_str = _format_step_payload({**har_query, **har_post}, value_ctx)
        else:
            data_str = format_parameter_value(api_data)
        template, code_kwargs = "s_step_data.j2", {"data_code": data_str}
    elif api_params:
        if request_info is not None:
            params_str = _format_step_payload({**har_path, **har_query}, value_ctx)
        else:
            params_str = _format_step_payload(api_params, value_ctx)
        template, code_kwargs = "s_step_params.j2", {"params_code": params_str}
    else:
        # API 文件未声明参数渠道：按 HAR 结构与请求方法推断渠道
        # （避免 HAR 录制参数因 api.json 无声明而被静默丢弃）
        if isinstance(har_post, list):
            data_str = format_parameter_value(har_post)
            template, code_kwargs = "s_step_data.j2", {"data_code": data_str}
        elif isinstance(har_post, dict) and har_post:
            data_str = _format_step_payload({**har_query, **har_post}, value_ctx)
            template, code_kwargs = "s_step_data.j2", {"data_code": data_str}
        elif har_query and request_info is not None and request_info.method != "GET":
            # POST 空 body 带 query：并入 data（与 API 生成侧渠道决策一致）
            data_str = _format_step_payload(har_query, value_ctx)
            template, code_kwargs = "s_step_data.j2", {"data_code": data_str}
        elif har_path or har_query:
            params_str = _format_step_payload({**har_path, **har_query}, value_ctx)
            template, code_kwargs = "s_step_params.j2", {"params_code": params_str}
        else:
            template, code_kwargs = "s_step_none.j2", {}

    content.extend(
        render_lines(
            template,
            ctx=render_ctx["with_keyword"],
            function_name=api_function_name,
            headers_arg=headers_arg,
            **code_kwargs,
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

    # 无类级别 headers 时输出本步骤全部 headers，否则只输出差异部分
    source = diff if class_headers else step_headers
    diff_str = ", ".join(f'"{k}": {header_value_formatter(v)}' for k, v in source.items())
    if class_headers:
        line = f"            headers = {{**self.headers, {diff_str}}}"
    else:
        line = f"            headers = {{{diff_str}}}"
    return [line, ""], "headers=headers"
