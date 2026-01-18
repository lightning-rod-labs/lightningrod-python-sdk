from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_file_set_files_response import ListFileSetFilesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    file_set_id: str,
    *,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/filesets/{file_set_id}/files",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListFileSetFilesResponse | None:
    if response.status_code == 200:
        response_200 = ListFileSetFilesResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListFileSetFilesResponse]:
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
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListFileSetFilesResponse]:
    """List Files In Set

     List all files in a FileSet.

    Args:
        file_set_id (str):
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListFileSetFilesResponse]
    """

    kwargs = _get_kwargs(
        file_set_id=file_set_id,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
) -> HTTPValidationError | ListFileSetFilesResponse | None:
    """List Files In Set

     List all files in a FileSet.

    Args:
        file_set_id (str):
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListFileSetFilesResponse
    """

    return sync_detailed(
        file_set_id=file_set_id,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListFileSetFilesResponse]:
    """List Files In Set

     List all files in a FileSet.

    Args:
        file_set_id (str):
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListFileSetFilesResponse]
    """

    kwargs = _get_kwargs(
        file_set_id=file_set_id,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: None | str | Unset = UNSET,
) -> HTTPValidationError | ListFileSetFilesResponse | None:
    """List Files In Set

     List all files in a FileSet.

    Args:
        file_set_id (str):
        limit (int | Unset):  Default: 10.
        cursor (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListFileSetFilesResponse
    """

    return (
        await asyncio_detailed(
            file_set_id=file_set_id,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
