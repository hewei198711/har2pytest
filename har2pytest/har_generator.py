"""HAR 文件生成器模块。

提供从 HAR 文件生成 API 接口文件的功能。
"""

import asyncio
import time
import traceback

from .config import APIConfig
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
    if not api_generator:
        return []

    har_parser = HARParser()
    requests = har_parser.extract_requests_from_har(har_file_path)

    if not requests:
        logger.info(f"HAR文件 {har_file_path} 中没有找到有效的API请求")
        return []

    logger.info(f"发现 {len(requests)} 个API请求")

    # 预取所有需要的 Swagger 文档（按 service_package 分组）
    logger.info("=" * 60)
    logger.info("[并行处理] 开始预取 Swagger 文档...")
    swagger_docs_cache = {}
    for request_info in requests:
        url = request_info["url"]
        service_package = APIConfig.determine_service_package(url)
        swagger_url = APIConfig.SWAGGER_DOC_URLS().get(service_package)
        if swagger_url and swagger_url not in swagger_docs_cache:
            doc = await api_generator.swagger_handler.get_swagger_doc(swagger_url)
            swagger_docs_cache[swagger_url] = doc
            logger.debug(f"  [预取] Swagger 文档已缓存: {swagger_url} (路径数: {len(doc.get('paths', {})) if doc else 0})")
    logger.info(f"[并行处理] Swagger 文档预取完成，缓存 {len(swagger_docs_cache)} 个文档")

    async def _process_one(request_info: dict) -> str | None:
        """异步处理单个请求，生成 API 文件。"""
        task_start = time.time()
        url = request_info.get("url", "")
        method = request_info.get("method", "")
        try:
            logger.debug(f"  [任务开始] {method} {url}")
            service_package = APIConfig.determine_service_package(url)
            swagger_url = APIConfig.SWAGGER_DOC_URLS().get(service_package)
            swagger_doc = swagger_docs_cache.get(swagger_url)
            result = await api_generator.generate_api_file(
                request_info, force_overwrite=force_overwrite, swagger_doc=swagger_doc,
            )
            elapsed = time.time() - task_start
            if result:
                logger.debug(f"  [任务完成] {method} {url} → {result} (耗时 {elapsed:.2f}s)")
            else:
                logger.debug(f"  [任务跳过] {method} {url} (耗时 {elapsed:.2f}s)")
            return result
        except Exception as e:
            elapsed = time.time() - task_start
            logger.error(f"  [任务失败] {method} {url} (耗时 {elapsed:.2f}s): {str(e)}")
            logger.error(traceback.format_exc())
            return None

    # 并行处理所有 API 请求，通过 swagger_doc 参数传参避免竞态条件
    logger.info(f"[并行处理] 开始并行处理 {len(requests)} 个 API 请求...")
    parallel_start = time.time()
    generated_files = []
    tasks = [_process_one(request_info) for request_info in requests]
    completed_count = 0
    fail_count = 0
    for coro in asyncio.as_completed(tasks):
        try:
            filepath = await coro
            if filepath:
                generated_files.append(filepath)
            else:
                fail_count += 1
        except Exception as e:
            fail_count += 1
            logger.error(f"  [并行异常] 处理请求时出错: {str(e)}")
        completed_count += 1
        if completed_count % 10 == 0 or completed_count == len(requests):
            logger.debug(f"  [并行进度] {completed_count}/{len(requests)} 已完成")
    parallel_elapsed = time.time() - parallel_start
    logger.info(f"[并行处理] 完成! 成功: {len(generated_files)}, 失败/跳过: {fail_count}, 总耗时: {parallel_elapsed:.2f}s")
    logger.info("=" * 60)

    # 批量格式化生成的 API 文件
    if generated_files and api_generator:
        await format_directory(api_generator.output_dir)

    return generated_files