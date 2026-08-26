import unittest

from projectpermit.source_watch import check_sources, digest


class SourceWatchTest(unittest.TestCase):
    def test_normalized_text_hash(self):
        self.assertEqual(digest(b"hello   world", "text/html"), digest(b"hello\nworld", "text/html"))

    def test_detects_change(self):
        manifest = {"sources": [{"source_id": "A", "url": "https://example.test/a", "criticality": "critical"}]}
        old = {"sources": {"A": {"sha256": digest(b"old", "text/plain")}}}

        def fake_fetch(_):
            return b"new", "text/plain", 200

        result = check_sources(manifest, old, fake_fetch)
        self.assertEqual(result["changes"][0]["change"], "CONTENT_CHANGED")
        self.assertEqual(result["changes"][0]["source_id"], "A")

    def test_fetch_failure_becomes_review_signal(self):
        manifest = {"sources": [{"source_id": "A", "url": "https://example.test/a", "criticality": "high"}]}

        def fail(_):
            raise RuntimeError("offline")

        result = check_sources(manifest, None, fail)
        self.assertEqual(result["changes"][0]["change"], "FETCH_FAILED")


if __name__ == "__main__":
    unittest.main()
