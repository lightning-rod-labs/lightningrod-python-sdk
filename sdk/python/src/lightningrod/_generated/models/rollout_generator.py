from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_config import ModelConfig


T = TypeVar("T", bound="RolloutGenerator")


@_attrs_define
class RolloutGenerator:
    """
    Attributes:
        models (list[ModelConfig]): Model names or ModelConfig objects
        config_type (Literal['ROLLOUT_GENERATOR'] | Unset):  Default: 'ROLLOUT_GENERATOR'.
        prompt_template (None | str | Unset): Prompt template with {column} placeholders. If None, uses sample.prompt
        input_columns (list[str] | Unset): Columns to substitute into template (from meta)
        output_schema (Any | None | Unset): Pydantic model for structured output
    """

    models: list[ModelConfig]
    config_type: Literal["ROLLOUT_GENERATOR"] | Unset = "ROLLOUT_GENERATOR"
    prompt_template: None | str | Unset = UNSET
    input_columns: list[str] | Unset = UNSET
    output_schema: Any | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        models = []
        for models_item_data in self.models:
            models_item = models_item_data.to_dict()
            models.append(models_item)

        config_type = self.config_type

        prompt_template: None | str | Unset
        if isinstance(self.prompt_template, Unset):
            prompt_template = UNSET
        else:
            prompt_template = self.prompt_template

        input_columns: list[str] | Unset = UNSET
        if not isinstance(self.input_columns, Unset):
            input_columns = self.input_columns

        output_schema: Any | None | Unset
        if isinstance(self.output_schema, Unset):
            output_schema = UNSET
        else:
            output_schema = self.output_schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "models": models,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if prompt_template is not UNSET:
            field_dict["prompt_template"] = prompt_template
        if input_columns is not UNSET:
            field_dict["input_columns"] = input_columns
        if output_schema is not UNSET:
            field_dict["output_schema"] = output_schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_config import ModelConfig

        d = dict(src_dict)
        models = []
        _models = d.pop("models")
        for models_item_data in _models:
            models_item = ModelConfig.from_dict(models_item_data)

            models.append(models_item)

        config_type = cast(Literal["ROLLOUT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "ROLLOUT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'ROLLOUT_GENERATOR', got '{config_type}'")

        def _parse_prompt_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_template = _parse_prompt_template(d.pop("prompt_template", UNSET))

        input_columns = cast(list[str], d.pop("input_columns", UNSET))

        def _parse_output_schema(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        output_schema = _parse_output_schema(d.pop("output_schema", UNSET))

        rollout_generator = cls(
            models=models,
            config_type=config_type,
            prompt_template=prompt_template,
            input_columns=input_columns,
            output_schema=output_schema,
        )

        rollout_generator.additional_properties = d
        return rollout_generator

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
