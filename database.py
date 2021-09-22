from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
# USER = os.getenv('POSTGRES_USER')
# PASSWORD = os.getenv('POSTGRES_PASSWORD')
# # SERVER = os.getenv('POSTGRES_SERVER')
# SERVER = 'localhost'
# PORT = os.getenv('POSTGRES_PORT')
# DB = os.getenv('POSTGRES_DB')

LOCAL_DATABASE_URL = os.getenv('LOCAL_DATABASE_URL')
DATABASE_URL = os.getenv('DATABASE_URL')

# SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}'
SQLALCHEMY_DATABASE_URL = f'{LOCAL_DATABASE_URL}'
# SQLALCHEMY_DATABASE_URL = f'{DATABASE_URL}'

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
