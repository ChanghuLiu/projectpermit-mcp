# ProjectPermit / BuildRequirements — Phase 0

ProjectPermit is an evidence-linked municipal permit preflight engine for construction and renovation projects. **BuildRequirements** is the deterministic rules engine inside it.

Phase 0 supports:

- `gatineau_qc`
- `ottawa_on`
- 8 project families
- address resolution using municipal GIS/geocoders
- rule-version and overlay-aware results
- official-source evidence on every rule result
- a FastAPI endpoint and a standard MCP tool
- x402-ready separation between the paid transport layer and the rules engine

The engine deliberately does **not** call an LLM. A calling agent normalizes natural-language scope into structured facts; BuildRequirements applies deterministic municipal rules.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn projectpermit.api:app --host 127.0.0.1 --port 8000
```

For MCP support:

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

The result is a preflight information package, **not municipal authorization, legal advice, engineering certification, or building-code design approval**.

## Repository map

- `src/projectpermit/engine.py` — deterministic rule engine
- `src/projectpermit/address.py` — municipal address/GIS adapters
- `src/projectpermit/api.py` — HTTP API
- `src/projectpermit/mcp_server.py` — standard MCP server
- `data/golden_cases.json` — deterministic regression corpus
- `data/source_manifest.json` — official source registry/freshness metadata
- `schemas/` — public request/response schemas
- `docs/PHASE0_SPEC.md` — product and engineering scope
- `docs/X402_ARCHITECTURE.md` — payment/discovery design

## Base Sepolia x402 smoke profile

A public-values-only testnet profile is provided at `config/x402.base-sepolia.env.example`.
It targets Base Sepolia (`eip155:84532`) and the x402.org testnet facilitator.
The receiving address is public; **never put a private key or seed phrase in this repository**.

```bash
set -a
source config/x402.base-sepolia.env.example
set +a
pip install -e '.[x402]'
uvicorn projectpermit.api:app --host 0.0.0.0 --port 8000
```

The protected resource is `POST /v1/check-project-requirements`. `/health` remains free for deployment monitoring.

## Phase 0 safety boundary

Determinations intentionally use preflight language such as `LIKELY_REQUIRED`, `LIKELY_NOT_REQUIRED`, `ADDITIONAL_REVIEW_REQUIRED`, and `MUNICIPAL_CONFIRMATION_REQUIRED` where uncertainty exists. The engine should not be presented as a municipality, permit issuer, lawyer, architect, or engineer.
