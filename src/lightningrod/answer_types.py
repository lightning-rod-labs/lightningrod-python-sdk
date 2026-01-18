from lightningrod._generated.models.answer_type import AnswerType
from lightningrod._generated.models.answer_type_enum import AnswerTypeEnum
from lightningrod._generated.types import UNSET, Unset


class AnswerTypes:
    @staticmethod
    def binary(
        answer_format_instruction: None | str | Unset = UNSET,
        labeler_instruction: None | str | Unset = UNSET,
        question_generation_instruction: None | str | Unset = UNSET,
    ) -> AnswerType:
        return AnswerType(
            answer_type=AnswerTypeEnum.BINARY,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
        )

    @staticmethod
    def continuous(
        answer_format_instruction: None | str | Unset = UNSET,
        labeler_instruction: None | str | Unset = UNSET,
        question_generation_instruction: None | str | Unset = UNSET,
    ) -> AnswerType:
        return AnswerType(
            answer_type=AnswerTypeEnum.CONTINUOUS,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
        )

    @staticmethod
    def free_response(
        answer_format_instruction: None | str | Unset = UNSET,
        labeler_instruction: None | str | Unset = UNSET,
        question_generation_instruction: None | str | Unset = UNSET,
    ) -> AnswerType:
        return AnswerType(
            answer_type=AnswerTypeEnum.FREE_RESPONSE,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
        )

    @staticmethod
    def multiple_choice(
        answer_format_instruction: None | str | Unset = UNSET,
        labeler_instruction: None | str | Unset = UNSET,
        question_generation_instruction: None | str | Unset = UNSET,
    ) -> AnswerType:
        return AnswerType(
            answer_type=AnswerTypeEnum.MULTIPLE_CHOICE,
            answer_format_instruction=answer_format_instruction,
            labeler_instruction=labeler_instruction,
            question_generation_instruction=question_generation_instruction,
        )

