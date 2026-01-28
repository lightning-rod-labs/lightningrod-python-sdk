from lightningrod._generated.api.organizations import get_balance_organizations_balance_get
from lightningrod._generated.client import AuthenticatedClient
from lightningrod._generated.models.balance_response import BalanceResponse
from lightningrod._errors import handle_response_error


class OrganizationsClient:

    def __init__(self, client: AuthenticatedClient):
        self._client = client

    def get_balance(self) -> float:
        response = get_balance_organizations_balance_get.sync_detailed(
            client=self._client,
        )
        parsed: BalanceResponse = handle_response_error(response, "get balance")
        return parsed.balance_dollars
