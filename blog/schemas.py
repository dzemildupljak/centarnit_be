from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


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


class CreateBlog(Blog):
    author: int

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    author: ShowUser

    class Config:
        orm_mode = True
