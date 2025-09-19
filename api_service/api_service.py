import json

import uvicorn
from fastapi.params import Depends
from fastapi_pagination import Params, paginate
from starlette.responses import JSONResponse
from fastapi import FastAPI, Header, HTTPException
from http import HTTPStatus

from helpers import PROJECT_ROOT, get_custom_params
from models.AppStatus import AppStatus
from models.Users import User

app = FastAPI()

users: list[User] = []

@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))

@app.get("/api/status", status_code=HTTPStatus.OK)
def api_status() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/api/users/{id}")
def get_user_by_id(id: int) -> User:
    if id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=("Invalid user id - ", id))
    if id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[id - 1]

@app.get("/api/users")
def get_users( x_api_key: str = Header(default=None), params: Params = Depends(get_custom_params)) -> dict:
    if x_api_key != "reqres-free-v1":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail={"error": "Missing API key"})

    paginated_data = paginate(users, params)

    response_message = {
        "page": params.page,
        "per_page": params.size,
        "total": len(users),
        "total_pages": (len(users) + params.size - 1) // params.size,
        "data": paginated_data.items,
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