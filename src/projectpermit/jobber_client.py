"""Minimal read-only Jobber GraphQL transport.

This module intentionally stops below OAuth persistence and below Jobber mutations.
It is safe to use with a Developer Center testing token once a ProjectPermit Jobber
app/test account exists.

Official Jobber API properties verified 2026-08-27:
- endpoint: https://api.getjobber.com/api/graphql
- OAuth 2.0 Bearer access tokens
- required X-JOBBER-GRAPHQL-VERSION header
- latest active version in the public changelog: 2025-04-16

The higher-level payload normalization remains in ``jobber_adapter.py``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import httpx


JOBBER_GRAPHQL_ENDPOINT = "https://api.getjobber.com/api/graphql"
JOBBER_API_VERSION = "2025-04-16"


@dataclass(frozen=True)
class JobberClientError(RuntimeError):
    message: str

    def __str__(self) -> str:
        return self.message


@dataclass(frozen=True)
class JobberGraphQLResponse:
    data: Mapping[str, Any]
    extensions: Mapping[str, Any]


class JobberReadOnlyClient:
    """Small query-only client for Jobber Developer Center validation.

    Mutations and subscriptions are rejected locally before network I/O.  This is
    deliberate: ProjectPermit's current Jobber milestone is read-only E3/E4
    validation, not write-back.
    """

    def __init__(
        self,
        access_token: str,
        *,
        api_version: str = JOBBER_API_VERSION,
        endpoint: str = JOBBER_GRAPHQL_ENDPOINT,
        timeout_seconds: float = 20.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        token = str(access_token or "").strip()
        if not token:
            raise JobberClientError("Jobber access token is required")
        version = str(api_version or "").strip()
        if not version:
            raise JobberClientError("Jobber API version is required")

        self._access_token = token
        self._api_version = version
        self._endpoint = endpoint
        self._client = httpx.Client(timeout=timeout_seconds, transport=transport)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "JobberReadOnlyClient":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    @staticmethod
    def _validate_query_only(query: str) -> str:
        text = str(query or "").strip()
        if not text:
            raise JobberClientError("GraphQL query is required")

        lowered = text.lower()
        # Conservative by design.  Even a mention in a GraphQL comment is rejected;
        # the validation client should contain only query operations.
        if "mutation" in lowered:
            raise JobberClientError("Jobber mutations are disabled in read-only validation mode")
        if "subscription" in lowered:
            raise JobberClientError("Jobber subscriptions are disabled in read-only validation mode")
        return text

    def execute(
        self,
        query: str,
        *,
        variables: Mapping[str, Any] | None = None,
    ) -> JobberGraphQLResponse:
        query_text = self._validate_query_only(query)
        payload: dict[str, Any] = {"query": query_text}
        if variables is not None:
            payload["variables"] = dict(variables)

        response = self._client.post(
            self._endpoint,
            headers={
                "Authorization": f"Bearer {self._access_token}",
                "X-JOBBER-GRAPHQL-VERSION": self._api_version,
                "Content-Type": "application/json",
            },
            json=payload,
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # Do not include response bodies or token-bearing request headers in the
            # exception: validation failures can be diagnosed from status + Jobber's
            # GraphQL error path after authentication succeeds.
            raise JobberClientError(f"Jobber HTTP request failed with status {response.status_code}") from exc

        try:
            decoded = response.json()
        except ValueError as exc:
            raise JobberClientError("Jobber returned a non-JSON response") from exc

        if not isinstance(decoded, Mapping):
            raise JobberClientError("Jobber returned an invalid GraphQL response envelope")

        errors = decoded.get("errors")
        if isinstance(errors, list) and errors:
            messages = []
            for item in errors:
                if isinstance(item, Mapping) and item.get("message"):
                    messages.append(str(item["message"]))
            summary = "; ".join(messages[:3]) or "unspecified GraphQL error"
            raise JobberClientError(f"Jobber GraphQL query failed: {summary}")

        data = decoded.get("data")
        if not isinstance(data, Mapping):
            raise JobberClientError("Jobber GraphQL response did not include a data object")

        extensions = decoded.get("extensions")
        if not isinstance(extensions, Mapping):
            extensions = {}
        return JobberGraphQLResponse(data=data, extensions=extensions)

    def get_account(self) -> Mapping[str, Any]:
        """Run Jobber's documented scope-independent account sanity query."""
        result = self.execute(
            """query GetAccount {
  account {
    id
    name
  }
}"""
        )
        account = result.data.get("account")
        if not isinstance(account, Mapping):
            raise JobberClientError("Jobber account query returned no account")
        return account
