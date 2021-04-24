from pydantic import BaseModel
from blog.schemas.user import ShowUser


class Blog(BaseModel):
    id: int
    title: str
    body: str


class CreateBlog(BaseModel):
    title: str
    body: str
    author: int

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    author: ShowUser

    class Config:
        orm_mode = True


class BlogTest(BaseModel):
    pass
