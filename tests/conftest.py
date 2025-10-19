import pytest
import json

import requests
from faker import Faker

from app.helpers import PROJECT_ROOT


@pytest.fixture(autouse=True, scope="class")
def api_config(request):
    if request.cls:
        setattr(request.cls, 'BASE_URL', "http://127.0.0.1:8002")
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

    user_ids = [user['id'] for user in api_users]
    user_emails = [user['email'] for user in api_users]

    yield user_ids, user_emails

    for user_id in user_ids:
        requests.delete(f'{request.cls.BASE_URL}/api/users/{user_id}')


@pytest.fixture
def generate_users_batch(request):

    fake = Faker()
    created_users_id = []

    def _generate_batch(count=3, **common_kwargs):
        users = []
        for i in range(count):
            first_name = common_kwargs.get('first_name', fake.first_name())
            last_name = common_kwargs.get('last_name', fake.last_name())
            email = f"{first_name.lower()}.{last_name.lower()}@reqres.in"

            user_data = {
                "email": f"{first_name.lower()}.{last_name.lower()}@reqres.in",
                "first_name": first_name,
                "last_name": last_name,
                "avatar": f"https://reqres.in/img/faces/{first_name}-image.jpg"
            }

            # Обновляем общими параметрами и индивидуальными
            user_data.update(common_kwargs)
            """
            specific_users = generate_users_batch(
                3, 
                first_name="SameFirstName"  # У всех одинаковое имя
            )
            """
            if count > 1:
                users.append(user_data)
            else:
                users = user_data


        # users = json.dumps(users)


        return users

    yield _generate_batch, created_users_id

    for user_id in created_users_id:
        try:
            requests.delete(f'{request.cls.BASE_URL}/api/users/{user_id}')
            print(f"Deleted user with ID: {user_id}")
        except Exception as e:
            print(f"Failed to delete user {user_id}: {e}")

    # return _generate_batch

@pytest.fixture()
def create_user(request):
    def _create_user(user):
        response = requests.post(f'{request.cls.BASE_URL}/api/users/', json=user)
        return response.json()['id']
    return _create_user