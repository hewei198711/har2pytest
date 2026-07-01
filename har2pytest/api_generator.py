import os
from typing import Any

from .config import APIConfig
from .logger import logger
from .swagger_handler import SwaggerHandler
from .url_matcher import URLMatcher
from .utils import (
    format_headers_for_python,
    format_parameter_value,
    format_params_for_python,
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
            output_dir: API文件输出目录，默认为APIConfig.DEFAULT_API_DIR

        Example:
            generator = APIGenerator(output_dir="api")
        """
        if output_dir is None:
            output_dir = APIConfig.DEFAULT_API_DIR()
        self.output_dir = output_dir
        self.swagger_handler = SwaggerHandler(api_generator=self)
        self.url_matcher = URLMatcher()

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
        function_name = URLMatcher.generate_function_name(url)
        filename = f"{function_name}.py"

        # 检查根目录是否存在
        root_filepath = os.path.join(self.output_dir, filename)
        if os.path.exists(root_filepath):
            return True

        # 检查服务包目录是否存在
        if service_package != "apis":
            package_filepath = os.path.join(self.output_dir, service_package, filename)
            if os.path.exists(package_filepath):
                return True

        return False

    def _parse_request_info(self, request_info: dict[str, Any]) -> dict[str, Any]:
        """解析请求信息"""
        method = request_info["method"].upper()
        url = request_info["url"]
        query_params = request_info.get("query_params", {})
        post_data = request_info.get("post_data", {})
        raw_headers = request_info.get("headers", {})

        headers = dict(raw_headers)
        required_headers = APIConfig.REQUIRED_HEADERS()
        for key, default_value in required_headers.items():
            if key not in headers:
                headers[key] = default_value

        # 一次性遍历 raw_headers 提取 content-type 和 content-length
        content_type = ""
        content_length = ""
        for k, v in raw_headers.items():
            kl = k.lower()
            if kl == "content-type":
                content_type = v
            elif kl == "content-length":
                content_length = v

        is_file_upload = False
        is_multipart = False
        is_json_content = False

        if method == "POST":
            if content_type and "application/json" in content_type:
                is_json_content = True
            elif content_type and content_type.startswith("multipart/form-data"):
                is_multipart = True
                if post_data and isinstance(post_data, dict):
                    for v in post_data.values():
                        v_str = str(v)
                        if v_str == "(binary)" or v_str.startswith("@"):
                            is_file_upload = True
                            break
            elif content_type and "application/x-www-form-urlencoded" in content_type:
                is_json_content = False
            elif not content_type:
                is_json_content = bool(post_data)

        is_need_urlencode = method == "POST" and content_length == "0" and not post_data

        # 清理 headers：移除 content-length 和 multipart 时的 content-type
        for key in list(headers.keys()):
            kl = key.lower()
            if kl == "content-length":
                del headers[key]
            elif not is_need_urlencode and kl == "content-type":
                del headers[key]

        # 使用统一的URL匹配器（swagger_data已在外部设置）
        url_info = self.url_matcher.get_url_info(url)

        return {
            "method": method,
            "url": url_info["pattern"] or url,  # 使用匹配到的模板URL
            "query_params": query_params,
            "post_data": post_data,
            "headers": headers,
            "is_file_upload": is_file_upload,
            "is_multipart": is_multipart,
            "is_need_urlencode": is_need_urlencode,
            "is_json_content": is_json_content,
            "path_params": url_info["path_params"],
            "url_pattern": url_info["pattern"],
            "function_name": url_info["function_name"],
        }

    async def generate_api_file(self, request_info: dict, force_overwrite: bool = False, swagger_info: dict = None, swagger_doc: dict = None):
        """生成API文件（异步）

        Args:
            request_info: 请求信息字典
            force_overwrite: 是否强制覆盖已存在的文件
            swagger_info: Swagger API 信息（summary、description、parameters）
            swagger_doc: 预取的 Swagger 完整文档，传入后跳过内部获取，避免并行竞态条件
        """
        method = request_info["method"].upper()
        url = request_info["url"]

        service_package = APIConfig.determine_service_package(url)
        # 如果已传入swagger_info，不需要获取Swagger文档
        if swagger_info is None:
            # 获取整个Swagger文档（用于URL模板匹配和获取API信息）
            if swagger_doc is None:
                if service_package in APIConfig.SWAGGER_DOC_URLS():
                    swagger_doc = await self.swagger_handler.get_swagger_doc(APIConfig.SWAGGER_DOC_URLS()[service_package])

            # 设置swagger_data到url_matcher
            self.url_matcher.swagger_data = swagger_doc

            # 解析请求信息，获取URL模式
            parsed_info = self._parse_request_info(request_info)
            url_pattern = parsed_info.get("url_pattern", url)

            # 获取特定URL的Swagger信息（summary、description、parameters）
            if swagger_doc:
                swagger_info = self.swagger_handler.find_api_info_in_swagger(swagger_doc, url_pattern, method)

            # 使用URLMatcher生成的函数名
            function_name = parsed_info["function_name"]
        else:
            parsed_info = self._parse_request_info(request_info)
            # 保留 swagger_handler 中提取的路径参数
            if "path_params" in request_info and request_info["path_params"]:
                parsed_info["path_params"] = request_info["path_params"]
            function_name = parsed_info["function_name"]
            url_pattern = parsed_info.get("url_pattern", url)

        # 检查文件是否存在
        if self.check_api_exists(url_pattern, service_package):
            if not force_overwrite:
                logger.info(f"接口已存在，跳过生成: {method} {url_pattern}")
                return None
            else:
                logger.info(f"接口已存在，强制覆盖: {method} {url_pattern}")

        # 生成文件路径
        filename = f"{function_name}.py"
        if service_package == "apis":
            filepath = os.path.join(self.output_dir, filename)
        else:
            filepath = os.path.join(self.output_dir, service_package, filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # 生成文件内容（使用从Swagger获取的数据）
        content = self.generate_file_content(request_info, function_name, swagger_info, parsed_info)
        write_test_file(filepath, content)

        return filepath

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

        # 直接使用 Swagger 的 parameters 字典（包含 dotted key 如 "payDTO.accountName"），
        # format_params_for_python 会递归查找嵌套键的注释
        comments = swagger_info.get("parameters", {})
        return format_params_for_python(params_dict, format_parameter_value, comments, inline=False)

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
        is_multipart = parsed_info.get("is_multipart", False)
        is_need_urlencode = parsed_info["is_need_urlencode"]

        imports.append("import os")
        if is_file_upload or is_multipart:
            imports.append("from requests_toolbelt import MultipartEncoder")

        if is_need_urlencode:
            imports.append("from urllib.parse import urlencode")

        imports.append("from util.client import client")
        imports.append("")
        return imports

    def _determine_param_info(self, parsed_info: dict[str, Any]) -> tuple[str | None, dict | None]:
        """根据解析后的请求信息确定参数名和参数数据，用于 _process_parameters 和 _generate_function_definition 共用。"""
        method = parsed_info["method"]
        path_params = parsed_info["path_params"]
        query_params = parsed_info["query_params"]
        post_data = parsed_info["post_data"]
        is_file_upload = parsed_info["is_file_upload"]
        is_multipart = parsed_info.get("is_multipart", False)
        is_need_urlencode = parsed_info["is_need_urlencode"]

        if method == "GET" and query_params:
            return "params", query_params
        elif path_params:
            return "params", path_params
        elif method == "POST":
            if is_need_urlencode and query_params:
                return "data", query_params
            elif post_data:
                if is_file_upload:
                    return "files", post_data
                else:
                    return "data", post_data
        return None, None

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

        headers = parsed_info["headers"]
        is_need_urlencode = parsed_info["is_need_urlencode"]

        param_name, param_data = self._determine_param_info(parsed_info)

        if param_name and param_data:
            formatted_params = self._generate_params_string(param_data, swagger_info)
            params_section.append(f"{param_name} = {formatted_params}")
            params_section.append("")

        # 添加 headers 参数定义
        formatted_headers = format_headers_for_python(headers)
        if is_need_urlencode:
            urlencode_headers = headers.copy()
            urlencode_headers["content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            formatted_urlencode_headers = format_headers_for_python(urlencode_headers)
            params_section.append(f"headers = {formatted_urlencode_headers}")
        else:
            params_section.append(f"headers = {formatted_headers}")

        return params_section

    def _handle_file_upload(self, post_data: Any) -> list[str]:
        """
        处理文件上传

        生成文件上传的代码实现，动态识别文件参数名

        Args:
            post_data: POST数据

        Returns:
            List[str]: 文件上传代码列表
        """
        if not isinstance(post_data, dict):
            raise ValueError("文件上传参数格式错误")

        # 动态识别文件参数名（值为 (binary) 或以 @ 开头的 key）
        file_key = None
        for key, value in post_data.items():
            if isinstance(value, str) and (value == "(binary)" or value.startswith("@")):
                file_key = key
                break

        if file_key is None:
            raise ValueError("文件上传参数格式错误：未找到文件参数")

        function_def = []
        function_def.append(f'    with open(files["{file_key}"], "rb") as f:')
        function_def.append(f'        filename = os.path.basename(files["{file_key}"])')
        function_def.append("        m = MultipartEncoder(")
        function_def.append("            fields={")
        for key, value in post_data.items():
            if key == file_key:
                function_def.append(f'                "{file_key}": (filename, f, "text/plain")')
            else:
                function_def.append(f'                "{key}": files["{key}"],')
        function_def.append("            }")
        function_def.append("        )")
        function_def.append('        headers["content-type"] = m.content_type')
        function_def.append("        with client.post(url=url, headers=headers, data=m) as r:")
        function_def.append("            return r")
        return function_def

    def _handle_multipart_form(self) -> list[str]:
        """
        处理 multipart/form-data 请求（无文件上传）

        生成 MultipartEncoder 编码的代码实现

        Returns:
            List[str]: multipart 表单代码列表
        """
        function_def = []
        function_def.append("    # 构建 multipart/form-data 请求")
        function_def.append("    m = MultipartEncoder(fields=data)")
        function_def.append("")
        function_def.append("    # 设置正确的 Content-Type（包含 boundary）")
        function_def.append('    headers["content-type"] = m.content_type')
        function_def.append("    with client.post(url=url, data=m, headers=headers) as r:")
        function_def.append("        return r")
        return function_def

    def _handle_http_method(
        self,
        method: str,
        has_data: bool,
        path_params: dict[str, Any],
        query_params: dict[str, Any],
        is_need_urlencode: bool,
        is_json_content: bool = False,
    ) -> list[str]:
        """
        处理HTTP方法

        生成不同HTTP方法的代码实现

        Args:
            method: HTTP方法
            has_data: 是否有请求体数据
            path_params: 路径参数
            query_params: 查询参数
            is_need_urlencode: 是否需要urlencode
            is_json_content: 是否为JSON请求

        Returns:
            List[str]: HTTP方法代码列表
        """
        function_def = []

        if method == "GET":
            if query_params:
                function_def.append("    with client.get(url=url, params=params, headers=headers) as r:")
            else:
                function_def.append("    with client.get(url=url, headers=headers) as r:")
        elif method == "POST":
            if path_params:
                function_def.append("    with client.post(url=url, headers=headers) as r:")
            elif has_data:
                if is_need_urlencode:
                    function_def.append(
                        "    data = urlencode(data) # application/x-www-form-urlencoded传参需要特殊处理"
                    )
                    function_def.append("")
                    function_def.append("    with client.post(url=url, data=data, headers=headers) as r:")
                elif is_json_content:
                    function_def.append("    with client.post(url=url, json=data, headers=headers) as r:")
                else:
                    function_def.append("    with client.post(url=url, data=data, headers=headers) as r:")
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
        is_multipart = parsed_info.get("is_multipart", False)
        is_need_urlencode = parsed_info["is_need_urlencode"]
        is_json_content = parsed_info.get("is_json_content", False)
        path_params = parsed_info["path_params"]
        url_pattern = parsed_info["url_pattern"]

        param_name, _ = self._determine_param_info(parsed_info)

        func_params = []
        if param_name:
            func_params.append(f"{param_name}={param_name}")
        func_params.append("headers=headers")

        function_def.append(f"def {function_name}({', '.join(func_params)}):")
        function_def.append('    """')

        # 使用Swagger文档中的描述信息(接口名称，url模板，参数说明)
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
        elif is_multipart:
            multipart_code = self._handle_multipart_form()
            function_def.extend(multipart_code)
        else:
            http_method_code = self._handle_http_method(
                method, param_name is not None, path_params, query_params, is_need_urlencode, is_json_content
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
            else:
                # 根目录下的文件，服务包就是 apis
                service_package = "apis"
            if service_package not in service_packages:
                service_packages[service_package] = []
            service_packages[service_package].append(filepath)

        # 为每个服务包生成索引文件
        for service_package, files in service_packages.items():
            if service_package == "apis":
                # 根目录下的文件，直接使用 output_dir 作为包目录
                package_dir = self.output_dir
            else:
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

                # 检查是否已存在该模块的导入（通过模块名匹配，避免多行导入和空格差异导致重复）
                already_imported = any(f"from .{last_part} import" in line for line in content)
                if not already_imported:
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
