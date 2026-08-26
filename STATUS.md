# ProjectPermit Status

Updated: 2026-08-26

## Current state

**Phase 0 testnet discovery / market-validation release readiness: PASS.**

**Phase 1A cross-jurisdiction expansion: IN PROGRESS — Toronto + Mississauga deterministic rule coverage is implemented and under public deployment verification.**

ProjectPermit is an evidence-linked deterministic municipal permit preflight engine. The calling Agent normalizes project scope; the server applies municipal rules and returns official-source evidence. The rules engine does not call an LLM and payment remains outside BuildRequirements.

## Jurisdiction coverage

- `gatineau_qc` — Phase 0 rules + address/GIS adapter
- `ottawa_on` — Phase 0 rules + address/GIS adapter
- `toronto_on` — Phase 1A deterministic rules; address adapter pending
- `mississauga_on` — Phase 1A deterministic rules; address adapter pending

All four jurisdictions are routed through the same public HTTP/MCP rule interface. Toronto and Mississauga should be called with `resolve_address=false` until their property/GIS adapters are locked.

## Phase 0 completed

- Product boundary and conservative determination vocabulary locked
- Gatineau + Ottawa Phase 0 rules implemented
- 8 normalized project families
- deterministic rules engine with official evidence and stable rule ids
- rule-version and property-overlay-aware results
- Ottawa official geocoder/GIS adapter
- Gatineau official municipal geocoder adapter
- FastAPI endpoint deployed publicly
- MCP Python SDK v2 Streamable HTTP server deployed publicly
- x402-native paid MCP tool deployed publicly
- official source manifest and source-change detector
- public request/response JSON schemas
- x402 v2 HTTP transport adapter
- Base Sepolia `eip155:84532` payment profile
- public payee configured without storing payer keys server-side
- no server-side LLM dependency
- no paid map/property-data dependency
- Docker + GitHub Actions CI
- MCP SDK v2 / x402 settlement-metadata compatibility bridge and regression test
- facilitator capability probe and Bazaar catalog lookup scripts
- GoPlausible Bazaar indexing proven end to end
- canonical HTTPS Bazaar resource URL proven after settlement

## Phase 1A implemented so far

- Toronto official required/not-required guidance converted to conservative deterministic rules
- Mississauga official required/not-required guidance converted to conservative deterministic rules
- explicit handling of ambiguous official thresholds instead of guessing
- four-jurisdiction dispatcher exported as the package's public evaluator
- HTTP, free MCP, paid MCP, and x402 discovery schemas advertise all four jurisdictions
- public request schema expanded with Toronto/Mississauga rule facts
- source manifest tracks Toronto/Mississauga critical official guidance
- regression tests added for window/door, basement, deck and accessory-structure cases
- `docs/MARKET_VALIDATION.md` added with call-volume model, pricing thesis, buyer priorities and expansion gates

## Live services

- Paid HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Free MCP: Railway service `projectpermit-mcp`
- Paid x402 MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

Paid MCP exposes:

- `projectpermit_info` — free discovery/status
- `check_project_requirements` — x402-paid permit preflight

Current **testnet discovery price**: **$0.01 USDC per paid tool/API call** on Base Sepolia. This is not the intended commercial price.

## Verification

CI verifies:

- Python 3.11 and 3.13 core tests
- deterministic rule/schema/source contracts
- Toronto/Mississauga regression cases
- MCP v2 integration
- x402 wire behavior
- MCP v2 settlement-receipt metadata compatibility
- Docker build and live container `/health`
- public free MCP connection/tool invocation
- public paid MCP unpaid challenge
- public HTTP Bazaar unpaid challenge
- facilitator capability matrix
- read-only Bazaar catalog state, including canonical HTTPS listing

Real buyer-side x402 calls have completed successfully through the public Railway services. No additional paid calls are needed for ordinary smoke testing.

Final canonical-HTTPS HTTP settlement transaction:

`0x2070aa9a55287162876d2d53a1f1ebe865ba912d7dfc66c75173b88967972950`

## Bazaar result

For Bazaar discovery, ProjectPermit uses:

`https://facilitator.goplausible.xyz`

The canonical resource is:

`https://projectpermit-api-v2-production.up.railway.app/v1/check-project-requirements`

The final Phase 0 catalog verification reported `FOUND_CANONICAL_HTTPS`. A stale pre-fix `http://` historical row remains in the external catalog but is not the canonical resource.

## Market decision

Two-city Gatineau/Ottawa coverage is a proving ground, not a sufficient standalone call market. The commercial thesis is now a **cross-jurisdiction B2B/Agent permit-requirements intelligence layer**, with contractor/property/construction software as primary distribution rather than direct homeowner acquisition.

The current working commercial hypothesis is roughly **$0.20-$0.50 per address-aware evidence-linked preflight** or an equivalent volume plan, subject to external willingness-to-pay validation. See `docs/MARKET_VALIDATION.md` for assumptions and scenario math.

## Known unresolved items

1. **Toronto/Mississauga property context:** deterministic rules are implemented, but official address/zoning/heritage adapters are not yet locked.
2. **Gatineau PIIA/heritage:** public municipal mapping confirms the concept/layers, but a stable unauthenticated machine endpoint has not yet been locked. Unknown overlay state must never be mapped to `false`.
3. **Mainnet:** intentionally disabled until external demand and willingness-to-pay validation pass.
4. **External Bazaar stale row:** historical `http://` discovery row remains alongside canonical HTTPS; non-blocking.

## Next phase gates

1. Finish public verification of Toronto + Mississauga rules.
2. Add Toronto and Mississauga official address/property adapters where reliable no-cost machine endpoints exist.
3. Add Laval, Longueuil and Vancouver to reach a visibly cross-jurisdiction validation footprint.
4. Seek at least 3 external Agent/platform developers, 100 non-owner external calls, one repeated integration with 20+ calls, and one buyer conversation accepting the commercial price range.
5. Do not expand to 20+ municipalities until there is 1,000 external calls/month, a credible platform path to 10k+ calls/month, or a paying design partner requesting jurisdictions.

No additional paid calls should be made merely for smoke testing unless a regression specifically requires them.
