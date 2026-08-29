# Credential-Isolated External Executor

Layer 7 introduces the first ProjectPermit component that is technically capable of a third-party write. The boundary is intentionally narrow and currently concrete only for ServiceM8.

## Safety contract

`execute_servicem8_plan()` accepts only a target-bound Layer 6 ServiceM8 execution plan.

It has these invariants:

- `execute` defaults to `false`; dry-run performs zero network calls.
- Layer 6 `NOOP` and `BLOCKED` plans perform zero network calls even if `execute=true`.
- A real call requires exactly one credential mode: OAuth access token or private-app API key.
- OAuth mode additionally requires the caller to declare the granted scopes. The executor refuses before the network if any plan-required scope is missing.
- Credentials are function arguments only. ProjectPermit does not persist them, log them, add them to the action bundle, or return them.
- The ServiceM8 host is pinned to `https://api.servicem8.com`.
- Planned paths are not trusted blindly. Before credentials are attached, the executor recomputes the only valid lookup/create/update paths from the deterministic record kind and UUID and verifies the job target in every write body.
- The executor performs exactly one lookup followed by one create or update.
- Provider/network failures are not automatically retried. The returned error does not echo provider response bodies, request headers, or exception messages that could contain sensitive material.
- Because Layer 6 uses a deterministic UUID derived from the ProjectPermit idempotency key, a caller can rebuild and retry after an ambiguous failure without creating a new logical ProjectPermit record.

## ServiceM8 credential modes

ServiceM8 documents two relevant authentication models:

1. Private application API key, sent as `X-API-Key`.
2. OAuth 2.0 access token, sent as `Authorization: Bearer ...`.

For OAuth execution, the plan determines the minimum scopes:

- Evidence-only Job Note: `read_job_notes`, `publish_job_notes`.
- Permit/review Task: `read_tasks`, `manage_tasks`.

Official references:

- https://developer.servicem8.com/docs/authentication
- https://developer.servicem8.com/reference/createnotes
- https://developer.servicem8.com/reference/getnotes
- https://developer.servicem8.com/reference/updatenotes
- https://developer.servicem8.com/reference/createtasks
- https://developer.servicem8.com/reference/gettasks
- https://developer.servicem8.com/reference/updatetasks

## Result shape

The executor returns only a minimal audit result:

- `executor_version`
- `platform`
- `status`
- `mutation_performed`
- `idempotency_key`
- `bundle_id`
- deterministic `record_kind` / `record_uuid`
- `operation` when a provider mutation was attempted
- provider HTTP status code where useful
- non-secret reason/error type metadata

Credential values are deliberately absent.

## Jobber remains execution-disabled

Layer 6 already generates a five-field Jobber plan and requires active-version GraphQL bindings. Layer 7 does not yet send Jobber writes. The current Jobber API is date-versioned and requires `X-JOBBER-GRAPHQL-VERSION`; app-configured custom fields are limited to five per app/object. A future Jobber executor must accept a tested GraphQL mutation document/schema binding rather than synthesize a mutation from stale field names.

Official references:

- https://developer.getjobber.com/docs/
- https://developer.getjobber.com/docs/using_jobbers_api/custom_fields/
- https://developer.getjobber.com/docs/using_jobbers_api/api_queries_and_mutations/

## Not a public write endpoint yet

This module is a library execution boundary, not an exposed ProjectPermit HTTP or MCP write tool. No production ServiceM8 or Jobber account is modified merely by deploying this code. A public/external execute surface requires a separate credential-isolation and authorization design review.