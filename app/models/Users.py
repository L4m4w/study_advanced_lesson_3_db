from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class User(SQLModel, table = True):
    id: int | None = Field(primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str