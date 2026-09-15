"""测试 har2pytest.config 模块中 APIConfig 配置加载、访问器、服务包判断与异常校验的功能与边界。"""

import json
import os

import allure
import pytest

from har2pytest.config import APIConfig


@pytest.fixture(autouse=True)
def _restore_config_env():
    """每个测试前后自动保存/恢复环境变量与配置缓存，确保测试间隔离。"""
    original_env = os.environ.get("HAR2PYTEST_CONFIG")
    original_config = APIConfig._config
    yield
    if original_env is not None:
        os.environ["HAR2PYTEST_CONFIG"] = original_env
    else:
        os.environ.pop("HAR2PYTEST_CONFIG", None)
    APIConfig._config = original_config
    APIConfig._load_config()


@pytest.fixture
def test_config():
    """加载项目测试目录下的 har2pytest_config_test.json 并返回配置字典。"""
    test_config_path = os.path.join(os.path.dirname(__file__), "har2pytest_config_test.json")
    os.environ["HAR2PYTEST_CONFIG"] = test_config_path
    APIConfig._config = None
    return APIConfig._load_config()


@pytest.fixture
def tmp_config(tmp_path):
    """创建临时配置文件并设置 HAR2PYTEST_CONFIG 环境变量，测试结束后由 autouse fixture 清理。"""
    def _create(config_dict):
        path = tmp_path / "config.json"
        path.write_text(json.dumps(config_dict, ensure_ascii=False), encoding="utf-8")
        os.environ["HAR2PYTEST_CONFIG"] = str(path)
        APIConfig._config = None
        return path
    return _create


# ==================== 默认配置与加载测试 ====================


@allure.feature("配置管理")
@allure.story("默认配置")
@allure.title("测试默认配置")
def test_default_config(test_config):
    assert APIConfig.BASE_URLS() == ["https://taobao.com/api"]
    assert APIConfig.KILL_URLS() == ["aliyuncs.com"]
    assert APIConfig.DEFAULT_API_DIR() == "apis"
    assert APIConfig.INVALID_PARAMS() == {"partnerKey", "sign", "timestamp", "nonce", "rnd"}
    assert APIConfig.HEADERS_TO_INCLUDE() == {
        "authorization": "f\"token {os.environ['token']}\"",
        "content-type": "application/json;charset=UTF-8",
    }
    assert APIConfig.REQUIRED_HEADERS() == {"authorization": "f\"token {os.environ['token']}\""}
    # 分页参数
    assert APIConfig.PAGINATION_PARAMS() == ["pageNum", "pageSize"]
    # PATH_URLS
    assert len(APIConfig.PATH_URLS()) == 5
    assert "/mobile/dashbord/{usrId}" in APIConfig.PATH_URLS()
    # 列表查询排除关键字（测试配置未设置，回退默认空列表）
    assert APIConfig.LIST_QUERY_EXCLUDE_KEYWORDS() == []
    # 单接口测试模式配置（测试配置未设置，回退默认空列表）
    assert APIConfig.TESTCASE_PROFILES() == []


@allure.feature("配置管理")
@allure.story("配置文件加载")
@allure.title("测试配置文件加载")
def test_config_file_loading(tmp_config):
    test_config = {
        "BASE_URLS": ["https://test.example.com/api"],
        "DEFAULT_API_DIR": "test_api",
        "TESTCASE_DIR": "test_testcases",
        "SERVICE_MAPPING": {"api": "test_service"},
        "SWAGGER_DOC_URLS": {"test_service": "https://test.example.com/swagger"},
    }
    tmp_config(test_config)
    config = APIConfig._load_config()

    assert config.get("BASE_URLS") == ["https://test.example.com/api"]
    assert config.get("DEFAULT_API_DIR") == "test_api"
    assert config.get("TESTCASE_DIR") == "test_testcases"


# ==================== 配置项访问器测试 ====================


@allure.feature("配置管理")
@allure.story("列表查询关键字")
@allure.title("测试列表查询关键字配置")
def test_list_query_keywords(test_config):
    keywords = APIConfig.LIST_QUERY_KEYWORDS()
    assert isinstance(keywords, list)
    assert "列表" in keywords
    assert "查询" in keywords
    assert len(keywords) == 2


@allure.feature("配置管理")
@allure.story("状态值提取模式")
@allure.title("测试状态值提取模式配置")
def test_state_value_patterns(test_config):
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


@allure.feature("配置管理")
@allure.story("默认配置值")
@allure.title("测试默认 LIST_QUERY_KEYWORDS 和 STATE_VALUE_PATTERNS")
@allure.description("测试无配置文件时 LIST_QUERY_KEYWORDS 和 STATE_VALUE_PATTERNS 的默认值")
def test_default_list_query_and_state_patterns(tmp_config):
    # 创建最小配置文件，满足必需配置项校验
    minimal_config = {
        "BASE_URLS": ["https://test.example.com"],
        "SERVICE_MAPPING": {"test": "test_service"},
        "SWAGGER_DOC_URLS": {"test_service": "https://test.example.com/swagger"},
    }
    tmp_config(minimal_config)
    APIConfig._load_config()

    # 默认 LIST_QUERY_KEYWORDS 应为 ["列表"]
    keywords = APIConfig.LIST_QUERY_KEYWORDS()
    assert keywords == ["列表"]

    # 默认 STATE_VALUE_PATTERNS 应为空列表
    patterns = APIConfig.STATE_VALUE_PATTERNS()
    assert patterns == []


# ==================== 服务包判断测试 ====================


@allure.feature("配置管理")
@allure.story("服务包判断")
@allure.title("测试根据URL判断服务包")
def test_determine_service_package(test_config):
    # 匹配 SERVICE_MAPPING 中的 mobile → mobile_application
    assert APIConfig.determine_service_package("/mobile/trade/orderCommit") == "mobile_application"
    # 匹配 SERVICE_MAPPING 中的 member → order_application
    assert APIConfig.determine_service_package("/member/order/detail") == "order_application"
    # 大小写不敏感匹配
    assert APIConfig.determine_service_package("/Mobile/Dashboard") == "mobile_application"
    # 未匹配时回退到 DEFAULT_API_DIR
    assert APIConfig.determine_service_package("/unknown/path") == "apis"
    # 空字符串和 None 回退到 DEFAULT_API_DIR
    assert APIConfig.determine_service_package("") == "apis"
    assert APIConfig.determine_service_package(None) == "apis"


# ==================== 配置异常分支测试 ====================


@allure.feature("配置管理")
@allure.story("配置异常分支")
@allure.title("测试缺少必需配置项时抛 ValueError")
def test_missing_required_config_raises(tmp_config):
    tmp_config({"BASE_URLS": ["https://x"]})

    with pytest.raises(ValueError, match="缺少必需配置项"):
        APIConfig._load_config()


@allure.feature("配置管理")
@allure.story("配置异常分支")
@allure.title("测试 HEADERS_TO_INCLUDE 非 dict 时抛 ValueError")
def test_headers_to_include_not_dict_raises(tmp_config):
    tmp_config({
        "BASE_URLS": ["https://x"],
        "SERVICE_MAPPING": {"a": "b"},
        "SWAGGER_DOC_URLS": {"b": "https://x/sw"},
        "DEFAULT_API_DIR": "apis",
        "TESTCASE_DIR": "testcases",
        "HEADERS_TO_INCLUDE": ["not", "a", "dict"],
    })

    with pytest.raises(ValueError, match="HEADERS_TO_INCLUDE 仅支持字典格式"):
        APIConfig._load_config()


@allure.feature("配置管理")
@allure.story("配置异常分支")
@allure.title("测试坏 JSON 配置文件回退默认后仍校验必需项")
def test_bad_json_config(tmp_path, tmp_config):
    # 写入坏 JSON：回退默认配置；默认 SERVICE_MAPPING 为 None → 触发必需项校验
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{broken json", encoding="utf-8")
    os.environ["HAR2PYTEST_CONFIG"] = str(bad_path)
    APIConfig._config = None

    with pytest.raises(ValueError):
        APIConfig._load_config()


# ==================== 配置自动加载与警告测试 ====================


@allure.feature("配置管理")
@allure.story("配置自动加载")
@allure.title("测试 get_config 在 _config 为 None 时自动触发加载")
def test_get_config_auto_loads(test_config):
    # 重置 _config 为 None，模拟首次调用
    APIConfig._config = None
    # get_config 应自动触发 _load_config
    result = APIConfig.get_config("BASE_URLS")
    assert result == ["https://taobao.com/api"]
    # _config 应已被填充
    assert APIConfig._config is not None


@allure.feature("配置管理")
@allure.story("配置缺失警告")
@allure.title("测试配置文件不存在时触发 _warn_missing_config 警告")
def test_warn_missing_config_when_file_absent():
    # 指向一个不存在的配置文件
    os.environ["HAR2PYTEST_CONFIG"] = "/nonexistent/path/config.json"
    APIConfig._config = None
    APIConfig._config_warned = False

    APIConfig.get_config("BASE_URLS")

    assert APIConfig._config_warned is True
