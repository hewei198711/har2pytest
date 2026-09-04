"""
测试 har_generator.py 模块
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock

import allure

from har2pytest.har_generator import generate_api_files_from_har


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试从HAR文件生成API文件")
def test_generate_api_files_from_har(tmp_path):
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://example.com/api/user/login",
                        "method": "POST",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "postData": {"mimeType": "application/json", "text": '{"username": "test"}'},
                    },
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 100,
                }
            ]
        }
    }

    har_path = tmp_path / "test_har_generator.har"
    har_path.write_text(json.dumps(test_har, ensure_ascii=False), encoding="utf-8")

    mock_api_generator = MagicMock()
    mock_api_generator.generate_api_file = AsyncMock(return_value="api/_user_login.py")

    generated_files = asyncio.run(generate_api_files_from_har(str(har_path), api_generator=mock_api_generator))

    assert len(generated_files) == 1
    assert generated_files[0] == "api/_user_login.py"
    mock_api_generator.generate_api_file.assert_called_once()


@allure.feature("HAR生成器")
@allure.story("空HAR文件")
@allure.title("测试空HAR文件的情况")
def test_generate_api_files_from_empty_har(tmp_path):
    test_har = {"log": {"entries": []}}

    har_path = tmp_path / "test_empty_har.har"
    har_path.write_text(json.dumps(test_har, ensure_ascii=False), encoding="utf-8")

    mock_api_generator = MagicMock()
    mock_api_generator.generate_api_file = AsyncMock(return_value=None)

    generated_files = asyncio.run(generate_api_files_from_har(str(har_path), api_generator=mock_api_generator))

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("生成API文件失败")
@allure.title("测试生成API文件失败的情况")
def test_generate_api_files_failure(tmp_path):
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {"url": "https://example.com/api/test", "method": "GET", "headers": []},
                    "response": {"status": 200, "content": {"text": "{}"}},
                    "time": 50,
                }
            ]
        }
    }

    har_path = tmp_path / "test_failure.har"
    har_path.write_text(json.dumps(test_har, ensure_ascii=False), encoding="utf-8")

    mock_api_generator = MagicMock()
    mock_api_generator.generate_api_file = AsyncMock(side_effect=Exception("生成失败"))

    generated_files = asyncio.run(generate_api_files_from_har(str(har_path), api_generator=mock_api_generator))

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("不存在的HAR文件")
@allure.title("测试不存在的HAR文件")
def test_generate_api_files_nonexistent_har():
    mock_api_generator = MagicMock()
    mock_api_generator.generate_api_file = AsyncMock(return_value=None)

    generated_files = asyncio.run(generate_api_files_from_har("nonexistent.har", api_generator=mock_api_generator))

    assert len(generated_files) == 0
