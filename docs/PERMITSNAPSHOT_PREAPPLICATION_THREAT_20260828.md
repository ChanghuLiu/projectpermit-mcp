# PermitSnapshot Pre-Application Threat — 2026-08-28

## Why this matters

PermitSnapshot is the closest Canadian public product found so far to ProjectPermit's intended **pre-application / pre-quote decision layer**.

It is materially different from issued-permit history APIs such as permit-record/property-intelligence products.

PermitSnapshot publicly states that it:

- accepts **property address + proposed project scope**;
- generates a property-specific permit feasibility report in under five minutes;
- is explicitly positioned for **builders and GCs before quoting**;
- covers all **414 Ontario municipalities**;
- returns **permit requirements with likelihood ratings**;
- includes zoning, setbacks, conservation-authority screening, fees, timelines and municipal contacts;
- uses confidence labels and conservative unknown handling;
- says unknowns should be surfaced as `NOT DETERMINED — CONTACT BUILDING DEPT` rather than guessed;
- lists data sources/model version in reports;
- charges **$49 CAD + HST per report**.

Primary public sources:

- https://permitsnapshot.ca/
- https://permitsnapshot.ca/about
- https://permitsnapshot.ca/disclaimers
- https://permitsnapshot.ca/blog

## Direct overlap with ProjectPermit

This overlaps ProjectPermit on several previously claimed differentiators:

1. **pre-quote timing** — PermitSnapshot explicitly markets to builders/GCs before quoting;
2. **address + scope input** — it asks for property details and proposed work;
3. **permit-requirement output** — reports include permit requirements with likelihood ratings;
4. **conservative uncertainty** — it exposes unknowns instead of always forcing a yes/no;
5. **source/transparency framing** — reports state sources/model version and confidence;
6. **cross-municipality coverage** — 414 Ontario municipalities is far broader than ProjectPermit's current Ontario footprint.

Therefore ProjectPermit can no longer claim that the Canadian market lacks a pre-application feasibility product.

## Important remaining differences

PermitSnapshot does **not yet publicly prove** all of the following:

- a B2B API, batch API, webhook or white-label contract;
- a lightweight high-frequency `required / likely_not_required / confirm` endpoint suitable for marketplace/CRM automation;
- stable rule IDs or deterministic reproducibility;
- explicit source-versioned municipality-specific rule logic for ordinary small renovation scopes;
- low per-call economics compatible with ProjectPermit's intended ~$0.20-$0.50 high-volume API model;
- externally benchmarked accuracy on ordinary historical cases.

Its public disclaimer materially limits its accuracy claims. It states that reports are generated entirely by AI, may contain errors/outdated information, can rely on general Ontario regulatory context, and may not reflect current municipality-specific by-laws, exceptions or site-specific amendments.

That keeps a possible narrow ProjectPermit wedge:

> **low-cost embedded deterministic applicability for ordinary renovation scopes, with maintained municipality-specific rules and auditable evidence, rather than a broad $49 feasibility report.**

But this wedge is now narrower and must be proven externally.

## Public-guidance precision signal

PermitSnapshot's public blog uses broad Ontario-level statements such as structural/plumbing/electrical/HVAC changes generally requiring permits.

That is useful guidance, but it does not publicly demonstrate all municipality-specific exceptions already observed in ProjectPermit research (for example Toronto's conditional basement-finishing exemption versus Mississauga's explicit basement-finishing permit requirement).

This is not evidence that PermitSnapshot's paid reports are wrong; it only means public evidence does not yet establish the same deterministic municipal granularity ProjectPermit is trying to provide.

## Direct falsification outreach

A short email was sent on 2026-08-28 to the contact address published in PermitSnapshot's own disclaimer (`Jackie605324@icloud.com`).

Questions:

1. Is there already, or is there planned, an API / batch / white-label integration?
2. For ordinary renovation scopes, is permit applicability municipality-specific or mainly broader Ontario-level feasibility guidance?
3. Would PermitSnapshot support a lightweight software-platform use case returning only `required / likely not required / confirm` plus source evidence?

No customer metrics or confidential information were requested.

Evidence status: **awaiting reply**.

## Go / No-Go impact

This discovery reduces ProjectPermit defensibility from **2/10 to 1/10**.

Reason:

- a Canadian product already independently converged on address + scope -> pre-quote permit feasibility;
- it already copies several transparency/uncertainty ideas that ProjectPermit previously treated as differentiation;
- its 414-municipality coverage demonstrates that breadth can be marketed with a much lighter AI-driven maintenance model.

However, because no public API/high-frequency economics or municipality-specific deterministic contract has been verified, this does **not yet** satisfy the existing stop trigger for an exact Canadian supplier with acceptable integration/procurement economics.

Revised score effect: **51 -> 50 / 100**.

Decision:

> **CONTINUE ONLY AS FALSIFICATION / VALIDATION. DO NOT EXPAND PRODUCT SCOPE.**

At 50/100, the next materially negative qualified signal should trigger an explicit stop/re-scope review.

## Immediate stop/re-scope conditions specific to PermitSnapshot

Move below 50 and initiate a No-Go/re-scope review if PermitSnapshot confirms any of the following:

- it already offers an API/batch/white-label integration suitable for contractor/marketplace software;
- it already provides reliable municipality-specific ordinary-renovation applicability at economics compatible with high-frequency workflows;
- buyers/platforms prefer its broad AI feasibility approach and do not value deterministic municipality-specific maintenance enough to switch/pay;
- ProjectPermit E3 shows no meaningful practical accuracy advantage on the edge cases where PermitSnapshot/generalized guidance is coarse.

## Do not react by feature expansion

Do not respond to PermitSnapshot by adding:

- more Ontario municipalities;
- zoning/lot-coverage/development-charge reports;
- grant discovery;
- broad property feasibility;
- document review;
- filing workflow.

Those would move ProjectPermit directly into PermitSnapshot/LandLogic/PermitFlow territory without evidence.

The only rational next proof is whether a **smaller, cheaper, deterministic, embeddable applicability layer** is valuable enough to buy.