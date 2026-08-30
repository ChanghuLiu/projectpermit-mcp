"""Structured-but-extensible input models for ProjectPermit MCP discovery.

The models exist primarily to give external Agents useful JSON Schema from tools/list.
They deliberately keep ``extra='allow'`` so municipal/project facts can evolve without
breaking callers or the deterministic engine's existing dict-based contract.
"""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field


JURISDICTION_DESCRIPTION = (
    "Municipality id. Supported now: gatineau_qc, ottawa_on, toronto_on, "
    "mississauga_on, laval_qc, longueuil_qc, vancouver_bc."
)
FAMILY_DESCRIPTION = (
    "Normalized project family. Supported now: window_door, interior_renovation, "
    "basement, dwelling_change, deck_porch, accessory_structure, addition, "
    "kitchen_bath_plumbing."
)

JurisdictionId = Annotated[
    str,
    Field(description=JURISDICTION_DESCRIPTION, examples=["ottawa_on"]),
]
CivicAddress = Annotated[
    str | None,
    Field(
        description=(
            "Optional civic address. Supply it with resolve_address=true only where "
            "ProjectPermit has a municipal address/GIS resolver."
        ),
        examples=["453 W 12TH AVE, Vancouver, BC"],
    ),
]
ResolveAddress = Annotated[
    bool,
    Field(
        description=(
            "When true, enrich known property facts from first-party municipal address/GIS "
            "data before deterministic rule evaluation."
        )
    ),
]


class ProjectFacts(BaseModel):
    """Common normalized project facts; unknown future/municipal facts remain accepted."""

    model_config = ConfigDict(extra="allow")

    family: str | None = Field(default=None, description=FAMILY_DESCRIPTION, examples=["window_door"])
    action: str | None = Field(
        default=None,
        description=(
            "Normalized scope action inside the family, for example replace_same_size, "
            "enlarge_existing_opening, finish_basement, painting, or outdoor_patio."
        ),
        examples=["replace_same_size"],
    )
    estimated_cost_cad: float | None = Field(default=None, description="Estimated labour + materials cost in CAD when a municipal cost threshold matters.")
    floor_area_increase: bool | None = Field(default=None, description="True when the work increases existing floor area, including an addition.")
    structural_change: bool | None = Field(default=None, description="Whether the project changes load-bearing/structural elements.")
    structural_repair: bool | None = Field(default=None, description="Whether the scope includes structural repair.")
    material_alteration: bool | None = Field(default=None, description="Whether the scope is a material alteration where that distinction is used by municipal guidance.")
    modifies_walls: bool | None = Field(default=None, description="Whether interior/exterior walls are added, removed, resized or otherwise modified.")
    moves_interior_walls: bool | None = Field(default=None, description="Whether interior walls or partitions are moved.")
    foundation_work: bool | None = Field(default=None, description="Whether foundation work is included.")
    new_opening: bool | None = Field(default=None, description="Whether a new door/window opening is created.")
    closes_opening: bool | None = Field(default=None, description="Whether an existing door/window opening is closed.")
    new_exit: bool | None = Field(default=None, description="Whether the work creates a new required exit/egress opening.")
    fire_safety_system_change: bool | None = Field(default=None, description="Whether fire separations/protection/detection systems change.")
    dwelling_unit_change: bool | None = Field(default=None, description="Whether a dwelling unit is added, removed, legalized or the residential use changes.")
    new_bedroom: bool | None = Field(default=None, description="Whether a new bedroom is created.")
    room_dimensions_change: bool | None = Field(default=None, description="Whether room dimensions change.")
    room_count_change: bool | None = Field(default=None, description="Whether the number of rooms changes.")
    plumbing_change: bool | None = Field(default=None, description="Whether plumbing lines/systems/fixture locations are added, removed, moved or otherwise changed.")
    replace_existing_plumbing_fixture_only: bool | None = Field(default=None, description="True only when replacing an existing plumbing fixture in place without system/line changes.")
    new_plumbing: bool | None = Field(default=None, description="Whether new plumbing is installed.")
    exterior_wall_cladding_change: bool | None = Field(default=None, description="Whether exterior wall cladding changes.")
    recladding: bool | None = Field(default=None, description="Whether the project re-clads the building exterior.")
    same_cladding_material: bool | None = Field(default=None, description="For re-cladding, whether the replacement material is the same as existing.")
    roof_replacement: bool | None = Field(default=None, description="Whether roof covering/replacement work is included.")
    roof_slope_percent: float | None = Field(default=None, description="Roof slope as a percent where a municipal low-slope threshold matters.")
    same_roof_material: bool | None = Field(default=None, description="For roof replacement, whether replacement material is the same as existing.")
    single_dwelling_house: bool | None = Field(default=None, description="Whether the building is a qualifying single-dwelling detached/semi/row house where a rule depends on building form/use.")
    deck_height_mm: float | None = Field(default=None, description="Deck/platform walking-surface height above adjacent grade in millimetres.")
    deck_area_m2: float | None = Field(default=None, description="Deck/platform area in square metres.")
    deck_attached: bool | None = Field(default=None, description="Whether the deck is attached/adjacent to the principal building.")
    principal_access: bool | None = Field(default=None, description="Whether the deck/platform provides principal access to the building.")
    required_exit: bool | None = Field(default=None, description="Whether the deck/platform forms part of a required exit.")
    covered: bool | None = Field(default=None, description="Whether the deck/porch is covered.")
    outdoor_patio: bool | None = Field(default=None, description="Whether the scope is an outdoor patio for a specific low-patio exception.")
    connected_to_building: bool | None = Field(default=None, description="Whether a patio/deck element is connected to the building.")
    yard: str | None = Field(default=None, description="Yard/location such as front, side, secondary_front, street_facing or rear when the rule is location-dependent.")
    accessory_structure_kind: str | None = Field(default=None, description="Accessory structure type such as shed, gazebo, pergola, garage or similar.")
    accessory_area_m2: float | None = Field(default=None, description="Accessory-structure gross/ground area in square metres.")
    accessory_detached: bool | None = Field(default=None, description="Whether the accessory structure is detached from the principal building.")
    accessory_plumbing: bool | None = Field(default=None, description="Whether the accessory structure contains plumbing.")
    accessory_heated: bool | None = Field(default=None, description="Whether the accessory structure is heated.")
    accessory_storeys: int | None = Field(default=None, description="Number of accessory-structure storeys.")
    accessory_storage_only: bool | None = Field(default=None, description="Whether an accessory shed is storage-only.")
    accessory_personal_ancillary_use: bool | None = Field(default=None, description="Whether an accessory structure is for personal ancillary residential use only.")
    accessory_permanent: bool | None = Field(default=None, description="Whether the accessory structure is permanent rather than movable.")
    distance_to_lot_line_m: float | None = Field(default=None, description="Distance from the affected opening/work to the property/lot line in metres when relevant.")


class PropertyFacts(BaseModel):
    """Known property overlays; resolver-specific facts are preserved as extras."""

    model_config = ConfigDict(extra="allow")

    heritage: bool | None = Field(default=None, description="Known heritage designation/district/overlay status when available.")
    piia: bool | None = Field(default=None, description="Known Quebec PIIA/design-review applicability when available.")
    zoning_code: str | None = Field(default=None, description="Municipal zoning code returned/provided when known.")


class WorkflowContext(BaseModel):
    """Optional non-sensitive integration context; unknown context remains accepted."""

    model_config = ConfigDict(extra="allow")

    client_tag: str | None = Field(default=None, description="Optional stable non-sensitive integration/pilot label used only for aggregate validation telemetry.")
    source_platform: str | None = Field(default=None, description="Optional source system name used to scope deterministic idempotency, e.g. servicem8 or jobber.")
    source_object_type: str | None = Field(default=None, description="Optional source work-record type used to scope deterministic idempotency.")
    source_object_id: str | None = Field(default=None, description="Optional source work-record id; ProjectPermit returns only a one-way scope fingerprint, not the raw id.")
    idempotency_scope: str | None = Field(default=None, description="Optional caller-defined stable scope string for deterministic duplicate suppression.")
    prior_decision_identity: dict[str, Any] | None = Field(default=None, description="Prior action_bundle.identity from the same scoped work record, used for change classification and NOOP_UNCHANGED detection.")
    permit_application_complete_date: str | None = Field(default=None, description="ISO YYYY-MM-DD application-complete date when a municipal transition rule depends on filing date.", examples=["2026-03-11"])


PropertyFactsInput = Annotated[
    PropertyFacts | None,
    Field(description="Known property/overlay facts. Resolver-specific fields are also accepted."),
]
WorkflowContextInput = Annotated[
    WorkflowContext | None,
    Field(description="Optional workflow/idempotency context. Preserve unknown facts rather than guessing them."),
]


class BatchItemFacts(BaseModel):
    """One batch item. Fields stay optional so batch service can isolate malformed items."""

    model_config = ConfigDict(extra="allow")

    client_ref: str | None = Field(default=None, description="Caller correlation id copied into the per-item batch result.")
    jurisdiction: str | None = Field(default=None, description=JURISDICTION_DESCRIPTION, examples=["ottawa_on"])
    project: ProjectFacts | None = Field(default=None, description="Normalized proposed-work facts. family + action are the usual starting keys.")
    address: str | None = Field(default=None, description="Optional civic address for address-aware evaluation.")
    property: PropertyFacts | None = Field(default=None, description="Known property/overlay facts.")
    context: WorkflowContext | None = Field(default=None, description="Optional workflow/idempotency context.")
    resolve_address: bool = Field(default=False, description="Opt into first-party municipal address/GIS enrichment where supported.")


class SinglePreflightArguments(BaseModel):
    """Standalone JSON Schema source for paid MCP/Bazaar discovery."""

    model_config = ConfigDict(extra="forbid")

    jurisdiction: str = Field(description=JURISDICTION_DESCRIPTION, examples=["ottawa_on"])
    project: ProjectFacts = Field(description="Normalized proposed-work facts. Start with family + action and supply known rule-relevant facts; do not guess unknowns.")
    address: str | None = Field(default=None, description="Optional civic address for address-aware evaluation.")
    property: PropertyFacts | None = Field(default=None, description="Known property/overlay facts.")
    context: WorkflowContext | None = Field(default=None, description="Optional workflow/idempotency context.")
    resolve_address: bool = Field(default=False, description="Opt into first-party municipal address/GIS enrichment where supported.")


def model_or_mapping(value: BaseModel | dict[str, Any] | None) -> dict[str, Any]:
    """Convert MCP-validated Pydantic inputs back to the engine's existing dict contract."""
    if value is None:
        return {}
    if isinstance(value, BaseModel):
        return value.model_dump(exclude_none=True)
    return dict(value)


def batch_items_to_mappings(items: list[BatchItemFacts | dict[str, Any]]) -> list[dict[str, Any]]:
    return [model_or_mapping(item) for item in items]


def paid_mcp_input_schema() -> dict[str, Any]:
    """Return the same structured facts contract for x402/Bazaar discovery."""
    return SinglePreflightArguments.model_json_schema()
