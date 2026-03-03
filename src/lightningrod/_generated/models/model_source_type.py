from enum import Enum


class ModelSourceType(str, Enum):
    DEEPINFRA = "DEEPINFRA"
    DEEPSEEK = "DEEPSEEK"
    DIRECT_COMPLETIONS = "DIRECT_COMPLETIONS"
    HUGGINGFACE_ENDPOINTS = "HUGGINGFACE_ENDPOINTS"
    MODAL_LORA_VLLM = "MODAL_LORA_VLLM"
    OPENAI = "OPENAI"
    OPEN_ROUTER = "OPEN_ROUTER"
    RUNPOD = "RUNPOD"
    SGLANG = "SGLANG"
    TINKER = "TINKER"
    VLLM = "VLLM"

    def __str__(self) -> str:
        return str(self.value)
