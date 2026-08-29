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
        self.assertEqual('phase1c-0.5.0', r.json()['engine_version'])

    def test_free_capabilities(self):
        r = self.client.get('/v1/capabilities')
        self.assertEqual(200, r.status_code)
        payload = r.json()
        jurisdictions = {item['id']: item for item in payload['jurisdictions']}
        self.assertEqual(
            {
                'gatineau_qc', 'ottawa_on', 'toronto_on', 'mississauga_on',
                'laval_qc', 'longueuil_qc', 'vancouver_bc',
            },
            set(jurisdictions),
        )
        for jurisdiction in (
            'gatineau_qc', 'ottawa_on', 'toronto_on', 'mississauga_on', 'vancouver_bc',
        ):
            self.assertTrue(jurisdictions[jurisdiction]['address_resolution'])
        for jurisdiction in ('laval_qc', 'longueuil_qc'):
            self.assertFalse(jurisdictions[jurisdiction]['address_resolution'])
        self.assertEqual(8, len(payload['project_families']))
        self.assertEqual('/v1/preview-project-requirements', payload['free_preview_resource'])
        self.assertEqual(
            '/v1/preview-project-requirements-batch',
            payload['free_batch_preview_resource'],
        )
        self.assertEqual(50, payload['bulk_max_items'])
        self.assertFalse(payload['free_preview_address_resolution'])

    def test_free_preview_returns_deterministic_result(self):
        r = self.client.post('/v1/preview-project-requirements', json={
            'jurisdiction': 'ottawa_on',
            'project': {'family': 'window_door', 'action': 'replace_same_size'},
            'property': {'heritage': False},
            'context': {'client_tag': 'unit-test-preview'},
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('LIKELY_NOT_REQUIRED', r.json()['determination'])

    def test_free_preview_rejects_raw_address_and_address_resolution_fields(self):
        r = self.client.post('/v1/preview-project-requirements', json={
            'jurisdiction': 'ottawa_on',
            'project': {'family': 'window_door', 'action': 'replace_same_size'},
            'address': '123 Example St',
            'resolve_address': True,
        })
        self.assertEqual(422, r.status_code)

    def test_free_batch_preview_isolates_bad_items_and_returns_audit(self):
        r = self.client.post('/v1/preview-project-requirements-batch', json={
            'items': [
                {
                    'client_ref': 'lead-good',
                    'jurisdiction': 'ottawa_on',
                    'project': {'family': 'window_door', 'action': 'replace_same_size'},
                    'property': {'heritage': False},
                },
                {
                    'client_ref': 'lead-bad',
                    'jurisdiction': 'ottawa_on',
                },
            ],
        })
        self.assertEqual(200, r.status_code)
        payload = r.json()
        self.assertEqual(2, payload['batch_size'])
        self.assertEqual(1, payload['succeeded'])
        self.assertEqual(1, payload['failed'])
        self.assertEqual('lead-good', payload['results'][0]['client_ref'])
        self.assertEqual('LIKELY_NOT_REQUIRED', payload['results'][0]['result']['determination'])
        self.assertEqual('validation_error', payload['results'][1]['error']['type'])
        self.assertGreaterEqual(payload['audit']['unique_rule_ids'], 1)
        self.assertGreaterEqual(payload['audit']['evidence_links'], 1)

    def test_free_batch_preview_rejects_batch_level_oversize(self):
        item = {
            'jurisdiction': 'ottawa_on',
            'project': {'family': 'window_door', 'action': 'replace_same_size'},
        }
        r = self.client.post('/v1/preview-project-requirements-batch', json={
            'items': [item] * 51,
        })
        self.assertEqual(422, r.status_code)

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

    def test_laval_same_size_window(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'laval_qc',
            'project': {'family': 'window_door', 'action': 'replace_same_size'},
            'property': {'piia': False},
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('LIKELY_NOT_REQUIRED', r.json()['determination'])

    def test_longueuil_window_enlargement(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'longueuil_qc',
            'project': {'family': 'window_door', 'action': 'enlarge_existing_opening'},
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('REQUIRED', r.json()['determination'])

    def test_vancouver_cosmetic_interior(self):
        r = self.client.post('/v1/check-project-requirements', json={
            'jurisdiction': 'vancouver_bc',
            'project': {'family': 'interior_renovation', 'action': 'painting'},
        })
        self.assertEqual(200, r.status_code)
        self.assertEqual('LIKELY_NOT_REQUIRED', r.json()['determination'])


if __name__ == '__main__':
    unittest.main()
