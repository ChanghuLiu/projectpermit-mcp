"""Fail-safe handling for property overlays that can invalidate permit exemptions.

Municipal rules sometimes allow a no-permit path only when parcel-specific overlays
(such as heritage status or a PIIA) do not apply.  Missing/unknown property facts must
never be interpreted as an explicit ``False`` in those branches.

This module is deliberately a post-evaluation guard.  Jurisdiction rules remain the
source of the underlying permit logic; the guard only prevents an exemption from
being returned as ``LIKELY_NOT_REQUIRED`` when a rule-required property fact is
unknown.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

GUARD_RULE_VERSION = "2026-08-28.1"
SOURCE_VERIFIED_AT = "2026-08-26"

GATINEAU_OVERLAY_SENSITIVE_EXEMPTIONS = {
    "GAT-COST-001",
    "GAT-DECK-001",
}

LAVAL_PIIA_SENSITIVE_EXEMPTIONS = {
    "LAV-SHED-002",
    "LAV-DECK-002",
}

EVIDENCE = {
    "gatineau_qc": [
        {
            "source_id": "GAT_GENERAL",
            "authority": "Ville de Gatineau",
            "title": "Ai-je besoin d'un permis de construire ou d'un certificat d'autorisation?",
            "url": "https://www.gatineau.ca/portail/default.aspx?c=fr-CA&p=guichet_municipal%2Fpermis_certificats_autorisation_urbanisme%2Fai_je_besoin_permis_construire_ou_certificat_autorisation",
        },
        {
            "source_id": "GAT_GIS",
            "authority": "Ville de Gatineau",
            "title": "Carte interactive (Géoportail urbanisme)",
            "url": "https://www.gatineau.ca/portail/default.aspx?p=publications_cartes_statistiques_donnees_ouvertes%2Fcartes%2Fcarte_interactive_geoportail_urbanisme",
        },
    ],
    "ottawa_on": [
        {
            "source_id": "OTT_EXEMPT",
            "authority": "City of Ottawa",
            "title": "Projects not requiring Building Permits",
            "url": "https://ottawa.ca/en/planning-development-and-construction/building-and-renovating/do-i-need-building-permit/projects-not-requiring-building-permits",
        }
    ],
    "laval_qc": [
        {
            "source_id": "LAV_SHED",
            "authority": "Ville de Laval",
            "title": "Remise (cabanon)",
            "url": "https://www.laval.ca/reglements-permis/trouver-mon-permis/remise/",
        },
        {
            "source_id": "LAV_BALCON",
            "authority": "Ville de Laval",
            "title": "Balcon et galerie",
            "url": "https://www.laval.ca/reglements-permis/trouver-mon-permis/balcon-galerie/",
        },
    ],
}


def _rule_ids(result: dict[str, Any]) -> set[str]:
    return {
        str(requirement.get("rule_id"))
        for requirement in result.get("requirements", [])
        if requirement.get("rule_id")
    }


def _required_unknown_facts(facts: dict[str, Any], result: dict[str, Any]) -> list[str]:
    """Return property facts that must be resolved before trusting an exemption."""
    if result.get("determination") != "LIKELY_NOT_REQUIRED":
        return []

    jurisdiction = facts.get("jurisdiction")
    prop = facts.get("property") or {}
    rules = _rule_ids(result)

    if jurisdiction == "gatineau_qc" and rules & GATINEAU_OVERLAY_SENSITIVE_EXEMPTIONS:
        return [
            key
            for key in ("piia", "heritage")
            if prop.get(key) is None
        ]

    # Ottawa's rule engine applies its heritage override generically to normal
    # permit exemptions when heritage=True.  Unknown heritage therefore cannot
    # safely be treated like heritage=False.
    if jurisdiction == "ottawa_on":
        return ["heritage"] if prop.get("heritage") is None else []

    if jurisdiction == "laval_qc" and rules & LAVAL_PIIA_SENSITIVE_EXEMPTIONS:
        return ["piia"] if prop.get("piia") is None else []

    return []


def apply_unknown_overlay_safety(
    facts: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    """Upgrade an unsafe exemption to municipal confirmation when overlays are unknown.

    Explicit caller/adapter values of ``False`` remain valid resolved facts.  ``None``
    or an absent key means unknown.  Required/likely-required outcomes are never
    downgraded or otherwise changed by this guard.
    """
    missing = _required_unknown_facts(facts, result)
    if not missing:
        return result

    out = deepcopy(result)
    jurisdiction = str(facts.get("jurisdiction") or "")

    if jurisdiction == "gatineau_qc":
        reason = (
            "This no-permit path depends on the property not being subject to a PIIA "
            "or heritage constraint. Resolve the listed property facts before relying "
            "on the exemption."
        )
        rule_id = "GAT-OVERLAY-UNKNOWN-001"
    elif jurisdiction == "ottawa_on":
        reason = (
            "Ottawa's normal permit exemptions can change for designated heritage "
            "buildings / Heritage District Overlay properties. Resolve heritage status "
            "before relying on the exemption."
        )
        rule_id = "OTT-HER-UNKNOWN-001"
    elif jurisdiction == "laval_qc":
        reason = (
            "This Laval no-permit path can change when a PIIA applies. Resolve PIIA "
            "status before relying on the exemption."
        )
        rule_id = "LAV-PIIA-UNKNOWN-001"
    else:  # defensive; _required_unknown_facts currently cannot reach this branch
        reason = "Resolve parcel-specific property context before relying on this exemption."
        rule_id = "PROPERTY-OVERLAY-UNKNOWN-001"

    out.setdefault("requirements", []).append(
        {
            "type": "property_overlay_review",
            "status": "MUNICIPAL_CONFIRMATION_REQUIRED",
            "reason": reason,
            "rule_id": rule_id,
            "rule_version": GUARD_RULE_VERSION,
            "source_verified_at": SOURCE_VERIFIED_AT,
            "evidence": deepcopy(EVIDENCE.get(jurisdiction, [])),
        }
    )
    out["determination"] = "MUNICIPAL_CONFIRMATION_REQUIRED"
    out["confidence"] = "MEDIUM"
    out["property_context_status"] = "UNRESOLVED_FOR_EXEMPTION"
    existing_required = set(out.get("required_property_facts") or [])
    out["required_property_facts"] = sorted(existing_required | set(missing))
    return out
