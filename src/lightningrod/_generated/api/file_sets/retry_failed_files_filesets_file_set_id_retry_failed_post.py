from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.retry_failed_files_request import RetryFailedFilesRequest
from ...models.retry_failed_files_response import RetryFailedFilesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    file_set_id: str,
    *,
    body: RetryFailedFilesRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/filesets/{file_set_id}/retry-failed".format(
            file_set_id=quote(str(file_set_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RetryFailedFilesResponse | None:
    if response.status_code == 200:
        response_200 = RetryFailedFilesResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | RetryFailedFilesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
    body: RetryFailedFilesRequest | Unset = UNSET,
) -> Response[HTTPValidationError | RetryFailedFilesResponse]:
    """Retry Failed Files

     Retry all failed files in a FileSet.

    Args:
        file_set_id (str):
        body (RetryFailedFilesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RetryFailedFilesResponse]
    """

    kwargs = _get_kwargs(
        file_set_id=file_set_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
    body: RetryFailedFilesRequest | Unset = UNSET,
) -> HTTPValidationError | RetryFailedFilesResponse | None:
    """Retry Failed Files

     Retry all failed files in a FileSet.

    Args:
        file_set_id (str):
        body (RetryFailedFilesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RetryFailedFilesResponse
    """

    return sync_detailed(
        file_set_id=file_set_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
    body: RetryFailedFilesRequest | Unset = UNSET,
) -> Response[HTTPValidationError | RetryFailedFilesResponse]:
    """Retry Failed Files

     Retry all failed files in a FileSet.

    Args:
        file_set_id (str):
        body (RetryFailedFilesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RetryFailedFilesResponse]
    """

    kwargs = _get_kwargs(
        file_set_id=file_set_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
    body: RetryFailedFilesRequest | Unset = UNSET,
) -> HTTPValidationError | RetryFailedFilesResponse | None:
    """Retry Failed Files

     Retry all failed files in a FileSet.

    Args:
        file_set_id (str):
        body (RetryFailedFilesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RetryFailedFilesResponse
    """

    return (
        await asyncio_detailed(
            file_set_id=file_set_id,
            client=client,
            body=body,
        )
    ).parsed
