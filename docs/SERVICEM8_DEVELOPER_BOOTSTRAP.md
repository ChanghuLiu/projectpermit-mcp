# ServiceM8 Developer Bootstrap — Read-Only Own-Account Validation

Verified against current official ServiceM8 documentation on 2026-08-27.

## Why this is a useful second live platform gate

Unlike a public multi-customer integration, ServiceM8 documents a **Private Application** path for connecting to your own ServiceM8 account or one specific customer's account using an API key.

A ServiceM8 Developer account is not required for that private API-key path.

ServiceM8's current public pricing also offers a `$0/month` Free plan with 1 user and up to 30 jobs/month. The only remaining account-level uncertainty is whether the Free-plan account UI currently exposes API-key creation. That must be verified in a real account rather than assumed from separate API/pricing pages.

## Safety requirement

Use a **Read Only** API key.

ServiceM8's official n8n integration guide explicitly documents two API-key types:

- `Read Only` — for workflows that only read ServiceM8 data;
- `Full Access` — required only when creating/updating ServiceM8 records.

ProjectPermit's current validation requires **Read Only only**.

Do not create or share a Full Access key for this phase.

## Manual step S0 — create/open the ServiceM8 account

This is an interactive account/login action and is intentionally not automated by the repository.

1. Open ServiceM8 and create/sign in to an account.
2. A Free account is sufficient for the initial experiment **if** its current UI exposes API keys.
3. In the online dashboard, go to:
   `Account -> Settings -> API Keys`
4. If `API Keys` is visible, choose `Add API Key`.
5. Name it something explicit, for example:
   `ProjectPermit Read Only Validation`
6. Choose API Key Type:
   **Read Only**
7. Copy the generated key into a local shell environment variable only.

Never paste the key into a GitHub issue, source file, README, chat screenshot, test fixture or commit.

If `API Keys` is not visible on the current Free account, stop there. Do **not** upgrade/pay automatically. Record the UI state first; we will decide whether a paid plan or the Development Partner route is justified.

## Manual step S1 — create synthetic own-account jobs

Before any independent customer data is used, create a few harmless synthetic Job records in the ServiceM8 account.

Recommended examples:

1. Quote — `Replace same-size front window`
2. Quote — `Finish basement with new plumbing rough-in`
3. Quote — `Build rear deck 700 mm above grade`
4. Work Order — `Create secondary suite`
5. Quote — `Paint and flooring only`

Use obviously synthetic customer/job details. Do not enter a real homeowner's personal information merely for integration testing.

Each test Job should contain:

- a supported-city civic address suitable for a test call;
- `Job Description` with the scope;
- `Status` as Quote or Work Order.

ServiceM8's current help material says new Job Cards contain `Job Address`, `Job Description`, and `Job Status`, where new jobs can begin as Quote or Work Order.

## S2 — run the repository connectivity probe

From the ProjectPermit repository:

```bash
export SERVICEM8_API_KEY='...'
python scripts/servicem8_readonly_probe.py
```

Expected safe output shape:

```json
{
  "jobs_visible_in_probe_page": 1,
  "read_only": true,
  "records_printed": 0,
  "servicem8_probe": "PASS"
}
```

The probe deliberately does **not** print the returned job because a live Job may contain customer data.

## S3 — retrieve one synthetic Job

Once connectivity passes, use `ServiceM8ReadOnlyClient.get_job(<uuid>)` in a local validation script/session.

Verify only the fields relevant to ProjectPermit:

- `uuid`
- `status`
- `job_address`
- `job_description`
- optional geocoded address components

Do not begin by pulling Company/customer, invoice, payment or staff data.

The documented current Job status values are:

- `Quote`
- `Work Order`
- `Unsuccessful`
- `Completed`

## S4 — adapter -> ProjectPermit integration

Feed the decoded Job into:

```python
extract_servicem8_work_object(job)
```

A caller/agent then converts `scope_text` into ProjectPermit's structured project facts before:

```python
build_preflight_facts(...)
```

The server still does not guess `project.family` with an LLM.

For deterministic local integration testing, set `resolve_address=False`. For an actual supported civic address when intentionally testing the municipal resolver, enable address resolution separately.

## S5 — optional JobMaterial scope

Do not request JobMaterial records by default.

First measure whether `job_description` is sufficient. Only add `read_job_materials` / JobMaterial retrieval if representative scopes are too sparse and line-item names materially improve classification.

This follows least-privilege and reduces irrelevant billing/price surface.

`servicem8_adapter.py` ignores price and cost fields even when JobMaterial objects are supplied.

## S6 — no write-back yet

`build_servicem8_routing_summary()` returns proposed ProjectPermit metadata only. It does not mutate ServiceM8.

Do not add ServiceM8 POST/DELETE operations during this phase.

ServiceM8 Custom Fields are documented as Public-Application-only and ServiceM8 itself recommends using custom fields sparingly. There is no need to solve write-back before E3/E4 validates repeated demand.

## S7 — public application only after evidence

A multi-customer product would move to ServiceM8's Public Application / Development Partner path:

- register as Development Partner;
- create an add-on;
- obtain App ID/App Secret;
- OAuth 2.0;
- request only required scopes;
- add webhooks/UI integration only if observed usage justifies it.

A Public Application may exist without being publicly listed in the Add-ons Directory.

## Evidence classification

These own-account steps prove only live technical compatibility.

They are **not** E3/E4 market evidence because the user controls both ProjectPermit and the synthetic ServiceM8 account/data.

True E3 still requires representative independent historical workflows; E4 requires repeated non-owner external use.

## Official sources

- Authentication / API-key path: https://developer.servicem8.com/docs/authentication
- ServiceM8 n8n guide documenting Read Only vs Full Access API keys: https://support.servicem8.com/help-center/servicem8-add-ons/n8n/how-to-connect-servicem8-to-n8n
- REST overview: https://developer.servicem8.com/docs/rest-overview
- Retrieve Job: https://developer.servicem8.com/reference/getjobs
- List Jobs: https://developer.servicem8.com/reference/listjobs
- Job field/status docs: https://developer.servicem8.com/reference/createjobs
- Pricing / Free plan: https://www.servicem8.com/pricing
