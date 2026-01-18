from enum import Enum


class AnswerTypeEnum(str, Enum):
    BINARY = "BINARY"
    CONTINUOUS = "CONTINUOUS"
    FREE_RESPONSE = "FREE_RESPONSE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"

    def __str__(self) -> str:
        return str(self.value)
