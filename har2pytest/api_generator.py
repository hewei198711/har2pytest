import os
from typing import Any

from .config import APIConfig
from .har_generator import HARGenerator
from .logger import logger
from .swagger_handler import SwaggerHandler
from .utils import (
    determine_service_package,
    extract_function_name,
    format_parameter_value,
    match_path_template,
    write_test_file,
)


class APIGenerator:
    """API文件生成器类"""

    # 定义默认的 Swagger 信息结构常量
    DEFAULT_SWAGGER_INFO = {"description": "", "parameters": {}, "summary": ""}

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
        self.swagger_handler = SwaggerHandler(api_generator=self)

        # 初始化子生成器
        self.har_generator = HARGenerator(output_dir, self)

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
        function_name = extract_function_name(url)
        filename = f"{function_name}.py"

        root_filepath = os.path.join(self.output_dir, filename)
        if os.path.exists(root_filepath):
            return True

        if service_package != "api":
            package_filepath = os.path.join(self.output_dir, service_package, filename)
            if os.path.exists(package_filepath):
                return True

        return False

    def _generate_params_string(self, params_dict: dict[str, Any], swagger_info: dict[str, Any] = None) -> str:
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

    def _parse_request_info(self, request_info: dict[str, Any], swagger_data: dict[str, Any] = None) -> dict[str, Any]:
        """
        解析请求信息

        解析请求信息字典，提取method、url、query_params、post_data、headers等
        并处理路径参数和URL模式匹配

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等
            swagger_data: Swagger文档数据，可选，用于匹配路径模板

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

        # 获取 headers 名称集合（支持字典格式）
        if isinstance(headers_to_include, dict):
            headers_to_include = set(headers_to_include.keys())

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
        url_pattern, path_params, _ = match_path_template(url, swagger_data)

        # 如果 request_info 中包含路径参数，使用它
        if "path_params" in request_info and request_info["path_params"]:
            path_params = request_info["path_params"]

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

    def _generate_imports(self, parsed_info: dict[str, Any]) -> list[str]:
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

    def _process_parameters(self, parsed_info: dict[str, Any], swagger_info: dict[str, Any] = None) -> list[str]:
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
            params_section.append(f"headers = {headers}")
        else:
            params_section.append(f"headers = {headers}")

        return params_section

    def _handle_file_upload(self, post_data: Any) -> list[str]:
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
        path_params: dict[str, Any],
        query_params: dict[str, Any],
        is_need_urlencode: bool,
    ) -> list[str]:
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

    def _generate_function_definition(
        self, parsed_info: dict[str, Any], function_name: str, swagger_info: dict[str, Any]
    ) -> list[str]:
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
            function_def.append("    TODO: 添加接口描述")

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

    def generate_file_content(
        self,
        request_info: dict[str, Any],
        function_name: str,
        swagger_info: dict[str, Any] = None,
        parsed_info: dict[str, Any] = None,
    ) -> str:
        """
        生成API文件内容

        根据请求信息和函数名生成API文件内容

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等
            function_name: 函数名
            swagger_info: Swagger文档信息，包含description、parameters等
            parsed_info: 预解析的请求信息字典，如果为None则内部会解析

        Returns:
            str: 生成的文件内容

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
        if parsed_info is None:
            parsed_info = self._parse_request_info(request_info)
        imports = self._generate_imports(parsed_info)
        params_section = self._process_parameters(parsed_info, swagger_info)
        function_def = self._generate_function_definition(parsed_info, function_name, swagger_info)

        content_parts = imports + params_section + function_def
        return "\n".join(content_parts)

    def generate_api_file(
        self, request_info: dict[str, Any], force_overwrite: bool = False, swagger_info: dict[str, Any] = None
    ) -> str | None:
        """
        为单个API请求生成接口文件

        根据请求信息生成单个API接口文件，包括检查文件是否已存在、生成文件内容和保存文件

        Args:
            request_info: 请求信息字典，包含method、url、query_params、post_data、headers等
            force_overwrite: 如果为True，即使文件存在也会覆盖；如果为False，跳过已存在的文件
            swagger_info: Swagger文档信息，包含description、parameters等

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

        service_package = determine_service_package(url)

        # 先获取Swagger文档数据
        swagger_data = None
        if swagger_info is None:
            swagger_info = self.DEFAULT_SWAGGER_INFO.copy()
            try:
                # 检查服务包是否有对应的Swagger文档URL
                if service_package in APIConfig.SWAGGER_DOC_URLS():
                    # 获取Swagger文档URL
                    doc_base_url = APIConfig.SWAGGER_DOC_URLS()[service_package]
                    logger.info(f"服务包: {service_package}, Swagger文档URL: {doc_base_url}")

                    # 获取Swagger文档
                    swagger_data = self.swagger_handler.get_swagger_doc(doc_base_url)
                    if swagger_data:
                        logger.info(f"成功获取Swagger文档，路径数量: {len(swagger_data.get('paths', {}))}")
                        # 查找API信息（先使用原始URL查找）
                        swagger_info = self.swagger_handler.find_api_info_in_swagger(swagger_data, url, method)
                        logger.info(f"使用原始URL查找Swagger信息: {url}, 结果: {swagger_info}")
                    else:
                        logger.warning(f"无法获取Swagger文档: {doc_base_url}")
            except Exception as e:
                logger.debug(f"获取Swagger文档信息失败: {str(e)}")

        # 解析请求信息，传递Swagger文档数据用于匹配路径模板
        parsed_info = self._parse_request_info(request_info, swagger_data)
        url_pattern = parsed_info.get("url_pattern", url)

        # 如果有Swagger文档数据，再次查找API信息（使用匹配后的路径模板）
        if swagger_data and url_pattern != url:
            swagger_info = self.swagger_handler.find_api_info_in_swagger(swagger_data, url_pattern, method)

        # 检查文件是否存在
        if self.check_api_exists(url_pattern, service_package):
            if not force_overwrite:
                logger.info(f"接口已存在，跳过生成 (设置 force_overwrite=True 可覆盖): {method} {url_pattern}")
                return None
            else:
                logger.info(f"接口已存在，强制覆盖: {method} {url_pattern}")

        # 使用匹配后的路径模板生成函数名
        function_name = extract_function_name(url_pattern)

        base_filename = function_name
        filename = f"{base_filename}.py"

        if service_package == "apis":
            filepath = os.path.join(self.output_dir, filename)
        else:
            filepath = os.path.join(self.output_dir, service_package, filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        content = self.generate_file_content(request_info, function_name, swagger_info, parsed_info)

        write_test_file(filepath, content)

        logger.info(f"生成API文件: {filepath} (服务包: {service_package})")
        return filepath

    def generate_index_file(self, generated_files: list[str]):
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
                with open(package_init_path, encoding="utf-8") as f:
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
                # 生成相对导入语句（如 from ._user_mgmt_order_page import _user_mgmt_order_page）
                import_stmt = f"from .{last_part} import {last_part} # noqa: F401"

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
