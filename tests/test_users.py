import requests
import pytest

class TestLocalApi:

    @pytest.mark.local
    def test_get_users_positive_response(self):
        response = requests.get(f"{self.BASE_URL}/api/users", headers=self.headers)
        assert response.status_code == 200

    @pytest.mark.local
    def test_get_users_unauthorized_response(self):
        response = requests.get(f"{self.BASE_URL}/api/users?page=2&size=3")
        assert response.status_code == 401

    @pytest.mark.local
    def test_get_users_unauthorized_response_message(self):
        response = requests.get(f"{self.BASE_URL}/api/users?page=2&size=3")
        assert response.json()['detail']['error'] == 'Missing API key'

    @pytest.mark.local
    @pytest.mark.usefixtures('fill_test_data')
    @pytest.mark.xfail
    @pytest.mark.parametrize("user_id, expected_email", [
                                 (1, "george.bluth@reqres.in"),
                                 (2, "janet.weaver@reqres.in"),
                                 (3, "emma.wong@reqres.in")
                             ])
    def test_get_users_check_email_of_user(self, user_id, expected_email):
        response = requests.get(f"{self.BASE_URL}/api/users/{user_id}", headers=self.headers)
        # item = [item for item in response.json()['data'] if item.get('id') == user_id]
        assert response.json()['email'] == expected_email

    """
    4. Добавить тесты на пагинацию. Тестовых данных должно быть достаточно для проверки пагинации (не менее 10).
    5. Проверяем:
    - ожидаемое количество объектов в ответе;
    - правильное количество страниц при разных значениях size;
    - возвращаются разные данные при разных значениях page;
    """

    @pytest.mark.usefixtures('fill_test_data')
    @pytest.mark.pagination
    def test_get_users_check_users_data_amount(self, get_users):
        response = requests.get(f"{self.BASE_URL}/api/users", headers=self.headers)
        assert len(response.json()['data']) == len(get_users)

    @pytest.mark.usefixtures('fill_test_data')
    @pytest.mark.pagination
    @pytest.mark.parametrize("size_param, expected_size", [
        (1, 1),
        (6, 6),
        (12, 12)
    ])
    def test_get_users_data_check_by_size_param(self, size_param, expected_size):
        response = requests.get(f"{self.BASE_URL}/api/users?size={size_param}", headers=self.headers)
        assert len(response.json()['data']) == expected_size

    @pytest.mark.usefixtures('fill_test_data')
    @pytest.mark.pagination
    @pytest.mark.xfail
    @pytest.mark.parametrize("page_param", [
        1, 6, 99
    ])
    def test_get_users_data_check_by_page_param(self, page_param, get_users_by_id):
        response = requests.get(f"{self.BASE_URL}/api/users?page={page_param}&size=1", headers=self.headers)
        assert response.json()['data'] == get_users_by_id(page_param)

    """
    2. Расширить тестовое покрытие:
    - Тест на post: создание. Предусловия: подготовленные тестовые данные
    - Тест на delete: удаление. Предусловия: созданный пользователь
    - Тест на patch: изменение. Предусловия: созданный пользователь
        
    По желанию:
    - Get после создания, изменения
    - Тест на 405 ошибку: Предусловия: ничего не нужно
    - 404 422 ошибки на delete patch    
    - 404 на удаленного пользователя    
    - user flow: создаем, читаем, обновляем, удаляем
    - валидность тестовых данных (емейл, урл)    
    - отправить модель без поля на создание
    """

    @pytest.mark.http
    def test_create_user(self, generate_users_batch):

        generate_func, user_ids_tracker = generate_users_batch
        users = generate_func(1)

        for user in users:
            create_response = requests.post(f'{self.BASE_URL}/api/users/', json=user)
            user_id = create_response.json()['id']

            user_ids_tracker.append(user_id)

            response = requests.get(f"{self.BASE_URL}/api/users/{create_response.json()['id']}", headers=self.headers)

            assert response.json()['avatar'] == user['avatar']
            assert response.json()['email'] == user['email']
            assert response.json()['first_name'] == user['first_name']
            assert response.json()['last_name'] == user['last_name']

    @pytest.mark.http
    def test_delete_user(self, generate_users_batch, create_user):
        generate_func, user_ids_tracker = generate_users_batch
        users = generate_func(1)

        user_to_delete = create_user(*users)

        requests.delete(f'{self.BASE_URL}/api/users/{user_to_delete}')

        response = requests.get(f"{self.BASE_URL}/api/users/{user_to_delete}", headers=self.headers)
        assert response.json()['detail'] == 'User not found'

    @pytest.mark.http
    def test_update_user(self, generate_users_batch, create_user):
        generate_func, user_ids_tracker = generate_users_batch
        user = generate_func(1)

        user_to_update = create_user(*user)
        update_info = generate_func(1)

        for info in update_info:
            put_response = requests.put(f'{self.BASE_URL}/api/users/{user_to_update}', json=info)
            user_id = put_response.json()['id']

            user_ids_tracker.append(user_id)

            response = requests.get(f"{self.BASE_URL}/api/users/{user_to_update}", headers=self.headers)

            assert response.json()['avatar'] != user[0]['avatar']
            assert response.json()['email'] != user[0]['email']
            assert response.json()['first_name'] != user[0]['first_name']
            assert response.json()['last_name'] != user[0]['last_name']
