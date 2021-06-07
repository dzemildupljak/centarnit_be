from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from blog.main import app
from user.helpers.JWToken import fake_secret_token
import os
from dotenv import load_dotenv
import pytest

load_dotenv()
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
SERVER = os.getenv('POSTGRES_SERVER')
PORT = os.getenv('POSTGRES_PORT')
DB = os.getenv('POSTGRES_DB_TEST')

SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}'

# print(f'postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}')

client = TestClient(app)


# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture(scope='session')
def engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def dbsession(engine, tables):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


def clear_table():
    with engine.connect() as con:
        con.execute('TRUNCATE TABLE users RESTART IDENTITY;')

# /////////////////////////////////////////////////////////////////////////
# /////////////////////////// Unauthorized ////////////////////////////////


def test_get_all_users_unauthorized():
    res = client.get("/user")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}


def test_get_user_by_id_unauthorized():
    res = client.get("/user/1")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}


def test_update_user_role_unauthorized():
    res = client.put("/user/2/role/sysadmin")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}


def test_delete_user_unauthorized():
    res = client.delete("/user/2")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}

# /////////////////////////////////////////////////////////////////////////


def test_create_user():
    clear_table()
    res = client.post('/user/',
                      json={
                          "name": "user1",
                          "email": "user1@mail.com",
                          "username": "user1",
                          "password": "sifra123",
                          "role": "admin"
                      })
    assert res.status_code == 200
    assert res.json() == {
        "id": 1,
        "name": "user1",
        "email": "user1@mail.com",
        "username": "user1",
        "role": "user"
    }
    clear_table()


def test_update_user_role():
    res = client.put('/user/1/role/admin',
                     headers={"Authorization": f"Bearer {fake_secret_token}"})
    assert res.status_code == 200
    assert res.json() == {"detail": "User with id 2 was updated"}
    clear_table()
