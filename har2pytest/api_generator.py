# coding:utf-8

import os
import sys
import traceback
import subprocess
from typing import Any, Dict, List, Optional

from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .utils import format_parameter_value
from .swagger_updater import SwaggerDocUpdater


class APIGenerator:
    """API文件生成器类"""

    # 定义默认的 Swagger 信息结构常量
    DEFAULT_SWAGGER_INFO = {
        "description": "",
        "parameters": {},
        "summary": ""
    }

    def __init__(self, output_dir: str = None):
        """
        初始化API生成器

        Args:
            output_dir: API文件输出目录，默认为APIConfig.DEFAULT_SERVICE_PACKAGE

        Example:
            generator = APIGenerator(output_dir="api")
        """
        if output_dir is None:
            output_dir = APIConfig.DEFAULT_SERVICE_PACKAGE()
        self.output_dir = output_dir
        self.har_parser = HARParser()
        self.swagger_updater = SwaggerDocUpdater()

    @staticmethod
    def _match_path_template(url: str) -> tuple:
        """
        匹配路径模板

        匹配URL与APIConfig.PATH_URLS中的路径模板，提取路径参数
        如果没有匹配到模板，自动识别路径中的数字参数

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
        clean_url = url.lstrip("/")
        url_parts = clean_url.split("/")

        for path_pattern in APIConfig.PATH_URLS():
            pattern_parts = path_pattern.lstrip("/").split("/")

            if len(url_parts) != len(pattern_parts):
                continue

            matched = True
            result_parts = []
            path_params = {}

            for url_part, pattern_part in zip(url_parts, pattern_parts):
                if pattern_part.startswith("{") and pattern_part.endswith("}"):
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

        # 如果没有匹配到模板，自动识别路径中的数字参数
        result_parts = []
        path_params = {}
        url_pattern_parts = []

        for i, part in enumerate(url_parts):
            # 检查是否是数字
            if part.isdigit():
                # 生成参数名，如 id, item_id, order_id 等
                if i == len(url_parts) - 1:
                    param_name = "id"
                else:
                    # 尝试从路径中获取参数名
                    if i + 1 < len(url_parts) and url_parts[i + 1].isdigit():
                        param_name = f"param_{i}"
                    else:
                        # 尝试使用前一个路径部分作为参数名的一部分
                        if i > 0:
                            param_name = f"{url_parts[i-1]}_id"
                        else:
                            param_name = f"param_{i}"
                result_parts.append(param_name)
                path_params[param_name] = part
                url_pattern_parts.append(f"{{{param_name}}}")
            else:
                result_parts.append(part)
                url_pattern_parts.append(part)

        url_pattern = "/" + "/".join(url_pattern_parts)
        return url_pattern, path_params, result_parts

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

        if service_package != "api":
            package_filepath = os.path.join(self.output_dir, service_package, filename)
            if os.path.exists(package_filepath):
                return True

        return False

    def _generate_params_string(self, params_dict: Dict[str, Any], swagger_info: Dict[str, Any] = None) -> str:
        """
        生成API文件中的参数字符串

        将参数字典生成为Python代码字符串，为每个参数添加参数说明

        Args:
            params_dict: 参数字典，如 {"keyword": "TS001", "pageNum": 1}
            swagger_info: Swagger文档信息，包含description、parameters等

        Returns:
            str: 生成的参数字符串

        Example:
            params = {"keyword": "TS001", "pageNum": 1}
            result = generator.generate_params_string(params)
            # 返回生成的参数字符串
        """
        if swagger_info is None:
            swagger_info = self.DEFAULT_SWAGGER_INFO.copy()
        if not params_dict:
            return "{}"

        items = []
        for key, value in params_dict.items():
            formatted_value = format_parameter_value(value)
            # 从Swagger文档中获取参数说明
            param_desc = swagger_info.get("parameters", {}).get(key, "")
            if param_desc:
                items.append(f'"{key}": {formatted_value},  # {param_desc}')
            else:
                items.append(f'"{key}": {formatted_value},  # TODO: 添加参数说明')

        return "{\n" + "\n".join(items) + "\n}"

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
        method = request_info["method"].upper()
        url = request_info["url"]
        query_params = request_info.get("query_params", {})
        post_data = request_info.get("post_data", {})
        raw_headers = request_info.get("headers", {})

        # 只收录配置中指定的 headers 参数
        headers_to_include = APIConfig.HEADERS_TO_INCLUDE()
        headers = {}
        for key, value in raw_headers.items():
            if key.lower() in [h.lower() for h in headers_to_include]:
                headers[key] = value

        # 添加必须的 headers 字段及其默认值
        required_headers = APIConfig.REQUIRED_HEADERS()
        for key, default_value in required_headers.items():
            if key not in headers:
                headers[key] = default_value

        is_file_upload = False
        if method == "POST" and raw_headers.get("content-type", "").startswith("multipart/form-data"):
            is_file_upload = True
        
        is_need_urlencode = False
        if method == "POST" and raw_headers.get("content-length", "") == "0" and not post_data:
            is_need_urlencode = True

        # 使用辅助方法匹配路径模板
        url_pattern, path_params, _ = APIGenerator._match_path_template(url)

        if url_pattern:
            url = url_pattern

        return {
            "method": method,
            "url": url,
            "query_params": query_params,
            "post_data": post_data,
            "headers": headers,
            "is_file_upload": is_file_upload,
            "is_need_urlencode": is_need_urlencode,
            "path_params": path_params,
            "url_pattern": url_pattern,
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
        imports = []
        is_file_upload = parsed_info["is_file_upload"]
        is_need_urlencode = parsed_info["is_need_urlencode"]

        if is_file_upload:
            imports.append("import os")
            imports.append("from requests_toolbelt import MultipartEncoder")

        if is_need_urlencode:
            imports.append("from urllib.parse import urlencode")

        imports.append("from util.client import client")
        imports.append("")
        return imports

    def _process_parameters(self, parsed_info: Dict[str, Any], swagger_info: Dict[str, Any] = None) -> List[str]:
        """
        处理参数

        处理路径参数、查询参数和POST数据，生成参数定义代码

        Args:
            parsed_info: 解析后的请求信息字典
            swagger_info: Swagger文档信息，包含description、parameters等

        Returns:
            List[str]: 参数定义代码列表
        """
        if swagger_info is None:
            swagger_info = self.DEFAULT_SWAGGER_INFO.copy()
        params_section = []

        method = parsed_info["method"]
        path_params = parsed_info["path_params"]
        query_params = parsed_info["query_params"]
        post_data = parsed_info["post_data"]
        is_file_upload = parsed_info["is_file_upload"]
        is_need_urlencode = parsed_info["is_need_urlencode"]
        headers = parsed_info["headers"]

        param_name = None
        param_data = None

        if path_params:
            param_name = "params"
            param_data = path_params
        elif method == "GET" and query_params:
            param_name = "params"
            param_data = query_params
        elif method == "POST":
            if is_need_urlencode and query_params:
                param_name = "data"
                param_data = query_params
            elif post_data:
                if is_file_upload:
                    param_name = "files"
                    if isinstance(post_data, dict):
                        param_data = post_data
                    else:
                        raise ValueError("文件上传参数格式错误")
                elif isinstance(post_data, dict):
                    param_name = "data"
                    param_data = post_data
                else:
                    raise ValueError("参数格式错误")

        if param_name and param_data:
            formatted_params = self._generate_params_string(param_data, swagger_info)
            params_section.append(f"{param_name} = {formatted_params}")
            params_section.append("")

        # 添加 headers 参数定义
        if is_need_urlencode:
            is_need_urlencode_headers = headers.copy()
            is_need_urlencode_headers["content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            params_section.append(f'headers = {headers}')
        else:
            params_section.append(f'headers = {headers}')

        return params_section

    def _handle_file_upload(self, post_data: Any) -> List[str]:
        """
        处理文件上传

        生成文件上传的代码实现

        Args:
            post_data: POST数据

        Returns:
            List[str]: 文件上传代码列表
        """
        function_def = []
        function_def.append('    with open(files["file"], "rb") as f:')
        function_def.append('        filename = os.path.basename(files["file"])')
        function_def.append("        m = MultipartEncoder(")
        function_def.append("            fields={")
        if isinstance(post_data, dict):
            for key, value in post_data.items():
                if key == "file":
                    function_def.append('                "file": (filename, f, "text/plain")')
                else:
                    function_def.append(f'                "{key}": files["{key}"],')
            if "file" not in post_data:
                raise ValueError("文件上传参数格式错误")
        else:
            raise ValueError("文件上传参数格式错误")
        function_def.append("            }")
        function_def.append("        )")
        function_def.append('    headers["content-type"] = m.content_type')
        function_def.append("    with client.post(url=url, headers=headers, data=m) as r:")
        function_def.append("        return r")
        return function_def

    def _handle_http_method(
        self,
        method: str,
        param_name: str,
        path_params: Dict[str, Any],
        query_params: Dict[str, Any],
        is_need_urlencode: bool,
    ) -> List[str]:
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

        if method == "GET":
            if path_params:
                function_def.append("    with client.get(url=url, headers=headers) as r:")
            elif query_params:
                function_def.append("    with client.get(url=url, params=params, headers=headers) as r:")
            else:
                function_def.append("    with client.get(url=url, headers=headers) as r:")
        elif method == "POST":
            if param_name:
                if is_need_urlencode:
                    function_def.append(
                        "    data = urlencode(data) # application/x-www-form-urlencoded传参需要特殊处理"
                    )
                    function_def.append("")
                    function_def.append("    with client.post(url=url, data=data, headers=headers) as r:")
                else:
                    function_def.append("    with client.post(url=url, json=data, headers=headers) as r:")
            else:
                function_def.append("    with client.post(url=url, headers=headers) as r:")
        else:
            raise ValueError(f"不支持的HTTP方法: {method}。目前只支持GET和POST请求。")

        function_def.append("        return r")
        return function_def

    def _generate_function_definition(self, parsed_info: Dict[str, Any], function_name: str, swagger_info: Dict[str, Any]) -> List[str]:
        """
        生成函数定义

        生成函数定义和实现代码

        Args:
            parsed_info: 解析后的请求信息字典
            function_name: 函数名称
            swagger_info: Swagger文档信息，包含description、parameters等

        Returns:
            List[str]: 函数定义和实现代码列表
        """
        function_def = []

        method = parsed_info["method"]
        url = parsed_info["url"]
        query_params = parsed_info["query_params"]
        post_data = parsed_info["post_data"]
        is_file_upload = parsed_info["is_file_upload"]
        is_need_urlencode = parsed_info["is_need_urlencode"]
        path_params = parsed_info["path_params"]
        url_pattern = parsed_info["url_pattern"]
        headers = parsed_info["headers"]

        if path_params:
            param_name = "params"
        elif method == "GET":
            param_name = "params" if query_params else None
        elif method == "POST":
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
        func_params.append("headers=headers")

        function_def.append(f"def {function_name}({', '.join(func_params)}):")
        function_def.append('    """')

        # 使用Swagger文档中的描述信息
        if swagger_info.get("summary"):
            function_def.append(f"    {swagger_info['summary']}")
        elif swagger_info.get("description"):
            function_def.append(f"    {swagger_info['description']}")
        else:
            function_def.append('    TODO: 添加接口描述')
        
        function_def.append(f"    {url}")

        # 添加参数说明
        if swagger_info.get("parameters"):
            function_def.append("")
            function_def.append("    参数说明:")
            for param_name, param_desc in swagger_info["parameters"].items():
                function_def.append(f"    - {param_name}: {param_desc}")
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
            file_upload_code = self._handle_file_upload(post_data)
            function_def.extend(file_upload_code)
        else:
            http_method_code = self._handle_http_method(
                method, param_name, path_params, query_params, is_need_urlencode
            )
            function_def.extend(http_method_code)

        function_def.append("")
        return function_def

    def generate_file_content(self, request_info: Dict[str, Any], function_name: str, swagger_info: Dict[str, Any] = None) -> str:
        """
        生成API文件的内容

        生成单个API接口文件的完整内容，包括导入语句、参数定义和函数实现

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等
            function_name: 函数名，如 "_mobile_trade_orderCommit"
            swagger_info: Swagger文档信息，包含description、parameters等

        Returns:
            str: 生成的API文件内容

        Example:
            request_info = {
                "method": "POST",
                "url": "/mobile/trade/orderCommit",
                "query_params": {},
                "post_data": {"productId": "123"},
                "headers": {"content-type": "application/json"}
            }
            content = generator.generate_file_content(request_info, "_mobile_trade_orderCommit")
            # 返回生成的文件内容
        """
        if swagger_info is None:
            swagger_info = self.DEFAULT_SWAGGER_INFO.copy()
        parsed_info = self._parse_request_info(request_info)
        imports = self._generate_imports(parsed_info)
        params_section = self._process_parameters(parsed_info, swagger_info)
        function_def = self._generate_function_definition(parsed_info, function_name, swagger_info)

        content_parts = imports + params_section + function_def
        return "\n".join(content_parts)

    def generate_api_file(self, request_info: Dict[str, Any], force_overwrite: bool = False) -> Optional[str]:
        """
        为单个API请求生成接口文件

        根据请求信息生成单个API接口文件，包括检查文件是否已存在、生成文件内容和保存文件

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等
            force_overwrite: 如果为True，即使文件存在也会覆盖；如果为False，跳过已存在的文件

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
        method = request_info["method"].upper()
        url = request_info["url"]

        service_package = self.determine_service_package(url)

        # 检查文件是否存在
        if self.check_api_exists(url, service_package):
            if not force_overwrite:
                logger.info(f"接口已存在，跳过生成 (设置 force_overwrite=True 可覆盖): {method} {url}")
                return None
            else:
                logger.info(f"接口已存在，强制覆盖: {method} {url}")

        function_name = self.extract_function_name(url)

        base_filename = function_name
        filename = f"{base_filename}.py"

        if service_package == "apis":
            filepath = os.path.join(self.output_dir, filename)
        else:
            filepath = os.path.join(self.output_dir, service_package, filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # 解析请求信息，获取 url_pattern
        parsed_info = self._parse_request_info(request_info)
        url_pattern = parsed_info.get("url_pattern", url)

        # 获取Swagger文档信息
        swagger_info = self.DEFAULT_SWAGGER_INFO.copy()
        try:
            swagger_info = self.swagger_updater.get_api_info(url_pattern, method)
        except Exception as e:
            logger.debug(f"获取Swagger文档信息失败: {str(e)}")

        content = self.generate_file_content(request_info, function_name, swagger_info)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        # 使用black格式化生成的文件
        try:
            black_path = os.path.join(os.path.dirname(sys.executable), "black")
            subprocess.run([black_path, filepath], capture_output=True, text=True)
            logger.info(f"使用black格式化API文件: {filepath}")
        except Exception as e:
            logger.warning(f"格式化文件失败: {str(e)}")

        logger.info(f"生成API文件: {filepath} (服务包: {service_package})")
        return filepath

    def generate_api_files_from_har(self, har_file_path: str, force_overwrite: bool = False) -> List[str]:
        """
        从HAR文件生成所有API接口文件

        解析HAR文件中的所有请求，为每个请求生成对应的API接口文件

        Args:
            har_file_path: HAR文件路径，如 "api_request.har"
            force_overwrite: 是否覆盖已存在的文件

        Returns:
            List[str]: 生成的文件路径列表

        Example:
            files = generator.generate_api_files_from_har("普通订单.har")
            # 返回生成的文件路径列表，如 ["api/_mobile_product_search.py", "api/_mobile_trade_orderCommit.py"]
        """
        requests = self.har_parser.extract_requests_from_har(har_file_path)

        if not requests:
            logger.info(f"HAR文件 {har_file_path} 中没有找到有效的API请求")
            return []

        logger.info(f"发现 {len(requests)} 个API请求")

        generated_files = []
        for request_info in requests:
            try:
                filepath = self.generate_api_file(request_info, force_overwrite=force_overwrite)
                if filepath:
                    generated_files.append(filepath)
            except Exception as e:
                logger.error(f"生成API文件失败: {str(e)}")
                logger.error(traceback.format_exc())

        return generated_files

    def generate_index_file(self, generated_files: List[str]):
        """
        生成API索引文件

        为生成的API文件生成__init__.py索引文件，包含所有API模块的导入语句
        按照服务包分组，在每个服务包的__init__.py文件中添加对应的导入语句

        Args:
            generated_files: 生成的文件路径列表，如 ["api/_mobile_product_search.py", "api/_mobile_trade_orderCommit.py"]

        Returns:
            None: 生成的索引文件保存在output_dir/__init__.py

        Example:
            files = generator.generate_api_files_from_har("普通订单.har")
            generator.generate_index_file(files)
            # 生成api/__init__.py索引文件
        """
        # 按照服务包分组
        service_packages = {}
        for filepath in generated_files:
            # 获取文件相对于 output_dir 的路径
            rel_path = filepath.replace(self.output_dir, "").replace("\\", "/").lstrip("/")
            # 获取服务包名称（第一级目录）
            path_parts = rel_path.split("/")
            if len(path_parts) >= 2:
                service_package = path_parts[0]
                if service_package not in service_packages:
                    service_packages[service_package] = []
                service_packages[service_package].append(filepath)

        # 为每个服务包生成索引文件
        for service_package, files in service_packages.items():
            package_dir = os.path.join(self.output_dir, service_package)
            package_init_path = os.path.join(package_dir, "__init__.py")

            # 确保服务包目录存在
            if not os.path.exists(package_dir):
                os.makedirs(package_dir, exist_ok=True)

            # 读取或创建服务包的 __init__.py 文件
            if os.path.exists(package_init_path):
                with open(package_init_path, "r", encoding="utf-8") as f:
                    content = f.read().splitlines()
            else:
                content = [""]

            # 收集需要添加的导入语句
            import_statements = []
            for filepath in files:
                module_path = filepath.replace(self.output_dir, "").replace("\\", "/").lstrip("/")
                module_name = module_path.replace(".py", "").replace("/", ".")
                # 获取模块名的最后一部分作为导入的函数名
                last_part = module_name.split(".")[-1]
                import_stmt = f"from {module_name} import {last_part}"
                
                # 检查导入语句是否已存在
                if import_stmt not in content:
                    import_statements.append(import_stmt)

            # 如果有新的导入语句，添加到文件末尾
            if import_statements:
                # 确保文件末尾有空白行
                if content and content[-1].strip():
                    content.append("")
                
                # 添加新的导入语句
                content.extend(import_statements)
                content.append("")

                # 写回文件
                with open(package_init_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(content))

                logger.info(f"更新服务包索引文件: {package_init_path}")
            else:
                logger.info(f"服务包索引文件已包含所有API引用: {package_init_path}")

        # 确保主目录存在 __init__.py 文件
        main_init_path = os.path.join(self.output_dir, "__init__.py")
        if not os.path.exists(main_init_path):
            # 创建空白的 __init__.py 文件
            with open(main_init_path, "w", encoding="utf-8") as f:
                f.write("")
            logger.info(f"创建主目录索引文件: {main_init_path}")

    def _extract_params_from_swagger(
        self,
        parameters: List[Dict[str, Any]],
        swagger_data: Dict[str, Any]
    ) -> tuple:
        """
        从Swagger文档提取参数

        处理查询参数和请求体参数，提取默认值和参数信息

        Args:
            parameters: Swagger文档中的参数列表
            swagger_data: 完整的Swagger文档数据

        Returns:
            tuple: (query_params, post_data, has_query_param, has_body_param)
        """
        query_params = {}
        post_data = {}
        has_query_param = False
        has_body_param = False

        for param in parameters:
            param_name = param.get("name")
            param_in = param.get("in")
            param_type = param.get("type", "string")

            if param_in == "query":
                has_query_param = True
                query_params[param_name] = self._get_default_value(param_type)
            elif param_in == "body" and "schema" in param:
                has_body_param = True
                post_data = self._extract_body_params(param["schema"], swagger_data)

        return query_params, post_data, has_query_param, has_body_param

    def _get_default_value(self, param_type: str) -> Any:
        """
        根据参数类型获取默认值

        Args:
            param_type: 参数类型

        Returns:
            Any: 默认值
        """
        if param_type == "string":
            return ""
        elif param_type == "integer":
            return 0
        elif param_type == "boolean":
            return False
        return ""

    def _extract_body_params(
        self,
        schema: Dict[str, Any],
        swagger_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        从body参数schema中提取参数

        处理模型引用和内联模型

        Args:
            schema: 参数的schema定义
            swagger_data: 完整的Swagger文档数据

        Returns:
            Dict[str, Any]: 提取的参数字典
        """
        body_params = {}

        if "$ref" in schema:
            ref = schema["$ref"]
            ref_name = ref.split("/")[-1]
            if "definitions" in swagger_data and ref_name in swagger_data["definitions"]:
                definition = swagger_data["definitions"][ref_name]
                if "properties" in definition:
                    for prop_name, prop_info in definition["properties"].items():
                        prop_type = prop_info.get("type", "string")
                        body_params[prop_name] = self._get_default_value(prop_type)
        elif "properties" in schema:
            for prop_name, prop_info in schema["properties"].items():
                prop_type = prop_info.get("type", "string")
                body_params[prop_name] = self._get_default_value(prop_type)

        return body_params

    def generate_apis_from_swagger(self, swagger_url: str, force_overwrite: bool = False) -> List[str]:
        """
        从Swagger文档生成API文件

        解析Swagger文档，获取所有API路径和方法，为每个API生成对应的API文件

        Args:
            swagger_url: Swagger文档URL
            force_overwrite: 是否覆盖已存在的文件

        Returns:
            List[str]: 生成的文件路径列表
        """

        generated_files = []

        try:
            # 获取Swagger文档
            swagger_data = self.swagger_updater.get_swagger_doc(swagger_url)
            if not swagger_data:
                logger.error(f"无法获取Swagger文档: {swagger_url}")
                return generated_files

            # 遍历所有API路径
            paths = swagger_data.get("paths", {})
            logger.info(f"从Swagger文档中发现 {len(paths)} 个API路径")

            for path, methods in paths.items():
                # 遍历支持的HTTP方法
                for method, method_data in methods.items():
                    try:
                        # 构建请求信息
                        request_info = {
                            "method": method.upper(),
                            "url": path,
                            "query_params": {},
                            "post_data": {},
                            "headers": APIConfig.REQUIRED_HEADERS()
                        }

                        # 提取参数
                        parameters = method_data.get("parameters", [])
                        query_params, post_data, has_query_param, has_body_param = \
                            self._extract_params_from_swagger(parameters, swagger_data)

                        request_info["query_params"] = query_params
                        request_info["post_data"] = post_data

                        # 判断是否需要urlencode
                        if method.upper() == "POST" and has_query_param and not post_data and not has_body_param:
                            request_info["headers"]["content-length"] = "0"

                        # 生成API文件
                        filepath = self.generate_api_file(request_info, force_overwrite)
                        if filepath:
                            generated_files.append(filepath)
                            logger.info(f"✓ 生成API文件: {filepath}")
                        else:
                            logger.info(f"- 跳过已存在的API文件: {path}")

                    except Exception as e:
                        logger.error(f"❌ 生成API文件失败 {path} {method}: {str(e)}")
                        logger.debug(traceback.format_exc())

            logger.info(f"\n============================================")
            logger.info(f"从Swagger文档生成完成:")
            logger.info(f"✓ 成功生成: {len(generated_files)} 个API文件")
            logger.info(f"============================================")

        except Exception as e:
            logger.error(f"❌ 从Swagger文档生成API文件失败: {str(e)}")
            logger.debug(traceback.format_exc())

        return generated_files
