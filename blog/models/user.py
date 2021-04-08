from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from blog.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    blog = relationship('Blog', backref='author')
