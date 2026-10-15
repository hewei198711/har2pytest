"""时间对参数处理上下文。

提供 TimePairContext 冻结数据类，统一管理时间对参数（start/end 配对）
的查找表和角色映射，供 list_query / batch 模式测试用例生成使用。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TimePairContext:
    """时间对处理的统一上下文。

    Attributes:
        active_pairs: 实际存在于 API 参数中的时间对元数据
            （base_name -> {"start": str, "end": str, "format": str}）
        start_to_end: start 参数名 -> end 参数名 映射
        end_names: end 参数名集合（用于跳过已由 start 组合方法覆盖的参数）
        param_role: 参数名 -> (role, format)，role 为 "start" 或 "end"
        all_names: 所有涉及的时间参数名集合（start ∪ end）
    """

    active_pairs: dict[str, dict[str, str]] = field(default_factory=dict)
    start_to_end: dict[str, str] = field(default_factory=dict)
    end_names: set[str] = field(default_factory=set)
    param_role: dict[str, tuple[str, str]] = field(default_factory=dict)
    all_names: set[str] = field(default_factory=set)

    @property
    def has_time_pairs(self) -> bool:
        """是否存在活跃时间对。"""
        return bool(self.active_pairs)

    @classmethod
    def build(
        cls,
        time_pairs: dict[str, dict[str, str]] | None,
        api_params: dict[str, Any],
    ) -> TimePairContext:
        """从 api.json 的 time_pairs 元数据构建统一上下文。

        一次性遍历构建所有查找表，避免下游方法重复迭代。仅保留 start/end
        参数都实际存在于 api_params 中的时间对（"活跃"时间对）。

        Args:
            time_pairs: api.json 中的时间对元数据（可为 None）
            api_params: API 文件中的所有参数

        Returns:
            TimePairContext：统一上下文；无活跃时间对时返回空上下文。
        """
        if not time_pairs:
            return cls()

        active_pairs: dict[str, dict[str, str]] = {}
        start_to_end: dict[str, str] = {}
        end_names: set[str] = set()
        param_role: dict[str, tuple[str, str]] = {}
        all_names: set[str] = set()

        for base, info in time_pairs.items():
            start, end, fmt = info["start"], info["end"], info["format"]
            # 仅保留 start/end 都实际存在于参数中的时间对
            if start not in api_params or end not in api_params:
                continue
            active_pairs[base] = info
            start_to_end[start] = end
            end_names.add(end)
            param_role[start] = ("start", fmt)
            param_role[end] = ("end", fmt)
            all_names.add(start)
            all_names.add(end)

        return cls(
            active_pairs=active_pairs,
            start_to_end=start_to_end,
            end_names=end_names,
            param_role=param_role,
            all_names=all_names,
        )
