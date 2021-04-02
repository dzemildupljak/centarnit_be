from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(Blog):
    pass

    class Config:
        orm_mode = True


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
