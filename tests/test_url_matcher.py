import allure

from har2pytest.url_matcher import URLMatcher


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


class TestFindMatchingApiFile:
    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试直接相等匹配")
    def test_exact_match(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, token=token):
    """
    用户信息
    /api/user/info
    """
    url = "/api/user/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file)])
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试路径参数模式匹配")
    def test_path_param_pattern_match(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, token=token):
    """
    用户信息
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        result = URLMatcher.find_matching_api_file("/api/user/123/info", [str(api_file)])
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试转换后URL匹配")
    def test_transformed_url_match(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, token=token):
    """
    用户信息
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        request_url_map = {"/api/user/123/info": "/api/user/{userId}/info"}

        result = URLMatcher.find_matching_api_file("/api/user/123/info", [str(api_file)], request_url_map)
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试无匹配文件")
    def test_no_matching_file(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, token=token):
    """
    用户信息
    /api/user/info
    """
    url = "/api/user/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        result = URLMatcher.find_matching_api_file("/api/order/list", [str(api_file)])
        assert result is None

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试多个API文件时的匹配优先级")
    def test_multiple_api_files_priority(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file1 = api_dir / "_user_info.py"
        with open(api_file1, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, token=token):
    """
    用户信息
    /api/user/info
    """
    url = "/api/user/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        api_file2 = api_dir / "_user_info_param.py"
        with open(api_file2, "w", encoding="utf-8") as f:
            f.write('''def _user_info_param(data=data, token=token):
    """
    用户信息带参数
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file1), str(api_file2)])
        assert result == str(api_file1)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试完整URL匹配（已清理前缀）")
    def test_full_url_with_base_url_stripped(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, token=token):
    """
    用户信息
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        result = URLMatcher.find_matching_api_file("/api/user/123/info", [str(api_file)])
        assert result == str(api_file)

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件")
    @allure.title("测试空API文件列表")
    def test_empty_api_files_list(self):
        result = URLMatcher.find_matching_api_file("/api/user/info", [])
        assert result is None


# ==================== _has_numeric_path_segment 测试 ====================

class TestHasNumericPathSegment:
    @allure.feature("URL匹配器")
    @allure.story("数字路径段检测")
    @allure.title("测试包含纯数字路径段")
    def test_pure_numeric_segment(self):
        matcher = URLMatcher()
        assert matcher._has_numeric_path_segment("/api/user/123/info") is True
        assert matcher._has_numeric_path_segment("/order/45678") is True

    @allure.feature("URL匹配器")
    @allure.story("数字路径段检测")
    @allure.title("测试包含3位以上数字的路径段")
    def test_long_numeric_segment(self):
        matcher = URLMatcher()
        assert matcher._has_numeric_path_segment("/api/product/abc123def") is True

    @allure.feature("URL匹配器")
    @allure.story("数字路径段检测")
    @allure.title("测试无数字路径段")
    def test_no_numeric_segment(self):
        matcher = URLMatcher()
        assert matcher._has_numeric_path_segment("/api/user/info") is False
        assert matcher._has_numeric_path_segment("/api/user/list") is False

    @allure.feature("URL匹配器")
    @allure.story("数字路径段检测")
    @allure.title("测试短数字路径段（仅1位数字不匹配）")
    def test_short_numeric_segment(self):
        matcher = URLMatcher()
        assert matcher._has_numeric_path_segment("/api/ab1") is False


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
        result = URLMatcher.normalize_url(
            "https://example.com/api/user/list",
            base_urls=["https://example.com"]
        )
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


# ==================== generate_function_name 测试 ====================

class TestGenerateFunctionName:
    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试从普通URL生成函数名")
    def test_normal_url(self):
        result = URLMatcher.generate_function_name("/api/user/login")
        assert result == "_api_user_login"

    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试从带路径参数的URL生成函数名")
    def test_url_with_path_params(self):
        result = URLMatcher.generate_function_name("/api/user/{userId}/info")
        assert result == "_api_user_userId_info"

    @allure.feature("URL匹配器")
    @allure.story("生成函数名")
    @allure.title("测试None输入")
    def test_none_url(self):
        result = URLMatcher.generate_function_name(None)
        assert result == "_unknown"

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
        assert result["has_path_params"] is False
        assert result["function_name"] is not None

    @allure.feature("URL匹配器")
    @allure.story("获取URL信息")
    @allure.title("测试带数字路径的URL（从配置匹配）")
    def test_url_with_numeric_path(self):
        matcher = URLMatcher()
        result = matcher.get_url_info("/api/user/12345/info")
        assert result["original_url"] == "/api/user/12345/info"

    @allure.feature("URL匹配器")
    @allure.story("获取URL信息")
    @allure.title("测试URL信息缓存")
    def test_url_info_cache(self):
        matcher = URLMatcher()
        result1 = matcher.get_url_info("/api/user/login")
        result2 = matcher.get_url_info("/api/user/login")
        assert result1 == result2


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


# ==================== _add_base_path 测试 ====================

class TestAddBasePath:
    @allure.feature("URL匹配器")
    @allure.story("添加基础路径")
    @allure.title("测试添加基础路径")
    def test_add_base_path(self):
        result = URLMatcher._add_base_path("/api/user/login", "/swagger")
        assert result == "/swagger/api/user/login"

    @allure.feature("URL匹配器")
    @allure.story("添加基础路径")
    @allure.title("测试空基础路径")
    def test_empty_base_path(self):
        result = URLMatcher._add_base_path("/api/user/login", "")
        assert result == "/api/user/login"

    @allure.feature("URL匹配器")
    @allure.story("添加基础路径")
    @allure.title("测试根路径基础路径")
    def test_root_base_path(self):
        result = URLMatcher._add_base_path("/api/user/login", "/")
        assert result == "/api/user/login"


# ==================== _extract_path_parts 测试 ====================

class TestExtractPathParts:
    @allure.feature("URL匹配器")
    @allure.story("提取路径部分")
    @allure.title("测试提取路径部分（含参数）")
    def test_extract_with_params(self):
        result = URLMatcher._extract_path_parts(
            "/api/user/123/info", "/api/user/{userId}/info"
        )
        assert result == ["api", "user", "userId", "info"]

    @allure.feature("URL匹配器")
    @allure.story("提取路径部分")
    @allure.title("测试提取路径部分（无参数）")
    def test_extract_without_params(self):
        result = URLMatcher._extract_path_parts(
            "/api/user/login", "/api/user/login"
        )
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
            }
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
            }
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
            }
        }
        matcher = URLMatcher(swagger_data)
        result1 = matcher.match_with_swagger("/user/123/info")
        result2 = matcher.match_with_swagger("/user/123/info")
        assert result1 == result2


# ==================== find_matching_api_file 边缘测试 ====================

class TestFindMatchingApiFileEdge:
    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件-边缘")
    @allure.title("测试URL标准化匹配")
    def test_normalized_url_match(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, token=token):
    """
    用户信息
    /api/user/info
    """
    url = "/api/user/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        # 带查询参数的URL应该匹配到标准化的API文件URL
        result = URLMatcher.find_matching_api_file("api/user/info", [str(api_file)])
        assert result is not None

    @allure.feature("URL匹配器")
    @allure.story("查找匹配API文件-边缘")
    @allure.title("测试API文件无URL")
    def test_api_file_no_url(self, tmp_path):
        api_dir = tmp_path / "apis"
        api_dir.mkdir()

        api_file = api_dir / "_no_url.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _no_url(data=data, token=token):
    """
    无URL
    """
    url = None
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file)])
        assert result is None