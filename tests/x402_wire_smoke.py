import os

os.environ['PROJECTPERMIT_X402_ENABLED'] = 'true'
os.environ['PROJECTPERMIT_X402_PRICE_USD'] = '$0.01'
os.environ['PROJECTPERMIT_X402_BATCH_PRICE_USD'] = '$0.05'
os.environ['PROJECTPERMIT_X402_NETWORK'] = 'eip155:84532'
os.environ['PROJECTPERMIT_X402_PAY_TO'] = '0xDAAef0FD525278aAD0bA11066A96c338642A3d1A'
os.environ['PROJECTPERMIT_X402_FACILITATOR_URL'] = 'https://x402.org/facilitator'

from fastapi.testclient import TestClient
from x402.http import decode_payment_required_header
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

challenge = decode_payment_required_header(header).model_dump(by_alias=True, exclude_none=True)
assert challenge.get('x402Version') == 2, challenge
assert challenge.get('accepts'), challenge
assert any(item.get('network') == 'eip155:84532' for item in challenge['accepts']), challenge

bazaar = (challenge.get('extensions') or {}).get('bazaar')
assert bazaar, challenge
info = bazaar.get('info') or {}
input_info = info.get('input') or {}
assert input_info.get('type') == 'http', input_info
assert input_info.get('method') == 'POST', input_info
assert input_info.get('bodyType') == 'json', input_info
assert (input_info.get('body') or {}).get('jurisdiction') == 'ottawa_on', input_info
output_info = info.get('output') or {}
assert output_info.get('type') == 'json', output_info
output_example = output_info.get('example') or {}
assert output_example.get('engine_version') == 'phase0-0.1.0', output_info
bundle = output_example.get('action_bundle') or {}
assert bundle.get('bundle_version') == '2026-08-29.2', output_example
identity = bundle.get('identity') or {}
assert identity.get('bundle_id'), identity
assert identity.get('idempotency_key'), identity
assert str(identity['bundle_id']).startswith('ppb_'), identity
assert str(identity['idempotency_key']).startswith('ppidem_'), identity
change = bundle.get('change') or {}
assert change.get('classification') == 'FIRST_OBSERVATION', change

# x402 v2 serializes the JSON Schema for `info` at extensions.bazaar.schema.
# OutputConfig.schema is folded into schema.properties.output.properties.example.
extension_schema = bazaar.get('schema') or {}
schema_properties = extension_schema.get('properties') or {}
input_body_schema = (((schema_properties.get('input') or {}).get('properties') or {}).get('body') or {})
assert 'ottawa_on' in ((((input_body_schema.get('properties') or {}).get('jurisdiction') or {}).get('enum')) or []), input_body_schema
output_example_schema = ((((schema_properties.get('output') or {}).get('properties') or {}).get('example') or {}))
output_properties = output_example_schema.get('properties') or {}
assert 'action_bundle' in output_properties, output_example_schema
bundle_schema = output_properties.get('action_bundle') or {}
bundle_properties = bundle_schema.get('properties') or {}
assert 'identity' in bundle_properties, bundle_schema
assert 'change' in bundle_properties, bundle_schema

batch_response = client.post('/v1/check-project-requirements-batch', json={
    'items': [
        {
            'client_ref': 'wire-smoke-001',
            'jurisdiction': 'ottawa_on',
            'project': {'family': 'window_door', 'action': 'replace_same_size'},
            'property': {'heritage': False},
        }
    ]
})
assert batch_response.status_code == 402, (batch_response.status_code, batch_response.text)
batch_header = batch_response.headers.get('payment-required')
assert batch_header, dict(batch_response.headers)
batch_challenge = decode_payment_required_header(batch_header).model_dump(by_alias=True, exclude_none=True)
assert batch_challenge.get('x402Version') == 2, batch_challenge
assert batch_challenge.get('accepts'), batch_challenge
assert any(item.get('network') == 'eip155:84532' for item in batch_challenge['accepts']), batch_challenge

print('x402 unpaid wire smoke: single + bulk 402 challenges + HTTP Bazaar identity/action-bundle metadata OK')
