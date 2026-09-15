"""测试 har2pytest.codegen 模块中 Jinja2 模板渲染与写盘前语法校验的功能与边界。"""

import allure
import pytest
from jinja2 import TemplateNotFound, UndefinedError

from har2pytest.codegen import render, render_lines, validate_python

# ==================== render 模板渲染测试 ====================


@allure.feature("代码生成")
@allure.story("模板渲染")
@allure.title("测试 render 渲染已有模板")
def test_render_existing_template():
    text = render("p_data_dict.j2", is_combination=False, param_name="keyword", param_safe="keyword", other_items=[])
    assert '"keyword": keyword,' in text


@allure.feature("代码生成")
@allure.story("模板渲染")
@allure.title("测试 render 渲染不存在的模板抛出 TemplateNotFound")
def test_render_nonexistent_template():
    with pytest.raises(TemplateNotFound):
        render("nonexistent_template.j2")


@allure.feature("代码生成")
@allure.story("模板渲染")
@allure.title("测试 render 缺少模板变量时抛出 UndefinedError")
def test_render_strict_undefined_raises():
    with pytest.raises(UndefinedError):
        render("p_data_dict.j2")


# ==================== render_lines 行列表渲染测试 ====================


@allure.feature("代码生成")
@allure.story("行列表渲染")
@allure.title("测试 render_lines 切分模板并去除末尾换行")
def test_render_lines_splits_and_strips_trailing_newline():
    lines = render_lines("p_data_dict.j2", is_combination=False, param_name="a", param_safe="a", other_items=[("b", "'x'")])
    assert lines == ['            "a": a,', '            "b": \'x\',']


@allure.feature("代码生成")
@allure.story("行列表渲染")
@allure.title("测试 render_lines 空模板返回空列表")
def test_render_lines_empty_template():
    from unittest.mock import patch

    with patch("har2pytest.codegen.render", return_value=""):
        assert render_lines("any.j2") == []

    with patch("har2pytest.codegen.render", return_value="\n"):
        assert render_lines("any.j2") == []


@allure.feature("代码生成")
@allure.story("行列表渲染")
@allure.title("测试 render_lines 渲染断言模板（搜索关闭）")
@allure.description("p_test_method_assertions 搜索分支关闭时，只渲染基础 with/断言块")
def test_render_lines_assertions_template():
    lines = render_lines(
        "p_test_method_assertions.j2",
        async_mode=False,
        function_name="list_page",
        param_var="params",
        search_enabled=False,
        search_param="",
        search_var="",
        verify_assert="",
    )
    assert lines[0] == "        with list_page(params=params, headers=self.headers) as r:"
    assert lines[-1] == "            assert data['code'] == 200"
    assert "验证返回数据符合搜索条件" not in "\n".join(lines)


# ==================== validate_python 语法校验测试 ====================


@allure.feature("代码生成")
@allure.story("语法校验")
@allure.title("测试 validate_python 校验合法 Python 不抛异常")
def test_validate_python_valid():
    validate_python("def f():\n    return 1\n")


@allure.feature("代码生成")
@allure.story("语法校验")
@allure.title("测试 validate_python 校验非法 Python 抛出 ValueError")
def test_validate_python_invalid_raises():
    with pytest.raises(ValueError):
        validate_python("def f(:\n", label="bad")


@allure.feature("代码生成")
@allure.story("语法校验")
@allure.title("测试 validate_python 自定义 label 出现在错误信息中")
def test_validate_python_label_in_error():
    with pytest.raises(ValueError, match="my_module"):
        validate_python("def f(:\n", label="my_module")


@allure.feature("代码生成")
@allure.story("语法校验")
@allure.title("测试 validate_python 异常链保留原始 SyntaxError")
def test_validate_python_exception_chain():
    with pytest.raises(ValueError) as exc_info:
        validate_python("def f(:\n")
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, SyntaxError)
