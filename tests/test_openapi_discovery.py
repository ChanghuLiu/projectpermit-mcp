import os
import unittest

from projectpermit.openapi_discovery import (
    BATCH_PATH,
    SINGLE_PATH,
    decorate_openapi_schema,
    discovery_settings,
)


class OpenApiDiscoveryTest(unittest.TestCase):
    def _base_schema(self):
        return {
            "openapi": "3.1.0",
            "info": {"title": "ProjectPermit", "version": "0.6.0"},
            "paths": {
                SINGLE_PATH: {"post": {"responses": {"200": {"description": "OK"}}}},
                BATCH_PATH: {"post": {"responses": {"200": {"description": "OK"}}}},
                "/v1/preview-project-requirements": {
                    "post": {"responses": {"200": {"description": "OK"}}}
                },
            },
        }

    def test_paid_routes_get_fixed_x402_payment_metadata(self):
        schema = decorate_openapi_schema(
            self._base_schema(),
            single_amount="0.20",
            batch_amount="5.00",
            network="eip155:8453",
        )

        info = schema["info"]
        self.assertIn("x-guidance", info)
        self.assertEqual("eip155:8453", info["x-projectpermit"]["commercialNetwork"])

        single = schema["paths"][SINGLE_PATH]["post"]
        self.assertEqual(
            {"mode": "fixed", "currency": "USD", "amount": "0.20"},
            single["x-payment-info"]["price"],
        )
        self.assertEqual([{"x402": {}}], single["x-payment-info"]["protocols"])
        self.assertIn("402", single["responses"])
        self.assertEqual("eip155:8453", single["x-projectpermit-payment"]["network"])

        batch = schema["paths"][BATCH_PATH]["post"]
        self.assertEqual("5.00", batch["x-payment-info"]["price"]["amount"])
        self.assertIn("402", batch["responses"])

    def test_free_preview_is_not_mislabeled_as_paid(self):
        schema = decorate_openapi_schema(
            self._base_schema(),
            single_amount="0.20",
            batch_amount="5.00",
            network="eip155:8453",
        )
        preview = schema["paths"]["/v1/preview-project-requirements"]["post"]
        self.assertNotIn("x-payment-info", preview)

    def test_input_schema_is_not_mutated(self):
        base = self._base_schema()
        decorate_openapi_schema(
            base,
            single_amount="0.20",
            batch_amount="5.00",
            network="eip155:8453",
        )
        self.assertNotIn("x-guidance", base["info"])
        self.assertNotIn("x-payment-info", base["paths"][SINGLE_PATH]["post"])

    def test_missing_paid_route_fails_closed(self):
        base = self._base_schema()
        del base["paths"][BATCH_PATH]
        with self.assertRaisesRegex(ValueError, "paid path missing"):
            decorate_openapi_schema(
                base,
                single_amount="0.20",
                batch_amount="5.00",
                network="eip155:8453",
            )

    def test_environment_prices_are_normalized(self):
        keys = (
            "PROJECTPERMIT_X402_PRICE_USD",
            "PROJECTPERMIT_X402_BATCH_PRICE_USD",
            "PROJECTPERMIT_X402_NETWORK",
        )
        previous = {key: os.environ.get(key) for key in keys}
        try:
            os.environ["PROJECTPERMIT_X402_PRICE_USD"] = "$0.37"
            os.environ["PROJECTPERMIT_X402_BATCH_PRICE_USD"] = "$7.25"
            os.environ["PROJECTPERMIT_X402_NETWORK"] = "eip155:8453"
            settings = discovery_settings()
            self.assertEqual("0.37", settings["single_amount"])
            self.assertEqual("7.25", settings["batch_amount"])
            self.assertEqual("eip155:8453", settings["network"])
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_launch_defaults_keep_full_batch_cheaper_than_50_singles(self):
        keys = (
            "PROJECTPERMIT_X402_PRICE_USD",
            "PROJECTPERMIT_X402_BATCH_PRICE_USD",
            "PROJECTPERMIT_X402_NETWORK",
        )
        previous = {key: os.environ.pop(key, None) for key in keys}
        try:
            settings = discovery_settings()
            self.assertEqual("0.05", settings["single_amount"])
            self.assertEqual("2.00", settings["batch_amount"])
            self.assertLess(float(settings["batch_amount"]), 50 * float(settings["single_amount"]))
        finally:
            for key, value in previous.items():
                if value is not None:
                    os.environ[key] = value

    def test_actual_fastapi_openapi_exposes_paid_contract(self):
        from projectpermit.api import app

        app.openapi_schema = None
        schema = app.openapi()
        self.assertTrue(schema["info"].get("x-guidance"))
        for path in (SINGLE_PATH, BATCH_PATH):
            operation = schema["paths"][path]["post"]
            self.assertIn("x-payment-info", operation)
            self.assertIn("402", operation["responses"])
        preview = schema["paths"]["/v1/preview-project-requirements"]["post"]
        self.assertNotIn("x-payment-info", preview)


if __name__ == "__main__":
    unittest.main()
