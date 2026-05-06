import os
import re
from typing import Any

from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .utils import deduplicate_values, extract_url_from_file, format_parameter_value, format_python_file


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
            api_dir = APIConfig.DEFAULT_SERVICE_PACKAGE()
        if output_dir is None:
            output_dir = APIConfig.TESTCASE_DIR()
        self.api_dir = api_dir
        self.output_dir = output_dir
        self.filter_duplicate_url = filter_duplicate_url
        self.har_parser = HARParser(base_urls=base_urls, kill_urls=kill_urls)

    def _get_output_dir(self, task_id: str = None) -> str:
        """
        获取输出目录路径
        :param task_id: 任务ID，如果提供则创建子目录 {output_dir}/{task_id}
        :return: 输出目录路径
        """
        if task_id:
            output_dir = os.path.join(self.output_dir, task_id)
        else:
            output_dir = self.output_dir
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def match_api_files_for_har(self, har_file_path: str) -> list[str]:
        """
        根据HAR文件查找对应的API文件
        """
        requests = self.har_parser.extract_requests_from_har(har_file_path)

        api_files = []

        for root, dirs, files in os.walk(self.api_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    filepath = os.path.join(root, file)

                    result = extract_url_from_file(filepath)
                    if result:
                        _, file_url = result
                        for request in requests:
                            request_url = request["url"]
                            # 支持两种匹配方式：
                            # 1. 直接相等
                            # 2. request_url 以 file_url 结尾（处理完整URL的情况）
                            if request_url == file_url or request_url.endswith(file_url):
                                api_files.append(filepath)
                                break

        return api_files

    def get_function_name_from_api_file(self, filepath: str) -> str | None:
        """
        从API文件路径中提取函数名

        由于API文件名就是函数名（如 _user_mgmt_order_page.py），
        直接从文件名提取，无需读取文件内容
        """
        try:
            basename = os.path.basename(filepath)
            function_name = os.path.splitext(basename)[0]
            return function_name
        except Exception as e:
            logger.error(f"从文件路径提取函数名失败 {filepath}: {str(e)}")
            return None

    def get_param_remarks_from_api_file(self, api_file: str) -> dict[str, str]:
        """
        从API文件中提取参数备注
        """
        param_remarks = {}
        try:
            with open(api_file, encoding="utf-8") as f:
                content = f.read()

            # 查找data字典定义
            data_match = re.search(r"data\s*=\s*\{[^}]*\}", content, re.DOTALL)
            if data_match:
                data_block = data_match.group(0)
                # 提取每个参数和备注
                param_matches = re.findall(r'"(\w+)"\s*:\s*([^#]+)\s*#\s*(.+?)\n', data_block)
                for param_name, _, remark in param_matches:
                    # 提取备注中的参数名称
                    # 例如："兑换流水号" 或 "顾客手机号"
                    param_remarks[param_name] = remark.strip()
        except Exception as e:
            logger.error(f"读取API文件 {api_file} 失败: {str(e)}")

        return param_remarks

    def extract_params_from_har_request(self, request_info: dict[str, Any]) -> dict[str, Any] | None:
        """
        从HAR请求信息中提取参数字典
        """
        method = request_info["method"].upper()
        post_data = request_info.get("post_data")
        query_params = request_info.get("query_params", {})

        if method == "POST" and post_data:
            if isinstance(post_data, dict):
                return post_data or None
            else:
                return None
        elif method == "POST" and query_params:
            return query_params or None
        elif method == "GET" and query_params:
            return query_params

        return None

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
            function_name = self.get_function_name_from_api_file(api_file)
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
        epic_name = "建议输入被测接口所属的微服务，如 mall_store_application"
        feature_name = "建议输入被测业务功能模块，如 订单管理"
        story_name = "建议输入被测接口，如 /appStore/order/orderSign/signCommit"
        title_name = "建议输入测试用例名称，如 提交订单"

        if target_api_file:
            # 提取服务名称
            module_path = target_api_file.replace(".py", "").replace("\\", ".").replace("/", ".")
            if len(module_path.split(".")) > 1:
                epic_name = module_path.split(".")[1]

            # 提取接口描述和URL
            api_description, api_url = extract_url_from_file(target_api_file)
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
                f"@allure.epic('{epic_name}')",
                f"@allure.feature('{feature_name}')",
                f"@allure.story('{story_name}')",
                f"@allure.title('{title_name}')",
            ]
        )

        # 生成测试函数名称
        if target_api_file:
            function_name = self.get_function_name_from_api_file(target_api_file)
            if function_name:
                clean_function_name = function_name.lstrip("_").strip()
                test_function_name = f"def test_{clean_function_name}():"
            else:
                test_function_name = "def test_har_api_flow():"
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
                _, file_url = extract_url_from_file(api_file)
                if file_url == url:
                    api_function = self.get_function_name_from_api_file(api_file)
                    break

            if api_function:
                api_description, _ = extract_url_from_file(api_file)

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

        if output_subdir:
            output_dir = os.path.join(self.output_dir, output_subdir)
            logger.info(output_dir)
        else:
            output_dir = self.output_dir

        os.makedirs(output_dir, exist_ok=True)

        test_filename = f"test_{os.path.splitext(os.path.basename(har_file_path))[0]}.py"
        test_filepath = os.path.join(output_dir, test_filename)

        test_content = self.generate_test_case_content(har_file_path, api_files)

        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write(test_content)

        # 使用ruff格式化生成的文件
        format_python_file(test_filepath)

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
        output_dir = self._get_output_dir(task_id)

        generated_files = []

        for api_file in api_files:
            try:
                function_name = self.get_function_name_from_api_file(api_file)
                if function_name:
                    clean_function_name = function_name.lstrip("_").strip()
                    test_filename = f"test_{clean_function_name}.py"
                else:
                    api_basename = os.path.splitext(os.path.basename(api_file))[0]
                    clean_basename = api_basename.lstrip("_").strip()
                    test_filename = f"test_{clean_basename}.py"

                test_filepath = os.path.join(output_dir, test_filename)

                # 生成参数化测试用例内容
                test_content = self.generate_parametrized_test_content(har_file_path, api_file, task_id)

                if not test_content:
                    logger.info(f"跳过文件（无法生成内容）: {api_file}")
                    continue

                with open(test_filepath, "w", encoding="utf-8") as f:
                    f.write(test_content)

                # 使用ruff格式化生成的文件
                format_python_file(test_filepath)

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
        function_name = self.get_function_name_from_api_file(api_file)
        if not function_name:
            return None

        clean_function_name = function_name.lstrip("_").strip()

        # 提取API信息
        api_description, api_url = extract_url_from_file(api_file)
        module_path = api_file.replace(".py", "").replace("\\", ".").replace("/", ".")

        # 解析HAR文件获取请求信息
        requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)
        if not requests:
            return None

        # 从HAR文件中提取所有参数和请求方法
        all_params = set()
        all_requests_params = []
        request_method = "GET"  # 默认GET方法
        for req in requests:
            if req["url"] == api_url:
                # 提取API参数
                api_params = self.extract_params_from_har_request(req)
                if isinstance(api_params, dict):
                    all_requests_params.append(api_params)
                    # 只添加非空参数到 all_params（空列表视为无效参数）
                    for param_name, param_value in api_params.items():
                        is_valid = param_value is not None and param_value != ""
                        if isinstance(param_value, (list, set)):
                            is_valid = is_valid and len(param_value) > 0
                        if is_valid:
                            all_params.add(param_name)
                # 记录请求方法（只记录第一个匹配的）
                if request_method == "GET":
                    request_method = req.get("method", "GET")
                # 继续处理所有匹配的请求，而不是只处理第一个

        if not all_requests_params:
            return None

        # 从API文件中提取参数备注
        param_remarks = self.get_param_remarks_from_api_file(api_file)
        if not param_remarks:
            param_remarks = {}

        # 提取服务包名称
        service_package = module_path.split(".")[1] if len(module_path.split(".")) > 1 else "default"

        # 生成测试用例内容
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
        content.extend(
            [
                f"@allure.epic('{service_package}')",
                "@allure.feature('建议输入被测业务功能模块，如订单管理')",
                f"@allure.story('{api_url}')",
                f'@allure.description("""接口说明：\n- 接口名称：{api_description}',
                f"- 接口地址：{api_url}",
                "",
                "主要参数说明：",
            ]
        )

        # 添加参数说明
        logger.debug(f"参数备注: {param_remarks}")
        for param_name in all_params:
            # 使用参数备注，如果没有备注则显示"可选"
            remark = param_remarks.get(param_name, "# TODO 请填写参数备注")
            # 检查是否包含 TODO
            if "TODO" in remark:
                remark = "# TODO 请填写参数备注"
            content.append(f"- {param_name}：{remark}")

        content.extend(
            [
                '""")',
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
        )

        # 生成参数化测试方法
        param_count = 0

        # 使用 normalize_params_for_parametrization 方法处理参数
        param_items = self.normalize_params_for_parametrization(all_requests_params)

        # 生成测试用例
        for item in param_items:
            # 提取参数名和值
            param_name = next((k for k in item if k != "other_params"), None)
            if not param_name:
                continue

            param_values = item[param_name]
            other_params = item["other_params"]

            # 生成参数化测试方法
            is_combination = "," in param_name

            # 准备参数化值
            parametrize_values = self._generate_parametrize_values(param_values, is_combination)

            # 生成参数化装饰器
            if is_combination:
                param_names = param_name.split(",")
                content.append(f'    @pytest.mark.parametrize("{", ".join(param_names)}, p", [')
            else:
                content.append(f'    @pytest.mark.parametrize("{param_name}, p", [')

            for i, value in enumerate(parametrize_values):
                if i == len(parametrize_values) - 1:
                    content.append(f"        {value}")
                else:
                    content.append(f"        {value},")

            # 获取参数的备注信息
            if is_combination:
                param_names = param_name.split(",")
                param_descriptions = set()
                for p in param_names:
                    desc = param_remarks.get(p, p)
                    # 只取空格前的部分作为参数描述
                    if "-" in desc:
                        desc = desc.split("-")[0]
                    param_descriptions.add(desc)
                param_description_str = "-".join(param_descriptions)
                content.extend(
                    [
                        "    ])",
                        f'    @allure.title("{api_description}-成功路径: {param_description_str} 查询")',
                        f"    def test_{param_count}_{clean_function_name}(self, {', '.join(param_names)}, p):",
                    ]
                )
            else:
                param_description = param_remarks.get(param_name, param_name)
                # 只取空格前的部分作为参数描述
                if " " in param_description:
                    param_description = param_description.split(" ")[0]
                content.extend(
                    [
                        "    ])",
                        f'    @allure.title("{api_description}-成功路径: {param_description} 查询")',
                        f"    def test_{param_count}_{clean_function_name}(self, {param_name}, p):",
                    ]
                )

            # 根据请求方法类型决定使用 data 还是 params
            param_var_name = "params" if request_method == "GET" else "data"

            content.extend(
                [
                    "",
                    "        # 用例级别",
                    "        allure.dynamic.severity(p)",
                    "",
                    f"        {param_var_name} =   {{",
                ]
            )

            # 生成数据字典
            self._generate_data_dict(content, param_name, other_params, is_combination, param_var_name)

            # 生成断言
            self._generate_assertions(content, function_name, param_name, is_combination, param_var_name)

            param_count += 1

        return "\n".join(content)

    def generate_scenario_testcase(self, har_file_path: str, target_url: str, task_id: str) -> str | None:
        """
        生成复杂场景流程测试用例
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None

        api_files = self.match_api_files_for_har(har_file_path)

        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return None

        logger.info(f"找到 {len(api_files)} 个对应的API文件")

        # 处理task_id，去掉test_前缀
        if task_id and task_id.startswith("test_"):
            task_id = task_id[5:]

        # 获取输出目录
        output_dir = self._get_output_dir(task_id)

        # 查找目标接口文件，用于生成文件名
        target_api_file = None
        if target_url:
            for api_file in api_files:
                _, file_url = extract_url_from_file(api_file)
                if file_url == target_url:
                    target_api_file = api_file
                    break

            if not target_api_file:
                logger.info(f"未找到指定URL对应的API文件: {target_url}")
                return None
        else:
            # 没有指定目标接口，退出
            return None

        # 生成测试用例文件
        function_name = self.get_function_name_from_api_file(target_api_file)
        if function_name:
            clean_function_name = function_name.lstrip("_").strip()
            test_filename = f"test_{clean_function_name}.py"
        else:
            api_basename = os.path.splitext(os.path.basename(target_api_file))[0]
            clean_basename = api_basename.lstrip("_").strip()
            test_filename = f"test_{clean_basename}.py"

        test_filepath = os.path.join(output_dir, test_filename)

        # 生成测试用例内容，传递所有API文件和接口信息
        test_content = self.generate_test_case_content(har_file_path, api_files, task_id, target_api_file, target_url)

        if not test_content:
            logger.info("无法生成测试用例内容")
            return None

        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write(test_content)

        # 使用ruff格式化文件
        format_python_file(test_filepath)

        logger.info(f"生成测试用例文件: {test_filepath}")
        return test_filepath
