from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sample_dataset_config import SampleDatasetConfig


T = TypeVar("T", bound="TrainingConfig")


@_attrs_define
class TrainingConfig:
    """
    Attributes:
        dataset (SampleDatasetConfig):
        base_model (str):
        training_steps (int):
        batch_size (int | None | Unset):
        lora_rank (int | None | Unset):
        learning_rate (float | None | Unset):
        adam_beta1 (float | None | Unset):
        adam_beta2 (float | None | Unset):
        save_every (int | None | Unset):
        resume_from (None | str | Unset):
        num_rollouts (int | None | Unset):
        max_response_length (int | None | Unset):
        start_idx (int | None | Unset):
    """

    dataset: SampleDatasetConfig
    base_model: str
    training_steps: int
    batch_size: int | None | Unset = UNSET
    lora_rank: int | None | Unset = UNSET
    learning_rate: float | None | Unset = UNSET
    adam_beta1: float | None | Unset = UNSET
    adam_beta2: float | None | Unset = UNSET
    save_every: int | None | Unset = UNSET
    resume_from: None | str | Unset = UNSET
    num_rollouts: int | None | Unset = UNSET
    max_response_length: int | None | Unset = UNSET
    start_idx: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset = self.dataset.to_dict()

        base_model = self.base_model

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

        learning_rate: float | None | Unset
        if isinstance(self.learning_rate, Unset):
            learning_rate = UNSET
        else:
            learning_rate = self.learning_rate

        adam_beta1: float | None | Unset
        if isinstance(self.adam_beta1, Unset):
            adam_beta1 = UNSET
        else:
            adam_beta1 = self.adam_beta1

        adam_beta2: float | None | Unset
        if isinstance(self.adam_beta2, Unset):
            adam_beta2 = UNSET
        else:
            adam_beta2 = self.adam_beta2

        save_every: int | None | Unset
        if isinstance(self.save_every, Unset):
            save_every = UNSET
        else:
            save_every = self.save_every

        resume_from: None | str | Unset
        if isinstance(self.resume_from, Unset):
            resume_from = UNSET
        else:
            resume_from = self.resume_from

        num_rollouts: int | None | Unset
        if isinstance(self.num_rollouts, Unset):
            num_rollouts = UNSET
        else:
            num_rollouts = self.num_rollouts

        max_response_length: int | None | Unset
        if isinstance(self.max_response_length, Unset):
            max_response_length = UNSET
        else:
            max_response_length = self.max_response_length

        start_idx: int | None | Unset
        if isinstance(self.start_idx, Unset):
            start_idx = UNSET
        else:
            start_idx = self.start_idx

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset": dataset,
                "base_model": base_model,
                "training_steps": training_steps,
            }
        )
        if batch_size is not UNSET:
            field_dict["batch_size"] = batch_size
        if lora_rank is not UNSET:
            field_dict["lora_rank"] = lora_rank
        if learning_rate is not UNSET:
            field_dict["learning_rate"] = learning_rate
        if adam_beta1 is not UNSET:
            field_dict["adam_beta1"] = adam_beta1
        if adam_beta2 is not UNSET:
            field_dict["adam_beta2"] = adam_beta2
        if save_every is not UNSET:
            field_dict["save_every"] = save_every
        if resume_from is not UNSET:
            field_dict["resume_from"] = resume_from
        if num_rollouts is not UNSET:
            field_dict["num_rollouts"] = num_rollouts
        if max_response_length is not UNSET:
            field_dict["max_response_length"] = max_response_length
        if start_idx is not UNSET:
            field_dict["start_idx"] = start_idx

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sample_dataset_config import SampleDatasetConfig

        d = dict(src_dict)
        dataset = SampleDatasetConfig.from_dict(d.pop("dataset"))

        base_model = d.pop("base_model")

        training_steps = d.pop("training_steps")

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

        def _parse_learning_rate(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        learning_rate = _parse_learning_rate(d.pop("learning_rate", UNSET))

        def _parse_adam_beta1(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        adam_beta1 = _parse_adam_beta1(d.pop("adam_beta1", UNSET))

        def _parse_adam_beta2(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        adam_beta2 = _parse_adam_beta2(d.pop("adam_beta2", UNSET))

        def _parse_save_every(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        save_every = _parse_save_every(d.pop("save_every", UNSET))

        def _parse_resume_from(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resume_from = _parse_resume_from(d.pop("resume_from", UNSET))

        def _parse_num_rollouts(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_rollouts = _parse_num_rollouts(d.pop("num_rollouts", UNSET))

        def _parse_max_response_length(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_response_length = _parse_max_response_length(d.pop("max_response_length", UNSET))

        def _parse_start_idx(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        start_idx = _parse_start_idx(d.pop("start_idx", UNSET))

        training_config = cls(
            dataset=dataset,
            base_model=base_model,
            training_steps=training_steps,
            batch_size=batch_size,
            lora_rank=lora_rank,
            learning_rate=learning_rate,
            adam_beta1=adam_beta1,
            adam_beta2=adam_beta2,
            save_every=save_every,
            resume_from=resume_from,
            num_rollouts=num_rollouts,
            max_response_length=max_response_length,
            start_idx=start_idx,
        )

        training_config.additional_properties = d
        return training_config

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
