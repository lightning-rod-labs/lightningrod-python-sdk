from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EstimateTrainingCostRequest")


@_attrs_define
class EstimateTrainingCostRequest:
    """
    Attributes:
        input_dataset_id (None | str | Unset):
        dataset_path (None | str | Unset):
        base_model (None | str | Unset):
        training_steps (int | None | Unset):
        batch_size (int | None | Unset):
        lora_rank (int | None | Unset):
    """

    input_dataset_id: None | str | Unset = UNSET
    dataset_path: None | str | Unset = UNSET
    base_model: None | str | Unset = UNSET
    training_steps: int | None | Unset = UNSET
    batch_size: int | None | Unset = UNSET
    lora_rank: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_dataset_id: None | str | Unset
        if isinstance(self.input_dataset_id, Unset):
            input_dataset_id = UNSET
        else:
            input_dataset_id = self.input_dataset_id

        dataset_path: None | str | Unset
        if isinstance(self.dataset_path, Unset):
            dataset_path = UNSET
        else:
            dataset_path = self.dataset_path

        base_model: None | str | Unset
        if isinstance(self.base_model, Unset):
            base_model = UNSET
        else:
            base_model = self.base_model

        training_steps: int | None | Unset
        if isinstance(self.training_steps, Unset):
            training_steps = UNSET
        else:
            training_steps = self.training_steps

        batch_size: int | None | Unset
        if isinstance(self.batch_size, Unset):
            batch_size = UNSET
        else:
            batch_size = self.batch_size

        lora_rank: int | None | Unset
        if isinstance(self.lora_rank, Unset):
            lora_rank = UNSET
        else:
            lora_rank = self.lora_rank

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_dataset_id is not UNSET:
            field_dict["input_dataset_id"] = input_dataset_id
        if dataset_path is not UNSET:
            field_dict["dataset_path"] = dataset_path
        if base_model is not UNSET:
            field_dict["base_model"] = base_model
        if training_steps is not UNSET:
            field_dict["training_steps"] = training_steps
        if batch_size is not UNSET:
            field_dict["batch_size"] = batch_size
        if lora_rank is not UNSET:
            field_dict["lora_rank"] = lora_rank

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_input_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_dataset_id = _parse_input_dataset_id(d.pop("input_dataset_id", UNSET))

        def _parse_dataset_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_path = _parse_dataset_path(d.pop("dataset_path", UNSET))

        def _parse_base_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base_model = _parse_base_model(d.pop("base_model", UNSET))

        def _parse_training_steps(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        training_steps = _parse_training_steps(d.pop("training_steps", UNSET))

        def _parse_batch_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        batch_size = _parse_batch_size(d.pop("batch_size", UNSET))

        def _parse_lora_rank(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        lora_rank = _parse_lora_rank(d.pop("lora_rank", UNSET))

        estimate_training_cost_request = cls(
            input_dataset_id=input_dataset_id,
            dataset_path=dataset_path,
            base_model=base_model,
            training_steps=training_steps,
            batch_size=batch_size,
            lora_rank=lora_rank,
        )

        estimate_training_cost_request.additional_properties = d
        return estimate_training_cost_request

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
