from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LLMModelUsageSummary")


@_attrs_define
class LLMModelUsageSummary:
    """Usage for a single LLM model.

    Attributes:
        count (int | Unset):  Default: 0.
        input_tokens (int | Unset):  Default: 0.
        output_tokens (int | Unset):  Default: 0.
        cost (float | Unset):  Default: 0.0.
        cached_count (int | Unset):  Default: 0.
    """

    count: int | Unset = 0
    input_tokens: int | Unset = 0
    output_tokens: int | Unset = 0
    cost: float | Unset = 0.0
    cached_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        cost = self.cost

        cached_count = self.cached_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if cost is not UNSET:
            field_dict["cost"] = cost
        if cached_count is not UNSET:
            field_dict["cached_count"] = cached_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count", UNSET)

        input_tokens = d.pop("input_tokens", UNSET)

        output_tokens = d.pop("output_tokens", UNSET)

        cost = d.pop("cost", UNSET)

        cached_count = d.pop("cached_count", UNSET)

        llm_model_usage_summary = cls(
            count=count,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            cached_count=cached_count,
        )

        llm_model_usage_summary.additional_properties = d
        return llm_model_usage_summary

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
