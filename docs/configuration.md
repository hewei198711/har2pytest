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
| `HEADERS_TO_INCLUDE` | dict | `{}` | 需保留的请求头白名单（**空 = 只保留 content-type、content-length 和 REQUIRED_HEADERS**）；只检查键名做过滤，值无实际作用 |
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

### complex_scenario 步骤取值（TRACK_PARAM_SOURCES 等）

| 配置项 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| `TRACK_PARAM_SOURCES` | bool | `true` | complex_scenario 模式下追踪步骤参数取值来源：开启后步骤参数按前序响应引用、未命中参数提升为用例级 `test_data`；关闭时参数保持 HAR 录制值字面量 |
| `PARAM_SOURCE_MIN_LENGTH` | int | `5 / 2` | 值匹配兜底的最短长度（内置常量）：数值型 5 字符、非数值（中文/字母）2 字符；低于门槛不参与，避免同值异义字段误引用 |
| `PARAM_SOURCE_IGNORE_KEYS` | list[str] | `[]` | 不参与来源追踪的参数名（如时间戳/签名类固定值） |
| `COLLECT_RESPONSE_APIS` | list[dict] | `[]` | 响应收集接口配置，见下文 |

#### COLLECT_RESPONSE_APIS（响应收集接口）

用于上传类接口：同一接口多次调用合并为一个带循环形参的步骤函数，每次调用的
响应片段按 `append_path` 追加到 `test_data` 的 `collect_key` 列表，后续步骤的
列表参数以列表推导引用（如附件 URL 列表）。

```json
{
    "COLLECT_RESPONSE_APIS": [
        {
            "url": "/upload",
            "collect_key": "upload",
            "files_key": "files",
            "file_field": "file",
            "append_path": ["datas"]
        }
    ]
}
```

| 字段 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `url` | str | 必填 | HAR 请求 URL 子串匹配（建议写去掉 `BASE_URLS` 前缀后的相对路径，如 `/upload`） |
| `collect_key` | str | 必填 | `test_data` 中收集响应片段的列表键 |
| `files_key` | str | `"files"` | `test_data` 中文件参数值列表的键（数量与接口调用次数一致，值取自各次请求的 `file_field` 录制值） |
| `file_field` | str | `"file"` | 表单中文件字段名，渲染为步骤函数形参（执行段 `for file in test_data[files_key]` 逐文件传入） |
| `append_path` | list[str] | `["datas"]` | 相对整个响应 JSON 的取值路径，追加到收集列表的片段 |

生成的代码形态（以 `/upload` 为例）：

```python
test_data: dict = {
    # ...
    "storage_upload": [],
    "files": ["data/1.png", "data/2.png", "data/3.png"],
}

@allure.step("")
async def step_storage_upload(file):
    files = {
        "storageType": test_data["storageType"],
        "clientKey": test_data["clientKey"],
        "file": file,
    }
    async with storage_upload(files=files, headers=self.headers) as r:
        assert r.status == 200
        data = await r.json()
        test_data["storage_upload"].append(data["datas"])

# 执行所有测试步骤
for file in test_data["files"]:
    await step_storage_upload(file)
# 后续步骤中列表参数以列表推导引用收集片段：
# "attachmentUrlList": [i["fileUrlKey"] for i in test_data["storage_upload"]],
```

注意：收集接口的步骤函数不生成 `assert data['code'] == 200`（此类响应常无
`code` 字段）；该接口的响应不参与普通取值引用，仅供列表推导投影匹配（列表
参数元素与收集片段按同一字段对齐、元素数一致时命中）。

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
