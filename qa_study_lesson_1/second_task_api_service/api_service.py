from starlette.responses import JSONResponse
from fastapi import FastAPI, Header

"""
Вместо https://reqres.in разработать свой микросервис в стеке Python + FastAPI (допускается также Flask, Django).
- Автотесты должны также успешно проходить.
- В коде микросервиса не должно быть хардкода.
"""

app = FastAPI()

@app.get("/api/users/{id}")
def get_user_by_id(id):
    return {
                "id": id,
                "email": "george.bluth@reqres.in",
                "first_name": "George",
                "last_name": "Bluth",
                "avatar": "https://reqres.in/img/faces/1-image.jpg"
            }

@app.get("/api/users", status_code=200)
def get_users(page='1', per_page=None, x_api_key = Header(default=None)):
    if x_api_key  != "reqres-free-v1":
        return JSONResponse(content={"error": "Missing API key"}, status_code=401)
    else:
        response_message = {
            "page": page,
            "per_page": per_page,
            "total": 3,
            "total_pages": 2,
            "data": [
                {
                    "id": 1,
                    "email": "george.bluth@reqres.in",
                    "first_name": "George",
                    "last_name": "Bluth",
                    "avatar": "https://reqres.in/img/faces/1-image.jpg"
                }
            ] if page == '1' else [],
            "support": {
                "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
                "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
            }
        }
        return response_message