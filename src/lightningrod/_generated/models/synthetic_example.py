from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyntheticExample")


@_attrs_define
class SyntheticExample:
    """A fabricated example of what the pipeline would produce.

    Attributes:
        seed_text (str): Example source data
        generated_question (str): Example question
        answer_type (str): Question type
        expected_answer (None | str | Unset): Example answer
    """

    seed_text: str
    generated_question: str
    answer_type: str
    expected_answer: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        seed_text = self.seed_text

        generated_question = self.generated_question

        answer_type = self.answer_type

        expected_answer: None | str | Unset
        if isinstance(self.expected_answer, Unset):
            expected_answer = UNSET
        else:
            expected_answer = self.expected_answer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seed_text": seed_text,
                "generated_question": generated_question,
                "answer_type": answer_type,
            }
        )
        if expected_answer is not UNSET:
            field_dict["expected_answer"] = expected_answer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        seed_text = d.pop("seed_text")

        generated_question = d.pop("generated_question")

        answer_type = d.pop("answer_type")

        def _parse_expected_answer(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        expected_answer = _parse_expected_answer(d.pop("expected_answer", UNSET))

        synthetic_example = cls(
            seed_text=seed_text,
            generated_question=generated_question,
            answer_type=answer_type,
            expected_answer=expected_answer,
        )

        synthetic_example.additional_properties = d
        return synthetic_example

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
