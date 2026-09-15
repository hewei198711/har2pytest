"""测试 har2pytest.har_generator 模块中 HAR 文件解析与 API 接口文件异步生成的功能与边界。"""

import json
import logging
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from har2pytest.api_generator import APIGenerator
from har2pytest.har_generator import generate_api_files_from_har

# ==================== Fixtures ====================


@pytest.fixture
def mock_generator():
    """工厂 fixture：返回一个可配置 return_value / side_effect 的 mock API 生成器。"""
    def _create(return_value=None, side_effect=None):
        gen = MagicMock()
        gen.generate_api_file = AsyncMock(return_value=return_value, side_effect=side_effect)
        return gen
    return _create


@pytest.fixture
def write_har(tmp_path):
    """工厂 fixture：将 entries 列表写入临时 HAR 文件并返回路径。"""
    def _write(entries, filename="test.har"):
        har_data = {"log": {"entries": entries}}
        har_path = tmp_path / filename
        har_path.write_text(json.dumps(har_data, ensure_ascii=False), encoding="utf-8")
        return har_path
    return _write


# ==================== Mock API 生成测试 ====================


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试从HAR文件生成API文件")
async def test_generate_api_files_from_har(write_har, mock_generator):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/user/login",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/json"}],
            "postData": {"mimeType": "application/json", "text": '{"username": "test"}'},
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 100,
    }])

    gen = mock_generator(return_value="api/_user_login.py")
    generated_files = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert len(generated_files) == 1
    assert generated_files[0] == "api/_user_login.py"
    gen.generate_api_file.assert_called_once()


@allure.feature("HAR生成器")
@allure.story("空HAR文件")
@allure.title("测试空HAR文件的情况")
async def test_generate_api_files_from_empty_har(write_har, mock_generator):
    har_path = write_har([])
    gen = mock_generator()

    generated_files = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("生成API文件失败")
@allure.title("测试生成API文件失败的情况")
async def test_generate_api_files_failure(write_har, mock_generator):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {"url": "https://example.com/api/test", "method": "GET", "headers": []},
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 50,
    }])
    gen = mock_generator(side_effect=Exception("生成失败"))

    generated_files = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("不存在的HAR文件")
@allure.title("测试不存在的HAR文件")
async def test_generate_api_files_nonexistent_har(mock_generator):
    gen = mock_generator()

    generated_files = await generate_api_files_from_har("nonexistent.har", api_generator=gen)

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("边界条件")
@allure.title("测试 api_generator 为 None 时直接返回空列表")
async def test_generate_api_files_no_generator():
    result = await generate_api_files_from_har("any.har", api_generator=None)
    assert result == []


@allure.feature("HAR生成器")
@allure.story("边界条件")
@allure.title("测试 HAR 文件缺少 log 键时返回空列表")
async def test_generate_api_files_har_missing_log_key(tmp_path, mock_generator):
    bad_har = tmp_path / "bad_structure.har"
    bad_har.write_text(json.dumps({"not_log": {}}), encoding="utf-8")
    gen = mock_generator()

    result = await generate_api_files_from_har(str(bad_har), api_generator=gen)

    assert result == []


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试 generate_api_file 返回 None 时记录任务跳过日志")
async def test_generate_api_files_process_returns_none(write_har, mock_generator, caplog):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {"url": "https://example.com/api/test", "method": "GET", "headers": []},
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 10,
    }])
    gen = mock_generator(return_value=None)

    with caplog.at_level(logging.DEBUG, logger="har2pytest"):
        result = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert result == []
    assert "任务跳过" in caplog.text


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试同URL不同方法生成两个文件而不是互相覆盖")
@allure.description("HAR 里同一个 URL 既有 POST 又有 PUT 时，不能并发写同一个文件互相覆盖")
async def test_generate_api_files_same_url_multi_method(tmp_path):

    def entry(method, body):
        return {
            "_resourceType": "xhr",
            "request": {
                "url": "https://example.com/appStore/role",
                "method": method,
                "headers": [{"name": "Content-Type", "value": "application/json"}],
                "postData": {"mimeType": "application/json", "text": body},
            },
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 20,
        }

    test_har = {"log": {"entries": [entry("POST", '{"roleName": "a"}'), entry("PUT", '{"roleName": "b"}')]}}
    har_path = tmp_path / "role.har"
    har_path.write_text(json.dumps(test_har, ensure_ascii=False), encoding="utf-8")

    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    files = await generate_api_files_from_har(str(har_path), force_overwrite=True, api_generator=generator)

    names = sorted(os.path.basename(f) for f in files)
    assert len(names) == 2
    assert any(n.endswith("role.py") for n in names)
    assert any(n.endswith("role_put.py") for n in names)

    contents = {os.path.basename(f): Path(f).read_text(encoding="utf-8") for f in files}
    plain = next(v for k, v in contents.items() if k.endswith("role.py"))
    suffixed = contents[next(k for k in contents if k.endswith("role_put.py"))]
    assert "client.post(" in plain
    assert "client.put(" in suffixed


# ==================== 集成场景测试 ====================


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试同一模板接口的重复抓包只生成一次")
@allure.description("同一 URL 的多个同方法请求（如重复抓包）只生成一个文件，避免覆盖内容不确定")
async def test_generate_api_files_duplicate_request_skipped(tmp_path, caplog):

    def entry():
        return {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/user/info", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 10,
        }

    test_har = {"log": {"entries": [entry(), entry(), entry()]}}
    har_path = tmp_path / "dup.har"
    har_path.write_text(json.dumps(test_har, ensure_ascii=False), encoding="utf-8")

    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    with caplog.at_level(logging.DEBUG, logger="har2pytest"):
        files = await generate_api_files_from_har(str(har_path), force_overwrite=True, api_generator=generator)

    assert len(files) == 1
    assert "跳过" in caplog.text
