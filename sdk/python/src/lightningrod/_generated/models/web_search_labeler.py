from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebSearchLabeler")


@_attrs_define
class WebSearchLabeler:
    """
    Attributes:
        config_type (Literal['WEB_SEARCH_LABELER'] | Unset): Type of transform configuration Default:
            'WEB_SEARCH_LABELER'.
    """

    config_type: Literal["WEB_SEARCH_LABELER"] | Unset = "WEB_SEARCH_LABELER"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_type = self.config_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config_type is not UNSET:
            field_dict["config_type"] = config_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        config_type = cast(Literal["WEB_SEARCH_LABELER"] | Unset, d.pop("config_type", UNSET))
        if config_type != "WEB_SEARCH_LABELER" and not isinstance(config_type, Unset):
            raise ValueError(f"config_type must match const 'WEB_SEARCH_LABELER', got '{config_type}'")

        web_search_labeler = cls(
            config_type=config_type,
        )

        web_search_labeler.additional_properties = d
        return web_search_labeler

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
