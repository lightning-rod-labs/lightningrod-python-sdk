from enum import Enum


class TransformJobStatus(str, Enum):
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"

    def __str__(self) -> str:
        return str(self.value)
