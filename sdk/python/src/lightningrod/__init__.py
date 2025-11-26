"""
Lightning Rod Python SDK

AI-powered forecasting dataset generation platform.
"""

from lightningrod.client import LightningRodClient
from lightningrod._generated.models.dataset_metadata import DatasetMetadata

__version__ = "0.1.0"
__all__ = [
    "LightningRodClient",
    "DatasetMetadata",
]

