from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.step_cost_breakdown import StepCostBreakdown
    from ..models.usage_summary import UsageSummary


T = TypeVar("T", bound="EstimateCostResponse")


@_attrs_define
class EstimateCostResponse:
    """
    Attributes:
        total_cost_dollars (float):
        llm_cost_dollars (float):
        web_search_cost_dollars (float):
        url_download_cost_dollars (float):
        usage (UsageSummary): Flexible usage statistics by event type and LLM model.
        steps (list[StepCostBreakdown]):
    """

    total_cost_dollars: float
    llm_cost_dollars: float
    web_search_cost_dollars: float
    url_download_cost_dollars: float
    usage: UsageSummary
    steps: list[StepCostBreakdown]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_cost_dollars = self.total_cost_dollars

        llm_cost_dollars = self.llm_cost_dollars

        web_search_cost_dollars = self.web_search_cost_dollars

        url_download_cost_dollars = self.url_download_cost_dollars

        usage = self.usage.to_dict()

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_cost_dollars": total_cost_dollars,
                "llm_cost_dollars": llm_cost_dollars,
                "web_search_cost_dollars": web_search_cost_dollars,
                "url_download_cost_dollars": url_download_cost_dollars,
                "usage": usage,
                "steps": steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.step_cost_breakdown import StepCostBreakdown
        from ..models.usage_summary import UsageSummary

        d = dict(src_dict)
        total_cost_dollars = d.pop("total_cost_dollars")

        llm_cost_dollars = d.pop("llm_cost_dollars")

        web_search_cost_dollars = d.pop("web_search_cost_dollars")

        url_download_cost_dollars = d.pop("url_download_cost_dollars")

        usage = UsageSummary.from_dict(d.pop("usage"))

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = StepCostBreakdown.from_dict(steps_item_data)

            steps.append(steps_item)

        estimate_cost_response = cls(
            total_cost_dollars=total_cost_dollars,
            llm_cost_dollars=llm_cost_dollars,
            web_search_cost_dollars=web_search_cost_dollars,
            url_download_cost_dollars=url_download_cost_dollars,
            usage=usage,
            steps=steps,
        )

        estimate_cost_response.additional_properties = d
        return estimate_cost_response

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
