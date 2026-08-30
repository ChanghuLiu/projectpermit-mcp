# Active Layer-C buyer evidence scorecard — 2026-08-30

## Purpose

Prevent qualitative-positive outreach replies from being mistaken for E2/E3 market evidence.

Every active buyer thread is scored on the same dimensions:

1. `RECENT_FREQUENCY` — bounded recent denominator, preferably `last 20 estimates` or a similarly concrete recent window;
2. `MATERIAL_CONSEQUENCE` — evidence that the regulatory result changes quote price/scope/schedule/professional/document/inspection/handoff/no-go;
3. `RESEARCH_BURDEN` — who does the work and how much repeated time/maintenance it consumes;
4. `EXTERNALIZATION` — buyer preference to buy/call a maintained external layer rather than maintain all logic/currentness internally;
5. `PAYMENT_PATH` — a plausible natural commercial unit the buyer says they would accept;
6. `REPRESENTATIVE_E3` — a real/sanitized work record or direct buyer-recognized example suitable for a representative prototype;
7. `REAL_USE` — substantive successful external ProjectPermit usage;
8. `PAYMENT` — real economic commitment/payment.

The scorecard is deliberately strict.

Public market research, platform scale, competitor precedents and generic workflow anecdotes do **not** fill buyer-specific cells.

## Current active threads

| Lead | Recent frequency | Material consequence | Research burden | Externalization | Payment path | Representative E3 | Real use | Payment | Current class |
|---|---|---|---|---|---|---|---|---|---|
| SubmitX / AutoSubmitX | ❌ | ❌ | partial qualitative only | ⚠️ qualitative boundary | ❌ | ❌ | ❌ | ❌ | E1 only |
| Contrax / Cameron | ❌ | ❌ | ❌ | ✅ qualitative boundary for maintained regulations/code; ❌ for narrow permit yes/no | ❌ | ❌ | ❌ | ❌ | E1 only |
| Join | ❌ | ❌ | ❌ | ❌ no reply | ❌ | ❌ | ❌ | ❌ | outreach only |
| BuildPass | ❌ | ❌ | ❌ | ❌ no reply | ❌ | ❌ | ❌ | ❌ | outreach only |
| Pacific Coast Contracting (PCC) | ❌ pending | public workflow evidence only — not buyer reply | public maintenance evidence only — not buyer reply | ❌ pending | ❌ | ❌ | ❌ | ❌ | P0 target / no E-level |

## 1. SubmitX / AutoSubmitX

### What exists

SubmitX provided a substantive qualitative reply to the earlier build-vs-buy question.

The reply supports the boundary that:

- some light municipal / Québec-specific legislative logic is already integrated or maintained internally / through existing AI/tooling;
- the usefulness of an external capability depends on it offering a deeper maintained layer rather than merely duplicating simple logic.

A follow-up asked for a bounded monthly workflow denominator.

### What is still missing

- no bounded monthly/recent frequency;
- no count of recent estimates/projects affected;
- no measured quote/scope/schedule consequence;
- no time/research burden;
- no payment structure;
- no representative work record;
- no ProjectPermit use.

### Classification

**E1 qualitative build-vs-buy evidence only.**

Do not upgrade based on the fact that the response was thoughtful or technically informed.

## 2. Contrax / Cameron

### What exists

Cameron's response gave the cleanest qualitative product boundary so far:

- narrow `do I need a permit?` logic would likely be built internally because that can be faster/cheaper and fit their own workflow;
- an external API providing **updated legal requirements / regulations / building-code information** would be materially more useful.

A follow-up asked for a bounded normal-month workflow range.

### What is still missing

- no recent/monthly denominator;
- no count of affected estimates;
- no measured material quote/scope/schedule consequence;
- no research-time burden;
- no natural payment unit;
- no representative record;
- no real use/payment.

### Classification

**E1 externalization-boundary evidence only.**

It strongly influences what to validate, but does not establish market volume.

## 3. Join

A bounded preconstruction-workflow question was sent.

As of this scorecard snapshot:

- no substantive reply;
- no denominator;
- no consequence;
- no externalization/payment evidence.

### Classification

**Outreach sent, no E-level evidence.**

## 4. BuildPass

A bounded current-regulatory-requirements-before-pricing question was sent.

As of this scorecard snapshot:

- no substantive reply;
- no denominator;
- no consequence;
- no externalization/payment evidence.

### Classification

**Outreach sent, no E-level evidence.**

## 5. Pacific Coast Contracting (PCC)

PCC is the strongest current-coverage public buyer archetype found so far because public material independently indicates:

- Vancouver is a current operating geography;
- work overlaps current ProjectPermit families such as windows/doors, interior renovation and kitchen/bath renovation;
- PCC publicly says its workflow uses Jobber/ClickUp;
- PCC publicly discusses permit timelines and local regulatory complexity;
- PCC publicly says it tracks zoning/bylaw changes weekly;
- permit/application/inspection activity appears inside its delivered renovation workflow.

A single narrow `last 20 estimates` email was sent asking only for a frequency band.

### Evidence-discipline boundary

None of the public PCC material fills buyer-specific E2 fields.

For example:

- `weekly tracking of bylaw changes` proves maintenance behavior, **not** estimates affected per month;
- lifetime project counts prove company activity, **not** current regulatory-check denominator;
- public permit/process content proves workflow relevance, **not** preference to externalize;
- use of Jobber proves integration fit, **not** willingness to pay.

### Classification

**P0 validation target; no E-level increase until PCC or an equivalent supported-city buyer provides bounded direct evidence.**

## Promotion rules

### No E2 from one positive sentence

Do not promote a lead merely because it says:

- `this would be useful`;
- `we have this problem`;
- `codes change a lot`;
- `we use AI for this`;
- `we would consider an API`.

### Minimum strong E2 package

A buyer should provide enough direct evidence to establish at least:

1. **recent bounded frequency** — e.g. `8 of last 20 estimates`;
2. **material consequence** — at least some of those estimates changed price/scope/schedule/professional/documents/inspection/handoff/no-go;
3. **repeated burden** — current research/maintenance is non-trivial;
4. **externalization preference** — buyer would rather externalize currentness/evidence/normalization than own all maintenance;
5. a plausible commercial path, even if no payment has occurred yet.

A lead with frequency but `we will build and maintain it ourselves` is weaker than a smaller-frequency lead with a clear maintained-layer buy preference.

## Suggested field interpretation

### `RECENT_FREQUENCY`

Strong:
- `8+ / last 20 estimates`

Moderate:
- `3–7 / last 20`

Weak:
- `0–2 / last 20`

Do not convert annual lifetime counts into a synthetic `last 20` denominator.

### `MATERIAL_CONSEQUENCE`

Count only buyer-confirmed effects on:

- quote price/allowance;
- quoted scope;
- engineer/architect/designer involvement;
- required documents/drawings;
- permit/approval path;
- schedule/start date;
- inspection/milestone sequencing;
- no-bid/no-go.

### `EXTERNALIZATION`

Strongest answer:

> buyer wants to keep its own judgement/UI/estimating logic but call an externally maintained source-of-truth layer for current facts/evidence/change handling.

This is especially relevant after the verified Vancity Electric DIY benchmark, which shows capable contractors can build generic permit calculators/GPTs internally.

## Current ProjectPermit status

As of this scorecard snapshot:

- buyer-specific Layer C evidence: **E1 only**;
- representative Layer C implementation: **not started**;
- real substantive external ProjectPermit usage: **E4 = 0**;
- real payment/economic commitment: **E5 = 0**.

The newly defined Vancouver license-light representative E3 slice is **readiness documentation only**. It becomes buildable only after the buyer gate is crossed.

## Stop rule

Do not respond to missing buyer evidence by:

- adding municipalities;
- broadening into electrical/fire/solar;
- buying protected code licences;
- building marketplace apps;
- adding a large obligation schema preemptively;
- counting crawler traffic as E4;
- counting public contractor anecdotes as direct buyer E2.

Continue to improve evidence quality, not scope size.