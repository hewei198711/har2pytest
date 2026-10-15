"""测试 har2pytest.har_generator 模块中 HAR 文件解析与 API 接口文件异步生成的功能与边界。"""

import json
import logging
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from har2pytest.api_generator import APIGenerator
from har2pytest.har_generator import _compute_constant_params, generate_api_files_from_har

# ==================== Fixtures ====================


@pytest.fixture
def mock_generator():
    """工厂 fixture：返回一个可配置 return_value / side_effect 的 mock API 生成器。"""
    def _create(return_value=None, side_effect=None):
        gen = MagicMock()
        gen.generate_api_file = AsyncMock(return_value=return_value, side_effect=side_effect)
        return gen
    return _create


@pytest.fixture
def write_har(tmp_path):
    """工厂 fixture：将 entries 列表写入临时 HAR 文件并返回路径。"""
    def _write(entries, filename="test.har"):
        har_data = {"log": {"entries": entries}}
        har_path = tmp_path / filename
        har_path.write_text(json.dumps(har_data, ensure_ascii=False), encoding="utf-8")
        return har_path
    return _write


# ==================== Mock API 生成测试 ====================


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试从HAR文件生成API文件")
async def test_generate_api_files_from_har(write_har, mock_generator):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {
            "url": "https://example.com/api/user/login",
            "method": "POST",
            "headers": [{"name": "Content-Type", "value": "application/json"}],
            "postData": {"mimeType": "application/json", "text": '{"username": "test"}'},
        },
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 100,
    }])

    gen = mock_generator(return_value="api/_user_login.py")
    generated_files = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert len(generated_files) == 1
    assert generated_files[0] == "api/_user_login.py"
    gen.generate_api_file.assert_called_once()


@allure.feature("HAR生成器")
@allure.story("空HAR文件")
@allure.title("测试空HAR文件的情况")
async def test_generate_api_files_from_empty_har(write_har, mock_generator):
    har_path = write_har([])
    gen = mock_generator()

    generated_files = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("生成API文件失败")
@allure.title("测试生成API文件失败的情况")
async def test_generate_api_files_failure(write_har, mock_generator):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {"url": "https://example.com/api/test", "method": "GET", "headers": []},
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 50,
    }])
    gen = mock_generator(side_effect=Exception("生成失败"))

    generated_files = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("不存在的HAR文件")
@allure.title("测试不存在的HAR文件")
async def test_generate_api_files_nonexistent_har(mock_generator):
    gen = mock_generator()

    generated_files = await generate_api_files_from_har("nonexistent.har", api_generator=gen)

    assert len(generated_files) == 0


@allure.feature("HAR生成器")
@allure.story("边界条件")
@allure.title("测试 api_generator 为 None 时直接返回空列表")
async def test_generate_api_files_no_generator():
    result = await generate_api_files_from_har("any.har", api_generator=None)
    assert result == []


@allure.feature("HAR生成器")
@allure.story("边界条件")
@allure.title("测试 HAR 文件缺少 log 键时返回空列表")
async def test_generate_api_files_har_missing_log_key(tmp_path, mock_generator):
    bad_har = tmp_path / "bad_structure.har"
    bad_har.write_text(json.dumps({"not_log": {}}), encoding="utf-8")
    gen = mock_generator()

    result = await generate_api_files_from_har(str(bad_har), api_generator=gen)

    assert result == []


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试 generate_api_file 返回 None 时记录任务跳过日志")
async def test_generate_api_files_process_returns_none(write_har, mock_generator, caplog):
    har_path = write_har([{
        "_resourceType": "xhr",
        "request": {"url": "https://example.com/api/test", "method": "GET", "headers": []},
        "response": {"status": 200, "content": {"text": "{}"}},
        "time": 10,
    }])
    gen = mock_generator(return_value=None)

    with caplog.at_level(logging.DEBUG, logger="har2pytest"):
        result = await generate_api_files_from_har(str(har_path), api_generator=gen)

    assert result == []
    assert "任务跳过" in caplog.text


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试同URL不同方法生成两个文件而不是互相覆盖")
@allure.description("HAR 里同一个 URL 既有 POST 又有 PUT 时，不能并发写同一个文件互相覆盖")
async def test_generate_api_files_same_url_multi_method(tmp_path):

    def entry(method, body):
        return {
            "_resourceType": "xhr",
            "request": {
                "url": "https://example.com/appStore/role",
                "method": method,
                "headers": [{"name": "Content-Type", "value": "application/json"}],
                "postData": {"mimeType": "application/json", "text": body},
            },
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 20,
        }

    test_har = {"log": {"entries": [entry("POST", '{"roleName": "a"}'), entry("PUT", '{"roleName": "b"}')]}}
    har_path = tmp_path / "role.har"
    har_path.write_text(json.dumps(test_har, ensure_ascii=False), encoding="utf-8")

    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    files = await generate_api_files_from_har(str(har_path), force_overwrite=True, api_generator=generator)

    names = sorted(os.path.basename(f) for f in files)
    assert len(names) == 2
    assert any(n.endswith("role.py") for n in names)
    assert any(n.endswith("role_put.py") for n in names)

    contents = {os.path.basename(f): Path(f).read_text(encoding="utf-8") for f in files}
    plain = next(v for k, v in contents.items() if k.endswith("role.py"))
    suffixed = contents[next(k for k in contents if k.endswith("role_put.py"))]
    assert "client.post(" in plain
    assert "client.put(" in suffixed


# ==================== 集成场景测试 ====================


@allure.feature("HAR生成器")
@allure.story("生成API文件")
@allure.title("测试同一模板接口的重复抓包只生成一次")
@allure.description("同一 URL 的多个同方法请求（如重复抓包）只生成一个文件，避免覆盖内容不确定")
async def test_generate_api_files_duplicate_request_skipped(tmp_path, caplog):

    def entry():
        return {
            "_resourceType": "xhr",
            "request": {"url": "https://example.com/api/user/info", "method": "GET", "headers": []},
            "response": {"status": 200, "content": {"text": "{}"}},
            "time": 10,
        }

    test_har = {"log": {"entries": [entry(), entry(), entry()]}}
    har_path = tmp_path / "dup.har"
    har_path.write_text(json.dumps(test_har, ensure_ascii=False), encoding="utf-8")

    generator = APIGenerator(output_dir=str(tmp_path / "apis"))
    with caplog.at_level(logging.DEBUG, logger="har2pytest"):
        files = await generate_api_files_from_har(str(har_path), force_overwrite=True, api_generator=generator)

    assert len(files) == 1
    assert "跳过" in caplog.text


# ==================== _compute_constant_params 单元测试 ====================


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("空快照列表返回空字典")
def test_compute_constant_params_empty():
    assert _compute_constant_params([]) == {}


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("所有请求值相同的参数被识别为常量")
def test_compute_constant_params_all_same():
    snapshots = [
        {"header": "1", "isDisSelfStoreOrder": "0", "keyword": "A"},
        {"header": "1", "isDisSelfStoreOrder": "0", "keyword": "B"},
        {"header": "1", "isDisSelfStoreOrder": "0", "keyword": "C"},
    ]
    result = _compute_constant_params(snapshots)
    assert result["header"] == "1"
    assert result["isDisSelfStoreOrder"] == "0"
    assert "keyword" not in result  # keyword 有不同值


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("值不同但都出现的不算常量参数")
def test_compute_constant_params_different_values():
    snapshots = [
        {"header": "1", "type": "A"},
        {"header": "1", "type": "B"},
    ]
    result = _compute_constant_params(snapshots)
    assert result == {"header": "1"}  # type 有不同值，不是常量


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("只在部分请求出现的参数不算常量")
def test_compute_constant_params_not_in_all_requests():
    snapshots = [
        {"header": "1", "extra": "x"},
        {"header": "1"},
        {"header": "1"},
    ]
    result = _compute_constant_params(snapshots)
    # header 在 3/3 请求中出现且值相同 → 常量
    assert result["header"] == "1"
    # extra 只在 1/3 请求中出现，不足 50% → 非常量
    assert "extra" not in result


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("单条快照中所有参数都是常量")
def test_compute_constant_params_single_snapshot():
    snapshots = [{"a": 1, "b": "hello"}]
    result = _compute_constant_params(snapshots)
    assert result == {"a": 1, "b": "hello"}


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("list/dict 类型值不崩溃且能正确识别为常量")
def test_compute_constant_params_unhashable_values():
    snapshots = [
        {"header": "1", "orderStatusList": [1, 2], "filter": {"type": "a"}},
        {"header": "1", "orderStatusList": [1, 2], "filter": {"type": "a"}},
        {"header": "1", "orderStatusList": [1, 2], "filter": {"type": "a"}},
    ]
    result = _compute_constant_params(snapshots)
    assert result["header"] == "1"
    assert result["orderStatusList"] == [1, 2]
    assert result["filter"] == {"type": "a"}


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("list 值不同时不算常量")
def test_compute_constant_params_unhashable_different():
    snapshots = [
        {"orderStatusList": [1, 2]},
        {"orderStatusList": [3, 4]},
        {"orderStatusList": [1, 2]},
    ]
    result = _compute_constant_params(snapshots)
    assert "orderStatusList" not in result


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("空值（空字符串、None）不被收录为常量参数")
def test_compute_constant_params_excludes_empty_values():
    snapshots = [
        {"header": "1", "serialNo": "", "evaluates": "", "discountLevelList": ""},
        {"header": "1", "serialNo": "", "evaluates": "", "discountLevelList": ""},
        {"header": "1", "serialNo": "", "evaluates": "", "discountLevelList": ""},
    ]
    result = _compute_constant_params(snapshots)
    assert result == {"header": "1"}
    assert "serialNo" not in result
    assert "evaluates" not in result
    assert "discountLevelList" not in result


@allure.feature("HAR生成器")
@allure.story("常量参数计算")
@allure.title("50% 阈值边界：恰好半数不算常量，超过半数算常量")
def test_compute_constant_params_threshold_boundary():
    # header 在 2/4 = 50% 请求中出现：不超过阈值 → 不算常量
    snapshots_4 = [
        {"header": "1", "x": "1"},
        {"header": "1", "x": "2"},
        {"y": "3"},
        {"z": "4"},
    ]
    result = _compute_constant_params(snapshots_4)
    assert "header" not in result  # 恰好 50%，不满足 > threshold

    # header 在 3/4 = 75% 请求中出现且值相同：超过阈值 → 算常量
    snapshots_4_majority = [
        {"header": "1"},
        {"header": "1"},
        {"header": "1"},
        {"other": "x"},
    ]
    result = _compute_constant_params(snapshots_4_majority)
    assert result["header"] == "1"  # 3/4 > 50%


# ==================== _compute_har_param_values 单元测试 ====================


@allure.feature("HAR生成器")
@allure.story("参数枚举值计算")
@allure.title("测试 _compute_har_param_values 单参数收录")
def test_compute_har_param_values_single_param():
    from har2pytest.har_generator import _compute_har_param_values

    snapshots = [{"keyword": "A"}, {"keyword": "B"}, {"keyword": "C"}]
    result = _compute_har_param_values(snapshots, {})
    assert result["keyword"] == ["A", "B", "C"]


@allure.feature("HAR生成器")
@allure.story("参数枚举值计算")
@allure.title("测试 _compute_har_param_values 组合参数收录为元组列表")
def test_compute_har_param_values_combo_param():
    from har2pytest.har_generator import _compute_har_param_values

    snapshots = [
        {"type": "A", "size": "1"},
        {"type": "B", "size": "2"},
    ]
    result = _compute_har_param_values(snapshots, {})
    # 组合参数键以逗号连接
    combo_key = next((k for k in result if "," in k), None)
    assert combo_key is not None
    assert all(isinstance(v, tuple) for v in result[combo_key])


@allure.feature("HAR生成器")
@allure.story("参数枚举值计算")
@allure.title("测试 _compute_har_param_values 单值参数仍被收录")
def test_compute_har_param_values_single_value_included():
    from har2pytest.har_generator import _compute_har_param_values

    snapshots = [{"type": "A"}, {"type": "A"}, {"type": "A"}]
    result = _compute_har_param_values(snapshots, {})
    # _compute_har_param_values 本身不过滤常量参数，单值仍收录
    assert result["type"] == ["A"]
