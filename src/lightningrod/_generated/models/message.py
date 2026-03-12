from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.message_role import MessageRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.preview_results import PreviewResults
    from ..models.structured_question import StructuredQuestion


T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """A message in the conversation.

    Attributes:
        role (MessageRole): Who sent the message
        content (str): The message content
        timestamp (datetime.datetime): When the message was sent
        tool_call_id (None | str | Unset): ID of the tool call if this is a tool message
        structured_question (None | StructuredQuestion | Unset): If present, render as clickable options instead of
            plain text
        preview_results (None | PreviewResults | Unset): If present, render preview results in a special UI component
    """

    role: MessageRole
    content: str
    timestamp: datetime.datetime
    tool_call_id: None | str | Unset = UNSET
    structured_question: None | StructuredQuestion | Unset = UNSET
    preview_results: None | PreviewResults | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.preview_results import PreviewResults
        from ..models.structured_question import StructuredQuestion

        role = self.role.value

        content = self.content

        timestamp = self.timestamp.isoformat()

        tool_call_id: None | str | Unset
        if isinstance(self.tool_call_id, Unset):
            tool_call_id = UNSET
        else:
            tool_call_id = self.tool_call_id

        structured_question: dict[str, Any] | None | Unset
        if isinstance(self.structured_question, Unset):
            structured_question = UNSET
        elif isinstance(self.structured_question, StructuredQuestion):
            structured_question = self.structured_question.to_dict()
        else:
            structured_question = self.structured_question

        preview_results: dict[str, Any] | None | Unset
        if isinstance(self.preview_results, Unset):
            preview_results = UNSET
        elif isinstance(self.preview_results, PreviewResults):
            preview_results = self.preview_results.to_dict()
        else:
            preview_results = self.preview_results

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "content": content,
                "timestamp": timestamp,
            }
        )
        if tool_call_id is not UNSET:
            field_dict["tool_call_id"] = tool_call_id
        if structured_question is not UNSET:
            field_dict["structured_question"] = structured_question
        if preview_results is not UNSET:
            field_dict["preview_results"] = preview_results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.preview_results import PreviewResults
        from ..models.structured_question import StructuredQuestion

        d = dict(src_dict)
        role = MessageRole(d.pop("role"))

        content = d.pop("content")

        timestamp = isoparse(d.pop("timestamp"))

        def _parse_tool_call_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tool_call_id = _parse_tool_call_id(d.pop("tool_call_id", UNSET))

        def _parse_structured_question(data: object) -> None | StructuredQuestion | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                structured_question_type_0 = StructuredQuestion.from_dict(data)

                return structured_question_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StructuredQuestion | Unset, data)

        structured_question = _parse_structured_question(d.pop("structured_question", UNSET))

        def _parse_preview_results(data: object) -> None | PreviewResults | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                preview_results_type_0 = PreviewResults.from_dict(data)

                return preview_results_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PreviewResults | Unset, data)

        preview_results = _parse_preview_results(d.pop("preview_results", UNSET))

        message = cls(
            role=role,
            content=content,
            timestamp=timestamp,
            tool_call_id=tool_call_id,
            structured_question=structured_question,
            preview_results=preview_results,
        )

        message.additional_properties = d
        return message

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
