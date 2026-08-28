import json
import unittest
from pathlib import Path

from projectpermit.jurisdiction_router import SUPPORTED_JURISDICTIONS


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "mcp" / "tool_contract.json"


class StaticMcpContractTest(unittest.TestCase):
    def test_static_contract_matches_live_jurisdiction_router(self):
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))

        self.assertEqual("check_project_requirements", payload["name"])
        self.assertNotIn("phase0_supported_jurisdictions", payload)
        self.assertEqual(
            list(SUPPORTED_JURISDICTIONS),
            payload["supported_jurisdictions"],
        )

    def test_static_contract_keeps_public_schema_refs(self):
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual("../schemas/request.schema.json", payload["inputSchema"]["$ref"])
        self.assertEqual("../schemas/response.schema.json", payload["outputSchema"]["$ref"])


if __name__ == "__main__":
    unittest.main()
