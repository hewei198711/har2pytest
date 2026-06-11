"""HAR 文件生成器模块。

提供从 HAR 文件生成 API 接口文件的功能。
"""

import asyncio
import traceback

from .har_parser import HARParser
from .logger import logger
from .utils import format_directory


async def generate_api_files_from_har(
    har_file_path: str,
    force_overwrite: bool = False,
    api_generator=None,
) -> list[str]:
    """从 HAR 文件生成所有 API 接口文件。

    Args:
        har_file_path: HAR 文件路径，如 "api_request.har"。
        force_overwrite: 是否覆盖已存在的文件（默认 False）。
        api_generator: 可选的 API 生成器实例。

    Returns:
        list[str]: 生成的文件路径列表。

    Example:
        >>> files = await generate_api_files_from_har("普通订单.har")
        >>> # 返回生成的文件路径列表，如 ["api/_mobile_product_search.py", ...]
    """
    har_parser = HARParser()
    requests = har_parser.extract_requests_from_har(har_file_path)

    if not requests:
        logger.info(f"HAR文件 {har_file_path} 中没有找到有效的API请求")
        return []

    logger.info(f"发现 {len(requests)} 个API请求")

    if not api_generator:
        return []

    async def _process_one(request_info: dict) -> str | None:
        """异步处理单个请求，生成 API 文件。"""
        try:
            return await api_generator.generate_api_file(request_info, force_overwrite=force_overwrite)
        except Exception as e:
            logger.error(f"生成API文件失败: {str(e)}")
            logger.error(traceback.format_exc())
            return None

    # 并行处理所有 API 请求
    generated_files = []
    tasks = [_process_one(req) for req in requests]
    for coro in asyncio.as_completed(tasks):
        filepath = await coro
        if filepath:
            generated_files.append(filepath)

    # 批量格式化生成的 API 文件
    if generated_files and api_generator:
        await format_directory(api_generator.output_dir)

    return generated_files