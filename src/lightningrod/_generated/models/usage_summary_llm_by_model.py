from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.llm_model_usage_summary import LLMModelUsageSummary


T = TypeVar("T", bound="UsageSummaryLlmByModel")


@_attrs_define
class UsageSummaryLlmByModel:
    """ """

    additional_properties: dict[str, LLMModelUsageSummary] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.llm_model_usage_summary import LLMModelUsageSummary

        d = dict(src_dict)
        usage_summary_llm_by_model = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = LLMModelUsageSummary.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        usage_summary_llm_by_model.additional_properties = additional_properties
        return usage_summary_llm_by_model

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> LLMModelUsageSummary:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: LLMModelUsageSummary) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
