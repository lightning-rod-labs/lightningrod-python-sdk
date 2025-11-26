from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.question_input_data import QuestionInputData


T = TypeVar("T", bound="Question")


@_attrs_define
class Question:
    """
    Attributes:
        question_text (str):
        input_data (QuestionInputData | Unset):
    """

    question_text: str
    input_data: QuestionInputData | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question_text = self.question_text

        input_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.input_data, Unset):
            input_data = self.input_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question_text": question_text,
            }
        )
        if input_data is not UNSET:
            field_dict["input_data"] = input_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.question_input_data import QuestionInputData

        d = dict(src_dict)
        question_text = d.pop("question_text")

        _input_data = d.pop("input_data", UNSET)
        input_data: QuestionInputData | Unset
        if isinstance(_input_data, Unset):
            input_data = UNSET
        else:
            input_data = QuestionInputData.from_dict(_input_data)

        question = cls(
            question_text=question_text,
            input_data=input_data,
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
