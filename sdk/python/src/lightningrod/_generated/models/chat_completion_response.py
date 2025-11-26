from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.choice import Choice
    from ..models.usage import Usage


T = TypeVar("T", bound="ChatCompletionResponse")


@_attrs_define
class ChatCompletionResponse:
    """
    Attributes:
        id (str): A unique identifier for the chat completion
        created (int): Unix timestamp of when the completion was created
        model (str): The model used for the chat completion
        choices (list[Choice]): A list of chat completion choices
        object_ (Literal['chat.completion'] | Unset): The object type Default: 'chat.completion'.
        usage (None | Unset | Usage): Usage statistics for the completion request
    """

    id: str
    created: int
    model: str
    choices: list[Choice]
    object_: Literal["chat.completion"] | Unset = "chat.completion"
    usage: None | Unset | Usage = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage import Usage

        id = self.id

        created = self.created

        model = self.model

        choices = []
        for choices_item_data in self.choices:
            choices_item = choices_item_data.to_dict()
            choices.append(choices_item)

        object_ = self.object_

        usage: dict[str, Any] | None | Unset
        if isinstance(self.usage, Unset):
            usage = UNSET
        elif isinstance(self.usage, Usage):
            usage = self.usage.to_dict()
        else:
            usage = self.usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created": created,
                "model": model,
                "choices": choices,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.choice import Choice
        from ..models.usage import Usage

        d = dict(src_dict)
        id = d.pop("id")

        created = d.pop("created")

        model = d.pop("model")

        choices = []
        _choices = d.pop("choices")
        for choices_item_data in _choices:
            choices_item = Choice.from_dict(choices_item_data)

            choices.append(choices_item)

        object_ = cast(Literal["chat.completion"] | Unset, d.pop("object", UNSET))
        if object_ != "chat.completion" and not isinstance(object_, Unset):
            raise ValueError(f"object must match const 'chat.completion', got '{object_}'")

        def _parse_usage(data: object) -> None | Unset | Usage:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                usage_type_0 = Usage.from_dict(data)

                return usage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | Usage, data)

        usage = _parse_usage(d.pop("usage", UNSET))

        chat_completion_response = cls(
            id=id,
            created=created,
            model=model,
            choices=choices,
            object_=object_,
            usage=usage,
        )

        chat_completion_response.additional_properties = d
        return chat_completion_response

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
