import requests

# Functions for other service
WORKPLACE_URL = 'http://workplace/workplaces'


def get_workplace(workplace_id):
    try:
        response = requests.get(f'{WORKPLACE_URL}/{workplace_id}')
    except Exception:
        return {'error': 'Cannot reach workplace service'}
    if response.status_code == 200:
        return response.json()
    return None


def create_workplace(data):
    try:
        response = requests.post(WORKPLACE_URL, json=data)
    except Exception:
        return {'error': 'Cannot reach workplace service'}
    if response.status_code == 201:
        return response.json()
    return None

