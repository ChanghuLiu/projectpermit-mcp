# ServiceM8 / Jobber marketplace gap — 2026-08-30

## Purpose

Test whether developer-accessible contractor platforms already contain a dynamic, jurisdiction-maintained permit/regulatory decision product comparable to the ProjectPermit Layer-C thesis.

This is a targeted public-marketplace scan. **Failure to surface a product is not proof that none exists.** Marketplace visibility can depend on account, country, plan or indexing.

## 1. ServiceM8 marketplace structure

ServiceM8 currently documents:

- at least 50 add-ons;
- 250+ purchasable Forms;
- third-party public add-ons distributed to ServiceM8 businesses;
- OAuth/API support and UI extensions through Job Actions, Client Actions and menu items;
- optional ServiceM8-managed recurring billing with 90% developer / 10% ServiceM8 revenue share.

Official sources:

- https://support.servicem8.com/help-center/servicem8-add-ons/servicem8-add-ons/servicem8-add-ons-overview
- https://developer.servicem8.com/docs/servicem8-add-on-store
- https://developer.servicem8.com/docs/add-on-capabilities

## 2. Existing compliance products are mostly static workflow artifacts

The public Form Store has a substantial Compliance category and related Safety / Inspection / Commissioning categories.

Examples observed in the current scan:

- Risk Management Checklist — $48.99 one-time; includes a `Permits Required` section plus site/equipment/safety questions;
- Gas Safety Certificate (CP12) — $124 one-time;
- Hazard / Incident / Accident — $99;
- Domestic Smoke Alarm / RCD Compliance Certificate — $114;
- Ground Source Heat Pump Commissioning Certificate — $149;
- many gas, refrigerant, plumbing and commissioning certificates around $99–$149;
- Site Safety Inspection — $24.99.

Official/public marketplace sources:

- https://www.servicem8.com/ca/form-store?category=Compliance
- https://www.servicem8.com/form-store-install?uuid=6fb22607-bb40-4b62-b29c-1c65beef019b
- https://www.servicem8.com/form-store-install?uuid=063335f7-e9b7-469e-b44c-1626946e569b

These products show that ServiceM8 users already pay for compliance-oriented workflow artifacts.

However, the products surfaced in this scan are primarily:

- fixed checklists;
- certificates;
- inspection/report templates;
- commissioning records;
- forms completed by the user/technician.

They do not demonstrate an authoritative service that dynamically determines current permit/code obligations from project + jurisdiction facts.

## 3. Targeted negative competition search

Multiple public searches were run around:

- `building permit`;
- `permit requirements`;
- `building code`;
- `regulation`;
- `jurisdiction compliance`;
- `dynamic compliance`;
- `permit add-on`;

across ServiceM8 Add-ons/Form Store and Jobber Marketplace/help/integration surfaces.

### Result

No public product surfaced that clearly provides all of the following:

`job/project facts -> jurisdiction-specific current permit/regulatory determination -> maintained authority/version -> evidence -> operational action`

This must be phrased only as:

> **No dynamic maintained permit/regulatory decision add-on surfaced in targeted public searches as of 2026-08-30.**

Do not claim market absence.

## 4. Jobber marketplace boundary

Jobber has a mature App Marketplace, OAuth 2.0/GraphQL Developer Center and app-review process.

Current public Marketplace/help content prominently surfaces integrations for:

- leads/marketing;
- finance/payments;
- document signing;
- fleet/location;
- measurement/photo/site documentation;
- automation;
- accounting/payroll.

Jobber also has native custom Checklists for safety, inspections, authorizations and field data collection.

Official sources:

- https://help.getjobber.com/en/articles/app-marketplace/
- https://help.getjobber.com/en/topics/app-marketplace/
- https://developer.getjobber.com/docs/getting_started/
- https://developer.getjobber.com/docs/publishing_your_app/app_review_process/
- https://help.getjobber.com/en/articles/checklists/

No dynamic jurisdiction-maintained permit/building-code decision integration surfaced in targeted public searches.

Again, this is not proof of absence; Jobber notes that some apps may be visible only to eligible accounts.

## 5. Willingness-to-pay interpretation

The ServiceM8 Form Store gives a useful **category spending precedent**, not ProjectPermit price validation.

Observed compliance/safety artifacts often sell for roughly `$49–$149` one-time.

This supports:

- compliance workflow artifacts are not expected to be universally free;
- contractors will pay to save field paperwork/time or standardize compliance records;
- a marketplace user can understand a compliance-related software purchase without understanding API/x402 economics.

It does **not** prove:

- willingness to pay a monthly ProjectPermit subscription;
- willingness to pay for permit/regulatory research specifically;
- a viable price point;
- repeated use;
- Layer-C consequence.

No pricing change follows from this evidence.

## 6. Important ServiceM8 approval risk

ServiceM8's current Add-on Store Requirements explicitly say an add-on should be safe to use and should not expose customers to legal or regulatory risk. They also require ongoing support/maintenance and reject redundant/problem-searching apps.

Official source:

- https://developer.servicem8.com/docs/addon-store-requirements

This creates a real product-positioning gate for ProjectPermit.

A future marketplace version should **not** claim:

- guaranteed compliance;
- municipal authorization;
- legal advice;
- definitive technical-code certification where facts/evidence are incomplete.

A safer fit is the current ProjectPermit architecture:

- deterministic preflight;
- `REQUIRED / LIKELY / ADDITIONAL_REVIEW / CONFIRMATION_REQUIRED / OUT_OF_SCOPE`-style bounded states;
- explicit missing/uncertain facts;
- official-source evidence + version/freshness;
- human confirmation when needed;
- proposed actions behind a safe-writeback gate.

This is strategically important: the conservative architecture is not only liability hygiene; it may also improve marketplace approvability.

## 7. Competitive interpretation

### Positive signal

The marketplace has:

- contractor/trade users;
- mature compliance-document spending;
- job-scoped form/action workflows;
- third-party distribution;
- recurring billing infrastructure.

### Gap signal

The public products surfaced are mostly **recording/completion artifacts after the user already knows what must be done**.

ProjectPermit's Layer-C thesis is different:

> determine what current requirements apply **before quote/design/work**, explain why, and turn that determination into bounded job/quote actions.

That is a more upstream decision layer.

### Competitive caution

This gap is easy to overstate.

QwikScope and other permit-tech competitors already show that permit/documents/fees/timeline outputs are commercially recognized outside these marketplaces. Therefore differentiation cannot simply be `we tell you which documents/permits are needed`.

The stronger differentiated bundle remains:

`Canada-specific maintained authority -> current obligation decision -> official evidence/version/freshness -> material quote/job consequence -> idempotent work-record action`

## 8. Distribution decision

ServiceM8 currently ranks as the strongest **post-E2 end-user distribution experiment** because:

- public developer onboarding exists;
- public store exists;
- billing exists;
- Job Action/UI extension is possible;
- existing ProjectPermit ServiceM8 adapter already handles job facts/action proposals;
- public search did not surface a directly equivalent maintained jurisdiction decision add-on.

Jobber remains the higher-scale second route, but marketplace publication has review friction and draft apps are limited to at most five paying accounts without approval.

## 9. Do not build yet

This scan does not cross E2.

Before building a ServiceM8/Jobber marketplace product, require buyer evidence that:

1. a real contractor workflow repeatedly needs the regulatory lookup;
2. the answer materially changes quote/scope/schedule/professional/document/inspection handling;
3. users prefer paying for a maintained decision layer instead of keeping a checklist/manual research process;
4. a bounded monthly denominator supports a recurring product.

If those conditions cross the gate, ServiceM8 is currently the cleanest place to test direct contractor subscription economics without needing an enterprise platform licence first.

## Evidence impact

No E-level increase.

Current interpretation:

- marketplace/distribution feasibility: **stronger**;
- obvious same-form competitor inside ServiceM8/Jobber: **not surfaced in targeted public scan**;
- category willingness-to-pay precedent: **present for static compliance artifacts**;
- Layer-C buyer demand: **still unproven**;
- E4 = 0;
- E5 = 0.
