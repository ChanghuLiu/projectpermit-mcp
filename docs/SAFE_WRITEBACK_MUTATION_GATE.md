# Safe Writeback Mutation Gate

ProjectPermit Action Bundle `2026-08-29.3` adds `action_bundle.mutation_gate` so contractor and field-service agents can distinguish an informational permit result from a result that is safe to hand to an explicitly authorized writeback integration.

ProjectPermit does **not** execute Jobber, ServiceM8, or other external mutations in this layer. A `READY_FOR_EXPLICIT_WRITE` result is permission for an authorized integration to consider an explicit atomic upsert; it is not an instruction that ProjectPermit already changed an external system.

## Gate states

### `READY_FOR_EXPLICIT_WRITE`

The result may be handed to an explicitly authorized integration when all safeguards pass:

- a work-record scope exists (`source_platform`, `source_object_type`, `source_object_id`), represented in output only by a one-way `scope_fingerprint`;
- workflow `automation_safe=true`;
- evidence freshness is `CURRENT`;
- no required inputs remain unresolved;
- a deterministic `idempotency_key` exists.

The integration must use `ATOMIC_UPSERT` semantics keyed by `idempotency_key`. Unconditional create is never allowed by the ProjectPermit contract.

A normal first observation or operational route change uses `UPSERT_OPERATIONAL_ROUTE`. A ruleset/evidence refresh that preserves the same operational idempotency key may use `UPSERT_METADATA`.

### `NOOP_UNCHANGED`

A repeated scoped check whose decision identity is `UNCHANGED` is duplicate-suppressed. `mutation_allowed=false` and `recommended_operation=NOOP`.

This is the core protection against an Agent creating the same permit task repeatedly on retries, polling cycles, or duplicate workflow events.

### `BLOCKED`

Writeback is blocked if any required safeguard is missing. Current blocker codes include:

- `MISSING_IDEMPOTENCY_KEY`
- `MISSING_WORK_RECORD_SCOPE`
- `AUTOMATION_NOT_SAFE`
- `EVIDENCE_NOT_CURRENT`
- `REQUIRED_INPUTS_PENDING`

The permit preflight result remains usable as information; only automated mutation is blocked.

## Repeat-check contract

For a repeated check of the same work record, pass the prior `action_bundle.identity` as:

```json
{
  "context": {
    "source_platform": "jobber",
    "source_object_type": "quote",
    "source_object_id": "<platform object id>",
    "prior_decision_identity": {"...": "prior identity"}
  }
}
```

Raw platform object IDs are used only to derive the scoped idempotency identity and are not returned in `action_bundle.identity`.

## Jobber and ServiceM8 proposal wrappers

`projectpermit.writeback_proposal` provides:

- `build_jobber_safe_writeback_proposal(result)`
- `build_servicem8_safe_writeback_proposal(result)`

They combine the existing read-only field-service proposal mapping with the platform-neutral mutation gate and expose:

- `writeback_ready`
- `proposed_operation`
- `mutation_gate`
- `mutation_performed=false`

These helpers still perform no external API call.

## Safety boundary

The mutation gate is a ProjectPermit product-automation policy. It is not municipal authorization, legal advice, engineering approval, permit issuance, or proof that a third-party platform accepted a write.
