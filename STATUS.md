# ProjectPermit Status

Updated: 2026-08-26

## Current state

**Phase 0 testnet discovery / market-validation release readiness: PASS.**

**Phase 1A Toronto + Mississauga expansion: IMPLEMENTED.** Both cities have deterministic rule coverage plus first-party municipal address/zoning/heritage adapters.

**Phase 1B six-city rule footprint: IMPLEMENTED; public remote verification is running.** Laval + Longueuil rules have been added conservatively from current official municipal guidance.

ProjectPermit is an evidence-linked deterministic municipal permit preflight engine. The calling Agent normalizes project scope; the server applies municipal rules and returns official-source evidence. The rules engine does not call an LLM and payment remains outside BuildRequirements.

## Jurisdiction coverage

- `gatineau_qc` — deterministic rules + municipal address geocoder; PIIA/heritage machine overlays still unresolved
- `ottawa_on` — deterministic rules + address/zoning/heritage GIS
- `toronto_on` — deterministic rules + City address/zoning/heritage GIS
- `mississauga_on` — deterministic rules + City address/zoning/heritage/property GIS
- `laval_qc` — Phase 1B deterministic rules; address/GIS adapter pending
- `longueuil_qc` — Phase 1B conservative deterministic rules; address/GIS adapter pending

All transports call the same `preflight_service` before the jurisdiction router. For supported address jurisdictions, `resolve_address=true` enriches the request with first-party municipal property context. Laval and Longueuil should currently use `resolve_address=false`.

## Phase 0 completed

- Gatineau + Ottawa proving-ground rules across 8 normalized project families
- deterministic rule results with stable rule ids and official evidence
- public FastAPI, standard MCP v2, and x402-native paid MCP
- Base Sepolia x402 payment profile
- real buyer-side paid HTTP + paid MCP verification/settlement
- GoPlausible Bazaar canonical HTTPS indexing
- Docker + GitHub Actions CI
- no server-side LLM dependency
- no paid map/property-data dependency

## Phase 1A completed

- Toronto official required/not-required guidance converted to conservative deterministic rules
- Mississauga official required/not-required guidance converted to conservative deterministic rules
- Toronto first-party address + zoning + heritage resolution
- Mississauga first-party address + zoning + heritage + property resolution
- four-city routing exposed through HTTP, free MCP, paid MCP and x402 discovery
- shared address-aware preflight service removes transport drift

## Phase 1B implemented

- Laval rule coverage from current official renovation, shed, balcony and addition guidance
- Longueuil conservative rules from current permit portal, urbanism rules and July 2025 simplified permit sheets
- six-jurisdiction request/discovery schemas
- six-city free MCP smoke cases
- six-city paid-MCP unpaid challenge verification (no USDC spend)
- six-city HTTP x402/Bazaar unpaid challenge verification
- source manifest extended with Laval and Longueuil official sources
- regressions preserve ambiguous thresholds as `MUNICIPAL_CONFIRMATION_REQUIRED`

## Live services

- Paid HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP: `https://projectpermit-mcp-production.up.railway.app/mcp`
- Paid x402 MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Paid MCP exposes:

- `projectpermit_info` — free discovery/status
- `check_project_requirements` — x402-paid permit preflight

Current **testnet discovery price**: **$0.01 USDC per paid tool/API call** on Base Sepolia. This is not the intended commercial price.

## Verification policy

CI verifies Python 3.11/3.13, rule/schema/source contracts, address adapters, shared preflight behavior, MCP v2 integration, x402 wire behavior, Docker health, remote free MCP, remote paid-MCP unpaid challenge, remote HTTP Bazaar unpaid challenge, facilitator capabilities and canonical Bazaar state.

Real buyer-side x402 plumbing is already proven. **Do not spend additional test USDC for routine expansion smoke tests.** Expansion verification should use free discovery or unpaid 402 challenges.

Final canonical-HTTPS Phase 0 HTTP settlement transaction:

`0x2070aa9a55287162876d2d53a1f1ebe865ba912d7dfc66c75173b88967972950`

## Market decision

The commercial thesis is a **cross-jurisdiction B2B/Agent permit-requirements intelligence layer**, not a homeowner-only wizard. Primary targets are contractor, property-management, construction/design, permitting and real-estate software workflows.

The working commercial hypothesis remains roughly **$0.20-$0.50 per address-aware evidence-linked preflight** or an equivalent volume plan, subject to external willingness-to-pay validation. See `docs/MARKET_VALIDATION.md` for the call-volume model and demand gates.

## Known unresolved items

1. **Laval/Longueuil property adapters:** rule coverage exists; stable no-cost address/zoning/overlay resolution still needs evaluation.
2. **Gatineau PIIA/heritage:** public mapping confirms the concepts/layers but a stable unauthenticated machine endpoint is not yet locked. Unknown must never become false.
3. **Longueuil exemptions:** current simplified material describes permit workflows more clearly than universal exemptions, so Phase 1B intentionally returns conservative outcomes for several families.
4. **Mainnet:** intentionally disabled until external demand and willingness-to-pay validation pass.
5. **External Bazaar stale row:** historical `http://` discovery row remains alongside canonical HTTPS; non-blocking.

## Next gates

1. Finish free public six-city verification after the latest Railway deployments.
2. Evaluate Laval and Longueuil first-party address/GIS endpoints without making rule coverage depend on paid data.
3. Add Vancouver as the next large-market rule jurisdiction.
4. Seek at least 3 external Agent/platform developers, 100 non-owner external calls, one repeated integration with 20+ calls, and one buyer conversation accepting the commercial price range.
5. Do not expand mechanically to 20+ municipalities until there is 1,000 external calls/month, a credible platform path to 10k+ calls/month, or a paying design partner requesting jurisdictions.
