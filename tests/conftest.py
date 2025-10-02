import pytest
import json

import requests

from app.helpers import PROJECT_ROOT


@pytest.fixture(autouse=True, scope="class")
def api_config(request):
    if request.cls:
        setattr(request.cls, 'BASE_URL', "http://localhost:8002")
        setattr(request.cls, 'headers', {"x-api-key": "reqres-free-v1"})

@pytest.fixture()
def get_users(file="users.json"):
    with open(file=PROJECT_ROOT / file) as f:
        users = json.load(f)

    return users

@pytest.fixture()
def get_users_list(file="users_list.json"):
    with open(file=PROJECT_ROOT / file) as f:
        users = json.load(f)

    return users

@pytest.fixture()
def get_users_by_id(get_users_list):

    def _find_user(user_id):
        return [item for item in get_users_list if item.get('id') == user_id]

    return _find_user

@pytest.fixture()
def fill_test_data(request, get_users):
    api_users = []
    for user in get_users:
        response = requests.post(f'{request.cls.BASE_URL}/api/users/', json=user)
        api_users.append(response.json())

    yield

    for user in api_users:
        requests.delete(f'{request.cls.BASE_URL}/api/users/{user['id']}')
