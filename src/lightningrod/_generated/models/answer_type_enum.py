from enum import Enum


class AnswerTypeEnum(str, Enum):
    BINARY = "BINARY"
    CONTINUOUS = "CONTINUOUS"
    CONTINUOUS_VALUE_ONLY = "CONTINUOUS_VALUE_ONLY"
    FREE_RESPONSE = "FREE_RESPONSE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"

    def __str__(self) -> str:
        return str(self.value)
