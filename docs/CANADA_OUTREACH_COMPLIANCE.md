# Canadian Outreach Compliance Gate

Updated: 2026-08-27

Purpose: keep Canadian design-partner outreach legally and operationally separate from product validation. This document is a conservative workflow control, not legal advice.

## Why this exists

ProjectPermit is currently contacting businesses about a commercial product/API. For recipients in Canada, an unsolicited email may be a Commercial Electronic Message (CEM) under Canada's Anti-Spam Legislation (CASL).

Current CRTC guidance states that a CEM generally requires:

1. prior express or qualifying implied consent;
2. identification/contact information; and
3. a working unsubscribe mechanism.

A publicly visible business email is **not automatically permission to send**. CRTC guidance says conspicuous publication can support implied consent only where the address was published by/for the recipient, there is no statement against unsolicited CEMs, and the message is relevant to the recipient's business role/functions. The sender has the burden of proving the basis and should preserve contemporaneous records such as the source URL and date.

CRTC material also states that CEM identification must include a mailing address, which must remain valid for at least 60 days, and an unsubscribe mechanism that is simple/readily performed. Unsubscribe requests must be acted on within 10 business days.

## Current ProjectPermit gate

**Do not send cold commercial email to Canadian contractor/operator prospects yet.**

The current sender identity is:

- Display name: `ProjectPermit`
- Email: `launchcircle.server@gmail.com`

The current outreach signature does not yet contain an approved business mailing address or standardized unsubscribe instruction. Do not invent or expose a personal address to fix this.

Canadian operator prospects may still be researched, ranked, and prepared internally. Their publicly posted contact details may be recorded only for due-diligence/validation planning; recording an address does not itself establish consent.

## Required pre-send record

Before a Canadian cold CEM is sent under a conspicuous-publication theory, create or complete a row in `data/outreach_consent_registry.csv` with:

- company and recipient address;
- first-party source URL;
- date checked;
- evidence that the address was conspicuously published by/for the recipient;
- whether any `no unsolicited messages` restriction was present;
- why ProjectPermit's message is relevant to the recipient's business role/functions;
- consent basis;
- approved sender mailing-address status;
- unsubscribe mechanism status;
- final `approved_to_send` status.

If any required field is uncertain, leave the target blocked.

## Safer validation alternatives while blocked

Continue the work without waiting for email permission:

- analyze public municipal permit activity in aggregate;
- build the Jobber connector/test-account adapter without customer data;
- prepare 20-case benchmark templates;
- use platform developer/support channels for technical eligibility questions;
- identify opt-in partner/application channels;
- seek introductions or explicit inbound interest;
- prepare Canadian operator outreach for later approval rather than sending it now.

## Existing emails

Do not retroactively classify already-sent messages as compliant or non-compliant in this document. Preserve their actual send history and apply the stricter gate to future Canadian cold operator outreach.

## Official references reviewed 2026-08-27

- CRTC CASL FAQ: https://www.crtc.gc.ca/eng/com500/faq500.htm
- CRTC Guidance on Implied Consent: https://crtc.gc.ca/eng/com500/guide.htm
- CRTC Act/regulations/guidelines overview: https://crtc.gc.ca/eng/internet/anti/reg.htm
- CRTC information session / identification requirements: https://www.crtc.gc.ca/eng/com500/info.htm

Re-check official guidance before operationalizing a large outreach campaign.
