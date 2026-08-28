# Integrator Build-vs-Buy Boundary — 2026-08-28

## Purpose

DigitalStaff and TradeOps were originally added as independent implementation-side falsification targets. This review narrows what their current public evidence can and cannot tell us about ProjectPermit's remaining buy thesis.

The result is asymmetric:

- **DigitalStaff is a strong custom-build comparator.** It publicly sells construction automation, Buildertrend integrations, permit/compliance document automation, building-code / permit-regulation compliance workflows, and public-sector permit-review / grounded-policy automation. A capable integrator can therefore plausibly internalize a client-specific permit layer if the economics make sense.
- **TradeOps is mainly an incidence / workflow sensor.** Its public offer is field-service software implementation, catalog import and migration for Canadian trade businesses. The current public surface does not show custom regulatory automation or permit-applicability logic.

Neither finding is independent buyer evidence. Both targets still require a human answer before they can move the commercial score.

## DigitalStaff — custom-build comparator

DigitalStaff's current construction page explicitly advertises:

- custom construction automation and integrations;
- automated permit tracking and renewals;
- compliance-document automation;
- compliance handling that includes building codes and permit regulations;
- Buildertrend automation connecting job data, cost codes and approvals to the office stack.

Source:

- `https://digitalstaff.ca/industries/construction`

Its public-sector page is more important for build-vs-buy interpretation. DigitalStaff publicly offers:

- permit-application completeness checks against requirements;
- structured reviewer handoff and audit trails;
- grounded citizen-service chatbots that answer only from approved published policies;
- source citation on every answer;
- escalation when the answer is unknown;
- deterministic automation for business execution, with workflows logged and reviewable.

Source:

- `https://digitalstaff.ca/industries/government`

DigitalStaff also publicly describes Buildertrend / QuickBooks integrations as a common construction use case and sells fixed-scope project builds plus ongoing managed automation.

Sources:

- `https://digitalstaff.ca/integrations/quickbooks`
- `https://digitalstaff.ca/pricing`

### What this proves

It is no longer reasonable to model a capable construction automation integrator as merely a distribution channel that lacks the technical ingredients to build regulatory workflow logic.

DigitalStaff publicly demonstrates most of the relevant implementation primitives:

1. construction-system integration;
2. permit/compliance workflow exposure;
3. grounded policy retrieval with citations;
4. deterministic execution;
5. audit trails;
6. ongoing managed maintenance.

That makes DigitalStaff a useful **build-vs-buy comparator** for the exact remaining ProjectPermit thesis.

### What this does not prove

The current public pages do **not** establish that DigitalStaff already delivers:

- pre-quote `permit required / not required` determination from renovation scope;
- a normalized cross-municipality permit-applicability engine;
- ProjectPermit-like deterministic rule IDs / version history;
- representative contractor demand for that decision;
- an external permit-specific API sold independently of a custom engagement.

Its construction permit examples are primarily tracking, renewal, documentation and compliance. Its government permit example is application completeness before reviewer intake. Those are adjacent to, but not the same as, ProjectPermit's upstream applicability decision.

### Falsification question

The useful question is therefore not simply whether DigitalStaff can integrate ProjectPermit.

It is:

> When multiple contractor clients need municipality-specific permit applicability before estimate / quote finalization, is it cheaper and more reliable for DigitalStaff to build and maintain each client's relevant municipal logic itself, or to reuse a maintained external cross-city deterministic/evidence-linked API?

**Positive evidence for ProjectPermit** requires DigitalStaff to identify repeated cross-client incidence and a concrete maintenance / reliability / evidence reason to prefer an external shared layer.

**Negative evidence** is a credible statement that this is straightforward enough to implement and maintain inside normal custom automation engagements, that customers do not value the deterministic/evidence contract, or that the pre-quote decision is too rare to automate.

## TradeOps — workflow / incidence sensor, not a proven build substitute

TradeOps Solutions' current Canadian site positions the company around field-service software implementation.

Its public offer includes:

- supplier catalog imports and cleanup;
- software migrations;
- full field-service implementations;
- employee onboarding and configuration;
- Jobber, simPRO, ServiceTitan, Housecall Pro, FieldEdge and FieldPulse;
- fixed-price implementation services for Canadian trade businesses.

Source:

- `https://tradeopsolutions.ca/`

The current public page does not describe permit research, building-code logic, municipal compliance automation, custom AI/RAG, or a developer platform. That absence is **not** evidence that TradeOps clients never encounter permit uncertainty; it only means the public product evidence does not support treating TradeOps as a DigitalStaff-like technical substitution threat.

### Entity-disambiguation warning

Search results contain several unrelated businesses using `TradeOps` in their names. In particular, `tradeopssystems.com` is a separate U.S. business whose site mentions permit coordination. It must not be attributed to `tradeopsolutions.ca`.

The same caution applies to other unrelated TradeOps consulting / operations domains found by generic search.

### Falsification question

TradeOps remains useful because it sees implementations across several field-service platforms and Canadian trade businesses.

The narrow question is:

> Across residential construction/remodeling-type customers, how often is municipal permit applicability genuinely unresolved when a quote/job is configured, and where in Jobber / ServiceTitan / simPRO / Housecall Pro would a reusable preflight decision be inserted if the problem is repeated?

**Positive evidence** requires a repeated cross-client workflow plus a clear insertion point and a reason existing process/software is insufficient.

**Negative evidence** is that applicability is normally already known, handled downstream, uncommon in their customer mix, or too judgment-heavy / infrequent to merit another integration.

## Score implication

**No score change.**

The canonical score is already at 51/100 with competitive headroom at 1/10. DigitalStaff strengthens the build-in-house threat qualitatively, but public capability evidence is not the same as a buyer saying it would internalize this exact permit decision. TradeOps supplies no public permit-applicability substitute evidence.

Lowering the score again from these pages alone would double-count architecture risk already captured by BuilderAI, GoBuild, LandLogic and the build-vs-buy maintenance audit.

The next score movement should come from one of these stronger events:

- DigitalStaff or another integrator explicitly prefers internal build for the bounded workflow;
- a software buyer explicitly prefers an external maintained layer for a concrete cross-city cost/reliability reason;
- TradeOps / another multi-account implementer provides bounded repeated cross-client incidence;
- representative E3/E4/E5 evidence resolves usage, accuracy or willingness to pay.

## Bottom line

DigitalStaff makes the remaining ProjectPermit buy thesis harder: a competent integrator already has the tools to build grounded, audited, permit-adjacent automation inside a construction client's existing stack.

TradeOps does not add the same technical threat, but it is a useful cross-platform reality check on whether the upstream decision occurs often enough to deserve automation at all.

The remaining validation question is therefore still external and economic, not technical:

> **Do buyers or integrators encounter enough cross-city permit-applicability maintenance burden that they prefer a shared maintained API over a client-specific build or existing embedded workflow?**
