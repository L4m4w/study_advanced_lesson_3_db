import pytest

from tests.models.user import GetUsers, GetUser

"""
1. Расширить тестовое покрытие smoke тестами на доступность микросервиса.
"""


class TestSmokeApi:

    @pytest.mark.smoke
    def test_smoke_status_of_users(self, local_api):
        response = local_api.get("/status")
        assert response.status_code == 200
        # assert response.json()['users'] is True

    @pytest.mark.smoke
    def test_smoke_status_of_api(self, local_api):
        response = local_api.get("/api/status")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'

    @pytest.mark.smoke
    def test_smoke_get_users_check_model(self, local_api):
        response = local_api.get("/api/users", headers=self.headers)
        GetUsers(**response.json())

    @pytest.mark.smoke
    def test_smoke_get_user_check_model(self, local_api):
        response = local_api.get("/api/users/1", headers=self.headers)
        GetUser(**response.json())


