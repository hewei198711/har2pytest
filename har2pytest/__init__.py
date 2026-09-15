"""
API工具包 - 用于从HAR文件生成API接口和测试用例

主要功能：
1. HAR文件解析
2. API文件生成
3. 测试用例生成
4. Swagger文档更新
"""

from .api_generator import APIGenerator
from .client import AsyncClient, AsyncResponseContext, Client, ResponseContext, async_client, client
from .config import APIConfig
from .har_parser import HARParser
from .logger import logger, setup_logger
from .pytest_utils import retry_step
from .swagger_handler import SwaggerHandler
from .testcase_generator import TestCaseGenerator
from .url_matcher import URLMatcher
from .utils import (
    format_directory,
    format_headers_for_python,
    format_parameter_value,
    format_params_for_python,
    header_value_formatter,
    parse_api_file,
    write_test_file,
)

# ===========================================================================
# Allure async step 兼容层
#
# allure-commons 的 @allure.step 对 async 函数是“同步包装”，导致异步场景用例里
# 请求/响应附件逃逸到用例级。这里在包被导入时自动安装 async 感知包装（幂等；
# 若 allure 已原生支持 async step 会自动跳过）。
# ===========================================================================
try:
    from .allure_compat import install_async_step_support as _install_allure_async_support

    _install_allure_async_support()
except Exception:  # pragma: no cover - 兼容层失败不影响主功能
    pass

__all__ = [
    "APIConfig",
    "HARParser",
    "APIGenerator",
    "TestCaseGenerator",
    "SwaggerHandler",
    "URLMatcher",
    "logger",
    "setup_logger",
    "Client",
    "ResponseContext",
    "AsyncClient",
    "AsyncResponseContext",
    "client",
    "async_client",
    "format_directory",
    "header_value_formatter",
    "parse_api_file",
    "format_parameter_value",
    "format_headers_for_python",
    "format_params_for_python",
    "write_test_file",
    "retry_step",
]
