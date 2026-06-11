from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transform_config import TransformConfig


T = TypeVar("T", bound="AggregateContextGenerator")


@_attrs_define
class AggregateContextGenerator:
    """
    Attributes:
        context_generator_configs (list[TransformConfig]): Context-generator transform configs to run in parallel and
            combine
        config_type (Literal['AGGREGATE_CONTEXT_GENERATOR'] | Unset): Type of transform configuration Default:
            'AGGREGATE_CONTEXT_GENERATOR'.
    """

    context_generator_configs: list[TransformConfig]
    config_type: Literal["AGGREGATE_CONTEXT_GENERATOR"] | Unset = "AGGREGATE_CONTEXT_GENERATOR"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context_generator_configs = []
        for context_generator_configs_item_data in self.context_generator_configs:
            context_generator_configs_item = context_generator_configs_item_data.to_dict()
            context_generator_configs.append(context_generator_configs_item)

        config_type = self.config_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context_generator_configs": context_generator_configs,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transform_config import TransformConfig

        d = dict(src_dict)
        context_generator_configs = []
        _context_generator_configs = d.pop("context_generator_configs")
        for context_generator_configs_item_data in _context_generator_configs:
            context_generator_configs_item = TransformConfig.from_dict(context_generator_configs_item_data)

            context_generator_configs.append(context_generator_configs_item)

        config_type = cast(Literal["AGGREGATE_CONTEXT_GENERATOR"] | Unset, d.pop("config_type", UNSET))
        if config_type != "AGGREGATE_CONTEXT_GENERATOR" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'AGGREGATE_CONTEXT_GENERATOR', got '{config_type}'")

        aggregate_context_generator = cls(
            context_generator_configs=context_generator_configs,
            config_type=config_type,
        )

        aggregate_context_generator.additional_properties = d
        return aggregate_context_generator

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
