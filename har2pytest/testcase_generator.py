"""pytest 测试用例生成器。

提供 TestCaseGenerator 类，支持 list_query / complex_scenario / batch 三种
测试用例生成模式。具体代码生成逻辑委托给以下子模块：

- ``time_pair``: TimePairContext 时间对上下文数据类
- ``param_builder``: 参数化项构建与标准化
- ``parametrized_codegen``: 参数化/列表查询模式代码生成辅助
- ``scenario_codegen``: complex_scenario 模式代码生成
"""

from __future__ import annotations

import asyncio
import fnmatch
import os
import time
from typing import Any

from .codegen import validate_python
from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .models import ParsedRequestInfo
from .param_builder import (
    build_pagination_only_items,
    build_param_items_from_api,
)
from .parametrized_codegen import (
    build_render_ctx,
    gen_batch_parametrized_test_methods,
    gen_list_query_data_class_attr,
    gen_test_0_collect_response_data,
    gen_test_case_description,
    gen_test_case_imports,
    insert_datetime_import,
)
from .scenario_codegen import (
    extract_api_info_for_scenario,
    gen_scenario_step_functions,
    gen_scenario_test_method_definition,
    get_requests_from_source,
)
from .swagger_handler import SwaggerHandler
from .time_pair import TimePairContext
from .url_matcher import URLMatcher
from .utils import (
    format_directory,
    parse_api_file,
    write_test_file,
)


class TestCaseGenerator:
    """pytest 测试用例生成器类。

    Attributes:
        api_dir: API 文件目录路径
        output_dir: 测试用例输出目录路径
        filter_duplicate_url: 是否过滤重复 URL
        har_parser: HAR 文件解析器实例
        swagger_handler: Swagger 文档处理器实例
        url_matcher: URL 匹配器实例
    """

    def __init__(
        self,
        api_dir: str | None = None,
        output_dir: str | None = None,
        filter_duplicate_url: bool = False,
        base_urls: list[str] | None = None,
        kill_urls: list[str] | None = None,
        async_mode: bool = False,
    ):
        """初始化测试用例生成器。

        Args:
            api_dir: API 文件目录路径，默认为配置的默认目录
            output_dir: 测试用例输出目录路径，默认为配置的测试用例目录
            filter_duplicate_url: 是否过滤重复 URL，默认为 False
            base_urls: 基础 URL 列表，用于 HAR 解析时过滤
            kill_urls: 需要排除的 URL 列表
            async_mode: 是否生成异步模式测试代码（使用 async/await）
        """
        self.api_dir = api_dir or APIConfig.DEFAULT_API_DIR()
        self.output_dir = output_dir or APIConfig.TESTCASE_DIR()
        self.filter_duplicate_url = filter_duplicate_url
        self.async_mode = async_mode
        self.render_ctx = build_render_ctx(async_mode, self.api_dir)
        self.har_parser = HARParser(base_urls=base_urls, kill_urls=kill_urls)
        self.swagger_handler = SwaggerHandler()
        self.url_matcher = URLMatcher()

    # ==================== API 文件处理 ====================

    def _get_all_api_files(self) -> list[str]:
        """获取所有 API 文件路径。"""
        api_files = []
        if not os.path.exists(self.api_dir):
            logger.warning(f"API目录不存在: {self.api_dir}")
            return api_files

        for root, _, files in os.walk(self.api_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    api_files.append(os.path.join(root, file))
        return api_files

    def _is_within_api_dir(self, api_file: str) -> bool:
        """判断 API 文件是否位于 api_dir 目录下。"""
        try:
            rel_path = os.path.relpath(os.path.abspath(api_file), os.path.abspath(self.api_dir))
        except ValueError:
            return False
        return not rel_path.startswith(os.pardir)

    def _validate_api_dir(self, api_file: str) -> bool:
        """校验 API 文件位于 api_dir 目录下。"""
        if self._is_within_api_dir(api_file):
            return True
        logger.error(
            f"API 文件 {api_file} 不在 --api-dir({self.api_dir}) 目录下，无法推导 import 包名。"
            f"请用 --api-dir 指定实际的 API 目录后重试。"
        )
        return False

    # ==================== 测试模式决策 ====================

    @staticmethod
    def _profile_matches(profile_url: str, api_url: str) -> bool:
        """判断 profile.url 是否命中接口 URL。"""
        norm_profile = URLMatcher.normalize_url(profile_url)
        norm_url = URLMatcher.normalize_url(api_url)

        if norm_url == norm_profile:
            return True
        if "*" in norm_profile:
            if fnmatch.fnmatchcase(norm_url, norm_profile):
                return True
        matched, _ = URLMatcher.match_url_pattern(norm_url, norm_profile)
        if matched:
            return True
        matched, _ = URLMatcher.match_url_pattern(norm_profile, norm_url)
        return matched

    def _find_profile(self, api_url: str | None) -> dict | None:
        """返回命中该接口 URL 的 TESTCASE_PROFILES 条目。"""
        if not api_url:
            return None
        for profile in APIConfig.TESTCASE_PROFILES() or []:
            if isinstance(profile, dict) and profile.get("url") and self._profile_matches(str(profile["url"]), api_url):
                return profile
        return None

    def _resolve_testcase_mode(self, api_file: str) -> str:
        """决策单个接口的测试生成模式。"""
        api_info = parse_api_file(api_file)
        description = api_info.description or ""
        profile = self._find_profile(api_info.url)

        explicit = (profile or {}).get("mode", "auto")
        if explicit == "list_query":
            return "parametrized"
        if explicit == "complex_scenario":
            return "scenario"

        if profile is not None:
            keywords = profile.get("keywords")
            exclude_keywords = profile.get("exclude_keywords")
        else:
            keywords = exclude_keywords = None
        list_keywords = keywords if isinstance(keywords, list) else APIConfig.LIST_QUERY_KEYWORDS()
        exclude = (
            exclude_keywords if isinstance(exclude_keywords, list) else APIConfig.LIST_QUERY_EXCLUDE_KEYWORDS()
        )

        keywords_matched = bool(list_keywords) and any(kw in description for kw in list_keywords)
        is_list_query = keywords_matched
        if is_list_query and exclude and any(kw in description for kw in exclude):
            is_list_query = False
        # 关键字未匹配时，检查 API 是否携带参数（Swagger 或 HAR 捕获），
        # 有参数的接口默认走参数化路径，避免生成无参数的空壳场景用例。
        # 注意：仅在关键字完全未匹配时回退，不覆盖 exclude_keywords 的排除决定
        if not is_list_query and not keywords_matched:
            has_params = bool(api_info.params or api_info.data or api_info.har_params)
            if has_params:
                is_list_query = True
        return "parametrized" if is_list_query else "scenario"

    # ==================== Swagger/URL 匹配 ====================

    async def _get_swagger_doc_for_url(self, url: str) -> dict[str, Any] | None:
        """根据 URL 获取 Swagger 文档。"""
        service_package = APIConfig.determine_service_package(url)
        swagger_url = APIConfig.SWAGGER_DOC_URLS().get(service_package)
        if not swagger_url:
            return None
        return await self.swagger_handler.get_swagger_doc(swagger_url)

    async def _prepare_url_matcher(self, url: str) -> None:
        """为指定 URL 准备 URLMatcher。"""
        swagger_doc = await self._get_swagger_doc_for_url(url)
        self.url_matcher.swagger_data = swagger_doc

    async def match_api_files_for_har(
        self, har_file_path: str, requests: list[ParsedRequestInfo] | None = None
    ) -> list[str]:
        """根据 HAR 文件查找对应的 API 文件。"""
        if requests is None:
            requests = self.har_parser.extract_requests_from_har(har_file_path)

        request_url_map = {}
        for request in requests:
            request_url = request.url
            await self._prepare_url_matcher(request_url)
            url_info = self.url_matcher.get_url_info(request_url)
            request_url_map[request_url] = url_info["pattern"] or request_url

        api_files_list = self._get_all_api_files()

        matched_files = set()
        for url in request_url_map.keys():
            matched_file = URLMatcher.find_matching_api_file(url, api_files_list, request_url_map)
            if matched_file:
                matched_files.add(matched_file)

        return list(matched_files)

    # ==================== 测试用例生成入口方法 ====================

    async def generate_parametrized_list_testcases(
        self, har_file_path: str, task_id: str | None, target_url: str | None = None, overwrite: bool = False
    ) -> list[str]:
        """生成查询类参数化测试用例。"""
        if not os.path.exists(har_file_path):
            return []

        all_requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)
        api_files = await self.match_api_files_for_har(har_file_path, all_requests)
        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return []

        os.makedirs(self.output_dir, exist_ok=True)
        generated_files: list[str] = []

        for api_file in api_files:
            try:
                api_info = parse_api_file(api_file)
                if target_url and api_info.url != target_url:
                    continue
                if not api_info.function_name:
                    continue
                test_filename = f"test_{api_info.function_name}.py"
                test_filepath = os.path.join(self.output_dir, test_filename)
                if not overwrite and os.path.exists(test_filepath):
                    logger.info(f"跳过已存在的测试文件: {test_filepath}")
                    continue

                test_content = self.generate_parametrized_test_content(api_file, task_id)
                if not test_content:
                    test_content = self.generate_scenario_test_content(
                        har_file_path, [api_file], task_id, api_file, all_requests
                    )
                if not test_content:
                    logger.warning(f"API文件 {api_file} 既无可用参数，场景模式也未生成内容，跳过该接口")
                    continue

                write_test_file(test_filepath, test_content)
                generated_files.append(test_filepath)
            except Exception:
                logger.exception(f"生成测试用例文件失败 {api_file}")

        if generated_files:
            await format_directory(self.output_dir)
        return generated_files

    async def generate_scenario_testcase(
        self, har_file_path: str, target_url: str, task_id: str | None, overwrite: bool = False
    ) -> str | None:
        """生成复杂场景流程测试用例。"""
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None

        all_requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)
        api_files = await self.match_api_files_for_har(har_file_path, all_requests)
        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return None

        target_api_file = URLMatcher.find_matching_api_file(target_url, api_files)
        if not target_api_file:
            logger.error(f"未找到指定URL对应的API文件: {target_url}")
            return None

        os.makedirs(self.output_dir, exist_ok=True)
        api_info = parse_api_file(target_api_file)
        if not api_info.function_name:
            logger.error(f"API文件 {target_api_file} 缺少 function_name，无法生成测试文件")
            return None
        test_filename = f"test_{api_info.function_name}.py"
        test_filepath = os.path.join(self.output_dir, test_filename)
        if not overwrite and os.path.exists(test_filepath):
            logger.info(f"跳过已存在的测试文件: {test_filepath}")
            return None

        test_content = self.generate_scenario_test_content(
            har_file_path, api_files, task_id, target_api_file, all_requests
        )
        if not test_content:
            return None

        write_test_file(test_filepath, test_content)
        await format_directory(self.output_dir)
        return test_filepath

    async def generate_batch_testcases(
        self,
        api_files_list: list[str],
        task_id: str | None = None,
        overwrite: bool = False,
        har_file_path: str | None = None,
    ) -> dict[str, Any]:
        """批量生成测试用例（异步 + 并行处理）。"""
        expanded_api_files: list[str] = []
        for api_path in api_files_list:
            if os.path.isdir(api_path):
                py_files = [
                    os.path.join(root, f)
                    for root, _, files in os.walk(api_path)
                    for f in files
                    if f.endswith(".py") and not f.startswith("__")
                ]
                expanded_api_files.extend(py_files)
                logger.info(f"发现目录 {api_path}，包含 {len(py_files)} 个 API 文件")
            elif os.path.isfile(api_path):
                if os.path.basename(api_path) != "__init__.py":
                    expanded_api_files.append(api_path)
            else:
                logger.warning(f"路径不存在: {api_path}")
                continue

        generated_count = 0
        skipped_count = 0
        failed_count = 0
        generated_files_list: list[str] = []

        invalid_files = [f for f in expanded_api_files if not self._is_within_api_dir(f)]
        if invalid_files:
            examples = "、".join(invalid_files[:3])
            more = f" 等 {len(invalid_files)} 个文件" if len(invalid_files) > 3 else ""
            logger.error(
                f"API 文件 {examples}{more} 不在 --api-dir({self.api_dir}) 目录下，无法推导 import 包名。"
                f"请用 --api-dir 指定实际的 API 目录后重试。"
            )
            return {
                "total": len(expanded_api_files), "skipped": 0, "generated": 0,
                "failed": len(invalid_files), "generated_files": [],
            }

        os.makedirs(self.output_dir, exist_ok=True)

        cached_requests = None
        if har_file_path is not None and os.path.exists(har_file_path):
            cached_requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

        async def process_single(api_file: str) -> tuple[str, str | None]:
            """返回 (status, test_filepath) 二元组。"""
            task_start = time.time()
            api_basename = os.path.basename(api_file)
            try:
                if not os.path.exists(api_file):
                    logger.warning(f"  [任务跳过] {api_basename} 文件不存在")
                    return "skipped", None

                api_info = parse_api_file(api_file)
                if not api_info.function_name:
                    logger.warning(f"  [任务跳过] {api_basename} 无法提取 API 信息")
                    return "failed", None

                test_filename = f"test_{api_info.function_name}.py"
                test_filepath = os.path.join(self.output_dir, test_filename)

                if os.path.exists(test_filepath):
                    if not overwrite:
                        elapsed = time.time() - task_start
                        logger.debug(f"  [任务跳过] {api_basename} 测试文件已存在 (耗时 {elapsed:.2f}s)")
                        return "skipped", None

                mode = self._resolve_testcase_mode(api_file)
                test_content = None
                if mode == "parametrized":
                    test_content = self.generate_parametrized_test_content(api_file, task_id)
                if not test_content:
                    test_content = self.generate_scenario_test_content(
                        har_file_path, [api_file], task_id, api_file, cached_requests
                    )

                if test_content:
                    write_test_file(test_filepath, test_content)
                    elapsed = time.time() - task_start
                    logger.debug(f"  [任务完成] {api_basename} → {test_filename} (耗时 {elapsed:.2f}s)")
                    return "generated", test_filepath
                else:
                    elapsed = time.time() - task_start
                    logger.warning(f"  [任务失败] {api_basename} 生成测试内容为空 (耗时 {elapsed:.2f}s)")
                    return "failed", None
            except Exception:
                elapsed = time.time() - task_start
                logger.exception(f"  [任务异常] {api_basename} (耗时 {elapsed:.2f}s)")
                return "failed", None

        logger.info(f"[并行处理] 开始并行处理 {len(expanded_api_files)} 个 API 文件...")
        parallel_start = time.time()
        tasks = [process_single(api_file) for api_file in expanded_api_files]
        all_results = await asyncio.gather(*tasks)
        parallel_elapsed = time.time() - parallel_start

        for status, test_filepath in all_results:
            if status == "generated":
                generated_count += 1
                if test_filepath is not None:
                    generated_files_list.append(test_filepath)
                    logger.info(f"成功生成: {os.path.basename(test_filepath)}")
            elif status == "skipped":
                skipped_count += 1
            elif status == "failed":
                failed_count += 1

        logger.info(
            f"[并行处理] 完成! 成功: {generated_count}, 跳过: {skipped_count}, "
            f"失败: {failed_count}, 总耗时: {parallel_elapsed:.2f}s"
        )

        if generated_count > 0:
            await format_directory(self.output_dir)

        return {
            "total": len(expanded_api_files), "skipped": skipped_count,
            "generated": generated_count, "failed": failed_count,
            "generated_files": generated_files_list,
        }

    # ==================== 测试用例内容生成 ====================

    def generate_parametrized_test_content(
        self,
        api_file: str,
        task_id: str | None,
    ) -> str | None:
        """生成参数化列表测试用例内容（list_query 模式）。"""
        api_info = parse_api_file(api_file)
        function_name = api_info.function_name

        if not function_name:
            return None
        if not api_info.url:
            logger.error(f"API文件 {api_file} 元数据缺少 url 字段，请重新生成该 API 文件（--overwrite）以补齐元数据")
            return None
        if not self._validate_api_dir(api_file):
            return None

        feature_name, story_name = extract_api_info_for_scenario(api_file, self.api_dir)

        api_params: dict[str, Any] = {}
        if api_info.params:
            api_params.update(api_info.params)
        if isinstance(api_info.data, list):
            logger.error(
                f"API文件 {api_file} 的请求体为 JSON 数组（list），"
                f"list_query 模式暂不支持此类请求体，请改用 complex_scenario 模式生成测试用例"
            )
            return None
        if api_info.data:
            api_params.update(api_info.data)
        # Swagger 未定义参数时，回退到 HAR 抓包捕获的参数作为基底
        if not api_params and api_info.har_params:
            api_params.update(api_info.har_params)

        param_items: list[dict[str, Any]] = []
        if api_info.data or api_info.files:
            param_var_name = "data"
        else:
            param_var_name = "params"

        # 参数化枚举值来源：Swagger 预计算的 param_values 优先；
        # 仅当 param_values 为空时回退 HAR 抓包的 har_param_values，
        # 避免 HAR 特有参数（如 header）与 Swagger 枚举混用进行参数化
        merged_pv = dict(api_info.param_values)
        if not merged_pv:
            merged_pv.update(api_info.har_param_values or {})

        if not api_params:
            logger.info(f"API文件 {api_file} 无参数定义（params/data 均为空），跳过参数化模式")
            return None
        param_items = build_param_items_from_api(api_params, merged_pv, is_batch_mode=True)

        if not param_items and api_params:
            param_items = build_pagination_only_items([api_params])
            if param_items:
                for item in param_items:
                    pn = item["param_name"]
                    merged_pv[pn] = item[pn]
                logger.info(f"API文件 {os.path.basename(api_file)} 仅有分页参数，按默认分页生成参数化用例")

        if not param_items:
            logger.info(f"API文件 {api_file} 没有有效的参数化参数，跳过参数化模式")
            return None

        # 单值参数不参数化，由 list_query_data 提供运行时取值
        # （嵌套结构的组合键除外：即使只有一组值也保留参数化结构，
        # 否则会走运行时取值路径引用 list_query_data 中不存在的组合键）
        single_value_params = {
            pn for pn, v in merged_pv.items()
            if v and len(v) < 2 and not ("," in pn and isinstance(v[0], (list, tuple)))
        }
        existing_names = {item["param_name"] for item in param_items}
        for pn in single_value_params:
            if pn in existing_names:
                continue
            if APIConfig.is_pagination_param(pn) or APIConfig.is_time_param(pn):
                continue
            param_items.append({"param_name": pn})
            existing_names.add(pn)

        # 补充多值枚举参数
        for pn, values in merged_pv.items():
            if not values or len(values) < 2 or pn in existing_names:
                continue
            if APIConfig.is_pagination_param(pn) or APIConfig.is_time_param(pn):
                continue
            param_items.append({"param_name": pn})
            existing_names.add(pn)

        # 补充 api_params 中剩余参数（走非枚举路径，用 list_query_data 取运行时值）
        for pn in api_params:
            if pn in existing_names:
                continue
            if APIConfig.is_pagination_param(pn) or APIConfig.is_time_param(pn):
                continue
            if api_info.constant_params and pn in api_info.constant_params:
                continue
            param_items.append({"param_name": pn})
            existing_names.add(pn)

        # 添加时间对 start 参数到 param_items，生成组合测试方法
        tp_ctx = TimePairContext.build(api_info.time_pairs, api_params)
        for start_name in tp_ctx.start_to_end:
            if start_name in existing_names:
                continue
            param_items.append({"param_name": start_name})
            existing_names.add(start_name)

        ctx = self.render_ctx
        content = gen_test_case_imports(
            ctx, service_package=feature_name, function_name=function_name, task_id=task_id, is_list_query=True,
        )
        content.extend(
            gen_test_case_description(
                ctx, story_name, feature_name or "TODO", severity="NORMAL",
                api_description=api_info.description, param_remarks=api_info.param_remarks,
                api_headers=api_info.headers,
            )
        )

        # 统一生成逻辑（无论有无 HAR 文件）
        content.extend(gen_list_query_data_class_attr(api_params, merged_pv, tp_ctx))
        content.append("")
        # test_0 探测请求与参数化方法体取同一基准：api_params + constant_params 覆盖
        # （时间参数统一置 "" 不限时间，datetime 动态值仅由 list_query_data 提供，
        # 避免无 Swagger 场景 har_params 首条请求实际值（写死日期）污染方法体）
        test0_params = dict(api_params)
        if api_info.constant_params:
            test0_params.update(api_info.constant_params)
        for pn in list(test0_params):
            if APIConfig.is_time_param(pn):
                test0_params[pn] = ""
        content.extend(
            gen_test_0_collect_response_data(
                ctx, api_info.description, function_name, param_var_name, test0_params,
            )
        )
        # 测试方法体：统一以 api_params 为基准，覆盖 constant_params（如有）。
        # 无条件填充，确保时间对 start 参数等后续追加的 item 也有 other_params 键
        # （否则 gen_batch_parametrized_test_methods 读取时抛 KeyError）。
        # 时间参数统一置 "" 不限时间（datetime 动态值由时间对组合方法注入）。
        for item in param_items:
            filled = dict(api_params)
            if api_info.constant_params:
                filled.update(api_info.constant_params)
            filled.pop(item["param_name"], None)
            for pn in list(filled):
                if APIConfig.is_time_param(pn):
                    filled[pn] = ""
            item["other_params"] = filled
        content.extend(
            gen_batch_parametrized_test_methods(
                ctx, param_items, api_info.description, function_name, param_var_name,
                {k: v for k, v in merged_pv.items() if k not in single_value_params},
                api_info.param_remarks, time_pair_ctx=tp_ctx,
            )
        )
        if tp_ctx.has_time_pairs:
            insert_datetime_import(content)

        rendered = "\n".join(content)
        validate_python(rendered, f"参数化测试用例 {os.path.basename(api_file)}")
        return rendered

    def generate_scenario_test_content(
        self,
        har_file_path: str | None,
        api_files: list[str],
        task_id: str | None = None,
        target_api_file: str | None = None,
        requests: list[ParsedRequestInfo] | None = None,
    ) -> str | None:
        """生成复杂场景流程测试用例内容（complex_scenario 模式）。"""
        if requests is None:
            requests = get_requests_from_source(
                har_file_path, api_files, target_api_file,
                har_parser=self.har_parser, filter_duplicate_url=self.filter_duplicate_url,
            )

        for api_file in api_files:
            if not self._validate_api_dir(api_file):
                return None

        ctx = self.render_ctx
        content = gen_test_case_imports(ctx, api_files=api_files, task_id=task_id)

        feature_name, story_name = extract_api_info_for_scenario(target_api_file, self.api_dir)

        api_description = ""
        param_remarks = None
        api_headers = None
        if target_api_file:
            api_info = parse_api_file(target_api_file)
            api_description = api_info.description
            param_remarks = api_info.param_remarks
            api_headers = api_info.headers
            class_headers = api_headers or {}
        else:
            class_headers = {}
        content.extend(
            gen_test_case_description(
                ctx, story_name, feature_name or "TODO", severity="CRITICAL",
                api_description=api_description, param_remarks=param_remarks,
                api_headers=api_headers,
            )
        )

        if target_api_file is not None:
            content.extend(gen_scenario_test_method_definition(ctx, target_api_file))

        step_functions = gen_scenario_step_functions(
            ctx, content, requests, api_files, class_headers,
        )

        if step_functions:
            content.append("        # 执行所有测试步骤")
            call_prefix = "await " if self.async_mode else ""
            for step_func in step_functions:
                content.append(f"        {call_prefix}{step_func}()")
            content.append("")

        rendered = "\n".join(content)
        validate_python(rendered, f"场景测试用例 {os.path.basename(target_api_file) if target_api_file else 'unknown'}")
        return rendered


