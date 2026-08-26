import os

os.environ['PROJECTPERMIT_X402_ENABLED'] = 'true'
os.environ['PROJECTPERMIT_X402_PRICE_USD'] = '$0.01'
os.environ['PROJECTPERMIT_X402_NETWORK'] = 'eip155:84532'
os.environ['PROJECTPERMIT_X402_PAY_TO'] = '0xDAAef0FD525278aAD0bA11066A96c338642A3d1A'
os.environ['PROJECTPERMIT_X402_FACILITATOR_URL'] = 'https://x402.org/facilitator'

from fastapi.testclient import TestClient
from projectpermit.api import app

client = TestClient(app)

health = client.get('/health')
assert health.status_code == 200, health.text

response = client.post('/v1/check-project-requirements', json={
    'jurisdiction': 'ottawa_on',
    'project': {'family': 'window_door', 'action': 'replace_same_size'},
    'property': {'heritage': False},
})
assert response.status_code == 402, (response.status_code, response.text)
header = response.headers.get('payment-required')
assert header, dict(response.headers)
print('x402 unpaid wire smoke: 402 + PAYMENT-REQUIRED OK')
