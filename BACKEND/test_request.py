import requests

resp = requests.post(
    'http://localhost:8001/api/auth/register',
    json={'name': 'TestUser', 'email': 'test@example.com', 'password': 'password123'}
)
print('status', resp.status_code)
print(resp.text)
