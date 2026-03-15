from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.training_job_list_response import TrainingJobListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: int | Unset = 1,
    limit: int | Unset = 10,
    status: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    else:
        json_status = status
    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/training-jobs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TrainingJobListResponse | None:
    if response.status_code == 200:
        response_200 = TrainingJobListResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | TrainingJobListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 10,
    status: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | TrainingJobListResponse]:
    """List Training Jobs

     List training jobs

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 10.
        status (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TrainingJobListResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 10,
    status: None | str | Unset = UNSET,
) -> HTTPValidationError | TrainingJobListResponse | None:
    """List Training Jobs

     List training jobs

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 10.
        status (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TrainingJobListResponse
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 10,
    status: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | TrainingJobListResponse]:
    """List Training Jobs

     List training jobs

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 10.
        status (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TrainingJobListResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 10,
    status: None | str | Unset = UNSET,
) -> HTTPValidationError | TrainingJobListResponse | None:
    """List Training Jobs

     List training jobs

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 10.
        status (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TrainingJobListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            status=status,
        )
    ).parsed
