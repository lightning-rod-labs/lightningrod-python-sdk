from enum import Enum


class MetadataFieldType(str, Enum):
    NUMBER = "number"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
