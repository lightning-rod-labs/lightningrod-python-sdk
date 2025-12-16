from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="RolloutGenerator")


@_attrs_define
class RolloutGenerator:
    """Configuration for generating rollouts from multiple models.

    Attributes:
        models (list[str]): List of model names to generate rollouts from (e.g., ["openai/gpt-4", "anthropic/claude-3"])
        prompt_template (str): Prompt template with {column_name} placeholders for input columns
        input_columns (list[str]): Column names to use as inputs to the prompt template
        config_type (Literal['ROLLOUT_GENERATOR'] | Unset): Type of transform configuration Default: 'ROLLOUT_GENERATOR'.
        concurrency_limit (int | Unset): Max concurrent API calls per model Default: 50.
    """

    models: list[str]
    prompt_template: str
    input_columns: list[str]
    config_type: Literal["ROLLOUT_GENERATOR"] | Unset = "ROLLOUT_GENERATOR"
    concurrency_limit: int | Unset = 50
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        models = self.models
        prompt_template = self.prompt_template
        input_columns = self.input_columns
        config_type = self.config_type
        concurrency_limit = self.concurrency_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "models": models,
                "prompt_template": prompt_template,
                "input_columns": input_columns,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if concurrency_limit is not UNSET:
            field_dict["concurrency_limit"] = concurrency_limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        models = cast(list[str], d.pop("models"))
        prompt_template = d.pop("prompt_template")
        input_columns = cast(list[str], d.pop("input_columns"))

        config_type = cast(Literal["ROLLOUT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "ROLLOUT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'ROLLOUT_GENERATOR', got '{config_type}'")

        concurrency_limit = d.pop("concurrency_limit", UNSET)

        rollout_generator = cls(
            models=models,
            prompt_template=prompt_template,
            input_columns=input_columns,
            config_type=config_type,
            concurrency_limit=concurrency_limit,
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
