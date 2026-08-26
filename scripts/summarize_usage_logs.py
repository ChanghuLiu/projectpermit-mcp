"""Summarize ProjectPermit structured usage events from stdin or log files.

Examples:
    cat railway.log | python scripts/summarize_usage_logs.py
    python scripts/summarize_usage_logs.py api.log mcp.log

Only lines containing the `PROJECTPERMIT_USAGE ` prefix are parsed.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

PREFIX = "PROJECTPERMIT_USAGE "


def _iter_lines(paths: list[str]) -> Iterable[str]:
    if not paths:
        yield from sys.stdin
        return
    for raw_path in paths:
        with Path(raw_path).open("r", encoding="utf-8", errors="replace") as handle:
            yield from handle


def _events(lines: Iterable[str]):
    for line in lines:
        marker = line.find(PREFIX)
        if marker < 0:
            continue
        raw = line[marker + len(PREFIX):].strip()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if payload.get("event") == "projectpermit_preflight":
            yield payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", help="Optional Railway/log files; stdin when omitted")
    args = parser.parse_args()

    events = list(_events(_iter_lines(args.paths)))
    external = [event for event in events if not event.get("internal_traffic")]
    internal = [event for event in events if event.get("internal_traffic")]

    print(f"events_total={len(events)}")
    print(f"events_external={len(external)}")
    print(f"events_internal={len(internal)}")
    print(
        "external_unique_client_tags="
        + str(len({event.get('client_tag_hash') for event in external if event.get('client_tag_hash')}))
    )

    for key in ("transport", "jurisdiction", "project_family", "determination"):
        counts = Counter(str(event.get(key) or "unknown") for event in external)
        print(f"external_by_{key}=" + json.dumps(dict(counts.most_common()), sort_keys=True))


if __name__ == "__main__":
    main()
