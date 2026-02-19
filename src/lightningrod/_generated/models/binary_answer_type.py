from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.reward_function_type import RewardFunctionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BinaryAnswerType")


@_attrs_define
class BinaryAnswerType:
    """
    Attributes:
        answer_type (Literal['BINARY'] | Unset):  Default: 'BINARY'.
        answer_format_instruction (str | Unset): Instructions describing how the answer should be formatted and given.
            Default: "This is a binary yes/no question. You are estimating the probability that the answer is 'Yes'. Provide
            your confidence as a value between 0 (definitely No) and 1 (definitely Yes). Provide your probability estimate
            for Yes as a decimal between 0 and 1. Provide your answer between <answer></answer> tags. Example:
            <answer>0.75</answer>".
        labeler_instruction (str | Unset): Instructions for the labeler. Default: "The answer should be ONLY '1', '0',
            or 'Undetermined'. '1' means yes, '0' means no, and 'Undetermined' means the answer is not clear. Do not include
            any other text or explanation.".
        question_generation_instruction (str | Unset): Instructions for generating questions of this type. Default:
            "Generate questions that can be answered with Yes or No. Frame the question so it has exactly two possible
            outcomes: Yes or No. The question should start with words like 'Will', 'Is', 'Does', 'Has', 'Can', etc. A clear
            and unambiguous yes/no question, based on the provided seed_text.".
        reward_function_type (None | RewardFunctionType | Unset):  Default: RewardFunctionType.BINARY_BRIER.
    """

    answer_type: Literal["BINARY"] | Unset = "BINARY"
    answer_format_instruction: str | Unset = (
        "This is a binary yes/no question. You are estimating the probability that the answer is 'Yes'. Provide your confidence as a value between 0 (definitely No) and 1 (definitely Yes). Provide your probability estimate for Yes as a decimal between 0 and 1. Provide your answer between <answer></answer> tags. Example: <answer>0.75</answer>"
    )
    labeler_instruction: str | Unset = (
        "The answer should be ONLY '1', '0', or 'Undetermined'. '1' means yes, '0' means no, and 'Undetermined' means the answer is not clear. Do not include any other text or explanation."
    )
    question_generation_instruction: str | Unset = (
        "Generate questions that can be answered with Yes or No. Frame the question so it has exactly two possible outcomes: Yes or No. The question should start with words like 'Will', 'Is', 'Does', 'Has', 'Can', etc. A clear and unambiguous yes/no question, based on the provided seed_text."
    )
    reward_function_type: None | RewardFunctionType | Unset = RewardFunctionType.BINARY_BRIER
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        answer_type = self.answer_type

        answer_format_instruction = self.answer_format_instruction

        labeler_instruction = self.labeler_instruction

        question_generation_instruction = self.question_generation_instruction

        reward_function_type: None | str | Unset
        if isinstance(self.reward_function_type, Unset):
            reward_function_type = UNSET
        elif isinstance(self.reward_function_type, RewardFunctionType):
            reward_function_type = self.reward_function_type.value
        else:
            reward_function_type = self.reward_function_type

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
        if reward_function_type is not UNSET:
            field_dict["reward_function_type"] = reward_function_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        answer_type = cast(Literal["BINARY"] | Unset, d.pop("answer_type", UNSET))
        if answer_type != "BINARY" and not isinstance(answer_type, Unset):
            raise ValueError(f"answer_type must match const 'BINARY', got '{answer_type}'")

        answer_format_instruction = d.pop("answer_format_instruction", UNSET)

        labeler_instruction = d.pop("labeler_instruction", UNSET)

        question_generation_instruction = d.pop("question_generation_instruction", UNSET)

        def _parse_reward_function_type(data: object) -> None | RewardFunctionType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reward_function_type_type_0 = RewardFunctionType(data)

                return reward_function_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RewardFunctionType | Unset, data)

        reward_function_type = _parse_reward_function_type(d.pop("reward_function_type", UNSET))

        binary_answer_type = cls(
            answer_type=answer_type,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
            reward_function_type=reward_function_type,
        )

        binary_answer_type.additional_properties = d
        return binary_answer_type

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
