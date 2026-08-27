# Outreach Batch 04 — Sent Log

Date: 2026-08-27

Purpose: move validation toward bounded workflow evidence and representative historical cases. Do not score routing acknowledgements, AI support answers, or positive opinions as market validation.

## Buildxact follow-up

Original recipient: `support@buildxact.com`

Buildxact returned an answer explicitly identified as composed by its AI support agent. The answer described REST API subscription/staging and date-bounded WIP report export capabilities.

Evidence classification: **E0 for market validation**.

Why: it contains useful technical/routing information but no human workflow claim, denominator, historical cases, observed usage, or economic commitment.

Action taken: replied in-thread asking for routing to a human in Product, Integrations/Partnerships, or Customer Success who can provide a bounded workflow count/timeframe or 5–20 de-identified representative historical scopes.

Do not upgrade this thread merely because the technical response was relevant.

## Association of Professional Builders (APB)

Recipient: `hello@apbbuilders.com`

Subject: `Do builders repeatedly research permit applicability before quoting?`

Why targeted: Buildxact publicly references APB in its partner/consultant material, and APB works across builder businesses. The purpose is to seek cross-builder workflow evidence rather than another software-platform opinion.

Evidence requested:

- bounded recent denominator/timeframe for permit-applicability research during estimate/quote workflows; or
- 5–20 representative de-identified historical scopes with the manual permit-applicability outcome.

Current classification: **no evidence yet**.

## Ontario Home Builders' Association (OHBA)

Recipient: `info@ohba.ca`

Requested routing: Paul Newman, Manager, Renovator & Regulatory Affairs, or the most relevant equivalent.

Subject: `For Renovator & Regulatory Affairs: permit research in real renovation workflows`

Why targeted: the role and member base are closer to real Ontario renovation/regulatory workflow evidence than a generic SaaS support inbox.

Evidence requested:

- bounded recent renovator workflow count/timeframe; or
- 5–20 representative de-identified historical renovation scopes with the actual permit-applicability outcome.

Current classification: **no evidence yet**.

## MaintainX

Current response is an automated support-ticket acknowledgement (`ticket #62973`).

Evidence classification: **E0**.

Do not pause engineering or validation work while waiting for a human reply.

## New low-friction benchmark path

A partner no longer needs a platform adapter, API key, or wallet to run historical cases. Use:

```bash
python scripts/run_remote_historical_benchmark.py path/to/partner_cases.csv \
  --output path/to/partner_cases.evaluated.csv \
  --client-tag partner-pilot-01
```

The public benchmark request is tracked in GitHub issue #2. Historical case data must remain de-identified and should not be posted publicly.

## Evidence rule

Keep the ladder strict:

`E2 bounded workflow -> E3 representative historical benchmark -> E4 repeated external usage -> E5 economic/resource commitment`

Replies are leads, not validation by themselves.
