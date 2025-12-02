from enum import Enum


class ModelSourceType(str, Enum):
    DEEPINFRA = "DEEPINFRA"
    DEEPSEEK = "DEEPSEEK"
    HUGGINGFACE_ENDPOINTS = "HUGGINGFACE_ENDPOINTS"
    OPENAI = "OPENAI"
    OPEN_ROUTER = "OPEN_ROUTER"
    RUNPOD = "RUNPOD"
    SGLANG = "SGLANG"
    VLLM = "VLLM"

    def __str__(self) -> str:
        return str(self.value)
