from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_dataset_linter_runs_response import ListDatasetLinterRunsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str,
    *,
    limit: int | Unset = 20,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/dataset-linter/datasets/{dataset_id}/linter-runs".format(
            dataset_id=quote(str(dataset_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListDatasetLinterRunsResponse | None:
    if response.status_code == 200:
        response_200 = ListDatasetLinterRunsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ListDatasetLinterRunsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | ListDatasetLinterRunsResponse]:
    """List Runs For Dataset

     List past linter runs for a dataset

    Args:
        dataset_id (str):
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListDatasetLinterRunsResponse]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> HTTPValidationError | ListDatasetLinterRunsResponse | None:
    """List Runs For Dataset

     List past linter runs for a dataset

    Args:
        dataset_id (str):
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListDatasetLinterRunsResponse
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | ListDatasetLinterRunsResponse]:
    """List Runs For Dataset

     List past linter runs for a dataset

    Args:
        dataset_id (str):
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListDatasetLinterRunsResponse]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> HTTPValidationError | ListDatasetLinterRunsResponse | None:
    """List Runs For Dataset

     List past linter runs for a dataset

    Args:
        dataset_id (str):
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListDatasetLinterRunsResponse
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
            limit=limit,
        )
    ).parsed
