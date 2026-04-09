from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResponseMessage")


@_attrs_define
class ResponseMessage:
    """
    Attributes:
        role (str): The role of the message author
        content (str): The content of the message
        thinking (None | str | Unset): The model's reasoning/thinking content, if available
    """

    role: str
    content: str
    thinking: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        content = self.content

        thinking: None | str | Unset
        if isinstance(self.thinking, Unset):
            thinking = UNSET
        else:
            thinking = self.thinking

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "content": content,
            }
        )
        if thinking is not UNSET:
            field_dict["thinking"] = thinking

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = d.pop("role")

        content = d.pop("content")

        def _parse_thinking(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        thinking = _parse_thinking(d.pop("thinking", UNSET))

        response_message = cls(
            role=role,
            content=content,
            thinking=thinking,
        )

        response_message.additional_properties = d
        return response_message

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
