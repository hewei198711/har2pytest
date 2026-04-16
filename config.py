# coding:utf-8


class APIConfig:
    """API配置类，包含服务包映射、默认配置和Swagger文档地址"""

    # 基础URL列表，用于解析HAR文件中的请求URL
    BASE_URLS = [
        "https://uc-test.perfect99.com/api",  # 测试环境API基础URL
        "https://uc-uat.perfect99.com/api",  # UAT环境API基础URL
    ]
    
    # 要过滤的URL关键字列表，包含这些关键字的URL将被过滤掉
    KILL_URLS = [
        "aliyuncs.com",  # 阿里云OSS URL，通常不需要测试
    ]
    
    # 路径URL列表，包含路径参数的URL模板
    PATH_URLS = [
        "/mobile/msg/manage/letter/dashbord/{usrId}",  # 消息管理仪表板URL
        "/mobile/msg/manage/letter/dashbord/{usrId}/{systemId}",  # 带系统ID的消息管理仪表板URL
        "/mobile/order/carts/getRecommendProduct/{serialNo}",  # 获取推荐产品URL
        "/mobile/order/before/by/store/{cardNo}",  # 按店铺查询订单前置信息URL
        "/mobile/order/before/by/{cardNo}",  # 按卡号查询订单前置信息URL
    ]

    # 服务包映射字典，将URL前缀映射到对应的服务包名称
    SERVICE_MAPPING = {
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
    }

    # 默认服务包名称，当无法确定服务包时使用
    DEFAULT_SERVICE_PACKAGE = 'api'

    # Swagger文档URL字典，用于获取API文档信息
    SWAGGER_DOC_URLS = {
        'mall_mgmt_application': "https://uc-test.perfect99.com/sw/mall-mgmt-application",  # 商城管理应用Swagger文档
        "mall_center_inventory": "https://uc-dev.perfect99.com/sw/mall-center-inventory",  # 商城中心库存Swagger文档
        "mall_center_store": "https://uc-dev.perfect99.com/sw/mall-center-store",  # 商城中心店铺Swagger文档
        'mall_store_application': "https://uc-dev.perfect99.com/sw/mall-store-application/appStore",  # 商城店铺应用Swagger文档
        'mall_mobile_application': "https://uc-test.perfect99.com/sw/mall-mobile-application",  # 商城移动应用Swagger文档
        'mall-center-seckill': "https://uc-dev.perfect99.com/sw/mall-center-seckill",  # 商城中心秒杀Swagger文档
        'settle_job': "https://uc-dev.perfect99.com/sw/settle-job",  # 结算任务Swagger文档
        'mall_center_user': "https://uc-dev.perfect99.com/sw/mall-center-user",  # 商城中心用户Swagger文档
        "mall_center_member": "https://uc-test.perfect99.com/sw/mall-center-member",  # 商城中心会员Swagger文档
    }

    # 无效参数集合，这些参数将在生成测试用例时被过滤掉
    INVALID_PARAMS = {
        'rnd', 'timestamp', '_t', '_timestamp', 'v', 'version',  # 时间戳和版本参数
        'channelType',  # 渠道类型参数
    }

    # 列表查询用例，这些参数不进行参数化处理
    PAGINATION_PARAMS = ['pageNum', 'pageSize',  "commitEndTime", "commitStartTime", "header"]

    # 测试用例目录，生成的测试用例文件将保存在此目录下
    TESTCASE_DIR = "testcases"

    @staticmethod
    def determine_service_package(url: str) -> str:
        """
        根据URL的第一个字段判断属于哪个微服务包
        """
        if not url:
            return APIConfig.DEFAULT_SERVICE_PACKAGE

        if '?' in url:
            url = url.split('?')[0]

        if url.startswith('/'):
            url = url[1:]

        first_segment = url.split('/')[0].lower()

        for prefix, package in APIConfig.SERVICE_MAPPING.items():
            if first_segment.startswith(prefix):
                return package

        return APIConfig.DEFAULT_SERVICE_PACKAGE
