"""核心数据模型模块。

使用 dataclass 替代裸 dict，提供类型安全、IDE 自动补全和自文档化的数据结构。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SwaggerInfo:
    """Swagger API 信息。

    Attributes:
        description: API 描述（通常为接口名称或详细说明）
        parameters: 参数说明字典，键为参数名（支持 dotted key），值为描述文本
        summary: API 摘要信息
        param_defaults: 参数类型感知默认值（string→"", integer→None 等）
    """

    description: str = ""
    parameters: dict[str, str] = field(default_factory=dict)
    summary: str = ""
    param_defaults: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedRequestInfo:
    """解析后的请求信息。

    由 _parse_request_info 生成，包含原始请求信息和派生字段。
    字段可变，支持 swagger_handler 路径参数覆盖等场景。

    Attributes:
        method: HTTP 方法（GET/POST）
        url: 接口 URL（模板化或原始 URL）
        full_url: HAR 中的完整原始 URL
        query_params: URL 查询参数
        post_data: POST 请求体数据
        headers: 请求头字典
        content_type: 请求体 Content-Type（来自 HAR postData.mimeType）
        cookies: Cookie 字典
        response_status: 响应状态码
        response_content: 响应内容（JSON 解析后的对象或原始文本）
        response_time: 响应时间（毫秒）
        server_ip: 服务器 IP 地址
        is_file_upload: 是否为文件上传请求
        is_multipart: 是否为 multipart/form-data 请求
        is_need_urlencode: 是否需要 urlencode 编码
        is_json_content: 是否为 JSON 请求体
        path_params: 路径参数
        url_pattern: 匹配到的 Swagger URL 模板
        function_name: 生成的函数名
    """

    method: str = ""
    url: str = ""
    full_url: str = ""
    query_params: dict[str, Any] = field(default_factory=dict)
    post_data: Any = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    content_type: str = ""
    cookies: dict[str, str] = field(default_factory=dict)
    response_status: int = 0
    response_content: Any = None
    response_time: float = 0.0
    server_ip: str = ""
    is_file_upload: bool = False
    is_multipart: bool = False
    is_need_urlencode: bool = False
    is_json_content: bool = False
    path_params: dict[str, Any] = field(default_factory=dict)
    url_pattern: str | None = None
    function_name: str = ""


@dataclass
class APIFileInfo:
    """API 文件元数据（由 parse_api_file 从 .api.json 读取）。

    用于测试用例生成时使用 API 文件的原始参数和备注信息。

    Attributes:
        function_name: 函数名（来自文件名去后缀，不含下划线前缀）
        description: 接口描述
        url: 接口 URL
        param_remarks: 参数备注字典（支持 dotted key）
        param_values: 从备注中解析出的参数枚举值字典（如 {"getType": [1,2,3]}）
        time_pairs: 时间参数对元数据（如 {"getTime": {"start": "getTimeStartTime", "end": "getTimeEndTime", "format": "yyyy-MM-dd"}}）
        headers: 请求头字典
        params: 参数值字典
        data: data 参数值
        files: files 参数值
        constant_params: 常量参数（在超过 50% 的 HAR 请求中值都相同的参数）
        har_param_values: HAR 参数枚举值字典（从所有 HAR 快照收集的去重值列表）
        har_params: HAR 参数基线值字典（常量参数 + 首条请求的所有参数值）
    """

    function_name: str | None = None
    description: str = ""
    url: str | None = None
    param_remarks: dict[str, str] = field(default_factory=dict)
    param_values: dict[str, list[Any]] = field(default_factory=dict)
    time_pairs: dict[str, dict[str, str]] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
    data: Any = field(default_factory=dict)
    files: dict[str, Any] = field(default_factory=dict)
    constant_params: dict[str, Any] = field(default_factory=dict)
    har_param_values: dict[str, list[Any]] = field(default_factory=dict)
    har_params: dict[str, Any] = field(default_factory=dict)
 