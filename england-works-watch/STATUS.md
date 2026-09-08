# England Works Watch — Status

Updated: 2026-09-08

Public description: **UK sponsor compliance/change intelligence**. The earlier Railway roadworks prototype is legacy and is not the current product direction.

## Completed V0.1 gates

- Skilled Worker + sponsor duties only
- 10 supported sponsor event types
- four-state fail-closed decision contract
- official source/effective-date evidence per decision
- 10 independent cases, 6 negative controls, 5 sponsor-event cases, 4 fail-closed cases
- 25 / 25 acceptance fixtures passing
- source registry, review state, fingerprints, 30-day review threshold and drift probe
- MCP 2.x Streamable HTTP implementation
- x402 v2 Base-USDC payment boundary implementation
- OpenAPI, llms, MCP server card, x402 discovery
- persistent privacy-minimal funnel analytics

## Production gates next

1. Railway online build/test/source audit.
2. Replace legacy roadworks deployment with this sponsor-compliance service.
3. Public health/MCP discovery smoke.
4. Enable Base-mainnet x402 with the same public seller wallet as UK Taxi.
5. Verify unpaid challenge cannot leak a business decision.
6. Execute owner-controlled paid smoke and classify it as owned validation, not external demand.
7. Publish agent discovery and enter commercial validation.
