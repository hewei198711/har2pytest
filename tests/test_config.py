"""
测试 config.py 模块
"""

import json
import os

import allure

from har2pytest.config import APIConfig


@allure.feature("配置管理")
@allure.story("默认配置")
@allure.title("测试默认配置")
def test_default_config():
    test_config_path = os.path.join(os.path.dirname(__file__), "har2pytest_config_test.json")
    original_config = os.environ.get("HAR2PYTEST_CONFIG")

    try:
        os.environ["HAR2PYTEST_CONFIG"] = test_config_path
        APIConfig._config = None
        APIConfig._load_config()

        assert APIConfig.BASE_URLS() == ["https://taobao.com/api"]
        assert APIConfig.KILL_URLS() == ["aliyuncs.com"]
        assert APIConfig.DEFAULT_API_DIR() == "apis"
        assert APIConfig.INVALID_PARAMS() == {"partnerKey", "sign", "timestamp", "nonce", "rnd"}
        assert APIConfig.HEADERS_TO_INCLUDE() == {
            "authorization": "f\"bearer {os.environ['access_token']}\"",
            "content-type": "application/json;charset=UTF-8"
        }
        assert APIConfig.REQUIRED_HEADERS() == {"authorization": "f\"bearer {os.environ['access_token']}\""}
    finally:
        if original_config:
            os.environ["HAR2PYTEST_CONFIG"] = original_config
        else:
            if "HAR2PYTEST_CONFIG" in os.environ:
                del os.environ["HAR2PYTEST_CONFIG"]
        APIConfig._config = None


@allure.feature("配置管理")
@allure.story("配置文件加载")
@allure.title("测试配置文件加载")
def test_config_file_loading():
    test_config = {
        "BASE_URLS": ["https://test.example.com/api"],
        "DEFAULT_API_DIR": "test_api",
        "TESTCASE_DIR": "test_testcases",
        "SERVICE_MAPPING": {"api": "test_service"},
        "SWAGGER_DOC_URLS": {"test_service": "https://test.example.com/swagger"},
    }

    with open("test_config.json", "w", encoding="utf-8") as f:
        json.dump(test_config, f)

    try:
        os.environ["HAR2PYTEST_CONFIG"] = "test_config.json"

        APIConfig._config = None
        config, config_file_exists = APIConfig._load_config()

        assert config.get("BASE_URLS") == ["https://test.example.com/api"]
        assert config.get("DEFAULT_API_DIR") == "test_api"
        assert config.get("TESTCASE_DIR") == "test_testcases"
        assert config_file_exists is True
    finally:
        if "HAR2PYTEST_CONFIG" in os.environ:
            del os.environ["HAR2PYTEST_CONFIG"]
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
        APIConfig._config = None
        APIConfig._load_config()


@allure.feature("配置管理")
@allure.story("服务包判断")
@allure.title("测试根据URL判断服务包")
def test_determine_service_package():
    assert APIConfig.determine_service_package("https://example.com/api/user/login") == "apis"

    assert APIConfig.determine_service_package("https://example.com/api/v1/user/login") == "apis"

    assert APIConfig.determine_service_package("") == "apis"

    assert APIConfig.determine_service_package(None) == "apis"