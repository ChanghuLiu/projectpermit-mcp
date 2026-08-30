# Low-cash private platform pilot gate — 2026-08-30

## Purpose

Define the smallest credible path from Layer-C buyer evidence to real external usage/payment without prematurely building a public marketplace product.

This is a **readiness/falsification plan only**. Current buyer evidence has not crossed E2, so implementation remains frozen.

## Core principle

Do not make Marketplace approval the prerequisite for E4.

Both ServiceM8 and Jobber expose private/pre-public integration paths that can support a small number of design-partner accounts.

The correct sequence is:

`E2 buyer denominator/consequence -> private 3–5 account pilot -> E4 repeated real work -> E5 payment -> only then public marketplace investment`

## 1. ServiceM8 private pilot path

Official developer documentation currently supports several useful low-friction facts:

- a Public Application/Add-on can be created without being publicly listed;
- before Store approval, a developer can test/share using a `Private Add-on Install URL`;
- Add-on SDK actions can add a button directly to a Job Card;
- an action event supplies `jobUUID` plus authentication context;
- ServiceM8 can issue a short-lived OAuth token for serverless action execution;
- serverless add-ons can be written in Python, Node.js or Java;
- a web-service hosted add-on can instead call existing HTTPS infrastructure in any language;
- ServiceM8's own Pool Calculator example follows the pattern `Job Action -> calculate/fetch -> show result -> optionally post Job Diary note`.

Official sources:

- https://developer.servicem8.com/docs/servicem8-add-on-store
- https://developer.servicem8.com/docs/getting-started-1
- https://developer.servicem8.com/docs/add-on-types
- https://developer.servicem8.com/docs/sample-event-data
- https://developer.servicem8.com/docs/examples

### Smallest ProjectPermit pilot shape

One Job Card action:

`Check requirements`

On click:

1. receive the current `jobUUID`;
2. retrieve only the current Job + scope-relevant JobMaterial fields;
3. use existing ProjectPermit ServiceM8 extraction logic;
4. ask the user to confirm/select a bounded ProjectPermit `project.family` + `action` rather than guessing from natural language in V0;
5. call the existing ProjectPermit API;
6. render a concise modal with determination, missing/uncertain facts, official evidence/freshness and recommended action;
7. **do not mutate the Job automatically**;
8. optionally expose an explicit user-controlled `Add note to Job` action only after the result is shown.

This is materially smaller than building an always-on regulatory automation engine.

## 2. Why manual bounded classification is acceptable for E4

Current `servicem8_adapter.py` already extracts:

- Job uuid;
- status;
- address;
- job description;
- scope-relevant JobMaterial text;
- source-object identity/idempotency context.

The current adapter intentionally leaves natural-language scope normalization to the caller/agent.

For a pilot, adding an LLM classifier would introduce an unnecessary failure mode. A bounded UI selection can answer the only missing structural input while preserving determinism.

Pilot goal is not zero-click automation. It is to prove:

> does a real contractor repeatedly want the current regulatory answer inside a live job/quote record, and does that answer change a material work decision?

If yes, classification automation can be tested later.

## 3. ServiceM8 Store investment is intentionally deferred

Public Store approval adds real work:

- feature-complete reviewed product;
- at least three real screenshots;
- complete help/onboarding documentation;
- monitored support email;
- timely ongoing support;
- OAuth/public activation UX;
- safety/relevance/redundancy review;
- partner preview before public release.

Official source:

- https://developer.servicem8.com/docs/addon-store-requirements

ServiceM8 also specifically warns that add-ons should not expose customers to legal/regulatory risk.

Therefore public launch should happen only after private pilot evidence shows enough value to justify this maintenance/support burden.

## 4. Jobber private pilot path

Jobber supports:

- a Developer Center + dedicated integration-testing account;
- OAuth 2.0/GraphQL apps;
- Custom Integrations for specific customer accounts;
- Draft apps without Marketplace review when they stay within the allowed small-account boundary;
- API access is blocked if a Draft integration connects to more than **5 paying Jobber accounts** without approval.

Official sources:

- https://developer.getjobber.com/docs/getting_started/
- https://developer.getjobber.com/docs/custom_integrations/

This creates a natural falsification cohort:

> **up to five real Jobber businesses before marketplace scale.**

The existing ProjectPermit Jobber adapter already reduces the product-side integration work similarly to ServiceM8.

## 5. Channel ranking for the pilot phase

### ServiceM8 — easiest embedded UX experiment

Advantages:

- direct Job Action pattern is documented;
- temporary OAuth/serverless path can avoid account/token infrastructure;
- pre-approval private install sharing exists;
- existing ProjectPermit adapter;
- later recurring billing can be handled by ServiceM8 with 90/10 revenue share.

Risks:

- public Canada customer count is not disclosed;
- third-party add-ons are plan-dependent;
- Store requires ongoing support and conservative regulatory-risk positioning.

### Jobber — stronger Canada/scale signal, slightly more review/account friction

Advantages:

- very large contractor/home-service ecosystem;
- strong Canada relevance;
- Requests/Quotes/Jobs are core workflow objects;
- existing ProjectPermit Jobber adapter;
- five-account Draft boundary creates a clean pre-marketplace experiment.

Risks:

- marketplace review required for scale;
- broad customer base includes low-regulatory service categories;
- larger platform has stronger eventual internal-build economics.

## 6. Pilot cohort size

Do not seek 100 users before learning anything.

A valid first cohort is **3–5 businesses** with actual permit/regulatory-sensitive work.

Why 3–5:

- enough to distinguish one idiosyncratic buyer from a repeatable workflow;
- fits Jobber's small Draft boundary;
- small enough for a solo developer to support manually during validation;
- allows detailed per-job observation instead of vanity signup counts.

## 7. E4 gate for private pilot

Do not count installation as E4.

Count a business toward E4 only if it uses the integration on a **real customer/work record**, not a synthetic demo.

Minimum event record:

- external business/account id hashed or internally pseudonymous;
- source platform;
- real work-object type;
- project family;
- jurisdiction;
- result classification;
- whether missing facts were requested;
- whether result changed quote/scope/schedule/professional/document/inspection handling;
- whether user explicitly saved/attached result;
- repeated use count in a bounded period.

Do not store unnecessary client PII for validation telemetry.

## 8. Strong E4 target

A stronger E4 threshold than `one click` is:

- at least **3 independent businesses**;
- at least **10 real work records total**;
- at least **2 businesses repeat use** on separate jobs;
- at least **3 work records** where the user identifies a material workflow consequence.

These are internal validation thresholds, not market claims.

If nobody repeats the action after the first novelty click, stop before public Store work.

## 9. E5 path

Do not require x402 from the contractor.

Possible first economic commitment after E4:

1. direct small monthly pilot fee;
2. ServiceM8 recurring add-on billing once public/eligible;
3. fixed pilot/platform fee;
4. x402 payment only for developers/agents that naturally use that rail.

An E5 signal should be an actual payment or economically binding commitment, not `I'd probably pay`.

No price is selected by this note.

## 10. Cash/development boundary

Before E2:

- do not create ServiceM8/Jobber marketplace listings;
- do not implement OAuth/store billing;
- do not build automatic webhooks;
- do not build LLM scope classification;
- do not buy content licences.

After E2 but before E4:

- implement only the private Job Action / limited account integration needed for representative real work;
- reuse the existing ProjectPermit API and adapters;
- maintain explicit user action before any writeback;
- use only legally safe/currently cleared data scope.

After repeated E4 + E5:

- then evaluate Store review, recurring billing, support docs, polished onboarding and automation.

## Current decision

This research materially lowers the **distribution experiment cost**, but it does not justify starting that experiment yet.

The current bottleneck remains buyer evidence, not engineering.

No E-level change.
