from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageSummary")


@_attrs_define
class UsageSummary:
    """Usage statistics for a step or total.

    Attributes:
        llm_call_count (int | Unset):  Default: 0.
        llm_input_tokens (int | Unset):  Default: 0.
        llm_output_tokens (int | Unset):  Default: 0.
        llm_total_cost (float | Unset):  Default: 0.0.
        web_search_count (int | Unset):  Default: 0.
        web_search_cost (float | Unset):  Default: 0.0.
        url_download_count (int | Unset):  Default: 0.
        url_download_cost (float | Unset):  Default: 0.0.
        gemini_grounding_count (int | Unset):  Default: 0.
        gemini_grounding_cost (float | Unset):  Default: 0.0.
        total_cost (float | Unset):  Default: 0.0.
    """

    llm_call_count: int | Unset = 0
    llm_input_tokens: int | Unset = 0
    llm_output_tokens: int | Unset = 0
    llm_total_cost: float | Unset = 0.0
    web_search_count: int | Unset = 0
    web_search_cost: float | Unset = 0.0
    url_download_count: int | Unset = 0
    url_download_cost: float | Unset = 0.0
    gemini_grounding_count: int | Unset = 0
    gemini_grounding_cost: float | Unset = 0.0
    total_cost: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        llm_call_count = self.llm_call_count

        llm_input_tokens = self.llm_input_tokens

        llm_output_tokens = self.llm_output_tokens

        llm_total_cost = self.llm_total_cost

        web_search_count = self.web_search_count

        web_search_cost = self.web_search_cost

        url_download_count = self.url_download_count

        url_download_cost = self.url_download_cost

        gemini_grounding_count = self.gemini_grounding_count

        gemini_grounding_cost = self.gemini_grounding_cost

        total_cost = self.total_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if llm_call_count is not UNSET:
            field_dict["llm_call_count"] = llm_call_count
        if llm_input_tokens is not UNSET:
            field_dict["llm_input_tokens"] = llm_input_tokens
        if llm_output_tokens is not UNSET:
            field_dict["llm_output_tokens"] = llm_output_tokens
        if llm_total_cost is not UNSET:
            field_dict["llm_total_cost"] = llm_total_cost
        if web_search_count is not UNSET:
            field_dict["web_search_count"] = web_search_count
        if web_search_cost is not UNSET:
            field_dict["web_search_cost"] = web_search_cost
        if url_download_count is not UNSET:
            field_dict["url_download_count"] = url_download_count
        if url_download_cost is not UNSET:
            field_dict["url_download_cost"] = url_download_cost
        if gemini_grounding_count is not UNSET:
            field_dict["gemini_grounding_count"] = gemini_grounding_count
        if gemini_grounding_cost is not UNSET:
            field_dict["gemini_grounding_cost"] = gemini_grounding_cost
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        llm_call_count = d.pop("llm_call_count", UNSET)

        llm_input_tokens = d.pop("llm_input_tokens", UNSET)

        llm_output_tokens = d.pop("llm_output_tokens", UNSET)

        llm_total_cost = d.pop("llm_total_cost", UNSET)

        web_search_count = d.pop("web_search_count", UNSET)

        web_search_cost = d.pop("web_search_cost", UNSET)

        url_download_count = d.pop("url_download_count", UNSET)

        url_download_cost = d.pop("url_download_cost", UNSET)

        gemini_grounding_count = d.pop("gemini_grounding_count", UNSET)

        gemini_grounding_cost = d.pop("gemini_grounding_cost", UNSET)

        total_cost = d.pop("total_cost", UNSET)

        usage_summary = cls(
            llm_call_count=llm_call_count,
            llm_input_tokens=llm_input_tokens,
            llm_output_tokens=llm_output_tokens,
            llm_total_cost=llm_total_cost,
            web_search_count=web_search_count,
            web_search_cost=web_search_cost,
            url_download_count=url_download_count,
            url_download_cost=url_download_cost,
            gemini_grounding_count=gemini_grounding_count,
            gemini_grounding_cost=gemini_grounding_cost,
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
