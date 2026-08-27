import sys
import unittest
from unittest.mock import patch

from projectpermit import mcp_server


class FakeServer:
    def __init__(self, *args, **kwargs):
        self.tools = {}

    def tool(self):
        def decorate(fn):
            self.tools[fn.__name__] = fn
            return fn
        return decorate


class McpServerTest(unittest.TestCase):
    def _build_fake_server(self):
        fake_module = type('FakeModule', (), {'MCPServer': FakeServer})
        with patch.dict(sys.modules, {'mcp': type('M', (), {})(), 'mcp.server': fake_module}):
            return mcp_server.build_server()

    def test_info_exposes_shared_capabilities_and_starter_example(self):
        server = self._build_fake_server()
        info = server.tools['projectpermit_info']()
        self.assertEqual('ProjectPermit', info['service'])
        self.assertEqual(7, len(info['jurisdictions']))
        self.assertIn('vancouver_bc', info['jurisdictions'])
        self.assertEqual(8, len(info['project_families']))
        self.assertIn('kitchen_bath_plumbing', info['project_families'])
        self.assertEqual('ottawa_on', info['example']['jurisdiction'])
        self.assertEqual('window_door', info['example']['project']['family'])

    def test_tool_wires_to_engine(self):
        server = self._build_fake_server()
        result = server.tools['check_project_requirements'](
            jurisdiction='ottawa_on',
            project={'family': 'window_door', 'action': 'replace_same_size'},
        )
        self.assertIn('determination', result)
        self.assertEqual(result['jurisdiction']['municipality'], 'Ottawa')


if __name__ == '__main__':
    unittest.main()
