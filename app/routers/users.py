import json

import uvicorn
from fastapi.params import Depends
from fastapi_pagination import Params, paginate
from fastapi import FastAPI, Header, HTTPException, APIRouter
from http import HTTPStatus

from app.helpers import  get_custom_params
from app.models.AppStatus import AppStatus
from app.models.Users import User, UserCreate, UserUpdate
from app.database import users


router = APIRouter(prefix='/api/users')


@router.get("/{id}")
def get_user_by_id(id: int) -> User:
    if id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=("Invalid user id - ", id))
    user = users.get_user(user_id=id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user

@router.get("", status_code=HTTPStatus.OK)
def get_users( x_api_key: str = Header(default=None), params: Params = Depends(get_custom_params)) -> dict:
    if x_api_key != "reqres-free-v1":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail={"error": "Missing API key"})

    paginated_data = paginate(users.get_users(), params)

    response_message = {
        "page": params.page,
        "per_page": params.size,
        "total": len(users.get_users()),
        "total_pages": (len(users.get_users()) + params.size - 1) // params.size,
        "data": paginated_data.items,
        "support": {
            "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
            "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
        }
    }
    return response_message

@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    UserCreate.model_validate(user)
    return users.create_user(user)

@router.put("/{user_id}", status_code=HTTPStatus.CREATED)
def update_user(user_id: int, user: User) -> User:
    if user_id <1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Invalid user ID')
    UserUpdate.model_validate(user)
    return users.update_user(user_id, user)

@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    if user_id <1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Invalid user ID')
    users.delete_user(user_id)
    return {'message': f'User: "{user_id}" deleted'}
