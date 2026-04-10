from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.grpo_training_config import GRPOTrainingConfig
    from ..models.sft_training_config import SFTTrainingConfig


T = TypeVar("T", bound="EstimateTrainingCostRequest")


@_attrs_define
class EstimateTrainingCostRequest:
    """
    Attributes:
        config (GRPOTrainingConfig | SFTTrainingConfig):
    """

    config: GRPOTrainingConfig | SFTTrainingConfig
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.grpo_training_config import GRPOTrainingConfig

        config: dict[str, Any]
        if isinstance(self.config, GRPOTrainingConfig):
            config = self.config.to_dict()
        else:
            config = self.config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grpo_training_config import GRPOTrainingConfig
        from ..models.sft_training_config import SFTTrainingConfig

        d = dict(src_dict)

        def _parse_config(data: object) -> GRPOTrainingConfig | SFTTrainingConfig:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_type_0 = GRPOTrainingConfig.from_dict(data)

                return config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            config_type_1 = SFTTrainingConfig.from_dict(data)

            return config_type_1

        config = _parse_config(d.pop("config"))

        estimate_training_cost_request = cls(
            config=config,
        )

        estimate_training_cost_request.additional_properties = d
        return estimate_training_cost_request

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
