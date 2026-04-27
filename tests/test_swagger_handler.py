# coding:utf-8
"""
测试 swagger_updater.py 模块
"""

import pytest
import allure
import os
from har2pytest.swagger_handler import SwaggerHandler
from har2pytest.config import APIConfig


@allure.feature("Swagger文档更新器")
@allure.story("确定服务包")
def test_determine_service_package():
    """测试根据URL判断服务包"""
    # 触发配置初始化
    APIConfig.get_config('SERVICE_MAPPING')

    # 临时设置 SERVICE_MAPPING 配置
    original_service_mapping = APIConfig._config.get('SERVICE_MAPPING', {})
    APIConfig._config['SERVICE_MAPPING'] = {
        "mobile": "mall_mobile_application",
        "user": "mall_center_user"
    }

    try:
        assert APIConfig.determine_service_package("/mobile/trade/orderCommit") == "mall_mobile_application"
        assert APIConfig.determine_service_package("/user/123/info") == "mall_center_user"
        assert APIConfig.determine_service_package("") == "apis"
    finally:
        # 恢复原始配置
        APIConfig._config['SERVICE_MAPPING'] = original_service_mapping


@allure.feature("Swagger文档更新器")
@allure.story("在Swagger中查找API信息")
def test_find_api_info_in_swagger():
    """测试在Swagger文档中查找API信息"""
    updater = SwaggerHandler()

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
@allure.story("带basePath的API路径匹配")
def test_find_api_info_with_basepath():
    """测试带basePath的API路径匹配"""
    updater = SwaggerHandler()

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
    updater = SwaggerHandler()

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