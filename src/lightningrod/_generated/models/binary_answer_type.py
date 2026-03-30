from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.answer_parser_type import AnswerParserType
from ..models.reward_function_type import RewardFunctionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BinaryAnswerType")


@_attrs_define
class BinaryAnswerType:
    r"""
    Attributes:
        answer_type (Literal['BINARY'] | Unset):  Default: 'BINARY'.
        answer_format_instruction (str | Unset): Appended to training/inference prompts to instruct the model how to
            format its prediction. Most users should not need to override this — if results are poor, override this field or
            open an issue at https://github.com/lightning-rod-labs/lightningrod-python-sdk/issues/new Default: "This is a
            binary yes/no question. You are estimating the probability that the answer is 'Yes'. Provide your confidence as
            a value between 0 (definitely No) and 1 (definitely Yes). Provide your probability estimate for Yes as a decimal
            between 0 and 1. Provide your answer between <answer></answer> tags. Example: <answer>0.75</answer>".
        labeler_instruction (str | Unset): Instructions for the labeler. Default: "The answer should be ONLY '1', '0',
            or 'Undetermined'. '1' means yes, '0' means no, and 'Undetermined' means the answer is not clear. Do not include
            any other text or explanation.".
        question_generation_instruction (str | Unset): Instructions for generating questions of this type. Default:
            "Generate binary forecasting questions about future events or outcomes that are unresolved at the time of asking
            and will resolve to a clear, publicly verifiable Yes or No.\n\nEach question MUST:\n- Have EXACTLY ONE binary
            answer: Yes or No\n- Be fully self-contained (all entities, locations, dates included)\n- Refer to a clearly
            defined event or threshold with an explicit resolution date or deadline\n- Describe an outcome plausibly
            reported in a major news headline or official release\n- Start with words like 'Will', 'Is', 'Does', 'Has',
            'Can', 'Did', or similar\n\nSTRICTLY DO NOT include:\n- Numeric or continuous outcomes\n- Multiple-choice or
            categorical questions\n- Trivial, obscure, or low-impact events\n- Vague language or ambiguous resolution
            criteria\n- Outcomes dependent on unpublished, proprietary, or speculative data\n- Questions with more than two
            possible outcomes".
        reward_function_type (None | RewardFunctionType | Unset):  Default: RewardFunctionType.BINARY_BRIER.
        answer_parser_type (AnswerParserType | None | Unset):  Default: AnswerParserType.BINARY.
    """

    answer_type: Literal["BINARY"] | Unset = "BINARY"
    answer_format_instruction: str | Unset = (
        "This is a binary yes/no question. You are estimating the probability that the answer is 'Yes'. Provide your confidence as a value between 0 (definitely No) and 1 (definitely Yes). Provide your probability estimate for Yes as a decimal between 0 and 1. Provide your answer between <answer></answer> tags. Example: <answer>0.75</answer>"
    )
    labeler_instruction: str | Unset = (
        "The answer should be ONLY '1', '0', or 'Undetermined'. '1' means yes, '0' means no, and 'Undetermined' means the answer is not clear. Do not include any other text or explanation."
    )
    question_generation_instruction: str | Unset = (
        "Generate binary forecasting questions about future events or outcomes that are unresolved at the time of asking and will resolve to a clear, publicly verifiable Yes or No.\n\nEach question MUST:\n- Have EXACTLY ONE binary answer: Yes or No\n- Be fully self-contained (all entities, locations, dates included)\n- Refer to a clearly defined event or threshold with an explicit resolution date or deadline\n- Describe an outcome plausibly reported in a major news headline or official release\n- Start with words like 'Will', 'Is', 'Does', 'Has', 'Can', 'Did', or similar\n\nSTRICTLY DO NOT include:\n- Numeric or continuous outcomes\n- Multiple-choice or categorical questions\n- Trivial, obscure, or low-impact events\n- Vague language or ambiguous resolution criteria\n- Outcomes dependent on unpublished, proprietary, or speculative data\n- Questions with more than two possible outcomes"
    )
    reward_function_type: None | RewardFunctionType | Unset = RewardFunctionType.BINARY_BRIER
    answer_parser_type: AnswerParserType | None | Unset = AnswerParserType.BINARY
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

        answer_parser_type: None | str | Unset
        if isinstance(self.answer_parser_type, Unset):
            answer_parser_type = UNSET
        elif isinstance(self.answer_parser_type, AnswerParserType):
            answer_parser_type = self.answer_parser_type.value
        else:
            answer_parser_type = self.answer_parser_type

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
        if answer_parser_type is not UNSET:
            field_dict["answer_parser_type"] = answer_parser_type

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

        def _parse_answer_parser_type(data: object) -> AnswerParserType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                answer_parser_type_type_0 = AnswerParserType(data)

                return answer_parser_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AnswerParserType | None | Unset, data)

        answer_parser_type = _parse_answer_parser_type(d.pop("answer_parser_type", UNSET))

        binary_answer_type = cls(
            answer_type=answer_type,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
            reward_function_type=reward_function_type,
            answer_parser_type=answer_parser_type,
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
