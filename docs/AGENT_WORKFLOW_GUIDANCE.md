# Agent workflow guidance

ProjectPermit does more than return a permit-applicability state. Every successful preflight now also returns a deterministic `workflow` object designed for contractor, field-service and property-workflow agents.

The permit determination remains the source of truth for the preflight result. Workflow guidance is additive routing metadata only; it is not municipal authorization, legal advice or permission to start work.

## Why this exists

A generic permit lookup answers: "Does this project appear to need a permit?"

An embedded contractor agent needs the next operational step as well:

- add a permit task/allowance when the rules indicate a permit path;
- continue with the official evidence attached when the rules indicate a high-confidence no-permit path;
- collect the highest-value missing project/property facts when another deterministic call may resolve the ambiguity;
- route heritage/planning/special cases for review;
- stop unsupported scopes from flowing through an automated finalization path.

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
    ]
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

## Integration pattern

A Jobber/ServiceM8/other field-service adapter can use `workflow.recommended_route` as a proposed routing signal without mutating the upstream platform:

1. normalize the Request/Quote/Job scope into ProjectPermit facts;
2. call ProjectPermit;
3. show/store the evidence-linked determination;
4. use `workflow` to propose the next operational action;
5. require explicit product/integration policy before any write-back or irreversible mutation.

`automation_safe=true` is deliberately narrow. It means the deterministic result is suitable for automated routing inside the preflight workflow; it does **not** mean the municipality has authorized construction.
