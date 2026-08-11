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
    """

    description: str = ""
    parameters: dict[str, str] = field(default_factory=dict)
    summary: str = ""


@dataclass
class ParsedRequestInfo:
    """解析后的请求信息。

    由 _parse_request_info 生成，包含原始请求信息和派生字段。
    字段可变，支持 swagger_handler 路径参数覆盖等场景。

    Attributes:
        method: HTTP 方法（GET/POST）
        url: 接口 URL（模板化或原始 URL）
        query_params: URL 查询参数
        post_data: POST 请求体数据
        headers: 请求头字典
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
    query_params: dict[str, Any] = field(default_factory=dict)
    post_data: Any = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    is_file_upload: bool = False
    is_multipart: bool = False
    is_need_urlencode: bool = False
    is_json_content: bool = False
    path_params: dict[str, Any] = field(default_factory=dict)
    url_pattern: str | None = None
    function_name: str = ""


@dataclass
class APIFileInfo:
    """解析后的 API 文件元数据。

    由 parse_api_file 生成，包含从已生成 API 文件中提取的所有元信息。
    用于测试用例生成时使用 API 文件的原始参数和备注信息。

    Attributes:
        function_name: 函数名（不含下划线前缀）
        description: 接口描述
        url: 接口 URL
        param_remarks: 参数备注字典（支持 dotted key）
        headers: 请求头字典
        params: 参数值字典
        data: data 参数值
        files: files 参数值
    """

    function_name: str | None = None
    description: str = ""
    url: str | None = None
    param_remarks: dict[str, str] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
    data: Any = field(default_factory=dict)
    files: dict[str, Any] = field(default_factory=dict)
 