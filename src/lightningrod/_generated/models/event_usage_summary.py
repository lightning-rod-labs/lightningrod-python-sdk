from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EventUsageSummary")


@_attrs_define
class EventUsageSummary:
    """Usage for a single event type.

    Attributes:
        count (int | Unset):  Default: 0.
        cost (float | Unset):  Default: 0.0.
        cached_count (int | Unset):  Default: 0.
    """

    count: int | Unset = 0
    cost: float | Unset = 0.0
    cached_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        cost = self.cost

        cached_count = self.cached_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if cost is not UNSET:
            field_dict["cost"] = cost
        if cached_count is not UNSET:
            field_dict["cached_count"] = cached_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count", UNSET)

        cost = d.pop("cost", UNSET)

        cached_count = d.pop("cached_count", UNSET)

        event_usage_summary = cls(
            count=count,
            cost=cost,
            cached_count=cached_count,
        )

        event_usage_summary.additional_properties = d
        return event_usage_summary

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
