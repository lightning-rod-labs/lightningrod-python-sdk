from enum import Enum


class AnswerParserType(str, Enum):
    BINARY = "binary"
    CONTINUOUS = "continuous"
    CONTINUOUS_VALUE_ONLY = "continuous_value_only"
    FRACTION = "fraction"
    MULTI_CHOICE = "multi_choice"

    def __str__(self) -> str:
        return str(self.value)
