from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.answer_parser_type import AnswerParserType
from ..models.reward_function_type import RewardFunctionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContinuousValueOnlyAnswerType")


@_attrs_define
class ContinuousValueOnlyAnswerType:
    r"""Continuous question type that predicts a single scalar value.

    Use this when the model should output a point estimate (e.g. "42.5") rather than
    a full distribution. Scored via CONTINUOUS_VALUE_ONLY_LOG_SCORE by default.

    For uncertainty-aware predictions use ContinuousAnswerType instead, which predicts
    {mean, standard_deviation} and is scored via CONTINUOUS_LOG_SCORE.

        Attributes:
            answer_type (Literal['CONTINUOUS_VALUE_ONLY'] | Unset):  Default: 'CONTINUOUS_VALUE_ONLY'.
            answer_format_instruction (str | Unset): Appended to training/inference prompts to instruct the model how to
                format its prediction. Most users should not need to override this — if results are poor, override this field or
                open an issue at https://github.com/lightning-rod-labs/lightningrod-python-sdk/issues/new Default: 'This
                question expects a numeric value as the answer. Provide your best single-number estimate. Include units if
                specified in the question. Provide your answer between <answer></answer> tags. Example: <answer>42.5</answer>'.
            labeler_instruction (str | Unset): Instructions for the labeler. Default: "The answer should be ONLY a single
                exact numeric value, not a range. For example: '42.5' or '1000', not '40-45' or 'between 900 and 1100', or
                'Undetermined'. Do not include any other text or explanation.".
            question_generation_instruction (str | Unset): Instructions for generating questions of this type. Default:
                'Generate forecasting questions that expect a single numeric answer.\n\nEach question MUST:\n- Have EXACTLY ONE
                numeric answer (integer or decimal)\n- Specify the unit of measurement\n- Be fully self-contained (all entities,
                locations, dates included)\n- Refer to a clearly defined event or measurement period with an explicit end
                date\n- Describe an outcome plausibly reported in a major news headline or official release\n\nSTRICTLY DO NOT
                include:\n- Binary or categorical outcomes\n- Trivial, obscure, or low-impact measurements\n- Vague language or
                approximations\n- Ranges, intervals, or multiple correct values\n- Ambiguous definitions or aggregations\n-
                Outcomes dependent on unpublished, proprietary, or speculative data'.
            reward_function_type (None | RewardFunctionType | Unset):  Default:
                RewardFunctionType.CONTINUOUS_VALUE_ONLY_LOG_SCORE.
            answer_parser_type (AnswerParserType | None | Unset):  Default: AnswerParserType.CONTINUOUS_VALUE_ONLY.
    """

    answer_type: Literal["CONTINUOUS_VALUE_ONLY"] | Unset = "CONTINUOUS_VALUE_ONLY"
    answer_format_instruction: str | Unset = (
        "This question expects a numeric value as the answer. Provide your best single-number estimate. Include units if specified in the question. Provide your answer between <answer></answer> tags. Example: <answer>42.5</answer>"
    )
    labeler_instruction: str | Unset = (
        "The answer should be ONLY a single exact numeric value, not a range. For example: '42.5' or '1000', not '40-45' or 'between 900 and 1100', or 'Undetermined'. Do not include any other text or explanation."
    )
    question_generation_instruction: str | Unset = (
        "Generate forecasting questions that expect a single numeric answer.\n\nEach question MUST:\n- Have EXACTLY ONE numeric answer (integer or decimal)\n- Specify the unit of measurement\n- Be fully self-contained (all entities, locations, dates included)\n- Refer to a clearly defined event or measurement period with an explicit end date\n- Describe an outcome plausibly reported in a major news headline or official release\n\nSTRICTLY DO NOT include:\n- Binary or categorical outcomes\n- Trivial, obscure, or low-impact measurements\n- Vague language or approximations\n- Ranges, intervals, or multiple correct values\n- Ambiguous definitions or aggregations\n- Outcomes dependent on unpublished, proprietary, or speculative data"
    )
    reward_function_type: None | RewardFunctionType | Unset = RewardFunctionType.CONTINUOUS_VALUE_ONLY_LOG_SCORE
    answer_parser_type: AnswerParserType | None | Unset = AnswerParserType.CONTINUOUS_VALUE_ONLY
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
        answer_type = cast(Literal["CONTINUOUS_VALUE_ONLY"] | Unset, d.pop("answer_type", UNSET))
        if answer_type != "CONTINUOUS_VALUE_ONLY" and not isinstance(answer_type, Unset):
            raise ValueError(f"answer_type must match const 'CONTINUOUS_VALUE_ONLY', got '{answer_type}'")

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

        continuous_value_only_answer_type = cls(
            answer_type=answer_type,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
            reward_function_type=reward_function_type,
            answer_parser_type=answer_parser_type,
        )

        continuous_value_only_answer_type.additional_properties = d
        return continuous_value_only_answer_type

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
