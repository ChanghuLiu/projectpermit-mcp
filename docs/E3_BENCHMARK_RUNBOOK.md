# E3 Historical Benchmark Runbook

Updated: 2026-08-27

Purpose: turn partner-supplied anonymized historical cases into reproducible E3 evidence without storing customer PII or inflating weak samples into market validation.

## Workflow

Start from `data/historical_benchmark_template.csv`.

After normalizing each anonymized scope into structured `project_facts_json` (and, only when required, de-identified `property_facts_json`), choose one of two evaluation paths.

### Local deterministic engine

For a contributor who has cloned the repository:

```bash
python scripts/run_partner_e3_cases.py path/to/partner_cases.csv
```

This writes `partner_cases.evaluated.csv` by default and refuses to overwrite the source file.

### Free hosted HTTP preview — no platform integration required

A partner can benchmark historical cases against the live developer-validation endpoint without an API key, wallet, MCP client, Jobber/ServiceM8 adapter, or other platform integration:

```bash
pip install -e .
python scripts/run_remote_historical_benchmark.py path/to/partner_cases.csv \
  --output path/to/partner_cases.evaluated.csv \
  --client-tag partner-pilot-01
```

Use a stable non-PII `--client-tag`. The server hashes it before telemetry is written; do not use a customer/person name, email, civic address, account id, or other identifying value.

The hosted runner uses the free HTTP route `POST /v1/preview-project-requirements`. That route's schema does not accept `address` or `resolve_address`, so historical benchmark files cannot accidentally trigger a civic-address/GIS lookup. If a rule depends on address-derived facts, resolve them in the partner's authorized workflow and retain only the de-identified facts needed to reproduce the decision in `property_facts_json`.

Both evaluation paths fill deterministic ProjectPermit result fields such as:

- `projectpermit_determination`
- `projectpermit_confidence`
- `agreement`
- `false_likely_not_required`

The local runner also records unsupported-family/jurisdiction flags. The remote runner preserves all source columns and never auto-labels a disagreement as harmless: when determinations disagree, `material_disagreement` remains blank for human review.

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

Do not put any of the following into the benchmark CSV:

- customer/person names;
- email addresses or phone numbers;
- exact civic addresses;
- invoice/payment values or account identifiers;
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
