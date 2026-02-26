from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message import Message
    from ..models.message_response_current_config_type_0 import MessageResponseCurrentConfigType0


T = TypeVar("T", bound="MessageResponse")


@_attrs_define
class MessageResponse:
    """Response from sending a message.

    Attributes:
        message (Message): A message in the conversation.
        current_config (MessageResponseCurrentConfigType0 | None | Unset): Updated pipeline configuration (if changed)
    """

    message: Message
    current_config: MessageResponseCurrentConfigType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.message_response_current_config_type_0 import MessageResponseCurrentConfigType0

        message = self.message.to_dict()

        current_config: dict[str, Any] | None | Unset
        if isinstance(self.current_config, Unset):
            current_config = UNSET
        elif isinstance(self.current_config, MessageResponseCurrentConfigType0):
            current_config = self.current_config.to_dict()
        else:
            current_config = self.current_config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if current_config is not UNSET:
            field_dict["current_config"] = current_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message import Message
        from ..models.message_response_current_config_type_0 import MessageResponseCurrentConfigType0

        d = dict(src_dict)
        message = Message.from_dict(d.pop("message"))

        def _parse_current_config(data: object) -> MessageResponseCurrentConfigType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_config_type_0 = MessageResponseCurrentConfigType0.from_dict(data)

                return current_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MessageResponseCurrentConfigType0 | None | Unset, data)

        current_config = _parse_current_config(d.pop("current_config", UNSET))

        message_response = cls(
            message=message,
            current_config=current_config,
        )

        message_response.additional_properties = d
        return message_response

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
