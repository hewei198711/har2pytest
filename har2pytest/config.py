# coding:utf-8
import os
import json
from typing import List, Dict, Set, Optional

from .logger import logger


class APIConfig:
    """API配置类，包含服务包映射、默认配置和Swagger文档地址"""

    # 默认配置
    _default_config = {
        # 基础URL列表，用于解析HAR文件中的请求URL
        'BASE_URLS': [
            "https://uc-test.perfect99.com/api",  # 测试环境API基础URL
            "https://uc-uat.perfect99.com/api",  # UAT环境API基础URL
        ],
        
        # 要过滤的URL关键字列表，包含这些关键字的URL将被过滤掉
        'KILL_URLS': [
            "aliyuncs.com",  # 阿里云OSS URL，通常不需要测试
        ],
        
        # 路径URL列表，包含路径参数的URL模板
        'PATH_URLS': [
            "/mobile/msg/manage/letter/dashbord/{usrId}",  # 消息管理仪表板URL
            "/mobile/msg/manage/letter/dashbord/{usrId}/{systemId}",  # 带系统ID的消息管理仪表板URL
            "/mobile/order/carts/getRecommendProduct/{serialNo}",  # 获取推荐产品URL
            "/mobile/order/before/by/store/{cardNo}",  # 按店铺查询订单前置信息URL
            "/mobile/order/before/by/{cardNo}",  # 按卡号查询订单前置信息URL
        ],

        # 服务包映射字典，将URL前缀映射到对应的服务包名称
        'SERVICE_MAPPING': {
            'appstore': 'mall_store_application',  # 应用商店服务
            'store': 'mall_center_store',  # 商城中心店铺服务
            'mobile': 'mall_mobile_application',  # 商城移动应用服务
            'member': 'mall_center_member',  # 商城中心会员服务
            'invt': 'mall_center_inventory',  # 商城中心库存服务
            'mgmt': 'mall_mgmt_application',  # 商城管理应用服务
            'seckill': 'mall_center_seckill',  # 商城中心秒杀服务
            'user': 'mall_center_user',  # 商城中心用户服务
            'xxl': 'basic_services',  # XXL任务服务
            'storage': 'basic_services',  # 存储服务
            'oss': 'oss_json'  # OSS JSON服务
        },

        # 默认服务包名称，当无法确定服务包时使用
        'DEFAULT_SERVICE_PACKAGE': 'custom_api',

        # Swagger文档URL字典，用于获取API文档信息
        'SWAGGER_DOC_URLS': {
            'mall_mgmt_application': "https://uc-test.perfect99.com/sw/mall-mgmt-application",  # 商城管理应用Swagger文档
            "mall_center_inventory": "https://uc-dev.perfect99.com/sw/mall-center-inventory",  # 商城中心库存Swagger文档
            "mall_center_store": "https://uc-dev.perfect99.com/sw/mall-center-store",  # 商城中心店铺Swagger文档
            'mall_store_application': "https://uc-dev.perfect99.com/sw/mall-store-application/appStore",  # 商城店铺应用Swagger文档
            'mall_mobile_application': "https://uc-test.perfect99.com/sw/mall-mobile-application",  # 商城移动应用Swagger文档
            'mall-center-seckill': "https://uc-dev.perfect99.com/sw/mall-center-seckill",  # 商城中心秒杀Swagger文档
            'settle_job': "https://uc-dev.perfect99.com/sw/settle-job",  # 结算任务Swagger文档
            'mall_center_user': "https://uc-dev.perfect99.com/sw/mall-center-user",  # 商城中心用户Swagger文档
            "mall_center_member": "https://uc-test.perfect99.com/sw/mall-center-member",  # 商城中心会员Swagger文档
        },

        # 无效参数集合，这些参数将在生成测试用例时被过滤掉
        'INVALID_PARAMS': {
            'nonce', 'sign', 'timestamp', 'partnerKey',  # 测试期望的参数
        },

        # 列表查询用例，这些参数不进行参数化处理
        'PAGINATION_PARAMS': ['pageNum', 'pageSize',  "commitEndTime", "commitStartTime", "header"],

        # 测试用例目录，生成的测试用例文件将保存在此目录下
        'TESTCASE_DIR': "testcases",
        
        # Swagger文档配置
        'SWAGGER_FILE': "swagger.json",
        'SWAGGER_HOST': "https://api.example.com",
        'SWAGGER_BASE_PATH': "/api",
        'SWAGGER_TITLE': "API Documentation",
        'SWAGGER_VERSION': "1.0.0"
    }

    # 初始化配置
    @classmethod
    def _load_config(cls):
        """加载配置，优先从环境变量和配置文件读取"""
        config = cls._default_config.copy()

        # 尝试从环境变量读取配置文件路径
        config_file = os.environ.get('HAR2PYTEST_CONFIG')
        if not config_file:
            # 默认配置文件路径
            config_file = os.path.join(os.getcwd(), 'har2pytest_config.json')

        logger.info(f"配置文件路径: {config_file}")
        logger.info(f"配置文件是否存在: {os.path.exists(config_file)}")

        # 尝试从配置文件读取
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    config.update(user_config)
                    logger.info(f"成功加载配置文件，DEFAULT_SERVICE_PACKAGE: {config.get('DEFAULT_SERVICE_PACKAGE')}")
            except Exception as e:
                # 配置文件读取失败，使用默认配置
                logger.warning(f"配置文件 {config_file} 读取失败: {str(e)}，将使用默认配置")
        else:
            # 配置文件不存在，使用默认配置
            logger.warning(f"未找到配置文件 {config_file}，将使用默认配置，这可能不符合您的实际要求")

        # 转换集合类型
        if isinstance(config.get('INVALID_PARAMS'), list):
            config['INVALID_PARAMS'] = set(config['INVALID_PARAMS'])

        return config

    # 类属性访问器
    @classmethod
    def get_config(cls, key):
        """获取配置值"""
        if not hasattr(cls, '_config'):
            cls._config = cls._load_config()
        if cls._config is None:
            return cls._default_config.get(key)
        return cls._config.get(key, cls._default_config.get(key))

    # 类属性访问方法
    @classmethod
    def BASE_URLS(cls) -> List[str]:
        return cls.get_config('BASE_URLS')

    @classmethod
    def KILL_URLS(cls) -> List[str]:
        return cls.get_config('KILL_URLS')

    @classmethod
    def PATH_URLS(cls) -> List[str]:
        return cls.get_config('PATH_URLS')

    @classmethod
    def SERVICE_MAPPING(cls) -> Dict[str, str]:
        return cls.get_config('SERVICE_MAPPING')

    @classmethod
    def DEFAULT_SERVICE_PACKAGE(cls) -> str:
        return cls.get_config('DEFAULT_SERVICE_PACKAGE')

    @classmethod
    def SWAGGER_DOC_URLS(cls) -> Dict[str, str]:
        return cls.get_config('SWAGGER_DOC_URLS')

    @classmethod
    def INVALID_PARAMS(cls) -> Set[str]:
        return cls.get_config('INVALID_PARAMS')

    @classmethod
    def PAGINATION_PARAMS(cls) -> List[str]:
        return cls.get_config('PAGINATION_PARAMS')

    @classmethod
    def TESTCASE_DIR(cls) -> str:
        return cls.get_config('TESTCASE_DIR')

    @classmethod
    def DEFAULT_TESTCASE_DIR(cls) -> str:
        return cls.get_config('TESTCASE_DIR')

    @classmethod
    def SWAGGER_FILE(cls) -> str:
        return cls.get_config('SWAGGER_FILE')

    @classmethod
    def SWAGGER_HOST(cls) -> str:
        return cls.get_config('SWAGGER_HOST')

    @classmethod
    def SWAGGER_BASE_PATH(cls) -> str:
        return cls.get_config('SWAGGER_BASE_PATH')

    @classmethod
    def SWAGGER_TITLE(cls) -> str:
        return cls.get_config('SWAGGER_TITLE')

    @classmethod
    def SWAGGER_VERSION(cls) -> str:
        return cls.get_config('SWAGGER_VERSION')

    @classmethod
    def determine_service_package(cls, url: str) -> str:
        """
        根据URL的第一个字段判断属于哪个微服务包
        """
        if not url:
            return cls.DEFAULT_SERVICE_PACKAGE()

        if '?' in url:
            url = url.split('?')[0]

        if url.startswith('/'):
            url = url[1:]

        first_segment = url.split('/')[0].lower()

        for prefix, package in cls.SERVICE_MAPPING().items():
            if first_segment.startswith(prefix):
                return package

        return cls.DEFAULT_SERVICE_PACKAGE()
