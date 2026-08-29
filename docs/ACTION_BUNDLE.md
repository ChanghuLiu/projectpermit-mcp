# Permit Evidence + Action Bundle

ProjectPermit returns a platform-neutral `action_bundle` with every successful preflight. The bundle is designed for contractor, field-service, property and Agent integrations that need an operational package rather than a permit answer alone.

The bundle is additive. It does not change the deterministic permit determination, does not mutate Jobber/ServiceM8/other systems, and does not represent municipal authorization, legal advice or permission to begin work.

## Why it exists

A normal permit API may return a status and source links. A workflow Agent usually needs several additional pieces before it can safely continue:

- the permit decision and confidence;
- the recommended operational route;
- whether quote finalization may continue;
- whether ProjectPermit's official-source verification is current enough for unattended automation;
- the highest-value missing facts;
- a concrete proposed task;
- deduplicated official evidence with rule ids and verification dates;
- audit metadata that can be stored with the work record;
- compact writeback hints that a platform adapter can map into its own fields.

`action_bundle` packages those pieces once in the shared preflight service so HTTP, free MCP, paid x402 MCP and batch results cannot drift.

## Shape

```json
{
  "action_bundle": {
    "bundle_version": "2026-08-29.1",
    "decision": {
      "determination": "REQUIRED",
      "confidence": "HIGH",
      "jurisdiction": {
        "country": "CA",
        "province": "ON",
        "municipality": "Ottawa"
      },
      "project_family": "addition"
    },
    "routing": {
      "recommended_route": "ADD_PERMIT_TASK",
      "quote_handling": "INCLUDE_PERMIT_ALLOWANCE",
      "automation_safe": true,
      "evidence_freshness": {
        "status": "CURRENT",
        "automation_blocked": false
      }
    },
    "required_inputs": [],
    "tasks": [
      {
        "task_type": "PERMIT_PROCESS",
        "blocking": true,
        "action": "Add a permit task/allowance before scheduling or design lock."
      },
      {
        "task_type": "ATTACH_EVIDENCE",
        "blocking": false,
        "action": "Attach the official-source evidence and rule metadata to the work record."
      }
    ],
    "evidence": [
      {
        "source_id": "OTT_GENERAL",
        "authority": "City of Ottawa",
        "title": "Building permit projects",
        "url": "https://ottawa.ca/...",
        "rule_ids": ["OTT-BLD-001"],
        "statuses": ["REQUIRED"],
        "source_verified_at": "2026-08-26"
      }
    ],
    "audit": {
      "engine_version": "phase0-0.1.0",
      "rule_ids": ["OTT-BLD-001"],
      "rule_versions": ["2026-08-26.1"],
      "source_verified_at_oldest": "2026-08-26",
      "source_verified_at_newest": "2026-08-26",
      "evidence_source_count": 1,
      "generated_from": "deterministic_preflight"
    },
    "writeback_hints": {
      "permit_status": "REQUIRED",
      "confidence": "HIGH",
      "recommended_route": "ADD_PERMIT_TASK",
      "quote_handling": "INCLUDE_PERMIT_ALLOWANCE",
      "automation_safe": true,
      "rule_version": "2026-08-26.1",
      "evidence_url": "https://ottawa.ca/...",
      "freshness_status": "CURRENT"
    }
  }
}
```

## Proposed task types

- `PERMIT_PROCESS` — create a permit workflow task/allowance before scheduling or design lock;
- `ATTACH_EVIDENCE` — preserve official evidence and rule metadata with the work record;
- `COLLECT_MISSING_FACTS` — ask for the listed facts and rerun ProjectPermit;
- `SPECIAL_REVIEW` — route planning/heritage/special cases for review;
- `MUNICIPAL_CONFIRMATION` — obtain municipal confirmation when the deterministic facts are insufficient;
- `MANUAL_SCOPE_REVIEW` — route unsupported scope outside unattended automation.

The task list is a **proposal**, not a mutation command.

## Evidence model

Evidence is deduplicated by `source_id` + URL. If multiple rules rely on the same official source, the bundle lists that source once and records all related `rule_ids`, statuses and the oldest relevant `source_verified_at` value.

This makes the bundle compact enough for work-record storage while preserving the rule-to-source audit trail.

## Jobber proposal mapping

`build_jobber_action_proposal(result)` returns:

- `mutation_performed: false`;
- proposed ProjectPermit custom-field values;
- proposed tasks;
- required inputs;
- deduplicated evidence;
- audit metadata.

The adapter does not call the Jobber API. Any future mutation path must be separately authorized and explicitly designed.

## ServiceM8 proposal mapping

`build_servicem8_action_proposal(result)` returns the same platform-neutral content with ServiceM8-oriented proposed routing fields.

It also performs no ServiceM8 API mutation.

## Safety boundary

`automation_safe=true` means ProjectPermit's deterministic result and source-freshness policy allow unattended **routing inside the preflight workflow**. It never means construction is municipally authorized.

A calling integration should preserve the underlying `determination`, evidence and disclaimer even when it uses the proposed tasks or writeback hints.
