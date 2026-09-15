# HAR 文件解析详解

## 概述

HAR（HTTP Archive）文件是浏览器或抓包工具导出的网络请求记录文件，格式为 JSON。`har2pytest` 通过解析 HAR 文件提取 API 请求信息，用于生成 API 文件或测试用例。

---

## 解析流程

### 调用链

```mermaid
flowchart TD
    A[HAR 文件 .har] --> B[HARParser.extract_requests_from_har<br/>har_file_path, filter_duplicate_url]
    B --> C[读取 JSON 文件]
    C --> D{_resourceType in xhr/fetch?}
    D -->|否| E[跳过非API请求]
    D -->|是| F{URL 包含 kill_url?}
    F -->|是| G[跳过]
    F -->|否| H[提取请求信息]
    H --> I[过滤 headers<br/>HEADERS_TO_INCLUDE]
    I --> J[过滤 query_params<br/>INVALID_PARAMS]
    J --> K{有 postData?}
    K -->|否| L[query_params 作为参数]
    K -->|是| M[解析 POST 数据]
    M --> N[过滤 postData<br/>INVALID_PARAMS]
    N --> O{filter_duplicate_url?}
    O -->|是| P[去重: method + clean_url]
    O -->|否| Q[保留所有]
    P --> R[返回 request_info 列表]
    Q --> R
```

### 详细步骤

#### Step 1: 读取 HAR 文件

```
输入: har_file_path
 └─ 以 UTF-8 编码读取 JSON 文件
 └─ 定位到 log.entries 数组
 └─ entries 为空 → 返回空列表
 └─ JSON 格式错误 / 文件不存在 → 返回空列表
```

#### Step 2: 过滤非 API 请求

仅保留 `_resourceType` 为 `"xhr"` 或 `"fetch"` 的条目；若 HAR 条目缺少 `_resourceType` 字段，默认按 `"xhr"` 保留（兼容无该字段的抓包）。过滤掉以下资源类型的请求：

| 资源类型 | 处理方式 |
|---------|---------|
| `xhr` | **保留** - API 请求 |
| `fetch` | **保留** - API 请求 |
| `document` | 跳过 - HTML 文档 |
| `stylesheet` | 跳过 - CSS 样式 |
| `script` | 跳过 - JS 脚本 |
| `image` | 跳过 - 图片 |
| `font` | 跳过 - 字体 |
| `media` | 跳过 - 媒体 |
| `websocket` | 跳过 - WebSocket |
| `other` | 跳过 - 其他 |

#### Step 3: 过滤无效 URL

检查 URL 是否包含 `KILL_URLS` 中的关键字。`KILL_URLS` **默认是空列表**（不过滤），下面只是配置示例：

```python
KILL_URLS = [
    ".js",
    ".css",
    ".png",
    ".jpg",
    ".gif",
    ".ico",
    ".svg",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
]
```

只要 URL 中任意位置包含以上关键字，即跳过该请求。

#### Step 4: 过滤 Headers

仅保留配置 `HEADERS_TO_INCLUDE` 中定义的 headers 和以下必要的 headers。
**当 `HEADERS_TO_INCLUDE` 为空时（默认值即空 `{}`），不做过滤，保留全部 headers**：

| Header | 说明 |
|--------|------|
| `content-type` | 必须保留，标识请求体格式 |
| `content-length` | 必须保留，标识请求体长度 |
| `authorization` | 认证信息（来自配置） |
| `channel` | 渠道标识（来自配置） |
| `...` | 其他配置中定义需保留的 headers |

#### Step 5: 过滤无效参数

使用 `INVALID_PARAMS` 配置过滤掉无效参数。`INVALID_PARAMS` **默认是空列表**，下面只是配置示例：

```python
INVALID_PARAMS = ["rnd", "timestamp", "_", "t", "callback", "jsonp"]
```

这些参数通常是前端框架或工具自动添加的，对 API 测试无实际意义。
过滤会**递归**进入嵌套的 dict/list（JSON body 内的同名字段同样被移除），
标量值（字符串/数字/布尔/None）原样保留。

#### Step 6: 解析 POST 数据

根据 `content-type` 决定解析方式：

| Content-Type | 解析方式 | 示例 |
|-------------|---------|------|
| `application/json` | `json.loads(postData.text)` | `{"pageNum": 1, "pageSize": 10}` |
| `multipart/form-data` | 遍历 `postData.params` | `{"file": "...", "name": "..."}` |
| `application/x-www-form-urlencoded` | `parse_qs(postData.text)` | `{"pageNum": "1", "pageSize": "10"}` |

> **不支持的 Content-Type**：若 `postData` 存在但 `content-type` 不属于以上三种，该请求会被跳过并输出警告日志。

#### Step 7: 提取 URL 相对路径

使用 `base_urls` 配置从完整 URL 中提取相对路径（默认空列表，需在配置文件中自定义）：

```python
BASE_URLS = [
    "https://api.example.com",
    "https://api.example.cn",
]
```

# 提取过程
# 完整 URL: https://api.example.com/taobao/mobile/order/page?pageNum=1
# 提取后  : /taobao/mobile/order/page
```

当未配置 `base_urls` 时，回退使用 `origin` header 进行提取。

#### Step 8: 去重（可选）

当 `filter_duplicate_url=True` 时，对 `method + clean_url` 进行去重，保留第一个出现的请求。

#### Step 9: 构建请求信息

每个请求最终生成 `ParsedRequestInfo` dataclass 实例（`har2pytest/models.py`），字段如下：

```python
request_info = ParsedRequestInfo(
    method="GET",              # HTTP 方法
    url="/api/example",        # 清理后的相对 URL
    full_url="https://...",    # 完整原始 URL
    headers={ ... },            # 过滤后的 headers
    content_type="...",        # 内容类型（来自 postData.mimeType）
    cookies={ ... },            # Cookie
    query_params={ ... },       # 过滤后的查询参数
    post_data={ ... },          # 解析后的 POST 数据
    response_status=200,        # 响应状态码
    response_content={ ... },   # 响应内容（JSON 解析后）
    response_time=123.45,       # 响应时间（毫秒）
    server_ip="192.168.1.1",   # 服务器 IP
    is_file_upload=False,       # 是否文件上传（api_generator 阶段填充）
    is_multipart=False,         # 是否 multipart 请求
    is_need_urlencode=False,    # 是否需 urlencode
    is_json_content=False,      # 是否 JSON 请求体
    path_params={ ... },        # 路径参数（URL 匹配后填充）
    url_pattern=None,           # 匹配到的 URL 模板
    function_name="...",        # 生成的函数名
)
```

`extract_requests_from_har` 返回 `list[ParsedRequestInfo]`，消费方通过属性访问字段（如 `request.url`、`request.query_params`），替代裸 dict 的下标访问。

---

## HAR 文件结构说明

HAR 文件的 JSON 结构如下所示：

```json
{
    "log": {
        "version": "1.2",
        "creator": { "name": "Chrome", "version": "91.0.4472.124" },
        "entries": [
            {
                "_resourceType": "xhr",          // 资源类型，用于过滤
                "request": {
                    "method": "GET",
                    "url": "https://api.example.com/taobao/mobile/order/page?pageNum=1&pageSize=10",
                    "headers": [
                        { "name": "authorization", "value": "bearer xxx" },
                        { "name": "content-type", "value": "application/json" }
                    ],
                    "queryString": [
                        { "name": "pageNum", "value": "1" },
                        { "name": "pageSize", "value": "10" }
                    ],
                    "postData": {
                        "mimeType": "application/json",
                        "text": "{\"keyword\": \"test\"}"
                    },
                    "cookies": []
                },
                "response": {
                    "status": 200,
                    "content": {
                        "text": "{\"code\": 200, \"data\": []}"
                    }
                },
                "time": 123.45,
                "serverIPAddress": "192.168.1.1"
            }
        ]
    }
}
```

---

## URL 路径参数识别

`get_url_info()` 按以下优先级依次尝试，命中即返回：

### 方式 1：通过配置中的 PATH_URLS 匹配（优先）

```python
PATH_URLS = [
    "/mobile/returnOrder/{id}",
    "/invt/order/{orderId}/detail",
    "/order/product/{productId}/sku/{skuId}",
]
```

将请求 URL 逐个与配置中的模板进行匹配，成功则提取路径参数并生成 `f-string` 格式 URL 模板。

### 方式 2：通过 Swagger 文档匹配

```
完整 URL: /mobile/returnOrder/12345

Swagger 路径: /mobile/returnOrder/{id}

匹配结果: { "id": "12345" }
URL 模板: /mobile/returnOrder/{params['id']}
```

流程：
1. 获取服务对应的 Swagger 文档数据
2. 先精确匹配 paths 中的键（避免具体路径被模板抢走）
3. 再与带 `{param}` 的路径模板逐一匹配
4. 匹配成功 → 提取路径参数 → 生成 `f-string` 格式 URL 模板

### 兜底：无模板命中

以上两种方式均未匹配时，URL 原样作为 pattern，无路径参数，函数名由 URL 直接生成。

---

## 辅助功能

### `print_api_summary()`

打印 HAR 文件中所有 API 请求的摘要信息，包含：

```
HAR文件: api_request.har
共发现 15 个API请求
--------------------------------------------------------------------------------
 1. GET     200   123.45ms /mobile/order/page
 2. POST    200   456.78ms /order/handledDetail
 3. GET     500    12.34ms /mobile/return/12345
...
--------------------------------------------------------------------------------
统计: 成功 13 个, 失败 2 个, 平均响应时间 234.56ms
```
