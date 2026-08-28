# Restoration / Insurance Claims Buyer-Class Boundary — 2026-08-28

## Purpose

ProjectPermit's upstream marketplace/operator discovery is now saturated. A new target should only be added if it contributes a materially different buyer/workflow class or a stronger evidence surface.

Canadian property-restoration networks qualify as a distinct falsification route because the workflow is not `homeowner lead -> contractor quote`. It is closer to:

`insured property loss -> damage assessment -> repair scope / estimate -> insurer approval -> rebuild`

The specific question is whether municipal permit applicability is a repeated unresolved decision **after the repair scope is known but before rebuild work begins**, and whether a centralized restoration operator would buy that logic externally or encode it inside its own claims/restoration systems.

This document does not add market score or assume restoration activity equals ProjectPermit calls.

---

## Primary target: On Side Restoration

### Why the insertion point is real

On Side's public restoration-process material describes three stages:

1. Emergency / mitigation;
2. Estimate / Approval;
3. Rebuild / Repair.

After mitigation, the Project Manager details a **scope of work**. During Estimate / Approval the Project Manager develops an itemized repair plan / scope of repair, which may be reviewed by an insurance adjuster before repair proceeds.

Source:

- https://www.onside.ca/en/2018/12/12/on-side-to-the-rescue

Current Project Manager job postings also say the role assesses damage and determines the scope of work, and current postings require Xactimate experience.

Sources:

- https://www.onside.ca/en/career/project-manager-iii-ottawa
- https://www.onside.ca/en/career/project-manager-sudbury

This establishes a real structured decision stage before rebuild rather than a speculative insertion point.

### Permit applicability is not constant across claims

On Side's current FAQ explicitly distinguishes cases:

- larger fires typically require a building permit;
- cosmetic-only damage generally does not require filing a building permit.

Source:

- https://www.onside.ca/en/questions

This is important because the restoration workflow contains both permit-positive and permit-negative work. It is not automatically equivalent to downstream permit filing where every job has already been classified as requiring a permit.

It does **not** reveal what share of repair scopes are genuinely uncertain at the estimate/approval stage.

### Centralized technology surface

On Side operates the proprietary **eClaim** project-management system. Its public B2B material says business partners can use eClaim to access project photos, day-to-day activity and relevant property-damage file details. On Side Live combines eClaim with its contact-centre services.

Sources:

- https://www.onside.ca/en/who-we-serve
- https://myclaims.onside.ca/public/

On Side also describes eClaim as supporting internal staff and external clients across its network.

Source:

- https://www.onside.ca/en/2024/06/06/on-side-restoration-continues-to-expand-in-the-atlantic

This makes an operator-level integration question more credible than a branch-by-branch integration thesis. It still does **not** prove that one external API can be inserted into eClaim or that permit applicability is centrally tracked.

### Scale anchor — context only

Intact Financial Corporation's 2023 Social Impact and ESG Report states that On Side helped **over 35,000 business and residential customers** in 2023, including Intact and non-Intact customers. The same report says On Side had grown to nearly 50 locations and almost 2,000 employees.

Source:

- https://cdn.intactfc.com/presentations/IFC-2023-Social-Impact-and-ESG-Report_EN.pdf

35,000/year is approximately **2,917 customers/month** as a gross activity context.

It is **not**:

- a residential-only denominator;
- a current-family denominator;
- an unresolved-permit denominator;
- a count of rebuild scopes;
- or a ProjectPermit call forecast.

If ProjectPermit's commercial-scale gate is 500 candidate preflights/month, then 500 / 2,917 is about **17.1%** of this gross historical activity anchor. Therefore a material fraction of On Side files would need to reach the relevant permit-decision state before this single operator could independently satisfy the 500/month gate.

That fraction is unknown and must not be assumed from company scale.

Current On Side public material separately states more than 1,900 personnel and over 1,000 emergency response vehicles coast to coast.

Source:

- https://www.onside.ca/en/

Those workforce/fleet counts confirm operational scale but are not call-volume evidence.

### Centralized decision-maker route

On Side's current leadership page lists:

- Ed Gooyers — Vice President, National Corporate Operations;
- Amanda Henry — Head of Technology, Corporate Strategy.

Source:

- https://www.onside.ca/en/about/leadership

The current Media page lists Sonia Manson, Director, Communications and Corporate Affairs, at `media@onside.ca` as a public corporate contact.

Source:

- https://www.onside.ca/en/about/media

ProjectPermit did **not** guess private/direct executive email addresses. The bounded workflow question was sent to the current public corporate route with a request to forward it to the relevant Operations / Technology owner.

Outreach message ID:

- Gmail `1a04a384024a29e7`

Delivery status at the time of this review:

- sent successfully from Gmail;
- no immediate delivery-failure message observed;
- no human response yet;
- evidence level remains **E0**.

---

## Independent industry corroborator: WINMAR

WINMAR is useful only to test whether the workflow class exists beyond one company.

Its current general-contracting page says its network has **90+ locations across Canada** and provides full-service contracting from conception and **permits** through demolition, construction and inspections. The service list includes framing, windows, electrical and other work that overlaps ProjectPermit-relevant repair/rebuild scopes.

Sources:

- https://www.winmar.ca/service/general-contracting/
- https://www.winmar.ca/residential/

Interpretation:

- permit handling is visibly part of a second national restoration/reconstruction network;
- the restoration/claims buyer class is not unique to On Side;
- WINMAR's public franchise/network model does **not** currently prove a centralized shared data/API surface comparable to On Side's eClaim;
- no outreach to WINMAR is justified now because On Side already provides the stronger, centralized falsification experiment.

WINMAR is therefore **corroboration, not a second denominator and not a second same-day outreach target**.

---

## Exact bounded E2 question

For one recent complete month, among **residential repair/rebuild files where the scope was already defined but repairs had not yet started**:

> approximately how many required someone to decide whether a municipal building permit was needed?

Useful bands:

- under 500/month;
- 500–2,000/month;
- 2,000–10,000/month;
- over 10,000/month.

The second question is build-vs-buy:

> if that decision repeats across branches, would the operator normally encode and maintain municipal logic inside its own restoration/claims system, or consider an external maintained deterministic API?

Answers such as `not tracked`, `already obvious before this stage`, `handled locally`, or `we would build it internally` are valid negative evidence.

---

## Rescue conditions

This buyer class becomes material rescue evidence only if a real operator can establish most of the following:

1. **>=500 candidate permit-preflight decisions/month** in covered/current-family-like residential repair/rebuild work, using a bounded recent period;
2. permit applicability is genuinely unresolved for a meaningful share after scope creation rather than already obvious to the PM;
3. scope/eClaim/Xactimate data contains enough decision facts to automate a useful share without adding a high-friction questionnaire;
4. the decision materially affects estimate, routing, schedule, insurer approval or rebuild start;
5. one centralized integration can serve meaningful multi-branch traffic;
6. the buyer prefers external maintained cross-municipality logic for a concrete cost/reliability/maintenance reason;
7. E4/E5 can subsequently be demonstrated through repeated calls or integration/resource/price commitment.

No single public scale number satisfies these gates.

---

## Kill / downgrade conditions

This route should be closed or deprioritized if substantive operator evidence shows any of the following:

- fewer than 500 relevant candidate decisions/month after filtering ordinary mitigation/cosmetic work;
- permit need is normally obvious to restoration PMs before the estimate/approval stage;
- permit handling is delegated locally and cannot benefit from a central integration;
- current eClaim/Xactimate data lacks the facts needed for low-friction applicability decisions;
- permits matter mainly for a narrow large-loss subset whose frequency is too low;
- the operator already has sufficient internal rules/vendor capability;
- the operator would build the relevant municipal rules internally rather than buy a maintained external API;
- ProjectPermit's current eight families do not map to enough reconstruction scopes;
- the buyer only values full permit procurement/expediting rather than preflight.

---

## Why this does not change the score now

The public evidence proves four useful structural facts:

- a repair scope is created before rebuild;
- permit applicability varies across restoration work;
- On Side has a centralized project-management/data surface;
- the company/network is operationally large enough that a bounded denominator is worth asking for.

It does **not** prove:

- a recent monthly unresolved permit-decision count;
- representative current-family share;
- fact sufficiency;
- material workflow effect;
- external-buy preference;
- E4 usage;
- E5 commitment.

Therefore:

> **No Go/No-Go score change. ProjectPermit remains 50/100 — PAUSE / RE-SCOPE.**

The value of the restoration buyer class is that it creates one new, structurally independent falsification route. It must now produce private workflow evidence or be closed; more restoration-company name collection is not useful.