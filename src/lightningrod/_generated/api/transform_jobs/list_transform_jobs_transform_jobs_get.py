from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_transform_jobs_response import ListTransformJobsResponse
from ...models.transform_job_status import TransformJobStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
    status: None | TransformJobStatus | Unset = UNSET,
    configuration_id: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, TransformJobStatus):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    json_configuration_id: None | str | Unset
    if isinstance(configuration_id, Unset):
        json_configuration_id = UNSET
    else:
        json_configuration_id = configuration_id
    params["configuration_id"] = json_configuration_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/transform-jobs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListTransformJobsResponse | None:
    if response.status_code == 200:
        response_200 = ListTransformJobsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListTransformJobsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
    status: None | TransformJobStatus | Unset = UNSET,
    configuration_id: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListTransformJobsResponse]:
    """List Transform Jobs

     List transform jobs for the authenticated organization

    Args:
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):
        status (None | TransformJobStatus | Unset):
        configuration_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListTransformJobsResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
        configuration_id=configuration_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
    status: None | TransformJobStatus | Unset = UNSET,
    configuration_id: None | str | Unset = UNSET,
) -> HTTPValidationError | ListTransformJobsResponse | None:
    """List Transform Jobs

     List transform jobs for the authenticated organization

    Args:
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):
        status (None | TransformJobStatus | Unset):
        configuration_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListTransformJobsResponse
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        status=status,
        configuration_id=configuration_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
    status: None | TransformJobStatus | Unset = UNSET,
    configuration_id: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListTransformJobsResponse]:
    """List Transform Jobs

     List transform jobs for the authenticated organization

    Args:
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):
        status (None | TransformJobStatus | Unset):
        configuration_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListTransformJobsResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        status=status,
        configuration_id=configuration_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
    status: None | TransformJobStatus | Unset = UNSET,
    configuration_id: None | str | Unset = UNSET,
) -> HTTPValidationError | ListTransformJobsResponse | None:
    """List Transform Jobs

     List transform jobs for the authenticated organization

    Args:
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):
        status (None | TransformJobStatus | Unset):
        configuration_id (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListTransformJobsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            status=status,
            configuration_id=configuration_id,
        )
    ).parsed
