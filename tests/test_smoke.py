from http import HTTPStatus

import requests
import pytest

"""
1. Расширить тестовое покрытие smoke тестами на доступность микросервиса.
"""


class TestSmokeApi:

    @pytest.mark.smoke
    def test_smoke_status_of_users(self):
        response = requests.get(f"{self.BASE_URL}/status")
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.smoke
    def test_smoke_status_of_api(self):
        response = requests.get(f"{self.BASE_URL}/api/status")
        assert response.status_code == HTTPStatus.OK
        assert response.json()['status'] == 'healthy'
