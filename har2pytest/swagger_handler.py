"""Swagger 文档处理器模块。

提供从 Swagger/OpenAPI 文档中获取 API 信息、提取参数等功能。
"""

from typing import Any

import aiohttp

from .logger import logger
from .models import SwaggerInfo
from .url_matcher import URLMatcher
from .utils import sanitize_remark


class SwaggerHandler:
    """Swagger 文档处理器类。

    用于获取和解析 Swagger/OpenAPI 文档，提取 API 信息和参数。
    """

    _HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }

    def __init__(self):
        """初始化 Swagger 文档处理器。"""
        self.swagger_cache: dict[str, dict[str, Any]] = {}
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建复用的 aiohttp 会话（懒初始化，连接池自动管理）。"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers=self._HEADERS,
            )
        return self._session

    async def close(self) -> None:
        """关闭内部 aiohttp 会话，释放连接池资源。"""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _send_request(self, url: str) -> Any | None:
        """异步发送 HTTP 请求并返回响应数据。

        Args:
            url: 请求的 URL。

        Returns:
            Any | None: 响应的 JSON 数据，如果请求失败则返回 None。
        """
        session = await self._get_session()
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

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
        Knife4j/springfox 常按分组暴露多份文档（如 ``/v2/api-docs?group=ApiV_1``），
        此时会遍历**所有分组并合并** paths/definitions/tags，避免只拿到第一个分组。
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
                merged = await self._merge_group_docs(service_base_url, resources)
                if merged is not None and "paths" in merged:
                    self.swagger_cache[service_base_url] = merged
                    return merged
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

    async def _merge_group_docs(self, service_base_url: str, resources: Any) -> dict[str, Any] | None:
        """遍历 swagger-resources 的所有分组，合并为一份文档。

        合并规则（以先出现的分组为准，避免后续聚合分组覆盖已有定义）：
        - ``paths``：按路径合并，同路径下不同 method 合并；同一 ``path+method`` 只保留首次出现；
        - ``definitions``/``tags``：取并集，重名保留首次出现的定义（保证 ``$ref`` 可解析）；
        - 其余顶层字段（swagger/info/host/basePath 等）取首个成功获取的分组。

        Args:
            service_base_url: 服务基础 URL（用于拼接相对 location）。
            resources: ``swagger-resources`` 返回的分组列表。

        Returns:
            dict[str, Any] | None: 合并后的文档；没有任何可用分组时返回 None。
        """
        if not isinstance(resources, list):
            return None

        merged: dict[str, Any] = {}
        group_count = 0
        skipped_ops = 0
        failed_groups = 0

        for resource in resources:
            if not isinstance(resource, dict):
                continue
            doc_path = resource.get("location") or resource.get("url")
            if not doc_path:
                continue
            doc_url = doc_path if str(doc_path).startswith("http") else f"{service_base_url}{doc_path}"
            try:
                data = await self._send_request(doc_url)
            except Exception as e:
                # 单个分组文档失败不应中断其余分组
                failed_groups += 1
                logger.debug(f"获取swagger-resources分组文档失败 {doc_url}: {str(e)}")
                continue
            if not data or "paths" not in data:
                continue

            group_count += 1
            if not merged:
                merged = {key: value for key, value in data.items() if key not in ("paths", "definitions", "tags")}
                merged["paths"] = {}
                merged["definitions"] = {}
                merged["tags"] = []

            for tag in data.get("tags") or []:
                if tag not in merged["tags"]:
                    merged["tags"].append(tag)

            for name, definition in (data.get("definitions") or {}).items():
                merged["definitions"].setdefault(name, definition)

            for path, methods in (data.get("paths") or {}).items():
                if not isinstance(methods, dict):
                    continue
                target = merged["paths"].setdefault(path, {})
                for method, operation in methods.items():
                    if method in target:
                        skipped_ops += 1
                        continue
                    target[method] = operation

        if not merged:
            return None

        # 没有分组的 tags 时不留空键，保持与单分组文档一致的形状
        if not merged["tags"]:
            merged.pop("tags")
        if not merged["definitions"]:
            merged.pop("definitions")

        op_count = sum(
            1 for methods in merged["paths"].values() for m in methods if isinstance(methods.get(m), dict)
        )
        logger.info(
            f"✓ 成功合并 {group_count} 个分组: {len(merged['paths'])} 个API路径 / {op_count} 个操作 "
            f"(跳过重复操作 {skipped_ops} 个, 失败分组 {failed_groups} 个) (使用 swagger-resources)"
        )
        return merged

    def find_api_info_in_swagger(
        self, swagger_data: dict[str, Any], api_path: str, method: str = "GET"
    ) -> SwaggerInfo:
        """在 Swagger 文档中查找特定 API 的信息。

        Args:
            swagger_data: Swagger 文档数据。
            api_path: API 路径。
            method: HTTP 方法（默认 GET）。

        Returns:
            SwaggerInfo: 包含 description、parameters、summary 的 Swagger 信息对象。
        """
        api_info = SwaggerInfo()

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

            api_info.summary = method_data.get("summary", "")
            api_info.description = method_data.get("description", "") or method_data.get("summary", "")

            parameters = method_data.get("parameters", [])
            for param in parameters:
                param_name = param.get("name", "")
                # 描述统一压成单行：多行 description 会破坏生成的注释/docstring/allure 标题
                param_desc = sanitize_remark(param.get("description", ""))
                param_in = param.get("in", "")

                if param_in != "body":
                    # query/path 参数：直接添加描述
                    if param_name and param_desc:
                        api_info.parameters[param_name] = param_desc
                elif "schema" in param:
                    # body 参数：统一使用递归提取嵌套描述（支持 $ref 和 properties）
                    self._extract_nested_descriptions(param["schema"], swagger_data, api_info.parameters)

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
            param_desc = sanitize_remark(param.get("description", ""))

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

    def _resolve_schema_ref(self, ref: str, swagger_data: dict[str, Any]) -> dict[str, Any] | None:
        """把 ``$ref`` 解析为 schema dict。

        兼容 Swagger 2.0(``#/definitions/X``)与 OpenAPI 3(``#/components/schemas/X``):
        - 按 ref 的 JSON Pointer 路径在文档中逐段深入查找;
        - 也支持“模型.json#/definitions/X”这种带文件前缀的写法(去掉前缀);
        - 未找到时返回 None(与旧实现一致,调用方回退为空值)。
        """
        if not ref:
            return None
        pointer = ref.split("#", 1)[-1]
        parts = [p for p in pointer.split("/") if p]
        if parts:
            node: Any = swagger_data
            for part in parts:
                if isinstance(node, dict) and part in node:
                    node = node[part]
                else:
                    node = None
                    break
            if isinstance(node, dict):
                return node

        # 兜底:只给名字时按 definitions / components.schemas 顺序查找
        name = parts[-1] if parts else ref
        for section in ("definitions",):
            defs = swagger_data.get(section)
            if isinstance(defs, dict) and name in defs:
                return defs[name]
        components = swagger_data.get("components")
        schemas = components.get("schemas") if isinstance(components, dict) else None
        if isinstance(schemas, dict) and name in schemas:
            return schemas[name]
        return None

    def _extract_body_params(self, schema: dict[str, Any], swagger_data: dict[str, Any]) -> dict[str, Any] | list:
        """
        从body参数schema中提取参数（递归处理嵌套结构）

        处理模型引用和内联模型，递归处理嵌套对象；
        顶层数组请求体（type=array）返回单元素数组（其元素按对象展开）。

        Args:
            schema: 参数的schema定义
            swagger_data: 完整的Swagger文档数据

        Returns:
            Dict[str, Any] | list: 提取的参数字典（包含嵌套结构）或数组请求体
        """
        # 顶层数组 body（如批量操作 JSON 数组）
        if schema.get("type") == "array":
            items = schema.get("items", {})
            if "$ref" in items or "properties" in items:
                nested = self._extract_param_value(items, swagger_data)
                return nested if isinstance(nested, list) else [nested]
            return []
        body_params: dict[str, Any] = {}

        if "$ref" in schema:
            definition = self._resolve_schema_ref(schema["$ref"], swagger_data)
            if definition and "properties" in definition:
                for prop_name, prop_info in definition["properties"].items():
                    body_params[prop_name] = self._extract_param_value(prop_info, swagger_data)
        elif "properties" in schema:
            for prop_name, prop_info in schema["properties"].items():
                body_params[prop_name] = self._extract_param_value(prop_info, swagger_data)

        return body_params

    def _extract_param_value(self, prop_info: dict[str, Any], swagger_data: dict[str, Any], _seen: set[str] | None = None) -> Any:
        """
        递归提取参数值，处理嵌套对象和数组

        Args:
            prop_info: 属性信息
            swagger_data: 完整的Swagger文档数据
            _seen: 已解析的 $ref（内部递归防环用，自引用模型不会无限递归）

        Returns:
            Any: 参数值（可能是基本类型、对象或数组）
        """
        if _seen is None:
            _seen = set()
        prop_type = prop_info.get("type", "string")

        # 如果有 $ref，优先处理引用（防自引用环）
        if "$ref" in prop_info:
            ref = str(prop_info["$ref"])
            if ref in _seen:
                return {}
            definition = self._resolve_schema_ref(ref, swagger_data)
            if definition and "properties" in definition:
                _seen.add(ref)
                result = {}
                for nested_name, nested_info in definition["properties"].items():
                    result[nested_name] = self._extract_param_value(nested_info, swagger_data, _seen)
                _seen.discard(ref)
                return result

        if prop_type == "object":
            if "properties" in prop_info:
                result = {}
                for nested_name, nested_info in prop_info["properties"].items():
                    result[nested_name] = self._extract_param_value(nested_info, swagger_data, _seen)
                return result
            return {}
        elif prop_type == "array":
            items = prop_info.get("items", {})
            if "$ref" in items:
                ref = str(items["$ref"])
                if ref in _seen:
                    return []
                definition = self._resolve_schema_ref(ref, swagger_data)
                if definition and "properties" in definition:
                    _seen.add(ref)
                    result = {}
                    for nested_name, nested_info in definition["properties"].items():
                        result[nested_name] = self._extract_param_value(nested_info, swagger_data, _seen)
                    _seen.discard(ref)
                    return [result]
            elif "properties" in items:
                result = {}
                for nested_name, nested_info in items["properties"].items():
                    result[nested_name] = self._extract_param_value(nested_info, swagger_data, _seen)
                return [result]
            return []
        else:
            return self._get_default_value(prop_type)

    def _extract_nested_descriptions(
        self,
        schema: dict[str, Any],
        swagger_data: dict[str, Any],
        descriptions: dict[str, str],
        parent_key: str = "",
        _active_refs: set[str] | None = None,
    ) -> None:
        """
        递归提取嵌套参数的描述信息

        自引用模型（如树形结构的 children 指向自身、A/B 互相引用）会在 ``$ref``
        处成环，因此沿递归分支记录已展开的 ``$ref``（``_active_refs``），再次遇到
        即停止；兄弟节点引用同一模型时互不影响，可各自完整展开。

        Args:
            schema: 参数的schema定义
            swagger_data: 完整的Swagger文档数据
            descriptions: 存储描述信息的字典
            parent_key: 父级参数名（用于嵌套参数）
            _active_refs: 当前递归分支上已展开的 $ref（内部防环用）
        """
        if _active_refs is None:
            _active_refs = set()

        properties: dict[str, Any] | None = None
        ref: str | None = None
        if isinstance(schema, dict) and "$ref" in schema:
            ref = str(schema["$ref"])
            if ref in _active_refs:
                return  # 自引用环：该分支已展开过，停止
            definition = self._resolve_schema_ref(ref, swagger_data)
            if definition and "properties" in definition:
                properties = definition["properties"]
                _active_refs.add(ref)
        elif isinstance(schema, dict) and "properties" in schema:
            properties = schema["properties"]

        if properties:
            for prop_name, prop_info in properties.items():
                if not isinstance(prop_info, dict):
                    continue
                full_key = f"{parent_key}.{prop_name}" if parent_key else prop_name
                prop_desc = sanitize_remark(prop_info.get("description", ""))
                if prop_name and prop_desc:
                    descriptions[full_key] = prop_desc
                # 递归处理嵌套对象/引用与数组元素
                if prop_info.get("type") == "object" or "$ref" in prop_info:
                    self._extract_nested_descriptions(prop_info, swagger_data, descriptions, full_key, _active_refs)
                elif prop_info.get("type") == "array":
                    items = prop_info.get("items", {})
                    self._extract_nested_descriptions(items, swagger_data, descriptions, full_key, _active_refs)

        if ref is not None:
            _active_refs.discard(ref)
