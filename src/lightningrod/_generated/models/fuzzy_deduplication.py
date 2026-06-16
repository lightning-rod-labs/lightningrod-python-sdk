from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fuzzy_match_config import FuzzyMatchConfig


T = TypeVar("T", bound="FuzzyDeduplication")


@_attrs_define
class FuzzyDeduplication:
    """
    Attributes:
        config_type (Literal['FUZZY_DEDUPLICATION'] | Unset): Type of transform configuration Default:
            'FUZZY_DEDUPLICATION'.
        keys (list[FuzzyMatchConfig] | Unset): Per-key match configuration. Each key can use exact or fuzzy matching
            independently.
    """

    config_type: Literal["FUZZY_DEDUPLICATION"] | Unset = "FUZZY_DEDUPLICATION"
    keys: list[FuzzyMatchConfig] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        keys: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.keys, Unset):
            keys = []
            for keys_item_data in self.keys:
                keys_item = keys_item_data.to_dict()
                keys.append(keys_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type
        if keys is not UNSET:
            field_dict["keys"] = keys

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fuzzy_match_config import FuzzyMatchConfig

        d = dict(src_dict)
        config_type = cast(Literal["FUZZY_DEDUPLICATION"] | Unset, d.pop("config_type", UNSET))
        if config_type != "FUZZY_DEDUPLICATION" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'FUZZY_DEDUPLICATION', got '{config_type}'")

        _keys = d.pop("keys", UNSET)
        keys: list[FuzzyMatchConfig] | Unset = UNSET
        if _keys is not UNSET:
            keys = []
            for keys_item_data in _keys:
                keys_item = FuzzyMatchConfig.from_dict(keys_item_data)

                keys.append(keys_item)

        fuzzy_deduplication = cls(
            config_type=config_type,
            keys=keys,
        )

        fuzzy_deduplication.additional_properties = d
        return fuzzy_deduplication

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
