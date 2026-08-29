# External Execution Plans

Layer 6 turns ProjectPermit's safe-writeback gate into a target-bound mutation plan while deliberately stopping before OAuth/network execution.

This boundary is intentional: the caller must explicitly provide the raw target identifier again, and ProjectPermit recomputes its one-way scope fingerprint. A mutation plan is emitted only when that fingerprint matches the work-record scope used by the permit decision.

## ServiceM8

ServiceM8 has concrete REST resources that fit ProjectPermit's deterministic idempotency model:

- job notes: `GET /api_1.0/dbonote/{uuid}.json`, `POST /api_1.0/note.json`, `POST /api_1.0/dbonote/{uuid}.json`
- tasks: `GET /api_1.0/task/{uuid}.json`, `POST /api_1.0/task.json`, `POST /api_1.0/task/{uuid}.json`
- ServiceM8 accepts a caller-supplied UUID on Note and Task creation.

`build_servicem8_execution_plan()` derives a stable UUID from the ProjectPermit `idempotency_key` and chooses:

- a Note for non-blocking `ATTACH_EVIDENCE` routing; required OAuth scopes: `read_job_notes`, `publish_job_notes`;
- a Task for blocking permit/review/confirmation routing; required OAuth scopes: `read_tasks`, `manage_tasks`.

The plan uses `GET_THEN_CREATE_OR_UPDATE_DETERMINISTIC_UUID`. Repeated Layer 5 `NOOP_UNCHANGED` results emit no mutation intents at all.

Official references:

- https://developer.servicem8.com/docs/authentication
- https://developer.servicem8.com/reference/createnotes
- https://developer.servicem8.com/reference/getnotes
- https://developer.servicem8.com/reference/updatenotes
- https://developer.servicem8.com/reference/createtasks
- https://developer.servicem8.com/reference/gettasks
- https://developer.servicem8.com/reference/updatetasks

## Jobber

Jobber uses a versioned GraphQL API and OAuth 2.0. Its current developer documentation says app-configured custom fields are available on Jobs and Quotes, but an app may configure only five custom fields on a particular object. Jobber also recommends minimal scopes and requires active-version API schema handling.

ProjectPermit therefore does **not** attempt to write the existing 11-field read-only proposal as-is. Layer 6 compresses the executable representation to exactly five app-owned fields:

1. `ProjectPermit Status` — text
2. `ProjectPermit Route` — text
3. `ProjectPermit Evidence` — link
4. `ProjectPermit Freshness` — text
5. `ProjectPermit Identity` — text containing the ProjectPermit idempotency key

All are designed as app-owned read-only fields.

`build_jobber_execution_plan()` requires two bindings before it can return `READY_TO_EXECUTE`:

- five `customFieldConfigurationId` values created/resolved for the connected Jobber account;
- a tested active-version GraphQL binding (`api_version`, mutation name, id argument, input argument) taken from Jobber GraphiQL.

Until both are supplied, the plan returns `BINDING_REQUIRED`. This avoids hard-coding a version-sensitive GraphQL mutation from stale documentation.

Requests are not an executable custom-field target in this layer because Jobber's documented app-configured custom-field object list includes Jobs and Quotes but not Requests.

Official references:

- https://developer.getjobber.com/docs/
- https://developer.getjobber.com/docs/getting_started/
- https://developer.getjobber.com/docs/building_your_app/app_authorization/
- https://developer.getjobber.com/docs/using_jobbers_api/custom_fields/
- https://developer.getjobber.com/docs/using_jobbers_api/api_queries_and_mutations/
- https://developer.getjobber.com/docs/custom_integrations/

## Safety properties

Every execution plan:

- is `mutation_performed=false`;
- requires a separate explicit execute call;
- binds the raw target to the same one-way `scope_fingerprint` as the permit decision;
- propagates Layer 5 duplicate suppression as `NOOP`;
- never turns a Layer 5 `BLOCKED` result into an executable plan;
- never stores or returns OAuth tokens.

The execution plan is a software integration contract, not municipal authorization or proof that a third-party platform accepted a mutation.
