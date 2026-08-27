# ProjectPermit Design-Partner Trial

Updated: 2026-08-27

## Purpose

This is a **workflow-fit trial**, not a sales contract and not municipal authorization. The goal is to determine whether ProjectPermit belongs at a repeated software decision point and whether the resulting call density can support a commercial API.

A useful trial is small: **20 anonymized real scopes** from one existing contractor/property/construction workflow, followed by one short review of accuracy, missing coverage and monthly frequency.

## No wallet required for the pilot

Design partners should use the standard MCP developer-validation preview:

`https://projectpermit-mcp-production.up.railway.app/mcp`

The preview is temporarily free so workflow value can be tested before commercial packaging is locked. Partners do **not** need MetaMask, USDC, x402 signing or a billing account for this pilot.

Paid HTTP/x402 transports remain available for payment-plumbing validation, but there is no reason to introduce wallet friction during initial product validation.

## Recommended 20-case sample

Prefer cases that represent the real distribution of work, not twenty carefully selected examples designed to make the product look good.

A strong sample includes:

- 10 routine/high-frequency jobs or work orders;
- 5 cases where staff currently stop to research permit requirements;
- 3 ambiguous/property-sensitive cases if available;
- 2 recent cases where the original permit expectation was wrong, disputed or surprisingly expensive.

If the workflow has no permit-research friction, that is valuable negative evidence and should be recorded rather than forcing a pilot.

## Safe data-sharing rule

Partners can remove customer names, phone numbers, email, account IDs, tenant information, contract values and other unnecessary personal/commercial identifiers.

For rule-only tests, a civic address is not required. Use `resolve_address=false` and provide municipality + normalized project facts.

For address-aware tests, use a real property address only when the partner is comfortable doing so and when zoning/heritage/property overlays are material to the question. ProjectPermit's structured usage telemetry does not log raw civic addresses or coordinates, but the partner should still minimize unnecessary data.

Template: `data/design_partner_scope_template.csv`

## Stable integration tag

Use one non-PII tag for the pilot so repeated calls can be measured without storing the raw integration name in telemetry:

```json
{
  "context": {
    "client_tag": "partner-pilot-random-id"
  }
}
```

Do not put a person's name, email, address, API key or secret in `client_tag`.

The server stores only a short SHA-256-derived hash of this tag in `PROJECTPERMIT_USAGE` logs.

## What ProjectPermit returns

The trial should evaluate whether these fields are useful enough for automation:

- determination such as `REQUIRED`, `LIKELY_NOT_REQUIRED` or `MUNICIPAL_CONFIRMATION_REQUIRED`;
- confidence;
- stable rule id;
- official-source evidence;
- machine-readable requirements;
- address/property context when requested and supported;
- explicit uncertainty rather than a guessed approval.

The trial is **not** testing permit filing, plan review, approval guarantees, inspection scheduling or human expediting.

## Trial scorecard

For each of the 20 cases record:

| Metric | Meaning |
|---|---|
| useful routing result | Would the result have changed or automated the next workflow step? |
| manual agreement | Does it agree with the team's current/manual understanding? |
| evidence useful | Is the official-source evidence sufficient to trust the routing decision? |
| confirmation needed | Did the result correctly preserve uncertainty, or was it too conservative? |
| missing project fact | Did the schema lack an important scope distinction? |
| missing jurisdiction | Was coverage the only blocker? |
| latency acceptable | Is the call fast enough at the intended workflow step? |

Do not treat disagreement as automatically proving ProjectPermit wrong or the manual process wrong. Investigate the official source and classify the cause.

## Pilot pass criteria

A 20-case pilot is promising when most of the following are true:

- at least 15/20 results are useful for workflow routing;
- official evidence is considered materially better than a generic AI answer;
- no serious false `LIKELY_NOT_REQUIRED` result is found;
- confirmation/uncertain results are operationally acceptable rather than useless;
- the partner can identify a production trigger for the call;
- the partner estimates **500+ candidate preflights/month**, or has strategic distribution across many customers;
- address-aware results create enough additional value that roughly `$0.20-$0.50/call` does not break the workflow economics.

A strong design partner is **2,000+ candidate calls/month**. Five such integrations would reach the initial 10,000 monthly-call commercial checkpoint.

## Pilot fail / pivot signals

Treat these as real negative evidence:

- permit applicability is always known before the partner's software sees a job;
- staff still need full human research after nearly every result;
- users only want permit submission/expediting rather than preflight;
- most relevant work requires unsupported licensed datasets or engineering judgment;
- relevant events occur only a few times per month;
- the partner would never automate routing from an evidence-linked preflight regardless of accuracy;
- required jurisdiction maintenance cost is too high relative to expected calls.

## Post-pilot questions

After the 20 cases, collect only the numbers needed for the business decision:

1. jobs/work orders/projects per month;
2. percentage that reaches a permit-research decision;
3. resulting candidate preflights/month;
4. whether one or multiple calls occur as scope changes;
5. address-aware share;
6. top requested jurisdictions by monthly volume;
7. price reaction at `$0.25` and `$0.50` per address-aware result;
8. preferred commercial mechanism: per-call, monthly commitment, API key/invoice or marketplace billing;
9. blocker to production adoption;
10. willingness to continue with a technical integration.

Record the result in `data/partner_feedback.csv`.

## Decision after each partner

### Expand coverage

Only when a missing jurisdiction is attached to credible repeat volume. Example:

`Los Angeles + Phoenix + Dallas = 4,000 candidate calls/month` is meaningful evidence.

`We might need Phoenix someday` is not.

### Continue integration

Prioritize partners that can produce 500-2,000+ calls/month and can embed the decision without new human operations.

### Stop pursuing the account

If the need is one-off homeowner guidance, full managed permit submission, or a workflow where applicability is already fully resolved before the product enters.

## Trial invitation sentence

When outreach receives interest, the next ask can stay simple:

> If useful, send 20 anonymized recent scopes or run them through the free MCP preview. I only need to learn whether the result changes the workflow, the rough monthly frequency, and which jurisdictions are missing.

No paid transaction is necessary for this validation stage.
