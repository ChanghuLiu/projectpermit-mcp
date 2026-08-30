"""Read-only visibility audit across public ProjectPermit discovery directories.

This script never submits a listing, sends credentials, or sends x402 payment headers. Provider
errors are reported as observations rather than treated as CI failures so a temporary directory
outage cannot block ProjectPermit development.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


ORIGIN = "https://projectpermit-api-v2-production.up.railway.app"
HOST = "projectpermit-api-v2-production.up.railway.app"
FREE_MCP = "https://projectpermit-mcp-production.up.railway.app/mcp"
OFFICIAL_MCP_NAME = "io.github.ChanghuLiu/projectpermit"
EXPECTED_MCP_VERSION = "0.4.1"
EXPECTED_SINGLE_PRICE_USD = Decimal("0.20")
INDEX_402_SERVICE_ID = "df86c16c-4c30-48d7-9c9d-6de53d782de3"
TRUE402_SERVICE_ID = "1f2f751a-bc3c-4f09-8099-20a976650d7c"
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


def _normalized_price(value: Any) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    rendered = str(value).strip()
    if rendered.startswith("$"):
        rendered = rendered[1:]
    try:
        return Decimal(rendered)
    except (InvalidOperation, ValueError):
        return None


def _price_contract_match(value: Any) -> bool | None:
    normalized = _normalized_price(value)
    if normalized is None:
        return None
    return normalized == EXPECTED_SINGLE_PRICE_USD


def _manifest_price(payload: Any) -> Any:
    manifest = payload
    if isinstance(manifest, str):
        try:
            manifest = json.loads(manifest)
        except json.JSONDecodeError:
            return None
    if not isinstance(manifest, dict):
        return None
    for key in ("request_price_usd", "price_usd"):
        if manifest.get(key) is not None:
            return manifest[key]
    pricing = manifest.get("pricing")
    if isinstance(pricing, dict):
        for key in ("base", "amount", "price_usd"):
            if pricing.get(key) is not None:
                return pricing[key]
    return None


def _audit_production_x402_manifest() -> dict[str, Any]:
    url = f"{ORIGIN}/.well-known/x402-service.json"
    response = _safe_get_json(url)
    payload = response.get("payload", {})
    result: dict[str, Any] = {
        "http_status": response.get("http_status"),
        "expected_single_price_usd": str(EXPECTED_SINGLE_PRICE_USD),
    }
    if isinstance(payload, dict):
        pricing = payload.get("pricing")
        observed = pricing.get("base") if isinstance(pricing, dict) else None
        result["observed_single_price_usd"] = observed
        result["price_contract_match"] = _price_contract_match(observed)
        result["endpoint"] = payload.get("endpoint")
        payment = payload.get("payment")
        if isinstance(payment, dict):
            result["network"] = payment.get("network")
    if "error" in response:
        result["error"] = response
    return result


def _audit_official_mcp_registry() -> dict[str, Any]:
    encoded_name = quote(OFFICIAL_MCP_NAME, safe="")
    url = (
        "https://registry.modelcontextprotocol.io/v0.1/servers/"
        f"{encoded_name}/versions/latest"
    )
    response = _safe_get_json(url)
    payload = response.get("payload", {})
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False).lower()
    result: dict[str, Any] = {
        "http_status": response.get("http_status"),
        "name": OFFICIAL_MCP_NAME,
        "publicly_visible": _contains_projectpermit(payload),
        "expected_version": EXPECTED_MCP_VERSION,
        "expected_version_present": EXPECTED_MCP_VERSION.lower() in serialized,
        "expected_free_mcp_remote_present": FREE_MCP.lower() in serialized,
    }
    if "error" in response:
        result["error"] = response
    return result


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
        "expected_single_price_usd": str(EXPECTED_SINGLE_PRICE_USD),
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
        if "price_usd" in service:
            result["price_contract_match"] = _price_contract_match(service.get("price_usd"))
    if "error" in detail:
        result["detail_error"] = detail
    if "error" in search:
        result["search_error"] = search
    return result


def _audit_true402() -> dict[str, Any]:
    """Read True402's documented free registry endpoints; never call a paid stall."""
    search_url = "https://true402.dev/api/v1/services?" + urlencode(
        {"q": "ProjectPermit", "limit": 100}
    )
    detail_url = f"https://true402.dev/api/v1/services/{TRUE402_SERVICE_ID}"
    reputation_url = f"{detail_url}/reputation"
    search = _safe_get_json(search_url)
    detail = _safe_get_json(detail_url)
    reputation = _safe_get_json(reputation_url)
    detail_payload = detail.get("payload", {})
    result: dict[str, Any] = {
        "service_id": TRUE402_SERVICE_ID,
        "search_http_status": search.get("http_status"),
        "detail_http_status": detail.get("http_status"),
        "reputation_http_status": reputation.get("http_status"),
        "public_search_visible": _contains_projectpermit(search.get("payload", {})),
        "detail_matches_projectpermit": _contains_projectpermit(detail_payload),
        "expected_single_price_usd": str(EXPECTED_SINGLE_PRICE_USD),
    }
    if isinstance(detail_payload, dict):
        for field in ("id", "url", "name", "description", "reputation", "manifest"):
            if field in detail_payload:
                result[field] = detail_payload[field]
        observed_price = _manifest_price(detail_payload.get("manifest"))
        result["observed_single_price_usd"] = observed_price
        result["price_contract_match"] = _price_contract_match(observed_price)
    reputation_payload = reputation.get("payload")
    if isinstance(reputation_payload, dict):
        result["reputation"] = reputation_payload
    for label, response in (("search", search), ("detail", detail), ("reputation", reputation)):
        if "error" in response:
            result[f"{label}_error"] = response
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
        "production_x402_manifest": _audit_production_x402_manifest(),
        "official_mcp_registry": _audit_official_mcp_registry(),
        "402index": _audit_402index(),
        "true402": _audit_true402(),
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
