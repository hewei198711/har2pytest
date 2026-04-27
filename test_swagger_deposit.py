from har2pytest.swagger_handler import SwaggerHandler

# 初始化 SwaggerHandler
updater = SwaggerHandler()

# 获取 Swagger 文档
swagger_data = updater.get_swagger_doc('https://uc-dev.perfect99.com/sw/mall-store-application/appStore')

if swagger_data:
    print('成功获取 Swagger 文档')
    
    # 检查 /store/deposit/msg 路径
    target_path = '/store/deposit/msg'
    paths = swagger_data.get('paths', {})
    
    if target_path in paths:
        print(f'\n找到路径: {target_path}')
        path_data = paths[target_path]
        print('路径数据:', path_data)
        
        # 检查 GET 方法
        if 'get' in path_data:
            get_data = path_data['get']
            print('\nGET 方法数据:')
            print('Summary:', get_data.get('summary'))
            print('Description:', get_data.get('description'))
            print('Parameters:', get_data.get('parameters', []))
        else:
            print('\nGET 方法不存在')
    else:
        print(f'\n未找到路径: {target_path}')
else:
    print('获取 Swagger 文档失败')
