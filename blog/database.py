from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# SQLALCHEMY_DATABASE_URL = 'postgresql' + os.environ['DATABASE_URL'][8:]
# if 'DATABASE_URL' in os.environ:
# SQLALCHEMY_DATABASE_URL = 'postgresql' + os.environ['DATABASE_URL'][8:]
# else:
# SQLALCHEMY_DATABASE_URL = "postgresql://wvayycvipuslad:589a7961d101195b9909f0194d365539fad055d1ef5de8fd6c144f5f6b52761e@ec2-54-72-155-238.eu-west-1.compute.amazonaws.com:5432/d70lha4t5efof3"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@db:5432/centarnit_db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/centarnit_db"
# print('dotenv_values()', dotenv_values()['SQLALCHEMY_DATABASE_URL'])
load_dotenv()
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
SERVER = os.getenv('POSTGRES_SERVER')
PORT = os.getenv('POSTGRES_PORT')
DB = os.getenv('POSTGRES_DB')

SQLALCHEMY_DATABASE_URL = f'postgresql://fmnvesrfbkblja:f082dcd08fe0b9f0b2b2cced8089e0950ee5331717697c1f0602cd1d15b1c629@ec2-99-80-200-225.eu-west-1.compute.amazonaws.com:5432/de4o28kcohdor3'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}'

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
