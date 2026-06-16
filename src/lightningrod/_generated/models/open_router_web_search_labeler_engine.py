from enum import Enum


class OpenRouterWebSearchLabelerEngine(str, Enum):
    AUTO = "auto"
    EXA = "exa"
    FIRECRAWL = "firecrawl"
    NATIVE = "native"
    PARALLEL = "parallel"

    def __str__(self) -> str:
        return str(self.value)
