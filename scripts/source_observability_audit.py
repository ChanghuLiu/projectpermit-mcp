"""One-shot, read-only observability audit for ProjectPermit official sources.

This is a validation tool, not continuous monitoring. It performs one GET per manifest
source, records fetch/validator metadata and a normalized content hash, and prints only
non-sensitive public-source observations. It never edits rules or source state.
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import httpx

from projectpermit.source_watch import digest


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "source_manifest.json"
USER_AGENT = "ProjectPermit-source-observability/0.1"


def audit_source(client: httpx.Client, source: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    base = {
        "source_id": source.get("source_id"),
        "authority": source.get("authority"),
        "kind": source.get("kind"),
        "criticality": source.get("criticality"),
        "url": source.get("url"),
    }
    try:
        response = client.get(str(source["url"]))
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        etag = response.headers.get("etag")
        last_modified = response.headers.get("last-modified")
        return {
            **base,
            "ok": True,
            "status": response.status_code,
            "final_url": str(response.url),
            "elapsed_ms": elapsed_ms,
            "bytes": len(response.content),
            "content_type": content_type,
            "etag": etag,
            "last_modified": last_modified,
            "cache_control": response.headers.get("cache-control"),
            "content_length_header": response.headers.get("content-length"),
            "has_http_validator": bool(etag or last_modified),
            "sha256": digest(response.content, content_type),
        }
    except Exception as exc:
        return {
            **base,
            "ok": False,
            "elapsed_ms": round((time.perf_counter() - started) * 1000),
            "error_type": type(exc).__name__,
            "error": str(exc)[:500],
        }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    ok_rows = [row for row in rows if row.get("ok")]
    failed = [row for row in rows if not row.get("ok")]
    validators = [row for row in ok_rows if row.get("has_http_validator")]
    by_authority: dict[str, dict[str, int]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("authority") or "unknown")].append(row)
    for authority, authority_rows in sorted(grouped.items()):
        authority_ok = sum(bool(row.get("ok")) for row in authority_rows)
        authority_validators = sum(bool(row.get("has_http_validator")) for row in authority_rows)
        by_authority[authority] = {
            "total": len(authority_rows),
            "ok": authority_ok,
            "failed": len(authority_rows) - authority_ok,
            "http_validator": authority_validators,
        }

    return {
        "total_sources": total,
        "fetch_ok": len(ok_rows),
        "fetch_failed": len(failed),
        "fetch_success_pct": round((len(ok_rows) / total) * 100, 1) if total else 0.0,
        "http_validator_count": len(validators),
        "http_validator_pct_of_ok": round((len(validators) / len(ok_rows)) * 100, 1) if ok_rows else 0.0,
        "critical_failures": [
            row.get("source_id")
            for row in failed
            if row.get("criticality") == "critical"
        ],
        "failure_types": dict(Counter(str(row.get("error_type")) for row in failed)),
        "by_authority": by_authority,
        "interpretation": {
            "purpose": "measure maintenance feasibility before operationalizing continuous regulatory monitoring",
            "continuous_monitoring_enabled": False,
            "source_state_written": False,
            "rules_modified": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit official-source fetch and validator coverage")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    sources = manifest.get("sources") or []
    if not isinstance(sources, list) or not sources:
        raise SystemExit("manifest contains no sources")

    with httpx.Client(
        timeout=args.timeout,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
    ) as client:
        rows = [audit_source(client, source) for source in sources]

    report = {
        "manifest_version": manifest.get("manifest_version"),
        "manifest_verified_at": manifest.get("verified_at"),
        "summary": summarize(rows),
        "sources": rows,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
