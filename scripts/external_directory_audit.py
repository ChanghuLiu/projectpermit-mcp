"""Read-only visibility audit across public ProjectPermit discovery directories.

This script never submits a listing, sends credentials, or sends x402 payment headers. Provider
errors are reported as observations rather than treated as CI failures so a temporary directory
outage cannot block ProjectPermit development.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
HOST = "projectpermit-api-v2-production.up.railway.app"
FREE_MCP = "https://projectpermit-mcp-production.up.railway.app/mcp"
INDEX_402_SERVICE_ID = "df86c16c-4c30-48d7-9c9d-6de53d782de3"
USER_AGENT = "ProjectPermit-External-Directory-Audit/1.0"


def _get_text(url: str) -> tuple[int, str, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        with urlopen(request, timeout=25) as response:
            return response.status, response.headers.get("Content-Type", ""), response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, exc.headers.get("Content-Type", ""), body


def _get_json(url: str) -> tuple[int, Any]:
    status, _, text = _get_text(url)
    try:
        return status, json.loads(text)
    except json.JSONDecodeError:
        return status, {"non_json_body": text[:1000]}


def _contains_projectpermit(payload: Any) -> bool:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False).lower()
    return HOST in serialized or FREE_MCP.lower() in serialized or "projectpermit" in serialized


def _safe_get_json(url: str) -> dict[str, Any]:
    try:
        status, payload = _get_json(url)
        return {"http_status": status, "payload": payload}
    except (URLError, TimeoutError, OSError) as exc:
        return {"error": type(exc).__name__, "detail": str(exc)[:500]}


def _audit_402index() -> dict[str, Any]:
    detail_url = f"https://402index.io/api/v1/services/{INDEX_402_SERVICE_ID}"
    search_url = "https://402index.io/api/v1/services?" + urlencode(
        {"q": "ProjectPermit", "limit": 100}
    )
    detail = _safe_get_json(detail_url)
    search = _safe_get_json(search_url)
    result: dict[str, Any] = {
        "service_id": INDEX_402_SERVICE_ID,
        "detail_http_status": detail.get("http_status"),
        "search_http_status": search.get("http_status"),
        "public_search_visible": _contains_projectpermit(search.get("payload", {})),
    }
    detail_payload = detail.get("payload")
    if isinstance(detail_payload, dict):
        service = detail_payload.get("service") if isinstance(detail_payload.get("service"), dict) else detail_payload
        for field in (
            "status",
            "name",
            "url",
            "health_status",
            "verified",
            "domain_verified",
            "source",
            "price_usd",
            "payment_asset",
            "payment_network",
        ):
            if field in service:
                result[field] = service[field]
    if "error" in detail:
        result["detail_error"] = detail
    if "error" in search:
        result["search_error"] = search
    return result


def _audit_open402() -> dict[str, Any]:
    url = "https://raw.githubusercontent.com/ArcedeDev/open-402/main/registry/domains.txt"
    try:
        status, _, text = _get_text(url)
    except (URLError, TimeoutError, OSError) as exc:
        return {"error": type(exc).__name__, "detail": str(exc)[:500]}
    matching = [line.strip() for line in text.splitlines() if HOST in line.lower()]
    return {
        "http_status": status,
        "listed": bool(matching),
        "matching_lines": matching[:5],
    }


def _agent_tools_search(path: str) -> dict[str, Any]:
    url = f"https://agent-tools.cloud{path}?" + urlencode(
        {"q": "ProjectPermit", "limit": 100}
    )
    response = _safe_get_json(url)
    payload = response.get("payload", {})
    result = {
        "http_status": response.get("http_status"),
        "listed": _contains_projectpermit(payload),
    }
    if isinstance(payload, dict):
        if "count" in payload:
            result["result_count"] = payload["count"]
        for key in ("services", "servers", "results", "resources"):
            rows = payload.get(key)
            if isinstance(rows, list):
                matches = [row for row in rows if _contains_projectpermit(row)]
                result["matches"] = matches[:3]
                break
    if "error" in response:
        result["error"] = response
    return result


def main() -> None:
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "projectpermit_origin": ORIGIN,
        "402index": _audit_402index(),
        "open402": _audit_open402(),
        "agent_tools_x402": _agent_tools_search("/api/v1/search"),
        "agent_tools_mcp": _agent_tools_search("/api/v1/mcp/search"),
        "safety": {
            "read_only": True,
            "listing_submission_performed": False,
            "payment_headers_sent": False,
            "credentials_sent": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
