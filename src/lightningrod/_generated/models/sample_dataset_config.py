from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SampleDatasetConfig")


@_attrs_define
class SampleDatasetConfig:
    """
    Attributes:
        id (str):
        sample_ids (list[str]):
        prompt_template (None | str | Unset):
        multiple_choice_options (None | str | Unset):
    """

    id: str
    sample_ids: list[str]
    prompt_template: None | str | Unset = UNSET
    multiple_choice_options: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sample_ids = self.sample_ids

        prompt_template: None | str | Unset
        if isinstance(self.prompt_template, Unset):
            prompt_template = UNSET
        else:
            prompt_template = self.prompt_template

        multiple_choice_options: None | str | Unset
        if isinstance(self.multiple_choice_options, Unset):
            multiple_choice_options = UNSET
        else:
            multiple_choice_options = self.multiple_choice_options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "sample_ids": sample_ids,
            }
        )
        if prompt_template is not UNSET:
            field_dict["prompt_template"] = prompt_template
        if multiple_choice_options is not UNSET:
            field_dict["multiple_choice_options"] = multiple_choice_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        sample_ids = cast(list[str], d.pop("sample_ids"))

        def _parse_prompt_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_template = _parse_prompt_template(d.pop("prompt_template", UNSET))

        def _parse_multiple_choice_options(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        multiple_choice_options = _parse_multiple_choice_options(d.pop("multiple_choice_options", UNSET))

        sample_dataset_config = cls(
            id=id,
            sample_ids=sample_ids,
            prompt_template=prompt_template,
            multiple_choice_options=multiple_choice_options,
        )

        sample_dataset_config.additional_properties = d
        return sample_dataset_config

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
