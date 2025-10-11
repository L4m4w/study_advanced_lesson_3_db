from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List

from tests.utils.base_session import BaseSession
from tests.utils.config import Server


"""
{
    "email": "george.bluth@reqres.in",
    "last_name": "Bluth",
    "avatar": "https://reqres.in/img/faces/1-image.jpg",
    "first_name": "George",
    "id": 1
}
"""

class GetUser(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl

    @property
    def json(self) -> dict:
        return self.model_dump()

"""
{
    "page": 1,
    "per_page": 12,
    "total": 36,
    "total_pages": 3,
    "data": [
        {
            "email": "george.bluth@reqres.in",
            "last_name": "Bluth",
            "avatar": "https://reqres.in/img/faces/1-image.jpg",
            "first_name": "George",
            "id": 1
        }
    ],
    "support": {
        "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
        "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
    }
}
"""

class Support(BaseModel):
    url: HttpUrl
    text: str

    @property
    def json(self) -> dict:
        return self.model_dump()

class GetUsers(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[GetUser]
    support: Support

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     response = kwargs.pop("response", None)
    #     json_ = kwargs.pop("json", response.json() if response else None)

    @property
    def json(self) -> dict:
        return self.model_dump()






class LocalAPI:
    def __init__(self, env: str):
        self.session = BaseSession(base_url=Server(env).local_api)

    def get_user(self, user_id: int):
        return ...