import os
from typing import Any

from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .swagger_handler import SwaggerHandler
from .url_matcher import URLMatcher
from .utils import (
    deduplicate_values,
    format_params_for_python,
    get_output_dir,
    parse_api_file,
    write_test_file,
)


class TestCaseGenerator:
    """pytest 测试用例生成器类。

    负责从 HAR 文件解析请求，匹配 API 文件，并生成相应的 pytest 测试用例。

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
        api_dir: str = None,
        output_dir: str = None,
        filter_duplicate_url: bool = False,
        base_urls: list[str] = None,
        kill_urls: list[str] = None,
    ):
        """初始化测试用例生成器。

        Args:
            api_dir: API 文件目录路径，默认为配置的默认目录
            output_dir: 测试用例输出目录路径，默认为配置的测试用例目录
            filter_duplicate_url: 是否过滤重复 URL，默认为 False
            base_urls: 基础 URL 列表，用于 HAR 解析时过滤
            kill_urls: 需要排除的 URL 列表
        """
        self.api_dir = api_dir or APIConfig.DEFAULT_API_DIR()
        self.output_dir = output_dir or APIConfig.TESTCASE_DIR()
        self.filter_duplicate_url = filter_duplicate_url
        self.har_parser = HARParser(base_urls=base_urls, kill_urls=kill_urls)
        self.swagger_handler = SwaggerHandler()
        self.url_matcher = URLMatcher()
        # API文件缓存
        self._api_file_cache = {}

    def _get_api_file_info(self, api_file: str) -> dict:
        """获取 API 文件信息（带缓存）。

        Args:
            api_file: API 文件路径

        Returns:
            API 文件信息字典，包含 function_name、url、description 等字段
        """
        if api_file not in self._api_file_cache:
            self._api_file_cache[api_file] = parse_api_file(api_file)
        return self._api_file_cache[api_file]

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

    def _get_swagger_doc_for_url(self, url: str) -> dict | None:
        """根据 URL 获取对应的 Swagger 文档。

        Args:
            url: 请求 URL

        Returns:
            Swagger 文档字典，如果未找到则返回 None
        """
        service_package = APIConfig.determine_service_package(url)
        swagger_url = APIConfig.SWAGGER_DOC_URLS().get(service_package)
        return self.swagger_handler.get_swagger_doc(swagger_url) if swagger_url else None

    def _prepare_url_matcher(self, url: str) -> None:
        """为指定 URL 准备 URLMatcher。

        根据 URL 获取对应的 Swagger 文档，并设置到 url_matcher 中，
        以便后续进行 URL 模式匹配和参数提取。

        Args:
            url: 请求 URL
        """
        swagger_doc = self._get_swagger_doc_for_url(url)
        self.url_matcher.swagger_data = swagger_doc

    def match_api_files_for_har(self, har_file_path: str) -> list[str]:
        """根据 HAR 文件查找对应的 API 文件。

        Args:
            har_file_path: HAR 文件路径

        Returns:
            匹配到的 API 文件路径列表
        """
        requests = self.har_parser.extract_requests_from_har(har_file_path)

        # 预处理URL映射
        request_url_map = {}
        for request in requests:
            request_url = request["url"]
            self._prepare_url_matcher(request_url)
            url_info = self.url_matcher.get_url_info(request_url)
            request_url_map[request_url] = url_info["pattern"] or request_url

        api_files_list = self._get_all_api_files()

        matched_files = []
        for request in requests:
            matched_file = URLMatcher.find_matching_api_file(request["url"], api_files_list, request_url_map)
            if matched_file and matched_file not in matched_files:
                matched_files.append(matched_file)

        return matched_files

    def extract_params_from_har_request(self, request_info: dict[str, Any]) -> dict[str, Any] | None:
        """从 HAR 请求信息中提取参数字典。

        从 HAR 请求中提取查询参数、POST 数据和路径参数，合并为统一的参数字典。

        Args:
            request_info: HAR 请求信息字典，包含 method、url、post_data、query_params 等字段

        Returns:
            参数字典，如果没有有效参数则返回 None
        """
        method = request_info["method"].upper()
        url = request_info["url"]
        post_data = request_info.get("post_data")
        query_params = request_info.get("query_params", {})

        params = {}

        if query_params:
            params.update(query_params)

        if method == "POST" and post_data and isinstance(post_data, dict):
            params.update(post_data)

        # 提取路径参数
        self._prepare_url_matcher(url)
        _, path_params, _ = self.url_matcher.match_with_swagger(url)
        if path_params:
            params.update(path_params)

        return params if params else None

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

    def normalize_params_for_parametrization(self, requests_params: list[dict[str, Any]]) -> list[dict]:
        """标准化参数化数据结构。

        将多个请求的参数整理为适合 pytest 参数化的格式，支持单参数和组合参数。

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

    def _extract_requests_for_url(self, requests: list, api_url: str) -> tuple[set, list, str]:
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
        request_method = "GET"

        normalized_api_url = URLMatcher.normalize_url(api_url)

        for req in requests:
            normalized_req_url = URLMatcher.normalize_url(req["url"])

            if normalized_req_url == normalized_api_url:
                api_params = self.extract_params_from_har_request(req)
                if isinstance(api_params, dict) and api_params:
                    all_requests_params.append(api_params)

                    for param_name, param_value in api_params.items():
                        if self._is_valid_param(param_value):
                            all_params.add(param_name)

                if request_method == "GET":
                    request_method = req.get("method", "GET")

        return all_params, all_requests_params, request_method

    def _find_target_api_file(self, api_files: list[str], target_url: str) -> str | None:
        """查找目标 API 文件。

        从 API 文件列表中查找与目标 URL 匹配的 API 文件。

        Args:
            api_files: API 文件路径列表
            target_url: 目标 URL

        Returns:
            匹配的 API 文件路径，如果未找到则返回 None
        """
        for api_file in api_files:
            api_info = self._get_api_file_info(api_file)
            file_url = api_info.get("url")
            if not file_url:
                continue

            if file_url == target_url:
                return api_file

            matched, _ = URLMatcher.match_url_pattern(target_url, file_url)
            if matched:
                return api_file

            matched, _ = URLMatcher.match_url_pattern(file_url, target_url)
            if matched:
                return api_file

            if URLMatcher.normalize_url(file_url) == URLMatcher.normalize_url(target_url):
                return api_file

        return None

    def generate_test_case_from_har(self, har_file_path: str, output_subdir: str = None) -> str | None:
        """从 HAR 文件生成 pytest 用例文件。

        Args:
            har_file_path: HAR 文件路径
            output_subdir: 输出子目录名称

        Returns:
            生成的测试用例文件路径，如果生成失败则返回 None
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None

        api_files = self.match_api_files_for_har(har_file_path)
        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return None

        output_dir = get_output_dir(self.output_dir, output_subdir)
        test_filename = f"test_{os.path.splitext(os.path.basename(har_file_path))[0]}.py"
        test_filepath = os.path.join(output_dir, test_filename)

        test_content = self.generate_test_case_content(har_file_path, api_files)
        write_test_file(test_filepath, test_content)

        return test_filepath

    def generate_parametrized_list_testcases(self, har_file_path: str, task_id: str) -> list[str]:
        """生成查询类参数化测试用例。

        为每个匹配的 API 生成独立的参数化测试文件。

        Args:
            har_file_path: HAR 文件路径
            task_id: 任务 ID，用于命名输出目录

        Returns:
            生成的测试用例文件路径列表
        """
        if not os.path.exists(har_file_path):
            return []

        api_files = self.match_api_files_for_har(har_file_path)
        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return []

        if task_id and task_id.startswith("test_"):
            task_id = task_id[5:]

        output_dir = get_output_dir(self.output_dir, task_id)
        generated_files = []

        for api_file in api_files:
            try:
                api_info = self._get_api_file_info(api_file)
                clean_function_name = api_info["function_name"].lstrip("_")
                test_filename = f"test_{clean_function_name}.py"
                test_filepath = os.path.join(output_dir, test_filename)

                test_content = self.generate_parametrized_test_content(har_file_path, api_file, task_id)
                if not test_content:
                    continue

                write_test_file(test_filepath, test_content)
                generated_files.append(test_filepath)
            except Exception as e:
                logger.error(f"生成测试用例文件失败 {api_file}: {str(e)}")

        return generated_files

    def generate_parametrized_test_content(self, har_file_path: str, api_file: str, task_id: str) -> str | None:
        """生成参数化测试用例内容。

        Args:
            har_file_path: HAR 文件路径
            api_file: API 文件路径
            task_id: 任务 ID

        Returns:
            参数化测试用例内容字符串，如果生成失败则返回 None
        """
        api_info = self._get_api_file_info(api_file)
        function_name = api_info["function_name"]

        if not function_name:
            return None

        requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

        all_params, all_requests_params, request_method = self._extract_requests_for_url(requests, api_info["url"])

        if not all_requests_params:
            return None

        module_path = api_file.replace(".py", "").replace("\\", ".").replace("/", ".")
        service_package = module_path.split(".")[1] if len(module_path.split(".")) > 1 else "default"
        clean_function_name = function_name.lstrip("_")

        # 生成测试用例内容
        content = self._generate_test_case_imports(service_package, function_name, task_id)
        content.extend(
            self._generate_test_case_description(
                api_info["description"], api_info["url"], service_package, all_params, api_info["param_remarks"]
            )
        )
        content.extend(self._generate_test_class_setup())

        param_items = self.normalize_params_for_parametrization(all_requests_params)
        content.extend(
            self._generate_parametrized_test_methods(
                param_items, api_info["description"], clean_function_name, request_method, api_info["param_remarks"]
            )
        )

        return "\n".join(content)

    def generate_scenario_testcase(self, har_file_path: str, target_url: str, task_id: str) -> str | None:
        """生成复杂场景流程测试用例。

        针对指定的目标 URL 生成场景化的流程测试用例。

        Args:
            har_file_path: HAR 文件路径
            target_url: 目标 URL
            task_id: 任务 ID

        Returns:
            生成的测试用例文件路径，如果生成失败则返回 None
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None

        api_files = self.match_api_files_for_har(har_file_path)
        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return None

        if task_id and task_id.startswith("test_"):
            task_id = task_id[5:]

        target_api_file = self._find_target_api_file(api_files, target_url)
        if not target_api_file:
            logger.info(f"未找到指定URL对应的API文件: {target_url}")
            return None

        output_dir = get_output_dir(self.output_dir, task_id)
        api_info = self._get_api_file_info(target_api_file)
        clean_function_name = api_info["function_name"].lstrip("_")
        test_filename = f"test_{clean_function_name}.py"
        test_filepath = os.path.join(output_dir, test_filename)

        test_content = self.generate_test_case_content(har_file_path, api_files, task_id, target_api_file, target_url)

        if not test_content:
            return None

        write_test_file(test_filepath, test_content)
        return test_filepath

    # 以下方法保持不变，只是添加缓存优化
    def generate_test_case_content(
        self,
        har_file_path: str,
        api_files: list[str],
        task_id: str = None,
        target_api_file: str = None,
        target_url: str = None,
    ) -> str:
        """生成 pytest 用例文件内容。

        Args:
            har_file_path: HAR 文件路径
            api_files: API 文件路径列表
            task_id: 任务 ID
            target_api_file: 目标 API 文件路径（可选）
            target_url: 目标 URL（可选）

        Returns:
            测试用例文件内容字符串
        """
        # 此方法保持原有实现不变，只添加缓存优化
        requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

        # 预加载所有API文件信息到缓存
        for api_file in api_files:
            self._get_api_file_info(api_file)

        content = [
            "import os",
            "import pytest",
            "import allure",
            "from allure_commons.types import Severity",
            "",
        ]

        imports = []
        for api_file in api_files:
            module_path = api_file.replace(".py", "").replace("\\", ".").replace("/", ".")
            result = parse_api_file(api_file)
            function_name = result["function_name"]
            if function_name:
                # 提取服务包名称（apis.mall_center_user._xxx -> mall_center_user）
                parts = module_path.split(".")
                if len(parts) >= 2:
                    service_package = parts[1]
                    imports.append(f"from apis.{service_package} import {function_name}")
                else:
                    imports.append(f"from {module_path} import {function_name}")

        if imports:
            content.extend(imports)
            content.append("")

        # 提取接口信息
        feature_name = "建议输入被测接口所属的微服务，如 mall_store_application"
        story_name = "建议输入被测接口，如 /appStore/order/orderSign/signCommit"
        title_name = "建议输入测试用例名称，如 提交订单"

        if target_api_file:
            # 提取服务名称
            module_path = target_api_file.replace(".py", "").replace("\\", ".").replace("/", ".")
            if len(module_path.split(".")) > 1:
                feature_name = module_path.split(".")[1]

            # 提取接口描述和URL
            result = parse_api_file(target_api_file)
            api_description = result["description"]
            api_url = result["url"]
            if api_description:
                title_name = api_description
            if api_url:
                story_name = api_url

        # 添加测试标记和接口说明
        if task_id:
            content.append(f"@pytest.mark.test_{task_id}")

        content.extend(
            [
                "@allure.severity(Severity.CRITICAL)",
                f"@allure.feature('{feature_name}')",
                f"@allure.story('{story_name}')",
                f"@allure.title('{title_name}')",
            ]
        )

        # 生成测试函数名称
        if target_api_file:
            clean_function_name = parse_api_file(target_api_file)["function_name"].lstrip("_")
            test_function_name = f"def test_{clean_function_name}():"
        else:
            test_function_name = "def test_har_api_flow():"
        content.append(test_function_name)

        content.extend(
            [
                "",
                "    # 初始化测试数据字典，用于在步骤间传递数据",
                "    test_data = {",
                '        "headers": {',
                '            "channel": "pc",',
                '            "client": "op",',
                '            "content-type": "application/json;charset=UTF-8",',
                '            "authorization": f"bearer {os.environ[\'access_token\']}",',
                "        },",
                "    }",
                "",
            ]
        )

        step_functions = []
        name_counters = {}
        for i, request_info in enumerate(requests):
            url = request_info["url"]
            method = request_info["method"]

            api_function = None
            api_description = None
            for api_file in api_files:
                result = parse_api_file(api_file)
                file_url = result["url"]
                # 1. 直接相等匹配
                if file_url == url:
                    api_function = result["function_name"]
                    api_description = result["description"]
                    break
                # 2. 如果API文件URL包含路径参数模板，尝试匹配
                elif file_url and "{" in file_url and "}" in file_url:
                    url_pattern, _, _ = URLMatcher({"paths": {file_url: {}}}).match_with_swagger(url)
                    if url_pattern == file_url:
                        api_function = result["function_name"]
                        api_description = result["description"]
                        break

            if api_function:
                clean_function_name = api_function.lstrip("_")

                if clean_function_name not in name_counters:
                    name_counters[clean_function_name] = 0

                count = name_counters[clean_function_name]

                if count == 0:
                    step_name = f"step_{clean_function_name}"
                else:
                    step_name = f"step_{count}_{clean_function_name}"

                name_counters[clean_function_name] += 1

                step_functions.append(step_name)

                function_parts = clean_function_name.split("_")
                if len(function_parts) >= 2:
                    data_key = "_".join(function_parts[-2:])
                else:
                    data_key = function_parts[0] if function_parts else f"response_{i + 1}"

                api_params = self.extract_params_from_har_request(request_info)
                if api_params:
                    api_params = format_params_for_python(api_params)

                content.extend([f'    @allure.step("{api_description}")', f"    def {step_name}():", ""])

                if api_params:
                    content_type = request_info.get("content_type", "")
                    is_file_upload = method == "POST" and content_type.startswith("multipart/form-data")

                    if is_file_upload:
                        # 处理文件上传请求
                        content.extend(
                            [
                                "        files = {",
                            ]
                        )

                        # 添加原始参数
                        if api_params:
                            params_lines = api_params.strip().split("\n")
                            # 跳过第一行（" {"）和最后一行（"        }"）
                            for line in params_lines[1:-1]:
                                if line.strip():
                                    content.append(f"            {line}")

                        # 添加文件参数
                        content.extend(['            "file": "data/示例文件.png"', "        }"])
                        content.extend(
                            [f"        with {api_function}(files=files, headers=test_data['headers']) as r:"]
                        )
                    elif method == "POST":
                        content.extend(
                            [
                                f"        data = {api_params}",
                                f"        with {api_function}(data=data, headers=test_data['headers']) as r:",
                            ]
                        )
                    else:
                        content.extend(
                            [
                                f"        params = {api_params}",
                                f"        with {api_function}(params=params, headers=test_data['headers']) as r:",
                            ]
                        )
                else:
                    content_type = request_info.get("content_type", "")
                    is_file_upload = method == "POST" and content_type.startswith("multipart/form-data")

                    if is_file_upload:
                        content.extend(
                            [
                                "        files = {",
                                '            "storageType": "PublicCloud",',
                                '            "clientKey": "mall-center-product",',
                                '            "file": "data/示例文件.png"',
                                "        }",
                                f"        with {api_function}(files=files, headers=test_data['headers']) as r:",
                            ]
                        )
                    else:
                        content.extend([f"        with {api_function}(headers=test_data['headers']) as r:"])

                content.extend(
                    [
                        "            assert r.status_code == 200",
                        "            assert r.json()['code'] == 200",
                        f"            test_data['{data_key}'] = r.json()",
                        "",
                    ]
                )

        if step_functions:
            content.append("    # 执行所有测试步骤")
            for step_func in step_functions:
                content.append(f"    {step_func}()")
            content.append("")

        return "\n".join(content)

    def _generate_test_case_imports(self, service_package: str, function_name: str, task_id: str) -> list[str]:
        """生成测试用例的导入部分。

        Args:
            service_package: 服务包名称
            function_name: API 函数名称
            task_id: 任务 ID

        Returns:
            导入语句列表
        """
        content = [
            "import os",
            "import pytest",
            "import allure",
            "from allure_commons.types import Severity",
            "",
            f"from apis.{service_package} import {function_name}",
            "",
        ]
        if task_id:
            content.append(f"@pytest.mark.test_{task_id}")
        return content

    def _generate_test_case_description(
        self, api_description: str, api_url: str, service_package: str, all_params: set, param_remarks: dict
    ) -> list[str]:
        """生成测试用例的描述部分。

        Args:
            api_description: API 描述信息
            api_url: API URL
            service_package: 服务包名称
            all_params: 参数名集合
            param_remarks: 参数备注字典

        Returns:
            描述语句列表
        """
        content = [
            f"@allure.feature('{service_package}')",
            f"@allure.story('{api_url}')",
            f'@allure.description("""接口说明：\n- 接口名称：{api_description}',
            f"- 接口地址：{api_url}",
            "",
            "主要参数说明：",
        ]

        for param_name in all_params:
            remark = param_remarks.get(param_name, "# TODO 请填写参数备注")
            if "TODO" in remark:
                remark = "# TODO 请填写参数备注"
            content.append(f"- {param_name}：{remark}")

        content.append('""")')
        return content

    def _generate_test_class_setup(self) -> list[str]:
        """生成测试类的 setup 方法。

        Returns:
            setup 方法代码行列表
        """
        return [
            "class TestClass:",
            "",
            "    def setup_class(self):",
            "        self.headers = {",
            '            "channel": "pc",',
            '            "client": "op",',
            '            "content-type": "application/json;charset=UTF-8",',
            '            "authorization": f"bearer {os.environ[\'access_token\']}",',
            "        }",
            "",
        ]

    def _generate_parametrized_test_methods(
        self,
        param_items: list,
        api_description: str,
        clean_function_name: str,
        request_method: str,
        param_remarks: dict,
    ) -> list[str]:
        """生成参数化测试方法。

        Args:
            param_items: 参数化数据列表
            api_description: API 描述信息
            clean_function_name: 清理后的函数名称
            request_method: 请求方法
            param_remarks: 参数备注字典

        Returns:
            参数化测试方法代码行列表
        """
        content = []

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
            content.extend(self._generate_test_method_assertions(clean_function_name, param_var_name))

        return content

    def _generate_parametrize_decorator(self, param_name: str, param_values: list, is_combination: bool) -> list[str]:
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
            param_names = param_name.split(",")
            decorator_line = f'    @pytest.mark.parametrize("{", ".join(param_names)}, p", ['
        else:
            decorator_line = f'    @pytest.mark.parametrize("{param_name}, p", ['

        content = [decorator_line]
        for i, value in enumerate(parametrize_values):
            suffix = "" if i == len(parametrize_values) - 1 else ","
            content.append(f"        {value}{suffix}")
        content.append("    ])")
        return content

    def _generate_parametrize_values(self, param_values, is_combination):
        """生成参数化值列表。

        Args:
            param_values: 参数值列表
            is_combination: 是否为组合参数

        Returns:
            格式化后的参数化值列表
        """
        parametrize_values = []
        if is_combination:
            for value_tuple in param_values:
                formatted_values = [self._format_value(v) for v in value_tuple]
                formatted_values.append("Severity.NORMAL")
                parametrize_values.append(f"({', '.join(formatted_values)})")
        else:
            for value in param_values:
                formatted_value = self._format_value(value)
                parametrize_values.append(f"({formatted_value}, Severity.NORMAL)")
        return parametrize_values

    @staticmethod
    def _format_value(value: Any) -> str:
        """格式化单个值为 Python 字符串表示。

        Args:
            value: 需要格式化的值

        Returns:
            格式化后的字符串
        """
        if value is None:
            return "None"
        if isinstance(value, str):
            return f'"{value}"'
        return str(value)

    def _generate_test_method_definition(
        self,
        api_description: str,
        param_name: str,
        param_remarks: dict,
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
        if is_combination:
            param_names = param_name.split(",")
            param_descriptions = []
            for p in param_names:
                desc = param_remarks.get(p, p)
                if "-" in desc:
                    desc = desc.split("-")[0]
                param_descriptions.append(desc)
            param_desc_str = "-".join(param_descriptions)
            return [
                f'    @allure.title("{api_description}-成功路径: {param_desc_str} 查询")',
                f"    def test_{param_count}_{clean_function_name}(self, {', '.join(param_names)}, p):",
            ]
        else:
            param_description = param_remarks.get(param_name, param_name)
            if " " in param_description:
                param_description = param_description.split(" ")[0]
            return [
                f'    @allure.title("{api_description}-成功路径: {param_description} 查询")',
                f"    def test_{param_count}_{clean_function_name}(self, {param_name}, p):",
            ]

    def _generate_test_method_body(
        self, param_var_name: str, param_name: str, other_params: dict, is_combination: bool
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
            "        # 用例级别",
            "        allure.dynamic.severity(p)",
            "",
            f"        {param_var_name} = {{",
        ]
        self._generate_data_dict(content, param_name, other_params, is_combination, param_var_name)
        content.append("        }")
        return content

    def _generate_data_dict(
        self, content: list, param_name: str, other_params: dict, is_combination: bool, param_var_name: str
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
                content.append(f'            "{key}": {key},')
        else:
            content.append(f'            "{param_name}": {param_name},')

        for key, value in other_params.items():
            if isinstance(value, str):
                content.append(f'            "{key}": "{value}",')
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
        return [
            f"        with {function_name}(data={param_var_name}, headers=self.headers) as r:",
            "            assert r.status_code == 200",
            "            assert r.json()['code'] == 200",
            "",
        ]
