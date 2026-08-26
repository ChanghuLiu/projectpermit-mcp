from projectpermit.jurisdiction_router import evaluate_project


def _check(jurisdiction: str, project: dict):
    return evaluate_project({
        "jurisdiction": jurisdiction,
        "project": project,
        "property": {},
        "context": {},
    })


def test_toronto_same_size_house_window_exempt():
    result = _check("toronto_on", {
        "family": "window_door",
        "action": "replace_same_size",
        "single_dwelling_house": True,
        "structural_change": False,
        "new_exit": False,
    })
    assert result["determination"] == "LIKELY_NOT_REQUIRED"
    assert result["requirements"][0]["rule_id"] == "TOR-WIN-002"


def test_toronto_same_size_window_non_house_requires_permit():
    result = _check("toronto_on", {
        "family": "window_door",
        "action": "replace_same_size",
        "single_dwelling_house": False,
    })
    assert result["determination"] == "REQUIRED"
    assert result["requirements"][0]["rule_id"] == "TOR-WIN-003"


def test_toronto_clean_basement_finish_exempt():
    result = _check("toronto_on", {
        "family": "basement",
        "action": "finish_basement",
        "structural_change": False,
        "material_alteration": False,
        "dwelling_unit_change": False,
        "new_plumbing": False,
    })
    assert result["determination"] == "LIKELY_NOT_REQUIRED"


def test_toronto_basement_with_new_plumbing_requires_permit():
    result = _check("toronto_on", {
        "family": "basement",
        "action": "finish_basement",
        "new_plumbing": True,
    })
    assert result["determination"] == "REQUIRED"


def test_toronto_deck_threshold():
    result = _check("toronto_on", {
        "family": "deck_porch",
        "deck_height_mm": 601,
    })
    assert result["determination"] == "REQUIRED"


def test_toronto_exact_15m2_shed_is_conservative():
    result = _check("toronto_on", {
        "family": "accessory_structure",
        "accessory_structure_kind": "shed",
        "accessory_area_m2": 15,
        "accessory_detached": True,
        "accessory_storeys": 1,
        "accessory_storage_only": True,
        "accessory_plumbing": False,
    })
    assert result["determination"] == "MUNICIPAL_CONFIRMATION_REQUIRED"


def test_mississauga_same_size_window_exempt():
    result = _check("mississauga_on", {
        "family": "window_door",
        "action": "replace_same_size",
    })
    assert result["determination"] == "LIKELY_NOT_REQUIRED"
    assert result["requirements"][0]["rule_id"] == "MIS-WIN-002"


def test_mississauga_basement_finish_requires_permit():
    result = _check("mississauga_on", {
        "family": "basement",
        "action": "finish_basement",
    })
    assert result["determination"] == "REQUIRED"
    assert result["requirements"][0]["rule_id"] == "MIS-BASE-001"


def test_mississauga_deck_published_gap_requires_confirmation():
    result = _check("mississauga_on", {
        "family": "deck_porch",
        "deck_height_mm": 605,
    })
    assert result["determination"] == "MUNICIPAL_CONFIRMATION_REQUIRED"
    assert result["requirements"][0]["rule_id"] == "MIS-DECK-610"


def test_mississauga_small_gazebo_exempt():
    result = _check("mississauga_on", {
        "family": "accessory_structure",
        "accessory_structure_kind": "gazebo",
        "accessory_area_m2": 10,
        "accessory_plumbing": False,
    })
    assert result["determination"] == "LIKELY_NOT_REQUIRED"


def test_mississauga_large_gazebo_requires_permit():
    result = _check("mississauga_on", {
        "family": "accessory_structure",
        "accessory_structure_kind": "gazebo",
        "accessory_area_m2": 10.1,
        "accessory_plumbing": False,
    })
    assert result["determination"] == "REQUIRED"


def test_unknown_jurisdiction_still_out_of_scope():
    result = _check("unknown_city", {"family": "window_door", "action": "replace_same_size"})
    assert result["determination"] == "OUT_OF_SCOPE"
