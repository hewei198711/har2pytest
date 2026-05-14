from har2pytest.url_matcher import URLMatcher


class TestMatchUrlPattern:
    """match_url_pattern 函数测试"""

    def test_exact_match_without_params(self):
        """测试无路径参数的完全匹配"""
        matched, params = URLMatcher.match_url_pattern("/api/user/info", "/api/user/info")
        assert matched is True
        assert params == {}

    def test_match_with_path_param(self):
        """测试带路径参数的匹配"""
        matched, params = URLMatcher.match_url_pattern("/api/user/123/info", "/api/user/{userId}/info")
        assert matched is True
        assert params == {"userId": "123"}

    def test_match_with_multiple_path_params(self):
        """测试多个路径参数的匹配"""
        matched, params = URLMatcher.match_url_pattern("/api/user/123/order/456", "/api/user/{userId}/order/{orderId}")
        assert matched is True
        assert params == {"userId": "123", "orderId": "456"}

    def test_length_mismatch(self):
        """测试URL长度不同时不匹配"""
        matched, params = URLMatcher.match_url_pattern("/api/user/info", "/api/user")
        assert matched is False
        assert params == {}
        
        matched, params = URLMatcher.match_url_pattern("/api/user", "/api/user/info")
        assert matched is False
        assert params == {}

    def test_non_param_part_mismatch(self):
        """测试非参数部分不匹配"""
        matched, params = URLMatcher.match_url_pattern("/api/user/123/info", "/api/order/{userId}/info")
        assert matched is False
        assert params == {}
        
        matched, params = URLMatcher.match_url_pattern("/api/user/123/info", "/api/user/{userId}/detail")
        assert matched is False
        assert params == {}

    def test_empty_url(self):
        """测试空URL"""
        matched, params = URLMatcher.match_url_pattern("", "")
        assert matched is True
        assert params == {}
        
        matched, params = URLMatcher.match_url_pattern("/", "/")
        assert matched is True
        assert params == {}
        
        matched, params = URLMatcher.match_url_pattern("", "/api/user")
        assert matched is False
        assert params == {}

    def test_numeric_param_value(self):
        """测试数字类型的路径参数值"""
        matched, params = URLMatcher.match_url_pattern("/api/order/12345/detail", "/api/order/{orderId}/detail")
        assert matched is True
        assert params == {"orderId": "12345"}
        
        matched, params = URLMatcher.match_url_pattern("/api/product/abc123", "/api/product/{productId}")
        assert matched is True
        assert params == {"productId": "abc123"}

    def test_full_url_vs_pattern(self):
        """测试完整URL与模式的匹配（不应该匹配，因为长度不同）"""
        # 完整URL包含协议域名，长度不同
        matched, params = URLMatcher.match_url_pattern("https://example.com/api/user/123", "/api/user/{userId}")
        assert matched is False
        assert params == {}


class TestFindMatchingApiFile:
    """find_matching_api_file 函数测试"""

    def test_exact_match(self, tmp_path):
        """测试直接相等匹配"""
        api_dir = tmp_path / "apis"
        api_dir.mkdir()
        
        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, access_token=access_token):
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


    def test_path_param_pattern_match(self, tmp_path):
        """测试路径参数模式匹配"""
        api_dir = tmp_path / "apis"
        api_dir.mkdir()
        
        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, access_token=access_token):
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

    def test_transformed_url_match(self, tmp_path):
        """测试转换后URL匹配（来自Swagger映射）"""
        api_dir = tmp_path / "apis"
        api_dir.mkdir()
        
        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, access_token=access_token):
    """
    用户信息
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        # 模拟Swagger映射：原始URL -> 模板URL
        request_url_map = {
            "/api/user/123/info": "/api/user/{userId}/info"
        }
        
        result = URLMatcher.find_matching_api_file("/api/user/123/info", [str(api_file)], request_url_map)
        assert result == str(api_file)

    def test_no_matching_file(self, tmp_path):
        """测试无匹配文件"""
        api_dir = tmp_path / "apis"
        api_dir.mkdir()
        
        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, access_token=access_token):
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

    def test_multiple_api_files_priority(self, tmp_path):
        """测试多个API文件时的匹配优先级"""
        api_dir = tmp_path / "apis"
        api_dir.mkdir()
        
        # 创建两个API文件
        api_file1 = api_dir / "_user_info.py"
        with open(api_file1, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, access_token=access_token):
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
            f.write('''def _user_info_param(data=data, access_token=access_token):
    """
    用户信息带参数
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        # 直接相等应该优先
        result = URLMatcher.find_matching_api_file("/api/user/info", [str(api_file1), str(api_file2)])
        assert result == str(api_file1)

    def test_full_url_with_base_url_stripped(self, tmp_path):
        """测试完整URL（已被HAR解析器清理前缀后）"""
        api_dir = tmp_path / "apis"
        api_dir.mkdir()
        
        api_file = api_dir / "_user_info.py"
        with open(api_file, "w", encoding="utf-8") as f:
            f.write('''def _user_info(data=data, access_token=access_token):
    """
    用户信息
    /api/user/{userId}/info
    """
    url = "/api/user/{userId}/info"
    headers = {}
    with client.get(url=url, headers=headers, params=data) as r:
        return r
''')

        # 模拟HAR解析器已移除base_url前缀的情况
        result = URLMatcher.find_matching_api_file("/api/user/123/info", [str(api_file)])
        assert result == str(api_file)

    def test_empty_api_files_list(self):
        """测试空API文件列表"""
        result = URLMatcher.find_matching_api_file("/api/user/info", [])
        assert result is None
