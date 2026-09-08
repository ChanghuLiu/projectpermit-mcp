from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import os
import re
import sqlite3


def runtime_dir() -> Path:
    p = Path(os.getenv("EWW_RUNTIME_DIR", "/data" if Path("/data").exists() else "runtime"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def _db():
    c = sqlite3.connect(runtime_dir() / "analytics.sqlite")
    c.execute(
        "CREATE TABLE IF NOT EXISTS events ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "occurred_at TEXT NOT NULL,"
        "tool TEXT NOT NULL,"
        "outcome TEXT NOT NULL,"
        "billable INTEGER NOT NULL,"
        "payment_state TEXT,"
        "actor_class TEXT NOT NULL,"
        "declared_client TEXT,"
        "latency_ms REAL"
        ")"
    )
    c.commit()
    return c


def _safe(v: Any, max_len: int = 80):
    if not isinstance(v, str) or not v.strip():
        return None
    return re.sub(r"[^A-Za-z0-9._:/+@-]", "_", v.strip())[:max_len]


def classify_actor(meta: dict[str, Any] | None):
    meta = meta or {}
    source = str(meta.get("englandworkswatch/actor", "")).strip().lower()
    actor = source if source in {"owned_ci", "declared_external"} else "unattributed"
    ci = meta.get("io.modelcontextprotocol/clientInfo")
    name = ci.get("name") if isinstance(ci, dict) else None
    return actor, _safe(name)


def record(
    tool: str,
    outcome: str,
    *,
    billable: bool,
    payment_state: str | None = None,
    meta: dict[str, Any] | None = None,
    latency_ms: float | None = None,
):
    actor, client = classify_actor(meta)
    with _db() as c:
        c.execute(
            "INSERT INTO events(occurred_at,tool,outcome,billable,payment_state,actor_class,declared_client,latency_ms) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (
                datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                tool,
                outcome,
                int(billable),
                payment_state,
                actor,
                client,
                latency_ms,
            ),
        )


def _nested_counts(rows, outer_index: int, inner_index: int) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for row in rows:
        outer = str(row[outer_index])
        inner = str(row[inner_index])
        bucket = result.setdefault(outer, {})
        bucket[inner] = bucket.get(inner, 0) + 1
    return result


def summary():
    try:
        with _db() as c:
            rows = c.execute(
                "SELECT tool,outcome,billable,payment_state,actor_class FROM events"
            ).fetchall()
    except sqlite3.Error:
        rows = []

    paid_rows = [row for row in rows if row[2]]
    paid_actor_rows = [
        (row[4], row[3] or "none")
        for row in paid_rows
    ]
    business_tools = {"assess_change_impact", "batch_assess_changes"}
    business_rows = [row for row in rows if row[0] in business_tools]

    by_actor_tool: dict[str, dict[str, int]] = {}
    by_actor_outcome: dict[str, dict[str, int]] = {}
    for tool, outcome, _billable, _payment_state, actor in rows:
        tool_bucket = by_actor_tool.setdefault(actor, {})
        tool_bucket[tool] = tool_bucket.get(tool, 0) + 1
        outcome_bucket = by_actor_outcome.setdefault(actor, {})
        outcome_bucket[outcome] = outcome_bucket.get(outcome, 0) + 1

    paid_funnel_by_actor: dict[str, dict[str, int]] = {}
    for actor, payment_state in paid_actor_rows:
        bucket = paid_funnel_by_actor.setdefault(actor, {})
        bucket[payment_state] = bucket.get(payment_state, 0) + 1

    return {
        "total_events": len(rows),
        "by_tool": dict(Counter(row[0] for row in rows)),
        "by_outcome": dict(Counter(row[1] for row in rows)),
        "by_actor_class": dict(Counter(row[4] for row in rows)),
        "by_actor_tool": by_actor_tool,
        "by_actor_outcome": by_actor_outcome,
        "business_tool_events_by_actor": dict(Counter(row[4] for row in business_rows)),
        "paid_funnel": dict(Counter((row[3] or "none") for row in paid_rows)),
        "paid_funnel_by_actor": paid_funnel_by_actor,
        "privacy": (
            "No employer/worker facts, raw MCP metadata, payment signatures, private keys or seed phrases are stored."
        ),
    }
