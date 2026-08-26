# ProjectPermit Phase 0 Specification

## Objective

Given a normalized construction/renovation scope and municipality, return a structured preflight package describing permits/reviews likely required and the official evidence supporting the determination.

ProjectPermit is evidence-first and intentionally conservative. It does not replace a municipality, lawyer, architect, engineer, building official, or permit approval.

## Supported jurisdictions

1. Gatineau, Quebec (`gatineau_qc`)
2. Ottawa, Ontario (`ottawa_on`)

## Supported project families

1. `window_door`
2. `interior_renovation`
3. `basement`
4. `dwelling_change`
5. `deck_porch`
6. `accessory_structure`
7. `addition`
8. `kitchen_bath_plumbing`

## Determination vocabulary

- `REQUIRED`
- `LIKELY_REQUIRED`
- `LIKELY_NOT_REQUIRED`
- `ADDITIONAL_REVIEW_REQUIRED`
- `MUNICIPAL_CONFIRMATION_REQUIRED`
- `OUT_OF_SCOPE`

An exemption is never presented as municipal authorization. Address overlays can upgrade an otherwise exempt result to additional review.

## Architecture

```text
natural language scope
        |
        v
caller / agent normalization
        |
        v
structured project facts
        |
        +-------> municipal address/GIS adapter
        |                   |
        |                   v
        |           zoning / heritage / PIIA / flood / appeal flags
        |                   |
        v                   v
         BuildRequirements deterministic rule engine
                         |
                         v
      requirements + rule ids + official evidence + confidence
                         |
                  +------+------+
                  |             |
                HTTP           MCP
                  |
               x402 wrapper
```

## Core rule model

Every production rule must be representable by jurisdiction, version/effective window, project-family predicate, structured conditions, address/property overlays, exceptions/priority, output requirement/status/reason, and official evidence.

Phase 0 keeps selected rules in Python for rapid validation while preserving stable `rule_id` identifiers so they can later migrate to data-driven evaluation without changing the public contract.

## Gatineau conservative boundaries

The engine covers common residential triggers including additions/floor-area increases, structure/foundation/interior-wall work, opening changes, selected fire/exterior/roof triggers, dwelling-unit changes, the public C$26,000 renovation threshold, accessory structures, common exterior structures, and PIIA/heritage override logic.

The exact C$26,000 equality case is intentionally routed to municipal confirmation because the public summary expresses the exemption as below the threshold and the required category as above it. Gatineau PIIA/heritage overlay values remain unknown until stable public machine endpoints are locked; unknown is never silently converted to false.

## Ottawa conservative boundaries

The engine covers additions, structural alterations, opening changes, additional dwelling units, plumbing alterations and fixture replacement exception, same-size window/door replacement, cosmetic work, basement preflight, deck thresholds, the 2025 accessory-structure advisory, heritage override, and the 2026 zoning transition.

For applications deemed complete on or after 2026-03-11, Phase 0 can flag dual zoning review under the legacy and 2026 zoning frameworks where the transition/appeal situation requires it.

## Phase 0 exit gate

- [x] 2 municipalities
- [x] 8 project families represented
- [x] deterministic engine
- [x] no server-side LLM
- [x] no paid map/property-data dependency
- [x] official evidence identifiers and source-watch manifest
- [x] Ottawa address/GIS prototype
- [x] Gatineau municipal geocoder prototype
- [x] standard HTTP API
- [x] MCP v2 tool implementation
- [x] x402 Base Sepolia configuration path
- [x] Docker and CI
- [ ] stable Gatineau PIIA/heritage machine-layer resolution
- [ ] live end-to-end municipal GIS smoke from public deployment
- [ ] live Base Sepolia x402 settlement
