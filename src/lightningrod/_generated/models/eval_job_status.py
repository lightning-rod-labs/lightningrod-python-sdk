from enum import Enum


class EvalJobStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    STARTING = "STARTING"

    def __str__(self) -> str:
        return str(self.value)
