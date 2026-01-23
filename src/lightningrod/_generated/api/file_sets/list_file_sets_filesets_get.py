from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_file_sets_response import ListFileSetsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_public: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_public"] = include_public

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/filesets/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListFileSetsResponse | None:
    if response.status_code == 200:
        response_200 = ListFileSetsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListFileSetsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    include_public: bool | Unset = False,
) -> Response[HTTPValidationError | ListFileSetsResponse]:
    """List File Sets

     List all FileSets for the organization, optionally including public filesets.

    Args:
        include_public (bool | Unset): Include public filesets Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListFileSetsResponse]
    """

    kwargs = _get_kwargs(
        include_public=include_public,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    include_public: bool | Unset = False,
) -> HTTPValidationError | ListFileSetsResponse | None:
    """List File Sets

     List all FileSets for the organization, optionally including public filesets.

    Args:
        include_public (bool | Unset): Include public filesets Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListFileSetsResponse
    """

    return sync_detailed(
        client=client,
        include_public=include_public,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    include_public: bool | Unset = False,
) -> Response[HTTPValidationError | ListFileSetsResponse]:
    """List File Sets

     List all FileSets for the organization, optionally including public filesets.

    Args:
        include_public (bool | Unset): Include public filesets Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListFileSetsResponse]
    """

    kwargs = _get_kwargs(
        include_public=include_public,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    include_public: bool | Unset = False,
) -> HTTPValidationError | ListFileSetsResponse | None:
    """List File Sets

     List all FileSets for the organization, optionally including public filesets.

    Args:
        include_public (bool | Unset): Include public filesets Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListFileSetsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            include_public=include_public,
        )
    ).parsed
