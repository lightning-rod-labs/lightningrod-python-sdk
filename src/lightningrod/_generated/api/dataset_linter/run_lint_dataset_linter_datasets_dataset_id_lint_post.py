from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_linter_run_request import DatasetLinterRunRequest
from ...models.dataset_linter_run_response import DatasetLinterRunResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str,
    *,
    body: DatasetLinterRunRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/dataset-linter/datasets/{dataset_id}/lint".format(
            dataset_id=quote(str(dataset_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DatasetLinterRunResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DatasetLinterRunResponse.from_dict(response.json())

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
) -> Response[DatasetLinterRunResponse | HTTPValidationError]:
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
    body: DatasetLinterRunRequest | Unset = UNSET,
) -> Response[DatasetLinterRunResponse | HTTPValidationError]:
    """Run Lint

     Run the dataset linter synchronously and return its results

    Args:
        dataset_id (str):
        body (DatasetLinterRunRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetLinterRunResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: DatasetLinterRunRequest | Unset = UNSET,
) -> DatasetLinterRunResponse | HTTPValidationError | None:
    """Run Lint

     Run the dataset linter synchronously and return its results

    Args:
        dataset_id (str):
        body (DatasetLinterRunRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetLinterRunResponse | HTTPValidationError
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: DatasetLinterRunRequest | Unset = UNSET,
) -> Response[DatasetLinterRunResponse | HTTPValidationError]:
    """Run Lint

     Run the dataset linter synchronously and return its results

    Args:
        dataset_id (str):
        body (DatasetLinterRunRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetLinterRunResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient,
    body: DatasetLinterRunRequest | Unset = UNSET,
) -> DatasetLinterRunResponse | HTTPValidationError | None:
    """Run Lint

     Run the dataset linter synchronously and return its results

    Args:
        dataset_id (str):
        body (DatasetLinterRunRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetLinterRunResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
            body=body,
        )
    ).parsed
