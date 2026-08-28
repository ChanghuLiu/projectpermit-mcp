# BC Building Permit Hub Boundary — 2026-08-28

## Why this matters

British Columbia's official Building Permit Hub is not an exact ProjectPermit substitute, but it materially reduces the long-term value of a private cross-jurisdiction information layer inside B.C.

The Province now provides a standardized digital permit-submission environment across participating local governments and First Nations and continues to add automated compliance tooling.

Official sources:

- `https://www2.gov.bc.ca/gov/content/housing-tenancy/building-or-renovating/permits/building-permit-hub`
- `https://www2.gov.bc.ca/gov/content/industry/construction-industry/building-codes-standards/innovation`
- 2024 launch release describing address-updated requirement checklists

## What the Hub currently does

Current official pages show that a submitter can:

- work across multiple participating jurisdictions in one system;
- view jurisdiction-specific requirements including BC Building Code, building bylaws, zoning and other regulations;
- enter project/location information and obtain the jurisdiction's required documentation/checklist;
- store application information and documents;
- submit permit applications digitally;
- track application status;
- use automated BC Energy and Zero Carbon Step Code tools;
- pre-check certain design-compliance requirements.

The Province's original launch roadmap stated that the Hub would provide a checklist of what is required for a building permit that **automatically updates when a builder inputs the project address**.

This is an important architecture signal: government itself is normalizing address/jurisdiction-specific permitting requirements rather than leaving all cross-municipality requirement knowledge to private vendors.

## Exact boundary versus ProjectPermit

ProjectPermit currently asks an earlier question:

`unfiled project scope + municipality/address + decisive facts`

→ `is a building permit required / likely not required / confirm?`

The Building Permit Hub generally assumes the user has entered a building-permit application flow. The current public user guidance still tells applicants to understand local permitting/zoning requirements and, in some cases, contact the local jurisdiction before applying.

Therefore the Hub does **not** currently prove a universal B.C. `permit required / not required` applicability engine.

Instead, its strongest overlap is:

- location-specific requirement normalization;
- application/document checklist generation;
- address-based local rule selection;
- cross-jurisdiction standardization;
- automated compliance checks.

## Vancouver-specific boundary

The original 2024 pilot list included Burnaby, North Vancouver, Surrey, Victoria and other communities, but not the City of Vancouver itself.

Current provincial pages say the Hub is expanding and is intended to support participating communities across B.C.; they do not establish from the reviewed public material that City of Vancouver has moved its main permit workflow into the Hub.

Therefore ProjectPermit's current Vancouver support is not directly made redundant by the Hub today.

However, Vancouver should not be treated as a durable province-level expansion moat because the Province is actively standardizing the surrounding ecosystem and funding local-government digital-approval alignment.

## 2026 direction of travel

As of May 2026 the Province publicly describes:

- Building Permit Hub expansion;
- compliance pre-check tools;
- address/jurisdiction lookup for Step Code requirements;
- guides for converting local bylaws/policies/Official Community Plans into machine-readable formats such as JSON and XML.

In July 2026 B.C. also announced new funding for 56 local governments to accelerate development approvals, including digitization projects aligned with the Hub.

This reduces the defensibility of any strategy based on manually owning B.C. municipal rule normalization forever.

## Score implication

**No immediate score change; canonical score remains 51/100.**

Reasons:

- the Hub is an official application/submission/compliance platform, not a proven general pre-quote applicability engine;
- Vancouver itself was not in the original pilot list and current reviewed evidence does not prove City of Vancouver participation at the same depth;
- ProjectPermit's competitive headroom and defensibility are already very low, so this regional infrastructure trend should not be double-counted as another generic architecture penalty.

## Expansion implication

This evidence is still strategically important:

> **Do not expand ProjectPermit further into B.C. merely to accumulate municipality count.**

Any additional B.C. jurisdiction should require buyer evidence that the upstream `permit required?` decision remains unresolved despite the official Hub and municipal guidance.

B.C. should be treated as a region where government standardization is likely to make private requirement-normalization progressively less scarce.

## Future kill / re-scope trigger

Reassess immediately if the Building Permit Hub adds a generalized pre-application tool that takes project scope/address and returns all required permit types or a clear `no building permit required` result across participating jurisdictions.

That would be an official, free competitor to the core applicability layer inside B.C.

## Bottom line

The B.C. Building Permit Hub is not yet ProjectPermit's exact product.

But it demonstrates that **cross-jurisdiction permit requirements, address-specific rule selection and compliance checks are becoming public infrastructure in B.C.**

That makes more B.C. engineering a poor default use of ProjectPermit resources unless external demand proves an upstream gap the Hub does not solve.