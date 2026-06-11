from enum import Enum


class LLMProvider(str, Enum):
    AUTO = "auto"
    VERTEX_AI = "vertex_ai"

    def __str__(self) -> str:
        return str(self.value)
