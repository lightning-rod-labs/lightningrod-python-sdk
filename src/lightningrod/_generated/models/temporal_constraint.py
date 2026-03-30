from enum import Enum


class TemporalConstraint(str, Enum):
    AFTER = "AFTER"
    BEFORE = "BEFORE"
    EQUAL = "EQUAL"
    NEXT_DOCUMENT = "NEXT_DOCUMENT"
    PREVIOUS_DOCUMENT = "PREVIOUS_DOCUMENT"

    def __str__(self) -> str:
        return str(self.value)
