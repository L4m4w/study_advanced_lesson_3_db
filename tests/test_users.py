import requests
import pytest

class TestLocalApi:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.BASE_URL = "http://localhost:8002/api"
        self.headers = {"x-api-key": "reqres-free-v1"}
        yield

    @pytest.mark.local
    def test_get_users_positive_response(self):
        response = requests.get(f"{self.BASE_URL}/users", headers=self.headers)
        assert response.status_code == 200

    @pytest.mark.local
    def test_get_users_unauthorized_response(self):
        response = requests.get(f"{self.BASE_URL}/users?page=2&per_page=3")
        assert response.status_code == 401

    @pytest.mark.local
    def test_get_users_unauthorized_response_message(self):
        response = requests.get(f"{self.BASE_URL}/users?page=2&per_page=3")
        assert response.json()['detail']['error'] == 'Missing API key'

    @pytest.mark.local
    @pytest.mark.parametrize("user_id, expected_email", [
                                 (1, "george.bluth@reqres.in"),
                                 (2, "janet.weaver@reqres.in"),
                                 (3, "emma.wong@reqres.in")
                             ])
    def test_get_users_check_email_of_first_user(self, user_id, expected_email):
        response = requests.get(f"{self.BASE_URL}/users", headers=self.headers)
        item = [item for item in response.json()['data'] if item.get('id') == user_id]
        assert item[0]['email'] == expected_email

"""
4. Добавить тесты на пагинацию. Тестовых данных должно быть достаточно для проверки пагинации (не менее 10).
5. Проверяем:
- ожидаемое количество объектов в ответе;
- правильное количество страниц при разных значениях size;
- возвращаются разные данные при разных значениях page;
"""