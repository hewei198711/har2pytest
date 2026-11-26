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
        { "url": "/mgmt/order/demoList", "mode": "list_query" },
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

### 数据库参数探测（DB_CONFIG）

api 生成阶段（`har2pytest api` / `har2pytest swagger`）按 `api_table_map` 的
URL→表 映射连接数据库，把接口参数名（驼峰转蛇形）匹配到表字段，取一条示例
记录的值写入 api.json 的 `db_params` 字段，供 complex_scenario 等消费端作为
参数示例值（摆脱对 HAR 录制值的依赖）。

| 配置项 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| `DB_CONFIG` | dict | `null` | 数据库探测配置；缺省不启用 |

```json
"DB_CONFIG": {
    "host": "demo.mysql.example.com",
    "port": 3306,
    "user": "tester",
    "password_env": "TEST_DB_PWD",
    "databases": ["demo_center_member", "demo_center_order"],
    "domain_schemas": {
        "member": {
            "schemas": ["demo_center_member"],
            "url": ["member", "vip", "card"],
            "cn": ["会员", "顾客", "客户"]
        },
        "order": {
            "schemas": ["demo_center_order"],
            "url": ["order", "refund", "return"],
            "cn": ["订单", "售后", "退货"]
        }
    },
    "preferred_tables": ["demo_center_member.demo_member_info"],
    "api_table_map": {
        "/demo/demoReview/demoAction": {
            "table": "demo_center_order.demo_review_record",
            "where": "demo_visit_status = 0"
        },
        "/demo/order/demoDetail": "demo_center_order.demo_order_info"
    }
}
```

- `host` / `port` / `user`：数据库连接信息（必填）。
- `password_env`：密码来源（必填），兼容两种写法：
  - 填**环境变量名**（如 `TEST_DB_PWD`）→ 密码从该环境变量读取，不落盘
    （运行前需注入环境变量，如 `TEST_DB_PWD=xxx`）；
  - 直接填**密码明文** → 环境变量中查不到该名字时，把该值本身当密码使用。
- `databases`：自动找表的库范围限定（可选，缺省查全部可见库）；它是可见库
  边界，`domain_schemas` 的域库会与它取交集，不会把查询扩到边界之外。
- `domain_schemas`：业务域→库映射（可选），按接口语义优先在配置的域库内
  找表。每个域三个键：
  - `schemas`：该域对应的库清单（必填，未填则该域定义被忽略）；
  - `url`：英文词元词表，接口 URL 词元（驼峰已拆词、小写）命中即属该域；
  - `cn`：中文词表，接口描述或参数备注包含该词即属该域。
  可命中多个域（取库并集）；未命中任何域、或域内找不到唯一胜出表时
  回退全库查找——词表只是“优先范围”而非硬过滤，因此词表误判不会导致漏探。
  参数级独立找表时以参数自身语义（备注中文 + 参数名词元）定域，如
  `storeCode` 备注“云商微店门店编码”→ 店铺库，不被接口主域带偏。
- `preferred_tables`：主表清单（可选），自动找表**同分时的消歧键**（排序
  次级），用于唯一索引并列时人工先验破局（如 `demoNo` 在主表与关联表同为
  唯一索引列）；**不参与加分**、不强制优先查表，因此不会让被配置的大表
  凭一个通用列（如 `store_code`）压过业务语义正确的主表。
- `api_table_map`：接口 URL 到表的显式映射（可选，最权威，可覆盖自动找表
  结果）。键支持精确路径、`{param}` 模板或末尾 `*` 通配；值可为
  `"库.表"` 字符串，或 `{"table": "库.表", "where": 过滤条件}` 对象
  （`where` 可选，用于限定示例行，如未回访记录）。

行为说明：

- 表来源优先级：
  1. `api_table_map` 显式映射命中 → 直接查该表（可带 `where`）；
  2. 未命中 → 按接口语义（URL 词元 + 描述中文）推断业务域，先在
     `domain_schemas` 配置的域库内自动反查 `information_schema`（列反查、
     唯一索引反查、表名反查三类查询均排除 `information_schema`/`mysql`/
     `performance_schema`/`sys` 系统库，避免系统表凭通用列混进候选），
     域内无唯一胜出者再回退全库。候选集 = 参数列反查 ∪ URL 词元表名匹配
     （主表可能根本没有参数对应的列，如活动主表无 `store_code`，仅靠列反查会把它
     结构性排除；但表名候选须至少含一个参数列才能入选，否则无法供值），
     按“非通用命中列数×10 + 表名与 URL 关键词相似度 + 唯一索引加分
     - 表名多余词段惩罚 - 备份表惩罚”打分：`id`/`status` 等通用列不计命中
     也不参与唯一索引反查（否则每张含主键的表都拿加分）；表名中未被 URL
     词元覆盖的词段每段扣 8 分（子表在主表名上追加限定词，需降权）；
     `bak`/`copy` 等备份表降权。唯一最高分胜出，同分时 `preferred_tables`
     配置的表优先，仍并列则视为歧义；
  3. 主表匹配不到的参数逐个独立找表（跨表接口如 `demoNo` 在会员主表、
     `demoCode` 在产品主表，各自查各自的表），域推断以参数自身语义优先；
     此阶段不施加表名多余词段惩罚（跨域主表表名天然与接口词元无关），
     主表识别交给唯一索引信号；
  4. 无候选或并列歧义 → 跳过探测（日志提示手动配 `api_table_map`）。
  以上均不影响 API 文件生成。
- 参数名匹配表字段：先按原样（小写）比对，再按驼峰转蛇形比对
  （`demoVisitOperator` → `demo_visit_operator`），复数参数自动去尾 s 匹配
  单数列（`ids` → `id`）；仍未命中时按“列名包含参数名”的子串兜底（如
  `messagecontent` 包含 `content`，多列并列时只取以参数名结尾的列，仍
  不唯一则跳过不猜）；未匹配到字段的参数不写入。
- 示例行取 `WHERE` 过滤后的主键倒序第一条（无主键时取首条）；值为 NULL 的
  字段不写入。
- 值策略：接口描述/URL 含“新增/添加”字样的接口，探测值生成与库中已有值
  不冲突的新值（数值列 MAX+1、字符串列加随机后缀）；含“编辑/修改”字样的
  接口唯一索引列同样生成不冲突值、主键列取已有值；其余接口一律取已有
  示例值（查询接口传新值会查空）。数组形声明的参数（如 `ids: []`）自动
  包装为单元素列表。有枚举声明的参数（api.json `param_values` 含枚举列表，
  如 `platform` 的 `[1,2,3]`）直接取首个枚举值，不查库。
- 探测失败（驱动缺失、连不上库、表或字段不存在、无示例行）一律警告并跳过，
  不阻断生成；自动找表成功时日志提示“建议在 api_table_map 中固化该映射”。
  探测结果写入 api.json 的 `db_params` 字段：

```json
"db_params": {
    "table": "demo_center_order.demo_review_record",
    "values": {
        "id": {"value": 9001, "remark": "示例值来自 demo_center_order.demo_review_record.id（demo_visit_status = 0）"}
    }
}
```

- 消费端（complex_scenario 无 HAR 时）用 `db_params.values` 覆盖同名参数的
  类型默认值，使场景用例拿到真实可用的传参；只覆盖同名键，不新增参数。
- 同一消费端还会对 id 类参数（`id`、`xxx_id`、`xxxId`）做空值兜底：库探测未能
  给该参数取到值（仍为 `None` 或空串）时补上主键 `1`。服务端普遍对主键/外键
  做非空校验，留空的用例必然被拒；而 id 常常探不到值——日志型接口的 id 指向
  被关联实体表，自动找表只会命中日志表或因并列候选放弃。兜底保持声明类型形态
  （数值声明给 `1`，字符串声明给 `"1"`），`db_params` 已给出值时不覆盖，非 id
  类的空值参数仍按原样输出；兜底后的 id 不再是空值，按常规进入用例级
  `test_data` 集中管理，便于运行前改值。
- 需要 `pymysql` 驱动（`pip install pymysql`），未安装时跳过并提示。

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
