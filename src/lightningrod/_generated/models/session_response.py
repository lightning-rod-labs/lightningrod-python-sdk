from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.session_response_autonomy_level import SessionResponseAutonomyLevel
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message import Message
    from ..models.session_response_current_config_type_0 import SessionResponseCurrentConfigType0


T = TypeVar("T", bound="SessionResponse")


@_attrs_define
class SessionResponse:
    """Response containing session state.

    Attributes:
        session_id (str): Unique session identifier
        goal (str): The user's stated goal
        autonomy_level (SessionResponseAutonomyLevel): Current autonomy level
        created_at (datetime.datetime): When the session was created
        current_config (None | SessionResponseCurrentConfigType0 | Unset): The current pipeline configuration (if
            generated)
        messages (list[Message] | Unset): Conversation history
        dataset_ids (list[str] | Unset): Dataset IDs generated during this session
    """

    session_id: str
    goal: str
    autonomy_level: SessionResponseAutonomyLevel
    created_at: datetime.datetime
    current_config: None | SessionResponseCurrentConfigType0 | Unset = UNSET
    messages: list[Message] | Unset = UNSET
    dataset_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.session_response_current_config_type_0 import SessionResponseCurrentConfigType0

        session_id = self.session_id

        goal = self.goal

        autonomy_level = self.autonomy_level.value

        created_at = self.created_at.isoformat()

        current_config: dict[str, Any] | None | Unset
        if isinstance(self.current_config, Unset):
            current_config = UNSET
        elif isinstance(self.current_config, SessionResponseCurrentConfigType0):
            current_config = self.current_config.to_dict()
        else:
            current_config = self.current_config

        messages: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.messages, Unset):
            messages = []
            for messages_item_data in self.messages:
                messages_item = messages_item_data.to_dict()
                messages.append(messages_item)

        dataset_ids: list[str] | Unset = UNSET
        if not isinstance(self.dataset_ids, Unset):
            dataset_ids = self.dataset_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "goal": goal,
                "autonomy_level": autonomy_level,
                "created_at": created_at,
            }
        )
        if current_config is not UNSET:
            field_dict["current_config"] = current_config
        if messages is not UNSET:
            field_dict["messages"] = messages
        if dataset_ids is not UNSET:
            field_dict["dataset_ids"] = dataset_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message import Message
        from ..models.session_response_current_config_type_0 import SessionResponseCurrentConfigType0

        d = dict(src_dict)
        session_id = d.pop("session_id")

        goal = d.pop("goal")

        autonomy_level = SessionResponseAutonomyLevel(d.pop("autonomy_level"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_current_config(data: object) -> None | SessionResponseCurrentConfigType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_config_type_0 = SessionResponseCurrentConfigType0.from_dict(data)

                return current_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SessionResponseCurrentConfigType0 | Unset, data)

        current_config = _parse_current_config(d.pop("current_config", UNSET))

        _messages = d.pop("messages", UNSET)
        messages: list[Message] | Unset = UNSET
        if _messages is not UNSET:
            messages = []
            for messages_item_data in _messages:
                messages_item = Message.from_dict(messages_item_data)

                messages.append(messages_item)

        dataset_ids = cast(list[str], d.pop("dataset_ids", UNSET))

        session_response = cls(
            session_id=session_id,
            goal=goal,
            autonomy_level=autonomy_level,
            created_at=created_at,
            current_config=current_config,
            messages=messages,
            dataset_ids=dataset_ids,
        )

        session_response.additional_properties = d
        return session_response

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
