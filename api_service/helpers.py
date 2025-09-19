from pathlib import Path

from fastapi_pagination.bases import AbstractParams, RawParams
from fastapi_pagination.default import Page, Params


def find_project_root():
    current = Path(__file__).parent
    while not (current / ".git").exists() and not (current / "pyproject.toml").exists():
        if current.parent == current:
            return Path.cwd()
        current = current.parent
    return current

PROJECT_ROOT = find_project_root()

def get_custom_params(page: int = 1, size: int = 12) -> Params:
    return Params(page=page, size=size)