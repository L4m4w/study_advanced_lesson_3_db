import json

import uvicorn
from starlette.responses import JSONResponse
from fastapi import FastAPI, Header, HTTPException
from http import HTTPStatus

from helpers import PROJECT_ROOT
from models.AppStatus import AppStatus
from models.Users import User

app = FastAPI()

users: list[User] = []

@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))

@app.get("/api/users/{id}")
def get_user_by_id(id: int):
    if id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=("Invalid user id - ", id))
    if id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[id - 1]

@app.get("/api/users")
def get_users(page='1', per_page=None, x_api_key = Header(default=None)):
    if x_api_key  != "reqres-free-v1":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail={"error": "Missing API key"})
    else:
        response_message = {
            "page": page,
            "per_page": per_page,
            "total": 3,
            "total_pages": 2,
            "data": users,
            "support": {
                "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
                "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
            }
        }
        return response_message

if __name__ == "__main__":
    with open(file=PROJECT_ROOT / "users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    print("Users loaded")

    uvicorn.run(app, host="localhost", port=8002)