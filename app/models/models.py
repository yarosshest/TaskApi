from typing import Optional

from pydantic import BaseModel

from db.models import Photo


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class LoginForm(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "assigned"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    complete: Optional[bool] = None
    status: Optional[str] = None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    complete: bool
    status: str


class PdPhoto(BaseModel):
    id: int
    url: str



