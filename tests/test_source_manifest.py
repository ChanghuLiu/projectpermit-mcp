import json
import unittest
from pathlib import Path

from projectpermit.engine import SOURCES

ROOT = Path(__file__).resolve().parents[1]


class SourceManifestTest(unittest.TestCase):
    def test_every_engine_source_is_watched(self):
        manifest = json.loads((ROOT / "data" / "source_manifest.json").read_text())
        ids = {s["source_id"] for s in manifest["sources"]}
        self.assertFalse(set(SOURCES) - ids, f"engine sources missing from watch manifest: {set(SOURCES)-ids}")


if __name__ == "__main__":
    unittest.main()
