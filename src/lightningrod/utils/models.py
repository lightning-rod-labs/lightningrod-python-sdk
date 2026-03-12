"""Model configuration helpers."""

from lightningrod._generated.models.model_config import ModelConfig
from lightningrod._generated.models.model_source_type import ModelSourceType


def open_router_model(model_name: str) -> ModelConfig:
    """Create a ModelConfig for an OpenRouter-hosted model."""
    return ModelConfig(
        model_name=model_name,
        model_source=ModelSourceType.OPEN_ROUTER,
        use_pipeline_key=True,
    )

def lightningrod_model(model_name = "foresight-v3") -> ModelConfig:
    """Create a ModelConfig for a Lightning Rod-hosted model."""
    return ModelConfig(
        model_name=f"LightningRodLabs/{model_name}",
        model_source=ModelSourceType.VLLM,
        reasoning_effort="high",
        is_lightningrod_model=True,
    )