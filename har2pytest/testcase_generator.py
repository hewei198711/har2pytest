# coding:utf-8
import os
import re
from typing import Dict, Any, List, Optional

from .config import APIConfig
from .har_parser import HARParser
from .utils import extract_url_from_file, format_single_parameter_value
from .logger import logger



class TestCaseGenerator:
    """pytest用例生成器类"""

    def __init__(self, api_dir: str = None, output_dir: str = None, filter_duplicate_url=False):
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
        self.har_parser = HARParser()

    def extract_function_name_from_file(self, filepath: str) -> Optional[str]:
        """
        从API文件中提取函数名
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            func_match = re.search(r'def\s+(\w+)\s*\(', content)
            if func_match:
                return func_match.group(1)
        except Exception as e:
            logger.error(f"读取文件 {filepath} 失败: {str(e)}")

        return None

    def extract_api_params_dict_from_har(self, request_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        从HAR请求信息中提取参数字典
        """
        method = request_info['method'].upper()
        post_data = request_info.get('post_data')
        query_params = request_info.get('query_params', {})

        if method == 'POST' and post_data:
            if isinstance(post_data, dict):
                return post_data or None
            else:
                return None
        elif method == 'POST' and query_params:
            return query_params or None
        elif method == 'GET' and query_params:
            return query_params

        return None

    def format_params_for_test_case(self, params_dict: Dict[str, Any]) -> str:
        """
        格式化参数为测试用例中的参数字符串
        """
        if not params_dict:
            return "{}"

        lines = [" {"]
        for i, (key, value) in enumerate(params_dict.items()):
            formatted_value = format_single_parameter_value(value)

            if '\n' in formatted_value:
                value_lines = formatted_value.split('\n')
                lines.append(f'            "{key}": {value_lines[0]}')
                for line in value_lines[1:]:
                    if line.strip():
                        lines.append(f'            {line}')
                    else:
                        lines.append('')
                if i < len(params_dict) - 1:
                    lines[-1] = lines[-1].rstrip() + ','
            else:
                lines.append(f'            "{key}": {formatted_value}' +
                            (',' if i < len(params_dict) - 1 else ''))

        lines.append("        }")

        return '\n'.join(lines)

    def process_params_to_map(self, requests_params: List[Dict[str, Any]]):
        """
        将 requests_params 中的数据处理成 标准样式的数据结构

        Args:
            requests_params: 包含多个参数字典的列表

        Returns:
            list: 处理后的结果，与 expected 结构一致
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
                # 只处理非分页参数
                if param_name not in APIConfig.PAGINATION_PARAMS():
                    # 非 None 且非空字符串的值视为有效参数
                    if param_value is not None and param_value != "":
                        valid_params[param_name] = param_value
                    else:
                        other_params[param_name] = param_value
                else:
                    # 分页参数总是包含在 other_params 中
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
                    param_value_map[combination_key] = {
                        "values": [],
                        "other_params": other_params
                    }
                param_value_map[combination_key]["values"].append(combination_value)

            elif len(valid_params) == 1:
                # 只有一个有效参数，作为单个参数处理
                param_name, param_value = list(valid_params.items())[0]

                # 添加到 param_value_map
                if param_name not in param_value_map:
                    param_value_map[param_name] = {
                        "values": [],
                        "other_params": other_params
                    }
                param_value_map[param_name]["values"].append(param_value)

        # 构建最终结果
        merged_result = []
        for param_name, data in param_value_map.items():
            # 判断是组合参数还是单个参数
            is_combination = "," in param_name

            if is_combination:
                # 对于组合参数，data["values"] 是一个包含多个列表的列表
                # 例如：[["2026-01-01", "2026-01-31"], ["2026-02-01", "2026-02-28"]]
                # 需要去重并保留所有不同的组合
                seen = set()
                unique_values = []
                for value_list in data["values"]:
                    # 将列表转换为元组以便去重
                    value_tuple = tuple(value_list)
                    if value_tuple not in seen:
                        seen.add(value_tuple)
                        # 将值列表转换为元组，保持与 expected 一致
                        unique_values.append(tuple(value_list))

                # 组合参数的值始终是元组列表
                unique_values = unique_values
            else:
                # 对于单个参数，data["values"] 是一个包含多个值的列表
                # 例如：[1, 2, 3, 2, 1]
                # 需要去重并保留所有不同的值
                unique_values = list(set(data["values"]))

            merged_item = {
                param_name: unique_values,
                "other_params": data["other_params"]
            }
            merged_result.append(merged_item)

        return merged_result

    def generate_test_case_content(self, har_file_path: str, api_files: List[str], task_id: str = None, target_api_file: str = None, target_url: str = None) -> str:
        """
        生成pytest用例文件内容
        """
        har_filename = os.path.basename(har_file_path)
        case_name = os.path.splitext(har_filename)[0]

        requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)

        content = [
            "# coding:utf-8",
            "",
            f"# 自动生成的pytest用例文件",
            f"# 基于HAR文件: {har_filename}",
            f"# 生成时间: {__import__('datetime').datetime.now()}",
            "",
            "import os",
            "import pytest",
            "import allure",
            "from setting import P1, P2, P3",
            ""
        ]

        imports = []
        for api_file in api_files:
            module_path = api_file.replace('.py', '').replace('\\', '.').replace('/', '.')
            function_name = self.extract_function_name_from_file(api_file)
            if function_name:
                imports.append(f"from {module_path} import {function_name}")

        if imports:
            content.extend(imports)
            content.append("")

        # 提取接口信息
        feature_name = "请填写被测试接口所属的微服务名称，如 mall_store_application"
        story_name = "请填写被测试接口，如 /appStore/order/orderSign/signCommit"
        title_name = "请填写测试用例名称，如 签约购提交订单"

        if target_api_file:
            # 提取服务名称
            module_path = target_api_file.replace('.py', '').replace('\\', '.').replace('/', '.')
            if len(module_path.split('.')) > 1:
                feature_name = module_path.split('.')[1]
            
            # 提取接口描述和URL
            api_description, api_url = extract_url_from_file(target_api_file)
            if api_description:
                title_name = api_description
            if api_url:
                story_name = api_url

        # 添加测试标记和接口说明
        if task_id:
            content.append(f"@pytest.mark.test_{task_id}")
        
        content.extend([
            "@allure.severity(P1)",
            f"@allure.feature('{feature_name}')",
            f"@allure.story('{story_name}')",
            f"@allure.title('{title_name}')",
        ])

        # 生成测试函数名称
        if target_api_file:
            function_name = self.extract_function_name_from_file(target_api_file)
            if function_name:
                clean_function_name = function_name.lstrip('_').strip()
                test_function_name = f"def test_{clean_function_name}():"
            else:
                test_function_name = "def test_har_api_flow():"
        else:
            test_function_name = "def test_har_api_flow():"
        content.append(test_function_name)

        content.extend([
            '    """',
            f"    基于HAR文件 {har_filename} 的API流程测试",
            "    每个API请求作为一个测试步骤",
            '    """',
            "",
            "    # 初始化测试数据字典，用于在步骤间传递数据",
            "    test_data = {",
            '        "access_token": os.environ["token_icbc_mall"],',
            "    }",
            ""
        ])

        step_functions = []
        name_counters = {}
        for i, request_info in enumerate(requests):
            url = request_info['url']
            method = request_info['method']

            api_function = None
            for api_file in api_files:
                _, file_url = extract_url_from_file(api_file)
                if file_url == url:
                    api_function = self.extract_function_name_from_file(api_file)
                    break

            if api_function:
                api_description, _ = extract_url_from_file(api_file)

                clean_function_name = api_function.lstrip('_')

                if clean_function_name not in name_counters:
                    name_counters[clean_function_name] = 0

                count = name_counters[clean_function_name]

                if count == 0:
                    step_name = f"step_{clean_function_name}"
                else:
                    step_name = f"step_{count}_{clean_function_name}"

                name_counters[clean_function_name] += 1

                step_functions.append(step_name)

                function_parts = clean_function_name.split('_')
                if len(function_parts) >= 2:
                    data_key = '_'.join(function_parts[-2:])
                else:
                    data_key = function_parts[0] if function_parts else f"response_{i+1}"

                api_params = self.extract_api_params_dict_from_har(request_info)
                if api_params:
                    api_params = self.format_params_for_test_case(api_params)

                content.extend([
                    f"    @allure.step(\"{api_description}\")",
                    f"    def {step_name}():",
                    ""
                ])

                if api_params:
                    content_type = request_info.get('content_type', '')
                    is_file_upload = method == 'POST' and content_type.startswith('multipart/form-data')

                    if is_file_upload:
                        # 处理文件上传请求
                        content.extend([
                            f"        files = {{",
                        ])
                        
                        # 添加原始参数
                        if api_params:
                            params_lines = api_params.strip().split('\n')
                            # 跳过第一行（" {"）和最后一行（"        }"）
                            for line in params_lines[1:-1]:
                                if line.strip():
                                    content.append(f"            {line}")
                        
                        # 添加文件参数
                        content.extend([
                            f'            "file": "data/示例文件.png"',
                            f"        }}"
                        ])
                        content.extend([
                            f"        with {api_function}(access_token=test_data['access_token'], files=files) as r:"
                        ])
                    elif method == 'POST':
                        content.extend([
                            f"        data = {api_params}",
                            f"        with {api_function}(access_token=test_data['access_token'], data=data) as r:"
                        ])
                    else:
                        content.extend([
                            f"        params = {api_params}",
                            f"        with {api_function}(access_token=test_data['access_token'], params=params) as r:"
                        ])
                else:
                    content_type = request_info.get('content_type', '')
                    is_file_upload = method == 'POST' and content_type.startswith('multipart/form-data')

                    if is_file_upload:
                        content.extend([
                            f"        files = {{",
                            f'            "storageType": "PublicCloud",',
                            f'            "clientKey": "mall-center-product",',
                            f'            "file": "data/示例文件.png"',
                            f"        }}",
                            f"        with {api_function}(access_token=test_data['access_token'], files=files) as r:"
                        ])
                    else:
                        content.extend([
                            f"        with {api_function}(access_token=test_data['access_token']) as r:"
                        ])

                content.extend([
                    f"            assert r.status_code == 200",
                    f"            assert r.json()['code'] == 200",
                    f"            test_data['{data_key}'] = r.json()",
                    ""
                ])

        if step_functions:
            content.append("    # 执行所有测试步骤")
            for step_func in step_functions:
                content.append(f"    {step_func}()")
            content.append("")

        return '\n'.join(content)

    def extract_service_package_from_url(self, url: str) -> str:
        """
        从URL中提取服务包名
        """
        return APIConfig.determine_service_package(url)

    def find_api_files_for_har(self, har_file_path: str) -> List[str]:
        """
        根据HAR文件查找对应的API文件
        """
        requests = self.har_parser.extract_requests_from_har(har_file_path)

        api_files = []

        for root, dirs, files in os.walk(self.api_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    filepath = os.path.join(root, file)

                    result = extract_url_from_file(filepath)
                    if result:
                        _, file_url = result
                        for request in requests:
                            if request['url'] == file_url:
                                api_files.append(filepath)
                                break

        return api_files

    def generate_test_case_from_har(self, har_file_path: str, output_subdir: str = None) -> Optional[str]:
        """
        从HAR文件生成pytest用例文件
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None

        api_files = self.find_api_files_for_har(har_file_path)

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

        with open(test_filepath, 'w', encoding='utf-8') as f:
            f.write(test_content)

        logger.info(f"生成测试用例文件: {test_filepath}")
        return test_filepath

    def generate_list_query_testcases(self, har_file_path: str, task_id: str) -> List[str]:
        """
        生成查询类参数化测试用例
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return []

        api_files = self.find_api_files_for_har(har_file_path)

        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return []

        logger.info(f"找到 {len(api_files)} 个对应的API文件")

        # 处理task_id，去掉test_前缀
        if task_id and task_id.startswith('test_'):
            task_id = task_id[5:]

        # 创建输出目录
        output_dir = os.path.join(self.output_dir, "版本接口测试", task_id)
        os.makedirs(output_dir, exist_ok=True)

        generated_files = []

        for api_file in api_files:
            try:
                function_name = self.extract_function_name_from_file(api_file)
                if function_name:
                    clean_function_name = function_name.lstrip('_').strip()
                    test_filename = f"test_{clean_function_name}.py"
                else:
                    api_basename = os.path.splitext(os.path.basename(api_file))[0]
                    clean_basename = api_basename.lstrip('_').strip()
                    test_filename = f"test_{clean_basename}.py"

                test_filepath = os.path.join(output_dir, test_filename)

                # 生成参数化测试用例内容
                test_content = self.generate_parametrized_test_content(har_file_path, api_file, task_id)

                if not test_content:
                    logger.info(f"跳过文件（无法生成内容）: {api_file}")
                    continue

                with open(test_filepath, 'w', encoding='utf-8') as f:
                    f.write(test_content)

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
                formatted_values.append("P2")
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
                parametrize_values.append(f"({value_str}, P2)")
        return parametrize_values

    def _generate_data_dict(self, content, param_name, other_params, is_combination, param_var_name):
        """
        生成数据字典
        """
        if is_combination:
            param_names = param_name.split(",")
            for key in param_names:
                content.append(f"            \"{key}\": {key},")
        else:
            content.append(f"            \"{param_name}\": {param_name},")
        
        for key, value in other_params.items():
            if isinstance(value, str):
                content.append(f"            \"{key}\": \"{value}\",")
            else:
                content.append(f"            \"{key}\": {value},")

    def _generate_assertions(self, content, function_name, param_name, is_combination, param_var_name):
        """
        生成断言
        """
        content.extend([
            "        }",
            f"        with {function_name}(access_token=self.access_token, {param_var_name}={param_var_name}) as r:",
            "            assert r.status_code == 200",
            "            assert r.json()['code'] == 200",
            "            data_list = r.json()[\"data\"][\"list\"]",
            "            assert len(data_list) > 0, \"返回数据列表为空\"",
        ])
        
        if not is_combination:
            content.extend([
                f"            if any(i.get(\"{param_name}\") is not None for i in data_list):",
                f"                assert any(i.get(\"{param_name}\") == {param_name} for i in data_list)",
            ])
        
        content.append("")

    def generate_parametrized_test_content(self, har_file_path: str, api_file: str, task_id: str) -> Optional[str]:
        """
        生成参数化测试用例内容
        """
        har_filename = os.path.basename(har_file_path)
        function_name = self.extract_function_name_from_file(api_file)
        if not function_name:
            return None
        
        clean_function_name = function_name.lstrip('_').strip()

        # 提取API信息
        api_description, api_url = extract_url_from_file(api_file)
        module_path = api_file.replace('.py', '').replace('\\', '.').replace('/', '.')

        # 解析HAR文件获取请求信息
        requests = self.har_parser.extract_requests_from_har(har_file_path, self.filter_duplicate_url)
        if not requests:
            return None

        # 从HAR文件中提取所有参数和请求方法
        all_params = set()
        all_requests_params = []
        request_method = 'GET'  # 默认GET方法
        for req in requests:
            if req['url'] == api_url:
                # 提取API参数
                api_params = self.extract_api_params_dict_from_har(req)
                if isinstance(api_params, dict):
                    all_requests_params.append(api_params)
                    all_params.update(api_params.keys())
                # 记录请求方法
                request_method = req.get('method', 'GET')
                break  # 只使用第一个匹配的请求

        if not all_requests_params:
            return None

        # 从API文件中提取参数备注
        param_remarks = self.extract_param_remarks_from_api_file(api_file)
        if not param_remarks:
            param_remarks = {}

        # 提取服务包名称
        service_package = module_path.split('.')[1] if len(module_path.split('.')) > 1 else 'default'

        # 生成测试用例内容
        content = [
            "# coding:utf-8",
            "",
            "# 自动生成的pytest用例文件",
            f"# 基于HAR文件: {har_filename}",
            f"# 生成时间: {__import__('datetime').datetime.now()}",
            "",
            "import os",
            "import pytest",
            "import allure",
            "from setting import P1, P2, P3",
            "",
            f"from {module_path} import {function_name}",
            "",
            f"@allure.feature('{service_package}')",
            f"@allure.story('{api_url}')",
            "@allure.description(\"\"\"接口说明：\n"
            f"- 接口名称：{api_description}",
            f"- 接口地址：{api_url}",
            "",
            "主要参数说明：",
        ]
        
        # 添加参数说明
        logger.debug(f"参数备注: {param_remarks}")
        for param_name in all_params:
            # 使用参数备注，如果没有备注则显示"可选"
            remark = param_remarks.get(param_name, "# TODO 请填写参数备注")
            # 检查是否包含 TODO
            if "TODO" in remark:
                remark = "# TODO 请填写参数备注"
            content.append(f"- {param_name}：{remark}")
        
        content.append("")
        content.append("业务场景：")
        content.append("1. 成功路径：使用各种条件查询订单列表")
        content.append("2. 验证逻辑：返回列表数据，验证code=200")
        content.append("3. 测试数据清理：无副作用，仅查询数据")
        content.append('""")')
        content.append("class TestClass:")
        content.append('    """')
        content.append(f"    基于HAR文件 {har_filename} 的API流程测试")
        content.append("    每个API请求作为一个测试步骤")
        content.append('    """')
        content.append("")
        content.append("    # 初始化测试数据字典，用于在步骤间传递数据")
        content.append("    def setup_class(self):")
        content.append("        self.access_token = os.environ['access_token']")
        content.append("")

        # 生成参数化测试方法
        param_count = 0

        # 使用 process_params_to_map 方法处理参数
        param_items = self.process_params_to_map(all_requests_params)

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
                content.extend([
                    f"    @pytest.mark.test_{task_id}",
                    f"    @pytest.mark.parametrize(\"{', '.join(param_names)}, p\", [",
                ])
            else:
                content.extend([
                    f"    @pytest.mark.test_{task_id}",
                    f"    @pytest.mark.parametrize(\"{param_name}, p\", [",
                ])
            
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
                content.extend([
                    f"    ])",
                    f"    @allure.title(\"{api_description}-成功路径: {param_description_str} 查询\")",
                    f"    def test_{param_count}_{clean_function_name}(self, {', '.join(param_names)}, p):",
                ])
            else:
                param_description = param_remarks.get(param_name, param_name)
                # 只取空格前的部分作为参数描述
                if ' ' in param_description:
                    param_description = param_description.split(' ')[0]
                content.extend([
                    f"    ])",
                    f"    @allure.title(\"{api_description}-成功路径: {param_description} 查询\")",
                    f"    def test_{param_count}_{clean_function_name}(self, {param_name}, p):",
                ])
            
            # 根据请求方法类型决定使用 data 还是 params
            param_var_name = 'params' if request_method == 'GET' else 'data'
            
            content.extend([
                "",
                "        # 用例级别",
                "        allure.dynamic.severity(p)",
                "",
                f"        {param_var_name} =   {{",
            ])

            # 生成数据字典
            self._generate_data_dict(content, param_name, other_params, is_combination, param_var_name)

            # 生成断言
            self._generate_assertions(content, function_name, param_name, is_combination, param_var_name)

            param_count += 1

        return '\n'.join(content)

    def extract_param_remarks_from_api_file(self, api_file: str) -> Dict[str, str]:
        """
        从API文件中提取参数备注
        """
        param_remarks = {}
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找data字典定义
            data_match = re.search(r'data\s*=\s*\{[^}]*\}', content, re.DOTALL)
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

    def generate_complex_scenario_testcase(self, har_file_path: str, target_url: str, task_id: str) -> Optional[str]:
        """
        生成复杂场景流程测试用例
        """
        if not os.path.exists(har_file_path):
            logger.info(f"HAR文件不存在: {har_file_path}")
            return None

        api_files = self.find_api_files_for_har(har_file_path)

        if not api_files:
            logger.info(f"未找到HAR文件 {har_file_path} 对应的API文件")
            return None

        logger.info(f"找到 {len(api_files)} 个对应的API文件")

        # 处理task_id，去掉test_前缀
        if task_id and task_id.startswith('test_'):
            task_id = task_id[5:]

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

        # 创建输出目录
        output_dir = os.path.join(self.output_dir, "版本接口测试", task_id)
        os.makedirs(output_dir, exist_ok=True)

        # 生成测试用例文件
        function_name = self.extract_function_name_from_file(target_api_file)
        if function_name:
            clean_function_name = function_name.lstrip('_').strip()
            test_filename = f"test_{clean_function_name}.py"
        else:
            api_basename = os.path.splitext(os.path.basename(target_api_file))[0]
            clean_basename = api_basename.lstrip('_').strip()
            test_filename = f"test_{clean_basename}.py"

        test_filepath = os.path.join(output_dir, test_filename)

        # 生成测试用例内容，传递所有API文件和接口信息
        test_content = self.generate_test_case_content(har_file_path, api_files, task_id, target_api_file, target_url)

        if not test_content:
            logger.info("无法生成测试用例内容")
            return None

        with open(test_filepath, 'w', encoding='utf-8') as f:
            f.write(test_content)

        logger.info(f"生成测试用例文件: {test_filepath}")
        return test_filepath
