from http import HTTPStatus

from fastapi import APIRouter

from app.models.AppStatus import AppStatus
# from app.database import users_from_db

router = APIRouter()

@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=True)

@router.get("/api/status", status_code=HTTPStatus.OK)
def api_status() -> dict[str, str]:
    return {"status": "healthy"}
