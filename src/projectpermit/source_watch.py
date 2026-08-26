"""Low-cost official-source change detector.

It intentionally does not auto-edit legal/regulatory rules. A changed source creates a
review signal; a human/developer then decides whether a rule or golden case changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import httpx

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "data" / "source_manifest.json"
DEFAULT_STATE = ROOT / "data" / "source_state.json"


def normalize_bytes(content: bytes, content_type: str = "") -> bytes:
    if "pdf" in content_type.lower() or b"%PDF" == content[:4]:
        return content
    try:
        text = content.decode("utf-8", errors="replace")
    except Exception:
        return content
    return " ".join(text.split()).encode("utf-8")


def digest(content: bytes, content_type: str = "") -> str:
    return hashlib.sha256(normalize_bytes(content, content_type)).hexdigest()


def fetch_url(url: str) -> tuple[bytes, str, int]:
    with httpx.Client(timeout=30, follow_redirects=True, headers={"User-Agent": "ProjectPermit-source-watch/0.1"}) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.content, response.headers.get("content-type", ""), response.status_code


def check_sources(
    manifest: dict[str, Any],
    previous: dict[str, Any] | None = None,
    fetcher: Callable[[str], tuple[bytes, str, int]] = fetch_url,
) -> dict[str, Any]:
    previous = previous or {"sources": {}}
    prior = previous.get("sources", {})
    current: dict[str, Any] = {"sources": {}}
    changes: list[dict[str, Any]] = []

    for source in manifest.get("sources", []):
        sid = source["source_id"]
        try:
            body, content_type, status = fetcher(source["url"])
            sha = digest(body, content_type)
            record = {
                "sha256": sha,
                "status": status,
                "content_type": content_type,
                "url": source["url"],
            }
            old_sha = (prior.get(sid) or {}).get("sha256")
            if old_sha and old_sha != sha:
                changes.append({
                    "source_id": sid,
                    "criticality": source.get("criticality", "unknown"),
                    "change": "CONTENT_CHANGED",
                    "old_sha256": old_sha,
                    "new_sha256": sha,
                })
        except Exception as exc:
            record = {"url": source["url"], "error": str(exc)}
            changes.append({
                "source_id": sid,
                "criticality": source.get("criticality", "unknown"),
                "change": "FETCH_FAILED",
                "error": str(exc),
            })
        current["sources"][sid] = record

    current["changes"] = changes
    return current


def main() -> None:
    parser = argparse.ArgumentParser(description="Check ProjectPermit official sources for changes")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--write", action="store_true", help="write the current state after checking")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text())
    previous = json.loads(args.state.read_text()) if args.state.exists() else None
    result = check_sources(manifest, previous)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.write:
        args.state.write_text(json.dumps({"sources": result["sources"]}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
