from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateEvalJobRequest")


@_attrs_define
class CreateEvalJobRequest:
    """
    Attributes:
        model_id (str):
        test_dataset_id (str):
        benchmark_model_id (None | str | Unset):
        temperature (float | Unset):  Default: 0.0.
    """

    model_id: str
    test_dataset_id: str
    benchmark_model_id: None | str | Unset = UNSET
    temperature: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

        test_dataset_id = self.test_dataset_id

        benchmark_model_id: None | str | Unset
        if isinstance(self.benchmark_model_id, Unset):
            benchmark_model_id = UNSET
        else:
            benchmark_model_id = self.benchmark_model_id

        temperature = self.temperature

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_id": model_id,
                "test_dataset_id": test_dataset_id,
            }
        )
        if benchmark_model_id is not UNSET:
            field_dict["benchmark_model_id"] = benchmark_model_id
        if temperature is not UNSET:
            field_dict["temperature"] = temperature

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_id = d.pop("model_id")

        test_dataset_id = d.pop("test_dataset_id")

        def _parse_benchmark_model_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        benchmark_model_id = _parse_benchmark_model_id(d.pop("benchmark_model_id", UNSET))

        temperature = d.pop("temperature", UNSET)

        create_eval_job_request = cls(
            model_id=model_id,
            test_dataset_id=test_dataset_id,
            benchmark_model_id=benchmark_model_id,
            temperature=temperature,
        )

        create_eval_job_request.additional_properties = d
        return create_eval_job_request

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
