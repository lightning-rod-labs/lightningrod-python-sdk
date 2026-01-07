from typing import TYPE_CHECKING, List

from lightningrod._generated.models.sample import Sample

if TYPE_CHECKING:
    from lightningrod.client import LightningRodClient


class Dataset:
    """
    Represents a dataset in Lightning Rod.
    
    A dataset contains rows of sample data. Use this class to access 
    dataset metadata and download the actual samples.
    
    Note: Datasets should only be created through LightningRodClient methods,
    not instantiated directly.
    
    Attributes:
        id: Unique identifier for the dataset
        num_rows: Number of rows in the dataset
    
    Example:
        >>> client = LightningRodClient(api_key="your-api-key")
        >>> dataset = client.pipeline(config).run()
        >>> samples = dataset.to_samples()
        >>> print(f"Dataset has {len(samples)} samples")
    """
    
    def __init__(
        self,
        id: str,
        num_rows: int,
        client: "LightningRodClient"
    ):
        self.id: str = id
        self.num_rows: int = num_rows
        self._client: "LightningRodClient" = client
    
    def to_samples(self) -> List[Sample]:
        """
        Download all samples from the dataset via the paginated API.
        
        Returns:
            List of Sample objects
        
        Example:
            >>> client = LightningRodClient(api_key="your-api-key")
            >>> dataset = client.pipeline(config).run()
            >>> samples = dataset.to_samples()
            >>> for sample in samples:
            ...     print(sample.seed.seed_text)
        """
        return self._client._fetch_all_samples(self.id)
