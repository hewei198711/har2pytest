# coding:utf-8
"""
调试 Swagger 文档结构的测试文件
"""
import json
import urllib.request
from har2pytest.swagger_updater import SwaggerDocUpdater
from har2pytest.config import APIConfig


def debug_swagger_doc():
    """
    调试 Swagger 文档结构
    """
    print("=" * 80)
    print("开始调试 Swagger 文档结构")
    print("=" * 80)
    
    # 初始化 SwaggerDocUpdater
    updater = SwaggerDocUpdater()
    
    # 获取服务包对应的 Swagger 文档 URL
    service_packages = APIConfig.SWAGGER_DOC_URLS()
    if not service_packages:
        print("\n❌ 未配置 Swagger 文档 URL，请在配置文件中设置 SWAGGER_DOC_URLS")
        return
    
    # 选择第一个服务包进行测试
    test_package = list(service_packages.keys())[0]
    test_url = service_packages[test_package]
    print(f"\n测试服务包: {test_package}")
    print(f"Swagger 文档 URL: {test_url}")
    
    # 获取 Swagger 文档
    print("\n正在获取 Swagger 文档...")
    swagger_data = updater.get_swagger_doc(test_url)
    
    if not swagger_data:
        print("\n❌ 无法获取 Swagger 文档")
        return
    
    # 打印文档基本结构
    print("\n" + "-" * 80)
    print("Swagger 文档基本结构:")
    print("-" * 80)
    print(f"文档类型: {swagger_data.get('openapi', swagger_data.get('swagger', 'Unknown'))}")
    print(f"标题: {swagger_data.get('info', {}).get('title', 'Unknown')}")
    print(f"版本: {swagger_data.get('info', {}).get('version', 'Unknown')}")
    print(f"路径数量: {len(swagger_data.get('paths', {}))}")
    
    # 打印前 5 个路径
    print("\n前 5 个 API 路径:")
    paths = list(swagger_data.get('paths', {}).keys())
    for i, path in enumerate(paths[:5]):
        print(f"  {i+1}. {path}")
    
    if paths:
        # 选择第一个路径进行测试
        test_path = paths[0]
        print(f"\n测试 API 路径: {test_path}")
        
        # 查找 API 信息
        api_info = updater.find_api_info_in_swagger(swagger_data, test_path)
        
        # 打印 API 信息
        print("\n" + "-" * 80)
        print("API 信息:")
        print("-" * 80)
        print(f"摘要: {api_info.get('summary', '无')}")
        print(f"描述: {api_info.get('description', '无')}")
        print(f"参数数量: {len(api_info.get('parameters', {}))}")
        
        if api_info.get('parameters'):
            print("\n参数说明:")
            for param, desc in api_info.get('parameters', {}).items():
                print(f"  {param}: {desc}")


if __name__ == "__main__":
    # debug_swagger_doc()
    url = "https://uc-dev.perfect99.com/sw/settle-job/v2/api-docs"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"paths 字段存在: {'paths' in data}")
        print(f"paths 数量: {len(data.get('paths', {}))}")