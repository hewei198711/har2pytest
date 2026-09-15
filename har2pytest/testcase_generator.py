from __future__ import annotations

import asyncio
import fnmatch
import os
import re
import time
from typing import Any

from .codegen import render_lines, validate_python
from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .models import APIFileInfo, ParsedRequestInfo
from .swagger_handler import SwaggerHandler
from .url_matcher import URLMatcher
from .utils import (
    deduplicate_values,
    format_directory,
    format_parameter_value,
    format_params_for_python,
    get_output_dir,
    header_value_formatter,
    merge_request_params,
    parse_api_file,
    sanitize_param_name,
    sanitize_remark,
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
        self.har_parser = HARParser(base_urls=base_urls, kill_urls=kill_urls)
        self.swagger_handler = SwaggerHandler()
        self.url_matcher = URLMatcher()
        # 场景模式下目标API的 headers（用于生成类级别 headers 属性，步骤 headers 差异对比基准）
        self._class_headers: dict[str, Any] = {}

    # ==================== API 文件处理相关 ====================

    def _get_api_file_info(self, api_file: str) -> APIFileInfo:
        """获取 API 文件信息（复用 parse_api_file 的全局缓存，不再自建第二层缓存）。

        Args:
            api_file: API 文件路径

        Returns:
            APIFileInfo: API 文件信息对象
        """
        return parse_api_file(api_file)

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

    def _extract_service_package(self, api_file: str) -> str | None:
        """从 API 文件路径中提取服务包名称。

        通过计算相对于 api_dir 的路径来提取子包名称。
        例如：api_dir=apis, api_file=apis/mall_user/order.py -> mall_user

        Args:
            api_file: API 文件路径

        Returns:
            服务包名称，文件直接在 api_dir 下时返回 None
        """
        try:
            rel_path = os.path.relpath(api_file, self.api_dir)
        except ValueError:
            # Windows 下跨盘符无法计算相对路径
            return None
        # 去掉 .py 后缀（removesuffix 仅匹配末尾，避免目录名中的 .py 子串被误删），统一分隔符
        module_path = rel_path.removesuffix(".py").replace("\\", "/")
        parts = module_path.split("/")
        if len(parts) > 1:
            return parts[0]
        return None

    def _is_within_api_dir(self, api_file: str) -> bool:
        """判断 API 文件是否位于 api_dir 目录下（不做日志）。"""
        try:
            rel_path = os.path.relpath(os.path.abspath(api_file), os.path.abspath(self.api_dir))
        except ValueError:
            return False
        return not rel_path.startswith(os.pardir)

    def _validate_api_dir(self, api_file: str) -> bool:
        """校验 API 文件位于 api_dir 目录下。

        import 语句的前缀包名由 api_dir 的目录名推导（如 ``from apis.svc import x``），
        因此 API 文件必须位于 api_dir 下；否则直接报错提示，而不是生成非法 import。

        Args:
            api_file: API 文件路径

        Returns:
            bool: 位于 api_dir 下返回 True，否则记录错误并返回 False
        """
        if self._is_within_api_dir(api_file):
            return True
        logger.error(
            f"API 文件 {api_file} 不在 --api-dir({self.api_dir}) 目录下，无法推导 import 包名。"
            f"请用 --api-dir 指定实际的 API 目录后重试。"
        )
        return False

    # ==================== 测试模式决策（配置化） ====================

    @staticmethod
    def _profile_matches(profile_url: str, api_url: str) -> bool:
        """判断 profile.url 是否命中接口 URL（精确 / {param} 模板 / 末尾通配 *）。"""
        norm_profile = URLMatcher.normalize_url(profile_url)
        norm_url = URLMatcher.normalize_url(api_url)

        if norm_url == norm_profile:
            return True
        if "*" in norm_profile:
            # 通配仅在结尾（如 /mgmt/order/*），用 fnmatch 匹配
            if fnmatch.fnmatchcase(norm_url, norm_profile):
                return True
        # 双向路径模板匹配（覆盖 {id} 与具体值的互转）
        matched, _ = URLMatcher.match_url_pattern(norm_url, norm_profile)
        if matched:
            return True
        matched, _ = URLMatcher.match_url_pattern(norm_profile, norm_url)
        return matched

    def _find_profile(self, api_url: str | None) -> dict | None:
        """返回命中该接口 URL 的 TESTCASE_PROFILES 条目（无命中返回 None）。"""
        if not api_url:
            return None
        for profile in APIConfig.TESTCASE_PROFILES() or []:
            if isinstance(profile, dict) and profile.get("url") and self._profile_matches(str(profile["url"]), api_url):
                return profile
        return None

    def _resolve_testcase_mode(self, api_file: str) -> str:
        """决策单个接口的测试生成模式，返回 ``parametrized`` 或 ``scenario``。

        决策优先级（消除分散在命令行/中文关键字中的判定点）：
        1. TESTCASE_PROFILES 中按 URL 命中且 ``mode`` 显式给出 → 直接采用；
        2. ``mode=auto``（缺省）或未配置 → 回落关键字启发式；
           keywords/exclude_keywords 条目可覆盖全局 LIST_QUERY_KEYWORDS/
           LIST_QUERY_EXCLUDE_KEYWORDS。

        Args:
            api_file: API 文件路径

        Returns:
            "parametrized"（列表参数化）或 "scenario"（复杂场景）
        """
        api_info = self._get_api_file_info(api_file)
        description = api_info.description or ""
        profile = self._find_profile(api_info.url)

        explicit = (profile or {}).get("mode", "auto")
        if explicit == "list_query":
            return "parametrized"
        if explicit == "complex_scenario":
            return "scenario"

        # 关键字启发式（profile 可覆盖全局默认）
        if profile is not None:
            keywords = profile.get("keywords")
            exclude_keywords = profile.get("exclude_keywords")
        else:
            keywords = exclude_keywords = None
        list_keywords = keywords if isinstance(keywords, list) else APIConfig.LIST_QUERY_KEYWORDS()
        exclude = (
            exclude_keywords if isinstance(exclude_keywords, list) else APIConfig.LIST_QUERY_EXCLUDE_KEYWORDS()
        )

        is_list_query = bool(list_keywords) and any(kw in description for kw in list_keywords)
        if is_list_query and exclude and any(kw in description for kw in exclude):
            is_list_query = False
        return "parametrized" if is_list_query else "scenario"

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
        self, har_file_path: str, requests: list[ParsedRequestInfo] | None = None
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
        # 内置匹配模式：(类型, 正则)
        # 注意：模式 1/5 添加 (?<!\w) 负向后行断言，避免匹配嵌入单词中的数字（如 "H5、APP" 中的 5）
        builtin_patterns = [
            ("int", r"(?<!\w)(-?\d+)\s*[:：、.]"),  # 匹配段首数字后跟冒号、顿号或点号（如 1.产品编码）
            ("int", r"(?<!\w)(\d+)\s*[-》>]"),  # 匹配段首数字后跟箭头或破折号（如 1->描述 或 1-描述）
            ("str", r"(\w+)\s*->"),  # 匹配文本后跟箭头（如 health->上海健康 ev->企业微信）
            ("bracket_int", r"\((.*?)\)"),  # 匹配括号内的连续数字
            ("int", r"(?<!\w)(\d+)(?=[\u4e00-\u9fff])"),  # 匹配段首数字后直接跟中文（如 1待审核 2审核通过）
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
        param_items: list[dict[str, Any]] = []
        pagination_params = set(APIConfig.PAGINATION_PARAMS())

        # 预构建完整参数字典
        other_params_base = dict(api_params)

        for param_name, param_value in api_params.items():
            # 跳过分页参数
            if param_name in pagination_params:
                continue

            # 从基础字典中临时移除当前参数，浅拷贝快照后恢复
            del other_params_base[param_name]
            other_params = dict(other_params_base)
            other_params_base[param_name] = param_value

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

        # 过滤分页参数后没有任何有效参数（如列表接口仅携带 pageNum/pageSize），
        # 退化为一条基于分页参数的默认参数化项，避免后续误报“没有有效的测试参数”。
        if not merged_result:
            return self._build_pagination_only_items(requests_params)
        return merged_result

    def _build_pagination_only_items(self, requests_params: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """请求仅有分页/无效参数时，退化为单条默认参数化项。

        列表类接口常只携带 ``pageNum``/``pageSize``（也可能全为空值参数），
        过滤分页参数后没有可变的“有效参数”。此时把分页参数本身当作变量，
        生成一条能正常发请求的参数化项：变量取各请求中的取值（去重），
        其余参数作为固定值放入 ``other_params``。

        Args:
            requests_params: 请求参数字典列表（每项为非空 dict）。

        Returns:
            含 0 或 1 条参数化项的列表；无可用参数时返回空列表。
        """
        if not requests_params:
            return []
        pagination_params = APIConfig.PAGINATION_PARAMS()
        first = requests_params[0]
        # 变量优先选配置中的分页参数（如 pageNum），否则退而求其次取首个键
        var = next((p for p in pagination_params if p in first), next(iter(first), None))
        if var is None:
            return []
        values = deduplicate_values([r[var] for r in requests_params if var in r and self._is_valid_param(r[var])])
        if not values:
            values = [first[var]]
        other_params = {key: value for key, value in first.items() if key != var}
        return [{var: values, "other_params": other_params}]

    def _extract_requests_for_url(self, requests: list[ParsedRequestInfo], api_url: str) -> list[dict[str, Any]]:
        """提取指定 URL 的请求参数列表。

        从请求列表中筛选出匹配指定 API URL 的请求，合并 query_params 与 post_data，
        返回有效请求参数字典列表。

        Args:
            requests: HAR 请求列表
            api_url: 目标 API URL

        Returns:
            请求参数字典列表（已合并 query 与 body）。
        """
        all_requests_params = []

        normalized_api_url = URLMatcher.normalize_url(api_url)

        for req in requests:
            normalized_req_url = URLMatcher.normalize_url(req.url)

            if normalized_req_url == normalized_api_url:
                # 直接合并 query_params 和 post_data
                api_params = merge_request_params(req)
                if isinstance(api_params, dict) and api_params:
                    all_requests_params.append(api_params)

        logger.debug(f"提取到的请求参数: {all_requests_params}")

        return all_requests_params

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

        output_dir = get_output_dir(self.output_dir)
        generated_files: list[str] = []

        for api_file in api_files:
            try:
                api_info = self._get_api_file_info(api_file)

                # 如果指定了 target_url，则只处理匹配的 API
                if target_url:
                    if api_info.url != target_url:
                        continue

                clean_function_name = (api_info.function_name or "").lstrip("_")
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
                    logger.warning(
                        f"API文件 {api_file} 既无可用参数，场景模式也未生成内容，跳过该接口"
                    )
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

        output_dir = get_output_dir(self.output_dir)
        api_info = self._get_api_file_info(target_api_file)
        clean_name = (api_info.function_name or "").lstrip("_")
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

        # 提前校验：API 文件必须位于 api_dir 下（import 前缀包名依赖该目录结构），
        # 否则直接报错提示，避免生成非法 import 的测试用例。
        invalid_files = [f for f in expanded_api_files if not self._is_within_api_dir(f)]
        if invalid_files:
            examples = "、".join(invalid_files[:3])
            more = f" 等 {len(invalid_files)} 个文件" if len(invalid_files) > 3 else ""
            logger.error(
                f"API 文件 {examples}{more} 不在 --api-dir({self.api_dir}) 目录下，无法推导 import 包名。"
                f"请用 --api-dir 指定实际的 API 目录后重试。"
            )
            return {
                "total": len(expanded_api_files),
                "skipped": 0,
                "generated": 0,
                "failed": len(invalid_files),
                "generated_files": [],
            }

        output_dir = get_output_dir(self.output_dir)

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
                if not api_info or not api_info.function_name:
                    logger.warning(f"  [任务跳过] {api_basename} 无法提取 API 信息")
                    return "failed", None

                clean_function_name = (api_info.function_name or "").lstrip("_")
                test_filename = f"test_{clean_function_name}.py"
                test_filepath = os.path.join(output_dir, test_filename)

                if os.path.exists(test_filepath):
                    if not overwrite:
                        elapsed = time.time() - task_start
                        logger.debug(f"  [任务跳过] {api_basename} 测试文件已存在 (耗时 {elapsed:.2f}s)")
                        return "skipped", None

                # 统一决策模式：TESTCASE_PROFILES 显式配置优先，否则关键字启发式
                mode = self._resolve_testcase_mode(api_file)
                if mode == "parametrized":
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
        requests: list[ParsedRequestInfo] | None = None,
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
        function_name = api_info.function_name

        if not function_name:
            return None

        if not self._validate_api_dir(api_file):
            return None

        # 提取接口信息（复用 complex_scenario 模式的方法）
        feature_name, story_name = self._extract_api_info(api_file)

        # 获取 API 文件中的所有参数（包括 params 和 data）
        api_params = {}
        if api_info.params:
            api_params.update(api_info.params)
        # JSON 数组请求体（list）无法用 dict.update 合并，保持整 list 交由下游分支处理
        if isinstance(api_info.data, dict):
            api_params.update(api_info.data)

        # 构建参数化项
        has_har = har_file_path is not None and os.path.exists(har_file_path)
        param_items = []
        # 从 API 文件参数类型确定调用参数名
        if api_info.data or api_info.files:
            param_var_name = "data"
        else:
            param_var_name = "params"

        # 如果有HAR文件，从HAR文件提取参数
        all_requests_params: list[dict[str, Any]] = []
        if has_har and har_file_path is not None:
            if requests is None:
                requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)
            all_requests_params = self._extract_requests_for_url(requests, api_info.url or "")

            if all_requests_params:
                param_items = self.normalize_params_for_parametrization(all_requests_params)

        # 只有batch模式（没有HAR文件）才从API文件读取参数
        if not param_items and not has_har:
            param_items = self._build_param_items_from_api(api_params, api_info.param_remarks, is_batch_mode=True)

        # 过滤分页参数后没有有效参数时，退化为单条默认参数化项（分页参数作变量，其余为固定值）
        if not param_items:
            fallback_source: list[dict[str, Any]] | None = None
            if all_requests_params:
                fallback_source = all_requests_params
            elif api_params:
                fallback_source = [api_params]
            if fallback_source:
                param_items = self._build_pagination_only_items(fallback_source)
                if param_items:
                    logger.info(
                        f"API文件 {os.path.basename(api_file)} 仅有分页参数，按默认分页生成参数化用例"
                    )

        if not param_items:
            # 无参数接口无需参数化：这里只是回退场景模式的正常路径，调用方会继续生成场景用例，
            # 因此用 INFO 记录，真正的失败（两种模式都没内容）由调用方告警。
            logger.info(f"API文件 {api_file} 没有有效的参数化参数，回退场景模式")
            return None

        # 生成测试用例内容（单函数模式，需要 pytest）
        content = self._generate_test_case_imports(
            service_package=feature_name, function_name=function_name, task_id=task_id,
            is_list_query=True,
        )
        content.extend(
            self._generate_test_case_description(
                story_name, feature_name or "TODO", severity="NORMAL",
                api_description=api_info.description, param_remarks=api_info.param_remarks,
                api_headers=api_info.headers,
            )
        )

        content.extend(
            self._generate_parametrized_test_methods(
                param_items, api_info.description, function_name, param_var_name, api_info.param_remarks
            )
        )

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
        """生成复杂场景流程测试用例内容（complex_scenario 模式）。

        根据 HAR 文件和多个 API 文件生成场景化的流程测试用例，包含多个步骤函数的调用链。

        Args:
            har_file_path: HAR 文件路径
            api_files: API 文件路径列表
            task_id: 任务 ID
            target_api_file: 目标 API 文件路径（可选）
            requests: 已解析的 HAR 请求列表（可选，避免重复解析）

        Returns:
            str | None: 场景流程测试用例文件内容字符串；API 文件不在 api_dir 下时返回 None
        """
        # 1. 提取请求（优先从 HAR 文件，没有则从 API 文件构建）
        if requests is None:
            requests = self._get_requests_from_source(har_file_path, api_files, target_api_file)

        # 1.1 API 文件必须位于 api_dir 下（import 前缀包名依赖该目录结构）
        for api_file in api_files:
            if not self._validate_api_dir(api_file):
                return None

        # 2. 生成导入语句（多函数模式，不需要 pytest）
        content = self._generate_test_case_imports(api_files=api_files, task_id=task_id)

        # 3. 提取接口信息
        feature_name, story_name = self._extract_api_info(target_api_file)

        # 4. 生成测试用例描述（使用 CRITICAL 级别）
        api_description = ""
        param_remarks = None
        api_headers = None
        if target_api_file:
            api_info = self._get_api_file_info(target_api_file)
            api_description = api_info.description
            param_remarks = api_info.param_remarks
            api_headers = api_info.headers
            self._class_headers = api_headers or {}
        content.extend(
            self._generate_test_case_description(
                story_name, feature_name or "TODO", severity="CRITICAL",
                api_description=api_description, param_remarks=param_remarks,
                api_headers=api_headers,
            )
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

        rendered = "\n".join(content)
        validate_python(rendered, f"场景测试用例 {os.path.basename(target_api_file) if target_api_file else 'unknown'}")
        return rendered

    # ==================== 场景测试辅助方法 ====================

    def _get_requests_from_source(
        self, har_file_path: str | None, api_files: list[str], target_api_file: str | None
    ) -> list[ParsedRequestInfo]:
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
                request_info = ParsedRequestInfo(
                    url=api_info.url or "",
                    method="GET",
                    query_params=api_info.params,
                    post_data=api_info.data,
                    headers=api_info.headers,
                )
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
            api_url = result.url
            if api_url:
                story_name = api_url

        return feature_name, story_name

    def _generate_scenario_test_method_definition(self, target_api_file: str) -> list[str]:
        """生成场景测试方法定义。

        由 Jinja2 模板 ``s_test_method_definition.j2`` 渲染。

        Args:
            target_api_file: 目标 API 文件路径（必选）

        Returns:
            测试方法定义代码行列表
        """
        api_info = self._get_api_file_info(target_api_file)
        clean_function_name = (api_info.function_name or "").lstrip("_")
        api_description = api_info.description or clean_function_name
        def_prefix = "    async def " if self.async_mode else "    def "

        return render_lines(
            "s_test_method_definition.j2",
            title_text=sanitize_remark(api_description),
            def_prefix=def_prefix,
            clean_name=clean_function_name,
        )

    def _generate_scenario_step_functions(
        self, content: list[str], requests: list[ParsedRequestInfo], api_files: list[str]
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
            url = request_info.url

            # 使用 URLMatcher 查找匹配的 API 文件
            matched_api_file = URLMatcher.find_matching_api_file(url, api_files)

            if matched_api_file:
                api_info = self._get_api_file_info(matched_api_file)
                api_function_name = api_info.function_name or ""
                api_description = api_info.description
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

                # 生成函数签名（模板渲染，避免手工拼接缩进）
                step_prefix = "        async def " if self.async_mode else "        def "
                content.extend(
                    render_lines(
                        "s_step_heading.j2",
                        step_description=api_description or "",
                        step_prefix=step_prefix,
                        step_name=step_name,
                    )
                )

                # 生成步骤函数体（从HAR请求中获取参数）
                self._generate_step_function_body(content, api_function_name, api_info, request_info)

                # 生成断言（模板渲染；同步 requests / 异步 aiohttp 响应字段不同）
                status_attr = "r.status" if self.async_mode else "r.status_code"
                json_call = "await r.json()" if self.async_mode else "r.json()"
                content.extend(
                    render_lines(
                        "s_step_asserts.j2",
                        status_attr=status_attr,
                        json_call=json_call,
                        data_key=data_key,
                    )
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
        api_info: APIFileInfo,
        request_info: ParsedRequestInfo | None = None,
    ) -> None:
        """生成步骤函数体。

        Args:
            content: 内容列表（会被修改）
            api_function_name: API 函数名称
            api_info: API 文件信息
            request_info: 解析后的请求信息（来自HAR文件，可选）
        """
        # 从 API 文件判断参数类型（data/params/files），决定调用格式
        api_files = api_info.files
        api_data = api_info.data
        api_params = api_info.params

        # 从 HAR 请求获取参数值（优先），否则从 API 文件获取
        if request_info:
            har_query = request_info.query_params or {}
            har_post = request_info.post_data or {}
            # JSON 数组请求体（list）无法与 dict 展开合并，整体作为 HAR 值
            if isinstance(har_post, list):
                har_values = har_post if har_post else {}
            else:
                har_values = {**har_post, **har_query} if (har_post or har_query) else {}
        else:
            har_values = {}

        # 根据 API 文件的参数类型确定请求方式
        is_file_upload = bool(api_files)

        ctx = "async with" if self.async_mode else "with"

        # 步骤 API 的 headers 与类级别 headers 存在差异时，生成局部 headers 覆盖（如额外的 content-type）
        header_lines, headers_arg = self._build_step_headers_arg(api_info.headers)
        if header_lines:
            content.extend(header_lines)

        # 步骤体代码行由 Jinja2 模板渲染（s_step_*.j2），避免手工拼接缩进
        if is_file_upload:
            # 文件上传请求，使用 files 参数（list 请求体不会出现在文件上传分支）
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
            # API 定义使用 data 参数，合并 HAR 值和 API 默认值
            if isinstance(api_data, dict) and isinstance(har_values, dict):
                # 最常见：API 默认值与 HAR 值均为 dict，直接合并
                actual_values = {**api_data, **har_values} if har_values else api_data
                data_str = format_params_for_python(actual_values, indent=16)
            elif isinstance(har_values, list):
                # JSON 数组请求体：HAR 数组优先（无法与 dict 合并）
                data_str = format_parameter_value(har_values)
            else:
                # API 文件 data 本身是数组（如行为采集接口），直接用 API 默认数组
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
            # API 定义使用 params 参数（list 请求体不会出现在 params 分支）
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
            # 没有参数时，直接调用函数（仍传 headers 覆盖模块级默认值）
            content.extend(
                render_lines(
                    "s_step_none.j2",
                    ctx=ctx,
                    function_name=api_function_name,
                    headers_arg=headers_arg,
                )
            )

    # ==================== 通用方法 ====================

    def _build_step_headers_arg(self, step_headers: dict[str, Any]) -> tuple[list[str], str]:
        """构建步骤调用的 headers 参数。

        步骤 API 的 headers 与类级别 headers（self._class_headers）存在差异时，
        生成局部 headers 变量（基于 self.headers 覆盖差异项）；否则直接使用 self.headers。

        Args:
            step_headers: 步骤对应 API 文件中的 headers 字典

        Returns:
            (额外的代码行列表, headers 参数字符串)
        """
        diff = {k: v for k, v in step_headers.items() if self._class_headers.get(k) != v}
        if not diff:
            return [], "headers=self.headers"

        if self._class_headers:
            diff_str = ", ".join(f'"{k}": {header_value_formatter(v)}' for k, v in diff.items())
            line = f"            headers = {{**self.headers, {diff_str}}}"
        else:
            diff_str = ", ".join(f'"{k}": {header_value_formatter(v)}' for k, v in step_headers.items())
            line = f"            headers = {{{diff_str}}}"
        return [line, ""], "headers=headers"

    def _generate_test_case_imports(
        self,
        api_files: list[str] | None = None,
        service_package: str | None = None,
        function_name: str | None = None,
        task_id: str | None = None,
        is_list_query: bool = False,
    ) -> list[str]:
        """生成测试用例的导入部分。

        Args:
            api_files: API 文件路径列表（用于多函数导入）
            service_package: 服务包名称（用于单函数导入）
            function_name: API 函数名称（用于单函数导入）
            task_id: 任务 ID
            is_list_query: 是否为 list_query 模式（自动添加 @pytest.mark.test_list_query）

        Returns:
            导入语句列表
        """
        content = [
            "import os",
            "",
        ]

        # 根据实际的 api_dir 目录名确定导入前缀（调用前已校验 API 文件在 api_dir 下）
        base_pkg = os.path.basename(self.api_dir) or APIConfig.DEFAULT_API_DIR()

        content.extend(
            [
                "import pytest",
                "import allure",
                "from allure_commons.types import Severity",
                "",
            ]
        )

        # 异步模式：切换全局 client 为 async_client
        if self.async_mode:
            content.extend(
                [
                    "from har2pytest.client import client, async_client",
                    "client.set_client(async_client)",
                    "",
                ]
            )

        if api_files:
            # 多函数模式：按服务包分组导入
            service_imports: dict[str | None, list[str]] = {}
            for api_file in api_files:
                result = self._get_api_file_info(api_file)
                func_name = result.function_name
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
            if service_package is not None and service_package.isidentifier():
                content.append(f"from {base_pkg}.{service_package} import {function_name}")
            else:
                # 根目录下的 API 文件（无子包）或服务包未知（如占位提示文本）：
                # 无法拼出合法的包路径，直接从 apis 导入，避免生成非法 Python
                content.append(f"from {base_pkg} import {function_name}")
            content.append("")

        if task_id:
            content.append(f"@pytest.mark.{task_id}")

        if is_list_query:
            content.append("@pytest.mark.test_list_query")

        return content

    def _generate_allure_description(
        self,
        api_url: str,
        api_description: str = "",
        param_remarks: dict[str, Any] | None = None,
    ) -> str:
        """生成 @allure.description 装饰器代码行。

        Args:
            api_url: 接口地址
            api_description: 接口名称/描述
            param_remarks: 参数备注字典 {param_name: remark}

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

    def _generate_test_case_description(
        self,
        api_url: str,
        service_package: str,
        severity: str = "NORMAL",
        api_description: str = "",
        param_remarks: dict[str, Any] | None = None,
        api_headers: dict[str, Any] | None = None,
    ) -> list[str]:
        """生成测试用例的描述部分。

        由 Jinja2 模板 ``tc_description.j2`` 渲染，避免手工拼接缩进。

        Args:
            api_url: API URL
            service_package: 服务包名称
            severity: 测试用例严重级别，可选值：NORMAL、CRITICAL、MINOR、MAJOR、BLOCKER
            api_description: 接口名称/描述
            param_remarks: 参数备注字典
            api_headers: API 文件中的 headers 字典，用于生成类级别 headers 属性

        Returns:
            描述语句列表
        """
        description = ""
        if api_description:
            description = self._generate_allure_description(api_url, api_description, param_remarks)
        header_items = []
        if api_headers:
            header_items = [(key, header_value_formatter(value)) for key, value in api_headers.items()]

        content = render_lines(
            "tc_description.j2",
            severity=severity,
            service_package=service_package,
            api_url=api_url,
            description=description,
            header_items=header_items,
        )
        # 与旧实现一致：描述段以空行结束，作为与后续代码块的间隔
        if not content or content[-1] != "":
            content.append("")
        return content

    # ==================== 参数化测试辅助方法 ====================

    def _generate_parametrized_test_methods(
        self,
        param_items: list[dict[str, Any]],
        api_description: str,
        function_name: str,
        param_var_name: str,
        param_remarks: dict[str, Any],
    ) -> list[str]:
        """生成参数化测试方法。

        Args:
            param_items: 参数化数据列表
            api_description: API 描述信息
            function_name: API 函数名称（带下划线前缀）
            param_var_name: 调用参数名（data 或 params，由 API 文件结构决定）
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
            # 组合参数判定：名称含逗号 且 取值为列表嵌套结构（HAR 流生成的组合参数）
            # 避免将名称本身含逗号的 Swagger 参数误判为组合参数
            is_combination = (
                "," in param_name
                and bool(param_values)
                and isinstance(param_values[0], list)
            )

            content.extend(self._generate_parametrize_decorator(param_name, param_values, is_combination))
            content.extend(
                self._generate_test_method_definition(
                    api_description, param_name, param_remarks, clean_function_name, idx, is_combination
                )
            )
            content.extend(self._generate_test_method_body(param_var_name, param_name, other_params, is_combination))
            content.extend(self._generate_test_method_assertions(function_name, param_var_name, param_name))

        return content

    def _generate_parametrize_decorator(
        self, param_name: str, param_values: list[Any], is_combination: bool
    ) -> list[str]:
        """生成 @pytest.mark.parametrize 装饰器。

        由 Jinja2 模板 ``p_parametrize_decorator.j2`` 渲染，避免手工拼接缩进。

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
            arg_names = ", ".join(safe_names)
        else:
            arg_names = sanitize_param_name(param_name)
        return render_lines(
            "p_parametrize_decorator.j2",
            arg_names=arg_names,
            values=parametrize_values,
        )

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
        """生成参数化测试方法定义（标题 + def 行）。

        由 Jinja2 模板 ``p_test_method_definition.j2`` 渲染。

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
        if is_combination:
            param_names = param_name.split(",")
            safe_names = [sanitize_param_name(p) for p in param_names]
            param_descriptions = []
            for p in param_names:
                # 备注可能含换行（多行 Swagger 描述），压成单行后再拼进字符串字面量
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

        def_prefix = "    async def " if self.async_mode else "    def "
        return render_lines(
            "p_test_method_definition.j2",
            api_description=sanitize_remark(api_description),
            title_param=title_param,
            def_prefix=def_prefix,
            clean_name=clean_function_name,
            idx=param_count,
            safe_names=safe_names,
        )

    def _generate_test_method_body(
        self, param_var_name: str, param_name: str, other_params: dict[str, Any], is_combination: bool
    ) -> list[str]:
        """生成测试方法体。

        由 Jinja2 模板 ``p_method_body.j2`` 渲染（内部复用 ``p_data_dict.j2``），
        避免手工拼接缩进。

        Args:
            param_var_name: 参数变量名（params 或 data）
            param_name: 参数名称
            other_params: 其他参数字典
            is_combination: 是否为组合参数

        Returns:
            测试方法体代码行列表
        """
        ctx = self._param_dict_context(param_name, other_params, is_combination)
        body_lines = render_lines(
            "p_method_body.j2",
            leading_blank=False,
            param_var_name=param_var_name,
            **ctx,
        )
        # 方法体第一行为空行（与 def 行之间留白），与旧实现保持一致
        return ["", *body_lines]

    def _param_dict_context(
        self, param_name: str, other_params: dict[str, Any], is_combination: bool
    ) -> dict[str, Any]:
        """构建参数化数据字典模板的渲染上下文（p_method_body/p_data_dict 共用）。"""
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

    @staticmethod
    def _is_time_param(param_name: str) -> bool:
        """判断参数是否为时间类参数。

        Args:
            param_name: 参数名称

        Returns:
            是否为时间类参数
        """
        lower = param_name.lower()
        return any(kw in lower for kw in ("time", "date", "starttime", "endtime"))

    def _generate_test_method_assertions(self, function_name: str, param_var_name: str, param_name: str = "") -> list[str]:
        """生成测试方法断言部分。

        由 Jinja2 模板 ``p_test_method_assertions.j2`` 渲染。

        Args:
            function_name: API 函数名称
            param_var_name: 参数变量名（params 或 data）
            param_name: 当前参数化的参数名，用于生成搜索条件验证断言

        Returns:
            断言代码行列表
        """
        search_enabled = bool(param_name) and not self._is_time_param(param_name) and "," not in param_name
        safe_name = sanitize_param_name(param_name) if param_name else ""
        verify_assert = ""
        if search_enabled:
            verify_assert = (
                f"assert str(v) == str({safe_name}), "
                f"f'字段 {{k}} 值 {{v}} 与搜索条件 {safe_name}={{{safe_name}}} 不一致'"
            )
        content = render_lines(
            "p_test_method_assertions.j2",
            async_mode=self.async_mode,
            function_name=function_name,
            param_var=param_var_name,
            search_enabled=search_enabled,
            search_param=param_name.lower() if search_enabled else "",
            verify_assert=verify_assert,
        )
        # 与旧实现一致：断言块后补空行分隔下一个测试方法
        content.append("")
        return content
