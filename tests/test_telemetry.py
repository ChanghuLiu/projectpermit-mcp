import io
import json
import unittest
from contextlib import redirect_stdout

from projectpermit.telemetry import emit_preflight_event


class TelemetryTest(unittest.TestCase):
    def test_event_omits_address_and_hashes_client_tag(self):
        facts = {
            "jurisdiction": "vancouver_bc",
            "address": "453 W 12TH AVE, Vancouver, BC",
            "resolve_address": True,
            "project": {"family": "interior_renovation", "action": "painting"},
            "context": {
                "_transport": "standard_mcp",
                "client_tag": "projectpermit-ci",
            },
        }
        result = {
            "determination": "LIKELY_NOT_REQUIRED",
            "confidence": "HIGH",
            "requirements": [{"type": "building_permit"}],
            "address_context": {
                "address_resolution": {
                    "matched_address": "453 W 12TH AV",
                    "longitude": -123.114,
                    "latitude": 49.260,
                }
            },
        }

        output = io.StringIO()
        with redirect_stdout(output):
            emit_preflight_event(facts, result)

        rendered = output.getvalue().strip()
        self.assertTrue(rendered.startswith("PROJECTPERMIT_USAGE "))
        payload = json.loads(rendered.split(" ", 1)[1])

        self.assertEqual("standard_mcp", payload["transport"])
        self.assertEqual("vancouver_bc", payload["jurisdiction"])
        self.assertEqual("interior_renovation", payload["project_family"])
        self.assertTrue(payload["resolve_address"])
        self.assertTrue(payload["internal_traffic"])
        self.assertIsNotNone(payload["client_tag_hash"])

        # Privacy contract: raw identifying location/integration values never appear.
        self.assertNotIn("453 W 12TH", rendered)
        self.assertNotIn("-123.114", rendered)
        self.assertNotIn("49.26", rendered)
        self.assertNotIn("projectpermit-ci", rendered)


if __name__ == "__main__":
    unittest.main()
