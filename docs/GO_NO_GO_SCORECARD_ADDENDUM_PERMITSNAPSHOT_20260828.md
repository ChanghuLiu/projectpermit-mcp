# Go / No-Go Addendum — PermitSnapshot — 2026-08-28

## Revised score: 50 / 100

Previous score earlier on 2026-08-28: **51 / 100**.

The only scoring change is **Defensibility: 2/10 -> 1/10** after discovering PermitSnapshot, an Ontario pre-application permit-feasibility product that materially overlaps ProjectPermit's intended decision layer.

| Dimension | Weight | Score | Weighted points |
|---|---:|---:|---:|
| Pain intensity | 15 | 8/10 | 12.0 |
| Willingness to pay / monetization fit | 15 | 4/10 | 6.0 |
| Addressable call volume | 15 | 6/10 | 9.0 |
| Repeat frequency | 10 | 5/10 | 5.0 |
| Distribution fit | 10 | 6/10 | 6.0 |
| Competitive headroom | 10 | 0/10 | 0.0 |
| **Defensibility** | **10** | **1/10** | **1.0** |
| Cash-cost fit | 5 | 9/10 | 4.5 |
| Technical feasibility | 5 | 9/10 | 4.5 |
| Evidence maturity | 5 | 3/10 | 1.5 |
| **Total** | **100** |  | **49.5 -> 50** |

## Why PermitSnapshot changes the score

PermitSnapshot publicly advertises:

- all 414 Ontario municipalities;
- address + proposed scope intake;
- pre-quote use by builders/GCs;
- permit requirements with likelihood ratings;
- confidence labels;
- source/model-version transparency;
- conservative `NOT DETERMINED` behavior;
- $49 CAD per report.

This materially overlaps the previously claimed ProjectPermit differentiation around cross-municipality preflight, conservative uncertainty and source-linked results.

See `docs/PERMITSNAPSHOT_PREAPPLICATION_THREAT_20260828.md`.

## Why the score is not below 50 yet

Current public evidence still does **not** establish that PermitSnapshot offers:

- an API/batch/white-label capability;
- high-frequency per-call economics;
- deterministic stable rule IDs;
- municipality-specific ordinary-renovation exceptions at ProjectPermit's intended granularity;
- externally benchmarked accuracy.

Its own disclaimer explicitly warns that outputs may use general Ontario regulatory context, may not reflect current municipal by-laws/site-specific exceptions, and require independent verification.

Therefore the exact ProjectPermit API contract is still not publicly proven as already purchasable.

## Decision state at 50

> **VALIDATION/FALSIFICATION ONLY — NO PRODUCT EXPANSION.**

This is no longer a normal `continue building` score.

The next materially negative qualified signal should trigger an explicit **STOP / RE-SCOPE** review rather than another score decrement followed by more speculative development.

Examples:

- PermitSnapshot confirms a suitable API/batch/white-label path;
- RealCraft/BuilderAI/QuoteXbert says internal permit guidance is cheap enough and external deterministic maintenance adds little value;
- representative E3 shows no material advantage from municipality-specific deterministic rules;
- high-volume platform says permit applicability is already resolved on >90% of relevant quote-stage projects;
- no >=500/month unresolved current-family workflow can be found after qualified platform conversations.

## No false positive from the $49 price

Do **not** count PermitSnapshot's advertised $49 price as ProjectPermit E5.

It proves only that a competitor is asking money for a broad feasibility report.

There is no verified evidence here of:

- actual paid customer count;
- repeat purchase frequency;
- willingness to pay for ProjectPermit's narrower API;
- willingness to integrate at $0.20-$0.50/call.

ProjectPermit E5 remains **0**.