from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_file_set_file_request import CreateFileSetFileRequest
from ...models.file_set_file import FileSetFile
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    file_set_id: str,
    *,
    body: CreateFileSetFileRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/filesets/{file_set_id}/files",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FileSetFile | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = FileSetFile.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[FileSetFile | HTTPValidationError]:
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
    body: CreateFileSetFileRequest,
) -> Response[FileSetFile | HTTPValidationError]:
    """Add File To Set

     Add a file to a FileSet by providing file information and metadata.

    Args:
        file_set_id (str):
        body (CreateFileSetFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileSetFile | HTTPValidationError]
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
    body: CreateFileSetFileRequest,
) -> FileSetFile | HTTPValidationError | None:
    """Add File To Set

     Add a file to a FileSet by providing file information and metadata.

    Args:
        file_set_id (str):
        body (CreateFileSetFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileSetFile | HTTPValidationError
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
    body: CreateFileSetFileRequest,
) -> Response[FileSetFile | HTTPValidationError]:
    """Add File To Set

     Add a file to a FileSet by providing file information and metadata.

    Args:
        file_set_id (str):
        body (CreateFileSetFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileSetFile | HTTPValidationError]
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
    body: CreateFileSetFileRequest,
) -> FileSetFile | HTTPValidationError | None:
    """Add File To Set

     Add a file to a FileSet by providing file information and metadata.

    Args:
        file_set_id (str):
        body (CreateFileSetFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileSetFile | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            file_set_id=file_set_id,
            client=client,
            body=body,
        )
    ).parsed
