from typing import Optional


class LightningRodClient:
    """
    Python client for the Lightning Rod API.
    
    This client provides access to Lightning Rod's AI-powered forecasting
    dataset generation platform.
    
    Args:
        api_key: Your Lightning Rod API key
        base_url: Base URL for the API (defaults to production)
    
    Example:
        >>> client = LightningRodClient(api_key="your-api-key")
        >>> version = client.get_version()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.lightningrod.ai"
    ):
        self.api_key: str = api_key
        self.base_url: str = base_url.rstrip("/")
        self._headers: dict[str, str] = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    
    def get_version(self) -> str:
        """
        Get the SDK version.
        
        Returns:
            SDK version string
        """
        return "0.1.0"
    
    # Future method signature (to be implemented):
    # def run(self, pipeline, dataset: Optional[str] = None) -> Dataset:
    #     """
    #     Run a pipeline on a dataset.
    #     
    #     Args:
    #         pipeline: Pipeline configuration (e.g., QuestionGenerationPipeline)
    #         dataset: Optional dataset ID to run the pipeline on
    #     
    #     Returns:
    #         Dataset containing the results
    #     """
    #     pass

