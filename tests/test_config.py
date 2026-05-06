"""
测试 config.py 模块
"""

import json
import os

import allure

from har2pytest.config import APIConfig


@allure.feature("配置管理")
@allure.story("默认配置")
def test_default_config():
    """测试默认配置"""
    # 测试默认配置值
    assert APIConfig.BASE_URLS() == ["https://uc-test.perfect99.com/api", "https://uc-uat.perfect99.com/api"]
    assert APIConfig.KILL_URLS() == ["aliyuncs.com"]
    assert APIConfig.DEFAULT_SERVICE_PACKAGE() == "apis"
    assert APIConfig.DEFAULT_TESTCASE_DIR() == "testcases"
    assert APIConfig.INVALID_PARAMS() == {"partnerKey", "sign", "timestamp", "nonce", "rnd"}
    assert APIConfig.HEADERS_TO_INCLUDE() == {
        "authorization": "bearer {os.environ['access_token']}",
        "channel": "pc",
        "content-type": "application/json;charset=UTF-8",
        "client": "op",
    }
    assert APIConfig.REQUIRED_HEADERS() == {"authorization": "请输入认证令牌"}
    assert APIConfig.SWAGGER_FILE() == "swagger.json"
    assert APIConfig.SWAGGER_HOST() == "https://api.example.com"
    assert APIConfig.SWAGGER_BASE_PATH() == "/api"
    assert APIConfig.SWAGGER_TITLE() == "API Documentation"
    assert APIConfig.SWAGGER_VERSION() == "1.0.0"


@allure.feature("配置管理")
@allure.story("配置文件加载")
def test_config_file_loading():
    """测试配置文件加载"""
    # 创建临时配置文件
    test_config = {"BASE_URLS": ["https://test.example.com/api"], "DEFAULT_SERVICE_PACKAGE": "test_api"}

    with open("test_config.json", "w", encoding="utf-8") as f:
        json.dump(test_config, f)

    try:
        # 设置环境变量指定配置文件
        os.environ["HAR2PYTEST_CONFIG"] = "test_config.json"

        # 重新加载配置
        APIConfig._config = None
        config, config_file_exists = APIConfig._load_config()

        # 测试配置是否正确加载
        assert config.get("BASE_URLS") == ["https://test.example.com/api"]
        assert config.get("DEFAULT_SERVICE_PACKAGE") == "test_api"
        assert config_file_exists is True
    finally:
        # 清理
        if "HAR2PYTEST_CONFIG" in os.environ:
            del os.environ["HAR2PYTEST_CONFIG"]
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
        # 恢复默认配置
        APIConfig._config = None
        APIConfig._load_config()


@allure.feature("配置管理")
@allure.story("服务包判断")
def test_determine_service_package():
    """测试根据URL判断服务包"""
    # 测试正常URL
    assert APIConfig.determine_service_package("https://example.com/api/user/login") == "apis"

    # 测试带路径的URL
    assert APIConfig.determine_service_package("https://example.com/api/v1/user/login") == "apis"

    # 测试空URL
    assert APIConfig.determine_service_package("") == "apis"

    # 测试None
    assert APIConfig.determine_service_package(None) == "apis"
