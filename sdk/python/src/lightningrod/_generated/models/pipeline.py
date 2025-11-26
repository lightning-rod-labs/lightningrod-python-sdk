from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transform_config import TransformConfig


T = TypeVar("T", bound="Pipeline")


@_attrs_define
class Pipeline:
    """
    Attributes:
        transform_configs (list[TransformConfig]): List of transform configs to execute in sequence
        config_type (Literal['PIPELINE'] | Unset): Type of transform configuration Default: 'PIPELINE'.
    """

    transform_configs: list[TransformConfig]
    config_type: Literal["PIPELINE"] | Unset = "PIPELINE"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transform_configs = []
        for transform_configs_item_data in self.transform_configs:
            transform_configs_item = transform_configs_item_data.to_dict()
            transform_configs.append(transform_configs_item)

        config_type = self.config_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transform_configs": transform_configs,
            }
        )
        if config_type is not UNSET:
            field_dict["config_type"] = config_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transform_config import TransformConfig

        d = dict(src_dict)
        transform_configs = []
        _transform_configs = d.pop("transform_configs")
        for transform_configs_item_data in _transform_configs:
            transform_configs_item = TransformConfig.from_dict(transform_configs_item_data)

            transform_configs.append(transform_configs_item)

        config_type = cast(Literal["PIPELINE"] | Unset, d.pop("config_type", UNSET))
        if config_type != "PIPELINE" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'PIPELINE', got '{config_type}'")

        pipeline = cls(
            transform_configs=transform_configs,
            config_type=config_type,
        )

        pipeline.additional_properties = d
        return pipeline

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
