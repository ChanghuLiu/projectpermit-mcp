# Canadian permit-data API procurement boundary — 2026-08-28

## Question

Is ProjectPermit accidentally rebuilding a Canadian permit-data API that can already be purchased cheaply, or is the remaining product thesis a different layer?

## Finding

Canada already has multiple commercial/public products that normalize **issued / filed building permit records** across municipalities. This data layer is increasingly commoditized.

Examples found in the current scan:

### Neighbourly / PermitAtlas

Neighbourly exposes Canadian address-keyed permit history through REST/JSON with a normalized permit taxonomy. Public material names Toronto, Vancouver, Calgary and Ottawa as high-density coverage, Mississauga as growing coverage, and additional cities under expansion.

PermitAtlas exposes the same/related Neighbourly-powered permit-record layer for developers, including permits by location, statistics and normalized JSON.

Neighbourly also publishes self-serve pricing for broader enriched-address access, including a Starter tier at CAD $299/month or a stated $0.04 per enriched address, with higher-volume tiers. The exact layer entitlements should be confirmed before procurement because public pricing/table presentation varies by tier.

Sources:
- https://neighbourly.io/building-permit-data-api
- https://neighbourly.io/developers
- https://neighbourly.io/pricing
- https://permitatlas.ca/developers

### RenoIntel

RenoIntel says it aggregates/normalizes Canadian renovation and construction permit/project intelligence, including early-stage and issued activity, geocoding/category enrichment and API access for CRM/marketing workflows.

Current 2026 product pages advertise a live Canadian project database, permit/project-stage signals and API delivery to builders, suppliers and other commercial users.

Sources:
- https://renointel.ca/
- https://renointel.ca/for/builder-programs.html

### SiteWire

SiteWire currently advertises Canadian permit intelligence across **31 cities**, including filed/pre-permit signals in major cities, normalized permit/project feeds, REST API access, webhooks and up to 10,000 API requests/day on its national Pro tier.

Its commercial purpose is explicitly sales/project intelligence: discover permit applications and issued projects early, filter them, and push those records into contractor/CRM workflows.

Sources:
- https://sitewire.ca/
- https://sitewire.ca/enterprise

This is strong evidence that Canadian **permit-record / filed-application intelligence** is already a real API market. It is not evidence of the separate pre-application applicability contract ProjectPermit is testing.

### BuildPermitData

BuildPermitData advertises a normalized Canadian permit record with stable IDs, municipal provenance, lifecycle stage, project classification, scope flags and REST/API or file delivery.

Source:
- https://buildpermitdata.ca/inside-the-data/

### Cloudpermit

Cloudpermit exposes APIs around municipal permitting workspaces, inspections, GIS/property attributes, fees and application data. It is municipal permitting infrastructure, not a pre-quote permit-applicability supplier.

Sources:
- https://cloudpermit.ca/products/building-permitting
- https://cloudpermit.ca/products/planning

## What these suppliers already commoditize

Do **not** position ProjectPermit around any of the following as a unique moat:

- historical permit records;
- filed / pre-permit application feeds;
- permit counts / market activity;
- normalized issued-permit taxonomy;
- address-keyed permit history;
- permit status/lifecycle data;
- basic geocoding or property enrichment;
- permit-data CRM feeds / alerts / webhooks;
- municipal application/workspace infrastructure.

Those layers can already be sourced commercially and, in many cities, ultimately derive from open municipal records.

## What was NOT found in this scan

No current Canadian supplier was found whose public API contract takes an **unfiled renovation scope before quote/application** and returns a municipality-specific deterministic result equivalent to:

- `REQUIRED`;
- `LIKELY_NOT_REQUIRED`;
- `CONFIRM`;

with the decisive scope facts, maintained municipal rules and auditable official-source evidence.

The closest exact conceptual analogues found previously remain outside the Canadian current product boundary (for example U.S.-oriented permit-requirements/preflight products), while Canadian products such as LandLogic, BuilderAI and RealCraft overlap through zoning/guidance/embedded permit content rather than a clearly documented external deterministic applicability API.

Absence from public search is **not proof that no private/internal supplier exists**. A credible buyer or platform saying it already purchases such a capability would be score-moving evidence.

## Strategic boundary

The product thesis must stay at the **pre-application decision layer**:

`new project scope + municipality/address + decisive project facts`

→ `does this work appear to require a permit here?`

not:

`address -> what permits were historically issued / filed?`

The latter is already a competitive data market.

## Potential complement, not current build task

Historical permit/property APIs could later be useful as optional enrichment or a validation data source. They should not be integrated merely because they exist.

Any paid dependency must first show one of:

- partner-requested need;
- measurable E3/E4 accuracy/workflow benefit;
- lower total cost than maintaining the equivalent first-party adapter;
- a credible external workflow large enough to justify recurring spend.

ProjectPermit currently has no reason to incur a paid permit-data dependency solely for validation.

## Score implication

**No Go/No-Go score change; canonical score remains 50/100, PAUSE / RE-SCOPE.**

Reason:

- the canonical scorecard now rates competitive headroom at **0/10** after the later Parcella / One Ontario delivery review;
- permit-record normalization is adjacent/downstream and was never the remaining claimed moat;
- the refreshed SiteWire/RenoIntel evidence strengthens the conclusion that this adjacent data layer is commoditized, but it does not prove demand for pre-application applicability;
- no new Canadian public API with ProjectPermit's exact pre-application deterministic contract was found in this refresh.

A newly discovered Canadian API with the exact pre-application deterministic contract and viable pricing would be materially different and should trigger an explicit score/re-scope review.

For score changes, `docs/GO_NO_GO_SCORECARD.md` is the canonical source. Research addenda should state their directional implication and update that scorecard explicitly if a score change is warranted rather than carrying an independent competing score.
