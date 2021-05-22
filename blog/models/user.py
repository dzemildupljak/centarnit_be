from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from blog.database import Base
from blog.models.blog import Blog


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    username = Column(String)
    password = Column(String)
    is_confirmed = Column(Boolean, default=False, nullable=False)
    blog = relationship(Blog, backref='author')
