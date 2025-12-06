from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.answer_type_enum import AnswerTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnswerType")


@_attrs_define
class AnswerType:
    """
    Attributes:
        answer_type (AnswerTypeEnum):
        instruction (str): Instructions describing how the answer should be given
        format_instruction (None | str | Unset): Custom format instructions for parsing the answer. If not set, uses
            default based on answer_type.
        labeler_instruction (None | str | Unset): Custom instructions for the labeler. If not set, uses default based on
            answer_type.
        question_generation_guidance (None | str | Unset): Custom guidance for generating questions of this type. If not
            set, uses default based on answer_type.
        question_field_description (None | str | Unset): Custom description for the question_text field in structured
            output. If not set, uses default based on answer_type.
    """

    answer_type: AnswerTypeEnum
    instruction: str
    format_instruction: None | str | Unset = UNSET
    labeler_instruction: None | str | Unset = UNSET
    question_generation_guidance: None | str | Unset = UNSET
    question_field_description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        answer_type = self.answer_type.value

        instruction = self.instruction

        format_instruction: None | str | Unset
        if isinstance(self.format_instruction, Unset):
            format_instruction = UNSET
        else:
            format_instruction = self.format_instruction

        labeler_instruction: None | str | Unset
        if isinstance(self.labeler_instruction, Unset):
            labeler_instruction = UNSET
        else:
            labeler_instruction = self.labeler_instruction

        question_generation_guidance: None | str | Unset
        if isinstance(self.question_generation_guidance, Unset):
            question_generation_guidance = UNSET
        else:
            question_generation_guidance = self.question_generation_guidance

        question_field_description: None | str | Unset
        if isinstance(self.question_field_description, Unset):
            question_field_description = UNSET
        else:
            question_field_description = self.question_field_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer_type": answer_type,
                "instruction": instruction,
            }
        )
        if format_instruction is not UNSET:
            field_dict["format_instruction"] = format_instruction
        if labeler_instruction is not UNSET:
            field_dict["labeler_instruction"] = labeler_instruction
        if question_generation_guidance is not UNSET:
            field_dict["question_generation_guidance"] = question_generation_guidance
        if question_field_description is not UNSET:
            field_dict["question_field_description"] = question_field_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        answer_type = AnswerTypeEnum(d.pop("answer_type"))

        instruction = d.pop("instruction")

        def _parse_format_instruction(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        format_instruction = _parse_format_instruction(d.pop("format_instruction", UNSET))

        def _parse_labeler_instruction(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        labeler_instruction = _parse_labeler_instruction(d.pop("labeler_instruction", UNSET))

        def _parse_question_generation_guidance(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        question_generation_guidance = _parse_question_generation_guidance(d.pop("question_generation_guidance", UNSET))

        def _parse_question_field_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        question_field_description = _parse_question_field_description(d.pop("question_field_description", UNSET))

        answer_type = cls(
            answer_type=answer_type,
            instruction=instruction,
            format_instruction=format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_guidance=question_generation_guidance,
            question_field_description=question_field_description,
        )

        answer_type.additional_properties = d
        return answer_type

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
