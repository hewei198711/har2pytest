"""HAR 文件生成器模块。

提供从 HAR 文件生成 API 接口文件的功能。
"""

import asyncio
import time
import traceback

from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .models import ParsedRequestInfo
from .url_matcher import URLMatcher
from .utils import format_directory


def _swagger_url_for(url: str) -> str | None:
    """由 URL 推导服务包并返回其 Swagger 文档 URL（未配置则 None）。"""
    return APIConfig.SWAGGER_DOC_URLS().get(APIConfig.determine_service_package(url))


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
    logger.info("[预取] 开始加载 Swagger 文档...")
    swagger_docs_cache = {}
    for request_info in requests:
        swagger_url = _swagger_url_for(request_info.url)
        if swagger_url and swagger_url not in swagger_docs_cache:
            doc = await api_generator.swagger_handler.get_swagger_doc(swagger_url)
            swagger_docs_cache[swagger_url] = doc
            logger.debug(
                f"  [预取] Swagger 文档已缓存: {swagger_url} (路径数: {len(doc.get('paths', {})) if doc else 0})"
            )
    logger.info(f"[预取] Swagger 文档加载完成，缓存 {len(swagger_docs_cache)} 个文档")

    async def _process_one(request_info: ParsedRequestInfo, function_name_suffix: str | None = None) -> str | None:
        """异步处理单个请求，生成 API 文件。"""
        task_start = time.time()
        url = request_info.url
        method = request_info.method
        try:
            logger.debug(f"  [任务开始] {method} {url}")
            swagger_url = _swagger_url_for(url)
            swagger_doc = swagger_docs_cache.get(swagger_url)
            result = await api_generator.generate_api_file(
                request_info,
                force_overwrite=force_overwrite,
                swagger_doc=swagger_doc,
                function_name_suffix=function_name_suffix,
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

    def _target_key(request_info: ParsedRequestInfo) -> str:
        """计算请求将写入的目标标识 ``服务包/函数名``（与 generate_api_file 的取名逻辑一致）。"""
        swagger_doc = swagger_docs_cache.get(_swagger_url_for(request_info.url))
        pattern = request_info.url
        if swagger_doc:
            # 使用临时 URLMatcher 避免污染 api_generator 的共享实例状态
            temp_matcher = URLMatcher(swagger_data=swagger_doc)
            info = temp_matcher.get_url_info(request_info.url)
            pattern = info["pattern"] or request_info.url
        return f"{APIConfig.determine_service_package(pattern)}/{URLMatcher.generate_function_name(pattern)}"

    # 并行处理所有 API 请求，通过 swagger_doc 参数传参避免竞态条件
    parallel_start = time.time()
    generated_files = []
    tasks = []
    # 同一目标文件的多个请求（同 URL 不同方法、或同一模板接口的多次抓包）不能并发写同一文件，
    # 否则内容取决于完成顺序：首个沿用原名，不同方法追加方法后缀，同方法重复请求只保留首个。
    seen_targets: dict[str, tuple[str, str]] = {}
    for request_info in requests:
        target = _target_key(request_info)
        function_name_suffix = None
        if target in seen_targets:
            prev_method, prev_url = seen_targets[target]
            if prev_method.upper() == request_info.method.upper():
                logger.debug(f"  [跳过重复请求] {request_info.method} {request_info.url} 与 {prev_url} 同文件")
                continue
            function_name_suffix = request_info.method.lower()
            logger.warning(
                f"{request_info.method} {request_info.url} 与 {prev_method} {prev_url} 目标文件同名，"
                f"改用方法后缀生成: {target}_{function_name_suffix}.py"
            )
        else:
            seen_targets[target] = (request_info.method, request_info.url)
        tasks.append(_process_one(request_info, function_name_suffix))
    skipped_count = len(requests) - len(tasks)
    if skipped_count:
        logger.info(f"[并行处理] 跳过 {skipped_count} 个重复请求，实际处理 {len(tasks)} 个任务")
    logger.info(f"[并行处理] 开始并行处理 {len(tasks)} 个 API 请求...")
    completed_count = 0
    fail_count = 0
    for coro in asyncio.as_completed(tasks):
        filepath = await coro
        if filepath:
            generated_files.append(filepath)
        else:
            fail_count += 1
        completed_count += 1
        if completed_count % 10 == 0 or completed_count == len(tasks):
            logger.debug(f"  [并行进度] {completed_count}/{len(tasks)} 已完成")
    parallel_elapsed = time.time() - parallel_start
    logger.info(
        f"[并行处理] 完成! 成功: {len(generated_files)}, 失败/跳过: {fail_count}, 总耗时: {parallel_elapsed:.2f}s"
    )
    logger.info("=" * 60)

    # 批量格式化生成的 API 文件
    if generated_files:
        await format_directory(api_generator.output_dir)

    return generated_files
