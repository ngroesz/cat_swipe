import simplejson as json
import re
import requests

def test_person_api(client, create_users, create_persons):
    response = client.get('/api/persons')
    assert response.status_code == 200
    assert response.json == {"authorized": "false"}

    response = client.post('/api/auth', json={'device_id': '1234', 'password': 'password'})
    print('status code: {}'.format(response.status_code))
    print('json: {}'.format(response.json))
    assert response.status_code == 200
    access_token = response.json['access_token']
    assert re.match(r'\w+', access_token)

    data = json.dumps(dict(access_token_cookie=access_token))
    client.set_cookie('localhost', 'access_token_cookie', access_token)
    response = client.get('/api/persons', data=data)
    assert response.status_code == 200
    assert int(response.json['meta']['count']) == 2


def test_person_api_again(client, create_users, create_persons):
    response = client.get('/api/persons')
    assert response.status_code == 200
