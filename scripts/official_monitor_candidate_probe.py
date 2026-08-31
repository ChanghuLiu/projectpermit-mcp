"""One-shot probe of official alternate URLs for low-cost regulatory monitoring.

This is validation only. It performs public GETs against explicitly listed municipal
sources, prints fetch/validator/hash observations, writes no source state, and does not
change the production source manifest.
"""
from __future__ import annotations

import hashlib
import json
import time

import httpx


CANDIDATES = (
    {
        "candidate_id": "OTT_ACCESSORY_PDF_CONTROL",
        "authority": "City of Ottawa",
        "purpose": "known-fetchable static official permit advisory control",
        "url": "https://documents.ottawa.ca/sites/default/files/permit_except_acc_structure_advisory_en.pdf",
    },
    {
        "candidate_id": "LAV_CDU_1_CURRENT_PDF",
        "authority": "Ville de Laval",
        "purpose": "current official Code de l'urbanisme consolidated regulation",
        "url": "https://www.laval.ca/wp-content/uploads/2025/02/cdu-1-reglement.pdf",
    },
    {
        "candidate_id": "VAN_VBBL_2025_VOL1_V4",
        "authority": "City of Vancouver",
        "purpose": "current official 2025 Vancouver Building By-law Book I Volume 1",
        "url": "https://vancouver.ca/files/cov/vbbl-2025-volume-1-v4-00.pdf",
    },
)


def probe(client: httpx.Client, candidate: dict[str, str]) -> dict[str, object]:
    started = time.perf_counter()
    try:
        response = client.get(candidate["url"])
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        content = response.content
        return {
            **candidate,
            "ok": response.is_success,
            "status": response.status_code,
            "final_url": str(response.url),
            "elapsed_ms": elapsed_ms,
            "content_type": response.headers.get("content-type"),
            "content_length": len(content),
            "etag": response.headers.get("etag"),
            "last_modified": response.headers.get("last-modified"),
            "cache_control": response.headers.get("cache-control"),
            "has_http_validator": bool(response.headers.get("etag") or response.headers.get("last-modified")),
            "sha256": hashlib.sha256(content).hexdigest() if response.is_success else None,
        }
    except Exception as exc:
        return {
            **candidate,
            "ok": False,
            "elapsed_ms": round((time.perf_counter() - started) * 1000),
            "error_type": type(exc).__name__,
            "error": str(exc)[:500],
        }


def main() -> None:
    with httpx.Client(
        timeout=45,
        follow_redirects=True,
        headers={"User-Agent": "ProjectPermit-official-monitor-candidate-probe/0.1", "Accept": "*/*"},
    ) as client:
        rows = [probe(client, candidate) for candidate in CANDIDATES]

    report = {
        "validation_only": True,
        "production_manifest_changed": False,
        "source_state_written": False,
        "paid_retrieval_used": False,
        "candidates": rows,
        "summary": {
            "total": len(rows),
            "fetch_ok": sum(bool(row.get("ok")) for row in rows),
            "with_http_validator": sum(bool(row.get("has_http_validator")) for row in rows),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
