from pydantic import BaseModel


class User(BaseModel):
    email: str

    class Config:
        orm_mode = True


class UserCreate(User):
    name: str
    password: str


class UserLogin(User):
    password: str
