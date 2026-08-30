import unittest

from scripts import external_directory_audit as audit


class ExternalDirectoryAuditTest(unittest.TestCase):
    def test_price_contract_normalizes_common_formats(self):
        self.assertTrue(audit._price_contract_match("0.20"))
        self.assertTrue(audit._price_contract_match("$0.20"))
        self.assertTrue(audit._price_contract_match(0.2))
        self.assertFalse(audit._price_contract_match("0.05"))
        self.assertIsNone(audit._price_contract_match("unknown"))

    def test_manifest_price_supports_projectpermit_and_directory_shapes(self):
        self.assertEqual(
            "0.20",
            audit._manifest_price({"pricing": {"currency": "USDC", "base": "0.20"}}),
        )
        self.assertEqual(
            0.2,
            audit._manifest_price({"request_price_usd": 0.2}),
        )
        self.assertEqual(
            "0.20",
            audit._manifest_price('{"request_price_usd":"0.20"}'),
        )
        self.assertIsNone(audit._manifest_price("not-json"))


if __name__ == "__main__":
    unittest.main()
