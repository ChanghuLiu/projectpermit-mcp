# Permitio Downstream Intake Boundary — 2026-08-28

## Why this matters

ProjectPermit is testing whether a permit-applicability decision is still unresolved at a useful upstream point in contractor/construction software.

On 2026-08-27, ProjectPermit asked Permitio a deliberately falsifying workflow question about jobs reaching its Jobber-connected permit workflow:

- were inbound jobs already known to require a permit, or
- did Permitio still need to determine whether a permit was required at all before filing?

Permitio's Ruslan Nikonchuk replied, in substance, that contractor jobs require permits and that contractors already know which permit they need.

When asked for a recent monthly volume bucket to bound the observation, he declined to share internal information because ProjectPermit could be a potential competitor.

The thread was then closed politely without further pressure.

## Evidence classification

This is **E1 — opinion/workflow boundary only** under `docs/VALIDATION_EVIDENCE_STANDARD.md`.

Why it is not E2:

- no recent denominator was provided;
- no timeframe-specific job count was provided;
- no measured percentage of already-permit-positive intake was provided;
- no historical sample was provided.

Do not convert this statement into a numeric incidence rate.

## What the evidence does establish

For the Permitio workflow described by the respondent, the useful permit-applicability decision appears to occur **before Permitio intake**.

That is meaningful negative evidence against positioning ProjectPermit directly in front of permit filing/expediting vendors if their incoming contractor jobs are already permit-positive.

It also fits the structure of downstream permit-management products generally: by the time a job is intentionally sent into a filing/expediting workflow, someone may already have classified it as a permit job.

## What it does not establish

This response does **not** prove that:

- all contractors across Canada/Quebec/Ontario always know permit applicability;
- homeowner leads are already classified before quote creation;
- renovation marketplaces know permit applicability at intake;
- estimator/CRM/field-service software users never research permit need before proposal signature;
- current ProjectPermit families have zero unresolved upstream incidence.

The respondent is associated with a permit-focused downstream workflow, so selection effects are strong.

## Validation implication

Stop spending validation effort asking downstream permit-filing vendors whether their already-routed permit jobs still need an applicability decision.

The higher-value question is one workflow step earlier:

> Before a job is deliberately routed to Permitio, a permit department, an expediter, or a municipal application workflow, how often does the quote/intake/project system still need to determine whether a permit is required at all?

Therefore prioritize:

- renovation marketplaces at project intake;
- contractor CRMs/estimators before proposal signature;
- Quebec contractor SaaS before job activation;
- multi-account integrators who can observe repeated pre-quote decisions;
- neutral industry research that can measure incidence before permit-positive routing.

## Score impact

**No score change from this E1 statement alone.**

ProjectPermit remains **50/100, PAUSE / RE-SCOPE**.

However, this is a directional negative signal consistent with an existing explicit stop condition in the canonical scorecard:

> permit necessity is usually known before the workflow reaches our insertion point.

That stop condition should be tested with representative E2/E3 evidence at the actual proposed upstream insertion point, not with more downstream permit-vendor interviews.

## Practical kill threshold

If multiple independent upstream software buyers or representative E2 datasets show that permit need/type is already known before estimate/proposal/job creation for most relevant projects, the ProjectPermit upstream preflight thesis should move toward **No-Go** even if technical accuracy remains strong.

Conversely, a rescue requires bounded evidence that a material share of current-family projects are still unresolved at the quote/intake stage, ideally with >=500 qualifying events/month in one aggregated workflow.
