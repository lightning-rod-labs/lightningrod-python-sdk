from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.question_option import QuestionOption


T = TypeVar("T", bound="StructuredQuestion")


@_attrs_define
class StructuredQuestion:
    """A structured question with selectable options.

    Attributes:
        question (str):
        options (list[QuestionOption]):
    """

    question: str
    options: list[QuestionOption]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question = self.question

        options = []
        for options_item_data in self.options:
            options_item = options_item_data.to_dict()
            options.append(options_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question": question,
                "options": options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.question_option import QuestionOption

        d = dict(src_dict)
        question = d.pop("question")

        options = []
        _options = d.pop("options")
        for options_item_data in _options:
            options_item = QuestionOption.from_dict(options_item_data)

            options.append(options_item)

        structured_question = cls(
            question=question,
            options=options,
        )

        structured_question.additional_properties = d
        return structured_question

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
