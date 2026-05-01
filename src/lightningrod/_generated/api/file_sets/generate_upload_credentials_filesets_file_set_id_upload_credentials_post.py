from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.upload_credentials_response import UploadCredentialsResponse
from ...types import Response


def _get_kwargs(
    file_set_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/filesets/{file_set_id}/upload-credentials".format(
            file_set_id=quote(str(file_set_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UploadCredentialsResponse | None:
    if response.status_code == 200:
        response_200 = UploadCredentialsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | UploadCredentialsResponse]:
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
) -> Response[HTTPValidationError | UploadCredentialsResponse]:
    """Generate Upload Credentials

     Generate short-lived, write-only credentials for uploading files via GCS Transfer Manager.

    Returns an OAuth2 token scoped to only create objects in this fileset's folder.

    Args:
        file_set_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UploadCredentialsResponse]
    """

    kwargs = _get_kwargs(
        file_set_id=file_set_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | UploadCredentialsResponse | None:
    """Generate Upload Credentials

     Generate short-lived, write-only credentials for uploading files via GCS Transfer Manager.

    Returns an OAuth2 token scoped to only create objects in this fileset's folder.

    Args:
        file_set_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UploadCredentialsResponse
    """

    return sync_detailed(
        file_set_id=file_set_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | UploadCredentialsResponse]:
    """Generate Upload Credentials

     Generate short-lived, write-only credentials for uploading files via GCS Transfer Manager.

    Returns an OAuth2 token scoped to only create objects in this fileset's folder.

    Args:
        file_set_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UploadCredentialsResponse]
    """

    kwargs = _get_kwargs(
        file_set_id=file_set_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    file_set_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | UploadCredentialsResponse | None:
    """Generate Upload Credentials

     Generate short-lived, write-only credentials for uploading files via GCS Transfer Manager.

    Returns an OAuth2 token scoped to only create objects in this fileset's folder.

    Args:
        file_set_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UploadCredentialsResponse
    """

    return (
        await asyncio_detailed(
            file_set_id=file_set_id,
            client=client,
        )
    ).parsed
