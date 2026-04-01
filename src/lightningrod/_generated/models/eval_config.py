from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.eval_model import EvalModel
    from ..models.sample_dataset_config import SampleDatasetConfig


T = TypeVar("T", bound="EvalConfig")


@_attrs_define
class EvalConfig:
    """
    Attributes:
        organization_id (str):
        models (list[EvalModel]):
        dataset (SampleDatasetConfig):
        temperature (float | Unset):  Default: 0.0.
        max_tokens (int | Unset):  Default: 8192.
        max_concurrent (int | Unset):  Default: 50.
        modal_use_ephemeral_app (bool | Unset):  Default: False.
    """

    organization_id: str
    models: list[EvalModel]
    dataset: SampleDatasetConfig
    temperature: float | Unset = 0.0
    max_tokens: int | Unset = 8192
    max_concurrent: int | Unset = 50
    modal_use_ephemeral_app: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organization_id = self.organization_id

        models = []
        for models_item_data in self.models:
            models_item = models_item_data.to_dict()
            models.append(models_item)

        dataset = self.dataset.to_dict()

        temperature = self.temperature

        max_tokens = self.max_tokens

        max_concurrent = self.max_concurrent

        modal_use_ephemeral_app = self.modal_use_ephemeral_app

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_id": organization_id,
                "models": models,
                "dataset": dataset,
            }
        )
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if max_concurrent is not UNSET:
            field_dict["max_concurrent"] = max_concurrent
        if modal_use_ephemeral_app is not UNSET:
            field_dict["modal_use_ephemeral_app"] = modal_use_ephemeral_app

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_model import EvalModel
        from ..models.sample_dataset_config import SampleDatasetConfig

        d = dict(src_dict)
        organization_id = d.pop("organization_id")

        models = []
        _models = d.pop("models")
        for models_item_data in _models:
            models_item = EvalModel.from_dict(models_item_data)

            models.append(models_item)

        dataset = SampleDatasetConfig.from_dict(d.pop("dataset"))

        temperature = d.pop("temperature", UNSET)

        max_tokens = d.pop("max_tokens", UNSET)

        max_concurrent = d.pop("max_concurrent", UNSET)

        modal_use_ephemeral_app = d.pop("modal_use_ephemeral_app", UNSET)

        eval_config = cls(
            organization_id=organization_id,
            models=models,
            dataset=dataset,
            temperature=temperature,
            max_tokens=max_tokens,
            max_concurrent=max_concurrent,
            modal_use_ephemeral_app=modal_use_ephemeral_app,
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
