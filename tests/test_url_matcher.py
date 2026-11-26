"""测试 har2pytest.url_matcher.URLMatcher 中 URL 模式匹配、API 文件查找、URL 规范化、函数名生成、URL 模板提取、Swagger 匹配与路径参数提取的功能与边界。"""

import json

import allure
import pytest

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
    @allure.title("测试 URL 模式匹配各形态")
    @pytest.mark.parametrize(
        "url,pattern,expected",
        [
            pytest.param("/api/user/info", "/api/user/info", (True, {}), id="无路径参数完全匹配"),
            pytest.param("/api/user/123/info", "/api/user/{userId}/info", (True, {"userId": "123"}), id="单路径参数"),
            pytest.param(
                "/api/user/123/order/456",
                "/api/user/{userId}/order/{orderId}",
                (True, {"userId": "123", "orderId": "456"}),
                id="多路径参数",
            ),
            pytest.param("/api/user/info", "/api/user", (False, {}), id="URL更长不匹配"),
            pytest.param("/api/user", "/api/user/info", (False, {}), id="URL更短不匹配"),
            pytest.param("/api/user/123/info", "/api/order/{userId}/info", (False, {}), id="非参数前缀段不匹配"),
            pytest.param("/api/user/123/info", "/api/user/{userId}/detail", (False, {}), id="非参数后缀段不匹配"),
            pytest.param("", "", (True, {}), id="双空URL匹配"),
            pytest.param("/", "/", (True, {}), id="根路径匹配"),
            pytest.param("", "/api/user", (False, {}), id="空URL不匹配非空模式"),
            pytest.param("/api/order/12345/detail", "/api/order/{orderId}/detail", (True, {"orderId": "12345"}), id="纯数字参数值"),
            pytest.param("/api/product/abc123", "/api/product/{productId}", (True, {"productId": "abc123"}), id="字母数字混合参数值"),
            pytest.param("https://example.com/api/user/123", "/api/user/{userId}", (False, {}), id="完整URL不匹配path模式"),
        ],
    )
    def test_match_url_pattern_forms(self, url, pattern, expected):
        assert URLMatcher.match_url_pattern(url, pattern) == expected


# ==================== 查找匹配API文件测试 ====================


class TestFindMatchingApiFile:
    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试单 API 文件查找匹配各形态")
    @pytest.mark.parametrize(
        "file_url,request_url,url_map,expected_name",
        [
            pytest.param("/api/user/info", "/api/user/info", None, "user_info.py", id="直接相等"),
            pytest.param("/api/user/{userId}/info", "/api/user/123/info", None, "user_info.py", id="路径参数模式"),
            pytest.param(
                "/api/user/{userId}/info",
                "/api/user/123/info",
                {"/api/user/123/info": "/api/user/{userId}/info"},
                "user_info.py",
                id="request_url_map转换后匹配",
            ),
            pytest.param("/api/user/info", "/api/order/list", None, None, id="无匹配"),
            # 请求 URL 带 scheme://host 前缀：应经 normalize_url 归一化（去除前缀）后命中 API 文件
            pytest.param("/api/user/info", "https://example.com/api/user/info", None, "user_info.py", id="完整URL前缀归一化"),
            # 带查询参数、无前导斜杠的请求 URL 应标准化（去 query、补斜杠）后命中 API 文件
            pytest.param("/api/user/info", "api/user/info?page=1&size=10", None, "user_info.py", id="查询参数与前导斜杠标准化"),
            # 请求 URL 为模板形式，API 文件 URL 为具体值：反向 match_url_pattern(file_url, request_url) 命中
            pytest.param("/api/user/123/info", "/api/user/{userId}/info", None, "user_123_info.py", id="反向模式匹配"),
        ],
    )
    def test_find_single_file_forms(self, tmp_path, file_url, request_url, url_map, expected_name):
        filename = expected_name or "user_info.py"
        api_file = _write_api_file(tmp_path, file_url, filename=filename)
        result = URLMatcher.find_matching_api_file(request_url, [str(api_file)], url_map)
        assert result == (str(api_file) if expected_name else None)

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
    @allure.title("测试空API文件列表")
    def test_empty_api_files_list(self):
        result = URLMatcher.find_matching_api_file("/api/user/info", [])
        assert result is None


# ==================== normalize_url 测试 ====================


class TestNormalizeUrl:
    @allure.feature("URL匹配器")
    @allure.story("URL规范化")
    @allure.title("测试 URL 规范化各形态")
    @pytest.mark.parametrize(
        "url,base_urls,expected",
        [
            pytest.param("/api/user/list?page=1&size=10", None, "/api/user/list", id="移除查询参数"),
            pytest.param("api/user/list", None, "/api/user/list", id="补开头斜杠"),
            pytest.param("https://example.com/api/user/list", ["https://example.com"], "/api/user/list", id="移除基础URL前缀"),
            pytest.param(
                "https://example.com/api/user",
                ["https://dev.example.com", "https://example.com"],
                "/api/user",
                id="多个基础URL前缀",
            ),
            pytest.param("/api/user/list", None, "/api/user/list", id="无基础URL原样保留"),
            # 绝对 URL 未匹配任何 base_url，应只保留 path 部分
            pytest.param("https://other.com/api/user/list", None, "/api/user/list", id="绝对URL无匹配base仅留path"),
            # 绝对 URL 仅 host 无 path，应回落到 "/"
            pytest.param("https://other.com", None, "/", id="仅host无path回落根路径"),
        ],
    )
    def test_normalize_url_forms(self, url, base_urls, expected):
        assert URLMatcher.normalize_url(url, base_urls=base_urls) == expected


# ==================== generate_function_name 测试 ====================


class TestGenerateFunctionName:
    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试从 URL 生成函数名各形态")
    @pytest.mark.parametrize(
        "url,expected",
        [
            pytest.param("/api/user/login", "api_user_login", id="普通URL"),
            pytest.param("/api/user/{userId}/info", "api_user_userId_info", id="带路径参数"),
            pytest.param(None, "unknown", id="None输入"),
            pytest.param("", "", id="空URL"),
        ],
    )
    def test_generate_function_name_forms(self, url, expected):
        assert URLMatcher.generate_function_name(url) == expected


# ==================== extract_url_template 测试 ====================


class TestExtractUrlTemplate:
    @allure.feature("URL匹配器")
    @allure.story("提取URL模板")
    @allure.title("测试提取 URL 模板各形态")
    @pytest.mark.parametrize(
        "url,patterns,expected",
        [
            pytest.param(
                "/api/user/123/info",
                ["/api/user/{userId}/info", "/api/order/{orderId}/detail"],
                ("/api/user/{userId}/info", {"userId": "123"}),
                id="命中模板",
            ),
            pytest.param("/api/order/list", ["/api/user/{userId}/info"], (None, {}), id="无匹配模板"),
            pytest.param("/api/user/123/info", [], (None, {}), id="空模板列表"),
        ],
    )
    def test_extract_url_template_forms(self, url, patterns, expected):
        assert URLMatcher.extract_url_template(url, patterns) == expected


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
    @allure.title("测试移除基础路径各形态")
    @pytest.mark.parametrize(
        "url,base_path,expected",
        [
            pytest.param("/swagger/api/user/login", "/swagger", "/api/user/login", id="移除基础路径"),
            pytest.param("/api/user/login", "", "/api/user/login", id="空基础路径"),
            pytest.param("/api/user/login", "/", "/api/user/login", id="根路径基础路径"),
            pytest.param("/api/user/login", "/v2", "/api/user/login", id="不匹配的基础路径"),
        ],
    )
    def test_remove_base_path_forms(self, url, base_path, expected):
        assert URLMatcher.remove_base_path(url, base_path) == expected


# ==================== _extract_path_parts 测试 ====================


class TestExtractPathParts:
    @allure.feature("URL匹配器")
    @allure.story("提取路径部分")
    @allure.title("测试提取路径部分各形态")
    @pytest.mark.parametrize(
        "url,pattern,expected",
        [
            pytest.param(
                "/api/user/123/info",
                "/api/user/{userId}/info",
                ["api", "user", "userId", "info"],
                id="含参数",
            ),
            pytest.param("/api/user/login", "/api/user/login", ["api", "user", "login"], id="无参数"),
        ],
    )
    def test_extract_path_parts_forms(self, url, pattern, expected):
        assert URLMatcher._extract_path_parts(url, pattern) == expected


# ==================== match_with_swagger 测试 ====================


class TestMatchWithSwagger:
    @allure.feature("URL匹配器")
    @allure.story("Swagger匹配")
    @allure.title("测试 Swagger 匹配各形态")
    @pytest.mark.parametrize(
        "swagger_data,url,expected",
        [
            pytest.param(None, "/api/user/123", (None, {}, []), id="无Swagger数据"),
            pytest.param({"info": {"title": "Test"}}, "/api/user/123", (None, {}, []), id="无paths字段"),
            pytest.param(
                {
                    "basePath": "/api",
                    "paths": {
                        "/user/{userId}/info": {"get": {}},
                        "/order/list": {"get": {}},
                    },
                },
                "/api/user/123/info",
                ("/api/user/{userId}/info", {"userId": "123"}, ["user", "userId", "info"]),
                id="路径命中模板",
            ),
            pytest.param(
                {
                    "basePath": "/api",
                    "paths": {
                        "/user/{userId}/info": {"get": {}},
                    },
                },
                "/api/order/list",
                (None, {}, []),
                id="不匹配",
            ),
        ],
    )
    def test_match_with_swagger_forms(self, swagger_data, url, expected):
        matcher = URLMatcher(swagger_data)
        assert matcher.match_with_swagger(url) == expected

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
        "basePath": "/demoStore",
        "paths": {
            "/mobile/demoAction/page": {"get": {}},
            "/mobile/demoAction/{id}": {"get": {}},
        },
    }

    exact = matcher.get_url_info("/demoStore/mobile/demoAction/page")
    assert exact["pattern"] == "/demoStore/mobile/demoAction/page"
    assert exact["path_params"] == {}
    assert exact["function_name"] == "demoStore_mobile_demoAction_page"

    # 具体取值（文档里没有该键）仍应命中模板并提取路径参数
    templated = matcher.get_url_info("/demoStore/mobile/demoAction/12345")
    assert templated["pattern"] == "/demoStore/mobile/demoAction/{id}"
    assert templated["path_params"] == {"id": "12345"}
