# Platform channel ranking addendum — 2026-08-30

## Why this addendum exists

Earlier 2026-08-30 platform notes classified Buildxact mainly as a vendor/partnership target because a general third-party developer route had not yet been confirmed.

That assumption is now superseded by current official Buildxact documentation.

Buildxact has a public developer portal, REST APIs for Estimates/Jobs/Leads/Clients, staging, webhooks and an explicitly documented third-party OAuth flow for SaaS applications. Third-party app registration still requires Buildxact support approval.

Detailed evidence:

- `docs/validation/buildxact-api-channel-2026-08-30.md`

## Revised ranking for current ProjectPermit families

### Tier 1A — Jobber private/draft pilot

Why first:

- explicit General Contractor and Remodeling product segments;
- ProjectPermit's current eight project families overlap strongly with renovation/remodel work;
- large contractor/home-service ecosystem;
- public OAuth/GraphQL Developer Center;
- small private/custom integration can remain Draft within Jobber's five-paying-account boundary;
- existing ProjectPermit Jobber adapter reduces implementation work.

Main risk:

- broad Jobber base contains many low-regulatory service categories, so eligible-account share remains unknown.

### Tier 1A/B — Buildxact third-party integration

Why promoted:

- strongest direct builder/remodeler/preconstruction workflow fit found in this platform pass;
- Estimate/Estimate Item data is part of the public API surface;
- official third-party SaaS OAuth flow;
- staging and webhooks;
- regulatory result can plausibly act before quote lock, where cost/scope/schedule impact is economically meaningful.

Main friction:

- third-party application registration requires Buildxact support approval;
- current public customer/account denominator is not as clean as Jobber's;
- exact adapter field mapping still needs endpoint-level verification only after E2.

### Tier 1B — ServiceM8 private add-on pilot

Why retained:

- lowest embedded-UX engineering friction;
- Job Action -> read current job -> external calculation/API -> modal result is an official example pattern;
- pre-approval private install URL;
- later built-in recurring billing with 90/10 developer/platform split;
- existing ProjectPermit ServiceM8 adapter.

Why below Jobber/Buildxact for current scope:

- public Canadian customer count is not disclosed;
- many ServiceM8 jobs are repair/maintenance/service workflows outside ProjectPermit's current renovation/construction family set;
- strong distribution mechanics do not compensate for weaker current-family fit.

### Tier 2A — Buildertrend vendor/integration route

- strong builder/remodeler relevance;
- large builder denominator;
- marketplace/integration precedent;
- public self-serve developer path still not confirmed from official sources in this pass.

### Tier 2B — ServiceTitan

- enormous trade workflow/GTV scale;
- formal integration/marketplace path;
- but substantial service/repair mix and stronger internal-build economics.

## What this ranking does not mean

It does **not** mean ProjectPermit should now build three integrations.

The correct sequence remains:

> buyer denominator + material consequence -> pick one representative private platform pilot -> repeated E4 -> E5 -> only then public marketplace / second platform.

## Current first-pilot default

If Layer-C buyer evidence crosses E2 without pointing to a specific platform, default pilot order should now be:

1. **Jobber** — fastest combination of Canada relevance, current-family fit and low-account private integration;
2. **Buildxact** — highest preconstruction fit, conditional on easy third-party app registration;
3. **ServiceM8** — lowest technical friction / clean recurring billing experiment, but weaker known Canadian/current-family denominator.

If a real buyer comes from one of these platforms first, buyer reality overrides this paper ranking.

No E-level change.
