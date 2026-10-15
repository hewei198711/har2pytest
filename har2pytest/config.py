"""配置管理模块。

负责加载和管理 har2pytest 的配置信息，包括 API 基础 URL、服务映射、Swagger 文档 URL 等。
"""

import copy
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
        # NOTE: 默认配置值包含 f-string 代码，运行时通过 eval 求值。请确保配置文件来源可信。
        "REQUIRED_HEADERS": {"authorization": "f\"bearer {os.environ.get('token', '')}\""},
        "HEADERS_TO_INCLUDE": {},
        # 分页参数配置：字典格式 {参数名: 默认值}
        # 例如 {"pageNum": 1, "pageSize": 10}
        # 键用于子串匹配判定是否为分页参数，值作为参数化排除后的默认值
        # 列表格式已废弃，加载时会警告并转换为空字典
        "PAGINATION_PARAMS": {},
        # 时间类参数关键字（包含匹配，不区分大小写），用于时间对组合传参
        "TIME_PARAMS": [],
        # 测试用例目录 - 必需配置，必须在配置文件中指定
        "TESTCASE_DIR": "testcases",
        # 服务映射配置 - 必需配置，必须在配置文件中指定
        "SERVICE_MAPPING": None,
        # 默认API文件目录 - 必需配置，必须在配置文件中指定
        "DEFAULT_API_DIR": "apis",
        "PATH_URLS": [],
        # Swagger文档URL配置 - 必需配置，必须在配置文件中指定
        "SWAGGER_DOC_URLS": {},
        # 列表查询接口识别关键字
        "LIST_QUERY_KEYWORDS": ["列表"],
        # 列表查询排除关键字：描述含这些关键字时不使用参数化列表模式（如“详情”）
        "LIST_QUERY_EXCLUDE_KEYWORDS": [],
        # 单接口测试模式配置（TESTCASE_PROFILES）：
        # 按 URL 显式指定生成模式，消除依赖中文关键字/命令行选项的脆弱判定。
        # 每条: {"url": "/mgmt/order/orderList", "mode": "auto|list_query|complex_scenario",
        #        "keywords": [...], "exclude_keywords": [...]}
        #  - mode=auto（缺省）时回落关键字启发式；keywords/exclude_keywords 可覆盖全局默认
        #  - url 支持精确路径、{param} 模板或末尾通配 *（如 "/mgmt/order/*"）
        "TESTCASE_PROFILES": [],
        # 状态值提取的额外正则模式（补充内置4种模式）
        "STATE_VALUE_PATTERNS": [],
    }

    # 初始化配置
    _config: dict | None = None
    _config_warned = False
    _service_mapping_lower: dict[str, str] = {}

    @classmethod
    def _load_config(cls):
        """加载配置。

        优先从环境变量 HAR2PYTEST_CONFIG 指定的配置文件读取，
        如果未设置则使用当前目录下的 har2pytest_config.json。

        Returns:
            dict: 返回配置字典。
        """
        config = copy.deepcopy(cls._default_config)

        # 尝试从环境变量读取配置文件路径
        config_file = os.environ.get("HAR2PYTEST_CONFIG")
        if not config_file:
            # 默认配置文件路径
            config_file = os.path.join(os.getcwd(), "har2pytest_config.json")

        # 一次性检查物理存在，后续复用（避免多次 os.path.exists）
        config_file_present = os.path.exists(config_file)
        logger.debug(f"配置文件路径: {config_file}")
        logger.debug(f"配置文件是否存在: {config_file_present}")

        # 尝试从配置文件读取
        if config_file_present:
            try:
                with open(config_file, encoding="utf-8") as f:
                    user_config = json.load(f)
                    config.update(user_config)
                    logger.debug(f"成功加载配置文件，DEFAULT_API_DIR: {config.get('DEFAULT_API_DIR')}")
            except Exception as e:
                # 配置文件读取失败（损坏/格式错误）：保留已读入的默认配置，交由必需项校验报错
                logger.warning(f"配置文件 {config_file} 读取失败: {str(e)}，将使用默认配置")
        else:
            # 配置文件不存在，使用默认配置
            logger.warning(f"未找到配置文件 {config_file}，将使用默认配置，这可能不符合您的实际要求")

        # 转换集合类型
        if isinstance(config.get("INVALID_PARAMS"), list):
            config["INVALID_PARAMS"] = set(config["INVALID_PARAMS"])

        # 校验 PAGINATION_PARAMS：仅支持字典格式
        pagination_params = config.get("PAGINATION_PARAMS")
        if isinstance(pagination_params, list):
            raise ValueError(
                "配置文件格式错误：PAGINATION_PARAMS 仅支持字典格式，请使用字典格式。\n"
                "旧格式（已废弃）：\n"
                '    "PAGINATION_PARAMS": ["pageNum", "pageSize"]\n'
                "新格式：\n"
                '    "PAGINATION_PARAMS": {\n'
                '        "pageNum": 1,\n'
                '        "pageSize": 10\n'
                "    }\n"
                "字典键用于判定是否为分页参数（子串匹配），值作为参数化排除后的默认值。"
            )

        # 检查 HEADERS_TO_INCLUDE 是否为字典，如果不是则报错
        if not isinstance(config.get("HEADERS_TO_INCLUDE"), dict):
            raise ValueError(
                "配置文件格式错误：HEADERS_TO_INCLUDE 仅支持字典格式，请使用字典格式。\n"
                "示例：\n"
                '    "HEADERS_TO_INCLUDE": {\n'
                '        "authorization": "bearer {os.environ.get(\'token\', \'\')}",\n'
                '        "channel": "pc",\n'
                '        "client": "op"\n'
                "    }"
            )

        # 校验必需配置项：仅当"配置文件存在但内容缺失/读取失败"时强制报错；
        # 完全没有配置文件时放行默认值并提示用户创建（见 _warn_missing_config）
        if not config_file_present:
            if config.get("SERVICE_MAPPING") is None:
                config["SERVICE_MAPPING"] = {}
        else:
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

        # 当配置文件物理不存在时，提示用户创建配置文件
        if not config_file_present:
            cls._warn_missing_config()

        # 预计算 SERVICE_MAPPING 的小写键映射，供 determine_service_package O(1) 查找
        service_mapping = config.get("SERVICE_MAPPING") or {}
        cls._service_mapping_lower = {k.lower(): v for k, v in service_mapping.items()}

        return config

    @classmethod
    def _warn_missing_config(cls):
        """提示用户创建配置文件。

        当配置文件不存在时，打印警告信息和配置示例。
        只会警告一次。
        """
        if cls._config_warned:
            return

        cls._config_warned = True
        logger.warning(
            "=" * 60 + "\n"
            "配置文件 har2pytest_config.json 不存在，使用默认配置\n"
            "=" * 60 + "\n"
            "如需自定义配置，请创建 har2pytest_config.json 文件\n"
            "配置示例:\n"
            """{
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
}""" + "\n" + "=" * 60
        )

    @classmethod
    def get_config(cls, key: str) -> Any:
        """获取配置值。

        Args:
            key: 配置项的键名。

        Returns:
            Any: 配置项的值，如果不存在则返回 None。
        """
        if cls._config is None:
            cls._config = cls._load_config()

        value = cls._config.get(key)
        return value

    # ------------------------------------------------------------------
    # 配置访问器：get_config 是唯一加载入口，下面的 classmethod 只是带类型的
    # 便捷别名（供 IDE 补全/类型检查）。刻意保留而非用 setattr 动态生成，
    # 以保证调用点的属性解析与类型推断不退化。
    # ------------------------------------------------------------------

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
    def PAGINATION_PARAMS(cls) -> dict:
        """返回分页参数字典（参数名 -> 默认值）。

        仅支持字典格式配置。若内部存储为非字典值，返回空字典。
        """
        value = cls.get_config("PAGINATION_PARAMS")
        if not isinstance(value, dict):
            return {}
        return value

    @classmethod
    def is_pagination_param(cls, param_name: str) -> bool:
        """判断参数名是否包含任一分页参数关键字（不区分大小写）。

        以 ``PAGINATION_PARAMS`` 字典的键作为关键字做子串匹配。
        空配置时返回 False（不再有内置默认回退）。
        """
        name_lower = param_name.lower()
        return any(key.lower() in name_lower for key in cls.PAGINATION_PARAMS().keys())

    @classmethod
    def get_pagination_default_value(cls, param_name: str) -> Any | None:
        """获取分页参数的默认值。

        从 ``PAGINATION_PARAMS`` 配置中按参数名查找默认值（不区分大小写）。
        配置示例：``{"pageNum": 1, "pageSize": 10}``。

        Args:
            param_name: 参数名称

        Returns:
            分页参数的默认值，或 None（表示非分页参数或配置中未指定）
        """
        if not param_name:
            return None
        name_lower = param_name.lower()
        for key, value in cls.PAGINATION_PARAMS().items():
            if key.lower() == name_lower:
                return value
        return None

    @classmethod
    def TIME_PARAMS(cls) -> list:
        return cls.get_config("TIME_PARAMS")

    @classmethod
    def is_time_param(cls, param_name: str) -> bool:
        """判断参数名是否包含任一时间参数关键字（不区分大小写）。"""
        name_lower = param_name.lower()
        return any(p.lower() in name_lower for p in cls.TIME_PARAMS())

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
    def LIST_QUERY_KEYWORDS(cls) -> list:
        return cls.get_config("LIST_QUERY_KEYWORDS")

    @classmethod
    def LIST_QUERY_EXCLUDE_KEYWORDS(cls) -> list:
        return cls.get_config("LIST_QUERY_EXCLUDE_KEYWORDS")

    @classmethod
    def STATE_VALUE_PATTERNS(cls) -> list:
        return cls.get_config("STATE_VALUE_PATTERNS")

    @classmethod
    def TESTCASE_PROFILES(cls) -> list[dict]:
        return cls.get_config("TESTCASE_PROFILES")

    @classmethod
    def determine_service_package(cls, url: str | None) -> str:
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
        if not url:
            return cls.DEFAULT_API_DIR()

        # 从URL中提取第一个路径段
        match = re.match(r"^/?([^/]+)", url)
        if not match:
            return cls.DEFAULT_API_DIR()

        first_segment = match.group(1).lower()
        # 先求默认值：触发配置懒加载（_load_config 内填充小写键映射），
        # 再从预计算的小写键映射中 O(1) 查找。若先读映射再求默认值，
        # 配置未加载的首次调用会拿到空映射而恒回退默认目录
        default = cls.DEFAULT_API_DIR()
        return cls._service_mapping_lower.get(first_segment, default)
