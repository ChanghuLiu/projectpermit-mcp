# Layer C maintained-code API precedent — 2026-08-30

## Purpose

Record a new qualitative buyer boundary from Contrax and compare it with current external products that monetize maintained regulatory/code content. This is validation evidence only. It does **not** authorize Layer C implementation or code-content licensing spend.

Layer C hypothesis:

> project / estimate facts -> current project-specific regulatory obligation bundle + official evidence + freshness/change identity

## 1. Contrax build-vs-buy signal

A Contrax respondent gave a clear qualitative boundary in the current outreach thread:

- for the narrow `do I need a permit?` decision, they would prefer to build the logic internally because it can fit their own flow and can be faster/cheaper;
- an external API that provides **updated legal requirements / regulations / building-code information** would be materially more useful.

A bounded monthly denominator was requested in follow-up (`under 10`, `10–50`, `50–200`, `200–500`, `500+`, `too rare`) and has **not** yet been received as of 2026-08-30.

### Evidence class

**E1 qualitative build-vs-buy evidence only.**

It supports a product-boundary hypothesis, not volume, willingness to pay, integration commitment, real usage or payment.

## 2. ICC Code Connect API — direct business-model precedent

ICC publicly offers **Code Connect API** specifically to integrate current ICC code content into third-party workflow software.

Official ICC source:

- https://solutions.iccsafe.org/codeconnect

Current public characteristics:

- positions the product as access to the **latest building code requirements within an existing workflow application**;
- software can search/import code content directly through the API;
- content is returned in JSON, from individual sections up to chapters;
- customers can access new versions as published as well as historical versions;
- ICC explicitly sells **real-time updates / never miss an update** as part of the value;
- the commercial structure requires both a **solutions implementation agreement/fee** and **content licensing**;
- content licensing is annual and varies by titles/jurisdiction or vendor/company characteristics;
- ICC also describes a vendor marketplace / reseller model around the API.

This is a strong precedent that the maintained-code-content layer can be sold as licensed infrastructure rather than a tiny commodity lookup.

### Evidence class

**Competitive/business-model precedent only.** It is not ProjectPermit buyer evidence and does not establish Canadian licensing feasibility.

## 3. UpCodes — project-specific requirement generation precedent

Current UpCodes documentation describes its Code Calculator as a project-specific tool that:

- takes jurisdiction, code year and project/design inputs;
- generates relevant compliance checks and code requirements;
- identifies missing inputs before calculation;
- flags non-compliant conditions;
- is explicitly useful during initial project phases and throughout the project lifecycle.

Sources:

- https://support.up.codes/support/solutions/articles/63000282986-an-introduction
- https://support.up.codes/support/solutions/articles/63000282987-setup-inputs
- https://cms.up.codes/features/projects

This demonstrates that `project facts -> applicable code requirements` is already a recognized software value unit. Public research in this pass did not establish a general UpCodes external API comparable to ICC Code Connect.

### Evidence class

Adjacent product precedent, not ProjectPermit buyer evidence.

## 4. Nimonik — maintained obligation/change layer precedent

Nimonik, headquartered in Montreal, publicly sells regulatory/standards compliance software centered on:

- regulations, standards, permits and obligations;
- continuous regulatory-change monitoring;
- structured requirements / obligations;
- version/change history;
- impact assessment and workflow actions;
- multi-jurisdiction coverage.

Sources:

- https://nimonik.com/
- https://nimonik.com/software/regulatory-change-management/
- https://nimonik.com/software/legal-register/

Nimonik is broader enterprise compliance software rather than a contractor preconstruction API, but it independently validates that **maintained obligations + change monitoring** can be the product rather than raw legal text alone.

### Evidence class

Adjacent-market precedent only.

## 5. Combined interpretation

The new evidence strengthens a specific product boundary:

### Weak / internally buildable value unit

`project facts -> permit required? yes/no`

This remains useful for ProjectPermit's current validation wedge, but Contrax explicitly indicates a capable software buyer may internalize this narrow logic.

### Stronger externalizable candidate

`project facts -> current regulatory/building-code obligations -> official authority/version -> workflow consequence -> change/freshness identity`

This better matches:

- Contrax's stated external interest;
- ICC Code Connect's licensed/current-content API model;
- UpCodes' project-specific compliance calculation model;
- Nimonik's maintained obligation/change-monitoring model;
- ProjectPermit's existing evidence/freshness/action-bundle architecture.

## 6. Commercial implication

Do **not** interpret this as permission to raise the existing `$0.20` preflight price or to build Layer C immediately.

It does change the pricing hypothesis that should eventually be tested:

- not merely a more expensive `permit yes/no` call;
- potentially an obligation/result bundle;
- a maintained cross-jurisdiction data capability;
- fixed platform licence / minimum commitment;
- implementation + licensed-content structure for buyers that need protected code content;
- premium tied to material quote/scope/schedule consequences rather than raw lookup count.

ICC is especially important because its public commercial model is **implementation + ongoing access + annual content licensing**, not a low-value per-call commodity model.

## 7. Licensing boundary remains a hard gate

The precedent also reinforces rather than removes the Canadian licensing issue.

Existing ProjectPermit research currently separates source-rights tiers:

- Ontario enacted statutes/regulations: comparatively permissive commercial reuse subject to conditions;
- Ontario Building Code Compendium: commercial reproduction/distribution requires ministry licensing;
- NRC National Building Code: commercial reproduction requires written consent;
- Québec LégisQuébec: restrictive reproduction/download/storage/adaptation terms; linking is safer, and written clarification is still required for structured derived facts.

Therefore no protected-code corpus should be ingested into a commercial Layer C product before the relevant rights are clear.

## 8. Decision consequence

**No E-level increase.**

Current classification:

- Contrax product-boundary signal: **E1**;
- bounded buyer denominator: pending;
- Layer C representative build: not started;
- real external usage: **E4 = 0**;
- payment/economic commitment: **E5 = 0**.

The evidence does, however, make the next falsification question sharper:

> For software platforms that say maintained regulatory/code content is useful, how many real pre-quote/project workflows per month need it, what material quote/scope/schedule decision changes, and at meaningful volume would they buy a maintained/licensed external layer rather than build it internally?

Until that is answered with bounded workflow evidence, Layer C remains validation-only.
