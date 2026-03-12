from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EstimateTrainingCostResponse")


@_attrs_define
class EstimateTrainingCostResponse:
    """
    Attributes:
        total_cost_dollars (float):
        prefill_tokens (int):
        sample_tokens (int):
        train_tokens (int):
        effective_steps (int):
        notes (str):
        warning_message (None | str | Unset):
    """

    total_cost_dollars: float
    prefill_tokens: int
    sample_tokens: int
    train_tokens: int
    effective_steps: int
    notes: str
    warning_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_cost_dollars = self.total_cost_dollars

        prefill_tokens = self.prefill_tokens

        sample_tokens = self.sample_tokens

        train_tokens = self.train_tokens

        effective_steps = self.effective_steps

        notes = self.notes

        warning_message: None | str | Unset
        if isinstance(self.warning_message, Unset):
            warning_message = UNSET
        else:
            warning_message = self.warning_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_cost_dollars": total_cost_dollars,
                "prefill_tokens": prefill_tokens,
                "sample_tokens": sample_tokens,
                "train_tokens": train_tokens,
                "effective_steps": effective_steps,
                "notes": notes,
            }
        )
        if warning_message is not UNSET:
            field_dict["warning_message"] = warning_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_cost_dollars = d.pop("total_cost_dollars")

        prefill_tokens = d.pop("prefill_tokens")

        sample_tokens = d.pop("sample_tokens")

        train_tokens = d.pop("train_tokens")

        effective_steps = d.pop("effective_steps")

        notes = d.pop("notes")

        def _parse_warning_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        warning_message = _parse_warning_message(d.pop("warning_message", UNSET))

        estimate_training_cost_response = cls(
            total_cost_dollars=total_cost_dollars,
            prefill_tokens=prefill_tokens,
            sample_tokens=sample_tokens,
            train_tokens=train_tokens,
            effective_steps=effective_steps,
            notes=notes,
            warning_message=warning_message,
        )

        estimate_training_cost_response.additional_properties = d
        return estimate_training_cost_response

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
