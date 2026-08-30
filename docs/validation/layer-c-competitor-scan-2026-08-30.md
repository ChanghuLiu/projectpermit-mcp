# Layer C competitor / product-form scan — 2026-08-30

## Question

Is there already a mature, directly substitutable API for project-specific regulatory obligations before estimate / preconstruction decisions, or is the market still split among adjacent layers?

This note is market research only. It is not E2/E3 buyer evidence and does not authorize implementation.

## Current product layers observed

### 1. Code-content delivery

**ICC Code Connect API**

- Delivers current ICC code content into third-party workflow applications.
- Supports search/import of code sections, tables and figures.
- Commercial use requires both an implementation agreement and content licensing agreement.
- Strong proof that current building-code content can be sold as API infrastructure.
- Weak fit to Layer C because it delivers code content/references, not a project-specific obligation bundle derived from project facts.

### 2. Automated compliance + permit execution

**Symbium**

- Performs real-time compliance checks against building, zoning and energy codes as a project is scoped.
- Supports jurisdiction-specific project eligibility, requirements and workflow steps.
- Can generate approval documents and, for some jurisdictions/workflows, create or issue permits through permitting-system integrations.
- This is deeper than ProjectPermit's intended Layer C boundary and approaches compliance / execution.
- Strong adjacent competitor, but not evidence of a neutral standalone obligations API sold for embedding in third-party estimate workflows.

**PermitFlow / similar permit-management platforms**

- Focus on research, application preparation/submission, municipality communication, permit status and embedded permit-management workflows.
- PermitFlow publicly offers API partnerships for embedded workflows.
- These products validate willingness to integrate permitting workflows but are operationally downstream of the proposed pre-estimate obligation bundle.

### 3. Permit / construction activity data APIs

Examples include Gryd, Physical Layer, PermitStack, SignedOff and similar products.

- Normalize historical/current permit records, contractor/license/property/project data or permit status.
- Strong proof that construction data infrastructure is sold by API.
- Mostly answer `what has been filed / issued / recorded?`, not `given this proposed scope, what obligations attach before pricing?`.

### 4. Closest product-form analogue: PermitBird

PermitBird is materially closer to the Layer C concept than the categories above.

Current public surface:

- U.S. stormwater + Section 404 permit determination.
- Inputs site/project facts.
- Returns whether coverage is triggered, the governing permit/version/authority, eligibility screens and site-specific requirements.
- Requirements include inspection frequency, stabilisation deadlines, filing windows, recordkeeping duties, buffers and citations.
- Each requirement carries a permit section and a `because` explanation.
- Deterministic rules engine; no model in the request path.
- Explicit unknown/unverified handling rather than substituting guessed requirements.
- REST API + hosted MCP server.
- Idempotency-key support.
- Public sandbox/test path.
- Paid plans currently advertise $49/month for 1,000 API calls and $149/month for 10,000 calls, with paid value also tied to required plan/document/record retention.

Product maturity signals:

- PermitBird's public Terms/Privacy/Security pages were updated 2026-08-06 and its developer/MCP surface is very recent.
- Its own security page explicitly describes it as a `small product early in its life` and states it has no SOC 2, ISO 27001 or completed penetration test.
- Publicly described stack is Vercel + Supabase.
- Current searches found no strong independent customer, usage-volume or enterprise-adoption evidence. This absence is not proof of zero usage.

Interpretation:

- PermitBird is **proof-of-form**, not yet proof-of-market.
- It independently validates the architecture: deterministic cited regulatory facts -> project-specific requirement bundle -> REST/MCP -> paid operational record/document layer.
- It also demonstrates that a solo/small product can build this form without a large enterprise compliance organization.
- It does **not** currently eliminate the ProjectPermit opportunity because its domain is narrow U.S. environmental permitting (stormwater / wetlands), not Canadian municipal building / renovation pre-estimate obligations.
- Its effective API price at advertised allowance is far below ProjectPermit's current $0.20/call ($49/1,000 ~= $0.049; $149/10,000 ~= $0.0149), so ProjectPermit cannot assume commodity determination calls alone sustain premium per-call pricing. Higher value must come from breadth, freshness/provenance, workflow consequence, distribution or a downstream compliance artifact.

## Competitive gap that still appears open

The narrow gap worth validating remains:

> **Project-specific, current, evidence-linked regulatory obligation data for pre-estimate / preconstruction workflows — before permit filing and below drawing/code-compliance certification.**

In practical terms:

- Input: jurisdiction + proposed project scope + known property/project facts.
- Output: applicable permits/approvals + preconditions + documents/professional involvement + inspections/sequence/deadlines + source/version/freshness + explicit unknowns.
- Consumer: estimating / preconstruction / field-service / contractor software or an agent already mid-workflow.
- Not: raw code search.
- Not: historical permit-record data.
- Not: permit filing/status management.
- Not: drawing/BIM code-compliance certification.

## Decision impact

1. **Do not kill Layer C because of competition.** The closest analogue is recent and narrow; mature products still cluster in adjacent layers.
2. **Do not treat PermitBird as E2/E4.** No independently verified recurring buyer volume was found.
3. **Raise the bar for differentiation.** `deterministic + cited + MCP` is no longer enough by itself; those are becoming table stakes.
4. **Keep the current buyer test unchanged.** The key unresolved question is whether estimating/preconstruction software has a repeated monthly workflow where the obligation bundle changes scope, price, schedule or handoff.
5. **Do not expand code/data licensing yet.** Buyer denominator and workflow consequence must cross the validation gate first.

## Evidence classification

- Market/product-form evidence: yes.
- Direct buyer evidence: no.
- E1/E2/E3/E4/E5 impact: none by itself.
- Current action: continue bounded buyer falsification; no implementation expansion.
