"""End-to-end smoke test for the public ProjectPermit bulk HTTP preview."""
from __future__ import annotations

import os

import httpx

BASE_URL = os.getenv(
    "PROJECTPERMIT_HTTP_BASE_URL",
    "https://projectpermit-api-v2-production.up.railway.app",
).rstrip("/")
INTERNAL_CONTEXT = {"client_tag": "projectpermit-ci"}


def main() -> None:
    capabilities_url = f"{BASE_URL}/v1/capabilities"
    batch_url = f"{BASE_URL}/v1/preview-project-requirements-batch"
    print(f"http_base_url={BASE_URL}")

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        capabilities_response = client.get(capabilities_url)
        capabilities_response.raise_for_status()
        capabilities = capabilities_response.json()
        if capabilities.get("free_batch_preview_resource") != "/v1/preview-project-requirements-batch":
            raise SystemExit(f"Bulk preview resource missing from capabilities: {capabilities}")
        if capabilities.get("bulk_max_items") != 50:
            raise SystemExit(f"Unexpected bulk_max_items: {capabilities.get('bulk_max_items')}")
        print("bulk_http_capabilities=PASS")

        response = client.post(
            batch_url,
            json={
                "items": [
                    {
                        "client_ref": "smoke-good",
                        "jurisdiction": "ottawa_on",
                        "project": {
                            "family": "window_door",
                            "action": "replace_same_size",
                        },
                        "property": {"heritage": False},
                        "context": INTERNAL_CONTEXT,
                    },
                    {
                        "client_ref": "smoke-bad",
                        "jurisdiction": "ottawa_on",
                        "context": INTERNAL_CONTEXT,
                    },
                ]
            },
        )
        response.raise_for_status()
        payload = response.json()

    if payload.get("batch_size") != 2:
        raise SystemExit(f"Unexpected batch_size: {payload}")
    if payload.get("succeeded") != 1 or payload.get("failed") != 1:
        raise SystemExit(f"Unexpected success/failure counts: {payload}")

    results = payload.get("results") or []
    if len(results) != 2:
        raise SystemExit(f"Unexpected result count: {payload}")

    good, bad = results
    good_result = good.get("result") or {}
    if good.get("client_ref") != "smoke-good" or good.get("ok") is not True:
        raise SystemExit(f"Good item correlation/status failed: {good}")
    if good_result.get("determination") != "LIKELY_NOT_REQUIRED":
        raise SystemExit(f"Unexpected good-item determination: {good}")

    bad_error = bad.get("error") or {}
    if bad.get("client_ref") != "smoke-bad" or bad.get("ok") is not False:
        raise SystemExit(f"Bad item correlation/status failed: {bad}")
    if bad_error.get("type") != "validation_error":
        raise SystemExit(f"Bad item was not isolated as validation_error: {bad}")

    audit = payload.get("audit") or {}
    if int(audit.get("unique_rule_ids") or 0) < 1:
        raise SystemExit(f"Bulk audit missing rule IDs: {audit}")
    if int(audit.get("evidence_links") or 0) < 1:
        raise SystemExit(f"Bulk audit missing evidence links: {audit}")
    if not audit.get("engine_versions"):
        raise SystemExit(f"Bulk audit missing engine versions: {audit}")
    if not audit.get("source_verified_at_oldest") or not audit.get("source_verified_at_newest"):
        raise SystemExit(f"Bulk audit missing source freshness range: {audit}")

    counts = payload.get("determination_counts") or {}
    if counts.get("LIKELY_NOT_REQUIRED") != 1:
        raise SystemExit(f"Unexpected determination counts: {counts}")

    print(
        "bulk_http_result="
        f"batch_size={payload['batch_size']} succeeded={payload['succeeded']} failed={payload['failed']} "
        f"unique_rule_ids={audit['unique_rule_ids']} evidence_links={audit['evidence_links']}"
    )
    print("remote_bulk_http_smoke=PASS")


if __name__ == "__main__":
    main()
