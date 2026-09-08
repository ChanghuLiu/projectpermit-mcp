# England Works Watch — Status

Updated: 2026-09-08

Public description: **UK sponsor compliance/change intelligence**. The earlier Railway roadworks prototype is legacy and is not the current product direction.

## Current maturity

England Works Watch V0.1 is live on Railway as a **Skilled Worker sponsor-duty change-impact preflight** with deterministic decisions, official-source lifecycle gating, x402 payment enforcement, public agent discovery, MCP Registry publication, and persistent privacy-minimal funnel analytics.

It is **not yet declared at full UK Taxi commercial-infrastructure parity** because one owner-controlled Base-mainnet settlement and the resulting PayAI Bazaar listing remain outstanding. Organic external customer demand is a separate commercial-validation metric and must not be inferred from owner/CI activity.

## Completed product and release gates

- Skilled Worker + sponsor duties only
- 10 supported sponsor event types
- four-state fail-closed decision contract: `AFFECTED`, `NOT_AFFECTED`, `REVIEW_REQUIRED`, `INSUFFICIENT_INPUT`
- official GOV.UK evidence, source version/effective date and required next action per substantive decision
- persistent runtime source fingerprints and fail-closed source lifecycle gate
- 14 automated tests passing in the Railway release build
- 25 / 25 acceptance fixtures passing
  - 10 independent cases
  - 6 negative controls
  - 5 sponsor-event cases
  - 4 fail-closed cases
- agent tool-selection benchmark release gate: baseline 14 / 25 (56%) -> effective 25 / 25 (100%)
- 4 / 4 official source audit baselines unchanged at release
- MCP 2.x Streamable HTTP transport smoke PASS
- x402 unpaid/non-leak release smoke PASS

## Production state

- Railway production: `https://england-works-watch-production.up.railway.app`
- MCP endpoint: `https://england-works-watch-production.up.railway.app/mcp`
- production health: ready
- payment enforcement: enabled
- network: Base mainnet `eip155:8453`
- asset: native Base USDC
- seller wallet: `0xDAAef0FD525278aAD0bA11066A96c338642A3d1A`
- facilitator: `https://facilitator.payai.network`
- `assess_change_impact`: `$0.02`
- `batch_assess_changes`: `$0.05`
- persistent SQLite analytics on Railway volume `/data`

## Outside-in evidence

A GitHub-hosted public runner has verified the live production service, not just local code:

- `PUBLIC_DISCOVERY_RUNTIME=PASS`
- `PRODUCTION_MCP_UNPAID_X402=PASS`
- `PERSISTENT_PAYMENT_ANALYTICS=PASS`
- benchmark-driven MCP discoverability smoke PASS
- payment challenge verified as exact Base mainnet / 20,000 USDC atomic units / expected payee
- unpaid call verified not to leak the protected sponsor decision

Public discovery includes health/status/version/metrics, OpenAPI, llms.txt, robots.txt, sitemap.xml, x402 metadata, MCP manifests/server card, agent manifests, Glama metadata, and AI/API catalogs.

## MCP Registry

Official MCP Registry listing is live:

- name: `io.github.ChanghuLiu/england-works-watch`
- version: `0.1.0`
- registry verification: `MCP_REGISTRY_LISTING=PASS`

The publish workflow is idempotent: an existing `0.1.0` version is treated as `ALREADY_EXISTS` and then independently verified through the Registry API.

## PayAI Bazaar

Current probe result:

- `PAYAI_MCP_BAZAAR_LISTING=PENDING_SETTLEMENT`
- current discovery query returns no England matches

Do not report Bazaar publication as complete until it is actually observed. The probe runs automatically and should be rechecked after a successful real settlement.

## Remaining owner validation gate

Repository script: `scripts/paid_mcp_buyer_smoke.py`

The script performs exactly one real `$0.02` Base-mainnet USDC call to `assess_change_impact`, with no retry loop. Before signing it hard-fails unless all of these match production expectations:

- network `eip155:8453`
- amount `20000` USDC atomic units
- native Base USDC contract
- pay-to `0xDAAef0FD525278aAD0bA11066A96c338642A3d1A`

It then requires a successful settlement receipt, transaction ID, and the expected deterministic `AFFECTED` / `EW-ABS-REPORT` result.

`EVM_PRIVATE_KEY` must exist only in the buyer's local environment. Never commit it, upload it, paste it into chat, or store it on Railway/GitHub.

After a successful owner settlement:

1. record only the non-secret settlement evidence/transaction hash;
2. classify it as `owned_mainnet_smoke`, not external demand;
3. re-run/observe the PayAI Bazaar probe;
4. confirm `paid_executed` in persistent analytics;
5. update this status only after Bazaar is actually observed.
