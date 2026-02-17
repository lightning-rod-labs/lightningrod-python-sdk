from enum import Enum


class FileSetFileStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"

    def __str__(self) -> str:
        return str(self.value)
