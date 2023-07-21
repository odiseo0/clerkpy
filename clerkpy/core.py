from __future__ import annotations
from typing import Any, Literal

from httpx import URL, AsyncClient, Response
from result import Ok, Err, Result

from .constants import URL_BASE, CONTENT_TYPE


class ClerkClient:
    """HTTP Client for `Clerk`"""

    def __init__(self, client: AsyncClient, secret: str, route: str) -> None:
        self.client = client
        self.secret = secret
        self.route = route

    async def request(
        self,
        method: Literal["GET", "POST", "PATCH", "PUT"],
        path: str,
        params: dict[str, Any] | None = {},
        data: Any = None,
        content_type: str | None = None,
    ) -> Result[Ok[Response], Err[dict[str, Any]]]:
        url = URL(
            f"{URL_BASE}/{self.route}/{path}",
            params=[(k, v) for k, v in sorted(params.items())],
        )
        response = await self.client.request(
            method,
            url,
            content=data,
            headers={
                "authorization": f"Bearer {self.secret}",
                "content-type": content_type or CONTENT_TYPE,
                "user-agent": "Clerkpy API Wrapper",
            },
        )

        if response.status_code >= 400:
            return Err(
                {
                    "detail": response.text,
                    "status_code": response.status_code,
                    "headers": response.headers,
                }
            )

        return Ok(response)

    async def get(self, path: str = "", params: dict[str, Any] | None = {}) -> Response:
        result = await self.request("GET", path, params)

        if isinstance(result, Err):
            return result.err_value

        return result.ok_value

    async def post(
        self,
        path: str = "",
        params: dict[str, Any] | None = {},
        content: Any = None,
        content_type: str | None = None,
    ):
        result = await self.request("POST", path, params, content, content_type)

        if isinstance(result, Err):
            return result.err_value

        return result.ok_value

    async def patch(
        self,
        path: str = "",
        params: dict[str, Any] | None = {},
        content: Any = None,
        content_type: str | None = None,
    ):
        result = await self.request("PATCH", path, params, content, content_type)

        if isinstance(result, Err):
            return result.err_value

        return result.ok_value

    async def put(
        self,
        path: str = "",
        params: dict[str, Any] | None = {},
        content: Any = None,
        content_type: str | None = None,
    ):
        result = await self.request("PUT", path, params, content, content_type)

        if isinstance(result, Err):
            return result.err_value

        return result.ok_value
