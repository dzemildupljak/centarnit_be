from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/centarnit_db"
# print('DATABASE_URL .get()', os.environ.get('DATABASE_URL'))
# print('DATABASE_URL []', 'postgresql' + os.environ['DATABASE_URL'][8:])
SQLALCHEMY_DATABASE_URL = 'postgresql' + os.environ['DATABASE_URL'][8:]

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
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


# postgres://fmnvesrfbkblja:f082dcd08fe0b9f0b2b2cced8089e0950ee5331717697c1f0602cd1d15b1c629@ec2-99-80-200-225.eu-west-1.compute.amazonaws.com:5432/de4o28kcohdor3