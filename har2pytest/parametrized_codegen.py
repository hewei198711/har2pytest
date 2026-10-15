"""参数化/列表查询模式代码生成辅助函数。

提供生成 pytest 测试用例代码片段的纯函数：导入语句、描述、list_query_data
类属性、test_0 收集用例、参数化测试方法、装饰器、方法体、断言等。

所有函数通过 ``render_ctx`` 字典接收 async_mode 相关的预计算常量
（def_prefix / body_indent / status_attr / json_call / with_keyword / async_mode），
避免依赖 TestCaseGenerator 实例。
"""

from __future__ import annotations

import os
from typing import Any

from .codegen import render_lines
from .config import APIConfig
from .time_pair import TimePairContext
from .utils import (
    extract_service_package,
    format_parameter_value,
    header_value_formatter,
    parse_api_file,
    sanitize_param_name,
    sanitize_remark,
)

# ==================== render_ctx 构建 ====================


def build_render_ctx(async_mode: bool, api_dir: str) -> dict[str, Any]:
    """构建模板渲染上下文字典。

    Args:
        async_mode: 是否为异步模式
        api_dir: API 文件目录路径（用于推导 import 前缀包名）

    Returns:
        包含 def_prefix / body_indent / status_attr / json_call /
        with_keyword / async_mode / api_dir 的字典
    """
    return {
        "def_prefix": "    async def " if async_mode else "    def ",
        "body_indent": "        ",
        "status_attr": "status" if async_mode else "status_code",
        "json_call": "await r.json()" if async_mode else "r.json()",
        "with_keyword": "async with" if async_mode else "with",
        "async_mode": async_mode,
        "api_dir": api_dir,
    }


# ==================== datetime 导入辅助 ====================


def insert_datetime_import(content: list[str]) -> None:
    """在 ``import os`` 后插入 ``from datetime import datetime``。

    统一 batch/HAR 两条路径的 datetime 导入逻辑，避免重复代码。

    Args:
        content: 已生成的代码行列表（就地修改）
    """
    os_import_idx = next(
        (i for i, line in enumerate(content) if line == "import os"), 0
    )
    content.insert(os_import_idx + 1, "from datetime import datetime")


# ==================== 导入与描述 ====================


def gen_test_case_imports(
    render_ctx: dict[str, Any],
    api_files: list[str] | None = None,
    service_package: str | None = None,
    function_name: str | None = None,
    task_id: str | None = None,
    is_list_query: bool = False,
) -> list[str]:
    """生成测试用例的导入部分。

    Args:
        render_ctx: 模板渲染上下文
        api_files: API 文件路径列表（用于多函数导入）
        service_package: 服务包名称（用于单函数导入）
        function_name: API 函数名称（用于单函数导入）
        task_id: 任务 ID
        is_list_query: 是否为 list_query 模式

    Returns:
        导入语句列表
    """
    content = [
        "import os",
        "",
    ]

    api_dir = render_ctx["api_dir"]
    async_mode = render_ctx["async_mode"]
    base_pkg = os.path.basename(api_dir) or APIConfig.DEFAULT_API_DIR()

    content.extend(
        [
            "import pytest",
            "import allure",
            "from allure_commons.types import Severity",
            "",
        ]
    )

    if async_mode:
        content.extend(
            [
                "from har2pytest.client import client, async_client",
                "client.set_client(async_client)",
                "",
            ]
        )

    if api_files:
        service_imports: dict[str | None, list[str]] = {}
        for api_file in api_files:
            result = parse_api_file(api_file)
            func_name = result.function_name
            if func_name:
                pkg = extract_service_package(api_file, api_dir)
                if pkg not in service_imports:
                    service_imports[pkg] = []
                service_imports[pkg].append(func_name)

        for pkg, functions in service_imports.items():
            if pkg is None:
                for func in functions:
                    content.append(f"from {base_pkg} import {func}")
                    content.append("")
            elif len(functions) > 1:
                content.append(f"from {base_pkg}.{pkg} import (")
                for func in functions:
                    content.append(f"    {func},")
                content.append(")")
                content.append("")
            else:
                content.append(f"from {base_pkg}.{pkg} import {functions[0]}")
                content.append("")
    elif function_name:
        if service_package is not None and service_package.isidentifier():
            content.append(f"from {base_pkg}.{service_package} import {function_name}")
        else:
            content.append(f"from {base_pkg} import {function_name}")
        content.append("")

    if task_id:
        content.append(f"@pytest.mark.{task_id}")

    if is_list_query:
        content.append("@pytest.mark.test_list_query")

    return content


def gen_allure_description(
    api_url: str,
    api_description: str = "",
    param_remarks: dict[str, Any] | None = None,
) -> str:
    """生成 @allure.description 装饰器代码行。

    Args:
        api_url: 接口地址
        api_description: 接口名称/描述
        param_remarks: 参数备注字典

    Returns:
        单行 @allure.description(...) 代码字符串
    """
    desc_lines = [f"接口说明：\n- 接口名称：{api_description}", f"- 接口地址：{api_url}"]
    if param_remarks:
        desc_lines.append("")
        desc_lines.append("主要参数说明：")
        for param_name, remark in param_remarks.items():
            desc_lines.append(f"- {param_name}：{sanitize_remark(remark) or '# TODO 请填写参数备注'}")
    return f'@allure.description("""{chr(10).join(desc_lines)}""")'


def gen_test_case_description(
    render_ctx: dict[str, Any],
    api_url: str,
    service_package: str,
    severity: str = "NORMAL",
    api_description: str = "",
    param_remarks: dict[str, Any] | None = None,
    api_headers: dict[str, Any] | None = None,
) -> list[str]:
    """生成测试用例的描述部分。

    Args:
        render_ctx: 模板渲染上下文
        api_url: API URL
        service_package: 服务包名称
        severity: 测试用例严重级别
        api_description: 接口名称/描述
        param_remarks: 参数备注字典
        api_headers: API 文件中的 headers 字典

    Returns:
        描述语句列表
    """
    description = ""
    if api_description:
        description = gen_allure_description(api_url, api_description, param_remarks)
    header_items = []
    if api_headers:
        header_items = [(key, header_value_formatter(value)) for key, value in api_headers.items()]

    content = render_lines(
        "tc_description.j2",
        severity=severity,
        service_package=service_package,
        api_url=api_url,
        api_description=description,
        header_items=header_items,
    )
    if not content or content[-1] != "":
        content.append("")
    return content


# ==================== list_query_data + test_0 收集 ====================


def gen_list_query_data_class_attr(
    api_params: dict[str, Any],
    param_values: dict[str, list[Any]],
    tp_ctx: TimePairContext,
) -> list[str]:
    """生成 list_query_data 类属性。

    分页参数从配置获取默认值。时间对参数用 datetime 动态计算：
    start 取当年1月1日，end 取当前时间。

    Args:
        api_params: API 文件中的所有参数
        param_values: 参数枚举值字典
        tp_ctx: 时间对统一上下文

    Returns:
        list_query_data 类属性代码行列表
    """
    data_items: list[tuple[str, str]] = []

    for param_name, param_value in api_params.items():
        if APIConfig.is_pagination_param(param_name):
            pagination_default = APIConfig.get_pagination_default_value(param_name)
            if pagination_default is not None:
                data_items.append((param_name, str(pagination_default)))
            continue

        if param_name in tp_ctx.param_role:
            role, fmt = tp_ctx.param_role[param_name]
            if role == "start":
                data_items.append((
                    param_name,
                    f'datetime(datetime.now().year, 1, 1).strftime("{fmt}")',
                ))
            else:
                data_items.append((
                    param_name,
                    f'datetime.now().strftime("{fmt}")',
                ))
            continue

        if param_name in param_values and param_values[param_name]:
            values = param_values[param_name]
            # 单值参数解包为纯值，多值参数保持列表
            rendered = repr(values[0]) if len(values) == 1 else repr(values)
            data_items.append((param_name, rendered))
            continue

        data_items.append((param_name, format_parameter_value(param_value)))

    return render_lines("p_list_query_data.j2", data_items=data_items)


def gen_test_0_collect_response_data(
    render_ctx: dict[str, Any],
    api_description: str,
    function_name: str,
    param_var_name: str,
    api_params: dict[str, Any],
) -> list[str]:
    """生成 test_0 "获取响应数据" 用例。

    发送默认查询（参数值已由调用方覆盖 constant_params），遍历响应收集字段值到
    list_query_data。分页参数优先使用传入的实际值（含 constant_params 覆盖值），
    缺失时回退配置默认值；时间参数直接使用 api_params 中的 Swagger 默认值（如 ""），
    datetime 表达式仅由 list_query_data 类属性提供，不注入 test_0 的 params 字典。

    Args:
        render_ctx: 模板渲染上下文
        api_description: API 描述信息
        function_name: API 函数名称
        param_var_name: 调用参数名（data 或 params）
        api_params: API 文件中的所有参数（已含 constant_params 覆盖值）

    Returns:
        test_0 用例代码行列表
    """
    data_items: list[tuple[str, str]] = []
    for param_name, param_value in api_params.items():
        if APIConfig.is_pagination_param(param_name):
            # 已有实际值（含 constant_params 覆盖值）时直接使用，
            # 否则回退配置默认值，保证与参数化方法体取值一致
            if param_value not in (None, ""):
                data_items.append((param_name, format_parameter_value(param_value)))
            else:
                pagination_default = APIConfig.get_pagination_default_value(param_name)
                if pagination_default is not None:
                    data_items.append((param_name, str(pagination_default)))
            continue
        data_items.append((param_name, format_parameter_value(param_value)))

    return render_lines(
        "p_test_0_collect.j2",
        api_description=sanitize_remark(api_description),
        def_prefix=render_ctx["def_prefix"],
        function_name=function_name,
        body_indent=render_ctx["body_indent"],
        param_var_name=param_var_name,
        data_items=data_items,
        status_attr=render_ctx["status_attr"],
        json_call=render_ctx["json_call"],
        with_keyword=render_ctx["with_keyword"],
    )


# ==================== batch 模式参数化测试方法 ====================


def gen_batch_parametrized_test_methods(
    render_ctx: dict[str, Any],
    param_items: list[dict[str, Any]],
    api_description: str,
    function_name: str,
    param_var_name: str,
    param_values: dict[str, list[Any]],
    param_remarks: dict[str, Any] | None = None,
    time_pair_ctx: TimePairContext | None = None,
) -> list[str]:
    """生成 batch 模式下的参数化测试方法。

    枚举参数用 parametrize，非枚举参数用运行时取值（从 list_query_data）。
    时间对参数合并为单个测试方法，同时传 start 和 end 参数。

    Args:
        render_ctx: 模板渲染上下文
        param_items: 参数化数据列表
        api_description: API 描述信息
        function_name: API 函数名称
        param_var_name: 调用参数名（data 或 params）
        param_values: 参数枚举值字典
        param_remarks: 参数备注字典（可选）
        time_pair_ctx: 时间对统一上下文（可选）

    Returns:
        测试方法代码行列表
    """
    content: list[str] = []
    tp_ctx = time_pair_ctx or TimePairContext()
    remarks = param_remarks or {}
    idx = 1

    for item in param_items:
        param_name = item["param_name"]
        if param_name in tp_ctx.end_names:
            continue

        other_params = item["other_params"]
        is_enum_param = param_name in param_values and bool(param_values[param_name])
        is_time_pair_start = param_name in tp_ctx.start_to_end

        if is_time_pair_start:
            end_param = tp_ctx.start_to_end[param_name]
            tp_data_items: list[tuple[str, str]] = []
            for k, v in other_params.items():
                if k == end_param:
                    continue
                tp_data_items.append((k, format_parameter_value(v)))
            tp_data_items.insert(0, (param_name, f'self.list_query_data["{param_name}"]'))
            tp_data_items.insert(1, (end_param, f'self.list_query_data["{end_param}"]'))

            start_title = sanitize_remark(remarks.get(param_name, param_name))
            end_title = sanitize_remark(remarks.get(end_param, end_param))
            if " " in start_title:
                start_title = start_title.split(" ")[0]
            if " " in end_title:
                end_title = end_title.split(" ")[0]
            combined_title = f"{start_title}-{end_title}"

            content.extend(
                render_lines(
                    "p_runtime_value_method.j2",
                    api_description=sanitize_remark(api_description),
                    title_param=combined_title,
                    def_prefix=render_ctx["def_prefix"],
                    idx=idx,
                    function_name=function_name,
                    body_indent=render_ctx["body_indent"],
                    param_var_name=param_var_name,
                    data_items=tp_data_items,
                    status_attr=render_ctx["status_attr"],
                    json_call=render_ctx["json_call"],
                    search_enabled=False,
                    param_name=param_name,
                    param_name_lower=param_name.lower(),
                    verify_assert="",
                    with_keyword=render_ctx["with_keyword"],
                )
            )

        elif is_enum_param:
            # 组合参数判定依据值的嵌套结构（首元素为 list/tuple），而非仅凭键名含逗号
            is_combo = "," in param_name and isinstance(param_values[param_name][0], (list, tuple))
            if is_combo:
                # 组合参数：拆分参数名并生成静态参数化列表（list_query_data 无组合键，
                # 不可运行时引用），other_params 排除子参数避免重复键覆盖参数化值
                content.extend(
                    gen_parametrize_decorator(param_name, param_values[param_name], is_combination=True)
                )
                combo_names = {n.strip() for n in param_name.split(",")}
                other_params = {k: v for k, v in other_params.items() if k not in combo_names}
            else:
                content.append(
                    f'    @pytest.mark.parametrize("{sanitize_param_name(param_name)}", list_query_data["{param_name}"])'
                )
            content.extend(
                gen_test_method_definition(
                    render_ctx, api_description, param_name, remarks, function_name, idx, is_combination=is_combo
                )
            )
            content.extend(
                gen_test_method_body(
                    render_ctx, param_var_name, param_name, other_params, is_combination=is_combo
                )
            )
            content.extend(
                gen_test_method_assertions(render_ctx, function_name, param_var_name, param_name)
            )
        else:
            data_items: list[tuple[str, str]] = []
            for k, v in other_params.items():
                data_items.append((k, format_parameter_value(v)))
            data_items.insert(0, (param_name, f'self.list_query_data["{param_name}"]'))

            title_param = sanitize_remark(remarks.get(param_name, param_name))
            if " " in title_param:
                title_param = title_param.split(" ")[0]

            search_enabled = "," not in param_name
            verify_assert = ""
            if search_enabled:
                verify_assert = (
                    f'assert v is None or str(v) == str(self.list_query_data["{param_name}"]), '
                    f"f'字段 {{k}} 值 {{v}} 与搜索条件 {param_name}={{self.list_query_data[\"{param_name}\"]}} 不一致'"
                )

            content.extend(
                render_lines(
                    "p_runtime_value_method.j2",
                    api_description=sanitize_remark(api_description),
                    title_param=title_param,
                    def_prefix=render_ctx["def_prefix"],
                    idx=idx,
                    function_name=function_name,
                    body_indent=render_ctx["body_indent"],
                    param_var_name=param_var_name,
                    data_items=data_items,
                    status_attr=render_ctx["status_attr"],
                    json_call=render_ctx["json_call"],
                    search_enabled=search_enabled,
                    param_name=param_name,
                    param_name_lower=param_name.lower(),
                    verify_assert=verify_assert,
                    with_keyword=render_ctx["with_keyword"],
                )
            )

        idx += 1

    return content


# ==================== 参数化测试辅助方法 ====================


def gen_parametrize_decorator(
    param_name: str, param_values: list[Any], is_combination: bool
) -> list[str]:
    """生成 @pytest.mark.parametrize 装饰器。"""
    parametrize_values = gen_parametrize_values(param_values, is_combination)

    if is_combination:
        safe_names = [sanitize_param_name(n.strip()) for n in param_name.split(",")]
        arg_names = ", ".join(safe_names)
    else:
        arg_names = sanitize_param_name(param_name)
    return render_lines(
        "p_parametrize_decorator.j2",
        arg_names=arg_names,
        values=parametrize_values,
    )


def gen_parametrize_values(param_values: list[Any], is_combination: bool) -> list[str]:
    """生成参数化值列表。"""
    parametrize_values: list[str] = []
    if is_combination:
        for value_tuple in param_values:
            formatted_values = [format_parameter_value(v) for v in value_tuple]
            parametrize_values.append(f"({', '.join(formatted_values)})")
    else:
        for value in param_values:
            formatted_value = format_parameter_value(value)
            parametrize_values.append(formatted_value)
    return parametrize_values


def gen_test_method_definition(
    render_ctx: dict[str, Any],
    api_description: str,
    param_name: str,
    param_remarks: dict[str, Any],
    function_name: str,
    param_count: int,
    is_combination: bool,
) -> list[str]:
    """生成参数化测试方法定义（标题 + def 行）。"""
    if is_combination:
        param_names = param_name.split(",")
        safe_names = [sanitize_param_name(p) for p in param_names]
        param_descriptions = []
        for p in param_names:
            desc = sanitize_remark(param_remarks.get(p, p))
            if "-" in desc:
                desc = desc.split("-")[0]
            param_descriptions.append(desc)
        title_param = "-".join(param_descriptions)
    else:
        safe_names = [sanitize_param_name(param_name)]
        title_param = sanitize_remark(param_remarks.get(param_name, param_name))
        if " " in title_param:
            title_param = title_param.split(" ")[0]

    return render_lines(
        "p_test_method_definition.j2",
        api_description=sanitize_remark(api_description),
        title_param=title_param,
        def_prefix=render_ctx["def_prefix"],
        function_name=function_name,
        idx=param_count,
        safe_names=safe_names,
    )


def gen_test_method_body(
    render_ctx: dict[str, Any],
    param_var_name: str,
    param_name: str,
    other_params: dict[str, Any],
    is_combination: bool,
) -> list[str]:
    """生成测试方法体。"""
    ctx = build_param_dict_context(param_name, other_params, is_combination)
    body_lines = render_lines(
        "p_method_body.j2",
        leading_blank=False,
        param_var_name=param_var_name,
        **ctx,
    )
    return ["", *body_lines]


def build_param_dict_context(
    param_name: str, other_params: dict[str, Any], is_combination: bool
) -> dict[str, Any]:
    """构建参数化数据字典模板的渲染上下文。"""
    if is_combination:
        param_pairs = [(key, sanitize_param_name(key)) for key in param_name.split(",")]
        combo_ctx: dict[str, Any] = {"param_pairs": param_pairs}
    else:
        combo_ctx = {"param_name": param_name, "param_safe": sanitize_param_name(param_name)}
    other_items = [(key, repr(value) if isinstance(value, str) else str(value)) for key, value in other_params.items()]
    return {
        "is_combination": is_combination,
        "other_items": other_items,
        **combo_ctx,
    }


def gen_test_method_assertions(
    render_ctx: dict[str, Any],
    function_name: str,
    param_var_name: str,
    param_name: str = "",
) -> list[str]:
    """生成测试方法断言部分。"""
    search_enabled = bool(param_name) and not APIConfig.is_time_param(param_name) and "," not in param_name
    safe_name = sanitize_param_name(param_name) if param_name else ""
    verify_assert = ""
    if search_enabled:
        verify_assert = (
            f"assert v is None or str(v) == str({safe_name}), "
            f"f'字段 {{k}} 值 {{v}} 与搜索条件 {safe_name}={{{safe_name}}} 不一致'"
        )
    content = render_lines(
        "p_test_method_assertions.j2",
        async_mode=render_ctx["async_mode"],
        function_name=function_name,
        param_var_name=param_var_name,
        search_enabled=search_enabled,
        search_param=param_name.lower() if search_enabled else "",
        verify_assert=verify_assert,
    )
    content.append("")
    return content
