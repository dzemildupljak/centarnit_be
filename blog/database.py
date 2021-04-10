from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = 'postgresql' + os.environ['DATABASE_URL'][8:]
if 'DATABASE_URL' in os.environ:
    SQLALCHEMY_DATABASE_URL = 'postgresql' + os.environ['DATABASE_URL'][8:]
else:
    # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@db:5432/centarnit_db"
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/centarnit_db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
