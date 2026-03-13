from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sample_dataset_config import SampleDatasetConfig


T = TypeVar("T", bound="EvalConfig")


@_attrs_define
class EvalConfig:
    """
    Attributes:
        organization_id (str):
        model_id (str):
        dataset (SampleDatasetConfig):
        benchmark_model_id (None | str | Unset):
        temperature (float | Unset):  Default: 0.0.
        max_tokens (int | Unset):  Default: 8192.
        max_concurrent (int | Unset):  Default: 50.
    """

    organization_id: str
    model_id: str
    dataset: SampleDatasetConfig
    benchmark_model_id: None | str | Unset = UNSET
    temperature: float | Unset = 0.0
    max_tokens: int | Unset = 8192
    max_concurrent: int | Unset = 50
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organization_id = self.organization_id

        model_id = self.model_id

        dataset = self.dataset.to_dict()

        benchmark_model_id: None | str | Unset
        if isinstance(self.benchmark_model_id, Unset):
            benchmark_model_id = UNSET
        else:
            benchmark_model_id = self.benchmark_model_id

        temperature = self.temperature

        max_tokens = self.max_tokens

        max_concurrent = self.max_concurrent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_id": organization_id,
                "model_id": model_id,
                "dataset": dataset,
            }
        )
        if benchmark_model_id is not UNSET:
            field_dict["benchmark_model_id"] = benchmark_model_id
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if max_concurrent is not UNSET:
            field_dict["max_concurrent"] = max_concurrent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sample_dataset_config import SampleDatasetConfig

        d = dict(src_dict)
        organization_id = d.pop("organization_id")

        model_id = d.pop("model_id")

        dataset = SampleDatasetConfig.from_dict(d.pop("dataset"))

        def _parse_benchmark_model_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        benchmark_model_id = _parse_benchmark_model_id(d.pop("benchmark_model_id", UNSET))

        temperature = d.pop("temperature", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        max_concurrent = d.pop("max_concurrent", UNSET)

        eval_config = cls(
            organization_id=organization_id,
            model_id=model_id,
            dataset=dataset,
            benchmark_model_id=benchmark_model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            max_concurrent=max_concurrent,
        )

        eval_config.additional_properties = d
        return eval_config

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
