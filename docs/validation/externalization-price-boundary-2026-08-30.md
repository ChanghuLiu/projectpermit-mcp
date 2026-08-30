# Permit/regulatory externalization price boundary — 2026-08-30

## Purpose

Test whether contractors/homeowners already pay third parties to externalize permit/regulatory work, and separate the value of **information/decision** from **professional deliverables and execution**.

This is category-pricing/externalization evidence only. It is not ProjectPermit willingness-to-pay evidence and must not be used to set API pricing mechanically.

## 1. A critical market pattern: basic permit determination is often free

Several current Canadian permit/design businesses use initial permit/feasibility assessment as a lead-generation service rather than the paid end product.

### Ontario Permit / GTA

Ontario Permit advertises a free initial project assessment and says it will identify what permits are needed, timeline/cost considerations and potential issues before the customer commits.

Its paid work then includes professional drawings, engineering, application preparation/submission, municipal correspondence and inspection support.

Sources:

- https://ontariopermit.com/
- https://ontariopermit.com/faq.html
- https://ontariopermit.com/toronto

### Canadian Blueprint / BC

Canadian Blueprint explicitly advertises **free upfront feasibility**. It says it does not want customers paying for drawings if zoning bylaws or mandatory code upgrades make the proposed build impractical.

Only after feasibility is confirmed does it quote technical drafting/coordination/permitting work.

Source:

- https://canadianblueprint.ca/resources/pricing/

### Interpretation

This is important negative pricing evidence for the narrow ProjectPermit wedge:

> `Do I need a permit / is this project feasible?` can be valuable while still being priced at $0 because it acquires customers for higher-value professional services.

Therefore the existence of expensive permit consultants does **not** imply a high standalone willingness to pay for a permit yes/no API.

It reinforces Contrax's build-vs-buy signal that narrow permit-required logic can be internally built/commoditized.

## 2. What customers do pay for

Public Canadian service pricing shows meaningful spend once the service includes professional or execution value.

### Permit-ready drawings / application package

Ren-Know Ontario publishes a building-permit package at about **$1,750**, including consultation/measurements, design options, scaled permit drawings and designer form. Submission/correspondence can be added.

Source:

- https://ren-know.ca/pricing

### Ontario permit consulting / drawings + professional stamps

Ontario Permit publishes examples such as:

- additions/sunrooms: minimum around **$1,500** plus scope-based architectural/structural pricing;
- commercial permit packages: minimum around **$3,500**;
- commercial repair permit management: roughly **$2,500–$7,500**.

These prices bundle drawings, architect/engineer stamps, application preparation/submission and related professional work.

Source:

- https://ontariopermit.com/pricing.html

### Renovation advisory with permit guidance

Reno-Guide in Montréal prices independent renovation consultation approximately:

- Starter: **$500**;
- Standard: **$800**;
- Premium: **$1,500+**;
- phone consult + written guide: about **$197**.

Permit guidance for the municipality is included alongside cost analysis, scope advice, grants and bid review.

Source:

- https://renogdca.ca/

Again, the customer pays for a broader advisory outcome, not a raw regulatory lookup.

### Permit-expediting / coordination range example

RenoNext's current Ajax permit-cost page publishes an estimated permit-expediting service range around **$1,325–$4,418**.

Source:

- https://renonext.com/costs/building-permit/ajax

This is a commercial vendor estimate, not audited market transaction data, and should be treated only as an order-of-magnitude service-price signal.

## 3. The value stack is layered

The public market suggests at least four distinct economic units.

### Layer A — basic determination / feasibility signal

Examples:

- is a permit likely needed?
- is there an obvious zoning/code blocker?
- which authority should be checked?

Observed pricing behavior:

- often free as lead generation;
- low standalone defensibility;
- easy for a capable platform/vendor to internalize narrowly.

ProjectPermit implication:

- keep current low-friction/free preview;
- do not treat this as the terminal value unit.

### Layer B — maintained project-specific obligation intelligence

Examples:

- current permit/approval/document/professional/inspection obligations;
- jurisdiction/version/effective-date tracking;
- missing/uncertain facts;
- official evidence;
- quote/scope/schedule consequence;
- repeat-check change identity.

Observed pricing behavior:

- direct Canadian consumer pricing is not established from this research;
- analogous maintained-code infrastructure (ICC Code Connect/Kestrel) uses licence/implementation structures.

ProjectPermit implication:

- this remains the core Layer-C commercial hypothesis;
- price should be tied to workflow value/maintenance externalization, not copied from permit-expediting prices.

### Layer C — professional artifacts

Examples:

- drawings;
- architect/engineer/BCIN stamp;
- calculations;
- permit-ready documentation.

Observed pricing behavior:

- hundreds to several thousands of dollars depending on scope.

ProjectPermit implication:

- do not pretend the API provides this professional value;
- it may route to/identify that professional involvement is required.

### Layer D — execution / expediting / representation

Examples:

- prepare/submit application;
- correspond with municipality;
- correction cycles;
- track approval;
- coordinate inspections/close-out.

Observed pricing behavior:

- can be thousands of dollars per project.

ProjectPermit implication:

- this is a downstream service opportunity/partner layer, not current product scope unless separately validated.

## 4. Commercial consequence for ProjectPermit

The strongest conclusion is **not** `permit services cost thousands, so ProjectPermit can charge a lot`.

The stronger conclusion is:

> **The narrow information layer is frequently used to sell higher-value work. ProjectPermit must either become the maintained intelligence infrastructure embedded in a repeated workflow, or participate in/enable a downstream high-value artifact or action.**

That makes the current commercial paths more coherent:

1. contractor add-on subscription for maintained pre-quote intelligence;
2. platform licence/minimum for cross-jurisdiction maintained obligations;
3. x402 low-friction per-call for developers/agents/long-tail use;
4. future partner/referral/integration layer for drawings, professional review or permit execution if independently validated.

## 5. Better willingness-to-pay question

Do not ask a contractor:

> Would you pay for a permit checker?

That compares ProjectPermit against a category that is often free.

Ask instead:

> **When a permit/code/professional/document requirement could change a quote, what do you do today to get the answer before signing — staff research, city calls, designer/engineer, permit consultant, or a contingency allowance? Roughly what does that step cost in staff time or outside fees, and would you rather pay a fixed monthly amount for a maintained in-workflow answer with official evidence?**

This identifies the **replacement budget**, which is much more useful than asking an abstract API price.

## 6. Evidence impact

No E-level increase.

What this establishes:

- permit/regulatory work is already externalized and monetized in Canada;
- professional/processing layers support meaningful service fees;
- narrow permit determination itself is often free;
- therefore high permit-service prices must not be used as a proxy for API willingness to pay;
- the best Layer-C WTP test is replacement of repeated staff/consultant research inside quote workflow.

Current E4 = 0; E5 = 0.
