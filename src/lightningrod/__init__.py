"""
Lightning Rod Python SDK

Calibrated probability forecasts through an OpenAI-compatible inference API.
"""

from lightningrod.client import LightningRod
from lightningrod.prediction import (
    DEFAULT_MODEL,
    AnswerType,
    ReasoningEffort,
    BinaryPrediction,
    ContinuousPrediction,
    MultiChoicePrediction,
    FreeResponsePrediction,
    Source,
    Usage,
    PredictionResult,
)
from lightningrod.utils.config import LightningrodAuthError

__version__ = "1.1.0"
__all__ = [
    "LightningRod",
    "DEFAULT_MODEL",
    "AnswerType",
    "ReasoningEffort",
    "BinaryPrediction",
    "ContinuousPrediction",
    "MultiChoicePrediction",
    "FreeResponsePrediction",
    "Source",
    "Usage",
    "PredictionResult",
    "LightningrodAuthError",
]
