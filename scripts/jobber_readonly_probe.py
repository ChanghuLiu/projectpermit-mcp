#!/usr/bin/env python3
"""Verify a Jobber Developer Center testing token without mutating Jobber.

Usage:
    JOBBER_ACCESS_TOKEN='...' python scripts/jobber_readonly_probe.py

Optional:
    JOBBER_GRAPHQL_VERSION='2025-04-16'

The script prints only the authorized account id/name and API version.  It never
prints the access token or a raw response body.
"""
from __future__ import annotations

import json
import os
import sys

from projectpermit.jobber_client import JOBBER_API_VERSION, JobberClientError, JobberReadOnlyClient


def main() -> int:
    token = os.getenv("JOBBER_ACCESS_TOKEN", "").strip()
    if not token:
        print("JOBBER_ACCESS_TOKEN is required", file=sys.stderr)
        return 2

    api_version = os.getenv("JOBBER_GRAPHQL_VERSION", JOBBER_API_VERSION).strip() or JOBBER_API_VERSION

    try:
        with JobberReadOnlyClient(token, api_version=api_version) as client:
            account = client.get_account()
    except JobberClientError as exc:
        print(f"jobber_probe=FAIL error={exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "jobber_probe": "PASS",
                "api_version": api_version,
                "account": {
                    "id": str(account.get("id") or ""),
                    "name": str(account.get("name") or ""),
                },
                "read_only": True,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
