# Local ServiceM8 Writeback

This is the recommended first real writeback path for ProjectPermit.

The commercial preflight remains hosted/x402-paid, but the ServiceM8 credential stays in the customer's own environment. ProjectPermit's Railway services never need the customer's ServiceM8 token or API key.

## 1. Scope the preflight to the real ServiceM8 Job

The ProjectPermit request context must identify the same ServiceM8 Job that will later receive the writeback:

```json
{
  "context": {
    "source_platform": "servicem8",
    "source_object_type": "job",
    "source_object_id": "<SERVICEM8_JOB_UUID>"
  }
}
```

ProjectPermit returns only a one-way `scope_fingerprint` and an `idempotency_key`; the raw source object id is not copied into decision identity.

Save the successful preflight response as `result.json`.

## 2. Dry-run locally

Install ProjectPermit, then run:

```bash
projectpermit-servicem8-exec \
  --result result.json \
  --job-uuid '<SERVICEM8_JOB_UUID>'
```

Dry-run is the default. It performs no provider request and prints:

- the target-bound execution plan;
- whether Layer 5 currently allows explicit writeback;
- the deterministic ServiceM8 record UUID;
- the exact lookup/create/update intents;
- the names of credential environment variables that would be used for execution.

If the raw Job UUID does not hash to the same scope used for the permit decision, the plan is blocked.

## 3A. Execute with a private-app API key

For a private integration to one ServiceM8 account, ServiceM8 supports API-key authentication.

```bash
export PROJECTPERMIT_SERVICEM8_API_KEY='...'
projectpermit-servicem8-exec \
  --result result.json \
  --job-uuid '<SERVICEM8_JOB_UUID>' \
  --execute
```

Do not pass the key as a command-line argument. Keeping it in an environment variable avoids placing it directly in shell history and keeps it outside the hosted ProjectPermit API.

## 3B. Execute with OAuth

```bash
export PROJECTPERMIT_SERVICEM8_ACCESS_TOKEN='...'
export PROJECTPERMIT_SERVICEM8_GRANTED_SCOPES='read_job_notes publish_job_notes'

projectpermit-servicem8-exec \
  --result result.json \
  --job-uuid '<SERVICEM8_JOB_UUID>' \
  --execute
```

For a permit/review Task, the expected scopes are normally:

```text
read_tasks manage_tasks
```

The executor refuses before making a provider request if the caller-declared OAuth scopes do not include the plan-required scopes.

## 4. Idempotency behavior

ProjectPermit derives the ServiceM8 Note/Task UUID from its own `idempotency_key`.

The local executor performs:

1. GET deterministic UUID;
2. if 404, POST create using that UUID;
3. if 200, POST update that UUID.

A repeat ProjectPermit check that is `NOOP_UNCHANGED` produces zero provider calls.

The executor intentionally does not auto-retry ambiguous provider/network failures. Re-run the command after checking connectivity; the deterministic UUID prevents a new logical ProjectPermit record from being chosen.

## Exit codes

- `0` — dry-run, duplicate NOOP, or successful create/update;
- `2` — invalid input or blocked/safety condition;
- `3` — provider/network execution failure.

## Credential boundary

The CLI reads only these variables:

- `PROJECTPERMIT_SERVICEM8_API_KEY`
- `PROJECTPERMIT_SERVICEM8_ACCESS_TOKEN`
- `PROJECTPERMIT_SERVICEM8_GRANTED_SCOPES`

Credential values are not accepted as CLI flags, are not written to ProjectPermit result JSON, and are not included in executor output.

Official ServiceM8 references:

- https://developer.servicem8.com/docs/authentication
- https://developer.servicem8.com/reference/createnotes
- https://developer.servicem8.com/reference/getnotes
- https://developer.servicem8.com/reference/updatenotes
- https://developer.servicem8.com/reference/createtasks
- https://developer.servicem8.com/reference/gettasks
- https://developer.servicem8.com/reference/updatetasks
