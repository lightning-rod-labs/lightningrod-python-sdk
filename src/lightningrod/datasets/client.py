from typing import List, Optional

from lightningrod._generated.models import (
    DatasetLinterRunRequest,
    DatasetLinterRunResponse,
    DatasetLinterRunStatus,
    ListDatasetsResponse,
    ListDatasetLinterRunsResponse,
    ListRulesResponse,
    UploadSamplesRequest,
)
from lightningrod._generated.models.sample import Sample
from lightningrod._generated.api.datasets import (
    create_dataset_datasets_post,
    get_dataset_datasets_dataset_id_get,
    get_dataset_samples_datasets_dataset_id_samples_get,
    list_datasets_datasets_get,
    upload_samples_datasets_dataset_id_samples_post,
)
from lightningrod._generated.api.dataset_linter.get_linter_run_dataset_linter_linter_runs_run_id_get import (
    sync_detailed as get_linter_run_detailed,
)
from lightningrod._generated.api.dataset_linter.list_rules_dataset_linter_rules_get import (
    sync_detailed as list_rules_detailed,
)
from lightningrod._generated.api.dataset_linter.list_runs_for_dataset_dataset_linter_datasets_dataset_id_linter_runs_get import (
    sync_detailed as list_runs_for_dataset_detailed,
)
from lightningrod._generated.api.dataset_linter.run_lint_dataset_linter_datasets_dataset_id_lint_post import (
    sync_detailed as run_lint_detailed,
)
from lightningrod._generated.types import UNSET, Unset
from lightningrod._generated.client import AuthenticatedClient
from lightningrod.datasets.dataset import SampleDataset
from lightningrod._errors import handle_response_error
from lightningrod._display import (
    _is_notebook,
    display_error,
    run_dataset_linter_live_display,
)


class DatasetSamplesClient:
    def __init__(self, client: AuthenticatedClient):
        self._client: AuthenticatedClient = client
    
    def list(self, dataset_id: str) -> List[Sample]:
        samples: List[Sample] = []
        cursor: Optional[str] = None
        
        while True:
            response = get_dataset_samples_datasets_dataset_id_samples_get.sync_detailed(
                dataset_id=dataset_id,
                client=self._client,
                limit=100,
                cursor=cursor,
            )
            
            parsed = handle_response_error(response, "fetch samples")
            
            samples.extend(parsed.samples)
            
            if not parsed.has_more:
                break
            if isinstance(parsed.next_cursor, Unset) or parsed.next_cursor is None:
                break
            cursor = str(parsed.next_cursor)
        
        return samples
    
    def upload(
        self,
        dataset_id: str,
        samples: List[Sample],
    ) -> None:
        """
        Upload samples to an existing dataset.
        
        Args:
            dataset_id: ID of the dataset to upload samples to
            samples: List of Sample objects to upload
            
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> samples = [Sample(seed=Seed(...), ...), ...]
            >>> lr.datasets.upload(samples)
        """
        request = UploadSamplesRequest(samples=samples)
        
        response = upload_samples_datasets_dataset_id_samples_post.sync_detailed(
            dataset_id=dataset_id,
            client=self._client,
            body=request,
        )
        
        handle_response_error(response, "upload samples")


class DatasetLinterClient:
    def __init__(self, client: AuthenticatedClient):
        self._client: AuthenticatedClient = client

    def list_rules(self) -> ListRulesResponse:
        response = list_rules_detailed(client=self._client)
        return handle_response_error(response, "list linter rules")

    def run(
        self,
        dataset_id: str,
        rules: Optional[List[str]] = None,
        random_sample_size: Optional[int] = None,
        poll_interval: float = 15,
    ) -> DatasetLinterRunResponse:
        if rules is None and random_sample_size is None:
            body = UNSET
        else:
            body = DatasetLinterRunRequest(
                rules=UNSET if rules is None else rules,
                random_sample_size=UNSET if random_sample_size is None else random_sample_size,
            )
        response = run_lint_detailed(
            dataset_id=dataset_id,
            client=self._client,
            body=body,
        )
        run = handle_response_error(response, "run dataset linter")

        def poll() -> DatasetLinterRunResponse:
            nonlocal run
            run = self.get_run(run.id)
            return run

        run_dataset_linter_live_display(poll, poll_interval=poll_interval, initial_run=run)

        if run.status == DatasetLinterRunStatus.FAILED:
            error_msg = (
                run.error_message
                if not isinstance(run.error_message, Unset) and run.error_message
                else "Unknown error"
            )
            display_error(error_msg, title="Dataset Linter Failed")
            if not _is_notebook():
                raise Exception(f"Dataset linter run {run.id} failed: {error_msg}")

        return run

    def get_run(self, run_id: str) -> DatasetLinterRunResponse:
        response = get_linter_run_detailed(
            run_id=run_id,
            client=self._client,
        )
        return handle_response_error(response, "get linter run")

    def list_runs(
        self,
        dataset_id: str,
        limit: int = 20,
    ) -> ListDatasetLinterRunsResponse:
        response = list_runs_for_dataset_detailed(
            dataset_id=dataset_id,
            client=self._client,
            limit=limit,
        )
        return handle_response_error(response, "list linter runs for dataset")


class DatasetsClient:
    def __init__(self, client: AuthenticatedClient, dataset_samples_client: DatasetSamplesClient):
        self._client: AuthenticatedClient = client
        self._dataset_samples_client: DatasetSamplesClient = dataset_samples_client
        self.linter: DatasetLinterClient = DatasetLinterClient(client)
    
    def create(self) -> SampleDataset:
        """
        Create a new empty dataset.
        
        Returns:
            Dataset object representing the newly created dataset
            
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> dataset = lr.datasets.create()
            >>> print(f"Created dataset: {dataset.id}")
        """
        response = create_dataset_datasets_post.sync_detailed(
            client=self._client,
        )
        
        create_result = handle_response_error(response, "create dataset")
        
        dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
            dataset_id=create_result.id,
            client=self._client,
        )
        dataset_result = handle_response_error(dataset_response, "get dataset")
        
        return SampleDataset(
            id=dataset_result.id,
            num_rows=dataset_result.num_rows,
            datasets_client=self._dataset_samples_client
        )
    
    def create_from_samples(
        self,
        samples: List[Sample],
        batch_size: int = 1000,
    ) -> SampleDataset:
        """
        Create a new dataset and upload samples to it.
        
        This is a convenience method that creates a dataset and uploads all samples
        in batches. Useful for creating input datasets from a collection of seeds.
        
        Args:
            samples: List of Sample objects to upload
            batch_size: Number of samples to upload per batch (default: 1000)
            
        Returns:
            Dataset object with all samples uploaded
            
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> samples = [Sample(seed=Seed(...), ...), ...]
            >>> dataset = lr.datasets.create_from_samples(samples, batch_size=1000)
            >>> print(f"Created dataset with {dataset.num_rows} samples")
        """
        dataset = self.create()
        
        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            self._dataset_samples_client.upload(dataset.id, batch)
        
        dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
            dataset_id=dataset.id,
            client=self._client,
        )
        dataset_result = handle_response_error(dataset_response, "refresh dataset")
        
        dataset.num_rows = dataset_result.num_rows
        return dataset
    
    def get(self, dataset_id: str) -> SampleDataset:
        """
        Get a dataset by ID.
        
        Args:
            dataset_id: ID of the dataset to retrieve
            
        Returns:
            Dataset object
            
        Example:
            >>> lr = LightningRod(api_key="your-api-key")
            >>> dataset = lr.datasets.get("dataset-id-here")
        """
        dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
            dataset_id=dataset_id,
            client=self._client,
        )
        dataset_result = handle_response_error(dataset_response, "get dataset")
        
        return SampleDataset(
            id=dataset_result.id,
            num_rows=dataset_result.num_rows,
            datasets_client=self._dataset_samples_client
        )

    def list(
        self,
        *,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> ListDatasetsResponse:
        response = list_datasets_datasets_get.sync_detailed(
            client=self._client,
            limit=limit,
            cursor=cursor if cursor is not None else UNSET,
        )
        return handle_response_error(response, "list datasets")
