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
            "authorization": "f\"bearer {os.environ['token']}\"",
            "content-type": "application/json;charset=UTF-8"
        }
        assert APIConfig.REQUIRED_HEADERS() == {"authorization": "f\"bearer {os.environ['token']}\""}
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
@allure.story("列表查询关键字")
@allure.title("测试列表查询关键字配置")
def test_list_query_keywords():
    """测试 LIST_QUERY_KEYWORDS 配置项"""
    test_config_path = os.path.join(os.path.dirname(__file__), "har2pytest_config_test.json")
    original_config = os.environ.get("HAR2PYTEST_CONFIG")

    try:
        os.environ["HAR2PYTEST_CONFIG"] = test_config_path
        APIConfig._config = None
        APIConfig._load_config()

        keywords = APIConfig.LIST_QUERY_KEYWORDS()
        assert isinstance(keywords, list)
        assert "列表" in keywords
        assert "查询" in keywords
        assert len(keywords) == 2
    finally:
        if original_config:
            os.environ["HAR2PYTEST_CONFIG"] = original_config
        else:
            if "HAR2PYTEST_CONFIG" in os.environ:
                del os.environ["HAR2PYTEST_CONFIG"]
        APIConfig._config = None


@allure.feature("配置管理")
@allure.story("状态值提取模式")
@allure.title("测试状态值提取模式配置")
def test_state_value_patterns():
    """测试 STATE_VALUE_PATTERNS 配置项"""
    test_config_path = os.path.join(os.path.dirname(__file__), "har2pytest_config_test.json")
    original_config = os.environ.get("HAR2PYTEST_CONFIG")

    try:
        os.environ["HAR2PYTEST_CONFIG"] = test_config_path
        APIConfig._config = None
        APIConfig._load_config()

        patterns = APIConfig.STATE_VALUE_PATTERNS()
        assert isinstance(patterns, list)
        assert len(patterns) == 2

        # 第一个是字符串格式
        assert isinstance(patterns[0], str)
        assert patterns[0] == "(-?\\d+)\\s*[:：]"

        # 第二个是字典格式
        assert isinstance(patterns[1], dict)
        assert patterns[1]["regex"] == "(\\w+)\\s*->"
        assert patterns[1]["type"] == "str"
    finally:
        if original_config:
            os.environ["HAR2PYTEST_CONFIG"] = original_config
        else:
            if "HAR2PYTEST_CONFIG" in os.environ:
                del os.environ["HAR2PYTEST_CONFIG"]
        APIConfig._config = None


@allure.feature("配置管理")
@allure.story("默认配置值")
@allure.title("测试默认 LIST_QUERY_KEYWORDS 和 STATE_VALUE_PATTERNS")
def test_default_list_query_and_state_patterns():
    """测试无配置文件时 LIST_QUERY_KEYWORDS 和 STATE_VALUE_PATTERNS 的默认值"""
    # 创建最小配置文件，满足必需配置项校验
    minimal_config = {
        "BASE_URLS": ["https://test.example.com"],
        "SERVICE_MAPPING": {"test": "test_service"},
        "SWAGGER_DOC_URLS": {"test_service": "https://test.example.com/swagger"},
    }
    with open("test_minimal_config.json", "w", encoding="utf-8") as f:
        json.dump(minimal_config, f)

    original_config = os.environ.get("HAR2PYTEST_CONFIG")

    try:
        os.environ["HAR2PYTEST_CONFIG"] = "test_minimal_config.json"
        APIConfig._config = None
        APIConfig._load_config()

        # 默认 LIST_QUERY_KEYWORDS 应为 ["列表"]
        keywords = APIConfig.LIST_QUERY_KEYWORDS()
        assert keywords == ["列表"]

        # 默认 STATE_VALUE_PATTERNS 应为空列表
        patterns = APIConfig.STATE_VALUE_PATTERNS()
        assert patterns == []
    finally:
        if original_config:
            os.environ["HAR2PYTEST_CONFIG"] = original_config
        else:
            if "HAR2PYTEST_CONFIG" in os.environ:
                del os.environ["HAR2PYTEST_CONFIG"]
        if os.path.exists("test_minimal_config.json"):
            os.remove("test_minimal_config.json")
        APIConfig._config = None


@allure.feature("配置管理")
@allure.story("服务包判断")
@allure.title("测试根据URL判断服务包")
def test_determine_service_package():
    assert APIConfig.determine_service_package("https://example.com/api/user/login") == "apis"

    assert APIConfig.determine_service_package("https://example.com/api/v1/user/login") == "apis"

    assert APIConfig.determine_service_package("") == "apis"

    assert APIConfig.determine_service_package(None) == "apis"