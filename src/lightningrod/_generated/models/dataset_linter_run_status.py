from enum import Enum


class DatasetLinterRunStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"

    def __str__(self) -> str:
        return str(self.value)
