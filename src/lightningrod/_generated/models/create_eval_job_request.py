from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_model import EvalModel
    from ..models.sample_dataset_config import SampleDatasetConfig


T = TypeVar("T", bound="CreateEvalJobRequest")


@_attrs_define
class CreateEvalJobRequest:
    """
    Attributes:
        dataset (SampleDatasetConfig):
        models (list[EvalModel]):
        temperature (float | Unset):  Default: 0.0.
    """

    dataset: SampleDatasetConfig
    models: list[EvalModel]
    temperature: float | Unset = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset = self.dataset.to_dict()

        models = []
        for models_item_data in self.models:
            models_item = models_item_data.to_dict()
            models.append(models_item)

        temperature = self.temperature

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset": dataset,
                "models": models,
            }
        )
        if temperature is not UNSET:
            field_dict["temperature"] = temperature

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_model import EvalModel
        from ..models.sample_dataset_config import SampleDatasetConfig

        d = dict(src_dict)
        dataset = SampleDatasetConfig.from_dict(d.pop("dataset"))

        models = []
        _models = d.pop("models")
        for models_item_data in _models:
            models_item = EvalModel.from_dict(models_item_data)

            models.append(models_item)

        temperature = d.pop("temperature", UNSET)

        create_eval_job_request = cls(
            dataset=dataset,
            models=models,
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
