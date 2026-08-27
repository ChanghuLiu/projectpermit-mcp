# ProjectPermit Target Account Ranking

Updated: 2026-08-27

Targets are ranked for **learning value and repeated API-call potential**, not prestige. A positive reply is not validation; evidence quality is governed by `docs/VALIDATION_EVIDENCE_STANDARD.md`.

## Score model

Each target is scored on five positive dimensions plus a competitive-overlap adjustment:

- `pain proximity` (0-5): how directly the product touches the permit-decision problem;
- `repeat density` (0-5): likelihood the workflow repeats across many jobs/work orders/projects;
- `integration readiness` (0-5): existing APIs / marketplace integration behavior;
- `distribution leverage` (0-5): ability to expose ProjectPermit to many end customers;
- `contactability` (0-3): public direct email/phone/contact route;
- `overlap adjustment` (0 to -2): penalty when the target already sells a full permit-research product and may treat the capability as competitive.

The score is directional. It chooses where to spend validation effort; it is not a revenue estimate.

## Ranked targets

| Rank | Target | Ecosystem | Pain | Repeat | Integration | Leverage | Contact | Overlap | Total | Why contact/build now |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | **Jobber** | Home services | 5 | 5 | 5 | 5 | 3 | 0 | **23** | Request/Quote/Job already exposes property + scope; GraphQL/OAuth/webhooks/custom fields; Canadian contractor distribution matches current geography |
| 2 | iPermit | ServiceTitan | 5 | 5 | 5 | 4 | 3 | 0 | **22** | Direct permit workflow; public 80+ jobs/month contractor example |
| 3 | ServiceChannel | ServiceTitan | 4 | 5 | 5 | 5 | 2 | 0 | **21** | Multi-location facilities work orders already flow into ServiceTitan |
| 4 | Property Meld | AppFolio | 5 | 5 | 5 | 4 | 2 | 0 | **21** | Maintenance work-order routing is an ideal upstream decision point |
| 5 | Lula | AppFolio | 4 | 5 | 5 | 4 | 3 | 0 | **21** | Contractor network + Partner API + high-frequency maintenance |
| 6 | HappyCo | AppFolio | 4 | 5 | 5 | 5 | 2 | 0 | **21** | Large multifamily maintenance/inspection footprint and APIs |
| 7 | AppWork | AppFolio | 4 | 5 | 5 | 3 | 3 | 0 | **20** | Structured work orders/inspections with direct sales contact |
| 8 | PermitFlow | Procore / permit tech | 5 | 5 | 5 | 4 | 3 | -2 | **20** | Tests whether upstream triage is useful to full permitting platforms |
| 9 | Provizual | Procore | 4 | 4 | 5 | 3 | 3 | 0 | **19** | Already consumes AHJ permit-inspection activity inside Procore |
| 10 | SyncEzy | Procore integrator | 3 | 4 | 5 | 4 | 3 | 0 | **19** | Reusable integration partner serving many Procore customers |
| 11 | Banner | AppFolio | 4 | 4 | 5 | 4 | 2 | 0 | **19** | CapEx project creation can trigger permit preflight before commitments |
| 12 | CompanyCam | ServiceTitan / home services | 2 | 4 | 5 | 5 | 3 | 0 | **19** | Broad contractor distribution; weaker direct permit pain |
| 13 | ArcSite | ServiceTitan | 3 | 4 | 5 | 4 | 2 | 0 | **18** | Scope/takeoff data exists at estimate time, before work begins |
| 14 | Contractor Commerce | ServiceTitan | 3 | 4 | 5 | 4 | 2 | 0 | **18** | Online quote journey captures scope/address before booking |
| 15 | Outbuild | Procore | 3 | 3 | 5 | 4 | 3 | 0 | **18** | Permit dependency could become an early schedule roadblock |
| 16 | Titan Pro Technologies | ServiceTitan consultant | 4 | 4 | 4 | 4 | 2 | 0 | **18** | Can validate pain across multiple ServiceTitan contractor clients |
| 17 | Calance | Cross-platform integrator | 3 | 4 | 5 | 4 | 2 | 0 | **18** | Builds custom Procore/AppFolio/Autodesk/Northspyre integrations |
| 18 | Pulley | Procore / permit tech | 5 | 4 | 5 | 3 | 3 | -2 | **18** | Strong product-boundary learning; direct full-permitting overlap |
| 19 | Northspyre | AppFolio / development | 3 | 3 | 4 | 4 | 3 | 0 | **17** | Open API and development workflow, but permit decision frequency less clear |
| 20 | BuildPass | Procore | 3 | 3 | 5 | 3 | 3 | 0 | **17** | Compliance/project setup and permit templates make applicability adjacency testable |
| 21 | Join | Procore | 3 | 3 | 5 | 3 | 3 | 0 | **17** | Preconstruction/design decision layer; permit implication could be surfaced before final choices |

## Why Jobber is now first

Jobber is unusually aligned with ProjectPermit's current footprint. Its official developer model exposes property address and request/quote/job scope at exactly the point where a permit preflight could run, and Draft custom integrations can be tested with a small number of paying accounts before a Marketplace launch. See `docs/JOBBER_DISTRIBUTION_WEDGE.md`.

This does **not** prove demand. The key unresolved question is whether experienced home-service contractors already know permit applicability cheaply enough that an automated result adds little value. That requires E3 historical cases and E4 observed use.

## Two-track validation

Platform conversations and operator evidence answer different questions:

- **Platforms/integrators** answer whether the capability fits an API/workflow and can distribute broadly.
- **Real contractors/operators** answer whether permit applicability actually consumes time, causes quote/schedule errors, and repeats often enough to pay for.

Major decisions should require the two tracks to converge. For example, a platform saying “interesting” is E1; a contractor providing 20 recent Jobber quotes with prior permit decisions is E3; repeated live calls are E4.

## Call-density bands

When a workflow is confirmed, ask for a denominator and timeframe rather than only a subjective band. Bands remain useful for triage:

- `<100 candidate decisions/month` — weak unless strategic;
- `100-500/month` — useful pilot;
- `500-2,000/month` — meaningful integration;
- `2,000-10,000/month` — strong design partner;
- `10,000+/month` — platform-scale distribution path.

A high fit score with low observed call volume is still a weak commercial target. E3/E4 evidence overrides this ranking immediately.

## Coverage request rule

When a target asks for unsupported jurisdictions, record both the requested geography and expected monthly permit-decision calls there. Do not implement a requested city merely because a prospect mentions it.

Examples:

- `Phoenix requested, 20 calls/month` -> wait;
- `Phoenix + Dallas + Los Angeles, 4,000 calls/month combined` -> high priority after historical-case evidence;
- `one workflow has 10,000 observed/candidate calls/month across 6 U.S. cities` -> expansion gate can be considered.

## Contact source registry

The machine-readable target list is `data/partner_targets.csv`. Canadian cold operator outreach has a separate compliance gate in `docs/CANADA_OUTREACH_COMPLIANCE.md` and `data/outreach_consent_registry.csv`.
