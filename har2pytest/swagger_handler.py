import json
import urllib.request
from typing import TYPE_CHECKING, Any, Optional

from .config import APIConfig
from .logger import logger
from .utils import handle_base_path

# 仅在类型检查时导入，运行时不会执行
if TYPE_CHECKING:
    from .api_generator import APIGenerator


class SwaggerHandler:
    """Swagger文档处理器类"""

    def __init__(self, api_generator: Optional["APIGenerator"] = None):
        """
        初始化Swagger文档处理器

        Args:
            api_generator: API生成器实例
        """
        self.swagger_cache: dict[str, dict[str, Any]] = {}
        self.api_generator: APIGenerator | None = api_generator  # API生成器实例

    def _send_request(self, url: str) -> Any | None:
        """
        发送HTTP请求并返回响应数据
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode("utf-8")
            return json.loads(content)

    def get_swagger_doc(self, service_base_url: str) -> dict[str, Any] | None:
        """
        获取Swagger API文档数据
        """
        if service_base_url in self.swagger_cache:
            return self.swagger_cache[service_base_url]

        # 首先尝试通过 swagger-resources 获取真实的文档路径
        swagger_resource_path = "/swagger-resources"
        try:
            logger.info(f"正在获取Swagger资源: {service_base_url}{swagger_resource_path}")

            # 发送请求获取 swagger-resources
            resources = self._send_request(f"{service_base_url}{swagger_resource_path}")
            if resources:
                # 查找所有 Swagger 文档资源
                for resource in resources:
                    doc_path = resource.get("location") or resource.get("url")
                    if doc_path:
                        # 构建完整的文档 URL
                        if doc_path.startswith("http"):
                            doc_url = doc_path
                        else:
                            doc_url = f"{service_base_url}{doc_path}"

                        logger.info(f"✓ 从swagger-resources获取文档路径: {doc_url}")

                        # 访问文档
                        data = self._send_request(doc_url)
                        if data and "paths" in data:
                            self.swagger_cache[service_base_url] = data
                            logger.info(f"✓ 成功获取 {len(data['paths'])} 个API路径 (使用 swagger-resources)")
                            return data
        except Exception as e:
            logger.debug(f"获取swagger-resources失败: {str(e)}")

        # 如果swagger-resources失败，回退到遍历常见路径
        doc_paths = [
            "/v3/api-docs",
            "/v2/api-docs",
            "/api-docs",
        ]

        for doc_path in doc_paths:
            try:
                logger.info(f"正在获取Swagger文档: {service_base_url}{doc_path}")

                # 发送请求获取文档
                data = self._send_request(f"{service_base_url}{doc_path}")
                if data and "paths" in data:
                    self.swagger_cache[service_base_url] = data
                    logger.info(f"✓ 成功获取 {len(data['paths'])} 个API路径 (使用 {doc_path})")
                    return data
                else:
                    logger.warning("❌ 文档格式不正确，缺少paths字段")
                    continue

            except Exception as e:
                logger.error(f"❌ 获取Swagger文档失败 {service_base_url}{doc_path}: {str(e)}")
                continue

        logger.error(f"❌ 尝试所有路径后仍然无法获取文档: {service_base_url}")
        return None

    def find_api_info_in_swagger(
        self, swagger_data: dict[str, Any], api_path: str, method: str = "GET"
    ) -> dict[str, Any]:
        """
        在Swagger文档中查找特定API的信息
        """
        api_info = {"description": "", "parameters": {}, "summary": ""}

        if not swagger_data or "paths" not in swagger_data:
            return api_info

        paths = swagger_data["paths"]

        path_data = None

        # 1. 获取Swagger文档的basePath并处理
        base_path = swagger_data.get("basePath", "")
        search_path = handle_base_path(api_path, base_path)

        # 2. 尝试匹配处理后的路径
        if search_path in paths:
            path_data = paths[search_path]
            logger.debug(f"使用处理后的路径匹配: {search_path}")

        if not path_data:
            logger.info(f"未找到路径: {api_path}")
            return api_info

        method_lower = method.lower()

        # 提高匹配的容错性，先精准匹配method_lower，再尝试get, post, put, delete
        for http_method in [method_lower, "get", "post", "put", "delete"]:
            if http_method in path_data:
                method_data = path_data[http_method]

                api_info["summary"] = method_data.get("summary", "")
                api_info["description"] = method_data.get("description", "") or method_data.get("summary", "")

                parameters = method_data.get("parameters", [])
                for param in parameters:
                    param_name = param.get("name", "")
                    param_desc = param.get("description", "")

                    # 对于所有参数，只要有名称和描述，就添加到参数列表中
                    # 包括 GET 请求的 body 参数（通常作为查询参数传递）
                    if param_name and param_desc:
                        api_info["parameters"][param_name] = param_desc

                    if "schema" in param and "$ref" in param["schema"]:
                        ref = param["schema"]["$ref"]
                        ref_name = ref.split("/")[-1]
                        if "definitions" in swagger_data and ref_name in swagger_data["definitions"]:
                            definition = swagger_data["definitions"][ref_name]
                            if "properties" in definition:
                                for prop_name, prop_info in definition["properties"].items():
                                    prop_desc = prop_info.get("description", "")
                                    if prop_desc:
                                        api_info["parameters"][prop_name] = prop_desc

                if api_info["summary"] or api_info["description"] or api_info["parameters"]:
                    break

        return api_info

    def _extract_params_from_swagger(self, parameters: list[dict[str, Any]], swagger_data: dict[str, Any]) -> tuple:
        """
        从Swagger文档提取参数

        处理查询参数、请求体参数和路径参数，提取默认值和参数描述信息

        Args:
            parameters: Swagger文档中的参数列表
            swagger_data: 完整的Swagger文档数据

        Returns:
            tuple: (query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions)
        """
        query_params = {}
        post_data = {}
        path_params = {}  # 路径参数，通过这个就可以判断是否路径url中包含动态参数
        param_descriptions = {}  # 参数描述信息
        has_query_param = False
        has_body_param = False

        for param in parameters:
            param_name = param.get("name")
            param_in = param.get("in")
            param_type = param.get("type", "string")
            param_desc = param.get("description", "")

            if param_in == "query":
                has_query_param = True
                query_params[param_name] = self._get_default_value(param_type)
                if param_desc:
                    param_descriptions[param_name] = param_desc
            elif param_in == "body" and "schema" in param:
                has_body_param = True
                post_data = self._extract_body_params(param["schema"], swagger_data)
                # 提取body参数的嵌套描述
                schema = param["schema"]
                if "$ref" in schema:
                    ref = schema["$ref"]
                    ref_name = ref.split("/")[-1]
                    if "definitions" in swagger_data and ref_name in swagger_data["definitions"]:
                        definition = swagger_data["definitions"][ref_name]
                        if "properties" in definition:
                            for prop_name, prop_info in definition["properties"].items():
                                prop_desc = prop_info.get("description", "")
                                if prop_name and prop_desc:
                                    param_descriptions[prop_name] = prop_desc
                elif "properties" in schema:
                    for prop_name, prop_info in schema["properties"].items():
                        prop_desc = prop_info.get("description", "")
                        if prop_name and prop_desc:
                            param_descriptions[prop_name] = prop_desc
            elif param_in == "path":
                # 处理路径参数
                path_params[param_name] = self._get_default_value(param_type)
                if param_desc:
                    param_descriptions[param_name] = param_desc

        return query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions

    def _get_default_value(self, param_type: str) -> Any:
        """
        根据参数类型获取默认值

        Args:
            param_type: 参数类型

        Returns:
            Any: 默认值
        """
        if param_type in ("string",):
            return ""
        elif param_type in ("integer", "int"):
            return 0
        elif param_type in ("number", "float"):
            return 0.0
        elif param_type == "boolean":
            return False
        elif param_type == "array":
            return []
        elif param_type == "object":
            return {}
        return ""

    def _extract_body_params(self, schema: dict[str, Any], swagger_data: dict[str, Any]) -> dict[str, Any]:
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

    def generate_apis_from_swagger(
        self, swagger_url: str, force_overwrite: bool = False, specific_path: str = None
    ) -> list[str]:
        """
        从Swagger文档生成API文件

        解析Swagger文档，获取所有API路径和方法，为每个API生成对应的API文件

        Args:
            swagger_url: Swagger文档URL
            force_overwrite: 是否覆盖已存在的文件
            specific_path: 只生成指定的API路径，默认为None（生成所有路径）

        Returns:
            List[str]: 生成的文件路径列表
        """

        generated_files = []

        try:
            # 获取Swagger文档
            swagger_data = self.get_swagger_doc(swagger_url)
            if not swagger_data:
                logger.error(f"无法获取Swagger文档: {swagger_url}")
                return generated_files

            # 遍历所有API路径
            paths = swagger_data.get("paths", {})
            logger.info(f"从Swagger文档中发现 {len(paths)} 个API路径")

            # 获取Swagger文档的basePath
            base_path = swagger_data.get("basePath", "")

            for path, methods in paths.items():
                # 构建完整的URL路径，包含basePath
                full_path = path
                if base_path and base_path != "/":
                    # 拼接路径，避免产生双斜杠
                    full_path = base_path.rstrip("/") + "/" + path.lstrip("/")

                # 如果指定了特定路径，只处理匹配的路径
                if specific_path and full_path != specific_path:
                    continue

                # 遍历支持的HTTP方法
                for method, method_data in methods.items():
                    try:
                        # 构建请求信息
                        request_info = {
                            "method": method.upper(),
                            "url": full_path,
                            "query_params": {},
                            "post_data": {},
                            "headers": APIConfig.REQUIRED_HEADERS(),
                        }

                        # 提取参数
                        parameters = method_data.get("parameters", [])
                        query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions = (
                            self._extract_params_from_swagger(parameters, swagger_data)
                        )

                        request_info["query_params"] = query_params
                        request_info["post_data"] = post_data
                        request_info["path_params"] = path_params

                        # 提取API信息（包括描述和参数说明）
                        swagger_info = {
                            "summary": method_data.get("summary", ""),
                            "description": method_data.get("description", "") or method_data.get("summary", ""),
                            "parameters": param_descriptions,
                        }

                        # 判断是否需要urlencode
                        if method.upper() == "POST" and has_query_param and not post_data and not has_body_param:
                            request_info["headers"]["content-length"] = "0"

                        # 生成API文件
                        if self.api_generator:
                            filepath = self.api_generator.generate_api_file(request_info, force_overwrite, swagger_info)
                            if filepath:
                                generated_files.append(filepath)
                                logger.info(f"✓ 生成API文件: {filepath}")
                            else:
                                logger.info(f"- 跳过已存在的API文件: {path}")

                    except Exception as e:
                        logger.error(f"❌ 生成API文件失败 {path} {method}: {str(e)}")

            logger.info("\n============================================")
            logger.info("从Swagger文档生成完成:")
            logger.info(f"✓ 成功生成: {len(generated_files)} 个API文件")
            logger.info("============================================")

        except Exception as e:
            logger.error(f"❌ 从Swagger文档生成API文件失败: {str(e)}")

        return generated_files
