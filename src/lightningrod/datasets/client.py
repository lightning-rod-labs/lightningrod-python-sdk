from typing import List, Optional

from lightningrod._generated.models import (
    HTTPValidationError,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.api.datasets import (
    get_dataset_samples_datasets_dataset_id_samples_get,
)
from lightningrod._generated.types import Unset
from lightningrod._generated.client import AuthenticatedClient



class DatasetSamplesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client: AuthenticatedClient = client
    
    def list(self, dataset_id: str) -> List[Sample]:
        samples: List[Sample] = []
        cursor: Optional[str] = None
        
        while True:
            response = get_dataset_samples_datasets_dataset_id_samples_get.sync(
                dataset_id=dataset_id,
                client=self._client,
                limit=100,
                cursor=cursor,
            )
            
            if isinstance(response, HTTPValidationError):
                raise Exception(f"Failed to fetch samples: {response.detail}")
            if response is None:
                raise Exception("Failed to fetch samples: received None response")
            
            samples.extend(response.samples)
            
            if not response.has_more:
                break
            if isinstance(response.next_cursor, Unset) or response.next_cursor is None:
                break
            cursor = str(response.next_cursor)
        
        return samples
