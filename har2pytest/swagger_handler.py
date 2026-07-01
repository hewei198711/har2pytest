"""Swagger 文档处理器模块。

提供从 Swagger/OpenAPI 文档中获取 API 信息、提取参数等功能。
"""

import asyncio
import time
from typing import TYPE_CHECKING, Any, Optional

import httpx

from .config import APIConfig
from .logger import logger
from .url_matcher import URLMatcher
from .utils import format_directory as _format_directory

# 仅在类型检查时导入，运行时不会执行
if TYPE_CHECKING:
    from .api_generator import APIGenerator


class SwaggerHandler:
    """Swagger 文档处理器类。

    用于获取和解析 Swagger/OpenAPI 文档，提取 API 信息和参数。
    """

    def __init__(self, api_generator: Optional["APIGenerator"] = None):
        """初始化 Swagger 文档处理器。

        Args:
            api_generator: API 生成器实例（可选）。
        """
        self.swagger_cache: dict[str, dict[str, Any]] = {}
        self.api_generator: APIGenerator | None = api_generator  # API生成器实例

    async def _send_request(self, url: str) -> Any | None:
        """异步发送 HTTP 请求并返回响应数据。

        Args:
            url: 请求的 URL。

        Returns:
            Any | None: 响应的 JSON 数据，如果请求失败则返回 None。
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _clean_swagger_url(url: str) -> str:
        """清洗 Swagger URL，移除 doc.html、#fragment 等 UI 页面后缀。

        用户可能从浏览器复制了 Swagger UI 页面地址（如 doc.html#），
        需要清理为实际的 API 文档基础 URL。

        Args:
            url: 用户输入的原始 URL。

        Returns:
            str: 清洗后的基础 URL。
        """
        # 1. 移除 URL fragment（# 及其后面的部分）
        url = url.split("#")[0]
        # 2. 移除 doc.html、index.html、swagger-ui.html 后缀
        suffixes = ["doc.html", "index.html", "swagger-ui.html"]
        for suffix in suffixes:
            if url.endswith(suffix):
                url = url[: -len(suffix)]
                break
        # 3. 移除末尾的 /
        url = url.rstrip("/")
        return url

    async def get_swagger_doc(self, service_base_url: str) -> dict[str, Any] | None:
        """异步获取 Swagger API 文档数据。

        首先尝试通过 swagger-resources 获取文档路径，失败后回退到常见路径。
        结果会被缓存以提高性能。

        Args:
            service_base_url: 服务基础 URL。

        Returns:
            dict[str, Any] | None: Swagger 文档数据，如果获取失败则返回 None。
        """
        # 清洗 URL：移除 doc.html、#fragment 等 UI 页面后缀
        service_base_url = self._clean_swagger_url(service_base_url)

        if service_base_url in self.swagger_cache:
            return self.swagger_cache[service_base_url]

        # 首先尝试通过 swagger-resources 获取真实的文档路径
        swagger_resource_path = "/swagger-resources"
        try:
            logger.info(f"正在获取Swagger资源: {service_base_url}{swagger_resource_path}")

            resources = await self._send_request(f"{service_base_url}{swagger_resource_path}")
            if resources:
                for resource in resources:
                    doc_path = resource.get("location") or resource.get("url")
                    if doc_path:
                        if doc_path.startswith("http"):
                            doc_url = doc_path
                        else:
                            doc_url = f"{service_base_url}{doc_path}"

                        logger.info(f"✓ 从swagger-resources获取文档路径: {doc_url}")

                        data = await self._send_request(doc_url)
                        if data and "paths" in data:
                            self.swagger_cache[service_base_url] = data
                            logger.info(f"✓ 成功获取 {len(data['paths'])} 个API路径 (使用 swagger-resources)")
                            return data
        except Exception as e:
            logger.debug(f"获取swagger-resources失败: {str(e)}")

        doc_paths = ["/v3/api-docs", "/v2/api-docs", "/api-docs"]

        for doc_path in doc_paths:
            try:
                logger.info(f"正在获取Swagger文档: {service_base_url}{doc_path}")

                data = await self._send_request(f"{service_base_url}{doc_path}")
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
        """在 Swagger 文档中查找特定 API 的信息。

        Args:
            swagger_data: Swagger 文档数据。
            api_path: API 路径。
            method: HTTP 方法（默认 GET）。

        Returns:
            dict[str, Any]: 包含 description、parameters、summary 的字典。
        """
        api_info = {"description": "", "parameters": {}, "summary": ""}

        if not swagger_data or "paths" not in swagger_data:
            return api_info

        paths = swagger_data["paths"]

        path_data = None

        # 1. 获取Swagger文档的basePath并处理
        base_path = swagger_data.get("basePath", "")
        search_path = URLMatcher.remove_base_path(api_path, base_path)

        # 2. 尝试匹配处理后的路径
        if search_path in paths:
            path_data = paths[search_path]
            logger.debug(f"使用处理后的路径匹配: {search_path}")

        if not path_data:
            logger.info(f"未找到路径: {api_path}")
            return api_info

        method_lower = method.lower()
        if method_lower in path_data:
            method_data = path_data[method_lower]

            api_info["summary"] = method_data.get("summary", "")
            api_info["description"] = method_data.get("description", "") or method_data.get("summary", "")

            parameters = method_data.get("parameters", [])
            for param in parameters:
                param_name = param.get("name", "")
                param_desc = param.get("description", "")
                param_in = param.get("in", "")

                if param_in != "body":
                    # query/path 参数：直接添加描述
                    if param_name and param_desc:
                        api_info["parameters"][param_name] = param_desc
                elif "schema" in param:
                    # body 参数：统一使用递归提取嵌套描述（支持 $ref 和 properties）
                    self._extract_nested_descriptions(
                        param["schema"], swagger_data, api_info["parameters"]
                    )


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
                # 递归提取body参数的嵌套描述
                schema = param["schema"]
                self._extract_nested_descriptions(schema, swagger_data, param_descriptions)
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
        从body参数schema中提取参数（递归处理嵌套结构）

        处理模型引用和内联模型，递归处理嵌套对象

        Args:
            schema: 参数的schema定义
            swagger_data: 完整的Swagger文档数据

        Returns:
            Dict[str, Any]: 提取的参数字典（包含嵌套结构）
        """
        body_params = {}

        if "$ref" in schema:
            ref = schema["$ref"]
            ref_name = ref.split("/")[-1]
            if "definitions" in swagger_data and ref_name in swagger_data["definitions"]:
                definition = swagger_data["definitions"][ref_name]
                if "properties" in definition:
                    for prop_name, prop_info in definition["properties"].items():
                        body_params[prop_name] = self._extract_param_value(prop_info, swagger_data)
        elif "properties" in schema:
            for prop_name, prop_info in schema["properties"].items():
                body_params[prop_name] = self._extract_param_value(prop_info, swagger_data)

        return body_params

    def _extract_param_value(self, prop_info: dict[str, Any], swagger_data: dict[str, Any]) -> Any:
        """
        递归提取参数值，处理嵌套对象和数组

        Args:
            prop_info: 属性信息
            swagger_data: 完整的Swagger文档数据

        Returns:
            Any: 参数值（可能是基本类型、对象或数组）
        """
        prop_type = prop_info.get("type", "string")

        # 如果有 $ref，优先处理引用
        if "$ref" in prop_info:
            ref = prop_info["$ref"]
            ref_name = ref.split("/")[-1]
            if "definitions" in swagger_data and ref_name in swagger_data["definitions"]:
                definition = swagger_data["definitions"][ref_name]
                if "properties" in definition:
                    result = {}
                    for nested_name, nested_info in definition["properties"].items():
                        result[nested_name] = self._extract_param_value(nested_info, swagger_data)
                    return result

        if prop_type == "object":
            if "properties" in prop_info:
                result = {}
                for nested_name, nested_info in prop_info["properties"].items():
                    result[nested_name] = self._extract_param_value(nested_info, swagger_data)
                return result
            return {}
        elif prop_type == "array":
            items = prop_info.get("items", {})
            if "$ref" in items:
                ref = items["$ref"]
                ref_name = ref.split("/")[-1]
                if "definitions" in swagger_data and ref_name in swagger_data["definitions"]:
                    definition = swagger_data["definitions"][ref_name]
                    if "properties" in definition:
                        result = {}
                        for nested_name, nested_info in definition["properties"].items():
                            result[nested_name] = self._extract_param_value(nested_info, swagger_data)
                        return [result]
            elif "properties" in items:
                result = {}
                for nested_name, nested_info in items["properties"].items():
                    result[nested_name] = self._extract_param_value(nested_info, swagger_data)
                return [result]
            return []
        else:
            return self._get_default_value(prop_type)

    def _extract_nested_descriptions(
        self, schema: dict[str, Any], swagger_data: dict[str, Any], descriptions: dict[str, str], parent_key: str = ""
    ) -> None:
        """
        递归提取嵌套参数的描述信息

        Args:
            schema: 参数的schema定义
            swagger_data: 完整的Swagger文档数据
            descriptions: 存储描述信息的字典
            parent_key: 父级参数名（用于嵌套参数）
        """
        if "$ref" in schema:
            ref = schema["$ref"]
            ref_name = ref.split("/")[-1]
            if "definitions" in swagger_data and ref_name in swagger_data["definitions"]:
                definition = swagger_data["definitions"][ref_name]
                if "properties" in definition:
                    for prop_name, prop_info in definition["properties"].items():
                        full_key = f"{parent_key}.{prop_name}" if parent_key else prop_name
                        prop_desc = prop_info.get("description", "")
                        if prop_name and prop_desc:
                            descriptions[full_key] = prop_desc
                        # 递归处理嵌套对象
                        if prop_info.get("type") == "object" or "$ref" in prop_info:
                            self._extract_nested_descriptions(prop_info, swagger_data, descriptions, full_key)
                        elif prop_info.get("type") == "array":
                            items = prop_info.get("items", {})
                            self._extract_nested_descriptions(items, swagger_data, descriptions, full_key)
        elif "properties" in schema:
            for prop_name, prop_info in schema["properties"].items():
                full_key = f"{parent_key}.{prop_name}" if parent_key else prop_name
                prop_desc = prop_info.get("description", "")
                if prop_name and prop_desc:
                    descriptions[full_key] = prop_desc
                # 递归处理嵌套对象
                if prop_info.get("type") == "object" or "$ref" in prop_info:
                    self._extract_nested_descriptions(prop_info, swagger_data, descriptions, full_key)
                elif prop_info.get("type") == "array":
                    items = prop_info.get("items", {})
                    self._extract_nested_descriptions(items, swagger_data, descriptions, full_key)

    async def generate_apis_from_swagger(
        self, swagger_url: str, force_overwrite: bool = False, specific_path: str = None
    ) -> list[str]:
        """
        从Swagger文档异步批量生成API文件

        解析Swagger文档，获取所有API路径和方法，为每个API生成对应的API文件

        Args:
            swagger_url: Swagger文档URL
            force_overwrite: 是否覆盖已存在的文件
            specific_path: 只生成指定的API路径，默认为None（生成所有路径）

        Returns:
            List[str]: 生成的文件路径列表
        """

        generated_files: list[str] = []

        try:
            # 异步获取Swagger文档
            swagger_data = await self.get_swagger_doc(swagger_url)
            if not swagger_data:
                logger.error(f"无法获取Swagger文档: {swagger_url}")
                return generated_files

            # 设置 swagger_data 到 url_matcher，确保后续 URL 匹配能正确提取路径参数
            if self.api_generator:
                self.api_generator.url_matcher.swagger_data = swagger_data

            # 获取Swagger文档的basePath
            base_path = swagger_data.get("basePath", "")

            # 遍历所有API路径
            paths = swagger_data.get("paths", {})
            logger.info(f"从Swagger文档中发现 {len(paths)} 个API路径")

            # 如果指定了特定路径，直接查找而不是遍历
            paths_to_process = list(paths.items())
            if specific_path:
                # 从specific_path中移除base_path前缀
                search_path = specific_path
                if base_path and base_path != "/":
                    if search_path.startswith(base_path):
                        search_path = search_path[len(base_path) :]
                        if not search_path.startswith("/"):
                            search_path = "/" + search_path

                # 直接在paths中查找
                if search_path in paths:
                    paths_to_process = [(search_path, paths[search_path])]
                else:
                    logger.warning(f"指定的路径 {specific_path} 在Swagger文档中未找到")
                    return generated_files

            # 定义异步任务函数：处理单个 API
            async def process_api(path: str, method: str, method_data: dict) -> str | None:
                """处理单个API路径和方法的文件生成。"""
                task_start = time.time()
                try:
                    # 构建完整的URL路径，包含basePath
                    full_path = path
                    if base_path and base_path != "/":
                        full_path = base_path.rstrip("/") + "/" + path.lstrip("/")

                    logger.debug(f"  [任务开始] {method.upper()} {full_path}")

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
                    (
                        query_params, post_data, has_query_param, has_body_param, path_params, param_descriptions,
                    ) = self._extract_params_from_swagger(parameters, swagger_data)

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
                        filepath = await self.api_generator.generate_api_file(request_info, force_overwrite, swagger_info)
                        elapsed = time.time() - task_start
                        if filepath:
                            logger.debug(f"  [任务完成] {method.upper()} {full_path} → {filepath} (耗时 {elapsed:.2f}s)")
                        else:
                            logger.debug(f"  [任务跳过] {method.upper()} {full_path} (耗时 {elapsed:.2f}s)")
                        return filepath
                    return None
                except Exception as e:
                    elapsed = time.time() - task_start
                    logger.error(f"  [任务失败] {method.upper()} {path} (耗时 {elapsed:.2f}s): {str(e)}")
                    return None

            # 创建所有异步任务
            logger.info(f"[并行处理] 创建 {len(paths_to_process)} 个路径的任务...")
            tasks = []
            task_count = 0
            for path, methods in paths_to_process:
                for method, method_data in methods.items():
                    tasks.append(process_api(path, method, method_data))
                    task_count += 1
            logger.info(f"[并行处理] 共创建 {task_count} 个任务，开始并行执行...")

            # 并行执行任务，swagger_data 已统一设置，各任务只读不写，无竞态条件
            parallel_start = time.time()
            success_count = 0
            completed_count = 0
            for coro in asyncio.as_completed(tasks):
                try:
                    filepath = await coro
                    if filepath:
                        generated_files.append(filepath)
                        success_count += 1
                        logger.info(f"✓ 生成API文件: {filepath}")
                    else:
                        logger.info("- 跳过已存在的API文件")
                except Exception as e:
                    logger.error(f"❌ 生成API文件失败: {str(e)}")
                completed_count += 1
                if completed_count % 10 == 0 or completed_count == task_count:
                    logger.debug(f"  [并行进度] {completed_count}/{task_count} 已完成")
            parallel_elapsed = time.time() - parallel_start

            logger.info("\n============================================")
            logger.info(f"从Swagger文档生成完成: 成功 {success_count} 个, 总耗时 {parallel_elapsed:.2f}s")
            logger.info("============================================")

            # 批量格式化生成的 API 文件
            if generated_files and self.api_generator:
                await _format_directory(self.api_generator.output_dir)

        except Exception as e:
            logger.error(f"❌ 从Swagger文档生成API文件失败: {str(e)}")

        return generated_files
