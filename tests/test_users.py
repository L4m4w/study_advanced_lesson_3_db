import requests
import pytest

class TestLocalApi:

    @pytest.mark.local
    def test_get_users_positive_response(self):
        response = requests.get(f"{self.BASE_URL}/users", headers=self.headers)
        assert response.status_code == 200

    @pytest.mark.local
    def test_get_users_unauthorized_response(self):
        response = requests.get(f"{self.BASE_URL}/users?page=2&size=3")
        assert response.status_code == 401

    @pytest.mark.local
    def test_get_users_unauthorized_response_message(self):
        response = requests.get(f"{self.BASE_URL}/users?page=2&size=3")
        assert response.json()['detail']['error'] == 'Missing API key'

    @pytest.mark.local
    @pytest.mark.parametrize("user_id, expected_email", [
                                 (1, "george.bluth@reqres.in"),
                                 (2, "janet.weaver@reqres.in"),
                                 (3, "emma.wong@reqres.in")
                             ])
    def test_get_users_check_email_of_user(self, user_id, expected_email):
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

    @pytest.mark.pagination
    def test_get_users_check_users_data_amount(self, get_users):
        response = requests.get(f"{self.BASE_URL}/users", headers=self.headers)
        assert len(response.json()['data']) == len(get_users)

    @pytest.mark.pagination
    @pytest.mark.parametrize("size_param, expected_size", [
        (1, 1),
        (6, 6),
        (99, 12)
    ])
    def test_get_users_data_check_by_size_param(self, size_param, expected_size):
        response = requests.get(f"{self.BASE_URL}/users?size={size_param}", headers=self.headers)
        assert len(response.json()['data']) == expected_size

    @pytest.mark.pagination
    @pytest.mark.parametrize("page_param", [
        1, 6, 99
    ])
    def test_get_users_data_check_by_page_param(self, page_param, get_users_by_id):
        response = requests.get(f"{self.BASE_URL}/users?page={page_param}&size=1", headers=self.headers)
        assert response.json()['data'] == get_users_by_id(page_param)


