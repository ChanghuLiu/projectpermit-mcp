# SubmitX Quebec Build-vs-Buy Boundary — 2026-08-28

## Why SubmitX matters to the Quebec rescue thesis

SubmitX is not currently public evidence of a municipal `permit required?` engine. It is valuable for a different reason: it shows how cheaply a Quebec-native contractor platform can already combine project scope, address, AI quoting, plan/document analysis and regulatory-compliance reasoning inside one vertical SaaS.

That makes SubmitX a high-value **build-vs-buy comparator** for the Quebec-only ProjectPermit rescue hypothesis.

## Current public product boundary

SubmitX currently markets itself as an all-in-one ERP for Quebec construction contractors, including general contractors, plumbers, electricians and residential renovators.

Public features include:

- AI-generated construction quotes;
- plan/document analysis;
- project and CRM workflow;
- SEAO monitoring;
- Quebec-specific CCQ, RBQ and CNESST compliance;
- mobile/web delivery;
- Quebec-focused pricing and operations.

Sources:

- `https://www.submitx.ca/`
- `https://app.submitx.ca/legal/terms`
- `https://app.submitx.ca/legal/privacy`

Its July 2026 Terms explicitly describe `évaluation de la conformité réglementaire (RBQ, CCQ, CNESST)` as part of the service.

Its privacy policy is more technically revealing: project description, jobsite address, work lines and company conditions can be sent to the Anthropic Claude API to generate estimates/analyses, with human validation before consequential use.

That means SubmitX already owns most of the workflow inputs ProjectPermit would need for pre-quote permit applicability:

`project description + address + work lines`

inside the same system that generates the quote.

## What public evidence does NOT show

The focused review did **not** find a current public SubmitX claim that it:

- determines whether a municipal building permit is required;
- identifies municipal permit types from scope/address;
- maintains municipal zoning/bylaw rules across Quebec;
- returns municipal official-source citations for permit applicability;
- exposes an external developer API for this regulatory layer.

Therefore SubmitX must not be counted as an exact ProjectPermit competitor today.

Its published compliance language currently names provincial/industry regimes such as RBQ, CCQ and CNESST rather than municipal permit applicability.

## Scale evidence is contradictory and must stay downgraded

SubmitX's own current marketing site claims:

- `300+ entrepreneurs québécois`;
- customer testimonials/logos;
- broad Quebec regional availability;
- strong review ratings.

Source:

- `https://www.submitx.ca/`

Independent public adoption signals found in the same review are much smaller:

- Google Play currently shows **1+ downloads** for the Android app;
- Apple's App Store currently shows **2 ratings**;
- the Android app was updated August 5, 2026, indicating the public mobile product is very recent.

Sources:

- `https://play.google.com/store/apps/details?id=ca.submitx.app`
- `https://apps.apple.com/ca/app/submitx/id6776807543`

These numbers do not prove the web SaaS lacks customers—most customers may never use the mobile app—but they are incompatible with treating the vendor's `300+` claim as independently verified adoption evidence.

Therefore:

> **Do not use SubmitX's claimed customer count as E2/E4 evidence, market denominator or proof of scale.**

SubmitX is useful here because of architecture and buyer behavior, not because its customer count is verified.

## The build-vs-buy falsification question

The highest-value question is:

> If SubmitX users repeatedly need municipality-specific `permit required?` answers while its AI is already generating a quote from project description + jobsite address + work lines, would SubmitX build and maintain that municipal rule/RAG layer internally, or buy a deterministic cross-municipality API that maintains official sources, version history and conservative unknown-state handling — and why?

This is more decision-useful than asking whether SubmitX generally thinks permit compliance is useful.

### Negative evidence for the Quebec rescue

A credible answer favoring internal build is strong negative evidence if the reason is that:

- municipal permit logic can be added cheaply to the existing Claude workflow;
- customers do not need deterministic rule IDs/version history;
- municipal source maintenance is manageable inside the vertical product;
- permit applicability is too rare to justify another vendor;
- latency/cost/dependency from an external API is worse than internal reasoning.

That would directly weaken the surviving Quebec-only thesis.

### Positive rescue evidence

A credible external-buy preference is materially positive if SubmitX says:

- municipality-by-municipality source drift is expensive or distracting;
- deterministic/auditable evidence matters for customer trust or liability;
- cross-city coverage is difficult enough to centralize externally;
- it would prefer a maintained API over internal prompt/RAG logic;
- it would allocate integration resources or test a real workflow.

An abstract `interesting idea` is not enough.

## Contact boundary

No prior ProjectPermit conversation with SubmitX was found in Gmail as of 2026-08-28.

SubmitX's Google Play listing exposes `autosubmitx@gmail.com` as the official app-support/developer email and a Quebec phone number. Its legal/privacy address `legal@submitx.ca` is explicitly for privacy/legal matters and should **not** be used for product-validation outreach.

Sources:

- Google Play listing for `ca.submitx.app`;
- SubmitX privacy policy.

If outreach is sent, use the public product-support route and keep the question narrow; do not request customer data or proprietary implementation details.

## Score implication

**No score change. ProjectPermit remains 50/100, PAUSE / RE-SCOPE.**

SubmitX adds architecture-level pressure to the Quebec rescue thesis, but it does not yet provide exact municipal permit-applicability competition or a verified large buyer denominator.

The result changes **which external answer matters next**, not the score:

- internal-build preference from a credible Quebec vertical SaaS would push the rescue toward No-Go;
- external-maintenance preference plus a real repeated workflow would support rescue.

## Bottom line

SubmitX shows that a Quebec contractor SaaS can already possess the exact upstream data and AI workflow needed to internalize permit reasoning cheaply.

That makes the Quebec rescue question narrower:

> **Is municipal rule maintenance/auditability difficult enough that Quebec vertical software prefers buying a shared deterministic API, or will products like SubmitX simply absorb this function into their existing quote/compliance stack?**

Only an external build-vs-buy answer should decide that.