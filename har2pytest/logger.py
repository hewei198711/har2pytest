"""
日志模块

作为库使用时，默认只添加 NullHandler，不污染调用方的日志配置。
CLI 入口（__main__.py）会在启动时调用 setup_logger() 激活控制台和文件输出。
"""

import logging
import os

# 创建日志记录器，默认添加 NullHandler（库标准做法，避免 "No handler found" 警告）
logger = logging.getLogger("har2pytest")
logger.addHandler(logging.NullHandler())

# 格式化器（模块级复用，setup_logger 共用）
_FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)


def setup_logger(level: int = logging.INFO, log_file: str | None = None) -> None:
    """配置日志记录器，添加控制台和文件输出。

    仅应在 CLI 入口或应用程序启动时调用一次。
    重复调用会先清除已有 handler 再重新配置，避免重复输出。

    Args:
        level: 日志级别，默认 INFO。
        log_file: 日志文件路径，默认写入当前工作目录下的 har2pytest.log。
    """
    # 清除已有 handler（包括 NullHandler），避免重复添加
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)

    logger.setLevel(level)

    # 控制台输出
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(_FORMATTER)
    logger.addHandler(stream_handler)

    # 文件输出
    if log_file is None:
        log_file = os.path.join(os.getcwd(), "har2pytest.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(_FORMATTER)
    logger.addHandler(file_handler)
