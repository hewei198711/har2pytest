# har2pytest testcase 命令执行流程详解

## 命令格式

```bash
har2pytest testcase 抽奖活动.har --pattern complex_scenario --url /mgmt/prmt/luckyActivity/luckyActivityList
```

### 命令参数说明

| 参数 | 说明 |
|------|------|
| `testcase` | 子命令，表示生成测试用例 |
| `抽奖活动.har` | HAR 文件路径 |
| `--pattern complex_scenario` | 复杂场景模式，针对指定 URL 生成场景化流程测试用例 |
| `--url /mgmt/prmt/luckyActivity/luckyActivityList` | 目标接口 URL（必填）|
| `--mark/-m` | 测试标记（可选）|
| `--output/-o` | 输出目录（默认 `testcases`）|
| `--api-dir` | API 文件目录（默认 `apis`）|

---

## 一、方法调用顺序

```
命令行输入
    ↓
argparse 参数解析
    ↓
handle_testcase (入口)
    ↓
TestCaseGenerator.__init__
    ↓
TestCaseGenerator.generate_scenario_testcase
        ├─> os.path.exists (文件存在性检查)
        ├─> TestCaseGenerator.match_api_files_for_har
        │     ├─> HARParser.extract_requests_from_har
        │     │     └─> URLMatcher.normalize_url
        │     ├─> TestCaseGenerator._get_all_api_files
        │     └─> URLMatcher.find_matching_api_file
        │
        ├─> URLMatcher.find_matching_api_file (查找目标API文件)
        ├─> get_output_dir
        ├─> TestCaseGenerator._get_api_file_info
        │     └─> parse_api_file (正则解析API文件)
        │
        ├─> TestCaseGenerator.generate_scenario_test_content
        │     ├─> HARParser.extract_requests_from_har (再次解析)
        │     ├─> _get_api_file_info (批量预加载)
        │     ├─> _extract_service_package
        │     ├─> merge_request_params
        │     ├─> format_params_for_python
        │     └─> format_python_file (格式化)
        │
        └─> write_test_file
              └─> format_python_file
```

---

## 二、处理逻辑详细分析

### 2.1 命令行入口 (`handle_testcase`)

**文件位置**: `har2pytest/__main__.py:230-297`

**核心代码**:
```python
def handle_testcase(args):
    """处理 testcase 命令"""
    har_file = args.har_file          # "抽奖活动.har"
    pattern = args.pattern            # "complex_scenario"
    task_id = args.mark               # None
    target_url = args.url             # "/mgmt/prmt/luckyActivity/luckyActivityList"
    output_dir = args.output          # "testcases"
    api_dir = args.api_dir            # "apis"
    
    # 如果 task_id 以 test_ 开头，去掉前缀
    if task_id and task_id.startswith("test_"):
        task_id = task_id[5:]
    
    if pattern == "complex_scenario":
        # 验证必填参数
        if not target_url:
            logger.error("错误: complex_scenario 模式必须指定 --url 参数")
            return
        
        generator = TestCaseGenerator(api_dir=api_dir, output_dir=output_dir)
        test_file = generator.generate_scenario_testcase(har_file, target_url, task_id)
```

**处理流程**:
1. 解析命令行参数
2. 验证 `complex_scenario` 模式下 `target_url` 必填
3. 创建 `TestCaseGenerator` 实例
4. 调用 `generate_scenario_testcase()` 生成测试用例

---

### 2.2 测试用例生成器初始化 (`TestCaseGenerator.__init__`)

**文件位置**: `har2pytest/testcase_generator.py:35-72`

**初始化组件**:

| 组件 | 类型 | 说明 |
|------|------|------|
| `self.api_dir` | str | API 文件目录 |
| `self.output_dir` | str | 测试用例输出目录 |
| `self.filter_duplicate_url` | bool | 是否过滤重复 URL |
| `self.har_parser` | HARParser | HAR 文件解析器 |
| `self.swagger_handler` | SwaggerHandler | Swagger 文档处理器 |
| `self.url_matcher` | URLMatcher | URL 匹配器 |
| `self._api_file_cache` | dict | API 文件信息缓存 |

---

### 2.3 复杂场景测试用例生成 (`generate_scenario_testcase`)

**文件位置**: `har2pytest/testcase_generator.py:370-413`

**处理流程**:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. 文件存在性检查                                                │
│    if not os.path.exists(har_file_path): return None           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. 查找 HAR 文件对应的所有 API 文件                              │
│    api_files = match_api_files_for_har(har_file_path)           │
│                                                                 │
│    内部流程:                                                     │
│    - 解析 HAR 文件，提取所有 XHR 请求                           │
│    - 获取所有 API 文件列表                                      │
│    - 使用 URLMatcher 匹配每个请求与 API 文件                    │
│    - 返回匹配的 API 文件列表                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. 查找目标 URL 对应的 API 文件                                 │
│    target_api_file = URLMatcher.find_matching_api_file(         │
│        target_url, api_files)                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. 获取 API 文件信息并生成输出路径                                │
│    api_info = _get_api_file_info(target_api_file)              │
│    test_filepath = os.path.join(output_dir, "test_xxx.py")     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. 生成测试用例内容                                              │
│    test_content = generate_scenario_test_content(                   │
│        har_file_path, api_files, task_id,                       │
│        target_api_file)                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. 写入文件并格式化                                              │
│    write_test_file(test_filepath, test_content)                 │
│    format_python_file(test_filepath)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.4 HAR 文件解析 (`HARParser.extract_requests_from_har`)

**文件位置**: `har2pytest/har_parser.py:31-178`

**核心处理流程**:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. 读取并解析 HAR 文件                                           │
│    har_data = json.load(open(har_file_path, encoding="utf-8"))   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. 遍历所有请求条目 (entries)                                    │
│    for entry in har_data["log"]["entries"]:                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. 过滤非 XHR 资源                                               │
│    if entry.get("_resourceType") != "xhr": continue             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. 提取请求信息                                                  │
│    ├─ 请求头 (headers)                                          │
│    ├─ 查询参数 (query_params)                                   │
│    ├─ POST 数据 (post_data)                                     │
│    └─ URL 标准化                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. 组装请求信息字典                                              │
│    request_info = {                                             │
│        "method": "POST",                                         │
│        "url": "/mgmt/prmt/luckyActivity/luckyActivityList",     │
│        "headers": {...},                                        │
│        "query_params": {...},                                    │
│        "post_data": {...},                                      │
│        ...                                                      │
│    }                                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. 过滤重复 URL (可选)                                          │
│    if filter_duplicate_url:                                     │
│        按 method:url 去重                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.5 API 文件匹配 (`match_api_files_for_har`)

**文件位置**: `har2pytest/testcase_generator.py:145-172`

**匹配策略**:

```
┌─────────────────────────────────────────────────────────────────┐
│ URL 匹配优先级:                                                  │
│                                                                 │
│ 1. 直接匹配                                                      │
│    if file_url == request_url: 匹配成功                         │
│                                                                 │
│ 2. 双向模式匹配                                                  │
│    - URLMatcher.match_url_pattern(request_url, file_url)       │
│    - URLMatcher.match_url_pattern(file_url, request_url)        │
│                                                                 │
│ 3. URL 标准化匹配                                                │
│    - URLMatcher.normalize_url(file_url) ==                      │
│      URLMatcher.normalize_url(request_url)                      │
└─────────────────────────────────────────────────────────────────┘
```

**URL 标准化处理**:
- 移除协议前缀 (`https://`)
- 移除域名部分
- 处理路径参数模板 (`/user/{id}` -> `/user/*`)

---

### 2.6 API 文件解析 (`parse_api_file`)

**文件位置**: `har2pytest/utils.py:124-250`

**解析内容**:

| 提取项 | 正则模式 | 说明 |
|--------|----------|------|
| `function_name` | 匹配函数定义 | API 函数名称 |
| `description` | 匹配 docstring | 接口描述 |
| `url` | 匹配 url = "..." | 接口路径 |
| `headers` | 匹配 headers = {...} | 请求头字典 |
| `params` | 匹配 params = {...} | GET 参数 |
| `data` | 匹配 data = {...} | POST 数据 |
| `files` | 匹配 files = {...} | 文件上传 |

**headers 解析优化**:
```python
# 处理嵌套大括号（如 f-string 中的 {os.environ['access_token']}）
headers_start = content.find("headers = {")
if headers_start != -1:
    headers_start += len("headers = {")
    brace_count = 1
    headers_end = headers_start
    while brace_count > 0 and headers_end < len(content):
        if content[headers_end] == "{":
            brace_count += 1
        elif content[headers_end] == "}":
            brace_count -= 1
        headers_end += 1
```

---

### 2.7 测试用例内容生成 (`generate_scenario_test_content`)

**文件位置**: `har2pytest/testcase_generator.py:415-645`

**生成流程**:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. 解析 HAR 文件 (再次解析，获取完整请求列表)                       │
│    requests = har_parser.extract_requests_from_har(...)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. 生成导入部分                                                  │
│    import os                                                    │
│    import pytest                                                │
│    import allure                                               │
│    from apis.{service_package} import {function_name}            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. 生成 test_headers fixture (从 API 文件获取)                    │
│    @pytest.fixture(scope="module")                              │
│    def test_headers():                                          │
│        return {                                                 │
│            "channel": "pc",                                     │
│            "client": "op",                                     │
│            "authorization": f"bearer {os.environ['access_token']}"│
│        }                                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. 生成 Allure 装饰器                                            │
│    @pytest.mark.test_{task_id}                                  │
│    @allure.severity(Severity.CRITICAL)                         │
│    @allure.feature('{service_package}')                         │
│    @allure.story('{api_url}')                                   │
│    @allure.title('{api_description}')                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. 生成测试函数定义                                              │
│    def test_{function_name}(test_headers):                       │
│        test_data = {}                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. 遍历所有请求，生成测试步骤                                    │
│    for request_info in requests:                                │
│        ├─> 查找对应的 API 函数                                   │
│        ├─> @allure.step("{api_description}")                    │
│        ├─> def step_{function_name}():                          │
│        ├─> 合并参数 + 格式化                                     │
│        └─> 生成断言代码                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. 生成步骤执行代码                                              │
│    for step_func in step_functions:                             │
│        content.append(f"    {step_func}()")                     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.8 参数合并与格式化

**参数合并** (`har2pytest/utils.py:285-302`):
```python
def merge_request_params(request_info):
    """合并请求中的 query_params 和 post_data"""
    params = {}
    if request_info.get("query_params"):
        params.update(request_info["query_params"])
    if request_info.get("post_data"):
        if isinstance(request_info["post_data"], dict):
            params.update(request_info["post_data"])
    return params
```

**参数格式化** (`har2pytest/utils.py:46-51`):
```python
def format_params_for_python(params, indent=12):
    """将参数字典格式化为 Python 代码字符串"""
    # 使用 json.dumps 格式化，保持缩进一致
```

---

### 2.9 文件写入与格式化 (`write_test_file`)

**文件位置**: `har2pytest/utils.py:88-107`

**处理流程**:
1. 写入文件（UTF-8 编码）
2. 使用 `ruff check --fix` 修复代码问题
3. 使用 `ruff format` 格式化代码

---

## 三、完整处理流程图

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           用户执行命令                                        │
│  har2pytest testcase 抽奖活动.har --pattern complex_scenario                 │
│                    --url /mgmt/prmt/luckyActivity/luckyActivityList         │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  __main__.py: handle_testcase()                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ 1. 解析命令行参数                                                        │  │
│  │ 2. 验证必填参数 target_url                                               │  │
│  │ 3. 创建 TestCaseGenerator 实例                                          │  │
│  │ 4. 调用 generate_scenario_testcase()                                    │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  testcase_generator.py: generate_scenario_testcase()                         │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ 步骤 1: 文件存在性检查                                                   │  │
│  │        os.path.exists(har_file_path)                                   │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │ 步骤 2: 匹配 HAR 文件对应的 API 文件                                     │  │
│  │        match_api_files_for_har(har_file_path)                          │  │
│  │        ├── HARParser.extract_requests_from_har()                       │  │
│  │        │   └── 解析 HAR JSON，提取每个请求的详细信息                     │  │
│  │        ├── 获取所有 API 文件列表                                         │  │
│  │        └── URLMatcher.find_matching_api_file()                          │  │
│  │            └── 多策略匹配: 直接匹配 → 双向匹配 → 标准化匹配               │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │ 步骤 3: 查找目标 URL 对应的 API 文件                                     │  │
│  │        URLMatcher.find_matching_api_file(target_url, api_files)        │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │ 步骤 4: 获取 API 文件信息                                                │  │
│  │        _get_api_file_info(target_api_file)                             │  │
│  │        └── parse_api_file()                                             │  │
│  │            └── 从 API 文件提取: 函数名、描述、URL、参数、请求头等         │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │ 步骤 5: 生成输出文件路径                                                 │  │
│  │        get_output_dir() + os.path.join()                               │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │ 步骤 6: 生成测试用例内容                                                 │  │
│  │        generate_scenario_test_content()                                    │  │
│  │        ├── 导入语句生成                                                  │  │
│  │        ├── test_headers fixture 生成                                    │  │
│  │        ├── Allure 装饰器生成                                            │  │
│  │        └── 测试步骤生成 (遍历 requests)                                │  │
│  │            ├── 查找 API 函数                                            │  │
│  │            ├── 合并参数 merge_request_params()                         │  │
│  │            ├── 格式化参数 format_params_for_python()                    │  │
│  │            └── 生成断言代码                                               │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │ 步骤 7: 写入文件并格式化                                                │  │
│  │        write_test_file()                                                │  │
│  │        └── format_python_file()                                        │  │
│  │            ├── ruff check --fix                                         │  │
│  │            └── ruff format                                              │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           生成测试用例文件                                    │
│  testcases/test_mgmt_prmt_luckyActivity_luckyActivityList.py               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 四、生成的测试用例结构

```python
import os
import pytest
import allure
from allure_commons.types import Severity

from apis.mall_mgmt_application import _mgmt_prmt_luckyActivity_luckyActivityList


@pytest.fixture(scope="module")
def test_headers():
    return {
        "channel": "pc",
        "client": "op",
        "authorization": f"bearer {os.environ['access_token']}",
    }


@pytest.mark.test_{task_id}
@allure.severity(Severity.CRITICAL)
@allure.feature("mall_mgmt_application")
@allure.story("/mgmt/prmt/luckyActivity/luckyActivityList")
@allure.title("抽奖活动列表")
def test_mgmt_prmt_luckyActivity_luckyActivityList(test_headers):

    # 初始化测试数据字典，用于在步骤间传递数据
    test_data = {}

    @allure.step("抽奖活动列表")
    def step_mgmt_prmt_luckyActivity_luckyActivityList():
        params = {
                    "page": 1,
                    "size": 10
                }
        with _mgmt_prmt_luckyActivity_luckyActivityList(
            params=params, headers=test_headers
        ) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200
            test_data["response"] = r.json()

    # 执行所有测试步骤
    step_mgmt_prmt_luckyActivity_luckyActivityList()
```

---

## 五、关键数据转换示例

### 5.1 HAR 文件原始数据

```json
{
  "log": {
    "entries": [{
      "_resourceType": "xhr",
      "request": {
        "method": "POST",
        "url": "https://api.example.com/mgmt/prmt/luckyActivity/luckyActivityList?timestamp=123",
        "headers": [
          {"name": "Content-Type", "value": "application/json"},
          {"name": "Authorization", "value": "Bearer xxx"}
        ],
        "queryString": [
          {"name": "timestamp", "value": "123"}
        ],
        "postData": {
          "mimeType": "application/json",
          "text": "{\"page\":1,\"size\":10}"
        }
      },
      "response": {...}
    }]
  }
}
```

### 5.2 解析后的 request_info

```python
request_info = {
    "method": "POST",
    "url": "/mgmt/prmt/luckyActivity/luckyActivityList",
    "full_url": "https://api.example.com/mgmt/prmt/luckyActivity/luckyActivityList?timestamp=123",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer xxx"
    },
    "content_type": "application/json",
    "query_params": {"timestamp": "123"},
    "post_data": {"page": 1, "size": 10},
    "response_status": 200,
    "response_content": {...},
    "response_time": 156,
    "server_ip": "192.168.1.1"
}
```

### 5.3 合并后的参数

```python
api_params = {
    "page": 1,
    "size": 10,
    "timestamp": "123"  # query_params 被合并
}
```

---

## 六、异常处理

| 异常场景 | 处理方式 | 返回值 |
|---------|---------|-------|
| HAR 文件不存在 | 记录日志 | `None` |
| HAR 文件 JSON 格式错误 | 记录日志 | `[]` |
| 没有 XHR 请求 | 记录日志 | `[]` |
| API 文件不存在 | 记录日志 | `None` |
| URL 匹配失败 | 记录日志 | `None` |
| 格式化失败 | 记录警告 | 继续执行 |

---

## 七、配置说明

### 7.1 URL 过滤配置 (`kill_urls`)

在 `config.py` 中定义需要过滤的 URL 关键字：

```python
KILL_URLS = [
    "/auth/captcha",      # 验证码接口
    "/common/config",     # 公共配置接口
    "/user/login",         # 登录接口（测试环境可能需要）
]
```

### 7.2 Base URLs 配置

用于标准化 URL，移除域名部分：

```python
BASE_URLS = [
    "https://api.example.com",
    "https://api-staging.example.com",
]
```

### 7.3 默认请求头配置

```python
HEADERS_TO_INCLUDE = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
}
```

---

## 八、核心模块职责

| 模块 | 职责 | 关键方法 |
|------|------|----------|
| `__main__.py` | 命令行入口，参数解析 | `handle_testcase()` |
| `testcase_generator.py` | 测试用例生成核心逻辑 | `generate_scenario_testcase()`, `generate_scenario_test_content()` |
| `har_parser.py` | HAR 文件解析 | `extract_requests_from_har()` |
| `url_matcher.py` | URL 匹配与标准化 | `find_matching_api_file()`, `normalize_url()` |
| `utils.py` | 工具函数 | `parse_api_file()`, `merge_request_params()`, `format_params_for_python()` |
| `config.py` | 配置管理 | `APIConfig.get_config()` |

---

## 九、总结

整个 `har2pytest testcase` 命令的执行过程可以概括为：

1. **入口处理**: 解析命令行参数，验证必填项
2. **HAR 解析**: 读取并解析 HAR 文件，提取所有 XHR 请求
3. **API 匹配**: 查找每个请求对应的 API 文件
4. **内容生成**: 生成完整的 pytest 测试用例代码
5. **文件输出**: 写入文件并使用 ruff 格式化

**核心特点**:
- 支持复杂场景模式，生成流程化测试用例
- 使用 `@pytest.fixture` 管理共享的请求头
- 自动匹配 HAR 请求与 API 文件
- 支持 f-string 格式的动态请求头（如 `authorization`）
- 代码自动格式化，保证代码质量
