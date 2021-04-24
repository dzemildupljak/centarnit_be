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
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

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
