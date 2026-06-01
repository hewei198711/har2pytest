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
| `--url /mgmt/prmt/luckyActivity/luckyActivityList` | 目标接口 URL |

---

## 一、方法调用顺序

```
handle_testcase (入口)
  └─> TestCaseGenerator.__init__
  └─> TestCaseGenerator.generate_scenario_testcase
        ├─> os.path.exists (文件存在性检查)
        ├─> TestCaseGenerator.match_api_files_for_har
        │     ├─> HARParser.extract_requests_from_har
        │     │     └─> TestCaseGenerator._prepare_url_matcher
        │     │     └─> URLMatcher.get_url_info
        │     ├─> TestCaseGenerator._get_all_api_files
        │     └─> URLMatcher.find_matching_api_file
        │
        ├─> URLMatcher.find_matching_api_file (查找目标API文件)
        ├─> get_output_dir
        ├─> TestCaseGenerator._get_api_file_info
        │     └─> parse_api_file
        │
        ├─> TestCaseGenerator.generate_test_case_content
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

```python
def handle_testcase(args):
    """处理 testcase 命令"""
    har_file = args.har_file          # "抽奖活动.har"
    pattern = args.pattern            # "complex_scenario"
    task_id = args.mark               # None
    target_url = args.url             # "/mgmt/prmt/luckyActivity/luckyActivityList"
    output_dir = args.output          # 默认输出目录
    api_dir = args.api_dir            # 默认API目录
```

**处理流程**:
1. 验证必填参数 `target_url` 是否存在
2. 创建 `TestCaseGenerator` 实例
3. 调用 `generator.generate_scenario_testcase(har_file, target_url, task_id)`

---

### 2.2 测试用例生成器初始化 (`TestCaseGenerator.__init__`)

**文件位置**: `har2pytest/testcase_generator.py:35-72`

```python
def __init__(self, api_dir=None, output_dir=None, filter_duplicate_url=False,
             base_urls=None, kill_urls=None):
```

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
│                                                                 │
│    target_url = "/mgmt/prmt/luckyActivity/luckyActivityList"   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. 生成输出文件路径                                              │
│    output_dir = get_output_dir(self.output_dir, task_id)        │
│    test_filepath = os.path.join(output_dir,                     │
│                        f"test_{clean_function_name}.py")       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. 生成测试用例内容                                              │
│    test_content = generate_test_case_content(                   │
│        har_file_path, api_files, task_id,                       │
│        target_api_file, target_url)                             │
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
│    with open(har_file_path, encoding="utf-8") as f:              │
│        har_data = json.load(f)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. 遍历所有请求条目 (entries)                                    │
│    for i, entry in enumerate(entries):                          │
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
│ 4. 提取请求头 (headers)                                          │
│    headers = {}                                                  │
│    for header in request.get("headers", []):                    │
│        headers[header["name"]] = header["value"]                │
│                                                                 │
│    # 转换格式:                                                  │
│    # 输入: [{"name": "Content-Type", "value": "application/json"}]│
│    # 输出: {"Content-Type": "application/json"}                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. 提取查询参数 (query_params)                                   │
│    query_params = {}                                             │
│    for param in request.get("queryString", []):                  │
│        query_params[param["name"]] = unquote(param["value"])    │
│                                                                 │
│    # URLDecode 解码处理                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. 提取 POST 数据 (post_data)                                    │
│                                                                 │
│    根据 Content-Type 分别处理:                                   │
│                                                                 │
│    a) multipart/form-data:                                      │
│       - 从 params 数组提取参数                                   │
│       - 组装为字典                                               │
│                                                                 │
│    b) application/json:                                         │
│       - 解析 JSON 文本                                           │
│       - 返回字典对象                                             │
│                                                                 │
│    c) 其他类型:                                                  │
│       - 抛出 ValueError                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. 清理 URL                                                     │
│    # 移除 query 参数和 base URL                                  │
│    clean_url = URLMatcher.normalize_url(full_url, base_urls)    │
│                                                                 │
│    # 示例:                                                      │
│    # 输入: "https://api.example.com/mgmt/prmt/luckyActivity/..." │
│    # 输出: "/mgmt/prmt/luckyActivity/luckyActivityList"         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. 组装请求信息字典                                              │
│    request_info = {                                             │
│        "method": "POST",                                         │
│        "url": "/mgmt/prmt/luckyActivity/luckyActivityList",     │
│        "full_url": "https://api.example.com/...",               │
│        "headers": {...},                                        │
│        "content_type": "application/json",                      │
│        "query_params": {...},                                    │
│        "post_data": {...},                                      │
│        "response_status": 200,                                  │
│        "response_content": {...},                                │
│        "response_time": 123,                                     │
│    }                                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. 过滤重复 URL                                                 │
│    url_key = f"{method}:{clean_url}"                            │
│    if url_key in seen_urls: continue                            │
│    seen_urls.add(url_key)                                       │
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

### 2.6 测试用例内容生成 (`generate_test_case_content`)

**文件位置**: `har2pytest/testcase_generator.py:415-645`

**生成流程**:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. 解析 HAR 文件                                                 │
│    requests = har_parser.extract_requests_from_har(...)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. 预加载所有 API 文件信息                                       │
│    for api_file in api_files:                                   │
│        _get_api_file_info(api_file)  # 写入缓存                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. 生成导入部分                                                  │
│    import os                                                    │
│    import pytest                                                │
│    import allure                                               │
│    from allure_commons.types import Severity                    │
│                                                                 │
│    from apis.{service_package} import {function_name}            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. 生成 Allure 装饰器                                            │
│    @pytest.mark.test_{task_id}                                  │
│    @allure.severity(Severity.CRITICAL)                         │
│    @allure.feature('{service_package}')                         │
│    @allure.story('{api_url}')                                   │
│    @allure.title('{api_description}')                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. 生成测试函数定义                                              │
│    def test_{function_name}():                                  │
│        # 初始化测试数据字典                                      │
│        test_data = {                                            │
│            "headers": {                                         │
│                "channel": "pc",                                 │
│                "client": "op",                                 │
│                "content-type": "application/json;charset=UTF-8",│
│                "authorization": f"bearer {os.environ[...]}",   │
│            },                                                   │
│        }                                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. 遍历所有请求，生成测试步骤                                    │
│    for i, request_info in enumerate(requests):                 │
│                                                                 │
│        # 查找对应的 API 函数                                     │
│        api_function, api_description = find_api_function(...)   │
│                                                                 │
│        # 生成步骤函数                                            │
│        @allure.step("{api_description}")                       │
│        def step_{function_name}():                              │
│            # 合并参数                                            │
│            api_params = merge_request_params(request_info)      │
│            api_params = format_params_for_python(api_params)    │
│                                                                 │
│            # 根据请求类型生成调用代码                            │
│            if method == "POST" and is_file_upload:              │
│                with api_function(files=files,                   │
│                                   headers=test_data['headers']):│
│                    assert ...                                   │
│            elif method == "POST":                               │
│                with api_function(data=data,                     │
│                                   headers=test_data['headers']):│
│                    assert ...                                   │
│            else:  # GET                                          │
│                with api_function(params=params,                 │
│                                   headers=test_data['headers']):│
│                    assert ...                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2.7 参数合并 (`merge_request_params`)

**文件位置**: `har2pytest/utils.py:285-302`

```python
def merge_request_params(request_info):
    """合并请求中的 query_params 和 post_data"""
    params = {}

    # 1. 添加查询参数
    if request_info.get("query_params"):
        params.update(request_info["query_params"])

    # 2. 添加 POST 数据
    if request_info.get("post_data"):
        if isinstance(request_info["post_data"], dict):
            params.update(request_info["post_data"])

    return params
```

**合并示例**:

```python
# 输入
request_info = {
    "query_params": {"page": 1, "size": 10},
    "post_data": {"name": "测试", "status": 1}
}

# 输出
params = {
    "page": 1,
    "size": 10,
    "name": "测试",
    "status": 1
}
```

---

### 2.8 参数格式化 (`format_params_for_python`)

**文件位置**: `har2pytest/utils.py:46-51`

```python
def format_params_for_python(params, indent=12):
    """将参数字典格式化为 Python 代码字符串"""
    # 使用 json.dumps 格式化字典，保持缩进一致
    # 处理引号转义
```

**格式化示例**:

```python
# 输入
params = {"name": "测试", "code": 200, "flag": True}

# 输出
params = {
            "name": "测试",
            "code": 200,
            "flag": True
        }
```

---

### 2.9 文件写入与格式化 (`write_test_file`)

**文件位置**: `har2pytest/utils.py:88-107`

```python
def write_test_file(filepath, content):
    # 1. 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. 使用 ruff 格式化
    # 2.1 修复代码问题
    subprocess.run([sys.executable, "-m", "ruff", "check", "--fix", filepath])

    # 2.2 格式化代码
    subprocess.run([sys.executable, "-m", "ruff", "format", filepath])
```

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
│  │        generate_test_case_content()                                    │  │
│  │        ├── 导入语句生成                                                  │  │
│  │        ├── Allure 装饰器生成                                            │  │
│  │        ├── 测试数据初始化                                                │  │
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

from apis.mall_mgmt_application import mgmt_prmt_luckyActivity_luckyActivityList


@pytest.mark.test_{task_id}
@allure.severity(Severity.CRITICAL)
@allure.feature("mall_mgmt_application")
@allure.story("/mgmt/prmt/luckyActivity/luckyActivityList")
@allure.title("抽奖活动列表")
def test_mgmt_prmt_luckyActivity_luckyActivityList():

    # 初始化测试数据字典，用于在步骤间传递数据
    test_data = {
        "headers": {
            "channel": "pc",
            "client": "op",
            "content-type": "application/json;charset=UTF-8",
            "authorization": f"bearer {os.environ['access_token']}",
        },
    }

    @allure.step("抽奖活动列表")
    def step_mgmt_prmt_luckyActivity_luckyActivityList():
        params = {
                    "page": 1,
                    "size": 10
                }
        with mgmt_prmt_luckyActivity_luckyActivityList(
            params=params, headers=test_data["headers"]
        ) as r:
            assert r.status_code == 200
            assert r.json()["code"] == 200

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
    "query_params": {
        "timestamp": "123"
    },
    "post_data": {
        "page": 1,
        "size": 10
    },
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

---

## 八、总结

整个 `har2pytest testcase` 命令的执行过程可以概括为：

1. **入口处理**: 解析命令行参数，验证必填项
2. **HAR 解析**: 读取并解析 HAR 文件，提取所有 XHR 请求
3. **API 匹配**: 查找每个请求对应的 API 文件
4. **内容生成**: 生成完整的 pytest 测试用例代码
5. **文件输出**: 写入文件并使用 ruff 格式化

核心模块交互：
- `__main__.py` - 命令行入口
- `testcase_generator.py` - 测试用例生成逻辑
- `har_parser.py` - HAR 文件解析
- `url_matcher.py` - URL 匹配逻辑
- `utils.py` - 工具函数
