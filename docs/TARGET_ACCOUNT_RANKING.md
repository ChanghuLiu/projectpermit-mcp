# ProjectPermit Target Account Ranking

Updated: 2026-08-27

The first 20 target accounts are ranked for **learning value and repeated API-call potential**, not prestige.

## Score model

Each target is scored on five positive dimensions plus a competitive-overlap adjustment:

- `pain proximity` (0-5): how directly the product touches the permit-decision problem;
- `repeat density` (0-5): likelihood the workflow repeats across many jobs/work orders/projects;
- `integration readiness` (0-5): existing APIs / marketplace integration behavior;
- `distribution leverage` (0-5): ability to expose ProjectPermit to many end customers;
- `contactability` (0-3): public direct email/phone/contact route;
- `overlap adjustment` (0 to -2): penalty when the target already sells a full permit-research product and may treat the capability as competitive.

The score is directional. It is designed to choose who to contact first, not to estimate revenue.

## Ranked targets

| Rank | Target | Ecosystem | Pain | Repeat | Integration | Leverage | Contact | Overlap | Total | Why contact now |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | iPermit | ServiceTitan | 5 | 5 | 5 | 4 | 3 | 0 | **22** | Direct permit workflow; public 80+ jobs/month contractor example |
| 2 | ServiceChannel | ServiceTitan | 4 | 5 | 5 | 5 | 2 | 0 | **21** | Multi-location facilities work orders already flow into ServiceTitan |
| 3 | Property Meld | AppFolio | 5 | 5 | 5 | 4 | 2 | 0 | **21** | Maintenance work-order routing is an ideal upstream decision point |
| 4 | Lula | AppFolio | 4 | 5 | 5 | 4 | 3 | 0 | **21** | Contractor network + Partner API + high-frequency maintenance |
| 5 | HappyCo | AppFolio | 4 | 5 | 5 | 5 | 2 | 0 | **21** | Large multifamily maintenance/inspection footprint and APIs |
| 6 | AppWork | AppFolio | 4 | 5 | 5 | 3 | 3 | 0 | **20** | Structured work orders/inspections with direct sales contact |
| 7 | PermitFlow | Procore / permit tech | 5 | 5 | 5 | 4 | 3 | -2 | **20** | Best test of whether upstream triage is useful to full permitting platforms |
| 8 | Provizual | Procore | 4 | 4 | 5 | 3 | 3 | 0 | **19** | Already consumes AHJ permit-inspection activity inside Procore |
| 9 | SyncEzy | Procore integrator | 3 | 4 | 5 | 4 | 3 | 0 | **19** | Reusable integration partner serving many Procore customers |
| 10 | Banner | AppFolio | 4 | 4 | 5 | 4 | 2 | 0 | **19** | CapEx project creation can trigger permit preflight before commitments |
| 11 | CompanyCam | ServiceTitan | 2 | 4 | 5 | 5 | 3 | 0 | **19** | Broad contractor distribution; weaker direct permit pain |
| 12 | ArcSite | ServiceTitan | 3 | 4 | 5 | 4 | 2 | 0 | **18** | Scope/takeoff data exists at estimate time, before work begins |
| 13 | Contractor Commerce | ServiceTitan | 3 | 4 | 5 | 4 | 2 | 0 | **18** | Online quote journey captures scope/address before booking |
| 14 | Outbuild | Procore | 3 | 3 | 5 | 4 | 3 | 0 | **18** | 2,777 marketplace installs; permit dependency could become schedule roadblock |
| 15 | Titan Pro Technologies | ServiceTitan consultant | 4 | 4 | 4 | 4 | 2 | 0 | **18** | Can validate pain across multiple ServiceTitan contractor clients |
| 16 | Calance | Cross-platform integrator | 3 | 4 | 5 | 4 | 2 | 0 | **18** | Builds custom Procore/AppFolio/Autodesk/Northspyre integrations |
| 17 | Pulley | Procore / permit tech | 5 | 4 | 5 | 3 | 3 | -2 | **18** | Strong product-boundary learning; direct full-permitting overlap |
| 18 | Northspyre | AppFolio / development | 3 | 3 | 4 | 4 | 3 | 0 | **17** | Open API and development workflow, but permit decision frequency less clear |
| 19 | BuildPass | Procore | 2 | 3 | 5 | 3 | 3 | 0 | **16** | Strong compliance integration, weaker building-permit adjacency |
| 20 | Join | Procore | 2 | 3 | 5 | 3 | 3 | 0 | **16** | Scope/design decision layer; permit need is plausible but not proven |

## Recommended first 8 conversations

The first wave should maximize **different workflow hypotheses**, not send eight variants to near-identical companies:

1. **iPermit** — full permit workflow receives contractor jobs;
2. **ServiceChannel** — multi-location facilities work-order intake;
3. **Property Meld** — property maintenance coordination;
4. **Lula** — contractor dispatch network / Partner API;
5. **HappyCo or AppWork** — multifamily inspection/maintenance operations;
6. **Provizual** — downstream AHJ/inspection workflow;
7. **PermitFlow** — full software permitting platform / upstream-routing test;
8. **SyncEzy or Calance** — integration consultancy that can validate pain across many clients.

If all eight say the permit decision is already known before their system sees a job, ProjectPermit's upstream wedge is weaker than expected and should be reconsidered before further outreach.

## Call-density bands to ask each target about

Do not ask only “would you use this?”. Ask them to place the workflow into a monthly band:

- `<100 candidate decisions/month` — weak unless strategic;
- `100-500/month` — useful pilot;
- `500-2,000/month` — meaningful integration;
- `2,000-10,000/month` — strong design partner;
- `10,000+/month` — platform-scale distribution path.

A target may have a high fit score but low actual call volume. Real observed frequency overrides this ranking immediately.

## Coverage request rule

When a target asks for unsupported jurisdictions, record both:

- requested jurisdictions;
- expected monthly permit-decision calls in those jurisdictions.

Do **not** implement a requested city merely because a prospect mentions it. Prioritize a new jurisdiction when the prospect can attach credible repeated volume to the request.

Example decision logic:

- `Phoenix requested, 20 calls/month` -> wait;
- `Phoenix + Dallas + Los Angeles requested, 4,000 calls/month combined` -> high priority;
- `one design partner requests 10,000 calls/month across 6 U.S. cities` -> expansion gate passed.

## Contact source registry

The machine-readable target list is `data/partner_targets.csv`. Public contact paths were taken from current official product/marketplace pages including ServiceTitan Marketplace, AppFolio Stack, Procore Marketplace and vendor websites. Re-verify contact details immediately before sending external outreach.
