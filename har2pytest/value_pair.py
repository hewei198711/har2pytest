"""数值范围对参数处理上下文。

提供 ValuePairContext 冻结数据类，管理非时间的 Start/End 配对参数
（如 monthExchangeAmtStart/End 金额区间、yearReturnCountStart/End 次数区间）
的查找表，供 list_query / batch 模式测试用例生成使用。

与 TimePairContext 的分工：时间对基线由 datetime 表达式动态计算，
数值对基线由 test_0 收集响应记录对应字段的 min/max 动态提供
（collect_list_query_data 的 value_pairs 聚合通道）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ValuePairContext:
    """数值范围对处理的统一上下文。

    Attributes:
        active_pairs: 实际存在于 API 参数中的数值对元数据
            （base_name -> {"start": str, "end": str}）
        start_to_end: start 参数名 -> end 参数名 映射
        start_to_base: start 参数名 -> 词干 映射（断言按词干匹配响应字段）
        end_names: end 参数名集合（用于跳过已由 start 组合方法覆盖的参数）
        all_names: 所有涉及的数值参数名集合（start ∪ end）
    """

    active_pairs: dict[str, dict[str, str]] = field(default_factory=dict)
    start_to_end: dict[str, str] = field(default_factory=dict)
    start_to_base: dict[str, str] = field(default_factory=dict)
    end_names: set[str] = field(default_factory=set)
    all_names: set[str] = field(default_factory=set)

    @property
    def has_value_pairs(self) -> bool:
        """是否存在活跃数值对。"""
        return bool(self.active_pairs)

    @classmethod
    def build(
        cls,
        value_pairs: dict[str, dict[str, str]] | None,
        api_params: dict[str, Any],
    ) -> ValuePairContext:
        """从 api.json 的 value_pairs 元数据构建统一上下文。

        仅保留 start/end 参数都实际存在于 api_params 中的数值对
        （"活跃"数值对）；消费侧只读落盘元数据，不做配对推断。

        Args:
            value_pairs: api.json 中的数值对元数据（可为 None）
            api_params: API 文件中的所有参数

        Returns:
            ValuePairContext：统一上下文；无活跃数值对时返回空上下文。
        """
        active_pairs: dict[str, dict[str, str]] = {}
        start_to_end: dict[str, str] = {}
        start_to_base: dict[str, str] = {}
        end_names: set[str] = set()
        all_names: set[str] = set()

        for base, info in (value_pairs or {}).items():
            start, end = info["start"], info["end"]
            # 仅保留 start/end 都实际存在于参数中的数值对
            if start not in api_params or end not in api_params:
                continue
            active_pairs[base] = info
            start_to_end[start] = end
            start_to_base[start] = base
            end_names.add(end)
            all_names.add(start)
            all_names.add(end)

        return cls(
            active_pairs=active_pairs,
            start_to_end=start_to_end,
            start_to_base=start_to_base,
            end_names=end_names,
            all_names=all_names,
        )