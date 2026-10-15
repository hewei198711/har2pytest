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

    # 精确检查 handler 类型（FileHandler 是 StreamHandler 子类，isinstance 会误匹配）
    assert any(type(h) is logging.StreamHandler for h in logger.handlers)
    assert any(type(h) is logging.FileHandler for h in logger.handlers)
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


@allure.feature("日志模块")
@allure.story("setup_logger")
@allure.title("多次调用 setup_logger 更新日志级别并替换 handler")
def test_setup_logger_level_update_on_reconfigure(tmp_path):
    log_warn = tmp_path / "warn.log"
    setup_logger(level=logging.WARNING, log_file=str(log_warn))
    assert logger.level == logging.WARNING

    # 重新配置为 INFO 级别
    log_info = tmp_path / "info.log"
    setup_logger(level=logging.INFO, log_file=str(log_info))
    assert logger.level == logging.INFO
    logger.info("info message after reconfigure")

    content = log_info.read_text(encoding="utf-8")
    assert "info message after reconfigure" in content


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
