"""
日志模块
"""

import logging
import os

# 日志文件默认写入当前工作目录，避免在 pip 安装后路径失效
_log_dir = os.getcwd()
_log_file = os.path.join(_log_dir, "har2pytest.log")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_log_file, encoding="utf-8"),
    ],
)

# 创建日志记录器
logger = logging.getLogger("har2pytest")


# 导出logger
def get_logger():
    """
    获取日志记录器
    """
    return logger


def reset_log_file():
    """重新设置日志文件路径为当前工作目录。"""
    global _log_dir, _log_file
    _log_dir = os.getcwd()
    _log_file = os.path.join(_log_dir, "har2pytest.log")
    for handler in list(logger.handlers):
        if isinstance(handler, logging.FileHandler):
            handler.close()
            logger.removeHandler(handler)
    logger.addHandler(logging.FileHandler(_log_file, encoding="utf-8"))
