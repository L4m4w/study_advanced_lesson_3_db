import logging
from http import HTTPStatus

import curlify
import requests

from requests import Session

class BaseSession(Session):
    def __init__(self, **kwargs):
        super().__init__()
        self.base_url = kwargs.get('base_url', None)

    def request(self, method, path, **kwargs):
        path = self.base_url + path
        logging.info(path)
        return super().request(method, path, **kwargs)

    def get(self, path="", expected_status=HTTPStatus.OK, **kwargs):
        headers = kwargs.pop("headers", None)
        response = requests.get(f"{self.base_url}/{path}", headers=headers)
        return response

    def post(self, path="", expected_status=HTTPStatus.CREATED, **kwargs):
        response = requests.post(f"{self.base_url}/{path}", json=kwargs["json"])
        return response

    def put(self, path="", expected_status=HTTPStatus.OK, **kwargs):
        response = requests.put(f"{self.base_url}/{path}", json=kwargs["json"])
        return response

    def patch(self, path="", expected_status=HTTPStatus.OK, **kwargs):
        response = requests.patch(f"{self.base_url}/{path}", json=kwargs["json"])
        return response

    def delete(self, path="", expected_status=HTTPStatus.OK, **kwargs):
        response = requests.delete(f"{self.base_url}/{path}")
        return response