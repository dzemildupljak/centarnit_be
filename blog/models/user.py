from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from blog.database import Base
from blog.models.blog import Blog


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    role = Column(String, default='user')
    username = Column(String)
    password = Column(String)
    blog = relationship(Blog, backref='author')
