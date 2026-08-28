# LandLogic / One Ontario Threat Addendum — 2026-08-28

This addendum records evidence discovered after the initial `docs/COMPETITIVE_LANDSCAPE.md` merge. It should be read as an escalation of the Ontario competitive threat, not as a replacement for the broader matrix.

## New evidence that materially changes the threat level

### 1. LandLogic is already targeting the same third-party buyer class

LandLogic's current AI Property Lead Engine is not limited to municipalities or internal land-use professionals.

The product explicitly targets:

- **builders & developers**;
- **proptech & platforms**;
- brokerages and lenders.

It states that partners can add a branded property assistant to their own product and that the underlying data foundation already covers **80+ Ontario municipalities** with no maintenance required by the embedding partner.

Source: `https://www.landlogic.ai/ai-property-lead-engine`

This removes `third-party software buyer`, `multi-municipality Ontario coverage`, `white-label embedding`, and `vendor-maintained regulatory/property data` from the list of plausible ProjectPermit moats.

### 2. LandLogic already exposes a partner-facing API/integration surface

LandLogic's API Integration product publicly supports:

- zoning / planning / land-use / property data integration;
- automatic updates;
- custom branding;
- report embedding;
- machine-ready data for conversational-AI integrations.

Its onboarding remains engagement-led: select an API, then LandLogic experts connect it into the partner's platform/business. Conversational-AI integration is described as pilot testing with demos for interested partners.

Source: `https://www.landlogic.ai/integration`

This means ProjectPermit **cannot** claim `API integration`, `machine-ready property intelligence`, `automatic regulatory updates`, `custom branding`, or `agent/conversational use` as unique by themselves.

The remaining potentially meaningful distinction is **self-serve permit-specific access**, not API availability in general.

### 3. Parcella has entered the permit-applicability question directly

LandLogic's Parcella materials explicitly use questions such as:

> `Do I need a permit for a swimming pool?`

Parcella is described as giving property owners clear direction on what is possible, **what permits may be required**, and how to move a project forward. The property-owner release started with build feasibility, permits and approvals.

Sources:

- `https://www.landlogic.ai/parcella-updates`
- `https://www.landlogic.ai/latest-updates/introducing-parcella`

Therefore the competitive overlap is no longer limited to zoning or development feasibility. LandLogic has publicly entered the `project/address -> likely permit requirements` decision space.

### 4. One Ontario is turning LandLogic capability into province-level permitting infrastructure

One Ontario appointed LandLogic as its first official technology partner for a province-wide AI-enabled permitting platform.

The publicly described LandLogic layer includes:

- requirement identification;
- automated code/compliance checking;
- agentic submission/tracking;
- direct integrations;
- standardized intelligence across Ontario's fragmented municipal environments.

Sources:

- `https://www.oneontario.ca/latest-updates/landlogic-joins-ai-for-housing`
- `https://www.oneontario.ca/owners-and-developers`
- `https://www.oneontario.ca/ai-for-housing`

One Ontario already lets users describe projects in plain language, discuss project requirements and request permits through the Parcella experience.

## Revised Ontario competitive classification

LandLogic / One Ontario should now be classified as:

> **DIRECT STRATEGIC THREAT — ONTARIO**

not merely a land-intelligence adjacency.

The only ProjectPermit wedge still publicly distinguishable in Ontario is the combination of:

1. **developer self-service**, rather than demo / partner implementation;
2. a **building-permit-specific machine contract**, rather than broad property/land intelligence;
3. an evidence-linked deterministic output such as `REQUIRED / LIKELY_NOT_REQUIRED / CONFIRMATION_REQUIRED` with rule/source versioning;
4. very lightweight per-call economics suitable for automated quote/work-order/agent invocation;
5. no mandatory municipality procurement or configuration;
6. the same third-party integration working across multiple provinces, including places where LandLogic currently has weaker/no coverage;
7. MCP/agent-native invocation as an ordinary developer surface rather than a bespoke conversational-AI partnership.

Every one of those remains **unvalidated customer value**.

## Important boundary: what is not yet publicly proven

The current public review still did **not** find evidence that LandLogic offers a universal, self-serve developer key that returns a standardized building-permit determination such as:

`address + normalized residential scope -> permit required/not required + official evidence`

across Ontario municipalities as an ordinary metered API product.

Its public API/integration workflow remains partner/demo-led, and the API pages emphasize property/zoning/planning intelligence rather than a published permit-determination schema.

This is now the narrowest defensible public-market gap for ProjectPermit in Ontario.

Do not assume this gap is durable. LandLogic can plausibly add it.

## New falsification test

Before adding another Ontario municipality, Ontario project family, or production integration, require a real third-party software buyer to answer all of the following:

1. Have you evaluated or could you use LandLogic / One Ontario / Parcella for this workflow?
2. If yes, why does it not fit?
3. Is the blocker specifically self-serve access, implementation cost/time, permit-specific output contract, cross-province coverage, workflow latency, or per-call economics?
4. Would you actually pay for a lightweight ProjectPermit-style call instead?
5. What bounded monthly current-family event volume would use that call?

If buyers cannot identify a concrete LandLogic/One Ontario gap, Ontario expansion should pause regardless of nominal call volume.

## Additional adoption evidence

LandLogic also publicly shows real third-party/professional integration/adoption signals:

- Teranet / GeoWarehouse integration is cited directly on the API page;
- DEVNEX Solutions is shown as a user/testimonial for LandLogic site-selection intelligence;
- the AI Property Lead Engine is explicitly designed for external builders, developers and proptech/platform partners.

Sources:

- `https://www.landlogic.ai/integration`
- `https://www.landlogic.ai/site-selection`
- `https://www.landlogic.ai/ai-property-lead-engine`

This means ProjectPermit should **not** rely on a story that LandLogic is only a government-facing or homeowner-facing product. It already serves third-party professional and platform contexts.

## Decision consequence

As of 2026-08-28:

> Ontario remains useful for validation because ProjectPermit already has rules and covered-city workflows there, but it should be treated as a **high-competition validation market, not the default expansion market**.

> New Ontario engineering should occur only after both the existing distribution gate and the LandLogic-specific differentiation test are passed.

> Quebec remains strategically interesting mainly because LandLogic's current public terms/coverage do not show the same penetration there, but that whitespace is not demand evidence and must be tested against maintenance cost and software-channel size.
