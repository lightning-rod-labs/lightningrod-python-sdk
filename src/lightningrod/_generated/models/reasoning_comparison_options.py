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
        model_a_id (str):
        model_b_id (str):
        judge_model_id (str | Unset):  Default: 'anthropic/claude-sonnet-4.6'.
        n (int | Unset): Number of sample pairs to compare Default: 10.
        instructions (str | Unset):  Default: 'Compare the reasoning quality of the two models.'.
    """

    model_a_id: str
    model_b_id: str
    judge_model_id: str | Unset = "anthropic/claude-sonnet-4.6"
    n: int | Unset = 10
    instructions: str | Unset = "Compare the reasoning quality of the two models."
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_a_id = self.model_a_id

        model_b_id = self.model_b_id

        judge_model_id = self.judge_model_id

        n = self.n

        instructions = self.instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_a_id": model_a_id,
                "model_b_id": model_b_id,
            }
        )
        if judge_model_id is not UNSET:
            field_dict["judge_model_id"] = judge_model_id
        if n is not UNSET:
            field_dict["n"] = n
        if instructions is not UNSET:
            field_dict["instructions"] = instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_a_id = d.pop("model_a_id")

        model_b_id = d.pop("model_b_id")

        judge_model_id = d.pop("judge_model_id", UNSET)

        n = d.pop("n", UNSET)

        instructions = d.pop("instructions", UNSET)

        reasoning_comparison_options = cls(
            model_a_id=model_a_id,
            model_b_id=model_b_id,
            judge_model_id=judge_model_id,
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
