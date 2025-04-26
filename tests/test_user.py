from fastapi.testclient import TestClient
from app.main import app
from app.schemas import *
from fastapi import status
from sqlmodel import create_engine, Session, SQLModel
from app.database import get_session
from app.config import settings
import pytest

DB_URL = f"postgresql://{settings.test_database_username}:{settings.test_database_password}@{settings.test_database_host}/{settings.test_database_name}"
engine = create_engine(DB_URL)


def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def client():
    return TestClient(app)


def test_base_route(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Welcome": "This is the index page"}


def test_no_users(client):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.parametrize("email, password",
                         [("user1@test.com", "password"),
                         ("user2@test.com", "password"),
                         ("user3@test.com", "password")])
def test_create_user(client, email, password):
    response = client.post("/users", json={"email":email, "password": password})
    assert response.status_code == status.HTTP_201_CREATED
    UserCreateResponse(**response.json())


def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    users_list = response.json()
    assert len(users_list) == 3


@pytest.mark.parametrize("idx", [1, 2, 3])
def test_get_user_by_id(client, idx):
    response = client.get(f"/users/{idx}")
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["id"] == idx


@pytest.mark.parametrize("idx", [4, 5, 6])
def test_get_user_that_does_not_exist(client, idx):
    response = client.get(f"/users/{idx}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    ExceptionSchema(**response.json())


@pytest.mark.parametrize("email, password",
                         [("user1@test.com", "password")])
def test_create_duplicate_user(client, email, password):
    response = client.post("/users", json={"email": email, "password": password})
    assert response.status_code == status.HTTP_409_CONFLICT
    ExceptionSchema(**response.json())