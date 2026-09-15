# 配置参考

`har2pytest` 通过 `har2pytest_config.json` 配置运行参数。配置文件的查找顺序：

1. 环境变量 `HAR2PYTEST_CONFIG` 指定的路径；
2. 否则使用当前工作目录下的 `har2pytest_config.json`。

未提供配置文件或文件缺失时，使用内置默认值（部分必需项会报错提示补齐）。
完整示例见仓库根目录 `har2pytest_config.json.example`。

## 配置项

### 基础（必需）

| 配置项 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| `BASE_URLS` | list[str] | `[]`（必须配置） | 用于从完整 URL 提取相对路径的前缀列表 |
| `SERVICE_MAPPING` | dict[str,str] | `None`（必须配置） | URL 首段 → 服务包目录 的映射 |
| `DEFAULT_API_DIR` | str | `"apis"`（必须配置） | API 文件默认输出目录 |
| `TESTCASE_DIR` | str | `"testcases"`（必须配置） | 测试用例默认输出目录 |
| `SWAGGER_DOC_URLS` | dict[str,str] | `{}`（必须配置） | 服务包名 → Swagger 文档 URL 的映射 |

### URL / 参数过滤

| 配置项 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| `KILL_URLS` | list[str] | `[]` | URL 含这些关键字时跳过（空 = 不过滤） |
| `INVALID_PARAMS` | list[str] | `[]` | 需要过滤的参数名，**递归**过滤嵌套 dict/list（空 = 不过滤） |
| `PATH_URLS` | list[str] | `[]` | URL 路径模板（如 `/order/{id}/detail`），用于识别路径参数 |

### Headers

| 配置项 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| `HEADERS_TO_INCLUDE` | dict | `{}` | 需保留的请求头白名单（**空 = 不过滤，保留全部**）；只检查键名做过滤，值无实际作用 |
| `REQUIRED_HEADERS` | dict | 见默认 | 每个接口都会补上的默认请求头（值可为 f-string 模板） |

### 列表查询判定

| 配置项 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| `PAGINATION_PARAMS` | list[str] | `[]` | 分页参数名，参数化迭代时跳过；在 list_query 模式下作为参数化变量使用 |
| `LIST_QUERY_KEYWORDS` | list[str] | `["列表"]` | 描述含这些关键字时判定为列表查询接口 |
| `LIST_QUERY_EXCLUDE_KEYWORDS` | list[str] | `[]` | 描述含这些关键字时排除列表判定（如“详情”） |
| `STATE_VALUE_PATTERNS` | list | `[]` | 从参数备注中提取枚举值的额外正则模式 |

### 测试模式配置（TESTCASE_PROFILES）

按 URL 显式指定单个接口的生成模式，优先于关键字启发式：

```json
{
    "TESTCASE_PROFILES": [
        { "url": "/mgmt/order/orderList", "mode": "list_query" },
        { "url": "/mgmt/order/{orderNo}", "mode": "complex_scenario" },
        { "url": "/mall/order/*", "mode": "auto", "keywords": ["列表"], "exclude_keywords": ["详情"] }
    ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `url` | str | 精确路径 / `{param}` 模板 / 末尾 `*` 通配 |
| `mode` | str | `list_query` / `complex_scenario` / `auto`（`auto` 或缺省回落关键字启发式） |
| `keywords` | list[str] | 可选，`auto` 模式下覆盖全局 `LIST_QUERY_KEYWORDS` |
| `exclude_keywords` | list[str] | 可选，`auto` 模式下覆盖全局 `LIST_QUERY_EXCLUDE_KEYWORDS` |

## HTTP 客户端行为

- 同步用 `requests`（`Client`，默认 `default_verify=False`、`raise_for_status=False`，因此默认**不会**对 4xx/5xx 抛 `requests.HTTPError`，便于测试断言 `r.status_code`）。
- 异步用 `aiohttp`（`AsyncClient`，`default_verify=False` → `TCPConnector(ssl=False)`，TLS 校验默认关闭）。
- 测试文件通过 `client.set_client(async_client)` 切换；`client.is_async` 判断当前模式。
- 两种模式响应字段不同：同步 `r.status_code` / `r.json()`，异步 `r.status` / `await r.json()`。

## 配置示例

最小可用配置（补齐必需项即可）：

```json
{
    "BASE_URLS": ["https://api.example.com"],
    "SERVICE_MAPPING": {"mgmt": "management_application"},
    "DEFAULT_API_DIR": "apis",
    "TESTCASE_DIR": "testcases",
    "SWAGGER_DOC_URLS": {"management_application": "https://api.example.com/v2/api-docs"}
}
```
