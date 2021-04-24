from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    username: str
    password: str
    role: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    username: str
    role: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str
