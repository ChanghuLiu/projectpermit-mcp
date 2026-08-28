# Operator Rescue Metrics Usage — 2026-08-28

This note accompanies `docs/OPERATOR_RESCUE_PILOT_PROTOCOL_20260828.md`.

The metrics script is a **denominator/consistency guard**, not an evidence-upgrade engine.

## Inputs

Start from copies of:

- `data/operator_rescue_monthly_aggregate_template.csv`
- `data/operator_rescue_pilot_sample_template.csv`

The monthly file must describe exactly one operator and one complete month. Keep these denominators separate:

1. `unique_requests` — unique homeowner/project requests in the current family;
2. `within_supported_jurisdictions` — unique requests inside current ProjectPermit geographic coverage;
3. `candidate_preflight_requests` — requests where the target workflow would actually call ProjectPermit;
4. `unresolved` — candidate requests whose permit applicability was unresolved at the insertion point;
5. `partner_deliveries` — downstream copies sold/routed to partners; never substitute this for unique upstream requests.

For sampled historical cases, explicitly populate:

- `within_supported_jurisdiction=yes/no`;
- `candidate_preflight=yes/no`.

A case cannot be a ProjectPermit candidate when it is outside current supported jurisdictions.

## Run

```bash
python market_research/operator_rescue_metrics.py \
  path/to/monthly.csv \
  --sample path/to/sample.csv \
  --json-output /tmp/operator-rescue.json \
  --decision-csv /tmp/operator-rescue-decision.csv
```

## Automatic consistency checks

The script rejects, among other things:

- candidate calls above supported-jurisdiction requests;
- unresolved cases above candidate calls;
- material-effect counts above candidate calls;
- fully populated mutually exclusive permit-state counts summing above unique requests;
- inconsistent `delivery_multiplier` vs `partner_deliveries / unique_requests`;
- duplicate sample IDs;
- candidate samples explicitly outside supported jurisdictions;
- invalid family / permit-state / fact-sufficiency / material-effect / integration-topology enums.

## Mechanical outputs

Important calculated fields include:

- `candidate_share_of_unique_pct`;
- `unresolved_share_of_candidate_pct`;
- `decision_fact_sufficiency_rate_pct` over sampled **candidate** cases;
- `material_hit_rate_pct` over sampled **candidate** cases;
- `commercial_500_call_gate` based only on `candidate_preflight_requests`;
- `central_integration_plausible`, true only when a central topology is explicitly reported and no separate-site topology is present.

`advance_to_e4_mechanical_screen=true` requires all of:

- >=500 candidate preflight requests/month;
- at least one unresolved candidate in the aggregate;
- an explicitly central integration topology;
- sampled candidate cases;
- non-zero candidate fact sufficiency;
- at least one confirmed material effect on a candidate case;
- zero recorded material less-conservative safety disagreements.

This is intentionally conservative, but it is still only a mechanical screen.

## Evidence boundary

The script does **not** decide that a claim is E2, a sample is representative E3, calls are independent E4, or a commitment is E5. Those require provenance and external evidence review under the canonical evidence standard.

The generated decision row therefore defaults to `evidence_level=E0`.

The script also never sets `renew_engineering=YES`. Restarting product/jurisdiction engineering remains a human commercial decision requiring the protocol's external evidence gates.
