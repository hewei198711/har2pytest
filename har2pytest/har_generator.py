# coding:utf-8

import traceback
from typing import List
from .har_parser import HARParser
from .logger import logger


class HARGenerator:
    """HAR文件生成器类"""

    def __init__(self, output_dir: str = None, api_generator=None):
        """
        初始化HAR生成器

        Args:
            output_dir: API文件输出目录
            api_generator: API生成器实例
        """
        self.output_dir = output_dir
        self.api_generator = api_generator
        self.har_parser = HARParser()

    def generate_api_files_from_har(self, har_file_path: str, force_overwrite: bool = False) -> List[str]:
        """
        从HAR文件生成所有API接口文件

        解析HAR文件中的所有请求，为每个请求生成对应的API接口文件

        Args:
            har_file_path: HAR文件路径，如 "api_request.har"
            force_overwrite: 是否覆盖已存在的文件

        Returns:
            List[str]: 生成的文件路径列表

        Example:
            files = generator.generate_api_files_from_har("普通订单.har")
            # 返回生成的文件路径列表，如 ["api/_mobile_product_search.py", "api/_mobile_trade_orderCommit.py"]
        """
        requests = self.har_parser.extract_requests_from_har(har_file_path)

        if not requests:
            logger.info(f"HAR文件 {har_file_path} 中没有找到有效的API请求")
            return []

        logger.info(f"发现 {len(requests)} 个API请求")

        generated_files = []
        for request_info in requests:
            try:
                if self.api_generator:
                    filepath = self.api_generator.generate_api_file(request_info, force_overwrite=force_overwrite)
                    if filepath:
                        generated_files.append(filepath)
            except Exception as e:
                logger.error(f"生成API文件失败: {str(e)}")
                logger.error(traceback.format_exc())

        return generated_files