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
    def test_tool_wires_to_engine(self):
        fake_module = type('FakeModule', (), {'MCPServer': FakeServer})
        with patch.dict(sys.modules, {'mcp': type('M', (), {})(), 'mcp.server': fake_module}):
            server = mcp_server.build_server()
            result = server.tools['check_project_requirements'](
                jurisdiction='ottawa_on',
                project={'family': 'window_door', 'action': 'replace_same_size'},
            )
        self.assertIn('determination', result)
        self.assertEqual(result['jurisdiction']['municipality'], 'Ottawa')


if __name__ == '__main__':
    unittest.main()
