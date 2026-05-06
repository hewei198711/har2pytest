import json
import os

from .logger import logger


class APIConfig:
    """API配置类，包含服务包映射、默认配置和Swagger文档地址"""

    # 默认配置
    _default_config = {
        # 基础URL列表，用于解析HAR文件中的请求URL
        "BASE_URLS": [],
        # 要过滤的URL关键字列表，包含这些关键字的URL将被过滤掉
        "KILL_URLS": [],
        # 路径URL列表，包含路径参数的URL模板
        "PATH_URLS": [],
        # 服务包映射字典，将URL前缀映射到对应的服务包名称
        "SERVICE_MAPPING": {},
        # 默认服务包名称，当无法确定服务包时使用
        "DEFAULT_SERVICE_PACKAGE": "apis",
        # Swagger文档URL字典，用于获取API文档信息
        "SWAGGER_DOC_URLS": {},
        # 无效参数集合，这些参数将在生成测试用例时被过滤掉
        "INVALID_PARAMS": set(),
        # 需要收录的headers参数及其默认值，用于生成测试用例时的headers
        "HEADERS_TO_INCLUDE": {
            "authorization": "bearer {os.environ['access_token']}",
        },
        # 必须包含的headers字段及其默认值
        "REQUIRED_HEADERS": {},
        # 列表查询用例，这些参数不进行参数化处理
        "PAGINATION_PARAMS": [],
        # 测试用例目录，生成的测试用例文件将保存在此目录下
        "TESTCASE_DIR": "testcases",
        # Swagger文档配置
        "SWAGGER_FILE": "swagger.json",
        "SWAGGER_HOST": "https://api.example.com",
        "SWAGGER_BASE_PATH": "/api",
        "SWAGGER_TITLE": "API Documentation",
        "SWAGGER_VERSION": "1.0.0",
    }

    # 初始化配置
    _config = None
    _config_warned = False
    _config_file_exists = False

    @classmethod
    def _load_config(cls):
        """加载配置，优先从环境变量和配置文件读取"""
        config = cls._default_config.copy()
        config_file_exists = False

        # 尝试从环境变量读取配置文件路径
        config_file = os.environ.get("HAR2PYTEST_CONFIG")
        if not config_file:
            # 默认配置文件路径
            config_file = os.path.join(os.getcwd(), "har2pytest_config.json")

        logger.info(f"配置文件路径: {config_file}")
        logger.info(f"配置文件是否存在: {os.path.exists(config_file)}")

        # 尝试从配置文件读取
        if os.path.exists(config_file):
            config_file_exists = True
            try:
                with open(config_file, encoding="utf-8") as f:
                    user_config = json.load(f)
                    config.update(user_config)
                    logger.info(f"成功加载配置文件，DEFAULT_SERVICE_PACKAGE: {config.get('DEFAULT_SERVICE_PACKAGE')}")
            except Exception as e:
                # 配置文件读取失败，使用默认配置
                config_file_exists = False
                logger.warning(f"配置文件 {config_file} 读取失败: {str(e)}，将使用默认配置")
        else:
            # 配置文件不存在，使用默认配置
            logger.warning(f"未找到配置文件 {config_file}，将使用默认配置，这可能不符合您的实际要求")

        # 转换集合类型
        if isinstance(config.get("INVALID_PARAMS"), list):
            config["INVALID_PARAMS"] = set(config["INVALID_PARAMS"])

        # 如果 HEADERS_TO_INCLUDE 是列表格式，转换为字典格式（兼容旧配置）
        if isinstance(config.get("HEADERS_TO_INCLUDE"), list):
            headers_dict = {}
            for header in config["HEADERS_TO_INCLUDE"]:
                # 使用默认值
                default_values = {
                    "authorization": "bearer {os.environ['access_token']}",
                    "channel": "pc",
                    "client": "op",
                    "content-type": "application/json;charset=UTF-8",
                }
                headers_dict[header] = default_values.get(header, "")
            config["HEADERS_TO_INCLUDE"] = headers_dict

        return config, config_file_exists

    @classmethod
    def _warn_missing_config(cls):
        """提示用户创建配置文件"""
        if cls._config_warned:
            return

        cls._config_warned = True
        logger.warning("=" * 60)
        logger.warning("未找到配置文件 har2pytest_config.json，请创建并配置")
        logger.warning("=" * 60)
        logger.warning("配置示例:")
        logger.warning("""{
    "BASE_URLS": ["https://api.example.com"],
    "SERVICE_MAPPING": {
        "mobile": "mall_mobile_application",
        "user": "mall_center_user"
    },
    "DEFAULT_SERVICE_PACKAGE": "apis",
    "PATH_URLS": ["/user/{id}/info"],
    "SWAGGER_DOC_URLS": {
        "mall-mobile-application": "https://api.example.com/swagger/mall-mobile-application"
    },
    "INVALID_PARAMS": ["sign", "token"],
    "HEADERS_TO_INCLUDE": ["content-type", "authorization"],
    "REQUIRED_HEADERS": {},
    "PAGINATION_PARAMS": ["pageNum", "pageSize"]
}""")
        logger.warning("=" * 60)

    # 类属性访问器
    @classmethod
    def get_config(cls, key):
        """获取配置值"""
        if cls._config is None:
            cls._config, config_file_exists = cls._load_config()
            # 只有当配置文件不存在时才显示警告
            if not config_file_exists:
                cls._warn_missing_config()
        return cls._config.get(key, cls._default_config.get(key))

    # 类属性访问方法
    @classmethod
    def BASE_URLS(cls) -> list[str]:
        return cls.get_config("BASE_URLS")

    @classmethod
    def KILL_URLS(cls) -> list[str]:
        return cls.get_config("KILL_URLS")

    @classmethod
    def PATH_URLS(cls) -> list[str]:
        return cls.get_config("PATH_URLS")

    @classmethod
    def SERVICE_MAPPING(cls) -> dict[str, str]:
        return cls.get_config("SERVICE_MAPPING")

    @classmethod
    def DEFAULT_SERVICE_PACKAGE(cls) -> str:
        return cls.get_config("DEFAULT_SERVICE_PACKAGE")

    @classmethod
    def SWAGGER_DOC_URLS(cls) -> dict[str, str]:
        return cls.get_config("SWAGGER_DOC_URLS")

    @classmethod
    def INVALID_PARAMS(cls) -> set[str]:
        return cls.get_config("INVALID_PARAMS")

    @classmethod
    def HEADERS_TO_INCLUDE(cls) -> set[str]:
        return cls.get_config("HEADERS_TO_INCLUDE")

    @classmethod
    def REQUIRED_HEADERS(cls) -> dict[str, str]:
        return cls.get_config("REQUIRED_HEADERS")

    @classmethod
    def PAGINATION_PARAMS(cls) -> list[str]:
        return cls.get_config("PAGINATION_PARAMS")

    @classmethod
    def TESTCASE_DIR(cls) -> str:
        return cls.get_config("TESTCASE_DIR")

    @classmethod
    def DEFAULT_TESTCASE_DIR(cls) -> str:
        return "testcases"

    @classmethod
    def SWAGGER_FILE(cls) -> str:
        return cls.get_config("SWAGGER_FILE")

    @classmethod
    def SWAGGER_HOST(cls) -> str:
        return cls.get_config("SWAGGER_HOST")

    @classmethod
    def SWAGGER_BASE_PATH(cls) -> str:
        return cls.get_config("SWAGGER_BASE_PATH")

    @classmethod
    def SWAGGER_TITLE(cls) -> str:
        return cls.get_config("SWAGGER_TITLE")

    @classmethod
    def SWAGGER_VERSION(cls) -> str:
        return cls.get_config("SWAGGER_VERSION")

    @classmethod
    def determine_service_package(cls, url: str) -> str:
        """
        根据URL的第一个字段判断属于哪个微服务包

        Args:
            url: 原始接口URL，如 /mobile/trade/orderCommit

        Returns:
            str: 服务包名称，如 mall_mobile_application

        Example:
            URL: /mobile/trade/orderCommit → 返回 mall_mobile_application
            URL: /member/info → 返回 mall_center_member
        """
        import re

        # 处理 None 或空字符串
        if url is None or not url:
            return cls.DEFAULT_SERVICE_PACKAGE()

        # 从URL中提取第一个路径段
        match = re.match(r"^/?([^/]+)", url)
        if not match:
            return cls.DEFAULT_SERVICE_PACKAGE()

        first_segment = match.group(1).lower()
        # 从SERVICE_MAPPING中查找对应的服务包（不区分大小写）
        service_mapping = cls.SERVICE_MAPPING()
        for key, value in service_mapping.items():
            if key.lower() == first_segment:
                return value

        # 默认服务包
        return cls.DEFAULT_SERVICE_PACKAGE()


# 导出配置实例
config = APIConfig()
