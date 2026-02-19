from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.reward_function_type import RewardFunctionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MultipleChoiceAnswerType")


@_attrs_define
class MultipleChoiceAnswerType:
    r"""
    Attributes:
        answer_type (Literal['MULTIPLE_CHOICE'] | Unset):  Default: 'MULTIPLE_CHOICE'.
        answer_format_instruction (str | Unset): Instructions describing how the answer should be formatted and given.
            Default: 'This is a multiple choice question with answer options. The list of options will be provided in the
            question. You are estimating the probability for each option being the correct answer. Provide your confidence
            for each option as a value between 0 and 1, where the probabilities must sum to 1. Provide your answer as a JSON
            dictionary between <answer></answer> tags, with keys like option_0, option_1, etc. corresponding to each option
            in order. Example: <answer>{\\"option_0\\": 0.3, \\"option_1\\": 0.4, \\"option_2\\": 0.2, \\"option_3\\":
            0.1}</answer>'.
        labeler_instruction (str | Unset): Instructions for the labeler. Default: "The answer should be ONLY one of the
            following options: 'A', 'B', 'C', or 'D', or 'Undetermined'. Do not include any other text or explanation.".
        question_generation_instruction (str | Unset): Instructions for generating questions of this type. Default:
            'Generate questions with multiple choice options (up to 10). Format the options on separate lines after the
            question:\nA) First option\nB) Second option\nC) Third option\n... and so on\n\nEach option should be distinct
            and mutually exclusive. A clear and unambiguous multiple-choice question, based on the provided seed_text.
            Include the options in the question text.'.
        reward_function_type (None | RewardFunctionType | Unset):  Default: RewardFunctionType.MULTI_CHOICE_LOG_SCORE.
    """

    answer_type: Literal["MULTIPLE_CHOICE"] | Unset = "MULTIPLE_CHOICE"
    answer_format_instruction: str | Unset = (
        'This is a multiple choice question with answer options. The list of options will be provided in the question. You are estimating the probability for each option being the correct answer. Provide your confidence for each option as a value between 0 and 1, where the probabilities must sum to 1. Provide your answer as a JSON dictionary between <answer></answer> tags, with keys like option_0, option_1, etc. corresponding to each option in order. Example: <answer>{\\"option_0\\": 0.3, \\"option_1\\": 0.4, \\"option_2\\": 0.2, \\"option_3\\": 0.1}</answer>'
    )
    labeler_instruction: str | Unset = (
        "The answer should be ONLY one of the following options: 'A', 'B', 'C', or 'D', or 'Undetermined'. Do not include any other text or explanation."
    )
    question_generation_instruction: str | Unset = (
        "Generate questions with multiple choice options (up to 10). Format the options on separate lines after the question:\nA) First option\nB) Second option\nC) Third option\n... and so on\n\nEach option should be distinct and mutually exclusive. A clear and unambiguous multiple-choice question, based on the provided seed_text. Include the options in the question text."
    )
    reward_function_type: None | RewardFunctionType | Unset = RewardFunctionType.MULTI_CHOICE_LOG_SCORE
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
        answer_type = cast(Literal["MULTIPLE_CHOICE"] | Unset, d.pop("answer_type", UNSET))
        if answer_type != "MULTIPLE_CHOICE" and not isinstance(answer_type, Unset):
            raise ValueError(f"answer_type must match const 'MULTIPLE_CHOICE', got '{answer_type}'")

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

        multiple_choice_answer_type = cls(
            answer_type=answer_type,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
            reward_function_type=reward_function_type,
        )

        multiple_choice_answer_type.additional_properties = d
        return multiple_choice_answer_type

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
