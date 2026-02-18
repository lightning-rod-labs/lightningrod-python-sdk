from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FreeResponseAnswerType")


@_attrs_define
class FreeResponseAnswerType:
    """
    Attributes:
        answer_type (Literal['FREE_RESPONSE'] | Unset):  Default: 'FREE_RESPONSE'.
        answer_format_instruction (str | Unset): Instructions describing how the answer should be formatted and given.
            Default: 'This question expects a free-form text response. Provide an answer that directly addresses what the
            question is asking. Provide your answer between <answer></answer> tags. Example: <answer>The company announced a
            new product line.</answer>'.
        labeler_instruction (str | Unset): Instructions for the labeler. Default: 'Respond with the correct answer as a
            text description.'.
        question_generation_instruction (str | Unset): Instructions for generating questions of this type. Default:
            'Generate questions that expect a free-form text response. A clear and unambiguous question, based on the
            provided seed_text, that expects a free-form text response.'.
    """

    answer_type: Literal["FREE_RESPONSE"] | Unset = "FREE_RESPONSE"
    answer_format_instruction: str | Unset = (
        "This question expects a free-form text response. Provide an answer that directly addresses what the question is asking. Provide your answer between <answer></answer> tags. Example: <answer>The company announced a new product line.</answer>"
    )
    labeler_instruction: str | Unset = "Respond with the correct answer as a text description."
    question_generation_instruction: str | Unset = (
        "Generate questions that expect a free-form text response. A clear and unambiguous question, based on the provided seed_text, that expects a free-form text response."
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        answer_type = self.answer_type

        answer_format_instruction = self.answer_format_instruction

        labeler_instruction = self.labeler_instruction

        question_generation_instruction = self.question_generation_instruction

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if answer_type is not UNSET:
            field_dict["answer_type"] = answer_type
        if answer_format_instruction is not UNSET:
            field_dict["answer_format_instruction"] = answer_format_instruction
        if labeler_instruction is not UNSET:
            field_dict["labeler_instruction"] = labeler_instruction
        if question_generation_instruction is not UNSET:
            field_dict["question_generation_instruction"] = question_generation_instruction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        answer_type = cast(Literal["FREE_RESPONSE"] | Unset, d.pop("answer_type", UNSET))
        if answer_type != "FREE_RESPONSE" and not isinstance(answer_type, Unset):
            raise ValueError(f"answer_type must match const 'FREE_RESPONSE', got '{answer_type}'")

        answer_format_instruction = d.pop("answer_format_instruction", UNSET)

        labeler_instruction = d.pop("labeler_instruction", UNSET)

        question_generation_instruction = d.pop("question_generation_instruction", UNSET)

        free_response_answer_type = cls(
            answer_type=answer_type,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
        )

        free_response_answer_type.additional_properties = d
        return free_response_answer_type

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
