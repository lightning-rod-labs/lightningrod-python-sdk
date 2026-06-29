from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.mpp_topup_response import MppTopupResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    amount_cents: int | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_amount_cents: int | None | Unset
    if isinstance(amount_cents, Unset):
        json_amount_cents = UNSET
    else:
        json_amount_cents = amount_cents
    params["amount_cents"] = json_amount_cents

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/mpp/topup",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | MppTopupResponse | None:
    if response.status_code == 200:
        response_200 = MppTopupResponse.from_dict(response.json())

        return response_200

    if response.status_code == 402:
        response_402 = cast(Any, None)
        return response_402

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError | MppTopupResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    amount_cents: int | None | Unset = UNSET,
) -> Response[Any | HTTPValidationError | MppTopupResponse]:
    """Add credits via MPP (Machine Payments Protocol)

     Pay via MPP to add credits and obtain (or refresh) an API key, then call the standard `/openai/*`
    endpoints with it as a `Bearer` token.

    **Flow:** call with no payment → `402` + `WWW-Authenticate: Payment` challenge (quotes the top-up
    amount, payable via card/Link Shared Payment Token) → pay → retry with `Authorization: Payment
    <credential>`.

    **Amount:** defaults to 500 cents ($5.00); pass `amount_cents` to choose a size (clamped to the
    credit-purchase limits). Send the **same** `amount_cents` on the paid retry as on the challenge
    call.

    **Headers:**
    - `Authorization: Payment <credential>` — the MPP payment credential.
    - `X-API-Key: sk_…` *(optional)* — refill an existing org; omit to mint a new org + key (returned
    once in the response body).

    Beta.

    Args:
        amount_cents (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | MppTopupResponse]
    """

    kwargs = _get_kwargs(
        amount_cents=amount_cents,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    amount_cents: int | None | Unset = UNSET,
) -> Any | HTTPValidationError | MppTopupResponse | None:
    """Add credits via MPP (Machine Payments Protocol)

     Pay via MPP to add credits and obtain (or refresh) an API key, then call the standard `/openai/*`
    endpoints with it as a `Bearer` token.

    **Flow:** call with no payment → `402` + `WWW-Authenticate: Payment` challenge (quotes the top-up
    amount, payable via card/Link Shared Payment Token) → pay → retry with `Authorization: Payment
    <credential>`.

    **Amount:** defaults to 500 cents ($5.00); pass `amount_cents` to choose a size (clamped to the
    credit-purchase limits). Send the **same** `amount_cents` on the paid retry as on the challenge
    call.

    **Headers:**
    - `Authorization: Payment <credential>` — the MPP payment credential.
    - `X-API-Key: sk_…` *(optional)* — refill an existing org; omit to mint a new org + key (returned
    once in the response body).

    Beta.

    Args:
        amount_cents (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | MppTopupResponse
    """

    return sync_detailed(
        client=client,
        amount_cents=amount_cents,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    amount_cents: int | None | Unset = UNSET,
) -> Response[Any | HTTPValidationError | MppTopupResponse]:
    """Add credits via MPP (Machine Payments Protocol)

     Pay via MPP to add credits and obtain (or refresh) an API key, then call the standard `/openai/*`
    endpoints with it as a `Bearer` token.

    **Flow:** call with no payment → `402` + `WWW-Authenticate: Payment` challenge (quotes the top-up
    amount, payable via card/Link Shared Payment Token) → pay → retry with `Authorization: Payment
    <credential>`.

    **Amount:** defaults to 500 cents ($5.00); pass `amount_cents` to choose a size (clamped to the
    credit-purchase limits). Send the **same** `amount_cents` on the paid retry as on the challenge
    call.

    **Headers:**
    - `Authorization: Payment <credential>` — the MPP payment credential.
    - `X-API-Key: sk_…` *(optional)* — refill an existing org; omit to mint a new org + key (returned
    once in the response body).

    Beta.

    Args:
        amount_cents (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | MppTopupResponse]
    """

    kwargs = _get_kwargs(
        amount_cents=amount_cents,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    amount_cents: int | None | Unset = UNSET,
) -> Any | HTTPValidationError | MppTopupResponse | None:
    """Add credits via MPP (Machine Payments Protocol)

     Pay via MPP to add credits and obtain (or refresh) an API key, then call the standard `/openai/*`
    endpoints with it as a `Bearer` token.

    **Flow:** call with no payment → `402` + `WWW-Authenticate: Payment` challenge (quotes the top-up
    amount, payable via card/Link Shared Payment Token) → pay → retry with `Authorization: Payment
    <credential>`.

    **Amount:** defaults to 500 cents ($5.00); pass `amount_cents` to choose a size (clamped to the
    credit-purchase limits). Send the **same** `amount_cents` on the paid retry as on the challenge
    call.

    **Headers:**
    - `Authorization: Payment <credential>` — the MPP payment credential.
    - `X-API-Key: sk_…` *(optional)* — refill an existing org; omit to mint a new org + key (returned
    once in the response body).

    Beta.

    Args:
        amount_cents (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | MppTopupResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            amount_cents=amount_cents,
        )
    ).parsed
