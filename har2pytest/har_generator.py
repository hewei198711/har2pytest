"""HAR 文件生成器模块。

提供从 HAR 文件生成 API 接口文件的功能。
"""

import asyncio
import json
import time
import traceback
from typing import Any

from .config import APIConfig
from .har_parser import HARParser
from .logger import logger
from .models import ParsedRequestInfo
from .param_builder import normalize_params_for_parametrization
from .url_matcher import URLMatcher
from .utils import format_directory, merge_request_params


def _compute_constant_params(snapshots: list[dict]) -> dict[str, Any]:
    """从请求快照中识别常量参数。

    常量参数定义：在超过 50% 的请求中都出现、且值都相同的参数。

    Args:
        snapshots: 同一接口的所有请求参数快照列表

    Returns:
        常量参数字典（参数名 → 固定值）
    """
    if not snapshots:
        return {}
    total = len(snapshots)
    threshold = total * 0.5

    def _hashable(value: Any) -> Any:
        """将不可哈希的值（如 list/dict）转为 JSON 字符串用于统计。"""
        if isinstance(value, (list, dict)):
            return json.dumps(value, sort_keys=True, ensure_ascii=False)
        return value

    # 统计每个参数的值分布（key 为可哈希表示，value 为 (原始值, 计数)）
    param_value_counts: dict[str, dict[Any, tuple[Any, int]]] = {}
    for snap in snapshots:
        for key, value in snap.items():
            h = _hashable(value)
            bucket = param_value_counts.setdefault(key, {})
            if h in bucket:
                orig, cnt = bucket[h]
                bucket[h] = (orig, cnt + 1)
            else:
                bucket[h] = (value, 1)
    # 筛选常量参数：>50% 请求都有且值相同，排除空值（""、None）
    constant: dict[str, Any] = {}
    for param_name, hash_counts in param_value_counts.items():
        if len(hash_counts) == 1:
            _h, (orig_value, count) = next(iter(hash_counts.items()))
            if count > threshold and orig_value not in ("", None):
                constant[param_name] = orig_value
    return constant


def _compute_har_param_values(snapshots: list[dict], constant_params: dict[str, Any]) -> dict[str, list[Any]]:
    """从请求快照中计算参数化结构（含组合参数），写入 api.json。

    直接复用 ``normalize_params_for_parametrization`` 的参数化逻辑，确保
    api.json 中的 ``har_param_values`` 与实际测试生成时的参数化结构一致：

    - 单参数：``{"orderTypes": ["1", "2", "3"]}``
    - 组合参数：``{"header,orderTypes": [("1","1"), ("1","2"), ...]}``
      （JSON 中 tuple 序列化为 array，读取时按组合键还原）
    - 单参数：全部收录（即使只有 1 个值，也保留以便测试用例直接读取 api.json）
    - 组合参数：始终收录（即使只有 1 个值，也保留参数关联结构）
    - 常量/分页/时间参数已在上游过滤

    Args:
        snapshots: 同一接口的所有请求参数快照列表
        constant_params: 常量参数字典

    Returns:
        参数枚举值字典（参数名 → 值列表，组合键 → 元组列表）
    """
    param_items = normalize_params_for_parametrization(snapshots, constant_params)
    result: dict[str, list[Any]] = {}
    for item in param_items:
        name = item["param_name"]
        values = item[name]
        is_combo = "," in name
        # 全量收录：单参数和组合参数都保留，测试用例生成时直接读取 api.json
        if is_combo:
            # 组合参数：每个值转为 tuple（语义：定长、不可变的参数组合）
            result[name] = [tuple(v) for v in values]
        else:
            result[name] = values
    return result


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
    # 一次全量解析，后续分别在内存中做去重（生成 API 文件）和全量统计（常量参数）
    all_requests = har_parser.extract_requests_from_har(har_file_path, filter_duplicate_url=False)

    if not all_requests:
        logger.info(f"HAR文件 {har_file_path} 中没有找到有效的API请求")
        return []

    logger.info(f"发现 {len(all_requests)} 个API请求（含重复）")

    # 收集所有请求的参数快照（不去重，保留参数变化），用于识别常量参数
    snapshots_by_url: dict[str, list[dict]] = {}
    for req in all_requests:
        url_key = URLMatcher.normalize_url(req.url)
        params = merge_request_params(req)
        if isinstance(params, dict) and params:
            snapshots_by_url.setdefault(url_key, []).append(params)

    # 内存去重：同 method+url 只保留第一个（与 HARParser 的去重逻辑一致）
    seen_urls: set[str] = set()
    requests: list[ParsedRequestInfo] = []
    for req in all_requests:
        url_key = f"{req.method}:{req.url}"
        if url_key in seen_urls:
            continue
        seen_urls.add(url_key)
        requests.append(req)
    # 按 URL 计算常量参数和 HAR 参数枚举值
    constant_params_by_url: dict[str, dict[str, Any]] = {}
    har_param_values_by_url: dict[str, dict[str, list[Any]]] = {}
    for url_key, snaps in snapshots_by_url.items():
        # --overwrite 时整文件覆盖：constant_params 随 HAR 数据重新计算，不复用旧值
        cp = _compute_constant_params(snaps)
        if cp:
            constant_params_by_url[url_key] = cp
        hpv = _compute_har_param_values(snaps, cp or {})
        if hpv:
            har_param_values_by_url[url_key] = hpv
    if constant_params_by_url:
        logger.debug(f"[常量参数] 覆盖 {len(constant_params_by_url)} 个接口")
    if har_param_values_by_url:
        logger.debug(f"[HAR参数枚举值] 覆盖 {len(har_param_values_by_url)} 个接口")

    # 预取所有需要的 Swagger 文档（按 service_package 分组）
    logger.info("=" * 60)
    logger.info("[预取] 开始加载 Swagger 文档...")
    swagger_docs_cache = {}
    url_to_swagger_url: dict[str, str | None] = {}  # 缓存 url → swagger_url 映射
    for request_info in requests:
        swagger_url = _swagger_url_for(request_info.url)
        url_to_swagger_url[request_info.url] = swagger_url
        if swagger_url and swagger_url not in swagger_docs_cache:
            doc = await api_generator.swagger_handler.get_swagger_doc(swagger_url)
            swagger_docs_cache[swagger_url] = doc
            logger.debug(
                f"  [预取] Swagger 文档已缓存: {swagger_url} (路径数: {len(doc.get('paths', {})) if doc else 0})"
            )
    logger.info(f"[预取] Swagger 文档加载完成，缓存 {len(swagger_docs_cache)} 个文档")

    async def _process_one(
        request_info: ParsedRequestInfo,
        function_name_suffix: str | None = None,
        constant_params: dict[str, Any] | None = None,
        har_param_values: dict[str, list[Any]] | None = None,
    ) -> str | None:
        """异步处理单个请求，生成 API 文件。"""
        task_start = time.time()
        url = request_info.url
        method = request_info.method
        try:
            logger.debug(f"  [任务开始] {method} {url}")
            swagger_url = url_to_swagger_url.get(url)
            swagger_doc = swagger_docs_cache.get(swagger_url) if swagger_url else None
            result = await api_generator.generate_api_file(
                request_info,
                force_overwrite=force_overwrite,
                swagger_doc=swagger_doc,
                function_name_suffix=function_name_suffix,
                constant_params=constant_params,
                har_param_values=har_param_values,
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
        swagger_url = url_to_swagger_url.get(request_info.url)
        swagger_doc = swagger_docs_cache.get(swagger_url) if swagger_url else None
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
        tasks.append(_process_one(
            request_info,
            function_name_suffix,
            constant_params_by_url.get(request_info.url),
            har_param_values_by_url.get(request_info.url),
        ))
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
