from pydantic import BaseModel
from user.schemas.user import ShowUser


class Blog(BaseModel):
    id: int
    title: str
    body: str
    cover_image: str = ''


class UpdateBlog(BaseModel):
    title: str
    body: str


class CreateBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    author: ShowUser

    class Config:
        orm_mode = True


class BlogTest(BaseModel):
    pass
