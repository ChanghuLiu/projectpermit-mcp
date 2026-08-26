# ProjectPermit / BuildRequirements — Phase 0

ProjectPermit is an evidence-linked municipal permit preflight engine for construction and renovation projects. **BuildRequirements** is the deterministic rules engine inside it.

Phase 0 supports:

- `gatineau_qc`
- `ottawa_on`
- 8 project families
- address resolution using municipal GIS/geocoders
- rule-version and overlay-aware results
- official-source evidence on every rule result
- a FastAPI endpoint and MCP v2 servers
- x402 pay-per-call at the transport/tool boundary

The engine deliberately does **not** call an LLM. A calling agent normalizes natural-language scope into structured facts; BuildRequirements applies deterministic municipal rules.

## Live Phase 0 endpoints

- HTTP API: `https://projectpermit-api-v2-production.up.railway.app`
- Paid MCP: `https://projectpermit-x402-mcp-production.up.railway.app/mcp`

The paid MCP exposes a free `projectpermit_info` tool and the paid `check_project_requirements` tool. The current test price is **$0.01 USDC** on Base Sepolia (`eip155:84532`).

The result is a preflight information package, **not municipal authorization, legal advice, engineering certification, or building-code design approval**.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn projectpermit.api:app --host 127.0.0.1 --port 8000
```

For standard MCP support:

```bash
pip install -e '.[mcp]'
projectpermit-mcp
```

`projectpermit-mcp` uses MCP Python SDK v2 Streamable HTTP, JSON responses, and stateless HTTP. It listens on `127.0.0.1:8001` by default. Override with `PROJECTPERMIT_MCP_HOST` and `PROJECTPERMIT_MCP_PORT`.

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## API

`POST /v1/check-project-requirements`

Example:

```json
{
  "jurisdiction": "ottawa_on",
  "address": "110 Laurier Ave W, Ottawa, ON",
  "resolve_address": false,
  "project": {
    "family": "window_door",
    "action": "enlarge_existing_window",
    "structural_change": true
  }
}
```

## Repository map

- `src/projectpermit/engine.py` — deterministic rule engine
- `src/projectpermit/address.py` — municipal address/GIS adapters
- `src/projectpermit/api.py` — HTTP API
- `src/projectpermit/mcp_server.py` — standard MCP v2 server
- `src/projectpermit/paid_mcp_server.py` — x402-native paid MCP v2 server
- `src/projectpermit/mcp_v2_x402_compat.py` — MCP SDK v2 / x402 result compatibility shim
- `data/golden_cases.json` — deterministic regression corpus
- `data/source_manifest.json` — official source registry/freshness metadata
- `schemas/` — public request/response schemas
- `scripts/paid_mcp_unpaid_smoke.py` — no-cost remote payment-challenge test
- `scripts/paid_mcp_buyer_smoke.py` — real buyer-side testnet paid MCP call
- `scripts/facilitator_capability_probe.py` — no-cost facilitator capability matrix
- `scripts/projectpermit_bazaar_lookup.py` — read-only Bazaar catalog lookup
- `docs/PHASE0_SPEC.md` — product and engineering scope
- `docs/X402_ARCHITECTURE.md` — payment/discovery design

## x402 profiles

### HTTP payment smoke

The public-values-only profile at `config/x402.base-sepolia.env.example` targets Base Sepolia and can use the x402.org public testnet facilitator for HTTP payment testing.

The protected HTTP resource is `POST /v1/check-project-requirements`; `/health` remains free.

### Paid MCP / Bazaar canary

The public paid MCP currently uses a Bazaar-capable facilitator canary:

`https://facilitator.goplausible.xyz`

The tool challenge declares the x402 Bazaar MCP discovery extension, including its tool name, transport, input schema, example, service name, and tags. A successful Bazaar-capable settlement is expected to make the tool queryable through the facilitator's discovery catalog.

## Real paid MCP smoke test

Run this only on your own machine. Keep the payer private key local; never paste or commit it. Do not repeat the paid smoke test unless a regression specifically requires another settlement.

```bash
python -m venv .venv-buyer
source .venv-buyer/bin/activate
pip install -e '.[buyer]'

read -s EVM_PRIVATE_KEY
export EVM_PRIVATE_KEY
echo

python scripts/paid_mcp_buyer_smoke.py
```

The payer wallet needs Base Sepolia test USDC. A successful run should show:

- `payment_made=True`
- `is_error=False`
- `settlement_success=True`
- `settlement_network=eip155:84532`
- `settlement_transaction=0x...`
- `paid_mcp_buyer_smoke=PASS`

The server never needs the payer private key.

## CI / verification

Current CI covers:

- Python 3.11 + 3.13
- deterministic rule and schema tests
- MCP v2 integration
- x402 wire behavior
- MCP v2 settlement-receipt compatibility
- Docker build + live `/health`
- public MCP tool invocation
- public paid-MCP payment challenge
- facilitator capability checks
- read-only Bazaar catalog state

A real buyer-side paid MCP call has already completed successfully through the public service, with server-side `/verify` and `/settle` confirmation. The remaining Phase 0 discovery gate is one settlement through the current Bazaar-capable facilitator followed by a catalog lookup.

See `STATUS.md` and `docs/PHASE0_RELEASE_READINESS.md` for the current gate status.

## Phase 0 safety boundary

Determinations intentionally use preflight language such as `LIKELY_REQUIRED`, `LIKELY_NOT_REQUIRED`, `ADDITIONAL_REVIEW_REQUIRED`, and `MUNICIPAL_CONFIRMATION_REQUIRED` where uncertainty exists. The engine should not be presented as a municipality, permit issuer, lawyer, architect, or engineer.
