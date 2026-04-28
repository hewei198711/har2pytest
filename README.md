# har2pytest - API 测试用例生成和更新工具使用说明

## 概述

`har2pytest` 是一个功能完整的API测试用例生成和更新工具，整合了HAR文件解析、API文件生成、Swagger文档更新等功能。

**特性**：

- 统一的配置管理（`APIConfig` 类）
- 路径URL参数处理（如 `{params['cardNo']}` → `{cardNo}`）
- 无效参数自动过滤（集中在HARParser中处理）
- 生成文件语法验证
- 自动查找Swagger文档更新API
- 测试用例格式化（正确处理列表和字典缩进）
- 统一的布尔值转换逻辑（支持true/false字符串转换）

- 查询类参数化测试用例生成（list_query模式，支持参数组合测试）
- 复杂场景流程测试用例生成（complex_scenario模式，支持指定接口测试）

## 安装

### 1. 安装依赖

```bash
# 克隆代码库后，在项目根目录执行
pip install -e .
```

### 2. 验证安装

```bash
# 查看版本和帮助信息
har2pytest help
```

## 主要功能

### 1. HAR文件解析 (`HARParser` 类)

- 解析HAR（HTTP Archive）文件，提取API请求信息
- 过滤非API请求（CSS、JS、图片等）
- 支持GET、POST等HTTP方法
- 自动解析请求头、查询参数、POST数据
- 支持响应内容解析和统计信息
- **集中无效参数过滤**：在解析阶段自动过滤无效参数（rnd、timestamp等）
- **布尔值自动转换**：将字符串形式的true/false转换为Python布尔值
- **统一参数处理**：查询参数和POST数据都经过相同的清理流程

### 2. API文件生成 (`APIGenerator` 类)

- 根据HAR文件自动生成Python API接口文件
- 智能识别服务包，按模块组织文件
- 支持参数转义和代码生成
- 自动生成函数定义和调用代码
- 跳过已存在的接口，避免重复生成

### 3. Swagger文档处理 (`SwaggerHandler` 类)

- 从Swagger文档获取接口描述和参数说明
- 自动更新API文件中的TODO注释
- 支持多种参数格式匹配
- 缓存文档数据，提高性能
- 从Swagger文档生成API文件
- 支持解析Swagger文档中的参数和模型

### 4. 测试用例生成 (`TestCaseGenerator` 类)

- 从HAR文件生成pytest+allure框架的测试用例
- 每个API请求作为一个测试步骤，支持步骤化测试
- 自动匹配API文件和HAR请求
- 生成完整的测试数据传递和断言逻辑
- 支持allure报告和日志记录
- 自动识别URL参数模式（如卡号替换）
- **改进的格式化**：正确处理列表和字典的缩进，避免格式错误
- **智能缩进处理**：多行内容（列表/字典）自动添加正确的tab缩进
- **参数化测试格式**：支持基于类结构的参数化测试用例生成
- **查询类测试**：支持list_query模式生成参数组合测试用例
- **复杂场景测试**：支持complex_scenario模式生成指定接口测试用例

## 使用方法

### 基本命令格式

```bash
har2pytest <command> [arguments]
```

### 支持的命令

#### 1. 生成API文件

```bash
# 使用默认参数
har2pytest generate

# 指定HAR文件和输出目录
har2pytest generate api_request.har api

# 只指定HAR文件（使用默认输出目录）
har2pytest generate api_request.har

# 强制覆盖已存在的文件
har2pytest generate api_request.har api --overwrite
```

#### 2. 从Swagger文档生成API文件

```bash
# 从Swagger文档生成API文件
har2pytest swagger https://petstore.swagger.io/v2/api-docs api

# 强制覆盖已存在的文件
har2pytest swagger https://petstore.swagger.io/v2/api-docs api --overwrite

# 只生成指定路径的API文件
har2pytest swagger https://petstore.swagger.io/v2/api-docs api --path /pet/{petId}
```

#### 3. 生成测试用例

```bash
# 使用默认参数
har2pytest testcase

# 指定HAR文件和输出目录
har2pytest testcase api_request.har testcases

# 只指定HAR文件（使用默认输出目录）
har2pytest testcase api_request.har
```

#### 4. 查看HAR文件摘要

```bash
# 查看默认HAR文件
har2pytest summary

# 指定HAR文件
har2pytest summary api_request.har
```

#### 5. 生成查询类参数化测试用例（list_query模式）

```bash
# 命令格式: har2pytest testcase list_query [task_id] [har_file]
# 示例：从兑换单代客售后.har 生成查询类测试用例，输出到 testcases/版本接口测试/test_4291/
har2pytest testcase list_query test_4291 兑换单代客售后.har

# 参数说明：
# - task_id: 任务ID（如 test_4295），会自动去掉 test_ 前缀，生成目录 testcases/版本接口测试/4295/
# - har_file: HAR文件路径
```

#### 6. 生成复杂场景流程测试用例（complex_scenario模式）

```bash
# 命令格式: har2pytest testcase complex_scenario [task_id] [url] [har_file]
# 示例：从代客售后.har 生成复杂场景测试用例
har2pytest testcase complex_scenario test_4295 /user/mgmt/order/return/submit 代客售后.har

# 参数说明：
# - task_id: 任务ID（如 test_4295），会自动去掉 test_ 前缀，生成目录 testcases/版本接口测试/4295/
# - url: 目标接口URL，工具会找到该接口并生成完整的测试用例
# - har_file: HAR文件路径
# 注意：如果 task_id 是 .har 文件，则自动切换为 list_query 模式
```


## 类结构说明

### APIConfig 类

```python
class APIConfig:
    """API配置类，包含服务包映射、默认配置和Swagger文档地址"""

    @staticmethod
    def determine_service_package(url: str) -> str:
        # 根据URL判断服务包

    # 配置属性
    BASE_URL = "https://uc-test.perfect99.com/api"
    KILL_URL = "arms-retcode.aliyuncs.com"
    SERVICE_MAPPING = {...}
    SWAGGER_DOC_URLS = {...}
    INVALID_PARAMS = {...}
```

### HARParser 类

```python
class HARParser:
    """HAR文件解析器"""

    def __init__(self, base_url=APIConfig.BASE_URL, 
                 kill_url=APIConfig.KILL_URL):
        # 初始化解析器，使用APIConfig配置

    def extract_requests_from_har(self, har_file_path, filter_duplicate_url=True):
        # 提取API请求信息，支持多种POST数据格式
        # 在解析阶段自动过滤无效参数和转换布尔值

    def filter_invalid_params(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # 过滤无效参数，使用APIConfig.INVALID_PARAMS配置

    def print_api_summary(self, har_file_path):
        # 打印API请求摘要
```

### APIGenerator 类

```python
class APIGenerator:
    """API文件生成器"""

    def __init__(self, output_dir=APIConfig.DEFAULT_SERVICE_PACKAGE):
        # 初始化生成器，使用APIConfig配置
        # 初始化Swagger文档处理器和HAR生成器

    def filter_invalid_params(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # 过滤无效参数，使用APIConfig.INVALID_PARAMS

    def sanitize_filename(self, filename: str) -> str:
        # 清理文件名，移除不合法字符

    def generate_api_files_from_har(self, har_file_path: str) -> List[str]:
        # 从HAR文件生成API文件，支持语法验证

    def generate_api_file(self, request_info):
        # 生成单个API文件，自动创建目录结构
        # 支持路径参数接口的参数化处理

    def generate_file_content(self, request_info: Dict[str, Any], function_name: str) -> str:
        # 生成API文件内容，支持路径参数模板化
        # 为路径参数接口生成params参数和f-string格式的URL

    def generate_index_file(self, generated_files):
        # 生成索引文件，包含时间戳和注释

    def generate_apis_from_swagger(self, swagger_url: str, force_overwrite: bool = False) -> List[str]:
        # 从Swagger文档生成API文件，解析所有API路径和方法
```

### TestCaseGenerator 类

```python
class TestCaseGenerator:
    """pytest用例生成器"""

    def __init__(self, api_dir="api", output_dir="testcases", test_format="step"):
        # 初始化生成器，支持多种测试格式：step（步骤化）和param（参数化）

    def extract_function_name_from_file(self, filepath: str) -> Optional[str]:
        # 从API文件中提取函数名

    def extract_url_from_file(self, filepath: str) -> Optional[str]:
        # 从API文件中提取URL路径，支持{params['cardNo']}替换

    def format_params_for_test_case(self, params_dict: Dict[str, Any]) -> str:
        # 格式化测试用例参数，正确处理列表和字典的缩进
        # 多行内容自动添加3个tab的距离，确保格式正确

    def generate_test_case_from_har(self, har_file_path, output_subdir=None):
        # 从HAR文件生成pytest用例，支持步骤化测试



    def find_api_files_for_har(self, har_file_path):
        # 根据HAR文件查找对应的API文件
```

### SwaggerHandler 类

```python
class SwaggerHandler:
    """Swagger文档处理器"""

    def __init__(self):
        # 初始化处理器，设置文档缓存和API生成器引用

    def set_api_generator(self, api_generator):
        # 设置API生成器实例

    def extract_url_from_file(self, filepath: str) -> Optional[str]:
        # 从API文件中提取URL，支持{params['cardNo']}替换

    def get_swagger_doc(self, service_base_url: str) -> Optional[Dict[str, Any]]:
        # 获取Swagger文档数据，支持缓存

    def find_api_info_in_swagger(self, swagger_data, api_path, method='GET'):
        # 在Swagger文档中查找API信息，支持多种匹配方式

    def scan_and_update_apis(self, api_dir="api"):
        # 扫描并更新API文件，使用APIConfig.SWAGGER_DOC_URLS

    def update_api_file(self, filepath, api_info):
        # 更新单个API文件的TODO注释

    def _extract_params_from_swagger(self, parameters: List[Dict[str, Any]], swagger_data: Dict[str, Any]) -> tuple:
        # 从Swagger文档提取参数

    def _get_default_value(self, param_type: str) -> Any:
        # 根据参数类型获取默认值

    def _extract_body_params(self, schema: Dict[str, Any], swagger_data: Dict[str, Any]) -> Dict[str, Any]:
        # 从body参数schema中提取参数

    def generate_apis_from_swagger(self, swagger_url: str, force_overwrite: bool = False) -> List[str]:
        # 从Swagger文档生成API文件，解析所有API路径和方法
```

## 配置说明

### APIConfig 配置类

所有配置都集中在 `APIConfig` 类中，包括：

#### 基础配置

```python
BASE_URL = "https://uc-test.perfect99.com/api"  # 基础URL，用于清理URL中的前缀
KILL_URL = "arms-retcode.aliyuncs.com"  # 过滤掉包含特定关键字的接口请求
DEFAULT_SERVICE_PACKAGE = 'api'  # 默认服务包
```

#### 服务包映射

工具根据URL前缀自动识别服务包：

```python
SERVICE_MAPPING = {
    'appstore': 'mall_store_application',
    'store': 'mall_center_store',
    'mobile': 'mall_mobile_application',
    'invt': 'mall_center_inventory',
    'mgmt': 'mall_mgmt_application',
    'xxl': 'basic_services',
    'oss': 'oss_json'
}
```

#### Swagger文档地址

```python
SWAGGER_DOC_URLS = {
    'mall_mgmt_application': "https://uc-test.perfect99.com/sw/mall-mgmt-application",
    "mall_center_inventory": "https://uc-dev.perfect99.com/sw/mall-center-inventory",
    "mall_center_store": "https://uc-dev.perfect99.com/sw/mall-center-store",
    'mall_store_application': "https://uc-dev.perfect99.com/sw/mall-store-application/appStore",
    'mall_mobile_application': "https://uc-test.perfect99.com/sw/mall-mobile-application",
    'settle_job': "https://uc-dev.perfect99.com/sw/settle-job",
    # basic_services 没有接口文档，忽略
}
```

#### 路径参数接口配置

```python
PATH_URLS = [
    "/mobile/msg/manage/letter/dashbord/{usrId}",
    "/mobile/msg/manage/letter/dashbord/{usrId}/{systemId}", # 用户站内信列表,按消息类型分类
    "/mobile/order/carts/getRecommendProduct/{serialNo}", # 根据商品编码获取顺手买一件商品集合
    "/mobile/order/before/by/store/{cardNo}", # /mobile/order/before/by/store/{cardNo}
    "/mobile/order/before/by/{cardNo}", # 根据用户卡号查询是否可购买商品
]
```

#### 无效参数过滤

```python
INVALID_PARAMS = {
    # 通用无效参数
    'rnd', 'timestamp', '_t', '_timestamp', 'v', 'version',
    # 特定接口的无效参数
    'channelType',  # 支付渠道控制接口中的无效参数
}
```

## 生成的文件结构

```python
api/                              # API接口文件目录
├── __init__.py                    # 索引文件
├── _appStore_complex_intro.py     # API接口文件
├── _mobile_order_before.py        # API接口文件
├── mall_center_inventory/         # 服务包目录
│   ├── _invt_controlLine_getControlLineSetData.py
│   └── ...
├── mall_center_order/             # 服务包目录
│   ├── _order_orderSign_detail.py
│   └── ...
└── basic_services/                # 服务包目录（无文档更新）
    └── _auth_getUserInfo.py

testcases/                        # 测试用例文件目录
├── 签约购/                        # HAR文件对应的测试目录
│   └── test_签约购.py             # pytest测试用例文件
├── 其他业务/                      # 其他HAR文件对应的测试目录
│   └── test_其他业务.py
└── ...
```

## 示例输出

### HAR文件摘要

```bash
har2pytest summary api_request.har
开始解析HAR文件，共 71 个请求记录
解析完成，提取到 22 个有效的API请求

HAR文件: api_request.har
共发现 22 个API请求
--------------------------------------------------------------------------------
 1. GET    200    59.19ms /appStore/complex/intro
 2. GET    200    67.80ms /appStore/complex/promotionList
 ...
--------------------------------------------------------------------------------
统计: 成功 22 个, 失败 0 个, 平均响应时间 265.20ms
```

### API文件生成

```bash
har2pytest generate api_request.har api
从HAR文件生成API接口文件: api_request.har
输出目录: api
--------------------------------------------------
发现 22 个API请求
--------------------------------------------------
生成API文件: api/mall_store_application/_appStore_complex_intro.py (服务包: mall_store_application)
生成API文件: api/mall_center_order/_mobile_order_before_thrivingHistoryList.py (服务包: mall_center_order)
...
--------------------------------------------------
成功生成 22 个API接口文件
生成索引文件: api/__init__.py
```

### 文档更新

```bash
har2pytest update api
更新API目录中的文档信息: api
--------------------------------------------------
正在获取Swagger文档: https://uc-dev.perfect99.com/sw/mall-center-inventory/v2/api-docs
✓ 成功获取 45 个API路径
✓ 更新接口描述: 获取管控线相关设置数据...
✓ 更新参数 storeCode: 门店编码...
✓ 更新成功: api/mall_center_inventory/_invt_controlLine_getControlLineSetData.py
...
```

### 测试用例生成

```bash
har2pytest testcase api_request.har testcases
从HAR文件生成pytest用例: api_request.har
输出目录: testcases
--------------------------------------------------
找到 22 个对应的API文件
生成测试用例文件: testcases/签约购/test_签约购.py
--------------------------------------------------
成功生成测试用例文件: testcases/签约购/test_签约购.py
```



### 查询类参数化测试用例生成（list_query模式）

```bash
har2pytest testcase list_query test_4291 兑换单代客售后.har
生成查询类测试用例: 兑换单代客售后.har
任务ID: test_4291
--------------------------------------------------
生成测试用例文件: testcases/版本接口测试/test_4291/test_user_mgmt_order_return_queryOrder.py
生成测试用例文件: testcases/版本接口测试/test_4291/test_user_mgmt_order_return_submit.py
--------------------------------------------------
成功生成 2 个测试用例文件
```

### 复杂场景流程测试用例生成（complex_scenario模式）

```bash
har2pytest testcase complex_scenario test_4291 /user/mgmt/order/return/submit 代客售后.har
生成复杂场景测试用例: 代客售后.har
任务ID: test_4291
目标接口: /user/mgmt/order/return/submit
--------------------------------------------------
生成测试用例文件: testcases/版本接口测试/4291/test_user_mgmt_order_return_submit.py
--------------------------------------------------
成功生成测试用例文件: testcases/版本接口测试/4291/test_user_mgmt_order_return_submit.py
```

## 测试用例功能说明

### 生成的测试用例特点

- **pytest框架**: 基于pytest测试框架，支持丰富的断言和测试工具
- **allure报告**: 集成allure测试报告，提供详细的测试步骤和结果展示
- **步骤化测试**: 每个API请求作为一个独立的测试步骤，便于定位问题
- **数据传递**: 支持测试步骤间的数据传递和共享
- **异常处理**: 完善的异常捕获和错误日志记录
- **断言验证**: 自动生成状态码和业务响应的断言

### 测试用例结构

#### 步骤化测试格式（原有格式）

```python
@allure.severity(P1)
@allure.feature('签约购')
@allure.story('基于HAR文件的API测试')
@pytest.mark.skipif(1 in currentStages, reason='暂不执行')
@allure.title('签约购 - API接口测试')
def test_har_api_flow():
    """基于HAR文件 api_request.har 的API流程测试"""

    # 初始化测试数据字典
    test_data = {
        "access_token": access_token,
    }

    @allure.step("GET /appStore/complex/intro")
    def step_1_get_appstore_complex_intro():
        try:
            with _appStore_complex_intro(access_token=test_data['access_token']) as r:
                assert r.status_code == 200
                assert r.json()['code'] == 200
                test_data['response_1'] = r.json()
                logger.info("步骤 1 GET /appStore/complex/intro 执行成功")
        except Exception as e:
            logger.error(f"步骤 1 GET /appStore/complex/intro 执行失败: {str(e)}")
            raise

    # 执行所有测试步骤
    step_1_get_appstore_complex_intro()
    # ... 更多步骤
```

#### 参数化测试格式（新增功能）

基于`test_user_mgmt_audience_editAudienceProduct.py`格式的参数化测试：

```python
# coding:utf-8
import os
import pytest
import allure
from setting import P1, P2, P3
from util.logger import logger
from api.mall_center_user._user_mgmt_audience_editAudienceProduct import _user_mgmt_audience_editAudienceProduct

@allure.feature('user')
@allure.story('/user/mgmt/audience/editAudienceProduct')
class TestClass:
    def setup_class(self):
        self.access_token = os.environ["access_token"]

    @pytest.mark.test_4270
    @pytest.mark.parametrize("doc, code, message, p", [
        ("测试用例描述", 200, "success", P1),
    ])
    def test_user_mgmt_audience_editAudienceProduct(self, doc, code, message, p):
        """用例描述 TODO"""
        allure.dynamic.title(doc)
        data = {
            "audienceId": "d09d0f871825442d83ff5e6a66b0017a",
            "productList": [
                {
                    "productType": 1,
                    "serialNo": "SGH006"
                }
            ]
        }

        with _user_mgmt_audience_editAudienceProduct(access_token=self.access_token, data=data) as r:
            assert r.status_code == code
            assert r.json()["message"] == message
```

**参数化测试格式特点**：

- **类结构**: 使用类组织测试用例，便于管理setup和teardown方法
- **参数化**: 使用`@pytest.mark.parametrize`支持多组测试数据
- **环境变量**: 通过`os.environ`获取access_token等环境变量
- **灵活断言**: 支持自定义状态码、返回消息和优先级参数
- **allure集成**: 完整的allure装饰器支持，包括feature、story、title等
- **单文件生成**: 每个接口生成一个独立的测试文件，便于维护

## 注意事项

1. **文件依赖**: 工具已完全整合，通过 `har2pytest` 命令即可使用
2. **网络访问**: 更新文档功能需要访问Swagger文档地址
3. **权限要求**: 需要对输出目录的写权限
4. **编码格式**: 支持UTF-8编码，处理中文内容无问题
5. **错误处理**: 包含完善的错误处理和日志输出
6. **测试依赖**: 生成测试用例需要确保API文件已存在，且项目配置了pytest和allure环境

## 扩展说明

工具采用面向对象设计，易于扩展和维护：

### 配置扩展

- 添加新的服务包映射：修改 `APIConfig.SERVICE_MAPPING` 字典
- 添加新的Swagger文档地址：修改 `APIConfig.SWAGGER_DOC_URLS` 字典
- 添加新的无效参数过滤：修改 `APIConfig.INVALID_PARAMS` 集合
- 添加新的路径参数接口：修改 `APIConfig.PATH_URLS` 列表
- 修改基础配置：更新 `APIConfig.BASE_URL` 和 `APIConfig.KILL_URL`

### 功能扩展

- 支持新的HTTP方法：扩展 `APIGenerator.generate_file_content` 方法
- 自定义文档解析：继承 `SwaggerHandler` 类
- 添加新的输出格式：扩展 `APIGenerator` 类
- 自定义测试用例模板：修改 `TestCaseGenerator.generate_test_case_content` 方法
- 扩展断言逻辑：在测试用例生成方法中添加更多验证规则

## 最佳实践

### 1. API生成流程

```bash
# 1. 从HAR文件生成API接口（自动处理路径参数）
har2pytest generate api_request.har api

# 2. 从Swagger文档生成API接口
har2pytest swagger https://petstore.swagger.io/v2/api-docs api

# 3. 更新API文档信息
har2pytest update api

# 4. 生成步骤化测试用例（原格式）
har2pytest testcase api_request.har testcases

# 5. 生成查询类参数化测试用例（list_query模式）
har2pytest testcase list_query test_4291 兑换单代客售后.har

# 6. 生成复杂场景测试用例（complex_scenario模式）
har2pytest testcase complex_scenario test_4291 /user/mgmt/order/return/submit 代客售后.har


```

### 2. 测试用例执行

```bash
# 执行特定测试用例
pytest testcases/签约购/test_签约购.py -v

# 生成allure报告
pytest testcases/签约购/test_签约购.py --alluredir=reports

# 查看allure报告
allure serve reports


```

### 3. 批量处理

```bash
# 批量生成多个HAR文件的API和步骤化测试用例
for har in *.har; do
    har2pytest generate "$har" api
    har2pytest testcase "$har" testcases
done



# 批量生成查询类测试用例（指定任务ID）
for har in *.har; do
    har2pytest testcase list_query test_4291 "$har"
done
```

## 常见问题

### 1. 为什么生成的API文件中有些参数被过滤了？

- 答：工具会自动过滤无效参数，如 `rnd`、`timestamp` 等随机参数，这些参数在 `APIConfig.INVALID_PARAMS` 中定义。

### 2. 如何处理路径参数接口？

- 答：工具会自动识别 `APIConfig.PATH_URLS` 中配置的路径参数模式，将实际值替换为参数名，并生成参数化的API文件。

### 3. 为什么生成的测试用例格式不正确？

- 答：工具已经改进了测试用例格式化，正确处理列表和字典的缩进，确保生成的代码格式正确。



### 5. 如何查看HAR文件中的API请求摘要？

- 答：使用 `har2pytest summary` 命令查看HAR文件的API请求摘要，包括请求方法、状态码、响应时间等信息。

## 版本历史

- **v1.0.0** - 初始版本
  - 支持从HAR文件生成API接口文件
  - 支持从HAR文件生成pytest测试用例
  - 支持更新API文档信息
  - 支持路径参数接口处理
  - 支持参数化测试用例生成
  - 支持查询类参数化测试用例生成
  - 支持复杂场景流程测试用例生成
  - 提供 `har2pytest` 命令行工具

- **v1.1.0** - 新增功能
  - 支持从Swagger文档生成API文件
  - 优化代码结构，避免循环引用
  - 增强Swagger文档解析能力
  - 支持自动发现Swagger文档路径

- **v1.2.0** - 代码结构优化
  - 合并工具方法到 utils.py，减少模块数量
  - 统一Swagger相关功能到 swagger_handler.py
  - 重命名 swagger_updater.py 为 swagger_handler.py，更准确反映功能
  - 优化模块间依赖关系，提高代码可维护性
