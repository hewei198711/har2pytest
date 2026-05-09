import sys

sys.path.insert(0, "d:/ligeit_github/har2pytest")

from har2pytest.utils import match_path_template


# 测试匹配逻辑
def test_match():
    # 模拟HAR文件中的请求
    har_url = "/api/appStore/store/dis/mortgageOrder/detail/96453"
    # API文件中的URL模板
    api_url = "/appStore/store/dis/mortgageOrder/detail/{id}"

    print(f"HAR URL: {har_url}")
    print(f"API URL: {api_url}")

    # 测试直接匹配
    result = match_path_template(har_url, {"paths": {api_url: {}}})
    print(f"直接匹配结果: {result}")

    # 测试移除/api前缀后的匹配
    if har_url.startswith("/api"):
        result2 = match_path_template(har_url[4:], {"paths": {api_url: {}}})
        print(f"移除/api前缀后的匹配结果: {result2}")


if __name__ == "__main__":
    test_match()
