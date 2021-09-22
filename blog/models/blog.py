from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now(), nullable=True)
