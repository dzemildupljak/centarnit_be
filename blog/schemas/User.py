from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    username: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    username: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str
