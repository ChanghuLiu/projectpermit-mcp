import unittest
from fastapi.testclient import TestClient
from projectpermit.api import app


class ApiSmokeTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        r = self.client.get('/health')
        self.assertEqual(200, r.status_code)
        self.assertTrue(r.json()['ok'])

    def test_ottawa_same_size_window(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'ottawa_on',
            'project': {'family': 'window_door', 'action': 'replace_same_size'},
            'property': {'heritage': False},
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('LIKELY_NOT_REQUIRED', r.json()['determination'])

    def test_gatineau_structural_change(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'gatineau_qc',
            'project': {
                'family': 'interior_renovation',
                'action': 'renovate',
                'structural_change': True,
                'estimated_cost_cad': 5000,
            },
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('REQUIRED', r.json()['determination'])


if __name__ == '__main__':
    unittest.main()
