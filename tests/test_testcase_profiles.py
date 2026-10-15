"""测试 har2pytest.testcase_generator 中 TESTCASE_PROFILES 配置化模式决策（_profile_matches / _find_profile / _resolve_testcase_mode）的 URL 匹配、显式模式覆盖、关键字回落与 profile 级关键字覆盖的功能与边界。"""

import allure
import pytest

from har2pytest.api_metadata import write_api_metadata
from har2pytest.config import APIConfig
from har2pytest.testcase_generator import TestCaseGenerator

# ==================== 辅助函数 ====================


def _set_profiles(profiles, keywords=None, exclude=None):
    if APIConfig._config is None:
        APIConfig._config = APIConfig._load_config()
    saved = dict(APIConfig._config)
    cfg = {**saved, "TESTCASE_PROFILES": profiles}
    if keywords is not None:
        cfg["LIST_QUERY_KEYWORDS"] = keywords
    if exclude is not None:
        cfg["LIST_QUERY_EXCLUDE_KEYWORDS"] = exclude
    APIConfig._config = cfg

    def restore():
        APIConfig._config = saved

    return restore


def _write_api(tmp_path, filename, description, url):
    api_dir = tmp_path / "apis" / "test_service"
    api_dir.mkdir(parents=True, exist_ok=True)
    api_file = api_dir / filename
    api_file.write_text(
        f'''params = {{"page": "1"}}

def {filename[:-3]}(params=params):
    """
    {description}
    {url}
    """
    url = "{url}"
''',
        encoding="utf-8",
    )
    # _resolve_testcase_mode 走 parse_api_file（只读 .api.json），需补同名元数据：
    # url/description 与 docstring 表达一致
    write_api_metadata(str(api_file), url=url, description=description, params={"page": "1"})
    return str(api_file)


# ==================== URL匹配测试 ====================


@allure.feature("测试模式配置化")
@allure.story("URL匹配")
@allure.title("测试精确 URL / 模板 / 通配匹配")
@pytest.mark.parametrize("profile_url,api_url,expected", [
    ("/mgmt/order/orderList", "/mgmt/order/orderList", True),   # 精确匹配
    ("/mgmt/order/{orderNo}", "/mgmt/order/1001", True),        # profile 模板 → 具体 URL
    ("/mgmt/order/1001", "/mgmt/order/{orderNo}", True),        # 具体 profile → 模板 URL（反向）
    ("/mgmt/order/*", "/mgmt/order/orderList", True),           # 通配符
    ("/mall/user/list", "/mgmt/order/orderList", False),        # 不匹配
])
def test_profile_matches(profile_url, api_url, expected):
    gen = TestCaseGenerator(api_dir="apis")
    assert gen._profile_matches(profile_url, api_url) == expected


# ==================== 模式决策优先级测试 ====================


@allure.feature("测试模式配置化")
@allure.story("模式决策优先级")
@allure.title("测试显式 list_query 覆盖描述无列表关键字")
def test_profile_explicit_list_query(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_list.py", "订单查询", "/mgmt/order/orderList")
    restore = _set_profiles([{"url": "/mgmt/order/orderList", "mode": "list_query"}], keywords=["列表"])
    try:
        assert gen._resolve_testcase_mode(api_file) == "parametrized"
    finally:
        restore()


@allure.feature("测试模式配置化")
@allure.story("模式决策优先级")
@allure.title("测试显式 complex_scenario 覆盖描述含列表关键字")
def test_profile_explicit_scenario(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_list.py", "订单列表查询", "/mgmt/order/orderList")
    restore = _set_profiles([{"url": "/mgmt/order/orderList", "mode": "complex_scenario"}], keywords=["列表"])
    try:
        assert gen._resolve_testcase_mode(api_file) == "scenario"
    finally:
        restore()


# ==================== _find_profile 边界测试 ====================


@allure.feature("测试模式配置化")
@allure.story("_find_profile边界")
@allure.title("测试 api_url 为 None 或空字符串时返回 None")
@pytest.mark.parametrize("api_url", [None, ""])
def test_find_profile_empty_url(api_url):
    gen = TestCaseGenerator(api_dir="apis")
    restore = _set_profiles([{"url": "/mgmt/order/*", "mode": "list_query"}])
    try:
        assert gen._find_profile(api_url) is None
    finally:
        restore()


# ==================== 关键字回落测试 ====================


@allure.feature("测试模式配置化")
@allure.story("关键字回落")
@allure.title("测试未配置时回落全局列表关键字")
def test_profile_fallback_keywords(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_list.py", "订单列表查询", "/mgmt/order/orderList")
    restore = _set_profiles([], keywords=["列表"])
    try:
        assert gen._resolve_testcase_mode(api_file) == "parametrized"
    finally:
        restore()


@allure.feature("测试模式配置化")
@allure.story("关键字回落")
@allure.title("测试模式 auto 且命中排除关键字时回落场景")
def test_profile_auto_with_exclude(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_detail.py", "订单列表详情", "/mgmt/order/detail")
    restore = _set_profiles(
        [{"url": "/mgmt/order/detail", "mode": "auto"}],
        keywords=["列表"],
        exclude=["详情"],
    )
    try:
        assert gen._resolve_testcase_mode(api_file) == "scenario"
    finally:
        restore()


@allure.feature("测试模式配置化")
@allure.story("关键字回落")
@allure.title("测试描述不含列表关键字但有参数时回落参数化模式")
def test_no_keyword_match_with_params_falls_back_to_parametrized(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_detail.py", "订单详情", "/mgmt/order/detail")
    # 全局关键字为 ["列表"]，描述 "订单详情" 不含 "列表"，但 API 携带参数，应回落为 parametrized
    restore = _set_profiles([], keywords=["列表"])
    try:
        assert gen._resolve_testcase_mode(api_file) == "parametrized"
    finally:
        restore()


@allure.feature("测试模式配置化")
@allure.story("profile级关键字覆盖")
@allure.title("测试profile级keywords覆盖全局默认")
def test_profile_level_keywords_override(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_list.py", "订单查询", "/mgmt/order/orderList")
    # profile 级 keywords 覆盖全局 LIST_QUERY_KEYWORDS（全局无"查询"，profile 有）
    restore = _set_profiles(
        [{"url": "/mgmt/order/orderList", "mode": "auto", "keywords": ["查询"]}],
        keywords=["列表"],
    )
    try:
        assert gen._resolve_testcase_mode(api_file) == "parametrized"
    finally:
        restore()


@allure.feature("测试模式配置化")
@allure.story("profile级关键字覆盖")
@allure.title("测试profile级exclude_keywords覆盖全局默认")
def test_profile_level_exclude_override(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_detail.py", "订单列表详情", "/mgmt/order/detail")
    # profile 级 exclude_keywords 覆盖全局 LIST_QUERY_EXCLUDE_KEYWORDS
    restore = _set_profiles(
        [{"url": "/mgmt/order/detail", "mode": "auto", "keywords": ["列表"], "exclude_keywords": ["详情"]}],
        keywords=["列表"],
        exclude=[],
    )
    try:
        assert gen._resolve_testcase_mode(api_file) == "scenario"
    finally:
        restore()


# ==================== 通配符匹配测试 ====================


@allure.feature("测试模式配置化")
@allure.story("模式决策")
@allure.title("测试 profile 通配符 URL 命中")
def test_profile_wildcard_url(tmp_path):
    gen = TestCaseGenerator(api_dir=str(tmp_path / "apis"))
    api_file = _write_api(tmp_path, "order_list.py", "订单查询", "/mgmt/order/orderList")
    restore = _set_profiles([{"url": "/mgmt/order/*", "mode": "list_query"}], keywords=[])
    try:
        assert gen._resolve_testcase_mode(api_file) == "parametrized"
    finally:
        restore()
