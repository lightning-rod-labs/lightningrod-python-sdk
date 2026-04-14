from typing import List, Optional, Union

from lightningrod._display import _is_notebook, display_error, display_warning, run_live_display
from lightningrod._generated.models import (
    FileSetDocumentContextGenerator,
    FileSetDocumentLabeler,
    FileSetQuerySeedGenerator,
    FileSetSeedGenerator,
    ForwardLookingQuestionGenerator,
    GdeltSeedGenerator,
    NewsSeedGenerator,
    QuestionAndLabelGenerator,
    QuestionGenerator,
    QuestionPipeline,
    QuestionRenderer,
    TransformJob,
    TransformJobStatus,
    CreateTransformJobRequest,
    HTTPValidationError,
    ListTransformJobsResponse,
    WebSearchLabeler,
    EstimateCostRequest,
    EstimateCostResponse,
    WebSearchContextGenerator,
)
from lightningrod._generated.api.datasets import (
    get_dataset_datasets_dataset_id_get,
)
from lightningrod._generated.api.transform_jobs import (
    create_transform_job_transform_jobs_post,
    get_transform_job_transform_jobs_job_id_get,
    get_transform_job_metrics_transform_jobs_job_id_metrics_get,
    cost_estimation_transform_jobs_cost_estimation_post,
    cancel_transform_job_transform_jobs_job_id_delete,
    list_transform_jobs_transform_jobs_get,
)
from lightningrod._generated.models.pipeline_metrics_response import PipelineMetricsResponse
from lightningrod.datasets.dataset import SampleDataset
from lightningrod._generated.client import AuthenticatedClient
from lightningrod.datasets.client import DatasetSamplesClient
from lightningrod._generated.types import UNSET, Unset
from lightningrod._errors import handle_response_error
from lightningrod.datasets.client import DatasetSamplesClient

TransformConfig = Union[FileSetDocumentContextGenerator, FileSetDocumentLabeler, FileSetQuerySeedGenerator, FileSetSeedGenerator, ForwardLookingQuestionGenerator, GdeltSeedGenerator, NewsSeedGenerator, QuestionAndLabelGenerator, QuestionGenerator, QuestionPipeline, QuestionRenderer, WebSearchLabeler, WebSearchContextGenerator]


def _fetch_error_details_from_samples(
    job: TransformJob,
    samples_client: DatasetSamplesClient,
    jobs_client: "TransformJobsClient",
) -> List[str]:
    details: List[str] = []
    if "rejection_error_messages" in job.additional_properties:
        msgs = job.additional_properties["rejection_error_messages"]
        if isinstance(msgs, list):
            for m in msgs:
                if isinstance(m, str) and m.strip():
                    details.append(m.strip())
        if details:
            return details
    metrics = jobs_client.get_metrics(job.id)
    if metrics:
        for step in metrics.steps:
            if (step.rejected_count > 0 or step.error_count > 0) and step.summary and step.summary.strip():
                details.append(step.summary.strip())
        if details:
            return details
    if not job.output_dataset_id:
        return []
    try:
        samples = samples_client.list(job.output_dataset_id, limit=10)
    except Exception:
        return []
    seen: set[str] = set()
    for sample in samples:
        msg = None
        if not isinstance(sample.meta, Unset) and sample.meta is not None and "error_message" in sample.meta:
            msg = sample.meta["error_message"]
        elif "error_message" in sample.additional_properties:
            msg = sample.additional_properties["error_message"]
        if msg and isinstance(msg, str) and msg.strip() and msg not in seen:
            seen.add(msg)
            details.append(msg.strip())
    return details


class TransformJobsClient:
    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get(self, job_id: str) -> TransformJob:
        response = get_transform_job_transform_jobs_job_id_get.sync_detailed(
            job_id=job_id,
            client=self._client,
        )
        return handle_response_error(response, "get transform job")

    def get_metrics(self, job_id: str) -> Optional[PipelineMetricsResponse]:
        """Fetch pipeline metrics. Returns None if not yet available (404) or on error."""
        response = get_transform_job_metrics_transform_jobs_job_id_metrics_get.sync_detailed(
            job_id=job_id,
            client=self._client,
        )
        if isinstance(response.parsed, PipelineMetricsResponse):
            return response.parsed
        return None

    def list(
        self,
        *,
        limit: int = 10,
        cursor: Optional[str] = None,
        status: Optional[TransformJobStatus] = None,
        configuration_id: Optional[str] = None,
    ) -> ListTransformJobsResponse:
        response = list_transform_jobs_transform_jobs_get.sync_detailed(
            client=self._client,
            limit=limit,
            cursor=cursor if cursor is not None else UNSET,
            status=status if status is not None else UNSET,
            configuration_id=configuration_id if configuration_id is not None else UNSET,
        )
        return handle_response_error(response, "list transform jobs")


class TransformsClient:
    def __init__(self, client: AuthenticatedClient, dataset_samples_client: DatasetSamplesClient):
        self._client: AuthenticatedClient = client
        self._dataset_samples_client: DatasetSamplesClient = dataset_samples_client
        self.jobs = TransformJobsClient(client)
    
    def run(
        self,
        config: TransformConfig,
        input_dataset: Optional[Union[SampleDataset, str]] = None,
        max_questions: Optional[int] = None,
        max_cost_dollars: Optional[float] = None,
        name: Optional[str] = None,
        # If True, will not stop the app if the local process dies or disconnects
        detach: bool = False,
    ) -> SampleDataset:
        job: TransformJob = self.submit(config, input_dataset, max_questions, max_cost_dollars, name)

        # Save the warning message before polling overwrites the job object
        warning_message = job.warning_message if (not isinstance(job.warning_message, Unset) and job.warning_message is not None) else None

        def poll() -> tuple[PipelineMetricsResponse, TransformJob]:
            nonlocal job
            job = self.jobs.get(job.id)
            metrics = self.jobs.get_metrics(job.id)
            return metrics, job

        try:
            run_live_display(poll, poll_interval=15, warning_message=warning_message)
        except KeyboardInterrupt:
            if not detach:
                try:
                    cancel_response = cancel_transform_job_transform_jobs_job_id_delete.sync_detailed(
                        job_id=job.id,
                        client=self._client,
                    )
                    handle_response_error(cancel_response, "cancel transform job")
                    print(f"Transform job {job.id} cancelled.")
                except Exception as e:
                    print(f"Failed to cancel transform job {job.id}: {e}")
            
            raise KeyboardInterrupt("Transform job interrupted by user")

        if job.status == TransformJobStatus.FAILED:
            error_msg = job.error_message if (not isinstance(job.error_message, Unset) and job.error_message) else "Unknown error"
            error_details = _fetch_error_details_from_samples(
                job, self._dataset_samples_client, self.jobs
            )
            display_error(error_msg, title="Job Failed", job=job, error_details=error_details)

            # No need to raise an exception in the notebook, as we display the error using display_error
            if not _is_notebook():
                raise Exception(f"Transform job {job.id} failed: {error_msg}")

        if job.status == TransformJobStatus.COMPLETED:
            if job.output_dataset_id is None:
                raise Exception(f"Transform job {job.id} completed but has no output dataset")
            
            dataset_response = get_dataset_datasets_dataset_id_get.sync_detailed(
                dataset_id=job.output_dataset_id,
                client=self._client,
            )
            dataset_result = handle_response_error(dataset_response, "get dataset")
            
            return SampleDataset(
                id=dataset_result.id,
                num_rows=dataset_result.num_rows,
                datasets_client=self._dataset_samples_client
            )
        
        raise Exception(f"Unexpected job status: {job.status}")
    
    def submit(
        self,
        config: TransformConfig,
        input_dataset: Optional[Union[SampleDataset, str]] = None,
        max_questions: Optional[int] = None,
        max_cost_dollars: Optional[float] = None,
        name: Optional[str] = None,
    ) -> TransformJob:
        dataset_id: Optional[str] = None
        if isinstance(input_dataset, SampleDataset):
            dataset_id = input_dataset.id
        elif isinstance(input_dataset, str):
            dataset_id = input_dataset
        request: CreateTransformJobRequest = CreateTransformJobRequest(
            config=config,
            input_dataset_id=dataset_id,
            max_questions=max_questions,
            max_cost_dollars=max_cost_dollars,
            name=name,
        )
        
        response = create_transform_job_transform_jobs_post.sync_detailed(
            client=self._client,
            body=request,
        )

        job: TransformJob = handle_response_error(response, "submit transform job")

        if not isinstance(job.error_message, Unset) and job.error_message is not None:
            display_error(job.error_message, title="Error", job=job)
            raise Exception(f"Transform job {job.id} error: {job.error_message}")
        if not isinstance(job.warning_message, Unset) and job.warning_message is not None:
            display_warning(job.warning_message)

        return job

    def estimate_cost(self, config: TransformConfig, max_questions: Optional[int] = None) -> float:
        response = cost_estimation_transform_jobs_cost_estimation_post.sync_detailed(
            client=self._client,
            body=EstimateCostRequest(
                config=config,
                max_questions=max_questions,
            ),
        )
        parsed: EstimateCostResponse = handle_response_error(response, "estimate cost")
        return parsed.total_cost_dollars