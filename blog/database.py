from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/centarnit_db"
SQLALCHEMY_DATABASE_URL = "postgres://jxtqnmnpzqkfqf:7303b16637618897b0264429c0b79a2aca8de6b3d484a56f2bb4f8b25c6fa7c7@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/d8u7aj6ruinb2g"

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
