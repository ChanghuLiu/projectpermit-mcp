#!/usr/bin/env python3
"""Verify a ServiceM8 private API key without mutating ServiceM8.

Usage:
    SERVICEM8_API_KEY='...' python scripts/servicem8_readonly_probe.py

The command performs GET-only access and prints a compact account-safe summary.
It does not print the API key, client identities, billing data or full job records.
"""
from __future__ import annotations

import json
import os
import sys

from projectpermit.servicem8_client import ServiceM8ClientError, ServiceM8ReadOnlyClient


def main() -> int:
    api_key = os.getenv("SERVICEM8_API_KEY", "").strip()
    if not api_key:
        print("SERVICEM8_API_KEY is required", file=sys.stderr)
        return 2

    try:
        with ServiceM8ReadOnlyClient(api_key) as client:
            # One shallow GET is enough to prove private-key connectivity. Avoid
            # printing the returned records because they may contain customer data.
            jobs = client.list_jobs(params={"$top": "1"})
    except ServiceM8ClientError as exc:
        print(f"servicem8_probe=FAIL error={exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "servicem8_probe": "PASS",
                "read_only": True,
                "jobs_visible_in_probe_page": len(jobs),
                "records_printed": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
