# Private local E3 benchmark

Updated: 2026-08-27

Use this path when a builder, estimator, consultant, platform operator or adjacent permit company is willing to benchmark ProjectPermit but does **not** want historical case details, customer scopes or internal volume data to leave its machine.

The private path uses the **same canonical E3 rules** as `docs/E3_BENCHMARK_RUNBOOK.md`. It does not lower the evidence standard and does not create a second benchmark definition.

## What leaves the partner machine

Only an aggregate JSON report, plus a short sampling attestation.

The aggregate report does **not** contain:

- partner/source-platform name;
- case IDs;
- scope summaries;
- exact addresses;
- project/property fact JSON;
- notes;
- customer names/contact data;
- row-level error details.

It does contain aggregate counts needed to detect unsafe or unrepresentative results, including:

- usable/comparable case count;
- agreement rate;
- material disagreements;
- false `LIKELY_NOT_REQUIRED` count;
- confirmation and `OUT_OF_SCOPE` outputs;
- sample window and sampling method;
- aggregate jurisdiction/family counts;
- address-aware-case count;
- aggregate manual-research minutes;
- aggregate workflow-changed count;
- canonical E3 validator pass/fail;
- SHA-256 of the evaluated local CSV so the same private file can be re-identified/reproduced later without disclosing it.

## Evidence rule

A private aggregate is **not E3 by itself**.

To count as E3, the partner must also attest that:

1. the sample came from one fixed historical window;
2. the sampling method was chronological/systematic/otherwise representative and defined **before** seeing ProjectPermit outputs;
3. cases were not hand-picked for success;
4. no sampled case was removed because ProjectPermit disagreed, returned `OUT_OF_SCOPE`, or produced an unfavorable result;
5. the historical determination is based on the real historical/manual outcome, not rewritten to match ProjectPermit.

Recommended one-line attestation:

> I confirm this sample covers `[start]` to `[end]`, was selected using `[chronological/systematic method]` before reviewing ProjectPermit outputs, and no sampled case was removed because of the benchmark result.

Partner identity can be established by the email/thread carrying that attestation; it does not need to be embedded in the JSON.

## Minimum sample

Canonical minimum: **5 usable cases**.

Preferred first benchmark: **10–20 consecutive/systematically selected cases** when available.

Do not cherry-pick only cases that fit ProjectPermit's current families. A representative sampled case that is genuinely unsupported should remain in the sample as `OUT_OF_SCOPE` negative evidence.

## Local-only workflow

Clone the public repository and install the deterministic engine locally:

```bash
git clone https://github.com/ChanghuLiu/projectpermit-mcp.git
cd projectpermit-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Copy the benchmark template:

```bash
cp data/historical_benchmark_template.csv private_cases.csv
```

Replace/delete the example row and enter the representative historical sample.

Privacy rules for `private_cases.csv`:

- no customer names;
- no email/phone;
- no invoice/contract value;
- no exact civic addresses;
- no free-text PII;
- for an address-aware case, store only derived non-identifying property facts actually needed by the rules engine.

The raw/private CSV stays local.

## Run ProjectPermit locally

```bash
python scripts/run_partner_e3_cases.py private_cases.csv \
  --output private_cases.evaluated.csv
```

This calls the local deterministic rules engine. It does **not** call the ProjectPermit production API/MCP and does not upload the cases.

The runner automatically writes `material_disagreement=no` for exact historical/ProjectPermit agreement. For every disagreement, it intentionally leaves `material_disagreement` blank so the case must receive a fresh human review; stale/pre-filled materiality values are cleared on re-run.

For every disagreement, review the historical/manual record locally and fill `material_disagreement=yes|no` in `private_cases.evaluated.csv`.

Do not change/remove a case merely because the result is unfavorable.

A historical `REQUIRED` case that ProjectPermit marks `LIKELY_NOT_REQUIRED` is a critical false-negative signal and must remain in the sample.

## Run the canonical E3 audit locally

```bash
python scripts/summarize_historical_benchmark.py private_cases.evaluated.csv
```

The canonical summary should show `e3_qualified: true` for the benchmark before it is presented as qualifying E3 evidence.

If it fails due to missing required fields, fix the missing metadata/facts without changing the sample composition or benchmark outcomes.

## Export only the private aggregate

```bash
python market_research/private_e3_aggregate.py \
  private_cases.evaluated.csv \
  --output private_e3_summary.json
```

Review `private_e3_summary.json` before sharing it.

The partner may share only:

1. `private_e3_summary.json`; and
2. the one-line sampling attestation above.

The raw CSV and evaluated CSV can remain private permanently.

## How ProjectPermit classifies the result

### E3-qualified private benchmark

Count as E3 only when all are true:

- canonical validator says qualified;
- at least 5 usable cases;
- one bounded sample window;
- one acceptable sampling method;
- no duplicate identifiers;
- no invalid cases;
- external partner attests representative/non-hand-picked sampling;
- unfavorable results and `OUT_OF_SCOPE` cases were retained.

### Not E3

Do not count as E3 when:

- sample is curated/hand-picked;
- sample window is undefined;
- only aggregate opinions are supplied with no historical benchmark;
- partner cannot attest how cases were sampled;
- failures/disagreements were removed;
- the benchmark was constructed from synthetic cases;
- public municipal backtests are substituted for a partner's representative historical workflow.

## What E3 still does not prove

Even a strong private E3 benchmark does **not** prove:

- repeated operational use (E4);
- buyer willingness to pay/resource commitment (E5);
- monthly candidate-call volume;
- that permit applicability is unresolved at the target Request/Assessment/Quote stage.

Those must remain separate evidence gates.

## Why this path exists

The goal is to remove an unnecessary validation blocker:

> a partner should be able to prove whether ProjectPermit is accurate on representative real work **without giving ProjectPermit its internal case dataset**.

Privacy protection is not permission to weaken sampling discipline.
