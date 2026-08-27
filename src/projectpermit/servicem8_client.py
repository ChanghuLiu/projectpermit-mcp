"""Minimal read-only ServiceM8 REST transport.

The client supports the documented private-integration API-key path and exposes
GET operations only. It intentionally does not implement POST/DELETE mutations,
OAuth persistence, webhooks or customer/billing endpoints.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import quote

import httpx


SERVICEM8_API_BASE = "https://api.servicem8.com/api_1.0"


@dataclass(frozen=True)
class ServiceM8ClientError(RuntimeError):
    message: str

    def __str__(self) -> str:
        return self.message


class ServiceM8ReadOnlyClient:
    """Small GET-only client for a ServiceM8 private own-account validation."""

    def __init__(
        self,
        api_key: str,
        *,
        api_base: str = SERVICEM8_API_BASE,
        timeout_seconds: float = 20.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        key = str(api_key or "").strip()
        if not key:
            raise ServiceM8ClientError("ServiceM8 API key is required")
        base = str(api_base or "").strip().rstrip("/")
        if not base.startswith("https://"):
            raise ServiceM8ClientError("ServiceM8 API base must use HTTPS")

        self._api_key = key
        self._api_base = base
        self._client = httpx.Client(timeout=timeout_seconds, transport=transport)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "ServiceM8ReadOnlyClient":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def _get(self, resource: str, *, params: Mapping[str, Any] | None = None) -> Any:
        path = str(resource or "").strip().lstrip("/")
        if not path or ".." in path:
            raise ServiceM8ClientError("Invalid ServiceM8 resource path")

        response = self._client.get(
            f"{self._api_base}/{path}",
            headers={
                "X-API-Key": self._api_key,
                "Accept": "application/json",
            },
            params=dict(params or {}),
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # Do not echo the raw body or request headers; either can contain
            # sensitive account data and the request header contains the API key.
            raise ServiceM8ClientError(
                f"ServiceM8 HTTP request failed with status {response.status_code}"
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise ServiceM8ClientError("ServiceM8 returned a non-JSON response") from exc

    def get_job(self, job_uuid: str) -> Mapping[str, Any]:
        job_id = str(job_uuid or "").strip()
        if not job_id:
            raise ServiceM8ClientError("ServiceM8 Job uuid is required")
        encoded = quote(job_id, safe="")
        payload = self._get(f"job/{encoded}.json")
        if not isinstance(payload, Mapping):
            raise ServiceM8ClientError("ServiceM8 Job response was not an object")
        return payload

    def list_jobs(self, *, params: Mapping[str, Any] | None = None) -> list[Mapping[str, Any]]:
        payload = self._get("job.json", params=params)
        if not isinstance(payload, list):
            raise ServiceM8ClientError("ServiceM8 jobs response was not an array")
        return [item for item in payload if isinstance(item, Mapping)]

    def list_job_materials(
        self,
        *,
        params: Mapping[str, Any] | None = None,
    ) -> list[Mapping[str, Any]]:
        """List JobMaterial records using caller-supplied documented filters.

        The client deliberately does not invent a filter syntax. Pass only filter
        parameters verified against ServiceM8's live/current REST documentation.
        """
        payload = self._get("jobmaterial.json", params=params)
        if not isinstance(payload, list):
            raise ServiceM8ClientError("ServiceM8 job-material response was not an array")
        return [item for item in payload if isinstance(item, Mapping)]
