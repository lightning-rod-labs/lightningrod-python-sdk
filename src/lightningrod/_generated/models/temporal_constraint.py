from enum import Enum


class TemporalConstraint(str, Enum):
    AFTER = "AFTER"
    BEFORE = "BEFORE"

    def __str__(self) -> str:
        return str(self.value)
