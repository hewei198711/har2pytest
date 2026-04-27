# coding:utf-8
"""
测试 har_parser.py 模块
"""

import pytest
import allure
import json
import os
from har2pytest.har_parser import HARParser


@allure.feature("HAR解析器")
@allure.story("提取请求信息")
def test_extract_requests_from_har():
    """测试从HAR文件提取请求信息"""
    from har2pytest.config import APIConfig

    # 触发配置初始化
    APIConfig.get_config('BASE_URLS')

    # 临时设置 BASE_URLS 配置
    original_base_urls = APIConfig._config.get('BASE_URLS', [])
    APIConfig._config['BASE_URLS'] = ["https://uc-test.perfect99.com/api"]

    # 创建测试HAR文件
    test_har = {
        "log": {
            "entries": [
                {
                    "_resourceType": "xhr",
                    "request": {
                        "url": "https://uc-test.perfect99.com/api/user/login",
                        "method": "POST",
                        "headers": [
                            {"name": "Content-Type", "value": "application/json"}
                        ],
                        "postData": {
                            "mimeType": "application/json",
                            "text": '{"username": "test", "password": "123456"}'
                        }
                    },
                    "response": {
                        "status": 200,
                        "content": {
                            "text": '{"code": 0, "message": "success"}'
                        }
                    },
                    "time": 100
                }
            ]
        }
    }

    with open("test.har", "w", encoding="utf-8") as f:
        json.dump(test_har, f)

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("test.har")

        assert len(requests) == 1
        assert requests[0]["method"] == "POST"
        assert requests[0]["url"] == "/user/login"
        assert requests[0]["response_status"] == 200
    finally:
        # 恢复原始配置
        APIConfig._config['BASE_URLS'] = original_base_urls

        if os.path.exists("test.har"):
            os.remove("test.har")


@allure.feature("HAR解析器")
@allure.story("过滤无效参数")
def test_filter_invalid_params():
    """测试过滤无效参数"""
    from har2pytest.config import APIConfig

    # 触发配置初始化
    APIConfig.get_config('INVALID_PARAMS')

    # 临时设置 INVALID_PARAMS 配置
    original_invalid_params = APIConfig._config.get('INVALID_PARAMS', set())
    APIConfig._config['INVALID_PARAMS'] = {"sign", "timestamp"}

    try:
        parser = HARParser()

        test_data = {
            "username": "test",
            "password": "123456",
            "sign": "test_sign",  # 无效参数
            "timestamp": "1234567890",  # 无效参数
            "file": "test.txt"  # 现在应该保留file参数
        }

        result = parser._filter_invalid_params(test_data)
        assert "username" in result
        assert "password" in result
        assert "sign" not in result
        assert "timestamp" not in result
        assert "file" in result  # 确保file参数被保留
    finally:
        # 恢复原始配置
        APIConfig._config['INVALID_PARAMS'] = original_invalid_params


@allure.feature("HAR解析器")
@allure.story("文件不存在处理")
def test_file_not_found():
    """测试文件不存在的情况"""
    parser = HARParser()
    requests = parser.extract_requests_from_har("nonexistent.har")
    assert len(requests) == 0


@allure.feature("HAR解析器")
@allure.story("无效JSON处理")
def test_invalid_json():
    """测试无效JSON的情况"""
    with open("invalid.har", "w", encoding="utf-8") as f:
        f.write("invalid json")

    try:
        parser = HARParser()
        requests = parser.extract_requests_from_har("invalid.har")
        assert len(requests) == 0
    finally:
        if os.path.exists("invalid.har"):
            os.remove("invalid.har")