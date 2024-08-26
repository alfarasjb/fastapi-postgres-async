from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str

    class Config:
        orm_mode = True
