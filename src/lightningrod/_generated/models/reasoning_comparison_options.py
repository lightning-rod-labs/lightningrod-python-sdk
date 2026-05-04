from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReasoningComparisonOptions")


@_attrs_define
class ReasoningComparisonOptions:
    """
    Attributes:
        base_model_id (str):
        trained_model_id (str):
        comparison_model_id (str | Unset):  Default: 'openai/gpt-4.1'.
        n (int | Unset): Number of sample pairs to compare Default: 10.
        instructions (str | Unset):  Default: 'Compare the reasoning quality of the base model vs. the trained model.'.
    """

    base_model_id: str
    trained_model_id: str
    comparison_model_id: str | Unset = "openai/gpt-4.1"
    n: int | Unset = 10
    instructions: str | Unset = "Compare the reasoning quality of the base model vs. the trained model."
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_model_id = self.base_model_id

        trained_model_id = self.trained_model_id

        comparison_model_id = self.comparison_model_id

        n = self.n

        instructions = self.instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_model_id": base_model_id,
                "trained_model_id": trained_model_id,
            }
        )
        if comparison_model_id is not UNSET:
            field_dict["comparison_model_id"] = comparison_model_id
        if n is not UNSET:
            field_dict["n"] = n
        if instructions is not UNSET:
            field_dict["instructions"] = instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        base_model_id = d.pop("base_model_id")

        trained_model_id = d.pop("trained_model_id")

        comparison_model_id = d.pop("comparison_model_id", UNSET)

        n = d.pop("n", UNSET)

        instructions = d.pop("instructions", UNSET)

        reasoning_comparison_options = cls(
            base_model_id=base_model_id,
            trained_model_id=trained_model_id,
            comparison_model_id=comparison_model_id,
            n=n,
            instructions=instructions,
        )

        reasoning_comparison_options.additional_properties = d
        return reasoning_comparison_options

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
