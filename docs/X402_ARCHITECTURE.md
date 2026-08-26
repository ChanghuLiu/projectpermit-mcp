# x402 Architecture — ProjectPermit

## Decision

Keep payment enforcement outside BuildRequirements. The rules engine is pure deterministic computation; payment wraps the transport endpoint.

```text
Agent
  |
  | paid POST
  v
x402-protected /v1/check-project-requirements
  |
  v
BuildRequirements
  |
  v
structured evidence result
```

A standard MCP server exposes the same underlying operation for integration testing and non-paid/private deployments.

## Why this split

- zero payment code in municipal rules
- payment protocol upgrades cannot change permit determinations
- engine tests do not need wallets or chain access
- HTTP payment can be validated independently from MCP transport
- direct paid-MCP transport can be added later without rewriting the engine

## x402 v2 deployment values

Keep payment configuration outside source code:

```text
PROJECTPERMIT_X402_ENABLED=false
PROJECTPERMIT_X402_PRICE_USD=
PROJECTPERMIT_X402_NETWORK=
PROJECTPERMIT_X402_PAY_TO=
PROJECTPERMIT_X402_FACILITATOR_URL=
```

For the Phase 0 smoke test, `config/x402.base-sepolia.env.example` uses Base Sepolia (`eip155:84532`), a one-cent test price, the public payee address, and the x402.org testnet facilitator. No private key or seed phrase is stored by the seller service.

## Low-cash sequence

1. Run the rules/GIS stack without payment locally and in CI.
2. Deploy publicly with x402 disabled; validate municipal GIS calls.
3. Enable Base Sepolia x402 and confirm an unpaid request returns HTTP 402.
4. Complete one buyer-side test payment and validate settlement.
5. Only after product validation consider mainnet and agent discovery.

## Retry safety

Before live paid traffic, add a caller/request identifier and payment idempotency protection so a retry cannot create an accidental duplicate charge.

## Direct MCP payment later

If direct paid-MCP becomes preferable, add it as a thin transport adapter around the same `evaluate_project()` function. Municipal logic must remain payment-agnostic.
