# har2pytest

从 HAR 抓包文件和 Swagger 文档生成 Python API 接口文件，并自动生成 pytest + allure 参数化测试用例的 CLI 工具。

主要特性：

- **API 元数据**：生成 API 文件时同步写 `<module>.api.json`，下游结构化读取，不再反向解析生成物
- **同步/异步自动适配**：`client` 代理默认走同步 requests，通过 `client.set_client(async_client)` 切换为 aiohttp 异步
- **模式配置化**：支持 `TESTCASE_PROFILES` 按 URL 显式指定参数化/场景模式
- **Jinja2 代码生成**：测试用例与 API 文件由模板渲染，写盘前做语法校验

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
# 生成 API 文件（同步/异步统一，运行时自动适配）
har2pytest api api_request.har
```

### 2. 从 Swagger 文档生成 API 文件

```bash
har2pytest swagger https://petstore.swagger.io/v2/api-docs
```

### 3. 生成测试用例

**命令格式：**

```bash
har2pytest testcase [har_file] --pattern <模式> [options]
```

**参数说明：**

| 参数 | 缩写 | 默认值 | 说明 |
|------|------|--------|------|
| `har_file` | - | `api_request.har` | HAR 文件路径（位置参数，可省略） |
| `--pattern` | - | `list_query` | 生成模式：`list_query` / `complex_scenario` / `batch` |
| `--url` | `-u` | - | 目标接口 URL；`list_query`/`complex_scenario` 模式**必填**，`batch` 模式忽略 |
| `--mark` | `-m` | - | pytest 标记（如 `test_4291`），生成 `@pytest.mark.test_4291` |
| `--output` | `-o` | `testcases` | 测试用例输出目录 |
| `--api-dir` | - | `apis` | API 文件目录（用于匹配 API 文件） |
| `--api-files` | - | `api_request.har` | batch 模式专用：API 文件目录或 HAR 文件，多个用逗号分隔 |
| `--overwrite` | - | `False` | 强制覆盖已存在的测试用例文件 |
| `--async` | - | `False` | 生成异步模式代码（async/await + async_client） |

**示例：**

```bash
# 查询类参数化测试（指定 URL）
har2pytest testcase api_request.har --pattern list_query --url /api/user/list

# 查询类参数化测试（全参数）,生成异步测试用例
har2pytest testcase api_request.har \
  --pattern list_query \
  --url /api/user/list \
  --mark test_4291 \
  --output testcases/async \
  --api-dir apis \
  --overwrite \
  --async

# 复杂场景流程测试（多步骤业务流），生成同步测试用例
har2pytest testcase api_request.har \
  --pattern complex_scenario \
  --url /api/order/create \
  --mark test_5012 \
  --output testcases/sync \
  --api-dir apis \
  --overwrite

# 批量生成（指定 API 文件目录，无 HAR 文件）
har2pytest testcase \
  --pattern batch \
  --api-files apis/mall_store_application \
  --output testcases/sync \
  --api-dir apis \
  --overwrite

# 批量生成（指定 HAR 文件，自动提取接口并匹配 API 文件）
har2pytest testcase \
  --pattern batch \
  --api-files api_request.har \
  --output testcases/sync \
  --api-dir apis

# 批量生成（多个 API 文件目录，用逗号分隔）
har2pytest testcase \
  --pattern batch \
  --api-files apis/mall_store_application,apis/mall_center_member \
  --output testcases/sync \
  --overwrite

# 异步模式测试用例（生成 async/await 代码，自动切换为 async_client）
har2pytest testcase api_request.har \
  --pattern list_query \
  --url /api/user/list \
  --output testcases/async \
  --async \
  --overwrite
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
| [配置参考](docs/configuration.md) | 全部配置项集中索引 |

## 配置

在项目根目录创建 `har2pytest_config.json` 自定义配置，完整配置项见 [配置参考](docs/configuration.md)。

### TESTCASE_PROFILES（推荐）

单个接口“列表参数化 vs 场景流程”的模式判定支持按 URL 显式配置，
避免依赖中文描述关键字（默认仍会回落 `LIST_QUERY_KEYWORDS` 启发式）。
配置格式、可用模式与优先级说明见 [模式配置化（TESTCASE_PROFILES）](docs/configuration.md#测试模式配置testcase_profiles)。

```json
{
    "TESTCASE_PROFILES": [
        { "url": "/mgmt/order/orderList", "mode": "list_query" },
        { "url": "/mgmt/order/{orderNo}", "mode": "complex_scenario" },
        { "url": "/mall/order/*", "mode": "auto", "keywords": ["列表"], "exclude_keywords": ["详情"] }
    ]
}
```

## 项目结构

```
har2pytest/
├── har2pytest/              # 核心代码
│   ├── __init__.py
│   ├── __main__.py          # CLI 入口
│   ├── api_generator.py     # API 文件生成 (APIGenerator)
│   ├── api_metadata.py      # API 元数据 .api.json 读写（结构化事实源）
│   ├── codegen.py           # Jinja2 渲染 + ast.parse 写盘前语法校验
│   ├── templates/           # *.j2 代码生成模板
│   ├── client.py            # HTTP 客户端 (Client, AsyncClient)
│   ├── config.py            # 配置管理 (APIConfig)
│   ├── har_parser.py        # HAR 文件解析 (HARParser)
│   ├── har_generator.py     # HAR → API 文件生成 (generate_api_files_from_har)
│   ├── models.py            # 核心数据模型 (ParsedRequestInfo/SwaggerInfo/APIFileInfo)
│   ├── pytest_utils.py      # pytest 工具 (retry_step 重试装饰器)
│   ├── swagger_handler.py   # Swagger 文档处理 (SwaggerHandler)
│   ├── testcase_generator.py # 测试用例生成 (TestCaseGenerator)
│   ├── url_matcher.py       # URL 规范化与匹配 (URLMatcher)
│   ├── utils.py             # 工具函数（parse_api_file / format_headers / deduplicate_values 等）
│   └── logger.py            # 日志配置
├── docs/                    # 详细文档
├── tests/                   # 单元测试
│   └── har2pytest_config_test.json  # 测试配置示例
├── pyproject.toml           # 项目配置
└── mkdocs.yml               # 文档站点配置
```