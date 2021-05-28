from datetime import date, datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from blog.database import Base
from blog.models.blog import Blog


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_identifier = Column(String)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    username = Column(String)
    password = Column(String)
    is_confirmed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)
    blog = relationship(Blog, backref='author')
