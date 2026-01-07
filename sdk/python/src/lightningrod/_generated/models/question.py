from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Question")


@_attrs_define
class Question:
    """
    Attributes:
        question_text (str):
        question_type (Literal['QUESTION'] | Unset):  Default: 'QUESTION'.
    """

    question_text: str
    question_type: Literal["QUESTION"] | Unset = "QUESTION"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_text = self.question_text

        question_type = self.question_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_text": question_text,
            }
        )
        if question_type is not UNSET:
            field_dict["question_type"] = question_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        question_text = d.pop("question_text")

        question_type = cast(Literal["QUESTION"] | Unset, d.pop("question_type", UNSET))
        if question_type != "QUESTION" and not isinstance(question_type, Unset):
            raise ValueError(f"question_type must match const 'QUESTION', got '{question_type}'")

        question = cls(
            question_text=question_text,
            question_type=question_type,
        )

        question.additional_properties = d
        return question

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
