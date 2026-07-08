from __future__ import annotations

import asyncio
import os
import time
from typing import Any

from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .swagger_handler import SwaggerHandler
from .url_matcher import URLMatcher
from .utils import (
    deduplicate_values,
    format_directory,
    format_parameter_value,
    format_params_for_python,
    get_output_dir,
    merge_request_params,
    parse_api_file,
    sanitize_param_name,
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
        _api_file_cache: API 文件信息缓存字典
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
        self.har_parser = HARParser(base_urls=base_urls, kill_urls=kill_urls)
        self.swagger_handler = SwaggerHandler()
        self.url_matcher = URLMatcher()
        # API文件缓存
        self._api_file_cache = {}

    # ==================== API 文件处理相关 ====================

    def _get_api_file_info(self, api_file: str) -> dict[str, Any]:
        """获取 API 文件信息（带缓存）。

        Args:
            api_file: API 文件路径

        Returns:
            API 文件信息字典，包含 function_name、url、description 等字段
        """
        if api_file not in self._api_file_cache:
            self._api_file_cache[api_file] = parse_api_file(api_file)
        return self._api_file_cache[api_file].copy()

    def _get_all_api_files(self) -> list[str]:
        """获取所有 API 文件路径。

        遍历 api_dir 目录，收集所有非 __init__.py 的 Python 文件。

        Returns:
            API 文件路径列表
        """
        api_files = []
        if not os.path.exists(self.api_dir):
            logger.warning(f"API目录不存在: {self.api_dir}")
            return api_files

        for root, _, files in os.walk(self.api_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    api_files.append(os.path.join(root, file))
        return api_files

    def _extract_service_package(self, api_file: str, index: int = 1) -> str | None:
        """从 API 文件路径中提取服务包名称。

        Args:
            api_file: API 文件路径
            index: 分割后取第几部分，默认1（apis.mall_user.xxx -> mall_user）

        Returns:
            服务包名称，无子包时返回 None
        """
        module_path = api_file.replace(".py", "").replace("\\", ".").replace("/", ".")
        parts = module_path.split(".")
        # 当 index 位置是路径最后一段时（即文件名），说明没有子包，返回 None
        if len(parts) > index + 1:
            return parts[index]
        return None

    # ==================== Swagger/URL 匹配相关 ====================

    async def _get_swagger_doc_for_url(self, url: str) -> dict[str, Any] | None:
        """根据 URL 获取对应的 Swagger 文档。

        Args:
            url: 请求 URL

        Returns:
            Swagger 文档字典，如果未找到则返回 None
        """
        service_package = APIConfig.determine_service_package(url)
        swagger_url = APIConfig.SWAGGER_DOC_URLS().get(service_package)
        if not swagger_url:
            return None
        return await self.swagger_handler.get_swagger_doc(swagger_url)

    async def _prepare_url_matcher(self, url: str) -> None:
        """为指定 URL 准备 URLMatcher。

        根据 URL 获取对应的 Swagger 文档，并设置到 url_matcher 中，
        以便后续进行 URL 模式匹配和参数提取。

        Args:
            url: 请求 URL
        """
        swagger_doc = await self._get_swagger_doc_for_url(url)
        self.url_matcher.swagger_data = swagger_doc

    async def match_api_files_for_har(
        self, har_file_path: str, requests: list[dict[str, Any]] | None = None
    ) -> list[str]:
        """根据 HAR 文件查找对应的 API 文件。

        Args:
            har_file_path: HAR 文件路径
            requests: 已解析的 HAR 请求列表（可选，避免重复解析）

        Returns:
            匹配到的 API 文件路径列表
        """
        if requests is None:
            requests = self.har_parser.extract_requests_from_har(har_file_path)

        # 预处理URL映射
        request_url_map = {}
        for request in requests:
            request_url = request["url"]
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

    # ==================== 参数处理相关 ====================

    def _is_valid_param(self, value: Any) -> bool:
        """判断参数值是否有效。

        有效参数定义为：非空字符串、非 None、非空列表/集合。

        Args:
            value: 参数值

        Returns:
            如果参数有效返回 True，否则返回 False
        """
        if value is None or value == "":
            return False
        if isinstance(value, (list, set)):
            return len(value) > 0
        return True

    def _parse_state_values(self, remark: str) -> list[int] | list[str]:
        """从参数备注中解析参数化取值。

        支持内置4种提取模式，并可通过配置 STATE_VALUE_PATTERNS 扩展。
        所有模式统一遍历，首个匹配成功即返回。

        Args:
            remark: 参数备注字符串

        Returns:
            参数化取值列表（整数或字符串）
        """
        import re

        # 内置匹配模式：(类型, 正则)
        builtin_patterns = [
            ("int", r"(-?\d+)\s*[:：、.]"),  # 匹配数字后跟冒号、顿号或点号（如 1.产品编码）
            ("int", r"(\d+)\s*[-》>]"),  # 匹配数字后跟箭头或破折号（如 1->描述 或 1-描述）
            ("str", r"(\w+)\s*->"),  # 匹配文本后跟箭头（如 health->上海健康 ev->企业微信）
            ("bracket_int", r"\((.*?)\)"),  # 匹配括号内的连续数字
            ("int", r"(\d+)(?=[\u4e00-\u9fff])"),  # 匹配数字后直接跟中文（如 1待审核 2审核通过）
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
            if not pattern:
                continue

            if pattern_type == "bracket_int":
                m = re.search(pattern, remark)
                if m:
                    numbers = re.findall(r"-?\d+", m.group(1))
                    if numbers:
                        return [int(n) for n in numbers]
                continue

            matches = re.findall(pattern, remark)
            if not matches:
                continue

            if pattern_type == "str":
                text_matches = [m for m in matches if not m.isdigit()]
                if text_matches:
                    return text_matches
            else:
                values = []
                for match in matches:
                    try:
                        values.append(int(match))
                    except ValueError:
                        pass
                if values:
                    return values

        return []

    def _build_param_items_from_api(
        self, api_params: dict[str, Any], param_remarks: dict[str, Any], is_batch_mode: bool = False
    ) -> list[dict[str, Any]]:
        """从 API 文件参数构建参数化项列表。

        遍历 API 文件中的所有参数，过滤分页参数，处理状态参数特殊逻辑，
        为每个非分页参数构建一个参数化项。

        Args:
            api_params: API 文件中的所有参数（包括 params 和 data）
            param_remarks: 参数备注字典
            is_batch_mode: 是否为 batch 模式（为 True 时包含空值参数）

        Returns:
            参数化项列表，每个元素包含参数名、参数值列表和其他参数
        """
        param_items = []
        pagination_params = set(APIConfig.PAGINATION_PARAMS())

        for param_name, param_value in api_params.items():
            # 跳过分页参数
            if param_name in pagination_params:
                continue

            # 收集其他参数
            other_params = {}
            for name, value in api_params.items():
                if name != param_name:
                    other_params[name] = value

            # 检查参数备注中是否有可提取的参数化取值
            if param_name in param_remarks:
                state_values = self._parse_state_values(param_remarks[param_name])
                if state_values:
                    if isinstance(param_value, list):
                        param_items.append({param_name: [[v] for v in state_values], "other_params": other_params})
                    else:
                        param_items.append({param_name: state_values, "other_params": other_params})
                elif self._is_valid_param(param_value):
                    param_items.append({param_name: [param_value], "other_params": other_params})
                elif is_batch_mode:
                    param_items.append({param_name: [param_value], "other_params": other_params})
            elif self._is_valid_param(param_value):
                param_items.append({param_name: [param_value], "other_params": other_params})
            elif is_batch_mode:
                if param_value == "" or param_value is None:
                    param_items.append({param_name: [""], "other_params": other_params})
                elif isinstance(param_value, list) and len(param_value) == 0:
                    param_items.append({param_name: [[]], "other_params": other_params})
                else:
                    param_items.append({param_name: [param_value], "other_params": other_params})

        return param_items

    def normalize_params_for_parametrization(self, requests_params: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """标准化参数化数据结构。

        将多个请求的参数整理为适合 pytest 参数化的格式，支持单参数和组合参数。
        过滤分页参数，对有效参数进行去重归类。

        Args:
            requests_params: 多个请求的参数字典列表

        Returns:
            标准化后的参数化数据列表，每个元素包含参数名、参数值列表和其他参数
        """
        param_value_map = {}
        pagination_params = set(APIConfig.PAGINATION_PARAMS())

        for req in requests_params:
            valid_params = {}
            other_params = {}

            for param_name, param_value in req.items():
                if param_name not in pagination_params:
                    if self._is_valid_param(param_value):
                        valid_params[param_name] = param_value
                    else:
                        other_params[param_name] = param_value
                else:
                    other_params[param_name] = param_value

            if not valid_params:
                continue

            if len(valid_params) > 1:
                # 组合参数
                sorted_names = sorted(valid_params.keys())
                combo_key = ",".join(sorted_names)
                combo_value = [valid_params[name] for name in sorted_names]

                if combo_key not in param_value_map:
                    param_value_map[combo_key] = {"values": [], "other_params": other_params}
                param_value_map[combo_key]["values"].append(combo_value)
            else:
                # 单参数
                param_name, param_value = next(iter(valid_params.items()))
                if param_name not in param_value_map:
                    param_value_map[param_name] = {"values": [], "other_params": other_params}
                param_value_map[param_name]["values"].append(param_value)

        # 构建最终结果并去重
        merged_result = []
        for param_name, data in param_value_map.items():
            merged_result.append({param_name: deduplicate_values(data["values"]), "other_params": data["other_params"]})

        return merged_result

    def _extract_requests_for_url(
        self, requests: list[dict[str, Any]], api_url: str
    ) -> tuple[set[str], list[dict[str, Any]], str | None]:
        """提取指定 URL 的请求参数。

        从请求列表中筛选出匹配指定 API URL 的请求，并提取其参数信息。

        Args:
            requests: HAR 请求列表
            api_url: 目标 API URL

        Returns:
            三元组：参数名集合、请求参数字典列表、请求方法
        """
        all_params = set()
        all_requests_params = []
        request_method = None

        normalized_api_url = URLMatcher.normalize_url(api_url)

        for req in requests:
            normalized_req_url = URLMatcher.normalize_url(req["url"])

            if normalized_req_url == normalized_api_url:
                # 直接合并 query_params 和 post_data
                api_params = merge_request_params(req)
                if isinstance(api_params, dict) and api_params:
                    all_requests_params.append(api_params)

                    for param_name, param_value in api_params.items():
                        if self._is_valid_param(param_value):
                            all_params.add(param_name)

                # 获取最后一个匹配请求的方法
                request_method = req.get("method", "GET")

        logger.info(f"提取到的参数: {all_params}")
        logger.info(f"提取到的请求参数: {all_requests_params}")
        logger.info(f"提取到的请求方法: {request_method}")

        return all_params, all_requests_params, request_method

    # ==================== 测试用例生成入口方法 ====================

    async def generate_parametrized_list_testcases(
        self, har_file_path: str, task_id: str | None, target_url: str | None = None, overwrite: bool = False
    ) -> list[str]:
        """生成查询类参数化测试用例。

        为每个匹配的 API 生成独立的参数化测试文件。

        Args:
            har_file_path: HAR 文件路径
            task_id: 任务 ID，用于命名输出目录
            target_url: 目标接口 URL（可选，指定后只生成该接口的测试用例）
            overwrite: 是否强制覆盖已存在的测试用例文件

        Returns:
            生成的测试用例文件路径列表
        """
        if not os.path.exists(har_file_path):
            return []

        all_requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

        api_files = await self.match_api_files_for_har(har_file_path, all_requests)
        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return []

        output_dir = get_output_dir(self.output_dir, task_id or "")
        generated_files: list[str] = []

        for api_file in api_files:
            try:
                api_info = self._get_api_file_info(api_file)

                # 如果指定了 target_url，则只处理匹配的 API
                if target_url:
                    if api_info["url"] != target_url:
                        continue

                clean_function_name = api_info["function_name"].lstrip("_")
                test_filename = f"test_{clean_function_name}.py"
                test_filepath = os.path.join(output_dir, test_filename)

                # 默认不覆盖已存在的测试文件
                if not overwrite and os.path.exists(test_filepath):
                    logger.info(f"跳过已存在的测试文件: {test_filepath}")
                    continue

                test_content = self.generate_parametrized_test_content(har_file_path, api_file, task_id, all_requests)
                # 参数化模式无参数时，fallback 到场景测试
                if not test_content:
                    test_content = self.generate_scenario_test_content(
                        har_file_path, [api_file], task_id, api_file, all_requests
                    )
                if not test_content:
                    continue

                write_test_file(test_filepath, test_content)
                generated_files.append(test_filepath)
            except Exception as e:
                logger.error(f"生成测试用例文件失败 {api_file}: {str(e)}")

        if generated_files:
            await format_directory(output_dir)

        return generated_files

    async def generate_scenario_testcase(
        self, har_file_path: str, target_url: str, task_id: str | None, overwrite: bool = False
    ) -> str | None:
        """生成复杂场景流程测试用例。

        针对指定的目标 URL 生成场景化的流程测试用例。

        Args:
            har_file_path: HAR 文件路径
            target_url: 目标 URL
            task_id: 任务 ID
            overwrite: 是否强制覆盖已存在的测试用例文件

        Returns:
            生成的测试用例文件路径，如果生成失败则返回 None
        """
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

        output_dir = get_output_dir(self.output_dir, task_id or "")
        api_info = self._get_api_file_info(target_api_file)
        clean_name = api_info["function_name"]
        test_filename = f"test_{clean_name}.py"
        test_filepath = os.path.join(output_dir, test_filename)

        # 默认不覆盖已存在的测试文件
        if not overwrite and os.path.exists(test_filepath):
            logger.info(f"跳过已存在的测试文件: {test_filepath}")
            return None

        test_content = self.generate_scenario_test_content(
            har_file_path, api_files, task_id, target_api_file, all_requests
        )

        if not test_content:
            return None

        write_test_file(test_filepath, test_content)
        await format_directory(output_dir)
        return test_filepath

    async def generate_batch_testcases(
        self,
        api_files_list: list[str],
        task_id: str | None = None,
        overwrite: bool = False,
        har_file_path: str | None = None,
    ) -> dict[str, Any]:
        """批量生成测试用例（异步 + 并行处理）。

        Args:
            api_files_list: API 文件路径列表
            task_id: 任务 ID
            overwrite: 是否强制覆盖已存在的测试用例文件
            har_file_path: HAR 文件路径（可选，指定后从 HAR 提取参数；否则从 API 文件提取）

        Returns:
            包含生成结果的字典：{
                'total': 总数,
                'skipped': 跳过数量,
                'generated': 生成数量,
                'failed': 失败数量,
                'generated_files': 生成的文件列表
            }
        """
        # 展开目录路径，获取所有 API 文件
        expanded_api_files = []
        for api_path in api_files_list:
            if os.path.isdir(api_path):
                # 如果是目录，遍历目录下所有 .py 文件（排除 __init__.py）
                py_files = [
                    os.path.join(root, f)
                    for root, _, files in os.walk(api_path)
                    for f in files
                    if f.endswith(".py") and not f.startswith("__")
                ]
                expanded_api_files.extend(py_files)
                logger.info(f"发现目录 {api_path}，包含 {len(py_files)} 个 API 文件")
            elif os.path.isfile(api_path):
                # 如果是文件，直接添加（排除 __init__.py）
                if not os.path.basename(api_path) == "__init__.py":
                    expanded_api_files.append(api_path)
            else:
                logger.warning(f"路径不存在: {api_path}")
                continue

        generated_count = 0
        skipped_count = 0
        failed_count = 0
        generated_files_list: list[str] = []

        output_dir = get_output_dir(self.output_dir, task_id or "")

        # 如果有 HAR 文件，提前解析一次请求列表，所有任务复用
        cached_requests = None
        if har_file_path is not None and os.path.exists(har_file_path):
            cached_requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

        # 定义异步任务：处理单个 API 文件
        async def process_single(api_file: str) -> tuple[str, str | None]:
            """返回 (status, test_filepath) 三元组。"""
            task_start = time.time()
            api_basename = os.path.basename(api_file)
            try:
                if not os.path.exists(api_file):
                    logger.warning(f"  [任务跳过] {api_basename} 文件不存在")
                    return "skipped", None

                api_info = self._get_api_file_info(api_file)
                if not api_info or not api_info.get("function_name"):
                    logger.warning(f"  [任务跳过] {api_basename} 无法提取 API 信息")
                    return "failed", None

                clean_function_name = api_info["function_name"].lstrip("_")
                test_filename = f"test_{clean_function_name}.py"
                test_filepath = os.path.join(output_dir, test_filename)

                if os.path.exists(test_filepath):
                    if not overwrite:
                        elapsed = time.time() - task_start
                        logger.debug(f"  [任务跳过] {api_basename} 测试文件已存在 (耗时 {elapsed:.2f}s)")
                        return "skipped", None

                api_description = api_info.get("description", "")
                list_keywords = APIConfig.LIST_QUERY_KEYWORDS()
                is_list_query = any(kw in api_description for kw in list_keywords) if list_keywords else False
                if is_list_query:
                    test_content = self.generate_parametrized_test_content(
                        har_file_path, api_file, task_id, cached_requests
                    )
                    # 参数化模式无参数时，fallback 到场景测试（无参数接口无需参数化）
                    if not test_content:
                        test_content = self.generate_scenario_test_content(
                            har_file_path, [api_file], task_id, api_file, cached_requests
                        )
                else:
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
            except Exception as e:
                elapsed = time.time() - task_start
                logger.error(f"  [任务异常] {api_basename} (耗时 {elapsed:.2f}s): {e}")
                return "failed", None

        # 并行处理所有 API 文件
        logger.info(f"[并行处理] 开始并行处理 {len(expanded_api_files)} 个 API 文件...")
        parallel_start = time.time()
        tasks = [process_single(api_file) for api_file in expanded_api_files]
        all_results = await asyncio.gather(*tasks)
        parallel_elapsed = time.time() - parallel_start

        # 汇总结果
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
            await format_directory(output_dir)

        return {
            "total": len(expanded_api_files),
            "skipped": skipped_count,
            "generated": generated_count,
            "failed": failed_count,
            "generated_files": generated_files_list,
        }

    # ==================== 测试用例内容生成 ====================

    def generate_parametrized_test_content(
        self,
        har_file_path: str | None,
        api_file: str,
        task_id: str | None,
        requests: list[dict[str, Any]] | None = None,
    ) -> str | None:
        """生成参数化列表测试用例内容（list_query 模式）。

        根据 HAR 文件和 API 文件生成基于参数化的列表查询测试用例。
        如果 HAR 文件不存在或无法提取参数，则直接从 API 文件读取参数（batch模式）。

        Args:
            har_file_path: HAR 文件路径（可选，为None时表示batch模式）
            api_file: API 文件路径
            task_id: 任务 ID
            requests: 已解析的 HAR 请求列表（可选，避免重复解析）

        Returns:
            参数化测试用例内容字符串，如果生成失败则返回 None
        """
        api_info = self._get_api_file_info(api_file)
        function_name = api_info["function_name"]

        if not function_name:
            return None

        # 提取接口信息（复用 complex_scenario 模式的方法）
        feature_name, story_name = self._extract_api_info(api_file)

        # 获取 API 文件中的所有参数（包括 params 和 data）
        api_params = {}
        if api_info.get("params"):
            api_params.update(api_info["params"])
        if api_info.get("data"):
            api_params.update(api_info["data"])

        # 构建参数化项
        has_har = har_file_path is not None and os.path.exists(har_file_path)
        param_items = []
        request_method = "GET"  # 默认请求方法

        # 如果有HAR文件，从HAR文件提取参数
        if has_har and har_file_path is not None:
            if requests is None:
                requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)
            _all_params, all_requests_params, request_method = self._extract_requests_for_url(requests, api_info["url"])

            if all_requests_params:
                param_items = self.normalize_params_for_parametrization(all_requests_params)

        # 只有batch模式（没有HAR文件）才从API文件读取参数
        if not param_items and not has_har:
            param_items = self._build_param_items_from_api(api_params, api_info["param_remarks"], is_batch_mode=True)

        if not param_items:
            logger.warning(f"API文件 {api_file} 中没有有效的测试参数")
            return None

        # 生成测试用例内容（单函数模式，需要 pytest）
        content = self._generate_test_case_imports(
            service_package=feature_name, function_name=function_name, task_id=task_id
        )
        content.extend(
            self._generate_test_case_description(story_name, feature_name or "TODO", severity="NORMAL")
        )

        content.extend(
            self._generate_parametrized_test_methods(
                param_items, api_info["description"], function_name, request_method or "GET", api_info["param_remarks"]
            )
        )

        return "\n".join(content)

    def generate_scenario_test_content(
        self,
        har_file_path: str | None,
        api_files: list[str],
        task_id: str | None = None,
        target_api_file: str | None = None,
        requests: list[dict[str, Any]] | None = None,
    ) -> str:
        """生成复杂场景流程测试用例内容（complex_scenario 模式）。

        根据 HAR 文件和多个 API 文件生成场景化的流程测试用例，包含多个步骤函数的调用链。

        Args:
            har_file_path: HAR 文件路径
            api_files: API 文件路径列表
            task_id: 任务 ID
            target_api_file: 目标 API 文件路径（可选）
            requests: 已解析的 HAR 请求列表（可选，避免重复解析）

        Returns:
            场景流程测试用例文件内容字符串
        """
        # 1. 提取请求（优先从 HAR 文件，没有则从 API 文件构建）
        if requests is None:
            requests = self._get_requests_from_source(har_file_path, api_files, target_api_file)

        # 2. 生成导入语句（多函数模式，不需要 pytest）
        content = self._generate_test_case_imports(api_files=api_files, task_id=task_id)

        # 3. 提取接口信息
        feature_name, story_name = self._extract_api_info(target_api_file)

        # 4. 生成测试用例描述（使用 CRITICAL 级别）
        content.extend(
            self._generate_test_case_description(story_name, feature_name or "TODO", severity="CRITICAL")
        )

        # 5. 生成测试方法定义
        if target_api_file is not None:
            content.extend(self._generate_scenario_test_method_definition(target_api_file))

        # 6. 生成步骤函数和步骤调用
        step_functions = self._generate_scenario_step_functions(content, requests, api_files)

        # 生成步骤调用
        if step_functions:
            content.append("        # 执行所有测试步骤")
            call_prefix = "await " if self.async_mode else ""
            for step_func in step_functions:
                content.append(f"        {call_prefix}{step_func}()")
            content.append("")

        return "\n".join(content)

    # ==================== 场景测试辅助方法 ====================

    def _get_requests_from_source(
        self, har_file_path: str | None, api_files: list[str], target_api_file: str | None
    ) -> list[dict[str, Any]]:
        """从 HAR 文件或 API 文件获取请求信息。

        优先从 HAR 文件获取，如果 HAR 文件不存在或为空，则从 API 文件构建请求信息。

        Args:
            har_file_path: HAR 文件路径
            api_files: API 文件路径列表
            target_api_file: 目标 API 文件路径

        Returns:
            请求信息列表
        """
        # 优先从 HAR 文件获取请求
        if har_file_path and os.path.exists(har_file_path):
            return self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

        # 如果没有 HAR 文件，则从 API 文件构建请求信息
        requests = []
        if target_api_file and os.path.exists(target_api_file):
            api_info = self._get_api_file_info(target_api_file)
            if api_info:
                # 构建模拟的请求信息，格式与 HAR 解析结果一致
                request_info = {
                    "url": api_info.get("url", ""),
                    "method": api_info.get("method", "GET"),
                    "query_params": api_info.get("params", {}),
                    "post_data": api_info.get("data", {}),
                    "headers": api_info.get("headers", {}),
                    "description": api_info.get("description", ""),
                    "api_file": target_api_file,
                }
                requests.append(request_info)

        return requests

    def _extract_api_info(self, target_api_file: str | None) -> tuple[str | None, str]:
        """从 API 文件提取接口信息。

        Args:
            target_api_file: 目标 API 文件路径

        Returns:
            (feature_name, story_name) 元组
        """
        feature_name = ""
        story_name = ""

        if target_api_file:
            # 提取服务名称
            feature_name = self._extract_service_package(target_api_file)
            if feature_name is None:
                feature_name = "TODO 未找到对应信息，请检查！"

            # 提取接口描述和URL
            result = self._get_api_file_info(target_api_file)
            api_url = result["url"]
            if api_url:
                story_name = api_url

        return feature_name, story_name

    def _generate_scenario_test_method_definition(self, target_api_file: str) -> list[str]:
        """生成场景测试方法定义。

        Args:
            target_api_file: 目标 API 文件路径（必选）

        Returns:
            测试方法定义代码行列表
        """
        api_info = self._get_api_file_info(target_api_file)
        clean_function_name = api_info["function_name"].lstrip("_")
        api_description = api_info.get("description", clean_function_name)
        prefix = "    async def " if self.async_mode else "    def "
        test_function_name = f"{prefix}test_{clean_function_name}(self):"

        return [
            f'    @allure.title("{api_description}")',
            test_function_name,
            "",
            "        # 初始化测试数据字典，用于在步骤间传递数据",
            "        test_data = {}",
            "",
        ]

    def _generate_scenario_step_functions(
        self, content: list[str], requests: list[dict[str, Any]], api_files: list[str]
    ) -> list[str]:
        """生成场景测试步骤函数。

        Args:
            content: 内容列表（会被修改）
            requests: 请求信息列表
            api_files: API 文件路径列表

        Returns:
            步骤函数名称列表
        """
        step_functions = []
        name_counters = {}

        for i, request_info in enumerate(requests):
            url = request_info["url"]

            # 使用 URLMatcher 查找匹配的 API 文件
            matched_api_file = URLMatcher.find_matching_api_file(url, api_files)

            if matched_api_file:
                api_info = self._get_api_file_info(matched_api_file)
                api_function_name = api_info["function_name"]
                api_description = api_info["description"]
                step_name = self._generate_step_function_name(api_function_name, name_counters)
                step_functions.append(step_name)

                # 生成数据键名
                clean_func_name = api_function_name.lstrip("_")
                func_parts = clean_func_name.split("_")
                data_key = (
                    "_".join(func_parts[-2:])
                    if len(func_parts) >= 2
                    else (func_parts[0] if func_parts else f"response_{i + 1}")
                )

                # 生成函数签名
                step_prefix = "        async def " if self.async_mode else "        def "
                content.extend([f'        @allure.step("{api_description}")', f"{step_prefix}{step_name}():", ""])

                # 生成步骤函数体（从HAR请求中获取参数）
                self._generate_step_function_body(content, api_function_name, api_info, request_info)

                # 生成断言
                status_attr = "r.status" if self.async_mode else "r.status_code"
                json_call = "await r.json()" if self.async_mode else "r.json()"
                content.extend(
                    [
                        f"                assert {status_attr} == 200",
                        f"                data = {json_call}",
                        "                assert data['code'] == 200",
                        f"                test_data['{data_key}'] = data['data']",
                        "",
                    ]
                )

        return step_functions

    def _generate_step_function_name(self, api_function_name: str, name_counters: dict[str, int]) -> str:
        """生成步骤函数名称。

        Args:
            api_function_name: API 函数名称
            name_counters: 名称计数器字典（会被修改）

        Returns:
            步骤函数名称
        """
        clean_function_name = api_function_name.lstrip("_")

        if clean_function_name not in name_counters:
            name_counters[clean_function_name] = 0

        count = name_counters[clean_function_name]

        if count == 0:
            step_name = f"step_{clean_function_name}"
        else:
            step_name = f"step_{count}_{clean_function_name}"

        name_counters[clean_function_name] += 1
        return step_name

    def _generate_step_function_body(
        self,
        content: list[str],
        api_function_name: str,
        api_info: dict[str, Any],
        request_info: dict[str, Any] | None = None,
    ) -> None:
        """生成步骤函数体。

        Args:
            content: 内容列表（会被修改）
            api_function_name: API 函数名称
            api_info: API 信息字典
            request_info: 请求信息字典（来自HAR文件，可选）
        """
        # 从 API 文件判断参数类型（data/params/files），决定调用格式
        api_files = api_info.get("files", {})
        api_data = api_info.get("data", {})
        api_params = api_info.get("params", {})

        # 从 HAR 请求获取参数值（优先），否则从 API 文件获取
        if request_info:
            har_query = request_info.get("query_params") or {}
            har_post = request_info.get("post_data") or {}
            har_values = {**har_post, **har_query}  # HAR 中的参数值
        else:
            har_values = {}

        # 根据 API 文件的参数类型确定请求方式
        is_file_upload = bool(api_files)

        ctx = "async with" if self.async_mode else "with"

        if is_file_upload:
            # 文件上传请求，使用 files 参数
            actual_values = {**api_files, **har_values} if har_values else api_files
            files_str = format_params_for_python(actual_values, indent=16)
            content.extend([f"            files = {files_str}", ""])
            content.extend([f"            {ctx} {api_function_name}(files=files) as r:"])
        elif api_data:
            # API 定义使用 data 参数，合并 HAR 值和 API 默认值
            actual_values = {**api_data, **har_values} if har_values else api_data
            data_str = format_params_for_python(actual_values, indent=16)
            content.extend([f"            data = {data_str}", ""])
            content.extend([f"            {ctx} {api_function_name}(data=data) as r:"])
        elif api_params:
            # API 定义使用 params 参数
            actual_values = {**api_params, **har_values} if har_values else api_params
            params_str = format_params_for_python(actual_values, indent=16)
            content.extend([f"            params = {params_str}", ""])
            content.extend([f"            {ctx} {api_function_name}(params=params) as r:"])
        else:
            # 没有参数时，直接调用函数
            content.extend([f"            {ctx} {api_function_name}() as r:"])

    # ==================== 通用方法 ====================

    def _generate_test_case_imports(
        self,
        api_files: list[str] | None = None,
        service_package: str | None = None,
        function_name: str | None = None,
        task_id: str | None = None,
    ) -> list[str]:
        """生成测试用例的导入部分。

        Args:
            api_files: API 文件路径列表（用于多函数导入）
            service_package: 服务包名称（用于单函数导入）
            function_name: API 函数名称（用于单函数导入）
            task_id: 任务 ID

        Returns:
            导入语句列表
        """
        content = [
            "import os",
            "",
        ]

        # 根据实际的 api_dir 目录名确定导入前缀
        base_pkg = os.path.basename(self.api_dir) or "apis"

        content.extend(
            [
                "import pytest",
                "import allure",
                "from allure_commons.types import Severity",
                "",
            ]
        )

        if api_files:
            # 多函数模式：按服务包分组导入
            service_imports: dict[str | None, list[str]] = {}
            for api_file in api_files:
                result = self._get_api_file_info(api_file)
                func_name = result["function_name"]
                if func_name:
                    pkg = self._extract_service_package(api_file)
                    if pkg not in service_imports:
                        service_imports[pkg] = []
                    service_imports[pkg].append(func_name)

            for pkg, functions in service_imports.items():
                if pkg is None:
                    # 根目录下无子包，直接从 apis 导入
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
            # 单函数模式
            if service_package is not None:
                content.append(f"from {base_pkg}.{service_package} import {function_name}")
            else:
                # 根目录下的 API 文件（无子包），直接从 apis 导入
                content.append(f"from {base_pkg} import {function_name}")
            content.append("")

        if task_id:
            content.append(f"@pytest.mark.{task_id}")

        return content

    def _generate_test_case_description(
        self, api_url: str, service_package: str, severity: str = "NORMAL"
    ) -> list[str]:
        """生成测试用例的描述部分。

        Args:
            api_url: API URL
            service_package: 服务包名称
            severity: 测试用例严重级别，可选值：NORMAL、CRITICAL、MINOR、MAJOR、BLOCKER

        Returns:
            描述语句列表
        """
        return [
            f"@allure.severity(Severity.{severity})",
            f"@allure.feature('{service_package}')",
            f"@allure.story('{api_url}')",
            "class TestClass:",
            "",
        ]

    # ==================== 参数化测试辅助方法 ====================

    def _generate_parametrized_test_methods(
        self,
        param_items: list[dict[str, Any]],
        api_description: str,
        function_name: str,
        request_method: str,
        param_remarks: dict[str, Any],
    ) -> list[str]:
        """生成参数化测试方法。

        Args:
            param_items: 参数化数据列表
            api_description: API 描述信息
            function_name: API 函数名称（带下划线前缀）
            request_method: 请求方法
            param_remarks: 参数备注字典

        Returns:
            参数化测试方法代码行列表
        """
        content = []
        clean_function_name = function_name.lstrip("_")

        for idx, item in enumerate(param_items):
            param_name = next((k for k in item if k != "other_params"), None)
            if not param_name:
                continue

            param_values = item[param_name]
            other_params = item["other_params"]
            is_combination = "," in param_name
            param_var_name = "params" if request_method == "GET" else "data"

            content.extend(self._generate_parametrize_decorator(param_name, param_values, is_combination))
            content.extend(
                self._generate_test_method_definition(
                    api_description, param_name, param_remarks, clean_function_name, idx, is_combination
                )
            )
            content.extend(self._generate_test_method_body(param_var_name, param_name, other_params, is_combination))
            content.extend(self._generate_test_method_assertions(function_name, param_var_name))

        return content

    def _generate_parametrize_decorator(
        self, param_name: str, param_values: list[Any], is_combination: bool
    ) -> list[str]:
        """生成 @pytest.mark.parametrize 装饰器。

        Args:
            param_name: 参数名称（可能包含多个参数，用逗号分隔）
            param_values: 参数值列表
            is_combination: 是否为组合参数

        Returns:
            装饰器代码行列表
        """
        parametrize_values = self._generate_parametrize_values(param_values, is_combination)

        if is_combination:
            safe_names = [sanitize_param_name(n.strip()) for n in param_name.split(",")]
            safe_param_name = ", ".join(safe_names)
        else:
            safe_param_name = sanitize_param_name(param_name)
        decorator_line = f'    @pytest.mark.parametrize("{safe_param_name}", ['

        content = [decorator_line]
        for i, value in enumerate(parametrize_values):
            suffix = "" if i == len(parametrize_values) - 1 else ","
            content.append(f"        {value}{suffix}")
        content.append("    ])")
        return content

    def _generate_parametrize_values(self, param_values: list[Any], is_combination: bool) -> list[str]:
        """生成参数化值列表。

        Args:
            param_values: 参数值列表
            is_combination: 是否为组合参数

        Returns:
            格式化后的参数化值列表
        """
        parametrize_values: list[str] = []
        if is_combination:
            for value_tuple in param_values:
                formatted_values = [format_parameter_value(v) for v in value_tuple]
                parametrize_values.append(f"({', '.join(formatted_values)})")
        else:
            for value in param_values:
                formatted_value = format_parameter_value(value)
                parametrize_values.append(f"{formatted_value}")
        return parametrize_values

    def _generate_test_method_definition(
        self,
        api_description: str,
        param_name: str,
        param_remarks: dict[str, Any],
        clean_function_name: str,
        param_count: int,
        is_combination: bool,
    ) -> list[str]:
        """生成测试方法定义。

        Args:
            api_description: API 描述信息
            param_name: 参数名称
            param_remarks: 参数备注字典
            clean_function_name: 清理后的函数名称
            param_count: 参数索引
            is_combination: 是否为组合参数

        Returns:
            测试方法定义代码行列表
        """
        prefix = "    async def " if self.async_mode else "    def "
        if is_combination:
            param_names = param_name.split(",")
            safe_param_names = [sanitize_param_name(p) for p in param_names]
            param_descriptions = []
            for p in param_names:
                desc = param_remarks.get(p, p)
                if "-" in desc:
                    desc = desc.split("-")[0]
                param_descriptions.append(desc)
            param_desc_str = "-".join(param_descriptions)
            return [
                f'    @allure.title("{api_description}: {param_desc_str} 查询")',
                f"{prefix}test_{param_count}_{clean_function_name}(self, {', '.join(safe_param_names)}):",
            ]
        else:
            safe_param_name = sanitize_param_name(param_name)
            param_description = param_remarks.get(param_name, param_name)
            if " " in param_description:
                param_description = param_description.split(" ")[0]
            return [
                f'    @allure.title("{api_description}: {param_description} 查询")',
                f"{prefix}test_{param_count}_{clean_function_name}(self, {safe_param_name}):",
            ]

    def _generate_test_method_body(
        self, param_var_name: str, param_name: str, other_params: dict[str, Any], is_combination: bool
    ) -> list[str]:
        """生成测试方法体。

        Args:
            param_var_name: 参数变量名（params 或 data）
            param_name: 参数名称
            other_params: 其他参数字典
            is_combination: 是否为组合参数

        Returns:
            测试方法体代码行列表
        """
        content = [
            "",
            f"        {param_var_name} = {{",
        ]
        self._generate_data_dict(content, param_name, other_params, is_combination, param_var_name)
        content.append("        }")
        return content

    def _generate_data_dict(
        self, content: list[str], param_name: str, other_params: dict[str, Any], is_combination: bool, param_var_name: str
    ) -> None:
        """生成数据字典。

        Args:
            content: 内容列表（会被修改）
            param_name: 参数名称
            other_params: 其他参数字典
            is_combination: 是否为组合参数
            param_var_name: 参数变量名
        """
        if is_combination:
            for key in param_name.split(","):
                safe_key = sanitize_param_name(key)
                content.append(f'            "{key}": {safe_key},')
        else:
            safe_name = sanitize_param_name(param_name)
            content.append(f'            "{param_name}": {safe_name},')

        for key, value in other_params.items():
            if isinstance(value, str):
                content.append(f'            "{key}": {repr(value)},')
            else:
                content.append(f'            "{key}": {value},')

    def _generate_test_method_assertions(self, function_name: str, param_var_name: str) -> list[str]:
        """生成测试方法断言部分。

        Args:
            function_name: API 函数名称
            param_var_name: 参数变量名（params 或 data）

        Returns:
            断言代码行列表
        """
        ctx = "async with" if self.async_mode else "with"
        status_attr = "r.status" if self.async_mode else "r.status_code"
        json_call = "await r.json()" if self.async_mode else "r.json()"
        return [
            f"        {ctx} {function_name}({param_var_name}={param_var_name}) as r:",
            f"            assert {status_attr} == 200",
            f"            data = {json_call}",
            "            assert data['code'] == 200",
            "",
        ]
