# NRC Deterministic Compliance Horizon — 2026-08-28

## Why this matters

Canada has now explicitly funded the architectural direction ProjectPermit relies on — deterministic, auditable, machine-readable construction-rule evaluation — even though the federal use case is a different layer of the permitting workflow.

Innovation, Science and Economic Development Canada's Innovative Solutions Canada challenge, sponsored by the National Research Council (NRC), sought Canadian automated compliance-checking solutions for building permit applications.

Official source:

- `https://ised-isde.canada.ca/site/innovative-solutions-canada/en/deterministic-artificial-intelligence-assisted-compliance-checking-building-permit-applications`

The challenge opened July 7, 2026 and closed August 5, 2026. It is no longer an application opportunity for ProjectPermit.

## What NRC is funding

The challenge is for Automated Compliance Checking (ACC) of:

- 2D permit drawings such as PDF/CAD;
- BIM / IFC building models;
- structured or unstructured data normally present in a Canadian building-permit submission.

Mandatory architecture includes:

- deterministic components using machine-readable construction codes, executable rules and/or construction-code ontologies;
- human-in-the-loop decision support;
- traceability and auditability against applicable code provisions;
- ingestion of digitalized construction-code sources and amendments;
- compatibility with structured code formats such as XML/DITA, JSON/JSON-LD, TTL/RDF and machine-executable logical expressions.

Additional desired outcomes include:

- open APIs for programmatic queries/workflow initiation;
- exchange with permitting systems through APIs or other automated mechanisms;
- source-linked compliance results;
- bilingual Canadian code support;
- target accuracy of at least 90% for simple digitalized rules and 80% for complex rules.

NRC expects a virtual integration test with its digital construction codes.

## Funding / commercialization signal

The challenge can fund up to **two Phase 2 grants of CAD $500,000 each**, with projects lasting up to 18 months.

More strategically important than the grant amount: NRC states that machine-readable National Codes will be made available to grant recipients and that it is **updating the licensing and distribution approach for commercial use of machine-readable codes**.

That means one historical source of implementation friction — converting prose construction codes into machine-consumable rules — may become materially cheaper for future Canadian compliance vendors.

## What this does NOT prove

This is not the same product as ProjectPermit's current narrow contract.

NRC's target workflow is approximately:

`permit application / drawing / BIM already exists`

→ `does the submitted design comply with applicable building-code provisions?`

ProjectPermit's remaining wedge is earlier:

`unfiled renovation scope + municipality/address + decisive facts`

→ `does this work appear to require a permit here?`

The first question assumes a permit/compliance-review workflow has already begun. The second asks whether one is required in the first place.

The NRC challenge therefore does **not** justify treating a future ACC recipient as an exact competitor unless it expands upstream into municipal permit-applicability determination.

## Why it still pressures defensibility

Even with the workflow distinction, this initiative weakens any thesis that ProjectPermit's moat is simply:

- deterministic rule execution;
- code citations;
- human-in-the-loop uncertainty handling;
- machine-readable rule ingestion;
- API delivery.

The federal challenge now describes those patterns as desired industry architecture and may subsidize Canadian companies to build them.

ProjectPermit's durable value therefore has to come from the hard combination of:

1. municipality-specific applicability coverage;
2. maintained local amendments/bylaws/source provenance;
3. a normalized cross-jurisdiction input/output contract;
4. correctness on real pre-quote scopes;
5. enough repeated buyer volume to justify external procurement;
6. maintenance economics that beat buyer-built narrow rules.

## Competitive watch trigger

When NRC/ISC announces Phase 2 recipients, each funded company should be screened for:

- existing permit-preflight or permit-requirement products;
- municipality/bylaw coverage beyond national/provincial code compliance;
- open developer API / MCP / white-label delivery;
- contractor/AEC pre-submission workflow positioning;
- ability to answer `permit required?`, not merely `design compliant?`;
- pricing/commercial licensing of deterministic Canadian rules.

A funded company crossing into the upstream applicability layer would be materially more important than another generic permit-record API.

## Score implication

**No immediate Go/No-Go score change; canonical score remains 51/100.**

Reason:

- the challenge is adjacent downstream compliance, not the exact pre-application decision contract;
- no Phase 2 recipient is yet identified here as a delivered applicability competitor;
- ProjectPermit's defensibility and competitive-headroom scores are already low, so another architecture-level warning should not be double-counted.

### Score-moving future events

Negative:

- a funded ACC vendor exposes cross-municipality `permit required?` determination through a reusable API;
- machine-readable municipal applicability rules become standardized/cheap enough that contractor platforms can internalize ProjectPermit's layer with little maintenance burden;
- buyers explicitly prefer an NRC-funded/general compliance platform over a separate applicability API.

Positive:

- funded ACC vendors stay downstream and do not want to maintain local applicability logic;
- they identify upstream permit applicability as a missing external dependency;
- a funded vendor/integrator explicitly prefers consuming a maintained cross-city applicability service rather than building it.

## Bottom line

The federal program validates deterministic, auditable construction-rule automation as a serious Canadian technology direction — but simultaneously makes that architecture less defensible as a standalone moat.

ProjectPermit must therefore stay focused on proving the **commercial value and maintenance burden of the upstream municipal applicability layer**, not on claiming that deterministic rule engines themselves are rare.