# har2pytest

从 HAR 抓包文件和 Swagger 文档生成 Python API 接口文件，并自动生成 pytest + allure 参数化测试用例的 CLI 工具。

## 安装

```bash
pip install har2pytest
```

验证安装：

```bash
har2pytest --help
```

## 快速开始

### 1. 从 HAR 文件生成 API 文件

```bash
# 同步模式（默认，使用 requests）
har2pytest api api_request.har

# 异步模式（使用 aiohttp + async/await）
har2pytest api api_request.har --async
```

### 2. 从 Swagger 文档生成 API 文件

```bash
# 同步模式
har2pytest swagger https://petstore.swagger.io/v2/api-docs

# 异步模式
har2pytest swagger https://petstore.swagger.io/v2/api-docs --async
```

### 3. 生成测试用例

```bash
# 查询类参数化测试（指定 URL）
har2pytest testcase api_request.har --pattern list_query --url /api/user/list

# 查询类参数化测试（带 task_id 标记）
har2pytest testcase api_request.har --pattern list_query --url /api/user/list --mark test_4291

# 复杂场景流程测试
har2pytest testcase api_request.har --pattern complex_scenario --url /api/user/login

# 批量生成（指定 API 文件目录）
har2pytest testcase --pattern batch --api-files apis/mobile_application

# 批量生成（指定 HAR 文件，自动提取接口并匹配 API 文件）
har2pytest testcase --pattern batch --api-files api_request.har

# 强制覆盖已存在的测试用例文件
har2pytest testcase api_request.har --pattern list_query --url /api/user/list --overwrite

# 异步模式（生成 async/await 测试代码，适用于所有模式）
har2pytest testcase api_request.har --pattern list_query --url /api/user/list --async
```

### 4. 查看 HAR 文件摘要

```bash
har2pytest summary api_request.har
```

## 详细文档

| 文档 | 说明 |
|------|------|
| [API 文件生成](docs/api_file_generation.md) | 从 HAR / Swagger 生成 API 文件的详细说明 |
| [HAR 文件解析](docs/har_file_parsing.md) | HAR 解析规则与参数过滤 |
| [Swagger 文档解析](docs/swagger_document_parsing.md) | Swagger 文档获取与参数提取 |
| [测试用例生成模式](docs/testcase_generation_modes.md) | list_query / complex_scenario / batch 三种模式详解 |

## 配置

在项目根目录创建 `har2pytest_config.json` 自定义配置。配置项详见 `APIConfig` 类（[config.py](har2pytest/config.py)）。

## 项目结构

```
har2pytest/
├── har2pytest/              # 核心代码
│   ├── __init__.py
│   ├── __main__.py          # CLI 入口
│   ├── client.py            # HTTP 客户端 (Client, AsyncClient)
│   ├── config.py            # 配置管理 (APIConfig)
│   ├── har_parser.py        # HAR 文件解析 (HARParser)
│   ├── har_generator.py     # HAR → API 文件生成
│   ├── api_generator.py     # API 文件生成 (APIGenerator)
│   ├── swagger_handler.py   # Swagger 文档处理 (SwaggerHandler)
│   ├── testcase_generator.py # 测试用例生成 (TestCaseGenerator)
│   ├── url_matcher.py       # URL 规范化与匹配 (URLMatcher)
│   ├── utils.py             # 工具函数
│   └── logger.py            # 日志配置
├── docs/                    # 详细文档
├── tests/                   # 单元测试
│   └── har2pytest_config_test.json  # 测试配置示例
├── pyproject.toml           # 项目配置
└── mkdocs.yml               # 文档站点配置
```