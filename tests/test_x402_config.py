import os
import unittest
from unittest.mock import patch

from projectpermit.x402_config import load_x402_settings, validate_x402_settings


class X402ConfigTest(unittest.TestCase):
    def test_disabled_needs_no_secrets(self):
        with patch.dict(os.environ, {}, clear=True):
            s = load_x402_settings()
            self.assertFalse(s['enabled'])
            validate_x402_settings(s)

    def test_enabled_requires_complete_caip2_config(self):
        env = {
            'PROJECTPERMIT_X402_ENABLED': 'true',
            'PROJECTPERMIT_X402_PRICE_USD': '$0.10',
            'PROJECTPERMIT_X402_NETWORK': 'eip155:84532',
            'PROJECTPERMIT_X402_PAY_TO': '0x0000000000000000000000000000000000000001',
            'PROJECTPERMIT_X402_FACILITATOR_URL': 'https://x402.org/facilitator',
        }
        with patch.dict(os.environ, env, clear=True):
            s = load_x402_settings()
            self.assertTrue(s['enabled'])
            self.assertEqual('$0.10', s['batch_price'])
            validate_x402_settings(s)

    def test_batch_price_can_be_overridden_independently(self):
        env = {
            'PROJECTPERMIT_X402_ENABLED': 'true',
            'PROJECTPERMIT_X402_PRICE_USD': '$0.10',
            'PROJECTPERMIT_X402_BATCH_PRICE_USD': '$0.50',
            'PROJECTPERMIT_X402_NETWORK': 'eip155:84532',
            'PROJECTPERMIT_X402_PAY_TO': '0x0000000000000000000000000000000000000001',
            'PROJECTPERMIT_X402_FACILITATOR_URL': 'https://x402.org/facilitator',
        }
        with patch.dict(os.environ, env, clear=True):
            s = load_x402_settings()
            self.assertEqual('$0.10', s['price'])
            self.assertEqual('$0.50', s['batch_price'])
            validate_x402_settings(s)

    def test_enabled_rejects_invalid_batch_price(self):
        env = {
            'PROJECTPERMIT_X402_ENABLED': 'true',
            'PROJECTPERMIT_X402_PRICE_USD': '$0.10',
            'PROJECTPERMIT_X402_BATCH_PRICE_USD': '0.50',
            'PROJECTPERMIT_X402_NETWORK': 'eip155:84532',
            'PROJECTPERMIT_X402_PAY_TO': '0x0000000000000000000000000000000000000001',
            'PROJECTPERMIT_X402_FACILITATOR_URL': 'https://x402.org/facilitator',
        }
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'BATCH_PRICE'):
                validate_x402_settings(load_x402_settings())

    def test_enabled_rejects_legacy_network_name(self):
        env = {
            'PROJECTPERMIT_X402_ENABLED': 'true',
            'PROJECTPERMIT_X402_PRICE_USD': '$0.10',
            'PROJECTPERMIT_X402_NETWORK': 'base-sepolia',
            'PROJECTPERMIT_X402_PAY_TO': '0x1',
            'PROJECTPERMIT_X402_FACILITATOR_URL': 'https://x402.org/facilitator',
        }
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(RuntimeError):
                validate_x402_settings(load_x402_settings())


if __name__ == '__main__':
    unittest.main()
