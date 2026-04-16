# coding:utf-8


import os
import re
from typing import Dict, Any, List, Optional

from .config import APIConfig
from .har_parser import HARParser
from .utils import format_single_parameter_value


class APIGenerator:
    """API文件生成器类"""

    def __init__(self, output_dir: str = APIConfig.DEFAULT_SERVICE_PACKAGE):
        """
        初始化API生成器

        Args:
            output_dir: API文件输出目录，默认为APIConfig.DEFAULT_SERVICE_PACKAGE

        Example:
            generator = APIGenerator(output_dir="api")
        """
        self.output_dir = output_dir
        self.har_parser = HARParser()

    @staticmethod
    def _match_path_template(url: str) -> tuple:
        """
        匹配路径模板

        匹配URL与APIConfig.PATH_URLS中的路径模板，提取路径参数

        Args:
            url: 原始接口URL，如 /mobile/trade/orderCommit

        Returns:
            tuple: (url_pattern, path_params, result_parts)
                - url_pattern: 匹配的路径模板，如 /user/{userId}/info
                - path_params: 路径参数字典，如 {"userId": "123"}
                - result_parts: 路径部分列表，用于生成函数名

        Example:
            url = "/user/123/info"
            pattern, params, parts = APIGenerator._match_path_template(url)
            # 返回 ("/user/{userId}/info", {"userId": "123"}, ["user", "userId", "info"])
        """
        clean_url = url.lstrip('/')
        url_parts = clean_url.split('/')

        for path_pattern in APIConfig.PATH_URLS:
            pattern_parts = path_pattern.lstrip('/').split('/')

            if len(url_parts) != len(pattern_parts):
                continue

            matched = True
            result_parts = []
            path_params = {}

            for url_part, pattern_part in zip(url_parts, pattern_parts):
                if pattern_part.startswith('{') and pattern_part.endswith('}'):
                    param_name = pattern_part[1:-1]
                    result_parts.append(param_name)
                    path_params[param_name] = url_part
                else:
                    if url_part != pattern_part:
                        matched = False
                        break
                    result_parts.append(url_part)

            if matched:
                return path_pattern, path_params, result_parts

        return None, {}, url_parts

    @staticmethod
    def extract_function_name(url: str) -> str:
        """
        从URL中提取测试方法函数名
        优先匹配 APIConfig.PATH_URLS 中的路径模板，处理路径参数 {xxx}
        无匹配时，直接将URL路径用下划线连接并清理非法字符

        Args:
            url: 原始接口URL，如 /mobile/trade/orderCommit

        Returns:
            str: 生成的函数名片段，如 _mobile_trade_orderCommit

        Example:
            URL: /mobile/trade/orderCommit → 返回 _mobile_trade_orderCommit
            URL: /user/{userId}/info → 返回 _user_userId_info
        """
        # 使用辅助方法匹配路径模板
        _, _, result_parts = APIGenerator._match_path_template(url)
        return f"_{'_'.join(result_parts)}"

    @staticmethod
    def determine_service_package(url: str) -> str:
        """
        根据URL的第一个字段判断属于哪个微服务包

        Args:
            url: 原始接口URL，如 /mobile/trade/orderCommit

        Returns:
            str: 服务包名称，如 mall_mobile_application

        Example:
            URL: /mobile/trade/orderCommit → 返回 mall_mobile_application
            URL: /member/info → 返回 mall_center_member
        """
        return APIConfig.determine_service_package(url)

    def check_api_exists(self, url: str, service_package: str) -> bool:
        """
        检查API接口文件是否已经存在

        Args:
            url: 原始接口URL，如 /mobile/trade/orderCommit
            service_package: 服务包名称，如 mall_mobile_application

        Returns:
            bool: 如果API文件已存在返回True，否则返回False

        Example:
            exists = generator.check_api_exists("/mobile/trade/orderCommit", "mall_mobile_application")
            # 如果文件存在返回True，否则返回False
        """
        function_name = self.extract_function_name(url)
        filename = f"{function_name}.py"

        root_filepath = os.path.join(self.output_dir, filename)
        if os.path.exists(root_filepath):
            return True

        if service_package != 'api':
            package_filepath = os.path.join(self.output_dir, service_package, filename)
            if os.path.exists(package_filepath):
                return True

        return False

    def format_params_for_api_file(self, params_dict: Dict[str, Any]) -> str:
        """
        格式化参数为API文件中的参数字符串

        将参数字典格式化为Python代码字符串，支持多行值和添加TODO注释

        Args:
            params_dict: 参数字典，如 {"keyword": "TS001", "pageNum": 1}

        Returns:
            str: 格式化后的参数字符串，如 '{\n    "keyword": "TS001", # TODO: 添加参数说明\n    "pageNum": 1 # TODO: 添加参数说明\n}'

        Example:
            params = {"keyword": "TS001", "pageNum": 1}
            result = generator.format_params_for_api_file(params)
            # 返回格式化后的参数字符串
        """
        if not params_dict:
            return "{}"

        lines = ["{"]
        for i, (key, value) in enumerate(params_dict.items()):
            formatted_value = format_single_parameter_value(value)

            if '\n' in formatted_value:
                value_lines = formatted_value.split('\n')
                lines.append(f'    "{key}": {value_lines[0]}')
                for line in value_lines[1:]:
                    if line.strip():
                        lines.append(f'    {line}')
                    else:
                        lines.append('')
                if i < len(params_dict) - 1:
                    lines[-1] = lines[-1].rstrip() + ', # TODO: 添加参数说明'
                else:
                    lines[-1] = lines[-1].rstrip() + ' # TODO: 添加参数说明'
            else:
                comment = ', # TODO: 添加参数说明' if i < len(params_dict) - 1 else ' # TODO: 添加参数说明'
                lines.append(f'    "{key}": {formatted_value}{comment}')

        lines.append("}")

        return '\n'.join(lines)

    def _parse_request_info(self, request_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析请求信息

        解析请求信息字典，提取method、url、query_params、post_data、headers等
        并处理路径参数和URL模式匹配

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等

        Returns:
            Dict[str, Any]: 解析后的请求信息字典
        """
        method = request_info['method'].upper()
        url = request_info['url']
        query_params = request_info.get('query_params', {})
        post_data = request_info.get('post_data', {})
        headers = request_info.get('headers', {})

        is_file_upload = False
        if method == 'POST' and headers.get('content-type', '').startswith('multipart/form-data'):
            is_file_upload = True

        # 使用辅助方法匹配路径模板
        url_pattern, path_params, _ = APIGenerator._match_path_template(url)

        if url_pattern:
            url = url_pattern

        return {
            'method': method,
            'url': url,
            'query_params': query_params,
            'post_data': post_data,
            'headers': headers,
            'is_file_upload': is_file_upload,
            'path_params': path_params,
            'url_pattern': url_pattern
        }

    def _generate_imports(self, parsed_info: Dict[str, Any]) -> List[str]:
        """
        生成导入语句

        根据解析后的请求信息生成必要的导入语句

        Args:
            parsed_info: 解析后的请求信息字典

        Returns:
            List[str]: 导入语句列表
        """
        imports = [
            "# coding:utf-8",
            "",
            "from setting import TIMEOUT, VERIFY, access_token",
        ]

        method = parsed_info['method']
        headers = parsed_info['headers']
        is_file_upload = parsed_info['is_file_upload']

        need_urlencode = False
        if method == 'POST' and headers.get('content-length', '') == '0':
            need_urlencode = True

        if need_urlencode:
            imports.append("from urllib.parse import urlencode")

        imports.append("from util.client import client")

        if is_file_upload:
            imports.append("from requests_toolbelt import MultipartEncoder")

        imports.append("")
        return imports

    def _process_parameters(self, parsed_info: Dict[str, Any]) -> List[str]:
        """
        处理参数

        处理路径参数、查询参数和POST数据，生成参数定义代码

        Args:
            parsed_info: 解析后的请求信息字典

        Returns:
            List[str]: 参数定义代码列表
        """
        params_section = []

        method = parsed_info['method']
        path_params = parsed_info['path_params']
        query_params = parsed_info['query_params']
        post_data = parsed_info['post_data']
        is_file_upload = parsed_info['is_file_upload']
        headers = parsed_info['headers']

        need_urlencode = False
        if method == 'POST' and headers.get('content-length', '') == '0':
            need_urlencode = True

        param_name = None
        param_data = None

        if path_params:
            param_name = "params"
            param_data = path_params
        elif method == 'GET' and query_params:
            param_name = "params"
            param_data = query_params
        elif method == 'POST':
            if need_urlencode and query_params:
                param_name = "data"
                param_data = query_params
            elif post_data:
                if is_file_upload:
                    param_name = "files"
                    if isinstance(post_data, dict):
                        param_data = post_data
                    else:
                        param_data = {
                            "storageType": "PublicCloud",
                            "clientKey": "mall-center-product",
                            "file": "data/示例文件.png"
                        }
                elif isinstance(post_data, dict):
                    param_name = "data"
                    param_data = post_data
                else:
                    raise ValueError("参数格式错误")

        if param_name and param_data:
            if param_name == "files" and isinstance(param_data, dict):
                params_section.append("files = {")
                for key, value in param_data.items():
                    if key == 'file':
                        params_section.append(f'    "{key}": "data/示例文件.png" # 文件路径')
                    else:
                        formatted_value = format_single_parameter_value(value)
                        params_section.append(f'    "{key}": {formatted_value}, # TODO: 添加参数说明')
                if 'file' not in param_data:
                    params_section.append('    "file": "data/示例文件.png" # 文件路径')
                params_section.append("}")
                params_section.append("")
            else:
                formatted_params = self.format_params_for_api_file(param_data)
                params_section.append(f"{param_name} = {formatted_params}")
                params_section.append("")

        return params_section

    def _handle_file_upload(self, post_data: Any, url: str) -> List[str]:
        """
        处理文件上传

        生成文件上传的代码实现

        Args:
            post_data: POST数据
            url: 请求URL

        Returns:
            List[str]: 文件上传代码列表
        """
        function_def = []
        function_def.append("    ")
        function_def.append('    with open(files["file"], "rb") as f:')
        function_def.append('        index = files["file"].find(".")')
        function_def.append('        m = MultipartEncoder(')
        function_def.append('            fields={')
        if isinstance(post_data, dict):
            for key, value in post_data.items():
                if key == 'file':
                    function_def.append('                "file": (files["file"][5:index], f, "text/plain")')
                else:
                    function_def.append(f'                "{key}": files["{key}"],')
            if 'file' not in post_data:
                function_def.append('                "file": (files["file"][5:index], f, "text/plain")')
        else:
            function_def.append('                "storageType": files["storageType"],')
            function_def.append('                "clientKey": files["clientKey"],')
            function_def.append('                "file": (files["file"][5:index], f, "text/plain")')
        function_def.append('            }')
        function_def.append('        )')
        function_def.append('        ')
        function_def.append('        headers = {"Authorization": f"bearer {access_token}", \'Content-Type\': m.content_type}')
        function_def.append('        ')
        function_def.append('        with client.post(url=url, headers=headers, data=m) as r:')
        function_def.append('            return r')
        return function_def

    def _handle_http_method(self, method: str, param_name: str, path_params: Dict[str, Any], 
                           query_params: Dict[str, Any], need_urlencode: bool, url: str) -> List[str]:
        """
        处理HTTP方法

        生成不同HTTP方法的代码实现

        Args:
            method: HTTP方法
            param_name: 参数名称
            path_params: 路径参数
            query_params: 查询参数
            need_urlencode: 是否需要urlencode
            url: 请求URL

        Returns:
            List[str]: HTTP方法代码列表
        """
        function_def = []
        if need_urlencode:
            function_def.append('    headers = {"Authorization": f"bearer {access_token}", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}')
        else:
            function_def.append('    headers = {"Authorization": f"bearer {access_token}"}')
        function_def.append("")

        if method == 'GET':
            if path_params:
                function_def.append('    with client.get(url=url, headers=headers) as r:')
            elif query_params:
                function_def.append('    with client.get(url=url, headers=headers, params=params) as r:')
            else:
                function_def.append('    with client.get(url=url, headers=headers) as r:')
        elif method == 'POST':
            if param_name:
                if need_urlencode:
                    function_def.append('    data = urlencode(data) # application/x-www-form-urlencoded传参需要特殊处理')
                    function_def.append('')
                    function_def.append('    with client.post(url=url, headers=headers, data=data) as r:')
                else:
                    function_def.append('    with client.post(url=url, headers=headers, json=data) as r:')
            else:
                function_def.append('    with client.post(url=url, headers=headers) as r:')
        else:
            raise ValueError(f"不支持的HTTP方法: {method}。目前只支持GET和POST请求。")

        function_def.append('        return r')
        return function_def

    def _generate_function_definition(self, parsed_info: Dict[str, Any], function_name: str) -> List[str]:
        """
        生成函数定义

        生成函数定义和实现代码

        Args:
            parsed_info: 解析后的请求信息字典
            function_name: 函数名称

        Returns:
            List[str]: 函数定义和实现代码列表
        """
        function_def = []

        method = parsed_info['method']
        url = parsed_info['url']
        query_params = parsed_info['query_params']
        post_data = parsed_info['post_data']
        is_file_upload = parsed_info['is_file_upload']
        path_params = parsed_info['path_params']
        url_pattern = parsed_info['url_pattern']
        headers = parsed_info['headers']

        need_urlencode = False
        if method == 'POST' and headers.get('content-length', '') == '0':
            need_urlencode = True

        if path_params:
            param_name = "params"
        elif method == 'GET':
            param_name = "params" if query_params else None
        elif method == 'POST':
            if query_params:
                param_name = "data"
            elif is_file_upload:
                param_name = "files" if post_data else None
            else:
                param_name = "data" if post_data else None
        else:
            param_name = None

        func_params = []
        if param_name:
            func_params.append(f"{param_name}={param_name}")
        func_params.append("access_token=access_token")

        function_def.append(f"def {function_name}({', '.join(func_params)}):")
        function_def.append('    """')
        function_def.append(f"    TODO: 添加接口描述")
        function_def.append(f"    {url}")
        function_def.append('    """')
        function_def.append("")

        if path_params and url_pattern:
            url_with_params = url_pattern
            for param_name in path_params.keys():
                url_with_params = url_with_params.replace(f"{{{param_name}}}", f"{{params['{param_name}']}}")
            function_def.append(f'    url = f"{url_with_params}"')
        else:
            function_def.append(f'    url = "{url}"')

        if is_file_upload:
            file_upload_code = self._handle_file_upload(post_data, url)
            function_def.extend(file_upload_code)
        else:
            http_method_code = self._handle_http_method(method, param_name, path_params, 
                                                      query_params, need_urlencode, url)
            function_def.extend(http_method_code)

        function_def.append("")
        return function_def

    def generate_file_content(self, request_info: Dict[str, Any], function_name: str) -> str:
        """
        生成API文件内容

        根据请求信息生成完整的API接口文件内容，包括导入语句、参数定义和函数实现

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等
            function_name: 函数名称，如 _mobile_trade_orderCommit

        Returns:
            str: 完整的API文件内容字符串

        Example:
            request_info = {
                "method": "POST",
                "url": "/mobile/trade/orderCommit",
                "query_params": {},
                "post_data": {"productId": "123"},
                "headers": {"content-type": "application/json"}
            }
            content = generator.generate_file_content(request_info, "_mobile_trade_orderCommit")
            # 返回完整的API文件内容
        """
        parsed_info = self._parse_request_info(request_info)
        imports = self._generate_imports(parsed_info)
        params_section = self._process_parameters(parsed_info)
        function_def = self._generate_function_definition(parsed_info, function_name)

        content_parts = imports + params_section + function_def
        return '\n'.join(content_parts)

    def generate_api_file(self, request_info: Dict[str, Any]) -> Optional[str]:
        """
        为单个API请求生成接口文件

        根据请求信息生成单个API接口文件，包括检查文件是否已存在、生成文件内容和保存文件

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等

        Returns:
            Optional[str]: 生成的文件路径，如果文件已存在则返回None

        Example:
            request_info = {
                "method": "POST",
                "url": "/mobile/trade/orderCommit",
                "query_params": {},
                "post_data": {"productId": "123"},
                "headers": {"content-type": "application/json"}
            }
            filepath = generator.generate_api_file(request_info)
            # 返回生成的文件路径，如 "api/mall_mobile_application/_mobile_trade_orderCommit.py"
        """
        method = request_info['method'].upper()
        url = request_info['url']

        service_package = self.determine_service_package(url)

        if self.check_api_exists(url, service_package):
            print(f"接口已存在，跳过生成: {method} {url} (服务包: {service_package})")
            return None

        function_name = self.extract_function_name(url)

        base_filename = function_name
        filename = f"{base_filename}.py"

        if service_package == 'api':
            filepath = os.path.join(self.output_dir, filename)
        else:
            filepath = os.path.join(self.output_dir, service_package, filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        content = self.generate_file_content(request_info, function_name)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"生成API文件: {filepath} (服务包: {service_package})")
        return filepath

    def generate_api_files_from_har(self, har_file_path: str) -> List[str]:
        """
        从HAR文件生成所有API接口文件

        解析HAR文件中的所有请求，为每个请求生成对应的API接口文件

        Args:
            har_file_path: HAR文件路径，如 "普通订单.har"

        Returns:
            List[str]: 生成的文件路径列表

        Example:
            files = generator.generate_api_files_from_har("普通订单.har")
            # 返回生成的文件路径列表，如 ["api/_mobile_product_search.py", "api/_mobile_trade_orderCommit.py"]
        """
        requests = self.har_parser.extract_requests_from_har(har_file_path)

        if not requests:
            print(f"HAR文件 {har_file_path} 中没有找到有效的API请求")
            return []

        print(f"发现 {len(requests)} 个API请求")

        generated_files = []
        for request_info in requests:
            try:
                filepath = self.generate_api_file(request_info)
                if filepath:
                    generated_files.append(filepath)
            except Exception as e:
                print(f"生成API文件失败: {str(e)}")
                import traceback
                traceback.print_exc()

        return generated_files

    def generate_index_file(self, generated_files: List[str]):
        """
        生成API索引文件

        为生成的API文件生成__init__.py索引文件，包含所有API模块的导入语句

        Args:
            generated_files: 生成的文件路径列表，如 ["api/_mobile_product_search.py", "api/_mobile_trade_orderCommit.py"]

        Returns:
            None: 生成的索引文件保存在output_dir/__init__.py

        Example:
            files = generator.generate_api_files_from_har("普通订单.har")
            generator.generate_index_file(files)
            # 生成api/__init__.py索引文件
        """
        index_path = os.path.join(self.output_dir, '__init__.py')

        content = [
            "# coding:utf-8",
            "",
            f"# 自动生成的API索引文件",
            f"# 生成时间: {__import__('datetime').datetime.now()}",
            "",
            ""
        ]

        for filepath in generated_files:
            module_path = filepath.replace(self.output_dir, '').replace('\\', '/').lstrip('/')
            module_name = module_path.replace('.py', '').replace('/', '.')
            content.append(f"# from {module_name} import *")

        content.append("")

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

        print(f"生成索引文件: {index_path}")
