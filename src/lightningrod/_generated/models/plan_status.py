from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlanStatus")


@_attrs_define
class PlanStatus:
    """Status of the progressive plan.

    Attributes:
        finalized (bool | Unset): Whether the plan has been finalized Default: False.
        summary (None | str | Unset): Plan summary (set after finalization)
        estimated_samples (int | None | Unset):
        fulfillment_type (None | str | Unset): 'auto' or 'manual' (set after finalization)
    """

    finalized: bool | Unset = False
    summary: None | str | Unset = UNSET
    estimated_samples: int | None | Unset = UNSET
    fulfillment_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        finalized = self.finalized

        summary: None | str | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        estimated_samples: int | None | Unset
        if isinstance(self.estimated_samples, Unset):
            estimated_samples = UNSET
        else:
            estimated_samples = self.estimated_samples

        fulfillment_type: None | str | Unset
        if isinstance(self.fulfillment_type, Unset):
            fulfillment_type = UNSET
        else:
            fulfillment_type = self.fulfillment_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if finalized is not UNSET:
            field_dict["finalized"] = finalized
        if summary is not UNSET:
            field_dict["summary"] = summary
        if estimated_samples is not UNSET:
            field_dict["estimated_samples"] = estimated_samples
        if fulfillment_type is not UNSET:
            field_dict["fulfillment_type"] = fulfillment_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        finalized = d.pop("finalized", UNSET)

        def _parse_summary(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_estimated_samples(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        estimated_samples = _parse_estimated_samples(d.pop("estimated_samples", UNSET))

        def _parse_fulfillment_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fulfillment_type = _parse_fulfillment_type(d.pop("fulfillment_type", UNSET))

        plan_status = cls(
            finalized=finalized,
            summary=summary,
            estimated_samples=estimated_samples,
            fulfillment_type=fulfillment_type,
        )

        plan_status.additional_properties = d
        return plan_status

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
