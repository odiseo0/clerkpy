from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, AsyncIterable, Literal, TypedDict

from .core import ClerkClient

if TYPE_CHECKING:
    from httpx import AsyncClient


# doc endpoint: https://clerk.com/docs/reference/backend-api/tag/Users
# TODO: Move to another file
class Error(TypedDict):
    message: str
    long_message: str
    code: str
    meta: dict
    clerk_trace_id: str


class Verification(TypedDict):
    status: str
    strategy: str
    attempts: int
    expire_at: int
    external_verification_redirect_url: str | None
    error: Error


class EmailAddress(TypedDict):
    id: str
    object: Literal["email_address"]
    email_address: str
    reserved: bool
    verification: Verification | None
    linked_to: list | list[dict[str, Any]]


class PhoneNumber(TypedDict):
    id: str
    object: Literal["phone_number"]
    phone_number: str
    reserved_for_second_factor: bool
    default_second_factor: bool
    reserved: bool
    verification: Verification | None
    linked_to: list | list[dict[str, Any]]
    backup_code: list | list[str]


class Web3Wallet(TypedDict):
    id: str
    object: Literal["web3_wallet"]
    verification: Verification | None


class SAMLAccount(TypedDict):
    id: str
    object: Literal["saml_account"]
    provider: str
    active: bool
    email_address: str
    first_name: str | None
    last_name: str | None
    provider_user_id: str
    verification: Verification | None


@dataclass
class User:
    id: str
    object: Literal["user"]
    external_id: str | None
    primary_email_address_id: str
    primary_phone_number_id: str | None
    primary_web3_wallet_id: str | None
    username: str | None
    first_name: str | None
    last_name: str | None
    profile_image_url: str
    image_url: str
    public_metadata: dict
    private_metadata: dict
    unsafe_metadata: dict
    gender: str | None
    birthday: str | None
    email_addresses: list | list[dict]
    phone_numbers: list | list[PhoneNumber]
    web3_wallets: list | list[Web3Wallet]
    password_enabled: bool
    two_factor_enabled: bool
    totp_enabled: bool
    backup_code_enabled: bool
    external_accounts: list
    saml_accounts: list | list[SAMLAccount]
    last_sign_in_at: 0
    banned: bool
    updated_at: 0
    created_at: 0
    delete_self_enabled: bool
    create_organization_enabled: bool


class UserClient:
    def __init__(self, http_client: AsyncClient, secret: str) -> None:
        self.client = ClerkClient(http_client, secret, "users")

    # TODO: Add type hint for `params`.
    async def list(self, params: dict[str, Any] = {}) -> AsyncIterable[User]:
        """
        List of all users. The users are returned sorted by creation date, with the newest users appearing first.

        Reference: https://clerk.com/docs/reference/backend-api/tag/Users#operation/GetUserList
        """
        users = await self.client.get(params=params)

        for user in users.json():
            yield User(**user)

    async def create(self):
        return

    async def create_many(self):
        return
