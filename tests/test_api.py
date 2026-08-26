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
        self.assertEqual('phase1a-0.2.0', r.json()['engine_version'])

    def test_free_capabilities(self):
        r = self.client.get('/v1/capabilities')
        self.assertEqual(200, r.status_code)
        payload = r.json()
        jurisdictions = {item['id']: item for item in payload['jurisdictions']}
        self.assertEqual(
            {'gatineau_qc', 'ottawa_on', 'toronto_on', 'mississauga_on'},
            set(jurisdictions),
        )
        self.assertTrue(jurisdictions['toronto_on']['address_resolution'])
        self.assertFalse(jurisdictions['mississauga_on']['address_resolution'])
        self.assertEqual(8, len(payload['project_families']))

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

    def test_toronto_same_size_single_house_window(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'toronto_on',
            'project': {
                'family': 'window_door',
                'action': 'replace_same_size',
                'single_dwelling_house': True,
                'structural_change': False,
                'new_exit': False,
            },
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('LIKELY_NOT_REQUIRED', r.json()['determination'])

    def test_mississauga_basement_finish(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'mississauga_on',
            'project': {'family': 'basement', 'action': 'finish_basement'},
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('REQUIRED', r.json()['determination'])

    def test_missing_mississauga_address_resolver_is_422(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'mississauga_on',
            'address': '300 City Centre Dr, Mississauga, ON',
            'resolve_address': True,
            'project': {'family': 'window_door', 'action': 'replace_same_size'},
        })
        self.assertEqual(422, r.status_code)


if __name__ == '__main__':
    unittest.main()
