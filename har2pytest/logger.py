# coding:utf-8
"""
日志模块
"""

import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'har2pytest.log'), encoding='utf-8')
    ]
)

# 创建日志记录器
logger = logging.getLogger('har2pytest')

# 导出logger
def get_logger():
    """
    获取日志记录器
    """
    return logger
