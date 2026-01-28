from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.transform_type import TransformType

if TYPE_CHECKING:
    from ..models.usage_summary import UsageSummary


T = TypeVar("T", bound="StepCostBreakdown")


@_attrs_define
class StepCostBreakdown:
    """
    Attributes:
        step_name (str):
        step_type (TransformType):
        total_cost_dollars (float):
        usage (UsageSummary): Flexible usage statistics by event type and LLM model.
        output_count (int):
        cost_per_output (float):
    """

    step_name: str
    step_type: TransformType
    total_cost_dollars: float
    usage: UsageSummary
    output_count: int
    cost_per_output: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step_name = self.step_name

        step_type = self.step_type.value

        total_cost_dollars = self.total_cost_dollars

        usage = self.usage.to_dict()

        output_count = self.output_count

        cost_per_output = self.cost_per_output

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step_name": step_name,
                "step_type": step_type,
                "total_cost_dollars": total_cost_dollars,
                "usage": usage,
                "output_count": output_count,
                "cost_per_output": cost_per_output,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_summary import UsageSummary

        d = dict(src_dict)
        step_name = d.pop("step_name")

        step_type = TransformType(d.pop("step_type"))

        total_cost_dollars = d.pop("total_cost_dollars")

        usage = UsageSummary.from_dict(d.pop("usage"))

        output_count = d.pop("output_count")

        cost_per_output = d.pop("cost_per_output")

        step_cost_breakdown = cls(
            step_name=step_name,
            step_type=step_type,
            total_cost_dollars=total_cost_dollars,
            usage=usage,
            output_count=output_count,
            cost_per_output=cost_per_output,
        )

        step_cost_breakdown.additional_properties = d
        return step_cost_breakdown

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
