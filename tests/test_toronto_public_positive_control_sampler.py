import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "market_research"
    / "toronto_public_positive_control_sampler.py"
)
SPEC = importlib.util.spec_from_file_location(
    "toronto_public_positive_control_sampler", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
sampler = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sampler
SPEC.loader.exec_module(sampler)


class TorontoPublicPositiveControlSamplerTest(unittest.TestCase):
    def test_only_building_permit_numbers_qualify(self):
        self.assertTrue(sampler._is_building_permit_number("26 123456 BLD"))
        self.assertTrue(sampler._is_building_permit_number("26 123456 bld"))
        self.assertFalse(sampler._is_building_permit_number("26 123456 HVA"))
        self.assertFalse(sampler._is_building_permit_number("26 123456 PLB"))
        self.assertFalse(sampler._is_building_permit_number("26 123456 DRN"))

    def test_low_rise_gate_rejects_non_target_structures_and_uses(self):
        self.assertTrue(
            sampler._low_rise_residential_basis(
                "SFD - Semi-Detached", "Sfd Semi Detached", "Sfd Semi Detached"
            )
        )
        self.assertTrue(
            sampler._low_rise_residential_basis(
                "Laneway / Rear Yard Suite", "Rear Yard Of Sfd", "Garden Suite"
            )
        )

        self.assertEqual(
            [],
            sampler._low_rise_residential_basis(
                "Apartment Building", "Vacant", "Residential Condominium"
            ),
        )
        self.assertEqual(
            [],
            sampler._low_rise_residential_basis(
                "Group Home", "Rooming House", "Group Home"
            ),
        )
        self.assertEqual(
            [],
            sampler._low_rise_residential_basis(
                "Multiple Use/Non Residential", "Automotive Shop", "Mixed Use"
            ),
        )
        self.assertEqual(
            [],
            sampler._low_rise_residential_basis(
                "SFD - Detached", "Warehouse", "Warehouse"
            ),
        )

    def test_address_redaction_preserves_unrelated_numeric_scope_facts(self):
        text = (
            "Construct 125 dwelling units. Related address 12 King Street. "
            "Area 12.5 sqm. Contact test@example.com or 416-555-1234."
        )
        sanitized = sampler._sanitize_scope_text(
            text,
            street_num="12",
            street_name="King",
            postal="M5V 2T6",
        )

        self.assertIn("125 dwelling units", sanitized)
        self.assertIn("12.5 sqm", sanitized)
        self.assertNotIn("12 King", sanitized)
        self.assertIn("[redacted-address]", sanitized)
        self.assertIn("[redacted-email]", sanitized)
        self.assertIn("[redacted-phone]", sanitized)

    def test_family_token_mapping_is_explicit_and_multi_family(self):
        matches = sampler._family_matches(
            "Multiple Projects",
            "Rear addition with interior alterations and basement underpinning",
        )
        self.assertIn("addition", matches)
        self.assertIn("interior_renovation", matches)
        self.assertIn("basement", matches)

    def test_revision_sort_key_prefers_numeric_revision(self):
        self.assertGreater(
            sampler._revision_sort_key("10"), sampler._revision_sort_key("2")
        )
        self.assertGreater(
            sampler._revision_sort_key("01"), sampler._revision_sort_key("")
        )


if __name__ == "__main__":
    unittest.main()
