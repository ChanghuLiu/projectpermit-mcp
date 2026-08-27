# E3 Historical Benchmark Runbook

Updated: 2026-08-27

Purpose: turn partner-supplied anonymized historical cases into reproducible E3 evidence without storing customer PII or inflating weak samples into market validation.

## Three contributor paths

The evidence standard is the same regardless of how the cases arrive.

### 1. Human-readable scope intake — lowest technical burden

For a permit consultant, estimator, builder or workflow expert who does not want to write JSON, start from:

`data/design_partner_scope_template.csv`

That template asks for ordinary scope facts such as:

- bounded sample window + sampling method;
- jurisdiction + project family;
- de-identified scope summary;
- structural/wall/plumbing/dwelling changes;
- deck height or accessory-structure facts when relevant;
- whether address/property context mattered;
- historical determination + decision source;
- manual research minutes / workflow impact when known.

Unknown facts should be left blank rather than guessed. Do not include an exact civic address.

The ProjectPermit side then normalizes those human-readable facts into the canonical `data/historical_benchmark_template.csv` shape. The normalization step must not change the historical determination, sample composition or sampling method merely to improve agreement.

This is the preferred path for non-technical experts willing to share de-identified scopes.

### 2. Canonical CSV + hosted HTTP preview

For a contributor comfortable with structured JSON fields, start directly from:

`data/historical_benchmark_template.csv`

After normalizing each anonymized scope into structured `project_facts_json` (and, only when required, de-identified `property_facts_json`), a partner can benchmark historical cases against the live developer-validation endpoint without an API key, wallet, MCP client, Jobber/ServiceM8 adapter, or other platform integration:

```bash
pip install -e .
python scripts/run_remote_historical_benchmark.py path/to/partner_cases.csv \
  --output path/to/partner_cases.evaluated.csv \
  --client-tag partner-pilot-01
```

Use a stable non-PII `--client-tag`. The server hashes it before telemetry is written; do not use a customer/person name, email, civic address, account id, or other identifying value.

The hosted runner uses the free HTTP route `POST /v1/preview-project-requirements`. That route's schema does not accept `address` or `resolve_address`, so historical benchmark files cannot accidentally trigger a civic-address/GIS lookup. If a rule depends on address-derived facts, resolve them in the partner's authorized workflow and retain only the de-identified facts needed to reproduce the decision in `property_facts_json`.

### 3. Fully private local benchmark — raw cases never leave partner machine

For a contributor who does not want historical case details to leave its machine, follow:

`docs/PRIVATE_E3_BENCHMARK.md`

Run the local deterministic evaluator:

```bash
python scripts/run_partner_e3_cases.py path/to/partner_cases.csv
```

Then, after human materiality review, export only the aggregate report with:

```bash
python market_research/private_e3_aggregate.py \
  path/to/partner_cases.evaluated.csv \
  --output private_e3_summary.json
```

The raw/evaluated CSV can remain private permanently. The shareable aggregate excludes partner/source name, case IDs, scope summaries, addresses, project/property facts, notes and row-level error records. A private aggregate counts as E3 only with the required external sampling attestation described in `docs/PRIVATE_E3_BENCHMARK.md`.

## Deterministic evaluation behavior

Both canonical evaluation paths fill deterministic ProjectPermit result fields such as:

- `projectpermit_determination`
- `projectpermit_confidence`
- `agreement`
- `false_likely_not_required`

The local runner also records unsupported-family/jurisdiction flags. Exact agreement automatically records `material_disagreement=no`. Any actual disagreement intentionally leaves `material_disagreement` blank so it must receive a fresh human review; a re-run clears stale/pre-filled materiality values on disagreements.

The remote runner likewise never auto-labels a disagreement as harmless: when determinations disagree, `material_disagreement` remains blank for human review.

Then record the human judgment fields that cannot safely be inferred automatically, especially `material_disagreement`, and audit the benchmark:

```bash
python scripts/summarize_historical_benchmark.py path/to/partner_cases.evaluated.csv
```

## What qualifies

An E3 benchmark must contain at least 5 usable historical cases from one partner/platform and should be representative of a bounded recent workflow window rather than hand-picked success examples.

The summarizer marks a partner/platform benchmark `e3_qualified=true` only when:

- at least 5 cases are marked usable;
- all usable cases have the same bounded sample window and sampling method;
- sampling is not explicitly hand-picked/curated/selected-successes;
- case ids are unique;
- jurisdiction and project family are present;
- a de-identified scope summary is present;
- `project_facts_json` is valid JSON and its `family` matches `project_family`;
- historical and ProjectPermit determinations are recorded;
- agreement/material-disagreement fields are explicit;
- address-aware cases include de-identified `property_facts_json` sufficient to reproduce the rule decision.

`OUT_OF_SCOPE` is intentionally retained as a valid ProjectPermit benchmark output. Removing unsupported cases from a representative historical sample would bias the evidence. An out-of-scope case should normally be recorded as a disagreement and then assessed for material workflow impact.

## Privacy boundary

Do not put any of the following into the benchmark CSV or human-readable intake:

- customer/person names;
- email addresses or phone numbers;
- exact civic addresses;
- invoice/payment/contract values or account identifiers;
- raw platform payloads containing customer/contact fields.

For address-aware rules, resolve the address in the authorized workflow and retain only derived non-PII facts required by the deterministic engine, for example heritage/zoning/property flags. The benchmark should remain reproducible without preserving the original customer address.

The E3 runners themselves perform no address lookup and accept no raw address field. They evaluate only the already-de-identified structured facts in the CSV.

## Recommended sampling

Preferred methods:

- chronological consecutive cases from a stated recent window;
- random sample from a stated recent window;
- all eligible cases from a stated recent window;
- systematic sample with a documented rule.

Do not call a benchmark E3 if the partner or ProjectPermit team selected only cases expected to succeed.

## Determination vocabulary

Historical benchmark decisions should use:

- `REQUIRED`
- `LIKELY_NOT_REQUIRED`
- `MUNICIPAL_CONFIRMATION_REQUIRED`

ProjectPermit may also return:

- `OUT_OF_SCOPE`

The summarizer derives the most important safety metric directly from determinations: a historical `REQUIRED` case returned as `LIKELY_NOT_REQUIRED` is counted as `false_likely_not_required` regardless of a manually entered flag.

## What E3 does not prove

Passing this audit does not mean the product has demand or commercial scale.

E3 is historical benchmark evidence only. It does not count as:

- E4 repeated external live usage;
- a 500/2,000/10,000 calls-per-month path;
- E5 willingness to pay or integration resource commitment.

The desired chain remains:

`E2 bounded workflow -> E3 representative historical benchmark -> E4 repeat live usage -> E5 economic behavior`
