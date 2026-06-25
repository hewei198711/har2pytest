"""配置管理模块。

负责加载和管理 har2pytest 的配置信息，包括 API 基础 URL、服务映射、Swagger 文档 URL 等。
"""

import json
import os
import re
from typing import Any

from .logger import logger


class APIConfig:
    """API 配置管理类。

    负责加载和管理配置信息，支持从配置文件和环境变量读取配置。
    配置文件默认为当前目录下的 har2pytest_config.json。
    """

    _default_config = {
        # 基础配置 - 必需配置，必须在配置文件中指定
        "BASE_URLS": [],
        "KILL_URLS": [],
        # 请求参数过滤配置
        "INVALID_PARAMS": [],
        # 请求头配置
        "REQUIRED_HEADERS": {"authorization": "f\"bearer {os.environ['access_token']}\""},
        "HEADERS_TO_INCLUDE": {},
        # 列表查询用例，这些参数不进行参数化处理
        "PAGINATION_PARAMS": [],
        # 测试用例目录 - 必需配置，必须在配置文件中指定
        "TESTCASE_DIR": "testcases",
        # 服务映射配置 - 必需配置，必须在配置文件中指定
        "SERVICE_MAPPING": None,
        # 默认API文件目录 - 必需配置，必须在配置文件中指定
        "DEFAULT_API_DIR": "apis",
        "PATH_URLS": [],
        # Swagger文档URL配置 - 必需配置，必须在配置文件中指定
        "SWAGGER_DOC_URLS": {},
    }

    # 初始化配置
    _config = None
    _config_warned = False
    _config_file_exists = False

    @classmethod
    def _load_config(cls):
        """加载配置。

        优先从环境变量 HAR2PYTEST_CONFIG 指定的配置文件读取，
        如果未设置则使用当前目录下的 har2pytest_config.json。

        Returns:
            tuple[dict, bool]: 返回配置字典和配置文件是否存在的标志。
        """
        config = cls._default_config.copy()
        config_file_exists = False

        # 尝试从环境变量读取配置文件路径
        config_file = os.environ.get("HAR2PYTEST_CONFIG")
        if not config_file:
            # 默认配置文件路径
            config_file = os.path.join(os.getcwd(), "har2pytest_config.json")

        logger.debug(f"配置文件路径: {config_file}")
        logger.debug(f"配置文件是否存在: {os.path.exists(config_file)}")

        # 尝试从配置文件读取
        if os.path.exists(config_file):
            config_file_exists = True
            try:
                with open(config_file, encoding="utf-8") as f:
                    user_config = json.load(f)
                    config.update(user_config)
                    logger.debug(f"成功加载配置文件，DEFAULT_API_DIR: {config.get('DEFAULT_API_DIR')}")
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

        # 检查 HEADERS_TO_INCLUDE 是否为字典，如果不是则报错
        if not isinstance(config.get("HEADERS_TO_INCLUDE"), dict):
            raise ValueError(
                "配置文件格式错误：HEADERS_TO_INCLUDE 仅支持字典格式，请使用字典格式。\n"
                "示例：\n"
                '    "HEADERS_TO_INCLUDE": {\n'
                '        "authorization": "bearer {os.environ[\'access_token\']}",\n'
                '        "channel": "pc",\n'
                '        "client": "op"\n'
                "    }"
            )

        # 校验必需配置项
        required_configs = [
            ("BASE_URLS", "基础URL列表"),
            ("TESTCASE_DIR", "测试用例目录"),
            ("SERVICE_MAPPING", "服务映射配置"),
            ("DEFAULT_API_DIR", "默认API文件目录"),
            ("SWAGGER_DOC_URLS", "Swagger文档URL配置"),
        ]

        missing_configs = []
        for key, description in required_configs:
            if config.get(key) is None:
                missing_configs.append(f"- {key} ({description})")

        if missing_configs:
            raise ValueError(
                "配置文件缺少必需配置项，请在配置文件中添加以下配置：\n"
                + "\n".join(missing_configs)
                + "\n\n请参考配置文件示例：har2pytest_config.json.example"
            )

        # 当配置文件不存在时，提示用户创建配置文件
        if not config_file_exists:
            cls._warn_missing_config()

        return config, config_file_exists

    @classmethod
    def _warn_missing_config(cls):
        """提示用户创建配置文件。

        当配置文件不存在时，打印警告信息和配置示例。
        只会警告一次。
        """
        if cls._config_warned:
            return

        cls._config_warned = True
        logger.warning("=" * 60)
        logger.warning("配置文件 har2pytest_config.json 不存在，使用默认配置")
        logger.warning("=" * 60)
        logger.warning("如需自定义配置，请创建 har2pytest_config.json 文件")
        logger.warning("配置示例:")
        logger.warning("""{
    "BASE_URLS": ["https://api.example.com"],
    "SERVICE_MAPPING": {
        "mobile": "mobile_application",
        "user": "center_application"
    },
    "DEFAULT_API_DIR": "apis",
    "PATH_URLS": ["/user/{id}/info"],
    "SWAGGER_DOC_URLS": {
        "mobile_application": "https://api.example.com/swagger/mobile-application",
        "center_application": "https://api.example.com/swagger/center-application"
    },
    "INVALID_PARAMS": ["sign", "token"]
}""")
        logger.warning("=" * 60)

    @classmethod
    def get_config(cls, key: str) -> Any:
        """获取配置值。

        Args:
            key: 配置项的键名。

        Returns:
            Any: 配置项的值，如果不存在则返回 None。
        """
        if cls._config is None:
            cls._config, cls._config_file_exists = cls._load_config()

        value = cls._config.get(key)
        return value

    @classmethod
    def BASE_URLS(cls) -> list:
        return cls.get_config("BASE_URLS")

    @classmethod
    def KILL_URLS(cls) -> list:
        return cls.get_config("KILL_URLS")

    @classmethod
    def INVALID_PARAMS(cls) -> set:
        return cls.get_config("INVALID_PARAMS")

    @classmethod
    def REQUIRED_HEADERS(cls) -> dict:
        return cls.get_config("REQUIRED_HEADERS")

    @classmethod
    def HEADERS_TO_INCLUDE(cls) -> dict:
        return cls.get_config("HEADERS_TO_INCLUDE")

    @classmethod
    def PAGINATION_PARAMS(cls) -> list:
        return cls.get_config("PAGINATION_PARAMS")

    @classmethod
    def TESTCASE_DIR(cls) -> str:
        return cls.get_config("TESTCASE_DIR")

    @classmethod
    def SERVICE_MAPPING(cls) -> dict[str, str]:
        return cls.get_config("SERVICE_MAPPING")

    @classmethod
    def DEFAULT_API_DIR(cls) -> str:
        return cls.get_config("DEFAULT_API_DIR")

    @classmethod
    def SWAGGER_DOC_URLS(cls) -> dict[str, str]:
        return cls.get_config("SWAGGER_DOC_URLS")

    @classmethod
    def PATH_URLS(cls) -> list:
        return cls.get_config("PATH_URLS")

    @classmethod
    def determine_service_package(cls, url: str) -> str:
        """根据 URL 判断所属的微服务包。

        通过 URL 的第一个路径段匹配 SERVICE_MAPPING 配置，
        确定该接口属于哪个微服务。

        Args:
            url: 原始接口 URL，如 /mobile/trade/orderCommit。

        Returns:
            str: 服务包名称，如 mall_mobile_application。

        Example:
            >>> APIConfig.determine_service_package("/mobile/trade/orderCommit")
            'mall_mobile_application'
        """

        # 处理 None 或空字符串
        if url is None or not url:
            return cls.DEFAULT_API_DIR()

        # 从URL中提取第一个路径段
        match = re.match(r"^/?([^/]+)", url)
        if not match:
            return cls.DEFAULT_API_DIR()

        first_segment = match.group(1).lower()
        # 从SERVICE_MAPPING中查找对应的服务包（不区分大小写）
        service_mapping = cls.SERVICE_MAPPING()
        for key, value in service_mapping.items():
            if key.lower() == first_segment:
                return value

        # 默认服务包
        return cls.DEFAULT_API_DIR()



