from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_summary_events import UsageSummaryEvents
    from ..models.usage_summary_llm_by_model import UsageSummaryLlmByModel


T = TypeVar("T", bound="UsageSummary")


@_attrs_define
class UsageSummary:
    """Flexible usage statistics by event type and LLM model.

    Attributes:
        events (UsageSummaryEvents | Unset):
        llm_by_model (UsageSummaryLlmByModel | Unset):
        total_cost (float | Unset):  Default: 0.0.
    """

    events: UsageSummaryEvents | Unset = UNSET
    llm_by_model: UsageSummaryLlmByModel | Unset = UNSET
    total_cost: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events: dict[str, Any] | Unset = UNSET
        if not isinstance(self.events, Unset):
            events = self.events.to_dict()

        llm_by_model: dict[str, Any] | Unset = UNSET
        if not isinstance(self.llm_by_model, Unset):
            llm_by_model = self.llm_by_model.to_dict()

        total_cost = self.total_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if events is not UNSET:
            field_dict["events"] = events
        if llm_by_model is not UNSET:
            field_dict["llm_by_model"] = llm_by_model
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_summary_events import UsageSummaryEvents
        from ..models.usage_summary_llm_by_model import UsageSummaryLlmByModel

        d = dict(src_dict)
        _events = d.pop("events", UNSET)
        events: UsageSummaryEvents | Unset
        if isinstance(_events, Unset):
            events = UNSET
        else:
            events = UsageSummaryEvents.from_dict(_events)

        _llm_by_model = d.pop("llm_by_model", UNSET)
        llm_by_model: UsageSummaryLlmByModel | Unset
        if isinstance(_llm_by_model, Unset):
            llm_by_model = UNSET
        else:
            llm_by_model = UsageSummaryLlmByModel.from_dict(_llm_by_model)

        total_cost = d.pop("total_cost", UNSET)

        usage_summary = cls(
            events=events,
            llm_by_model=llm_by_model,
            total_cost=total_cost,
        )

        usage_summary.additional_properties = d
        return usage_summary

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
