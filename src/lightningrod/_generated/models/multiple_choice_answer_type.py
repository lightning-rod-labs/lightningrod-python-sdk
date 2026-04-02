from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.answer_parser_type import AnswerParserType
from ..models.reward_function_type import RewardFunctionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.multiple_choice_answer_type_multiple_choice_options_type_0 import (
        MultipleChoiceAnswerTypeMultipleChoiceOptionsType0,
    )


T = TypeVar("T", bound="MultipleChoiceAnswerType")


@_attrs_define
class MultipleChoiceAnswerType:
    r"""
    Attributes:
        answer_type (Literal['MULTIPLE_CHOICE'] | Unset):  Default: 'MULTIPLE_CHOICE'.
        answer_format_instruction (str | Unset): Appended to training/inference prompts to instruct the model how to
            format its prediction. Most users should not need to override this — if results are poor, override this field or
            open an issue at https://github.com/lightning-rod-labs/lightningrod-python-sdk/issues/new Default: 'This is a
            multiple choice question with answer options. The list of options (option_0, option_1, …) will be provided in
            the question. You are estimating the probability for each option being the correct answer. Provide your
            confidence for each option as a value between 0 and 1, where the probabilities must sum to 1. Provide your
            answer as a JSON dictionary between <answer></answer> tags, with keys option_0, option_1, etc. corresponding to
            each option in order. Example: <answer>{\\"option_0\\": 0.3, \\"option_1\\": 0.4, \\"option_2\\": 0.2,
            \\"option_3\\": 0.1}</answer>'.
        labeler_instruction (str | Unset): Instructions for the labeler. Default: "The answer must be EXACTLY the full
            text of one of the listed answer options.\nDo NOT include the option label (e.g., 'option_0') and do NOT add any
            extra words, punctuation, or explanation.\n\nEach question contains BETWEEN 3 AND 6 answer options, written in
            the question text as:\n  option_0: <brief phrase>\n  option_1: <brief phrase>\n  option_2: <brief phrase>\n
            ...\n\nEach option text is a SHORT PHRASE (typically a few words), not a full sentence.\n\nRespond with:\n- The
            exact text of the correct option, character-for-character, if it can be determined from public web information
            at the resolution date\n- Otherwise, respond with exactly: Undetermined".
        question_generation_instruction (str | Unset): Instructions for generating questions of this type. Default:
            "Generate multiple-choice forecasting questions about a specific future real-world event, based on recent news
            coverage.\n\nThe question text MUST explicitly list all answer options (option_0, option_1, option_2, …) as part
            of the question itself. Do not separate options from the question or imply them indirectly.\n\nEach question
            MUST:\n- Be about ONE clearly defined real-world event or decision (not multiple unrelated events)\n- Ask what
            will happen by a specific resolution date (exact date required)\n- Include BETWEEN 3 AND 6 explicitly listed
            answer options labeled option_0, option_1, option_2, …\n- Have EXACTLY ONE correct answer among the listed
            options\n- Be fully self-contained, including all necessary names, locations, dates, and context\n- Be
            newsworthy and likely to be reported on if it occurs\n- Be resolvable via public web search at the resolution
            date\n- Cover a plausible range of outcomes (no option should be absurd, trivial, or irrelevant)\n\nAnswer
            options MUST:\n- Contain more than two options\n- Be written directly in the question text as 'option_0:
            <text>', 'option_1: <text>', etc.\n- Be mutually exclusive and collectively exhaustive for the event
            described\n- Contain ONLY brief phrases (a few words); do NOT use full sentences\n- Represent alternative
            outcomes of the SAME underlying event\n- Avoid logical dependence or nesting (e.g., no 'both option_0 and
            option_2', no subset relationships)\n- Preserve independence of irrelevant alternatives (IIA): removing any
            incorrect option should not change which option is correct\n\nSTRICTLY AVOID:\n- Past or ongoing events
            presented as future\n- Options that differ only by vague or qualitative wording (e.g., 'significant', 'major',
            'substantial')\n- Context-dependent references (e.g., 'the country', 'the leader', 'later this year')\n- Options
            that combine multiple events, conditions, or contingencies".
        reward_function_type (None | RewardFunctionType | Unset):  Default: RewardFunctionType.MULTI_CHOICE_LOG_SCORE.
        answer_parser_type (AnswerParserType | None | Unset):  Default: AnswerParserType.MULTI_CHOICE.
        multiple_choice_options (MultipleChoiceAnswerTypeMultipleChoiceOptionsType0 | None | Unset): Maps option labels
            to option text, e.g. {'option_0': 'Rate increase', 'option_1': 'No change'}. If not set, options are extracted
            from the question text at scoring time.
    """

    answer_type: Literal["MULTIPLE_CHOICE"] | Unset = "MULTIPLE_CHOICE"
    answer_format_instruction: str | Unset = (
        'This is a multiple choice question with answer options. The list of options (option_0, option_1, …) will be provided in the question. You are estimating the probability for each option being the correct answer. Provide your confidence for each option as a value between 0 and 1, where the probabilities must sum to 1. Provide your answer as a JSON dictionary between <answer></answer> tags, with keys option_0, option_1, etc. corresponding to each option in order. Example: <answer>{\\"option_0\\": 0.3, \\"option_1\\": 0.4, \\"option_2\\": 0.2, \\"option_3\\": 0.1}</answer>'
    )
    labeler_instruction: str | Unset = (
        "The answer must be EXACTLY the full text of one of the listed answer options.\nDo NOT include the option label (e.g., 'option_0') and do NOT add any extra words, punctuation, or explanation.\n\nEach question contains BETWEEN 3 AND 6 answer options, written in the question text as:\n  option_0: <brief phrase>\n  option_1: <brief phrase>\n  option_2: <brief phrase>\n  ...\n\nEach option text is a SHORT PHRASE (typically a few words), not a full sentence.\n\nRespond with:\n- The exact text of the correct option, character-for-character, if it can be determined from public web information at the resolution date\n- Otherwise, respond with exactly: Undetermined"
    )
    question_generation_instruction: str | Unset = (
        "Generate multiple-choice forecasting questions about a specific future real-world event, based on recent news coverage.\n\nThe question text MUST explicitly list all answer options (option_0, option_1, option_2, …) as part of the question itself. Do not separate options from the question or imply them indirectly.\n\nEach question MUST:\n- Be about ONE clearly defined real-world event or decision (not multiple unrelated events)\n- Ask what will happen by a specific resolution date (exact date required)\n- Include BETWEEN 3 AND 6 explicitly listed answer options labeled option_0, option_1, option_2, …\n- Have EXACTLY ONE correct answer among the listed options\n- Be fully self-contained, including all necessary names, locations, dates, and context\n- Be newsworthy and likely to be reported on if it occurs\n- Be resolvable via public web search at the resolution date\n- Cover a plausible range of outcomes (no option should be absurd, trivial, or irrelevant)\n\nAnswer options MUST:\n- Contain more than two options\n- Be written directly in the question text as 'option_0: <text>', 'option_1: <text>', etc.\n- Be mutually exclusive and collectively exhaustive for the event described\n- Contain ONLY brief phrases (a few words); do NOT use full sentences\n- Represent alternative outcomes of the SAME underlying event\n- Avoid logical dependence or nesting (e.g., no 'both option_0 and option_2', no subset relationships)\n- Preserve independence of irrelevant alternatives (IIA): removing any incorrect option should not change which option is correct\n\nSTRICTLY AVOID:\n- Past or ongoing events presented as future\n- Options that differ only by vague or qualitative wording (e.g., 'significant', 'major', 'substantial')\n- Context-dependent references (e.g., 'the country', 'the leader', 'later this year')\n- Options that combine multiple events, conditions, or contingencies"
    )
    reward_function_type: None | RewardFunctionType | Unset = RewardFunctionType.MULTI_CHOICE_LOG_SCORE
    answer_parser_type: AnswerParserType | None | Unset = AnswerParserType.MULTI_CHOICE
    multiple_choice_options: MultipleChoiceAnswerTypeMultipleChoiceOptionsType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.multiple_choice_answer_type_multiple_choice_options_type_0 import (
            MultipleChoiceAnswerTypeMultipleChoiceOptionsType0,
        )

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

        multiple_choice_options: dict[str, Any] | None | Unset
        if isinstance(self.multiple_choice_options, Unset):
            multiple_choice_options = UNSET
        elif isinstance(self.multiple_choice_options, MultipleChoiceAnswerTypeMultipleChoiceOptionsType0):
            multiple_choice_options = self.multiple_choice_options.to_dict()
        else:
            multiple_choice_options = self.multiple_choice_options

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
        if multiple_choice_options is not UNSET:
            field_dict["multiple_choice_options"] = multiple_choice_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.multiple_choice_answer_type_multiple_choice_options_type_0 import (
            MultipleChoiceAnswerTypeMultipleChoiceOptionsType0,
        )

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

        def _parse_multiple_choice_options(
            data: object,
        ) -> MultipleChoiceAnswerTypeMultipleChoiceOptionsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                multiple_choice_options_type_0 = MultipleChoiceAnswerTypeMultipleChoiceOptionsType0.from_dict(data)

                return multiple_choice_options_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MultipleChoiceAnswerTypeMultipleChoiceOptionsType0 | None | Unset, data)

        multiple_choice_options = _parse_multiple_choice_options(d.pop("multiple_choice_options", UNSET))

        multiple_choice_answer_type = cls(
            answer_type=answer_type,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
            reward_function_type=reward_function_type,
            answer_parser_type=answer_parser_type,
            multiple_choice_options=multiple_choice_options,
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
