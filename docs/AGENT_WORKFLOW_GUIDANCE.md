# Agent workflow guidance

ProjectPermit does more than return a permit-applicability state. Every successful preflight also returns a deterministic `workflow` object designed for contractor, field-service and property-workflow agents.

The permit determination remains the source of truth for the preflight result. Workflow guidance is additive routing metadata only; it is not municipal authorization, legal advice or permission to start work.

## Why this exists

A generic permit lookup answers: "Does this project appear to need a permit?"

An embedded contractor agent needs the next operational step as well:

- add a permit task/allowance when the rules indicate a permit path;
- continue with official evidence attached when the rules indicate a high-confidence no-permit path;
- collect the highest-value missing project/property facts when another deterministic call may resolve ambiguity;
- route heritage/planning/special cases for review;
- stop unsupported scopes from flowing through an automated finalization path;
- stop unattended automation when ProjectPermit's official-source verification is old or unknown, even if the underlying permit determination is otherwise high confidence.

## Response shape

```json
{
  "determination": "MUNICIPAL_CONFIRMATION_REQUIRED",
  "confidence": "MEDIUM",
  "workflow": {
    "mode": "NEEDS_MORE_CONTEXT",
    "recommended_route": "COLLECT_MISSING_FACTS",
    "quote_handling": "HOLD_AUTOMATED_FINALIZATION",
    "automation_safe": false,
    "summary": "Collect the highest-value missing facts and run the deterministic preflight again.",
    "follow_up_questions": [
      {
        "fact_path": "project.estimated_cost_cad",
        "question": "What is the estimated total labour-and-material cost before tax?",
        "why_it_matters": "Gatineau's general existing-building renovation exemption uses a project-cost threshold."
      }
    ],
    "evidence_freshness": {
      "status": "CURRENT",
      "oldest_verified_at": "2026-08-26",
      "newest_verified_at": "2026-08-26",
      "oldest_age_days": 3,
      "review_after_days": 90,
      "stale_after_days": 180,
      "automation_blocked": false
    }
  }
}
```

## Stable routes

- `ADD_PERMIT_TASK`
- `CONTINUE_WITH_EVIDENCE`
- `COLLECT_MISSING_FACTS`
- `ROUTE_SPECIAL_REVIEW`
- `MUNICIPAL_CONFIRMATION`
- `MANUAL_SCOPE_REVIEW`

## Evidence freshness guardrail

Every rule result already records `source_verified_at`: the date ProjectPermit last verified the official source used by that rule. It is not the municipality's publication date and it does not claim a legal validity period.

ProjectPermit applies a deliberately conservative **product automation policy**:

- `CURRENT`: oldest relevant source verification is 90 days old or less;
- `REVIEW_DUE`: older than 90 days and no more than 180 days;
- `STALE`: older than 180 days;
- `UNKNOWN`: no parseable verification date is available.

`REVIEW_DUE`, `STALE`, and `UNKNOWN` force `workflow.automation_safe=false`. They do **not** rewrite the permit determination or route. A calling Agent can still show the result and evidence, but it should not treat that result as safe for unattended workflow finalization until the source/rules are re-verified.

The 90/180-day thresholds are ProjectPermit maintenance policy, not municipal/legal deadlines.

## Integration pattern

A Jobber/ServiceM8/other field-service adapter can use `workflow.recommended_route` as a proposed routing signal without mutating the upstream platform:

1. normalize the Request/Quote/Job scope into ProjectPermit facts;
2. call ProjectPermit;
3. show/store the evidence-linked determination;
4. inspect `workflow.evidence_freshness` before unattended automation;
5. use `workflow.recommended_route` to propose the next operational action;
6. require explicit product/integration policy before any write-back or irreversible mutation.

`automation_safe=true` is deliberately narrow. It means the deterministic result is suitable for automated routing inside the preflight workflow **and** ProjectPermit's relevant source verification is current under its maintenance policy; it does **not** mean the municipality has authorized construction.
