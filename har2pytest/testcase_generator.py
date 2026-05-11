import os
from typing import Any

from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .swagger_handler import SwaggerHandler
from .url_matcher import URLMatcher
from .utils import (
    deduplicate_values,
    format_headers_for_python,
    format_parameter_value,
    get_function_name_from_api_file,
    get_headers_from_api_file,
    get_output_dir,
    get_param_remarks_from_api_file,
    get_url_from_api_file,
    write_test_file,
)


class TestCaseGenerator:
    """pytest用例生成器类"""

    def __init__(
        self,
        api_dir: str = None,
        output_dir: str = None,
        filter_duplicate_url=False,
        base_urls: list[str] = None,
        kill_urls: list[str] = None,
    ):
        """
        初始化用例生成器
        """
        if api_dir is None:
            api_dir = APIConfig.DEFAULT_API_DIR()
        if output_dir is None:
            output_dir = APIConfig.TESTCASE_DIR()
        self.api_dir = api_dir
        self.output_dir = output_dir
        self.filter_duplicate_url = filter_duplicate_url
        self.har_parser = HARParser(base_urls=base_urls, kill_urls=kill_urls)
        self.swagger_handler = SwaggerHandler()
        self.url_matcher = URLMatcher()

    def _get_all_api_files(self) -> list[str]:
        """
        获取所有API文件路径
        
        Returns:
            list[str]: API文件路径列表
        """
        api_files = []
        if not os.path.exists(self.api_dir):
            logger.warning(f"API目录不存在: {self.api_dir}")
            return api_files
        
        for root, dirs, files in os.walk(self.api_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    api_files.append(os.path.join(root, file))
        
        return api_files

    def _get_clean_function_name(self, filepath: str) -> str:
        """
        获取清理后的函数名
        """
        function_name = get_function_name_from_api_file(filepath)
        if function_name:
            return function_name.lstrip("_").strip()
        return os.path.splitext(os.path.basename(filepath))[0].lstrip("_").strip()

    def _get_headers_str(self, api_file: str = None) -> str:
        """
        从API文件或配置文件中获取需要包含的 headers，生成测试用例中的 headers 字符串

        优先从API文件中提取 headers，如果没有提供API文件或提取失败，则使用配置文件中的默认值

        Args:
            api_file: API文件路径，可选

        Returns:
            headers 字符串，用于测试用例中
        """
        api_headers = {}
        if api_file:
            api_headers = get_headers_from_api_file(api_file)

        default_headers = APIConfig.HEADERS_TO_INCLUDE()

        headers_config = {**default_headers, **api_headers}

        return format_headers_for_python(headers_config)

    def match_api_files_for_har(self, har_file_path: str) -> list[str]:
        """根据HAR文件查找对应的API文件（优化版）"""
        requests = self.har_parser.extract_requests_from_har(har_file_path)
        
        # 使用URLMatcher预处理所有请求URL
        request_url_map = {}
        for request in requests:
            request_url = request["url"]
            # 获取Swagger数据
            swagger_data = self.swagger_handler.get_swagger_data_for_url(request_url)
            self.url_matcher.swagger_data = swagger_data
            
            # 使用统一的匹配器获取URL信息
            url_info = self.url_matcher.get_url_info(request_url)
            transformed_url = url_info["pattern"] or request_url
            request_url_map[request_url] = transformed_url
        
        # 获取所有API文件
        api_files_list = self._get_all_api_files()
        
        # 使用统一的URL匹配服务查找匹配的API文件
        matched_files = []
        for request in requests:
            request_url = request["url"]
            matched_file = self._find_matching_api_file_unified(
                request_url, api_files_list, request_url_map
            )
            if matched_file and matched_file not in matched_files:
                matched_files.append(matched_file)
        
        logger.debug(f"匹配到的API文件: {matched_files}")
        return matched_files

    def _find_matching_api_file_unified(
        self, 
        request_url: str, 
        api_files: list[str], 
        request_url_map: dict = None
    ) -> str | None:
        """
        统一的API文件查找方法
        
        Args:
            request_url: 请求URL
            api_files: API文件路径列表
            request_url_map: 请求URL到转换后URL的映射
            
        Returns:
            Optional[str]: 匹配的API文件路径
        """
        # 获取转换后的URL
        transformed_url = request_url_map.get(request_url, request_url) if request_url_map else request_url
        
        # 为每个API文件创建匹配器（避免重复创建）
        for api_file in api_files:
            result = get_url_from_api_file(api_file)
            if not result:
                continue
                
            _, file_url = result
            
            # 三种匹配方式
            # 1. 直接匹配
            if request_url == file_url:
                return api_file
            
            # 2. 转换后匹配
            if transformed_url == file_url:
                return api_file
            
            # 3. 使用URLMatcher进行模板匹配
            matched, _ = URLMatcher.match_url_pattern(request_url, file_url)
            if matched:
                return api_file
        
        return None

    def extract_params_from_har_request(self, request_info: dict[str, Any]) -> dict[str, Any] | None:
        """
        从HAR请求信息中提取参数字典（包括路径参数）
        """
        method = request_info["method"].upper()
        url = request_info["url"]
        post_data = request_info.get("post_data")
        query_params = request_info.get("query_params", {})

        # 合并所有参数
        params = {}

        # 添加查询参数
        if query_params:
            params.update(query_params)

        # 添加POST数据
        if method == "POST" and post_data and isinstance(post_data, dict):
            params.update(post_data)

        # 从URL中提取路径参数（使用Swagger文档）
        swagger_data = self.swagger_handler.get_swagger_data_for_url(url)
        _, path_params, _ = URLMatcher(swagger_data).match_with_swagger(url)
        if path_params:
            params.update(path_params)

        return params if params else None

    def format_test_case_params(self, params_dict: dict[str, Any]) -> str:
        """
        格式化参数为测试用例中的参数字符串
        """
        if not params_dict:
            return "{}"

        items = []
        for key, value in params_dict.items():
            formatted_value = format_parameter_value(value)
            items.append(f'"{key}": {formatted_value}')

        return "{" + ", ".join(items) + "}"

    def normalize_params_for_parametrization(self, requests_params: list[dict[str, Any]]):
        """
        将 requests_params 中的数据处理成标准样式的数据结构，用于生成参数化测试用例

        处理逻辑：
        1. 遍历每个请求，分离有效参数和其他参数（分页参数、空值参数）
        2. 有效参数：非 None、非空字符串、非空列表，且不在 PAGINATION_PARAMS 中
        3. 根据有效参数数量决定处理方式：
           - 单个有效参数：作为独立参数处理
           - 多个有效参数：作为组合参数处理（参数名用逗号连接）
        4. 对参数值进行去重处理
        5. 返回标准化的参数化结构

        Args:
            requests_params: 包含多个参数字典的列表，每个字典代表一个请求的参数

        Returns:
            list: 处理后的结果列表，每个元素包含参数名、参数值列表和其他参数

        Example:
            输入：
            requests_params = [
                {"customerType": 1, "page": 1, "pageSize": 10},
                {"customerType": 2, "page": 1, "pageSize": 10},
                {"customerType": 3, "page": 1, "pageSize": 10},
                {"creatorCard": "A123", "page": 1, "pageSize": 10},
                {"startDate": "2026-01-01", "endDate": "2026-01-31", "page": 1},
                {"startDate": "2026-02-01", "endDate": "2026-02-28", "page": 1},
            ]

            输出：
            [
                {"customerType": [1, 2, 3], "other_params": {"page": 1, "pageSize": 10}},
                {"creatorCard": ["A123"], "other_params": {"page": 1, "pageSize": 10}},
                {"startDate,endDate": [("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")], "other_params": {"page": 1}},
            ]

            说明：
            - customerType 参数有3个不同值，被参数化
            - creatorCard 参数有1个值，被参数化
            - startDate 和 endDate 同时出现，作为组合参数处理
            - page、pageSize 属于分页参数，被放入 other_params
        """

        # 用于收集所有参数值
        # key: 参数名或组合参数名（如 "hxTimeBegin,hxTimeEnd"）
        # value: {"values": [], "other_params": {}}
        param_value_map = {}

        # 收集所有参数值
        for req in requests_params:
            # 收集当前请求中所有非 None 且非空字符串的参数
            valid_params = {}
            # 收集其他参数（None 或空字符串）
            other_params = {}

            for param_name, param_value in req.items():
                # 只处理指定的参数之外的其他参数
                if param_name not in APIConfig.PAGINATION_PARAMS():
                    # 非 None、非空字符串且非空列表的值视为有效参数
                    is_valid = param_value is not None and param_value != ""
                    # 额外检查：如果是列表或集合，必须非空才视为有效参数
                    if isinstance(param_value, (list, set)):
                        is_valid = is_valid and len(param_value) > 0
                    if is_valid:
                        valid_params[param_name] = param_value
                    else:
                        other_params[param_name] = param_value
                else:
                    # PAGINATION_PARAMS 中的参数总是包含在 other_params 中
                    other_params[param_name] = param_value

            # 如果有多个有效参数，认为是组合参数
            if len(valid_params) > 1:
                # 对参数名进行排序，确保相同参数组合的顺序一致
                sorted_param_names = sorted(valid_params.keys())
                # 创建组合参数的 key
                combination_key = ",".join(sorted_param_names)
                # 创建组合参数的值列表
                combination_value = [valid_params[param_name] for param_name in sorted_param_names]

                # 添加到 param_value_map
                if combination_key not in param_value_map:
                    param_value_map[combination_key] = {"values": [], "other_params": other_params}
                param_value_map[combination_key]["values"].append(combination_value)

            elif len(valid_params) == 1:
                # 只有一个有效参数，作为单个参数处理
                param_name, param_value = list(valid_params.items())[0]

                # 添加到 param_value_map
                if param_name not in param_value_map:
                    param_value_map[param_name] = {"values": [], "other_params": other_params}
                param_value_map[param_name]["values"].append(param_value)

        # 构建最终结果
        merged_result = []
        for param_name, data in param_value_map.items():
            # 去重
            unique_values = deduplicate_values(data["values"])

            merged_item = {param_name: unique_values, "other_params": data["other_params"]}
            merged_result.append(merged_item)

        return merged_result

    def generate_test_case_content(
        self,
        har_file_path: str,
        api_files: list[str],
        task_id: str = None,
        target_api_file: str = None,
        target_url: str = None,
    ) -> str:
        """
        生成pytest用例文件内容
        """

        requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

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
            function_name = get_function_name_from_api_file(api_file)
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
            api_description, api_url = get_url_from_api_file(target_api_file)
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
            clean_function_name = self._get_clean_function_name(target_api_file)
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
            for api_file in api_files:
                _, file_url = get_url_from_api_file(api_file)
                # 1. 直接相等匹配
                if file_url == url:
                    api_function = get_function_name_from_api_file(api_file)
                    break
                # 2. 如果API文件URL包含路径参数模板，尝试匹配
                elif file_url and "{" in file_url and "}" in file_url:
                    url_pattern, _, _ = URLMatcher({"paths": {file_url: {}}}).match_with_swagger(url)
                    if url_pattern == file_url:
                        api_function = get_function_name_from_api_file(api_file)
                        break

            if api_function:
                api_description, _ = get_url_from_api_file(api_file)

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
                    api_params = self.format_test_case_params(api_params)

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

    def generate_test_case_from_har(self, har_file_path: str, output_subdir: str = None) -> str | None:
        """
        从HAR文件生成pytest用例文件
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None

        api_files = self.match_api_files_for_har(har_file_path)

        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return None

        logger.info(f"找到 {len(api_files)} 个对应的API文件")

        output_dir = get_output_dir(self.output_dir, output_subdir)

        test_filename = f"test_{os.path.splitext(os.path.basename(har_file_path))[0]}.py"
        test_filepath = os.path.join(output_dir, test_filename)

        test_content = self.generate_test_case_content(har_file_path, api_files)
        write_test_file(test_filepath, test_content)

        logger.info(f"生成测试用例文件: {test_filepath}")
        return test_filepath

    def generate_parametrized_list_testcases(self, har_file_path: str, task_id: str) -> list[str]:
        """
        生成查询类参数化测试用例
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return []

        api_files = self.match_api_files_for_har(har_file_path)

        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return []

        logger.info(f"找到 {len(api_files)} 个对应的API文件")

        # 处理task_id，去掉test_前缀
        if task_id and task_id.startswith("test_"):
            task_id = task_id[5:]

        # 获取输出目录
        output_dir = get_output_dir(self.output_dir, task_id)

        generated_files = []

        for api_file in api_files:
            try:
                clean_function_name = self._get_clean_function_name(api_file)
                test_filename = f"test_{clean_function_name}.py"
                test_filepath = os.path.join(output_dir, test_filename)

                # 生成参数化测试用例内容
                test_content = self.generate_parametrized_test_content(har_file_path, api_file, task_id)

                if not test_content:
                    logger.info(f"跳过文件（无法生成内容）: {api_file}")
                    continue

                write_test_file(test_filepath, test_content)

                generated_files.append(test_filepath)
                logger.info(f"生成测试用例文件: {test_filepath}")

            except Exception as e:
                logger.error(f"生成测试用例文件失败 {api_file}: {str(e)}")

        return generated_files

    def _generate_parametrize_values(self, param_values, is_combination):
        """
        生成参数化值列表
        """
        parametrize_values = []
        if is_combination:
            for value_tuple in param_values:
                # 格式化值
                formatted_values = []
                for val in value_tuple:
                    if val is None:
                        formatted_values.append("None")
                    elif isinstance(val, str):
                        formatted_values.append(f'"{val}"')
                    else:
                        formatted_values.append(str(val))
                # 添加严重程度参数
                formatted_values.append("Severity.NORMAL")
                # 组合成参数化值字符串
                parametrize_values.append(f"({', '.join(formatted_values)})")
        else:
            for value in param_values:
                if value is None:
                    value_str = "None"
                elif isinstance(value, str):
                    value_str = f'"{value}"'
                else:
                    value_str = str(value)
                parametrize_values.append(f"({value_str}, Severity.NORMAL)")
        return parametrize_values

    def _generate_data_dict(self, content, param_name, other_params, is_combination, param_var_name):
        """
        生成数据字典
        """
        if is_combination:
            param_names = param_name.split(",")
            for key in param_names:
                content.append(f'            "{key}": {key},')
        else:
            content.append(f'            "{param_name}": {param_name},')

        for key, value in other_params.items():
            if isinstance(value, str):
                content.append(f'            "{key}": "{value}",')
            else:
                content.append(f'            "{key}": {value},')

    def _generate_assertions(self, content, function_name, param_name, is_combination, param_var_name):
        """
        生成断言
        """
        content.extend(
            [
                "        }",
                f"        with {function_name}(data={param_var_name}, headers=self.headers) as r:",
                "            assert r.status_code == 200",
                "            assert r.json()['code'] == 200",
                '            data_list = r.json()["data"]["list"]',
                '            assert len(data_list) > 0, "返回数据列表为空"',
            ]
        )

        if not is_combination:
            content.extend(
                [
                    f'            if any(i.get("{param_name}") is not None for i in data_list):',
                    f'                assert any(i.get("{param_name}") == {param_name} for i in data_list)',
                ]
            )

        content.append("")

    def generate_parametrized_test_content(self, har_file_path: str, api_file: str, task_id: str) -> str | None:
        """
        生成参数化测试用例内容
        """
        function_name = get_function_name_from_api_file(api_file)
        if not function_name:
            return None
        
        # 获取API信息
        api_description, api_url = get_url_from_api_file(api_file)
        
        # 解析HAR文件获取请求信息
        requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)
        
        # 从HAR文件中提取所有参数和请求方法（使用统一方法）
        all_params, all_requests_params, request_method = self._extract_params_unified(
            requests, api_url
        )
        
        if not all_requests_params:
            return None

        # 从API文件中提取参数备注
        param_remarks = get_param_remarks_from_api_file(api_file) or {}

        # 提取服务包名称
        module_path = api_file.replace(".py", "").replace("\\", ".").replace("/", ".")
        service_package = module_path.split(".")[1] if len(module_path.split(".")) > 1 else "default"

        # 获取清理后的函数名
        clean_function_name = self._get_clean_function_name(api_file)

        # 生成测试用例内容
        content = self._generate_test_case_imports(service_package, function_name, task_id)
        content.extend(self._generate_test_case_description(api_description, api_url, service_package, all_params, param_remarks))
        content.extend(self._generate_test_class_setup())

        # 生成参数化测试方法
        param_items = self.normalize_params_for_parametrization(all_requests_params)
        content.extend(self._generate_parametrized_test_methods(param_items, api_description, clean_function_name, request_method, param_remarks))

        return "\n".join(content)

    def _extract_params_from_requests(self, requests: list, api_url: str) -> tuple:
        """
        从请求列表中提取参数和请求方法
        """
        all_params = set()
        all_requests_params = []
        request_method = "GET"

        for req in requests:
            if req["url"] == api_url:
                api_params = self.extract_params_from_har_request(req)
                if isinstance(api_params, dict):
                    all_requests_params.append(api_params)
                    for param_name, param_value in api_params.items():
                        is_valid = param_value is not None and param_value != ""
                        if isinstance(param_value, (list, set)):
                            is_valid = is_valid and len(param_value) > 0
                        if is_valid:
                            all_params.add(param_name)
                if request_method == "GET":
                    request_method = req.get("method", "GET")

        return all_params, all_requests_params, request_method

    def _extract_params_unified(self, requests: list, api_url: str) -> tuple:
        """
        统一提取参数的方法
        
        Args:
            requests: 请求列表
            api_url: API URL（可能是模板）
            
        Returns:
            tuple: (所有参数集合, 所有请求参数字典列表, 请求方法)
        """
        all_params = set()
        all_requests_params = []
        request_method = "GET"
        
        for req in requests:
            # 使用URLMatcher规范化URL进行比较
            normalized_req_url = URLMatcher.normalize_url(req["url"])
            normalized_api_url = URLMatcher.normalize_url(api_url)
            
            if normalized_req_url == normalized_api_url:
                api_params = self.extract_params_from_har_request(req)
                if isinstance(api_params, dict):
                    all_requests_params.append(api_params)
                    
                    # 收集有效参数
                    for param_name, param_value in api_params.items():
                        is_valid = param_value is not None and param_value != ""
                        if isinstance(param_value, (list, set)):
                            is_valid = is_valid and len(param_value) > 0
                        if is_valid:
                            all_params.add(param_name)
                
                if request_method == "GET":
                    request_method = req.get("method", "GET")
        
        return all_params, all_requests_params, request_method

    def generate_scenario_testcase(self, har_file_path: str, target_url: str, task_id: str) -> str | None:
        """生成复杂场景流程测试用例"""
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None
        
        api_files = self.match_api_files_for_har(har_file_path)
        
        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return None
        
        logger.info(f"找到 {len(api_files)} 个对应的API文件")
        
        # 处理task_id
        if task_id and task_id.startswith("test_"):
            task_id = task_id[5:]
        
        # 获取输出目录
        output_dir = get_output_dir(self.output_dir, task_id)
        
        # 使用统一方法查找目标接口文件
        target_api_file = self._find_target_api_file_unified(api_files, target_url)
        
        if not target_api_file:
            logger.info(f"未找到指定URL对应的API文件: {target_url}")
            return None
        
        # 生成测试用例
        clean_function_name = self._get_clean_function_name(target_api_file)
        test_filename = f"test_{clean_function_name}.py"
        test_filepath = os.path.join(output_dir, test_filename)
        
        test_content = self.generate_test_case_content(
            har_file_path, api_files, task_id, target_api_file, target_url
        )
        
        if not test_content:
            logger.info("无法生成测试用例内容")
            return None
        
        write_test_file(test_filepath, test_content)
        logger.info(f"生成测试用例文件: {test_filepath}")
        return test_filepath
    
    def _find_target_api_file_unified(self, api_files: list[str], target_url: str) -> str | None:
        """
        统一的目标API文件查找方法
        
        Args:
            api_files: API文件列表
            target_url: 目标URL（可能是模板）
            
        Returns:
            Optional[str]: 匹配的API文件路径
        """
        for api_file in api_files:
            result = get_url_from_api_file(api_file)
            if not result:
                continue
                
            _, file_url = result
            
            # 1. 直接匹配
            if file_url == target_url:
                return api_file
            
            # 2. 模板匹配（实际URL匹配模板）
            matched, _ = URLMatcher.match_url_pattern(target_url, file_url)
            if matched:
                return api_file
            
            # 3. 实际URL匹配模板URL
            matched, _ = URLMatcher.match_url_pattern(file_url, target_url)
            if matched:
                return api_file
            
            # 4. 规范化后比较
            normalized_file_url = URLMatcher.normalize_url(file_url)
            normalized_target_url = URLMatcher.normalize_url(target_url)
            if normalized_file_url == normalized_target_url:
                return api_file
        
        return None

    def _generate_test_case_imports(self, service_package: str, function_name: str, task_id: str) -> list[str]:
        """
        生成测试用例的导入部分
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

    def _generate_test_case_description(self, api_description: str, api_url: str, service_package: str, all_params: set, param_remarks: dict) -> list[str]:
        """
        生成测试用例的描述部分（装饰器和文档）
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
        """
        生成测试类的setup方法
        """
        return [
            "class TestClass:",
            "",
            "    # 初始化测试数据字典，用于在步骤间传递数据",
            "    def setup_class(self):",
            "        self.headers = {",
            '            "channel": "pc",',
            '            "client": "op",',
            '            "content-type": "application/json;charset=UTF-8",',
            '            "authorization": f"bearer {os.environ[\'access_token\']}",',
            "        }",
            "",
        ]

    def _generate_parametrized_test_methods(self, param_items: list, api_description: str, clean_function_name: str, request_method: str, param_remarks: dict) -> list[str]:
        """
        生成参数化测试方法
        """
        content = []
        param_count = 0

        for item in param_items:
            param_name = next((k for k in item if k != "other_params"), None)
            if not param_name:
                continue

            param_values = item[param_name]
            other_params = item["other_params"]
            is_combination = "," in param_name
            param_var_name = "params" if request_method == "GET" else "data"

            # 生成参数化装饰器
            content.extend(self._generate_parametrize_decorator(param_name, param_values, is_combination))

            # 生成方法定义
            content.extend(self._generate_test_method_definition(api_description, param_name, param_remarks, clean_function_name, param_count, is_combination))

            # 生成方法体
            content.extend(self._generate_test_method_body(param_var_name, param_name, other_params, is_combination))

            # 生成断言
            content.extend(self._generate_test_method_assertions(clean_function_name, param_var_name))

            param_count += 1

        return content

    def _generate_parametrize_decorator(self, param_name: str, param_values: list, is_combination: bool) -> list[str]:
        """
        生成@pytest.mark.parametrize装饰器
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

    def _generate_test_method_definition(self, api_description: str, param_name: str, param_remarks: dict, clean_function_name: str, param_count: int, is_combination: bool) -> list[str]:
        """
        生成测试方法定义（装饰器+方法签名）
        """
        if is_combination:
            param_names = param_name.split(",")
            param_descriptions = set()
            for p in param_names:
                desc = param_remarks.get(p, p)
                if "-" in desc:
                    desc = desc.split("-")[0]
                param_descriptions.add(desc)
            param_description_str = "-".join(param_descriptions)
            return [
                f'    @allure.title("{api_description}-成功路径: {param_description_str} 查询")',
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

    def _generate_test_method_body(self, param_var_name: str, param_name: str, other_params: dict, is_combination: bool) -> list[str]:
        """
        生成测试方法体
        """
        content = [
            "",
            "        # 用例级别",
            "        allure.dynamic.severity(p)",
            "",
            f"        {param_var_name} =   {{",
        ]
        self._generate_data_dict(content, param_name, other_params, is_combination, param_var_name)
        return content

    def _generate_test_method_assertions(self, function_name: str, param_var_name: str) -> list[str]:
        """
        生成测试方法断言部分
        """
        content = [
            f"        with {function_name}(data={param_var_name}, headers=self.headers) as r:",
            "            assert r.status_code == 200",
            "            assert r.json()['code'] == 200",
            "",
        ]
        return content

