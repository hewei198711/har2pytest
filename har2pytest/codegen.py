"""Jinja2 代码生成基础设施。

把“生成什么代码”从 Python 字符串拼接/手工缩进中剥离，交给 ``templates/``
下的 Jinja2 模板表达。本模块负责模板加载、渲染与生成结果语法校验：

- :func:`render` 渲染单个模板（含子模板 include），返回完整文本；
- :func:`render_lines` 渲染为行列表（去掉末尾一个换行后按 ``\\n`` 切分），
  供既有的“行列表组装”代码使用，保证行为与旧实现兼容；
- :func:`validate_python` 在写盘前用 ``ast.parse`` 校验，语法错误在生成期
  暴露而不是等 pytest 收集时才炸。
"""

from __future__ import annotations

import ast
import os
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .logger import logger

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

_ENVIRONMENT = Environment(
    loader=FileSystemLoader(_TEMPLATE_DIR),
    autoescape=False,
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined,
)


def render(template_name: str, **context: Any) -> str:
    """渲染模板并返回完整文本。"""
    template = _ENVIRONMENT.get_template(template_name)
    return template.render(**context)


def render_lines(template_name: str, **context: Any) -> list[str]:
    """渲染模板并切成行列表（兼容旧的逐行拼接代码）。

    约定模板文件末尾的单个换行属于“行结束符”，会先去掉再切分；
    模板内部需要空行时请显式输出空行。
    """
    text = render(template_name, **context)
    if text.endswith("\n"):
        text = text[:-1]
    if not text:
        return []
    return text.split("\n")


def validate_python(source: str, label: str = "generated code") -> None:
    """用 ast.parse 校验生成内容；语法错误直接抛出，避免写入坏文件。"""
    try:
        ast.parse(source)
    except SyntaxError as e:
        line = e.lineno or 0
        snippet = "\n".join(source.splitlines()[max(0, line - 2) : line + 1])
        logger.error(f"{label} 语法错误(第 {line} 行): {e.msg}\n{snippet}")
        raise ValueError(f"{label} 生成内容不是合法 Python: {e.msg} (line {line})") from e
