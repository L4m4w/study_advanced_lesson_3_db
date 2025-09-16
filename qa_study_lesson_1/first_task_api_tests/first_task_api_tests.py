import requests
import pytest

"""
1. Разработать несколько API-автотестов на https://reqres.in
(если обучались на основном курсе python - можно взять код автотестов из домашнего задания)
"""

class TestRegressApi:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.BASE_URL = "https://reqres.in/api"
        self.headers = {"x-api-key": "reqres-free-v1"}
        yield

    def test_get_users_positive_response(self):
        response = requests.get(f"{self.BASE_URL}/users", headers=self.headers)
        assert response.status_code == 200

    def test_get_users_unauthorized_response(self):
        response = requests.get(f"{self.BASE_URL}/users?page=2&per_page=3")
        assert response.status_code == 401

    def test_get_users_unauthorized_response_body(self):
        response = requests.get(f"{self.BASE_URL}/users?page=2&per_page=3")
        assert response.json()['error'] == 'Missing API key'

    @pytest.mark.parametrize("user_id, expected_email", [
                                 (1, "george.bluth@reqres.in")
                             ])
    def test_get_users_check_email_of_first_user(self, user_id, expected_email):
        response = requests.get(f"{self.BASE_URL}/users", headers=self.headers)
        item = [item for item in response.json()['data'] if item.get('id') == user_id]
        assert item[0]['email'] == expected_email

