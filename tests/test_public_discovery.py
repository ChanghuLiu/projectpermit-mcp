from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from projectpermit.public_discovery import FREE_MCP_URL, landing_html, llms_text


class PublicDiscoveryTests(unittest.TestCase):
    def test_landing_targets_problem_intent_and_launch_price(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            html = landing_html()
        self.assertIn("Building permit requirements API &amp; MCP", html)
        self.assertIn("contractors and AI agents", html)
        self.assertIn("Toronto building permit", html)
        self.assertIn("Ottawa renovation permit", html)
        self.assertIn("Vancouver building permit", html)
        self.assertIn("$0.20 USDC / call", html)
        self.assertIn(FREE_MCP_URL, html)
        self.assertIn("/openapi.json", html)
        self.assertIn("/v1/preview-project-requirements", html)

    def test_llms_text_is_agent_readable_and_price_aware(self) -> None:
        with patch.dict(os.environ, {"PROJECTPERMIT_X402_PRICE_USD": "$0.07"}, clear=True):
            text = llms_text()
        self.assertIn("Building permit requirements API & MCP", text)
        self.assertIn("Launch price: $0.07 USDC per full preflight", text)
        self.assertIn("Base mainnet (eip155:8453)", text)
        self.assertIn("io.github.ChanghuLiu/projectpermit", text)
        self.assertIn("building permit API", text)
        self.assertIn("permit requirements MCP", text)


if __name__ == "__main__":
    unittest.main()
