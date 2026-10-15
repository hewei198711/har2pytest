from __future__ import annotations

import asyncio
import os
import time
from typing import Any

from .api_metadata import write_api_metadata
from .codegen import render_lines, validate_python
from .config import APIConfig
from .logger import logger
from .models import ParsedRequestInfo, SwaggerInfo
from .swagger_handler import SwaggerHandler
from .url_matcher import URLMatcher
from .utils import (
    build_param_values,
    build_time_pairs,
    format_headers_for_python,
    format_parameter_value,
    format_params_for_python,
    sanitize_remark,
    write_test_file,
)
from .utils import (
    format_directory as _format_directory,
)

_BODY_METHODS = ("POST", "PUT", "PATCH", "DELETE")
"""按请求体携带方式处理的方法（GET 之外的常见写操作，client 均支持）。"""


def _find_file_upload_key(post_data: Any) -> str | None:
    """从 multipart post_data 中识别文件参数字典的键名（值为 "(binary)" 或以 "@" 开头）。

    用于解析期 is_file_upload 判定与 _handle_file_upload 共用，避免两处判定漂移。
    """
    if not isinstance(post_data, dict):
        return None
    for key, value in post_data.items():
        if isinstance(value, str) and (value == "(binary)" or value.startswith("@")):
            return key
    return None


class APIGenerator:
    """API 文件生成器类"""

    # 定义默认的 Swagger 信息结构常量
    DEFAULT_SWAGGER_INFO = SwaggerInfo()

    def __init__(self, output_dir: str | None = None):
        """
        初始化 API 生成器

        Args:
            output_dir: API 文件输出目录，默认为 APIConfig.DEFAULT_API_DIR

        Example:
            generator = APIGenerator(output_dir="api")
        """
        if output_dir is None:
            output_dir = APIConfig.DEFAULT_API_DIR()
        self.output_dir = output_dir
        self.swagger_handler = SwaggerHandler()
        self.url_matcher = URLMatcher()

    def check_api_exists(self, url: str, service_package: str, function_name: str | None = None) -> bool:
        """
        检查 API 接口文件是否已经存在

        Args:
            url: 原始接口URL，如 /mobile/trade/orderCommit
            service_package: 服务包名称，如 mall_mobile_application
            function_name: 目标函数名（缺省由 url 推导；同名多方法场景会带方法后缀）

        Returns:
            bool: 如果 API 文件已存在返回True，否则返回False

        Example:
            exists = generator.check_api_exists("/mobile/trade/order", "mall_mobile_application")
            # 如果文件存在返回True，否则返回False
        """
        function_name = function_name or URLMatcher.generate_function_name(url)
        filename = f"{function_name}.py"
        # 候选路径：根目录 + 服务包目录（service_package 非默认时）
        paths = [os.path.join(self.output_dir, filename)]
        if service_package != APIConfig.DEFAULT_API_DIR():
            paths.append(os.path.join(self.output_dir, service_package, filename))
        return any(os.path.exists(p) for p in paths)

    def _parse_request_info(self, request_info: ParsedRequestInfo) -> ParsedRequestInfo:
        """解析请求信息"""
        method = request_info.method.upper()
        url = request_info.url
        query_params = request_info.query_params
        post_data = request_info.post_data
        raw_headers = request_info.headers

        headers = dict(raw_headers)
        # 用 REQUIRED_HEADERS 覆盖默认头：HTTP 头名大小写不敏感，
        # 若已有同名（仅大小写不同）的抓包头，先移除再写入配置的规范键名，
        required_headers = APIConfig.REQUIRED_HEADERS()
        for key, default_value in required_headers.items():
            existing = next((k for k in headers if k.lower() == key.lower()), None)
            if existing is not None and existing != key:
                del headers[existing]
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

        if method in _BODY_METHODS:
            if content_type and "application/json" in content_type:
                is_json_content = True
            elif content_type and content_type.startswith("multipart/form-data"):
                is_multipart = True
                is_file_upload = _find_file_upload_key(post_data) is not None
            elif not content_type and request_info.content_type:
                # 没有 content-type 请求头时回退到 postData.mimeType
                mime = request_info.content_type.lower()
                if "application/json" in mime:
                    is_json_content = True
                elif mime.startswith("multipart/form-data"):
                    is_multipart = True
                    is_file_upload = _find_file_upload_key(post_data) is not None
            elif not content_type:
                is_json_content = bool(post_data)

        # 仅 POST 且无有效请求体时按 application/x-www-form-urlencoded 处理：
        # - content-length=0 的空 body POST（HAR 无参数），生成空 data 占位便于手动补充表单参数
        # - body 为空 JSON（{}）但 URL 带 query 参数（如 ?orderNo=xxx），query 参数作为表单数据 urlencode 传参
        # PUT/PATCH/DELETE 的 query 参数是 URL 语义，不能塞进 body（见 _determine_param_info）
        is_need_urlencode = (
            method == "POST" and not post_data and not is_multipart and (content_length == "0" or bool(query_params))
        )

        # 清理 headers：移除 content-length 和 content-type
        # content-type 由各分支按需重新设置：urlencode 在 _process_parameters 中统一添加，
        # multipart/文件上传在函数体内动态设置，json/data 由 requests 自动处理
        for key in list(headers.keys()):
            kl = key.lower()
            if kl in ("content-length", "content-type"):
                del headers[key]

        # 使用统一的URL匹配器（swagger_data已在外部设置）
        url_info = self.url_matcher.get_url_info(url)

        return ParsedRequestInfo(
            method=method,
            url=url_info["pattern"] or url,
            query_params=query_params,
            post_data=post_data,
            headers=headers,
            is_file_upload=is_file_upload,
            is_multipart=is_multipart,
            is_need_urlencode=is_need_urlencode,
            is_json_content=is_json_content,
            path_params=url_info["path_params"],
            url_pattern=url_info["pattern"],
            function_name=url_info["function_name"],
        )

    async def generate_api_file(
        self,
        request_info: ParsedRequestInfo,
        force_overwrite: bool = False,
        swagger_info: SwaggerInfo | None = None,
        swagger_doc: dict[str, Any] | None = None,
        function_name_suffix: str | None = None,
        service_package: str | None = None,
        constant_params: dict[str, Any] | None = None,
        har_param_values: dict[str, list[Any]] | None = None,
    ) -> str | None:
        """生成 API 文件（异步）

        Args:
            request_info: 解析后的请求信息
            force_overwrite: 是否强制覆盖已存在的文件
            swagger_info: Swagger API 信息（summary、description、parameters）
            swagger_doc: 预取的 Swagger 完整文档，传入后跳过内部获取，避免并行竞态条件
            function_name_suffix: 函数名后缀（同一路径存在多个 HTTP 方法时用于区分文件，
                如 ``put`` → ``xxx_put.py``），默认不追加
            service_package: 显式指定的服务包名称。Swagger 命令场景下由
                ``generate_apis_from_swagger`` 根据 SWAGGER_DOC_URLS 键名自动传入；
                HAR 场景下未指定时通过 URL 前缀匹配 SERVICE_MAPPING 决定。
        """
        method = request_info.method.upper()
        url = request_info.url

        # 服务包判定：显式指定优先（Swagger 命令场景），否则通过 URL 前缀匹配
        if service_package is None:
            service_package = APIConfig.determine_service_package(url)
        # 如果已传入swagger_info，不需要获取Swagger文档
        if swagger_info is None:
            # 获取整个Swagger文档（用于URL模板匹配和获取 API 信息）
            if swagger_doc is None:
                if service_package in APIConfig.SWAGGER_DOC_URLS():
                    swagger_doc = await self.swagger_handler.get_swagger_doc(
                        APIConfig.SWAGGER_DOC_URLS()[service_package]
                    )

            # 设置swagger_data到url_matcher
            self.url_matcher.swagger_data = swagger_doc

            # 解析请求信息，获取URL模式
            parsed_info = self._parse_request_info(request_info)
            url_pattern = parsed_info.url_pattern or url

            # 获取特定URL的Swagger信息（summary、description、parameters）
            if swagger_doc:
                swagger_info = self.swagger_handler.find_api_info_in_swagger(swagger_doc, url_pattern, method)

            # 使用URLMatcher生成的函数名
            function_name = parsed_info.function_name
        else:
            parsed_info = self._parse_request_info(request_info)
            # 保留 swagger_handler 中提取的路径参数
            if request_info.path_params:
                parsed_info.path_params = request_info.path_params
            function_name = parsed_info.function_name
            url_pattern = parsed_info.url_pattern or url

        # 检查文件是否存在（function_name_suffix 会改变目标文件名，需据此判断）
        if function_name_suffix:
            function_name = f"{function_name}_{function_name_suffix}"
        if self.check_api_exists(url_pattern, service_package, function_name):
            if not force_overwrite:
                logger.info(f"接口已存在，跳过生成: {method} {url_pattern}")
                return None
            else:
                logger.info(f"接口已存在，强制覆盖: {method} {url_pattern}")

        # 生成文件路径
        filename = f"{function_name}.py"
        if service_package == APIConfig.DEFAULT_API_DIR():
            filepath = os.path.join(self.output_dir, filename)
        else:
            filepath = os.path.join(self.output_dir, service_package, filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # 生成文件内容（使用从Swagger获取的数据）
        content = self.generate_file_content(request_info, function_name, swagger_info, parsed_info)
        write_test_file(filepath, content)

        # 同步写 API 元数据：下游（URL匹配/测试用例生成）只消费结构化元数据，
        # 不再解析生成的源码文本。
        # params/data/files/headers 的当前值由 _module_value_snapshot 直接给出
        # （与 _process_parameters 渲染模块级赋值共用同一决策，无需二次解析）。
        # 无 swagger 文档（如纯 HAR 场景）时与 generate_file_content 一样用默认值
        meta_swagger = swagger_info if swagger_info is not None else self.DEFAULT_SWAGGER_INFO
        description = self._docstring_first_line(meta_swagger)
        # 没有 swagger 描述时不写 "TODO: 添加接口描述" 占位（避免冻结占位符当真实描述）
        if description == "TODO: 添加接口描述":
            description = ""
        current_values = self._module_value_snapshot(parsed_info)
        param_remarks_dict = dict(meta_swagger.parameters or {})
        param_values = build_param_values(param_remarks_dict)
        time_pairs = build_time_pairs(param_remarks_dict)
        # HAR 场景：params 纯粹来自 Swagger 定义（类型感知默认值），
        # 实际请求值写入 har_params（与 Swagger 的 params 完全分离）
        is_har = constant_params is not None
        # HAR 实际请求参数基线：GET 的参数落在 params（query+path），
        # POST 的落在 data（query+body），两键可能并存（如 POST body + 路径参数），
        # 因此合并而非二选一，避免 POST 接口 har_params 恒为 null
        har_params = None
        har_time_pairs = None
        if is_har:
            har_params = {}
            for key in ("params", "data"):
                value = current_values.get(key)
                if isinstance(value, dict):
                    har_params.update(value)
            # 补齐 har_param_values 中未出现在首条请求基线的单参数键（值为 ""），
            # 保证键集合完整：参数化枚举覆盖的参数名可能只出现在部分请求中
            # （如 orderNo 仅个别请求携带），缺失会让下游 list_query_data 缺键
            # （收集期 KeyError）且方法体 params 缺参数定义（组合键不补）
            if har_param_values:
                for pn in har_param_values:
                    if "," not in pn and pn not in har_params:
                        har_params[pn] = ""
            # HAR 场景从参数基线自行配对时间对（无 Swagger 备注可提取格式，
            # 默认 %Y-%m-%d），写入 har_time_pairs 供测试生成动态计算时间参数
            har_time_pairs = build_time_pairs({name: "" for name in har_params}) or None
        # 以 param_remarks 为基准（保证所有 Swagger 定义的参数都在），
        # 用类型感知默认值覆盖（缺失的参数字符串兜底）
        swagger_params: dict[str, Any] = {
            name: meta_swagger.param_defaults.get(name, "")
            for name in param_remarks_dict
        }
        if not is_har:
            # 非 HAR 场景：params 包含请求实际值（无 har_params 字段）
            request_params = current_values.get("params") or {}
            if isinstance(request_params, dict):
                swagger_params.update(request_params)
        meta_file = write_api_metadata(
            filepath,
            function_name=function_name,
            url=parsed_info.url or url,
            description=description,
            method=parsed_info.method or method,
            service_package=service_package,
            param_remarks=param_remarks_dict,
            param_values=param_values,
            time_pairs=time_pairs,
            params=swagger_params,
            data=current_values.get("data"),
            files=current_values.get("files"),
            headers=current_values.get("headers"),
            constant_params=constant_params,
            har_param_values=har_param_values,
            har_params=har_params,
            har_time_pairs=har_time_pairs,
        )
        if meta_file:
            logger.debug(f"已写入 API 元数据: {meta_file}")

        return filepath

    @staticmethod
    def _docstring_candidate(swagger_info: SwaggerInfo) -> str:
        """返回 docstring 首段候选文本（summary 优先，其次 description，缺省 TODO 占位）。"""
        return swagger_info.summary or swagger_info.description or "TODO: 添加接口描述"

    @classmethod
    def _docstring_first_line(cls, swagger_info: SwaggerInfo) -> str:
        """返回生成 docstring 第一行（与旧 parse_api_file 提取语义一致）。"""
        lines = [ln.strip() for ln in cls._docstring_candidate(swagger_info).splitlines() if ln.strip()]
        return lines[0] if lines else "TODO: 添加接口描述"

    def _generate_params_string(
        self, params_dict: dict[str, Any] | list[Any], swagger_info: SwaggerInfo | None = None
    ) -> str:
        """
        生成 API 文件中的参数字符串

        将参数字典生成为Python代码字符串，为每个参数添加参数说明

        Args:
            params_dict: 参数字典，如 {"keyword": "TS001", "pageNum": 1}；
                也可能是 JSON 数组请求体（list），此时直接生成 Python 字面量
            swagger_info: Swagger文档信息，包含description、parameters等

        Returns:
            str: 生成的参数字符串

        Example:
            params = {"keyword": "TS001", "pageNum": 1}
            result = generator._generate_params_string(params)
            # 返回生成的参数字符串
        """
        if isinstance(params_dict, dict):
            if not params_dict:
                return "{}"

            # 直接使用 Swagger 的 parameters 字典（包含 dotted key 如 "payDTO.accountName"），
            # format_params_for_python 会递归查找嵌套键的注释
            if swagger_info is None:
                swagger_info = self.DEFAULT_SWAGGER_INFO
            comments = swagger_info.parameters
            return format_params_for_python(params_dict, format_parameter_value, comments, inline=False)

        # 非 dict 请求体（如 JSON 数组 body）直接生成 Python 字面量，无参数备注
        return format_parameter_value(params_dict) if params_dict else "[]"

    def _generate_imports(self, parsed_info: ParsedRequestInfo) -> list[str]:
        """
        生成导入语句

        由 Jinja2 模板 ``api_imports.j2`` 渲染。

        Args:
            parsed_info: 解析后的请求信息

        Returns:
            List[str]: 导入语句列表
        """
        lines = render_lines(
            "api_imports.j2",
            is_file_upload=parsed_info.is_file_upload,
            is_multipart=parsed_info.is_multipart,
            is_need_urlencode=parsed_info.is_need_urlencode,
            plain_client=not (parsed_info.is_file_upload or parsed_info.is_multipart),
        )
        # 与旧实现一致：导入段以空行结束（分隔参数定义）
        if not lines or lines[-1] != "":
            lines.append("")
        return lines

    def _determine_param_info(self, parsed_info: ParsedRequestInfo) -> tuple[str | None, dict[str, Any] | None]:
        """根据解析后的请求信息确定参数名和参数数据，用于 _process_parameters 和 _generate_function_definition 共用。

        返回 ``(param_name, param_data)``：
        - GET：带 query/路径参数时合并进 ``params``（路径键供 URL f-string 引用）；
        - POST：优先按 payload（urlencode/body/query）返回 ``data``（或上传 ``files``），
          路径参数由模块级 ``params``（路径默认值）单独承载，避免 body/query 被丢弃；
        - POST 无 payload 但有路径参数：仅 ``params``（URL f-string 引用）。
        """
        method = parsed_info.method
        path_params = parsed_info.path_params or {}
        query_params = parsed_info.query_params or {}
        post_data = parsed_info.post_data
        is_file_upload = parsed_info.is_file_upload
        is_need_urlencode = parsed_info.is_need_urlencode

        if method == "GET":
            if not path_params and not query_params:
                return None, None
            # GET + 路径参数 + query：合并进 params（URL f-string 引用路径键）
            merged = dict(path_params)
            merged.update(query_params)
            return "params", merged

        if method in _BODY_METHODS:
            if is_need_urlencode:
                # urlencoded：query 作为表单数据（无 query 时空 data 占位）
                return "data", query_params or {}
            if is_file_upload:
                return "files", post_data
            if post_data:
                if isinstance(post_data, dict) and query_params:
                    # body 为 dict 时合并 URL query 参数，避免参数丢失（post 覆盖同名 query）
                    merged_data = dict(query_params)
                    merged_data.update(post_data)
                    return "data", merged_data
                return "data", post_data
            if query_params:
                if method != "POST":
                    # 非 POST 写方法（PUT/PATCH/DELETE）无请求体时，query 参数属于 URL 语义，
                    # 必须走 params 拼到 URL 上；塞进 body 会让服务端按 URL 寻址时丢参
                    merged = dict(path_params)
                    merged.update(query_params)
                    return "params", merged
                # POST 空 body 但带 query 参数（如 ?orderNo=xxx），并入 data 生成，避免参数丢失
                return "data", query_params
            if path_params:
                # POST 空 body + 路径参数：仅路径 params（URL f-string 引用）
                return "params", dict(path_params)
        return None, None

    def _process_parameters(self, parsed_info: ParsedRequestInfo, swagger_info: SwaggerInfo | None = None) -> list[str]:
        """
        处理参数

        处理路径参数、查询参数和POST数据，生成参数定义代码

        Args:
            parsed_info: 解析后的请求信息
            swagger_info: Swagger文档信息，包含description、parameters等

        Returns:
            List[str]: 参数定义代码列表
        """
        if swagger_info is None:
            swagger_info = self.DEFAULT_SWAGGER_INFO
        params_section = []

        headers = parsed_info.headers
        is_need_urlencode = parsed_info.is_need_urlencode

        param_name, param_data = self._determine_param_info(parsed_info)

        if param_name:
            formatted_params = self._generate_params_string(param_data or {}, swagger_info)
            params_section.append(f"{param_name} = {formatted_params}")
            params_section.append("")

        # 路径参数 + POST body/query（模块级 params 由路径默认值提供，供 URL f-string 引用；
        # 不并入 data，避免路径键泄漏进请求体）
        if (
            parsed_info.path_params
            and param_name
            and param_name != "params"
        ):
            formatted_path = self._generate_params_string(dict(parsed_info.path_params), swagger_info)
            params_section.insert(0, f"params = {formatted_path}")
            params_section.insert(1, "")

        # 添加 headers 参数定义
        formatted_headers = format_headers_for_python(headers)
        if is_need_urlencode:
            urlencode_headers = headers.copy()
            urlencode_headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            formatted_urlencode_headers = format_headers_for_python(urlencode_headers)
            params_section.append(f"headers = {formatted_urlencode_headers}")
        else:
            params_section.append(f"headers = {formatted_headers}")

        return params_section

    def _module_value_snapshot(self, parsed_info: ParsedRequestInfo) -> dict[str, Any]:
        """模块级赋值（params/data/files/headers）的**当前值**快照。

        与 ``_process_parameters`` 渲染的模块级赋值使用同一决策（_determine_param_info +
        headers 规则），因此直接作为元数据快照写入，无需再对生成文本做二次解析。

        Returns:
            dict: 可能含 ``params``/``data``/``files`` 之一与 ``headers`` 的字典。
        """
        snapshot: dict[str, Any] = {}
        param_name, param_data = self._determine_param_info(parsed_info)
        if param_name:
            snapshot[param_name] = param_data if param_data is not None else {}
        # 路径参数与 body 并存时，模块顶部另有一条独立的 params = {路径默认值}
        if param_name and param_name != "params" and parsed_info.path_params:
            snapshot["params"] = dict(parsed_info.path_params)

        headers = dict(parsed_info.headers or {})
        if parsed_info.is_need_urlencode:
            headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        snapshot["headers"] = headers
        return snapshot

    def _handle_file_upload(self, post_data: Any) -> list[str]:
        """处理文件上传，生成代码实现。

        Args:
            post_data: POST数据

        Returns:
            List[str]: 文件上传代码列表
        """
        if not isinstance(post_data, dict):
            raise ValueError("文件上传参数格式错误")

        # 动态识别文件参数名（值为 (binary) 或以 @ 开头的 key），与解析期共用同一判定
        file_key = _find_file_upload_key(post_data)
        if file_key is None:
            raise ValueError("文件上传参数格式错误：未找到文件参数")

        # 统一使用 build_multipart_data，自动适配同步/异步客户端
        return render_lines("api_file_upload.j2", file_key=file_key)

    def _handle_multipart_form(self) -> list[str]:
        """处理 multipart/form-data 请求（无文件上传）。

        由 Jinja2 模板 ``api_multipart_form.j2`` 渲染。

        Returns:
            List[str]: multipart 表单代码列表
        """
        return render_lines("api_multipart_form.j2")

    def _handle_http_method(
        self,
        method: str,
        params_var: str | None,
        path_params: dict[str, Any],
        query_params: dict[str, Any],
        is_need_urlencode: bool,
        is_json_content: bool = False,
    ) -> list[str]:
        """
        处理HTTP方法

        生成不同HTTP方法的代码实现，由 Jinja2 模板 ``api_http_method.j2`` 渲染。

        Args:
            method: HTTP方法
            params_var: 数据参数名（data/params，决定请求体/查询串分支）
            path_params: 路径参数
            query_params: 查询参数
            is_need_urlencode: 是否需要urlencode
            is_json_content: 是否为JSON请求

        Returns:
            List[str]: HTTP方法代码列表
        """
        if method not in ("GET", *_BODY_METHODS):
            raise ValueError(f"不支持的HTTP方法: {method}。目前支持 GET/POST/PUT/PATCH/DELETE 请求。")

        return render_lines(
            "api_http_method.j2",
            method=method,
            has_params=bool(query_params),
            has_path_params=bool(path_params),
            # data 变量只存在于 POST 带请求体/表单数据（params 仅用于 URL f-string）
            has_data=params_var == "data",
            is_urlencode=is_need_urlencode,
            is_json_content=is_json_content,
        )

    def _generate_function_definition(
        self, parsed_info: ParsedRequestInfo, function_name: str, swagger_info: SwaggerInfo
    ) -> list[str]:
        """
        生成函数定义

        由 Jinja2 模板 ``api_function_def.j2`` 渲染（签名、docstring、url、函数体）。

        Args:
            parsed_info: 解析后的请求信息
            function_name: 函数名称
            swagger_info: Swagger文档信息，包含description、parameters等

        Returns:
            List[str]: 函数定义和实现代码列表
        """
        method = parsed_info.method
        url = parsed_info.url
        query_params = parsed_info.query_params
        post_data = parsed_info.post_data
        is_file_upload = parsed_info.is_file_upload
        is_multipart = parsed_info.is_multipart
        is_need_urlencode = parsed_info.is_need_urlencode
        is_json_content = parsed_info.is_json_content
        path_params = parsed_info.path_params
        url_pattern = parsed_info.url_pattern

        param_name, _ = self._determine_param_info(parsed_info)

        # 函数签名：body/query 参数（data/files）优先；带路径参数时总是带上
        # params=params（路径默认值，URL f-string 引用），二者互不覆盖
        func_params = []
        if path_params and param_name and param_name != "params":
            func_params.append("params=params")
        if param_name:
            func_params.append(f"{param_name}={param_name}")
        func_params.append("headers=headers")

        # docstring 首段：summary 优先，其次 description，缺省 TODO 占位
        doc_first = self._docstring_candidate(swagger_info)

        # 路径参数时 url 用 f-string 占位替换（值来自 params 路径默认值）；否则普通字符串
        if path_params and url_pattern:
            url_with_params = url_pattern
            for path_param in path_params.keys():
                url_with_params = url_with_params.replace(f"{{{path_param}}}", f"{{params['{path_param}']}}")
            url_code = f'url = f"{url_with_params}"'
        else:
            url_code = f'url = "{url}"'

        # 生成函数体（文件上传 / multipart / 普通 HTTP 方法）
        if is_file_upload:
            body_lines = self._handle_file_upload(post_data)
        elif is_multipart:
            body_lines = self._handle_multipart_form()
        else:
            body_lines = self._handle_http_method(
                method, param_name, path_params, query_params, is_need_urlencode, is_json_content
            )

        return render_lines(
            "api_function_def.j2",
            function_name=function_name,
            func_params=", ".join(func_params),
            doc_first=doc_first,
            doc_url=url,
            param_docs=[(name, sanitize_remark(remark)) for name, remark in (swagger_info.parameters or {}).items()],
            url_code=url_code,
            body_lines=body_lines,
        )

    def generate_file_content(
        self,
        request_info: ParsedRequestInfo,
        function_name: str,
        swagger_info: SwaggerInfo | None = None,
        parsed_info: ParsedRequestInfo | None = None,
    ) -> str:
        """
        生成 API 文件内容

        根据请求信息和函数名生成 API 文件内容

        Args:
            request_info: 解析后的请求信息，包含 method、url、query_params、post_data、headers 等
            function_name: 函数名
            swagger_info: Swagger文档信息，包含description、parameters等
            parsed_info: 预解析的请求信息，如果为 None 则内部会解析

        Returns:
            str: 生成的文件内容

        Example:
            request_info = ParsedRequestInfo(
                method="POST",
                url="/mobile/trade/orderCommit",
                post_data={"productId": "123"},
                headers={"content-type": "application/json"},
            )
            content = generator.generate_file_content(request_info, "_mobile_trade_orderCommit")
            # 返回生成的文件内容
        """
        if swagger_info is None:
            swagger_info = self.DEFAULT_SWAGGER_INFO
        if parsed_info is None:
            parsed_info = self._parse_request_info(request_info)
        imports = self._generate_imports(parsed_info)
        params_section = self._process_parameters(parsed_info, swagger_info)
        function_def = self._generate_function_definition(parsed_info, function_name, swagger_info)

        content = "\n".join(imports + params_section + function_def)
        # 写盘前语法校验：模板渲染错误在生成期暴露，避免落盘非法 Python
        validate_python(content, f"API 模块 {function_name}")
        return content

    def generate_index_file(self, generated_files: list[str]) -> None:
        """
        生成 API 索引文件

        为生成的 API 文件生成__init__.py索引文件，包含所有 API 模块的导入语句
        按照服务包分组，在每个服务包的__init__.py文件中添加对应的导入语句

        Args:
            generated_files: 生成的文件路径列表，如 ["api/_mobile_product_search.py", "api/_mobile_trade_orderCommit.py"]

        Returns:
            None: 生成的索引文件保存在output_dir/__init__.py

        Example:
            from .har_generator import generate_api_files_from_har

            files = await generate_api_files_from_har("普通订单.har", api_generator=generator)
            generator.generate_index_file(files)
            # 生成api/__init__.py索引文件
        """
        # 按照服务包分组
        service_packages: dict[str, list[str]] = {}
        for filepath in generated_files:
            # 获取文件相对于 output_dir 的路径
            rel_path = os.path.relpath(filepath, self.output_dir).replace("\\", "/")
            # 获取服务包名称（第一级目录）
            path_parts = rel_path.split("/")
            if len(path_parts) >= 2:
                service_package = path_parts[0]
            else:
                # 根目录下的文件，服务包就是默认 API 目录名
                service_package = APIConfig.DEFAULT_API_DIR()
            if service_package not in service_packages:
                service_packages[service_package] = []
            service_packages[service_package].append(filepath)

        # 为每个服务包生成索引文件
        for service_package, files in service_packages.items():
            if service_package == APIConfig.DEFAULT_API_DIR():
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
            import_statements: list[str] = []
            for filepath in files:
                module_path = os.path.relpath(filepath, self.output_dir).replace("\\", "/")
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
                logger.info(f"服务包索引文件已包含所有 API 引用: {package_init_path}")

        # 确保主目录存在 __init__.py 文件
        main_init_path = os.path.join(self.output_dir, "__init__.py")
        if not os.path.exists(main_init_path):
            # 创建空白的 __init__.py 文件
            with open(main_init_path, "w", encoding="utf-8") as f:
                f.write("")
            logger.info(f"创建主目录索引文件: {main_init_path}")

    @staticmethod
    def _build_full_path(path: str, base_path: str) -> str:
        """构建完整的 URL 路径：若 path 已包含 base_path 则原样返回，否则拼接。"""
        base_prefix = base_path.rstrip("/") if base_path else ""
        if base_prefix and not (path == base_prefix or path.startswith(base_prefix + "/")):
            return base_prefix + "/" + path.lstrip("/")
        return path

    def _operation_target_key(self, path: str, base_path: str, service_package: str | None = None) -> str:
        """返回该 operation 将写入的目标标识 ``服务包/函数名``（用于去重同名文件）。

        Args:
            path: Swagger 文档中的原始路径。
            base_path: 文档 basePath。
            service_package: 显式指定的服务包名称（Swagger 命令场景下由 SWAGGER_DOC_URLS 键名确定）。

        Returns:
            str: ``<service_package>/<function_name>`` 形式的目标标识。
        """
        full_path = self._build_full_path(path, base_path)
        info = self.url_matcher.get_url_info(full_path)
        pattern = info["pattern"] or full_path
        pkg = service_package or APIConfig.determine_service_package(pattern)
        return f"{pkg}/{URLMatcher.generate_function_name(pattern)}"

    @staticmethod
    def _resolve_service_package_for_swagger_url(swagger_url: str) -> str | None:
        """根据 Swagger URL 反查 SWAGGER_DOC_URLS 中对应的服务包名称。

        通过比较清洗后的 URL，找到该 Swagger 文档在配置中对应的服务包键名。
        用于 Swagger 命令场景下直接按配置键名决定文件目录，
        避免依赖 SERVICE_MAPPING 的 URL 前缀匹配。

        Args:
            swagger_url: 用户提供的 Swagger 文档 URL。

        Returns:
            str | None: 匹配的服务包名称，未找到时返回 None。
        """
        swagger_doc_urls = APIConfig.SWAGGER_DOC_URLS()
        if not swagger_doc_urls:
            return None
        cleaned = SwaggerHandler._clean_swagger_url(swagger_url)
        for service_name, doc_url in swagger_doc_urls.items():
            if SwaggerHandler._clean_swagger_url(doc_url) == cleaned:
                return service_name
        return None

    async def generate_apis_from_swagger(
        self,
        swagger_url: str,
        force_overwrite: bool = False,
        specific_path: str | None = None,
        service_package: str | None = None,
    ) -> list[str]:
        """
        从Swagger文档异步批量生成 API 文件

        解析Swagger文档，获取所有 API 路径和方法，为每个 API 生成对应的 API 文件

        Args:
            swagger_url: Swagger文档URL
            force_overwrite: 是否覆盖已存在的文件
            specific_path: 只生成指定的 API 路径，默认为None（生成所有路径）
            service_package: 显式指定的服务包名称；未指定时自动从 swagger_url 反查
                SWAGGER_DOC_URLS，仍找不到则抛出 ValueError。

        Returns:
            List[str]: 生成的文件路径列表
        """

        generated_files: list[str] = []

        try:
            # 服务包必须可从 SWAGGER_DOC_URLS 解析，否则直接报错
            if service_package is None:
                service_package = self._resolve_service_package_for_swagger_url(swagger_url)
            if not service_package:
                raise ValueError(
                    f"Swagger URL 未在 SWAGGER_DOC_URLS 中找到对应配置: {swagger_url}\n"
                    f"请在 har2pytest_config.json 的 SWAGGER_DOC_URLS 中添加该 URL 的映射。"
                )
            logger.info(f"✓ Swagger URL 匹配服务包: {service_package}")

            # 异步获取Swagger文档
            swagger_data = await self.swagger_handler.get_swagger_doc(swagger_url)
            if not swagger_data:
                logger.error(f"无法获取Swagger文档: {swagger_url}")
                return generated_files

            # 设置 swagger_data 到 url_matcher，确保后续 URL 匹配能正确提取路径参数
            self.url_matcher.swagger_data = swagger_data

            # 获取Swagger文档的basePath
            base_path = swagger_data.get("basePath", "")

            # 遍历所有 API 路径
            paths = swagger_data.get("paths", {})
            logger.info(f"从Swagger文档中发现 {len(paths)} 个 API 路径")

            # 如果指定了特定路径，直接查找而不是遍历
            paths_to_process = list(paths.items())
            if specific_path:
                # paths 的键可能已包含 basePath（springfox 常见：basePath=/admin 且键为 /admin/xxx），
                # 也可能不含，因此按“原样 → 去掉 basePath → 拼上 basePath”依次尝试
                candidates = [specific_path]
                stripped = specific_path
                if base_path and base_path != "/" and stripped.startswith(base_path):
                    stripped = stripped[len(base_path) :]
                    if not stripped.startswith("/"):
                        stripped = "/" + stripped
                    candidates.append(stripped)
                if base_path and base_path != "/":
                    candidates.append(base_path.rstrip("/") + "/" + specific_path.lstrip("/"))

                search_path = next((candidate for candidate in candidates if candidate in paths), None)

                # 直接在paths中查找
                if search_path:
                    paths_to_process = [(search_path, paths[search_path])]
                else:
                    logger.warning(f"指定的路径 {specific_path} 在Swagger文档中未找到")
                    return generated_files

            # 定义异步任务函数：处理单个 API
            async def process_api(
                path: str, method: str, method_data: dict, function_name_suffix: str | None = None
            ) -> str | None:
                """处理单个 API 路径和方法的文件生成。"""
                task_start = time.time()
                try:
                    full_path = self._build_full_path(path, base_path)
                    logger.debug(f"  [任务开始] {method.upper()} {full_path}")

                    # 构建请求信息
                    request_info = ParsedRequestInfo(
                        method=method.upper(),
                        url=full_path,
                        query_params={},
                        post_data={},
                        headers=dict(APIConfig.REQUIRED_HEADERS()),
                    )

                    # 提取参数
                    parameters = method_data.get("parameters", [])
                    (
                        query_params,
                        post_data,
                        has_query_param,
                        has_body_param,
                        path_params,
                        param_descriptions,
                    ) = self.swagger_handler._extract_params_from_swagger(parameters, swagger_data)

                    request_info.query_params = query_params
                    request_info.post_data = post_data
                    request_info.path_params = path_params

                    # 提取 API 信息（包括描述、参数说明和类型感知默认值）。
                    # param_defaults 与 find_api_info_in_swagger 保持同一填充顺序
                    # （query → path → body），保证 params 字段类型感知默认值不退化
                    swagger_info = SwaggerInfo(
                        summary=method_data.get("summary", ""),
                        description=method_data.get("description", "") or method_data.get("summary", ""),
                        parameters=param_descriptions,
                    )
                    swagger_info.param_defaults.update(query_params)
                    swagger_info.param_defaults.update(path_params)
                    if isinstance(post_data, dict):
                        swagger_info.param_defaults.update(post_data)

                    # 判断是否需要urlencode
                    if method.upper() in _BODY_METHODS and has_query_param and not post_data and not has_body_param:
                        request_info.headers["content-length"] = "0"

                    # 生成 API 文件
                    filepath = await self.generate_api_file(
                        request_info, force_overwrite, swagger_info,
                        function_name_suffix=function_name_suffix,
                        service_package=service_package,
                    )
                    elapsed = time.time() - task_start
                    if filepath:
                        logger.debug(f"  [任务完成] {method.upper()} {full_path} → {filepath} (耗时 {elapsed:.2f}s)")
                    else:
                        logger.debug(f"  [任务跳过] {method.upper()} {full_path} (耗时 {elapsed:.2f}s)")
                    return filepath
                except Exception as e:
                    elapsed = time.time() - task_start
                    logger.error(f"  [任务失败] {method.upper()} {path} (耗时 {elapsed:.2f}s): {str(e)}")
                    return None

            # 创建所有异步任务
            logger.info(f"[并行处理] 创建 {len(paths_to_process)} 个路径的任务...")
            tasks = []
            task_count = 0
            # 同一 path 的多个 method（如 GET+POST）会落到同一个 API 文件名：
            # 首个沿用原名，其余追加方法后缀，避免并发互相覆盖导致接口丢失/内容不确定。
            seen_targets: dict[str, tuple[str, str]] = {}
            for path, methods in paths_to_process:
                for method, method_data in methods.items():
                    method_upper = method.upper()
                    if method_upper not in ("GET", *_BODY_METHODS):
                        logger.info(f"跳过不支持的HTTP方法: {method_upper} {path}")
                        continue
                    target = self._operation_target_key(path, base_path, service_package=service_package)
                    if target in seen_targets:
                        prev_method, prev_path = seen_targets[target]
                        function_name_suffix = method.lower()
                        logger.warning(
                            f"{method_upper} {path} 与 {prev_method.upper()} {prev_path} 目标文件同名，"
                            f"改用方法后缀生成: {target}_{function_name_suffix}.py"
                        )
                    else:
                        seen_targets[target] = (method, path)
                        function_name_suffix = None
                    tasks.append(process_api(path, method, method_data, function_name_suffix))
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
                        logger.info(f"✓ 生成 API 文件: {filepath}")
                    else:
                        logger.info("- 跳过已存在的 API 文件")
                except Exception as e:
                    logger.error(f"❌ 生成 API 文件失败: {str(e)}")
                completed_count += 1
                if completed_count % 10 == 0 or completed_count == task_count:
                    logger.debug(f"  [并行进度] {completed_count}/{task_count} 已完成")
            parallel_elapsed = time.time() - parallel_start

            logger.info("\n============================================")
            logger.info(f"从Swagger文档生成完成: 成功 {success_count} 个, 总耗时 {parallel_elapsed:.2f}s")
            logger.info("============================================")

            # 批量格式化生成的 API 文件
            if generated_files:
                await _format_directory(self.output_dir)

        except Exception as e:
            logger.error(f"❌ 从Swagger文档生成 API 文件失败: {str(e)}")

        return generated_files
