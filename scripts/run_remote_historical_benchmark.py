"""Run anonymized historical benchmark cases against the free remote MCP preview.

This intentionally uses the same CSV as the E3 audit flow. It fills deterministic
ProjectPermit result fields while leaving business/material-disagreement judgment to
a human reviewer when results disagree.
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
from pathlib import Path
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

DEFAULT_URL = "https://projectpermit-mcp-production.up.railway.app/mcp"
TOOL = "check_project_requirements"


def _yes(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def _json_object(raw: str, field: str, case_id: str) -> dict[str, Any]:
    try:
        value = json.loads(raw or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"{case_id}: invalid {field}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{case_id}: {field} must be a JSON object")
    return value


def _result_payload(result: Any) -> dict[str, Any]:
    structured = getattr(result, "structured_content", None)
    if structured:
        return dict(structured)
    rendered = "\n".join(getattr(block, "text", "") for block in result.content)
    value = json.loads(rendered)
    if not isinstance(value, dict):
        raise ValueError("MCP tool returned non-object JSON")
    return value


async def run(input_path: Path, output_path: Path, client_tag: str, url: str) -> None:
    with input_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit("Input CSV has no header")
        rows = list(reader)
        fieldnames = list(reader.fieldnames)

    required = {
        "case_id",
        "jurisdiction",
        "project_family",
        "project_facts_json",
        "property_facts_json",
        "usable_case",
        "historical_determination",
        "projectpermit_determination",
        "projectpermit_confidence",
        "agreement",
        "material_disagreement",
        "false_likely_not_required",
    }
    missing = sorted(required - set(fieldnames))
    if missing:
        raise SystemExit("Input CSV missing columns: " + ", ".join(missing))

    if not client_tag.strip():
        raise SystemExit("--client-tag must be a stable non-PII integration/pilot identifier")

    attempted = 0
    completed = 0
    disagreements = 0
    false_negatives = 0

    async with streamable_http_client(url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = {tool.name for tool in tools.tools}
            if TOOL not in names:
                raise SystemExit(f"Remote MCP does not expose {TOOL}")

            for row in rows:
                if not _yes(row.get("usable_case")):
                    continue
                case_id = (row.get("case_id") or "<missing-case-id>").strip()
                project = _json_object(row.get("project_facts_json", ""), "project_facts_json", case_id)
                property_facts = _json_object(row.get("property_facts_json", ""), "property_facts_json", case_id)
                family = (row.get("project_family") or "").strip()
                if project.get("family") != family:
                    raise ValueError(
                        f"{case_id}: project_facts_json family {project.get('family')!r} "
                        f"does not match project_family {family!r}"
                    )

                attempted += 1
                result = await session.call_tool(
                    TOOL,
                    {
                        "jurisdiction": (row.get("jurisdiction") or "").strip(),
                        "project": project,
                        "property": property_facts,
                        "context": {"client_tag": client_tag},
                        # Historical benchmark files must not contain exact civic addresses.
                        # Reproducible derived property facts are supplied above instead.
                        "resolve_address": False,
                    },
                )
                if result.is_error:
                    raise RuntimeError(f"{case_id}: remote MCP tool returned an error: {result}")
                payload = _result_payload(result)
                determination = str(payload.get("determination") or "")
                confidence = str(payload.get("confidence") or "")
                if not determination:
                    raise RuntimeError(f"{case_id}: response missing determination: {payload}")

                historical = (row.get("historical_determination") or "").strip()
                agrees = bool(historical) and historical == determination
                false_negative = historical == "REQUIRED" and determination == "LIKELY_NOT_REQUIRED"

                row["projectpermit_determination"] = determination
                row["projectpermit_confidence"] = confidence
                row["agreement"] = "yes" if agrees else "no"
                row["false_likely_not_required"] = "yes" if false_negative else "no"

                # Exact agreement is non-material by definition for this comparison.
                # A disagreement needs human workflow judgment; never auto-label it harmless.
                row["material_disagreement"] = "no" if agrees else ""

                completed += 1
                disagreements += int(not agrees)
                false_negatives += int(false_negative)
                print(
                    f"case={case_id} determination={determination} confidence={confidence} "
                    f"agreement={'yes' if agrees else 'no'} false_likely_not_required={'yes' if false_negative else 'no'}"
                )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"attempted={attempted}")
    print(f"completed={completed}")
    print(f"disagreements_requiring_human_review={disagreements}")
    print(f"false_likely_not_required={false_negatives}")
    print(f"output={output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run anonymized historical cases against ProjectPermit's free remote MCP preview."
    )
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--client-tag",
        required=True,
        help="Stable non-PII pilot/integration id, e.g. buildxact-pilot-01. It is hashed server-side.",
    )
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()
    asyncio.run(run(args.input_csv, args.output, args.client_tag, args.url))


if __name__ == "__main__":
    main()
