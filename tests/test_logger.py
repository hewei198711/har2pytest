"""测试 har2pytest.logger 模块中日志器初始化、handler 配置、日志级别与文件输出的功能与边界。"""

import logging

import allure
import pytest

from har2pytest.logger import logger, setup_logger

# ==================== Fixtures ====================


@pytest.fixture(autouse=True)
def reset_logger_state():
    """测试后恢复 logger 默认状态（仅 NullHandler），避免污染其他测试"""
    original_level = logger.level
    yield
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    logger.setLevel(original_level)
    logger.addHandler(logging.NullHandler())


# ==================== setup_logger 测试 ====================


@allure.feature("日志模块")
@allure.story("setup_logger")
@allure.title("测试默认配置添加控制台与文件handler")
def test_setup_logger_default_handlers(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    setup_logger()

    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    assert not any(isinstance(h, logging.NullHandler) for h in logger.handlers)
    # 默认日志文件写入当前工作目录
    assert (tmp_path / "har2pytest.log").exists()


@allure.feature("日志模块")
@allure.story("setup_logger")
@allure.title("测试日志级别设置")
def test_setup_logger_level(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    setup_logger(level=logging.DEBUG)
    assert logger.level == logging.DEBUG


@allure.feature("日志模块")
@allure.story("setup_logger")
@allure.title("测试自定义日志文件写入")
def test_setup_logger_custom_log_file(tmp_path):
    log_file = tmp_path / "custom.log"
    setup_logger(log_file=str(log_file))
    logger.info("hello logger test")

    content = log_file.read_text(encoding="utf-8")
    assert "hello logger test" in content
    # 格式化器包含时间、级别、文件名行号等字段
    assert "INFO" in content
    assert "test_logger.py" in content


@allure.feature("日志模块")
@allure.story("setup_logger")
@allure.title("测试重复调用不重复添加handler")
def test_setup_logger_idempotent(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    setup_logger()
    setup_logger()

    # 第二次调用先清除旧 handler 再重新配置，总数为 1 控制台 + 1 文件
    assert len(logger.handlers) == 2


# ==================== 库模式默认行为测试 ====================


@allure.feature("日志模块")
@allure.story("库模式默认行为")
@allure.title("库导入时仅挂载 NullHandler，不产生任何日志输出")
def test_default_library_mode_null_handler_only():
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.NullHandler)


@allure.feature("日志模块")
@allure.story("setup_logger")
@allure.title("WARNING 级别过滤：低于阈值的 INFO 消息不输出")
def test_warning_level_filters_info(tmp_path):
    log_file = tmp_path / "warn.log"
    setup_logger(level=logging.WARNING, log_file=str(log_file))
    logger.info("should not appear")
    logger.warning("should appear")

    content = log_file.read_text(encoding="utf-8")
    assert "should not appear" not in content
    assert "should appear" in content
