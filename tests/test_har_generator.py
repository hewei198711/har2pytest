"""
测试 har_generator.py 模块
"""

import asyncio
import json
import os
from unittest.mock import AsyncMock, MagicMock

import allure

from har2pytest.har_generator import generate_api_files_from_har


@allure.feature("HAR生成器")
@allure.story("生成API文件")
def test_generate_api_files_from_har():
    """测试从HAR文件生成API文件"""
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

    with open("test_har_generator.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        # 创建mock的api_generator
        mock_api_generator = MagicMock()
        mock_api_generator.generate_api_file = AsyncMock(return_value="api/_user_login.py")

        generated_files = asyncio.run(generate_api_files_from_har("test_har_generator.har", api_generator=mock_api_generator))

        assert len(generated_files) == 1
        assert generated_files[0] == "api/_user_login.py"
        mock_api_generator.generate_api_file.assert_called_once()
    finally:
        if os.path.exists("test_har_generator.har"):
            os.remove("test_har_generator.har")


@allure.feature("HAR生成器")
@allure.story("空HAR文件")
def test_generate_api_files_from_empty_har():
    """测试空HAR文件的情况"""
    test_har = {"log": {"entries": []}}

    with open("test_empty_har.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        generated_files = asyncio.run(generate_api_files_from_har("test_empty_har.har"))

        assert len(generated_files) == 0
    finally:
        if os.path.exists("test_empty_har.har"):
            os.remove("test_empty_har.har")


@allure.feature("HAR生成器")
@allure.story("生成API文件失败")
def test_generate_api_files_failure():
    """测试生成API文件失败的情况"""
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

    with open("test_failure.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        # 创建会抛出异常的mock
        mock_api_generator = MagicMock()
        mock_api_generator.generate_api_file = AsyncMock(side_effect=Exception("生成失败"))

        generated_files = asyncio.run(generate_api_files_from_har("test_failure.har", api_generator=mock_api_generator))

        # 即使单个生成失败，也应该返回空列表（不抛出异常）
        assert len(generated_files) == 0
    finally:
        if os.path.exists("test_failure.har"):
            os.remove("test_failure.har")


@allure.feature("HAR生成器")
@allure.story("不存在的HAR文件")
def test_generate_api_files_nonexistent_har():
    """测试不存在的HAR文件"""
    generated_files = asyncio.run(generate_api_files_from_har("nonexistent.har"))

    assert len(generated_files) == 0
