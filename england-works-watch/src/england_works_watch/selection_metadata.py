from __future__ import annotations

from copy import deepcopy
from typing import Any

SERVER_SELECTION_DESCRIPTION = (
    "UK Skilled Worker sponsor-compliance change intelligence for employer, HR and HRIS agents. "
    "Use for official GOV.UK source freshness, supported sponsor change categories, one-event or batch impact preflight, "
    "including absence, salary, role, work-location, delayed start, stop sponsorship, organisation change, TUPE, merger "
    "or takeover. Paid deterministic decisions return AFFECTED, NOT_AFFECTED, REVIEW_REQUIRED or INSUFFICIENT_INPUT "
    "with evidence and fail closed on stale/changed sources. Not individual visa advice or a Home Office decision."
)

TOOL_SELECTION_DESCRIPTIONS: dict[str, str] = {
    "england_works_watch_info": (
        "Free product information. Use for service scope, what England Works Watch does, pricing, cost, x402 network, "
        "payment, MCP endpoint, discovery metadata, or legal-advice disclaimer. Not for source freshness, supported-event "
        "lists, or change decisions."
    ),
    "licensing_source_status": (
        "Free GOV.UK evidence source status. Use for current guidance, source freshness, stale sources, changed "
        "fingerprints, blocking sources, review status, evidence lifecycle, or source coverage. Not for a specific "
        "sponsor change decision."
    ),
    "list_supported_change_events": (
        "Free supported-event list. Use when asking which sponsor events the tool can handle, which change "
        "types/categories are supported, or to list supported events: absence, salary, role, work location, start delay, "
        "stop sponsorship, organisation change, TUPE, merger, takeover. Capability/list only; not impact, reporting, or "
        "required-action decisions."
    ),
    "assess_change_impact": (
        "Paid single-event change decision. Use for one concrete Skilled Worker sponsor event to determine impact, "
        "whether reporting is triggered, whether it is AFFECTED/NOT_AFFECTED, what the sponsor must do, or required "
        "actions. Handles one absence, salary, role, remote/home/work-location, delayed start, stop-sponsoring, "
        "organisation, TUPE, merger, or takeover event. x402 USDC. Not multiple events."
    ),
    "batch_assess_changes": (
        "Paid batch/multiple-event change decision for 1-25 events. Use for a list, batch, set, several, many, multiple, "
        "5, 8, 20 or other collection of sponsor changes; evaluate them together and return per-event results plus "
        "outcome counts. x402 USDC. Not for one event."
    ),
}

CHANGE_PROPERTIES: dict[str, dict[str, Any]] = {
    "event_type": {
        "type": "string",
        "enum": [
            "worker_start_delay",
            "unauthorised_absence",
            "unpaid_or_reduced_pay_absence",
            "salary_change",
            "role_change",
            "work_location_change",
            "stop_sponsoring",
            "organisation_change",
            "tupe_transfer",
            "merger_takeover",
        ],
        "description": "Sponsor change event category to assess.",
    },
    "route": {
        "type": "string",
        "enum": ["skilled_worker"],
        "description": "V0.1 supports Skilled Worker only; unsupported routes fail closed.",
    },
    "delay_days": {"type": "integer", "minimum": 0},
    "consecutive_working_days": {"type": "integer", "minimum": 0},
    "total_weeks": {"type": "number", "minimum": 0},
    "valid_exception": {"type": "boolean"},
    "compelling_reason": {"type": "boolean"},
    "direction": {"type": "string", "enum": ["increase", "decrease"]},
    "pre_registration_nurse_or_midwife": {"type": "boolean"},
    "same_salary_option_still_met": {"type": "boolean"},
    "revised_salary_meets_skilled_worker": {"type": "boolean"},
    "same_occupation_code": {"type": "boolean"},
    "role_eligible": {"type": "boolean"},
    "salary_requirements_met": {"type": "boolean"},
    "hybrid_only": {"type": "boolean"},
    "new_main_office": {"type": "boolean"},
    "new_client_site": {"type": "boolean"},
    "permanent_remote": {"type": "boolean"},
    "occasional_only": {"type": "boolean"},
    "reason": {"type": "string"},
    "change_kind": {"type": "string"},
    "duties_unchanged": {"type": "boolean"},
    "new_sponsor_has_relevant_licence": {"type": "boolean"},
    "change_type": {"type": "string"},
    "old_entity_continues_trading": {"type": "boolean"},
    "new_entity_has_relevant_licence": {"type": "boolean"},
}

_CHANGE_SCHEMA = {
    "type": "object",
    "properties": CHANGE_PROPERTIES,
    "required": ["event_type", "route"],
    "additionalProperties": True,
}

PAID_TOOL_INPUT_SCHEMAS: dict[str, dict[str, Any]] = {
    "assess_change_impact": {
        "type": "object",
        "properties": {
            "payload": {
                **deepcopy(_CHANGE_SCHEMA),
                "description": "One structured Skilled Worker sponsor-change event. Supply the event-specific facts you know; missing required decision facts fail closed rather than being guessed.",
                "examples": [
                    {"event_type": "unauthorised_absence", "route": "skilled_worker", "consecutive_working_days": 11}
                ],
            }
        },
        "required": ["payload"],
        "additionalProperties": False,
        "title": "assess_change_impactArguments",
    },
    "batch_assess_changes": {
        "type": "object",
        "properties": {
            "payload": {
                "type": "object",
                "properties": {
                    "changes": {
                        "type": "array",
                        "items": deepcopy(_CHANGE_SCHEMA),
                        "minItems": 1,
                        "maxItems": 25,
                        "description": "1-25 structured Skilled Worker sponsor-change events.",
                    }
                },
                "required": ["changes"],
                "additionalProperties": False,
            }
        },
        "required": ["payload"],
        "additionalProperties": False,
        "title": "batch_assess_changesArguments",
    },
}


def _tool_registry(mcp_server: Any) -> dict[str, Any]:
    manager = getattr(mcp_server, "_tool_manager", None)
    tools = getattr(manager, "_tools", None)
    if not isinstance(tools, dict):
        raise RuntimeError("MCPServer tool registry unavailable for selection metadata override")
    return tools


def apply_selection_metadata(mcp_server: Any) -> None:
    lowlevel = getattr(mcp_server, "_lowlevel_server", None)
    if lowlevel is None or not hasattr(lowlevel, "description"):
        raise RuntimeError("MCPServer low-level description unavailable for selection metadata override")
    lowlevel.description = SERVER_SELECTION_DESCRIPTION

    tools = _tool_registry(mcp_server)
    missing = sorted(set(TOOL_SELECTION_DESCRIPTIONS) - set(tools))
    if missing:
        raise RuntimeError(f"MCP tools missing before selection metadata override: {', '.join(missing)}")
    for name, description in TOOL_SELECTION_DESCRIPTIONS.items():
        tools[name].description = description
    for name, schema in PAID_TOOL_INPUT_SCHEMAS.items():
        tools[name].parameters = deepcopy(schema)
