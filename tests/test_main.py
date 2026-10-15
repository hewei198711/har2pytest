"""测试 har2pytest.__main__ 模块中 CLI 命令分发、参数校验与各处理函数的功能与边界。"""

import json
import logging
import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

import har2pytest.__main__ as main_module

# ==================== 辅助函数 ====================


def _mock_cli_env(monkeypatch, tmp_path, argv):
    """mock 掉 CLI 启动依赖（日志配置、全局配置加载），返回不受影响的纯净环境"""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setattr(main_module, "setup_logger", MagicMock())
    monkeypatch.setattr(main_module.APIConfig, "get_config", classmethod(lambda cls, key: []))


def _tc_args(**overrides):
    defaults = dict(
        har_file="api_request.har",
        pattern="list_query",
        mark=None,
        url=None,
        output="testcases",
        api_dir="apis",
        api_files="api_request.har",
        overwrite=False,
        async_mode=False,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


# ==================== main() 命令分发测试 ====================


@allure.feature("CLI入口")
@allure.story("命令分发")
@allure.title("测试无子命令时默认执行api命令")
def test_main_default_command_api(monkeypatch, tmp_path):
    _mock_cli_env(monkeypatch, tmp_path, ["har2pytest"])
    handle_api = AsyncMock()
    monkeypatch.setattr(main_module, "handle_api", handle_api)

    main_module.main()

    handle_api.assert_called_once()
    args = handle_api.call_args[0][0]
    assert args.command == "api"
    assert args.har_file == "api_request.har"  # 默认 HAR 文件


@allure.feature("CLI入口")
@allure.story("命令分发")
@allure.title("测试api子命令参数传递")
def test_main_api_command_args(monkeypatch, tmp_path):
    output_dir = str(tmp_path / "apis")
    _mock_cli_env(monkeypatch, tmp_path, ["har2pytest", "api", "test.har", "--output", output_dir, "--overwrite"])
    handle_api = AsyncMock()
    monkeypatch.setattr(main_module, "handle_api", handle_api)

    main_module.main()

    args = handle_api.call_args[0][0]
    assert args.har_file == "test.har"
    assert args.output == output_dir
    assert args.overwrite is True


@allure.feature("CLI入口")
@allure.story("命令分发")
@allure.title("测试summary子命令分发")
def test_main_summary_command(monkeypatch, tmp_path):
    _mock_cli_env(monkeypatch, tmp_path, ["har2pytest", "summary", "test.har"])
    handle_summary = MagicMock()
    monkeypatch.setattr(main_module, "handle_summary", handle_summary)

    main_module.main()

    handle_summary.assert_called_once()
    assert handle_summary.call_args[0][0].har_file == "test.har"


@allure.feature("CLI入口")
@allure.story("命令分发")
@allure.title("测试testcase子命令分发")
def test_main_testcase_command(monkeypatch, tmp_path):
    _mock_cli_env(
        monkeypatch,
        tmp_path,
        ["har2pytest", "testcase", "test.har", "--pattern", "complex_scenario", "--url", "/api/login"],
    )
    handle_testcase = AsyncMock()
    monkeypatch.setattr(main_module, "handle_testcase", handle_testcase)

    main_module.main()

    args = handle_testcase.call_args[0][0]
    assert args.pattern == "complex_scenario"
    assert args.url == "/api/login"
    assert args.mark is None


@allure.feature("CLI入口")
@allure.story("命令分发")
@allure.title("测试swagger子命令分发")
def test_main_swagger_command(monkeypatch, tmp_path):
    _mock_cli_env(monkeypatch, tmp_path, ["har2pytest", "swagger", "https://example.com/api-docs", "--overwrite"])
    handle_swagger = AsyncMock()
    monkeypatch.setattr(main_module, "handle_swagger", handle_swagger)

    main_module.main()

    args = handle_swagger.call_args[0][0]
    assert args.swagger_url == "https://example.com/api-docs"
    assert args.overwrite is True


@allure.feature("CLI入口")
@allure.story("命令分发")
@allure.title("测试--version参数输出版本号")
def test_main_version(monkeypatch, tmp_path, capsys):
    _mock_cli_env(monkeypatch, tmp_path, ["har2pytest", "--version"])

    with pytest.raises(SystemExit):
        main_module.main()

    output = capsys.readouterr().out
    assert "har2pytest" in output


@allure.feature("CLI入口")
@allure.story("命令分发")
@allure.title("测试未知子命令报错退出")
def test_main_unknown_command(monkeypatch, tmp_path):
    _mock_cli_env(monkeypatch, tmp_path, ["har2pytest", "foobar"])

    with pytest.raises(SystemExit):
        main_module.main()


@allure.feature("CLI入口")
@allure.story("testcase参数校验")
@allure.title("测试list_query模式缺少url参数时拒绝执行")
async def test_handle_testcase_list_query_missing_url(caplog):
    caplog.set_level(logging.ERROR, logger="har2pytest")

    result = await main_module.handle_testcase(_tc_args(pattern="list_query", url=None))

    assert result is None
    assert "必须指定 --url 参数" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase参数校验")
@allure.title("测试complex_scenario模式缺少url参数时拒绝执行")
async def test_handle_testcase_complex_missing_url(caplog):
    caplog.set_level(logging.ERROR, logger="har2pytest")

    result = await main_module.handle_testcase(_tc_args(pattern="complex_scenario", url=None))

    assert result is None
    assert "必须指定 --url 参数" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase参数校验")
@allure.title("测试batch模式缺少api-files参数时拒绝执行")
async def test_handle_testcase_batch_missing_api_files(caplog):
    caplog.set_level(logging.ERROR, logger="har2pytest")

    result = await main_module.handle_testcase(_tc_args(pattern="batch", api_files=""))

    assert result is None
    assert "必须指定 --api-files 参数" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase参数校验")
@allure.title("测试list_query模式har_file为空时拒绝执行")
async def test_handle_testcase_list_query_empty_har(caplog):
    caplog.set_level(logging.ERROR, logger="har2pytest")

    result = await main_module.handle_testcase(_tc_args(pattern="list_query", har_file="", url="/api/test"))

    assert result is None
    assert "必须指定 HAR 文件" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase参数校验")
@allure.title("测试batch模式空HAR文件导致无有效API文件时拒绝执行")
async def test_handle_testcase_batch_empty_har_no_valid_files(tmp_path, caplog):
    caplog.set_level(logging.ERROR, logger="har2pytest")
    empty_har = tmp_path / "empty.har"
    empty_har.write_text(json.dumps({"log": {"entries": []}}), encoding="utf-8")

    result = await main_module.handle_testcase(
        _tc_args(pattern="batch", api_files=str(empty_har))
    )

    assert result is None
    assert "没有找到有效的 API 文件" in caplog.text


# ==================== handle_testcase 成功场景测试 ====================


@allure.feature("CLI入口")
@allure.story("testcase命令处理")
@allure.title("测试list_query模式成功生成测试用例")
async def test_handle_testcase_list_query_success(monkeypatch, caplog):
    caplog.set_level(logging.INFO, logger="har2pytest")
    generator_instance = MagicMock()
    generator_instance.swagger_handler.close = AsyncMock()
    generator_instance.generate_parametrized_list_testcases = AsyncMock(return_value=["test_user_list.py"])
    monkeypatch.setattr(main_module, "TestCaseGenerator", MagicMock(return_value=generator_instance))

    args = _tc_args(pattern="list_query", url="/api/user/list", mark="test_4291")
    await main_module.handle_testcase(args)

    generator_instance.generate_parametrized_list_testcases.assert_awaited_once_with(
        "api_request.har", "test_4291", "/api/user/list", overwrite=False
    )
    assert "成功生成 1 个测试用例文件" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase命令处理")
@allure.title("测试list_query模式未生成文件时提示")
async def test_handle_testcase_list_query_no_files(monkeypatch, caplog):
    caplog.set_level(logging.INFO, logger="har2pytest")
    generator_instance = MagicMock()
    generator_instance.swagger_handler.close = AsyncMock()
    generator_instance.generate_parametrized_list_testcases = AsyncMock(return_value=[])
    monkeypatch.setattr(main_module, "TestCaseGenerator", MagicMock(return_value=generator_instance))

    args = _tc_args(pattern="list_query", url="/api/user/list", overwrite=True)
    await main_module.handle_testcase(args)

    assert "未生成新的测试用例文件" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase参数校验")
@allure.title("测试--mark非合法标识符时拒绝执行")
async def test_handle_testcase_invalid_mark(caplog):
    caplog.set_level(logging.ERROR, logger="har2pytest")

    result = await main_module.handle_testcase(_tc_args(mark="2025-01-01", url="/api/test"))

    assert result is None
    assert "--mark 必须是合法的 Python 标识符" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase命令处理")
@allure.title("测试complex_scenario模式成功生成测试用例")
async def test_handle_testcase_complex_success(monkeypatch, caplog):
    caplog.set_level(logging.INFO, logger="har2pytest")
    generator_instance = MagicMock()
    generator_instance.swagger_handler.close = AsyncMock()
    generator_instance.generate_scenario_testcase = AsyncMock(return_value="testcases/test_login.py")
    monkeypatch.setattr(main_module, "TestCaseGenerator", MagicMock(return_value=generator_instance))

    args = _tc_args(pattern="complex_scenario", url="/api/login", mark="test_4295")
    await main_module.handle_testcase(args)

    generator_instance.generate_scenario_testcase.assert_awaited_once_with(
        "api_request.har", "/api/login", "test_4295", overwrite=False
    )
    assert "成功生成测试用例文件" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase命令处理")
@allure.title("测试complex_scenario模式未生成文件时提示")
async def test_handle_testcase_complex_no_files(monkeypatch, caplog):
    caplog.set_level(logging.INFO, logger="har2pytest")
    generator_instance = MagicMock()
    generator_instance.swagger_handler.close = AsyncMock()
    generator_instance.generate_scenario_testcase = AsyncMock(return_value=None)
    monkeypatch.setattr(main_module, "TestCaseGenerator", MagicMock(return_value=generator_instance))

    args = _tc_args(pattern="complex_scenario", url="/api/login")
    await main_module.handle_testcase(args)

    assert "未生成新的测试用例文件" in caplog.text


@allure.feature("CLI入口")
@allure.story("testcase命令处理")
@allure.title("测试batch模式成功批量生成测试用例")
async def test_handle_testcase_batch_success(monkeypatch, caplog):
    caplog.set_level(logging.INFO, logger="har2pytest")
    generator_instance = MagicMock()
    generator_instance.swagger_handler.close = AsyncMock()
    generator_instance.generate_batch_testcases = AsyncMock(
        return_value={"total": 2, "skipped": 0, "generated": 2, "failed": 0, "generated_files": ["a.py", "b.py"]}
    )
    monkeypatch.setattr(main_module, "TestCaseGenerator", MagicMock(return_value=generator_instance))

    args = _tc_args(pattern="batch", api_files="api1.py,api2.py", mark="test_4295")
    await main_module.handle_testcase(args)

    generator_instance.generate_batch_testcases.assert_awaited_once_with(
        ["api1.py", "api2.py"], "test_4295", overwrite=False, har_file_path=None
    )
    assert "总API文件数: 2" in caplog.text
    assert "成功生成: 2" in caplog.text


# ==================== handle_* 命令处理函数测试 ====================


@allure.feature("CLI入口")
@allure.story("命令处理函数")
@allure.title("测试handle_api生成API文件")
async def test_handle_api(monkeypatch, tmp_path):
    api_generator = MagicMock()
    api_generator.swagger_handler.close = AsyncMock()
    monkeypatch.setattr(main_module, "APIGenerator", MagicMock(return_value=api_generator))
    monkeypatch.setattr(
        main_module,
        "generate_api_files_from_har",
        AsyncMock(return_value=["apis/a.py", "apis/b.py"]),
    )

    args = SimpleNamespace(har_file="test.har", output=str(tmp_path / "apis"), overwrite=True)
    await main_module.handle_api(args)

    main_module.generate_api_files_from_har.assert_awaited_once_with(
        "test.har", force_overwrite=True, api_generator=api_generator
    )
    api_generator.generate_index_file.assert_called_once_with(["apis/a.py", "apis/b.py"])


@allure.feature("CLI入口")
@allure.story("命令处理函数")
@allure.title("测试handle_api未生成文件时不生成索引")
async def test_handle_api_no_files(monkeypatch, tmp_path):
    api_generator = MagicMock()
    api_generator.swagger_handler.close = AsyncMock()
    monkeypatch.setattr(main_module, "APIGenerator", MagicMock(return_value=api_generator))
    monkeypatch.setattr(
        main_module,
        "generate_api_files_from_har",
        AsyncMock(return_value=[]),
    )

    args = SimpleNamespace(har_file="test.har", output=str(tmp_path / "apis"), overwrite=False)
    await main_module.handle_api(args)

    api_generator.generate_index_file.assert_not_called()


@allure.feature("CLI入口")
@allure.story("命令处理函数")
@allure.title("测试handle_summary打印HAR摘要")
def test_handle_summary(monkeypatch):
    parser_instance = MagicMock()
    monkeypatch.setattr(main_module, "HARParser", MagicMock(return_value=parser_instance))

    args = SimpleNamespace(har_file="test.har")
    main_module.handle_summary(args)

    parser_instance.print_api_summary.assert_called_once_with("test.har")


@allure.feature("CLI入口")
@allure.story("命令处理函数")
@allure.title("测试handle_swagger生成API文件及索引条件")
@pytest.mark.parametrize(
    "generated,overwrite,path,expect_index",
    [
        ([], True, None, False),
        (["apis/swagger_api.py"], False, "/pet/{petId}", True),
    ],
    ids=["no_files_no_index", "with_files_with_index"],
)
async def test_handle_swagger(monkeypatch, tmp_path, generated, overwrite, path, expect_index):
    api_generator = MagicMock()
    api_generator.swagger_handler.close = AsyncMock()
    api_generator.generate_apis_from_swagger = AsyncMock(return_value=generated)
    monkeypatch.setattr(main_module, "APIGenerator", MagicMock(return_value=api_generator))

    args = SimpleNamespace(
        swagger_url="https://example.com/api-docs",
        output=str(tmp_path / "apis"),
        overwrite=overwrite,
        path=path,
    )
    await main_module.handle_swagger(args)

    api_generator.generate_apis_from_swagger.assert_awaited_once_with(
        "https://example.com/api-docs", overwrite, path
    )
    if expect_index:
        api_generator.generate_index_file.assert_called_once_with(generated)
    else:
        api_generator.generate_index_file.assert_not_called()
