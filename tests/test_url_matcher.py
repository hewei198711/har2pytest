"""测试 har2pytest.url_matcher.URLMatcher 中 URL 模式匹配、API 文件查找、URL 规范化、函数名生成、URL 模板提取、Swagger 匹配与路径参数提取的功能与边界。"""

import json

import allure

from har2pytest.config import APIConfig
from har2pytest.url_matcher import URLMatcher

# ==================== 辅助函数 ====================


def _write_api_file(tmp_path, url, filename="user_info.py"):
    """在 tmp_path/apis 下写入一个最小 API 文件及其旁车元数据，返回文件路径。

    供 find_matching_api_file 各测试复用写盘样板。函数名取自文件名（不含 .py），
    url 同时写入 docstring 与 .api.json 元数据（parse_api_file 以元数据为准）。
    """
    api_dir = tmp_path / "apis"
    api_dir.mkdir(exist_ok=True)
    api_file = api_dir / filename
    func_name = filename[: -len(".py")]
    api_file.write_text(
        f'''def {func_name}(data=data, token=token):
    """
    {func_name}
    {url}
    """
    url = "{url}"
    headers = {{}}
    return client.get(url=url, headers=headers, params=data)
''',
        encoding="utf-8",
    )
    meta = {
        "function_name": func_name,
        "url": url,
        "description": func_name,
        "method": "GET",
    }
    (api_dir / f"{filename[:-3]}.api.json").write_text(json.dumps(meta), encoding="utf-8")
    return api_file


# ==================== URL模式匹配测试 ====================


class TestMatchUrlPattern:
    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试无路径参数的完全匹配")
    def test_exact_match_without_params(self):
        matched, params = URLMatcher.match_url_pattern("/api/user/info", "/api/user/info")
        assert matched is True
        assert params == {}

    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试带路径参数的匹配")
    def test_match_with_path_param(self):
        matched, params = URLMatcher.match_url_pattern("/api/user/123/info", "/api/user/{userId}/info")
        assert matched is True
        assert params == {"userId": "123"}

    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试多个路径参数的匹配")
    def test_match_with_multiple_path_params(self):
        matched, params = URLMatcher.match_url_pattern("/api/user/123/order/456", "/api/user/{userId}/order/{orderId}")
        assert matched is True
        assert params == {"userId": "123", "orderId": "456"}

    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试URL长度不同时不匹配")
    def test_length_mismatch(self):
        matched, params = URLMatcher.match_url_pattern("/api/user/info", "/api/user")
        assert matched is False
        assert params == {}

        matched, params = URLMatcher.match_url_pattern("/api/user", "/api/user/info")
        assert matched is False
        assert params == {}

    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试非参数部分不匹配")
    def test_non_param_part_mismatch(self):
        matched, params = URLMatcher.match_url_pattern("/api/user/123/info", "/api/order/{userId}/info")
        assert matched is False
        assert params == {}

        matched, params = URLMatcher.match_url_pattern("/api/user/123/info", "/api/user/{userId}/detail")
        assert matched is False
        assert params == {}

    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试空URL")
    def test_empty_url(self):
        matched, params = URLMatcher.match_url_pattern("", "")
        assert matched is True
        assert params == {}

        matched, params = URLMatcher.match_url_pattern("/", "/")
        assert matched is True
        assert params == {}

        matched, params = URLMatcher.match_url_pattern("", "/api/user")
        assert matched is False
        assert params == {}

    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试数字类型的路径参数值")
    def test_numeric_param_value(self):
        matched, params = URLMatcher.match_url_pattern("/api/order/12345/detail", "/api/order/{orderId}/detail")
        assert matched is True
        assert params == {"orderId": "12345"}

        matched, params = URLMatcher.match_url_pattern("/api/product/abc123", "/api/product/{productId}")
        assert matched is True
        assert params == {"productId": "abc123"}

    @allure.feature("URL匹配器")
    @allure.story("URL模式匹配")
    @allure.title("测试完整URL与模式的匹配")
    def test_full_url_vs_pattern(self):
        matched, params = URLMatcher.match_url_pattern("https://example.com/api/user/123", "/api/user/{userId}")
        assert matched is False
        assert params == {}


# ==================== 查找匹配API文件测试 ====================


class TestFindMatchingApiFile:
    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试直接相等匹配")
    def test_exact_match(self, tmp_path):
        api_file = _write_api_file(tmp_path, "/api/user/info")
        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file)])
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试路径参数模式匹配")
    def test_path_param_pattern_match(self, tmp_path):
        api_file = _write_api_file(tmp_path, "/api/user/{userId}/info")
        result = URLMatcher.find_matching_api_file("/api/user/123/info", [str(api_file)])
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试转换后URL匹配")
    def test_transformed_url_match(self, tmp_path):
        api_file = _write_api_file(tmp_path, "/api/user/{userId}/info")

        request_url_map = {"/api/user/123/info": "/api/user/{userId}/info"}

        result = URLMatcher.find_matching_api_file("/api/user/123/info", [str(api_file)], request_url_map)
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试无匹配文件")
    def test_no_matching_file(self, tmp_path):
        api_file = _write_api_file(tmp_path, "/api/user/info")

        result = URLMatcher.find_matching_api_file("/api/order/list", [str(api_file)])
        assert result is None

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试多个API文件时的匹配优先级")
    def test_multiple_api_files_priority(self, tmp_path):
        api_file1 = _write_api_file(tmp_path, "/api/user/info", filename="user_info.py")
        api_file2 = _write_api_file(tmp_path, "/api/user/{userId}/info", filename="user_info_param.py")

        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file1), str(api_file2)])
        assert result == str(api_file1)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试完整URL前缀归一化匹配")
    def test_full_url_with_base_url_stripped(self, tmp_path):
        # 请求 URL 带 scheme://host 前缀：应经 normalize_url 归一化（去除前缀）后命中 API 文件
        api_file = _write_api_file(tmp_path, "/api/user/info")

        result = URLMatcher.find_matching_api_file("https://example.com/api/user/info", [str(api_file)])
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试空API文件列表")
    def test_empty_api_files_list(self):
        result = URLMatcher.find_matching_api_file("/api/user/info", [])
        assert result is None


# ==================== normalize_url 测试 ====================


class TestNormalizeUrl:
    @allure.feature("URL匹配器")
    @allure.story("URL规范化")
    @allure.title("测试移除查询参数")
    def test_remove_query_params(self):
        result = URLMatcher.normalize_url("/api/user/list?page=1&size=10")
        assert result == "/api/user/list"

    @allure.feature("URL匹配器")
    @allure.story("URL规范化")
    @allure.title("测试添加开头的斜杠")
    def test_add_leading_slash(self):
        result = URLMatcher.normalize_url("api/user/list")
        assert result == "/api/user/list"

    @allure.feature("URL匹配器")
    @allure.story("URL规范化")
    @allure.title("测试移除基础URL前缀")
    def test_remove_base_url(self):
        result = URLMatcher.normalize_url("https://example.com/api/user/list", base_urls=["https://example.com"])
        assert result == "/api/user/list"

    @allure.feature("URL匹配器")
    @allure.story("URL规范化")
    @allure.title("测试多个基础URL前缀")
    def test_multiple_base_urls(self):
        base_urls = ["https://dev.example.com", "https://example.com"]
        result = URLMatcher.normalize_url("https://example.com/api/user", base_urls=base_urls)
        assert result == "/api/user"

    @allure.feature("URL匹配器")
    @allure.story("URL规范化")
    @allure.title("测试无基础URL")
    def test_no_base_url(self):
        result = URLMatcher.normalize_url("/api/user/list")
        assert result == "/api/user/list"

    @allure.feature("URL匹配器")
    @allure.story("URL规范化")
    @allure.title("测试绝对URL无匹配base_url时仅保留path部分")
    def test_absolute_url_no_base_match(self):
        # 绝对 URL 未匹配任何 base_url，应只保留 path 部分
        result = URLMatcher.normalize_url("https://other.com/api/user/list")
        assert result == "/api/user/list"

        # 绝对 URL 仅 host 无 path，应回落到 "/"
        result2 = URLMatcher.normalize_url("https://other.com")
        assert result2 == "/"


# ==================== generate_function_name 测试 ====================


class TestGenerateFunctionName:
    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试从普通URL生成函数名")
    def test_normal_url(self):
        result = URLMatcher.generate_function_name("/api/user/login")
        assert result == "api_user_login"

    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试从带路径参数的URL生成函数名")
    def test_url_with_path_params(self):
        result = URLMatcher.generate_function_name("/api/user/{userId}/info")
        assert result == "api_user_userId_info"

    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试None输入")
    def test_none_url(self):
        result = URLMatcher.generate_function_name(None)
        assert result == "unknown"

    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试空URL")
    def test_empty_url(self):
        result = URLMatcher.generate_function_name("")
        assert result == ""


# ==================== extract_url_template 测试 ====================


class TestExtractUrlTemplate:
    @allure.feature("URL匹配器")
    @allure.story("提取URL模板")
    @allure.title("测试匹配URL模板")
    def test_match_template(self):
        patterns = ["/api/user/{userId}/info", "/api/order/{orderId}/detail"]
        template, params = URLMatcher.extract_url_template("/api/user/123/info", patterns)
        assert template == "/api/user/{userId}/info"
        assert params == {"userId": "123"}

    @allure.feature("URL匹配器")
    @allure.story("提取URL模板")
    @allure.title("测试无匹配模板")
    def test_no_match(self):
        patterns = ["/api/user/{userId}/info"]
        template, params = URLMatcher.extract_url_template("/api/order/list", patterns)
        assert template is None
        assert params == {}

    @allure.feature("URL匹配器")
    @allure.story("提取URL模板")
    @allure.title("测试空模板列表")
    def test_empty_patterns(self):
        template, params = URLMatcher.extract_url_template("/api/user/123/info", [])
        assert template is None
        assert params == {}


# ==================== get_url_info 测试 ====================


class TestGetUrlInfo:
    @allure.feature("URL匹配器")
    @allure.story("获取URL信息")
    @allure.title("测试普通URL（无路径参数）")
    def test_plain_url(self):
        matcher = URLMatcher()
        result = matcher.get_url_info("/api/user/login")
        assert result["original_url"] == "/api/user/login"
        assert result["pattern"] == "/api/user/login"
        assert result["has_path_params"] is False

    @allure.feature("URL匹配器")
    @allure.story("获取URL信息")
    @allure.title("测试带花括号的URL")
    def test_url_with_braces(self):
        matcher = URLMatcher()
        result = matcher.get_url_info("/api/user/{userId}/info")
        # 无配置/无 Swagger 命中时，花括号 URL 按字面值回落：pattern=原URL、不提取路径参数
        assert result["original_url"] == "/api/user/{userId}/info"
        assert result["pattern"] == "/api/user/{userId}/info"
        assert result["path_params"] == {}
        assert result["has_path_params"] is False
        assert result["function_name"] == "api_user_userId_info"

    @allure.feature("URL匹配器")
    @allure.story("获取URL信息")
    @allure.title("测试带数字路径的URL（从配置匹配）")
    def test_url_with_numeric_path(self, monkeypatch):
        # PATH_URLS 配置了路径模板后，数值路径 URL 应命中模板并提取路径参数
        if APIConfig._config is None:
            APIConfig._config = APIConfig._load_config()
        monkeypatch.setitem(APIConfig._config, "PATH_URLS", ["/api/user/{userId}/info"])
        matcher = URLMatcher()
        result = matcher.get_url_info("/api/user/12345/info")
        assert result["original_url"] == "/api/user/12345/info"
        assert result["pattern"] == "/api/user/{userId}/info"
        assert result["path_params"] == {"userId": "12345"}
        assert result["has_path_params"] is True

    @allure.feature("URL匹配器")
    @allure.story("获取URL信息")
    @allure.title("测试URL信息缓存")
    def test_url_info_cache(self):
        matcher = URLMatcher()
        result1 = matcher.get_url_info("/api/user/login")
        result2 = matcher.get_url_info("/api/user/login")
        assert result1 == result2
        # 第二次调用命中 _url_info_cache，缓存只保留一条
        assert len(matcher._url_info_cache) == 1


# ==================== remove_base_path 测试 ====================


class TestRemoveBasePath:
    @allure.feature("URL匹配器")
    @allure.story("移除基础路径")
    @allure.title("测试移除基础路径")
    def test_remove_base_path(self):
        result = URLMatcher.remove_base_path("/swagger/api/user/login", "/swagger")
        assert result == "/api/user/login"

    @allure.feature("URL匹配器")
    @allure.story("移除基础路径")
    @allure.title("测试空基础路径")
    def test_empty_base_path(self):
        result = URLMatcher.remove_base_path("/api/user/login", "")
        assert result == "/api/user/login"

    @allure.feature("URL匹配器")
    @allure.story("移除基础路径")
    @allure.title("测试根路径基础路径")
    def test_root_base_path(self):
        result = URLMatcher.remove_base_path("/api/user/login", "/")
        assert result == "/api/user/login"

    @allure.feature("URL匹配器")
    @allure.story("移除基础路径")
    @allure.title("测试不匹配的基础路径")
    def test_non_matching_base_path(self):
        result = URLMatcher.remove_base_path("/api/user/login", "/v2")
        assert result == "/api/user/login"


# ==================== _extract_path_parts 测试 ====================


class TestExtractPathParts:
    @allure.feature("URL匹配器")
    @allure.story("提取路径部分")
    @allure.title("测试提取路径部分（含参数）")
    def test_extract_with_params(self):
        result = URLMatcher._extract_path_parts("/api/user/123/info", "/api/user/{userId}/info")
        assert result == ["api", "user", "userId", "info"]

    @allure.feature("URL匹配器")
    @allure.story("提取路径部分")
    @allure.title("测试提取路径部分（无参数）")
    def test_extract_without_params(self):
        result = URLMatcher._extract_path_parts("/api/user/login", "/api/user/login")
        assert result == ["api", "user", "login"]


# ==================== match_with_swagger 测试 ====================


class TestMatchWithSwagger:
    @allure.feature("URL匹配器")
    @allure.story("Swagger匹配")
    @allure.title("测试无Swagger数据")
    def test_no_swagger_data(self):
        matcher = URLMatcher()
        result = matcher.match_with_swagger("/api/user/123")
        assert result == (None, {}, [])

    @allure.feature("URL匹配器")
    @allure.story("Swagger匹配")
    @allure.title("测试Swagger数据无paths字段")
    def test_swagger_no_paths(self):
        matcher = URLMatcher({"info": {"title": "Test"}})
        result = matcher.match_with_swagger("/api/user/123")
        assert result == (None, {}, [])

    @allure.feature("URL匹配器")
    @allure.story("Swagger匹配")
    @allure.title("测试Swagger路径匹配")
    def test_swagger_path_match(self):
        swagger_data = {
            "basePath": "/api",
            "paths": {
                "/user/{userId}/info": {"get": {}},
                "/order/list": {"get": {}},
            },
        }
        matcher = URLMatcher(swagger_data)
        full_path, params, parts = matcher.match_with_swagger("/api/user/123/info")
        assert full_path == "/api/user/{userId}/info"
        assert params == {"userId": "123"}
        assert parts == ["user", "userId", "info"]

    @allure.feature("URL匹配器")
    @allure.story("Swagger匹配")
    @allure.title("测试Swagger不匹配")
    def test_swagger_no_match(self):
        swagger_data = {
            "basePath": "/api",
            "paths": {
                "/user/{userId}/info": {"get": {}},
            },
        }
        matcher = URLMatcher(swagger_data)
        result = matcher.match_with_swagger("/api/order/list")
        assert result == (None, {}, [])

    @allure.feature("URL匹配器")
    @allure.story("Swagger匹配")
    @allure.title("测试Swagger匹配缓存")
    def test_swagger_match_cache(self):
        swagger_data = {
            "basePath": "",
            "paths": {
                "/user/{userId}/info": {"get": {}},
            },
        }
        matcher = URLMatcher(swagger_data)
        result1 = matcher.match_with_swagger("/user/123/info")
        result2 = matcher.match_with_swagger("/user/123/info")
        assert result1 == result2
        # 第二次调用命中 _swagger_match_cache，缓存只保留一条
        assert len(matcher._swagger_match_cache) == 1


# ==================== find_matching_api_file 边缘测试 ====================


class TestFindMatchingApiFileEdge:
    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件-边缘")
    @allure.title("测试URL标准化匹配")
    def test_normalized_url_match(self, tmp_path):
        api_file = _write_api_file(tmp_path, "/api/user/info")

        # 带查询参数、无前导斜杠的请求 URL 应标准化（去 query、补斜杠）后命中 API 文件
        result = URLMatcher.find_matching_api_file("api/user/info?page=1&size=10", [str(api_file)])
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件-边缘")
    @allure.title("测试API文件缺少元数据时跳过")
    def test_api_file_no_metadata_skipped(self, tmp_path):
        # 无 .api.json 元数据 → parse_api_file 抛 ValueError → 候选文件被跳过
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "no_meta.py"
        api_file.write_text(
            '''def no_meta(data=data, token=token):
    """
    无元数据
    """
    url = "/api/user/info"
    headers = {}
    return client.get(url=url, headers=headers, params=data)
''',
            encoding="utf-8",
        )

        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file)])
        assert result is None

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件-边缘")
    @allure.title("测试API文件元数据url为空时作为无效文件跳过")
    def test_api_file_empty_url_skipped(self, tmp_path):
        # .api.json 存在但 url 为空 → parse_api_file 抛 ValueError → 候选文件被跳过
        # （parse_api_file 对 url 做 if not url: raise ValueError 校验）
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "empty_url.py"
        api_file.write_text("def empty_url(): pass\n", encoding="utf-8")
        meta = {"function_name": "empty_url", "url": "", "description": "空URL", "method": "GET"}
        (api_dir / "empty_url.api.json").write_text(json.dumps(meta), encoding="utf-8")

        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file)])
        assert result is None

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件-边缘")
    @allure.title("测试反向模式匹配命中API文件")
    def test_reverse_pattern_match(self, tmp_path):
        # 请求 URL 为模板形式，API 文件 URL 为具体值：反向 match_url_pattern(file_url, request_url) 命中
        api_file = _write_api_file(tmp_path, "/api/user/123/info", filename="user_123_info.py")
        result = URLMatcher.find_matching_api_file("/api/user/{userId}/info", [str(api_file)])
        assert result == str(api_file)


@allure.feature("URL匹配器")
@allure.story("Swagger模板匹配")
@allure.title("测试 paths 键已含 basePath 时模板匹配仍然生效")
def test_template_match_when_paths_include_basepath():
    matcher = URLMatcher()
    matcher.swagger_data = {
        "basePath": "/admin",
        "paths": {
            "/admin/x/page": {"get": {}},
            "/admin/x/{id}": {"get": {}},
        },
    }

    # 具体取值应命中模板并提取路径参数（修复前 pattern 退化成原 URL、参数丢失）
    templated = matcher.get_url_info("/admin/x/12345")
    assert templated["pattern"] == "/admin/x/{id}"
    assert templated["path_params"] == {"id": "12345"}
    assert templated["function_name"] == "admin_x_id"

    # 文档里存在的具体路径仍精确命中，且不会被重复加 basePath
    exact = matcher.get_url_info("/admin/x/page")
    assert exact["pattern"] == "/admin/x/page"
    assert exact["path_params"] == {}
    assert "admin/admin" not in exact["pattern"]


@allure.feature("URL匹配器")
@allure.story("Swagger模板匹配")
@allure.title("测试 paths 键不含 basePath 与含 basePath 结果一致")
def test_template_match_basepath_shapes_equivalent():
    results = []
    for paths in ({"/x/{id}": {"get": {}}}, {"/admin/x/{id}": {"get": {}}}):
        matcher = URLMatcher()
        matcher.swagger_data = {"basePath": "/admin", "paths": paths}
        info = matcher.get_url_info("/admin/x/12345")
        results.append((info["pattern"], info["path_params"], info["function_name"]))

    assert results[0] == results[1]
    assert results[0] == ("/admin/x/{id}", {"id": "12345"}, "admin_x_id")


@allure.feature("URL匹配器")
@allure.story("Swagger模板匹配")
@allure.title("测试具体路径优先精确命中而非被通配模板劫持")
def test_exact_path_wins_over_wildcard_template():
    matcher = URLMatcher()
    matcher.swagger_data = {
        "basePath": "/appStore",
        "paths": {
            "/mobile/returnOrder/page": {"get": {}},
            "/mobile/returnOrder/{id}": {"get": {}},
        },
    }

    exact = matcher.get_url_info("/appStore/mobile/returnOrder/page")
    assert exact["pattern"] == "/appStore/mobile/returnOrder/page"
    assert exact["path_params"] == {}
    assert exact["function_name"] == "appStore_mobile_returnOrder_page"

    # 具体取值（文档里没有该键）仍应命中模板并提取路径参数
    templated = matcher.get_url_info("/appStore/mobile/returnOrder/12345")
    assert templated["pattern"] == "/appStore/mobile/returnOrder/{id}"
    assert templated["path_params"] == {"id": "12345"}
