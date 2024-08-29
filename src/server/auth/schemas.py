from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    email: str

    class Config:
        orm_mode = True


class UserCreate(User):
    name: str
    password: str


class UserLogin(User):
    password: str


class OAuthToken(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True
