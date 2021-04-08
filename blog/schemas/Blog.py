from typing import Optional
from pydantic import BaseModel
from .User import ShowUser


class Blog(BaseModel):
    title: str
    body: str


class CreateBlog(Blog):
    author: int

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    author: ShowUser

    class Config:
        orm_mode = True
