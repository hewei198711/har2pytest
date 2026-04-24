# coding:utf-8
"""
测试 swagger_updater.py 模块
"""

import pytest
import allure
import os
from har2pytest.swagger_updater import SwaggerDocUpdater
from har2pytest.config import APIConfig


@allure.feature("Swagger文档更新器")
@allure.story("确定服务包")
def test_determine_service_package():
    """测试根据URL判断服务包"""
    assert APIConfig.determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"
    assert APIConfig.determine_service_package("/user/123/info") == "mall_center_user"
    assert APIConfig.determine_service_package("") == "apis"


@allure.feature("Swagger文档更新器")
@allure.story("在Swagger中查找API信息")
def test_find_api_info_in_swagger():
    """测试在Swagger文档中查找API信息"""
    updater = SwaggerDocUpdater()
    
    # 测试Swagger数据
    swagger_data = {
        "paths": {
            "/user/login": {
                "post": {
                    "summary": "用户登录",
                    "description": "用户登录接口",
                    "parameters": [
                        {
                            "name": "username",
                            "description": "用户名"
                        },
                        {
                            "name": "password",
                            "description": "密码"
                        }
                    ]
                }
            }
        }
    }
    
    # 测试查找存在的API
    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")
    assert api_info["summary"] == "用户登录"
    assert api_info["description"] == "用户登录接口"
    assert api_info["parameters"]["username"] == "用户名"
    assert api_info["parameters"]["password"] == "密码"
    
    # 测试查找不存在的API
    api_info = updater.find_api_info_in_swagger(swagger_data, "/nonexistent", "GET")
    assert api_info["summary"] == ""
    assert api_info["description"] == ""
    assert api_info["parameters"] == {}


@allure.feature("Swagger文档更新器")
@allure.story("更新API文件")
def test_update_api_file():
    """测试更新API文件"""
    updater = SwaggerDocUpdater()
    
    # 创建测试API文件
    test_content = """
# coding:utf-8

from setting import TIMEOUT, VERIFY, access_token
from util.client import client

data = {
    "username": "test", # TODO: 添加参数说明
    "password": "123456" # TODO: 添加参数说明
}

def _user_login(data=data, access_token=access_token):
    \"\"\"
    TODO: 添加接口描述
    /user/login
    \"\"\"
    url = "/user/login"
    headers = {"Authorization": f"bearer {access_token}"}
    with client.post(url=url, headers=headers, json=data) as r:
        return r
"""
    
    with open("test_api.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        # 测试API信息
        api_info = {
            "summary": "用户登录",
            "description": "用户登录接口",
            "parameters": {
                "username": "用户名",
                "password": "密码"
            }
        }
        
        # 确保文件存在
        import os
        assert os.path.exists("test_api.py")
        
        # 更新文件
        result = updater.update_api_file("test_api.py", api_info)
        assert result is True
        
        # 验证更新结果
        with open("test_api.py", "r", encoding="utf-8") as f:
            updated_content = f.read()
        
        assert "用户登录" in updated_content
        assert "# 用户名" in updated_content
        assert "# 密码" in updated_content
    finally:
        if os.path.exists("test_api.py"):
            os.remove("test_api.py")


@allure.feature("Swagger文档更新器")
@allure.story("带basePath的API路径匹配")
def test_find_api_info_with_basepath():
    """测试带basePath的API路径匹配"""
    updater = SwaggerDocUpdater()
    
    # 测试带basePath的Swagger数据
    swagger_data = {
        "basePath": "/appStore",
        "paths": {
            "/storage/upload": {
                "post": {
                    "summary": "文件上传",
                    "description": "文件上传接口",
                    "parameters": [
                        {
                            "name": "storageType",
                            "description": "存储类型"
                        },
                        {
                            "name": "clientKey",
                            "description": "客户端密钥"
                        }
                    ]
                }
            }
        }
    }
    
    # 测试带basePath的API路径
    api_info = updater.find_api_info_in_swagger(swagger_data, "/appStore/storage/upload", "POST")
    assert api_info["summary"] == "文件上传"
    assert api_info["description"] == "文件上传接口"
    assert api_info["parameters"]["storageType"] == "存储类型"
    assert api_info["parameters"]["clientKey"] == "客户端密钥"


@allure.feature("Swagger文档更新器")
@allure.story("模型引用处理")
def test_model_reference_handling():
    """测试模型引用处理"""
    updater = SwaggerDocUpdater()
    
    # 测试带模型引用的Swagger数据
    swagger_data = {
        "paths": {
            "/user/login": {
                "post": {
                    "summary": "用户登录",
                    "description": "用户登录接口",
                    "parameters": [
                        {
                            "name": "dto",
                            "in": "body",
                            "schema": {
                                "$ref": "#/definitions/LoginRequest"
                            }
                        }
                    ]
                }
            }
        },
        "definitions": {
            "LoginRequest": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "用户名"
                    },
                    "password": {
                        "type": "string",
                        "description": "密码"
                    }
                }
            }
        }
    }
    
    # 测试模型引用处理
    api_info = updater.find_api_info_in_swagger(swagger_data, "/user/login", "POST")
    assert api_info["summary"] == "用户登录"
    assert api_info["description"] == "用户登录接口"
    assert api_info["parameters"]["username"] == "用户名"
    assert api_info["parameters"]["password"] == "密码"
