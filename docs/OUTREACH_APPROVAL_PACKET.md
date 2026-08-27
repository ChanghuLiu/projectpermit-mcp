# ProjectPermit External Outreach Approval Packet

Updated: 2026-08-27

Status: **READY FOR OWNER APPROVAL — NOTHING SENT**

This file defines the exact first external action so approval can be narrow and unambiguous. No email, marketplace form, phone call or partner application has been sent/submitted.

## Proposed Batch A — five direct written contacts

These five are selected because they test different workflow hypotheses and have a direct public written contact route. Start with five rather than twenty so messaging can be corrected after the first replies.

| Order | Company | Workflow hypothesis | Public route | Subject |
|---:|---|---|---|---|
| 1 | iPermit | Is low-cost triage useful before full permit expediting? | `STSupport@iPermitUSA.com` | `Upstream permit preflight before an iPermit order?` |
| 2 | Property Meld | Does permit research belong before maintenance dispatch/approval? | `support@propertymeld.com` | `Permit preflight inside property-maintenance work orders` |
| 3 | Provizual | Is permit applicability already known before AHJ inspection tracking begins? | `sales@provizual.com` | `Upstream permit-requirements signal for AHJ inspection workflows` |
| 4 | AppWork | Can a work-order/estimate approval step trigger permit preflight? | `sales@appworkco.com` | `Permit preflight at work-order / estimate approval time` |
| 5 | SyncEzy | Do Procore customers repeatedly need permit-research logic in custom integrations? | `support@syncezy.com` | `Reusable permit-preflight component for Procore integrations` |

Full tailored bodies are in `docs/OUTREACH_BATCH_01.md`.

Before sending, re-verify each public contact on its official site/marketplace page because public routing addresses can change.

## Why these five first

This batch spans five different positions in the workflow:

1. downstream full permitting;
2. property-maintenance orchestration;
3. AHJ/inspection tracking;
4. maintenance operations;
5. integration consultancy.

If several independently identify the same upstream permit-decision pain, confidence increases. If all say applicability is already known before their systems enter the workflow, ProjectPermit's wedge should be downgraded before expanding outreach.

## Sender identity required before sending

Owner should explicitly approve:

- sender display name;
- sender email/account or alias to use;
- whether to describe the sender as `ProjectPermit`, an independent developer, or a company/organization name;
- optional public website/GitHub link to include;
- whether replies should go directly to the sender account.

Do not invent a company name, job title, legal entity or domain.

## Proposed signature

Use only after sender identity is approved:

```text
<approved sender name>
ProjectPermit / independent developer
https://github.com/ChanghuLiu/projectpermit-mcp
```

If the owner prefers not to expose GitHub in first contact, omit the final line and offer the live endpoint only after a reply.

## First-message rules

- No attachment.
- No wallet/x402 explanation in the first message.
- No claim that ProjectPermit is a legal/compliance authority.
- No claim of nationwide coverage.
- No TAM/revenue claims.
- No request for customer PII.
- No request to buy.
- Primary ask: validate workflow and monthly decision frequency.
- Secondary ask: 20 anonymized scopes or a small free MCP pilot if the pain is real.

## Reply handling

Immediately record each reply in `data/partner_feedback.csv` using:

- response class A-F;
- workflow step;
- jobs/work orders per month when given;
- permit-research share when given;
- candidate preflights/month;
- address-aware need;
- price reaction only when actually discussed;
- requested jurisdictions with expected volume;
- pilot scopes/calls;
- integration status.

Never manufacture missing values. Blank means unknown.

Run:

```bash
python scripts/summarize_partner_feedback.py
```

after responses are recorded.

## Follow-up trigger

Send a pilot invitation only when the response is `A — integration interest` or a strong `B — workflow confirmed`.

Recommended next ask:

> If useful, send 20 anonymized recent scopes or run them through the free MCP preview. I only need to learn whether the result changes the workflow, the rough monthly frequency, and which jurisdictions are missing.

Use `docs/DESIGN_PARTNER_TRIAL.md` for the pilot. No wallet or payment is needed during initial validation.

## Stop conditions during Batch A

Pause before sending the remaining targets if:

- a recipient reports a serious accuracy/liability concern that applies broadly;
- two or more recipients say permit applicability is already known before their workflow;
- the contact route is clearly inappropriate for partnership/product feedback;
- a recipient asks for confidential/customer data that is unnecessary for the pilot;
- external feedback exposes a product/safety issue that should be fixed before more outreach.

## Approval requested

A narrow approval can be phrased as:

> Approve Batch A. Send as `<display name>` from `<email/account>`, describe me as `<independent developer / approved organization wording>`. GitHub link: `<include / omit>`.

Until that explicit approval is received, **do not send anything externally**.
