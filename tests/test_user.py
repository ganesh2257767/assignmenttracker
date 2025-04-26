from fastapi.testclient import TestClient
from app.main import app
from app.schemas import *
from fastapi import status
from sqlmodel import create_engine, Session, SQLModel
from app.database import get_session
from app.config import settings

DB_URL = f"postgresql://{settings.test_database_username}:{settings.test_database_password}@{settings.test_database_host}/{settings.test_database_name}"
engine = create_engine(DB_URL)

SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Welcome": "This is the index page"}


def test_create_user():
    response = client.post("/users", json={"email":"test@test.com", "password": "Password123"})
    UserCreateResponse(**response.json())
    assert response.status_code == status.HTTP_201_CREATED


def test_create_duplicate_user():
    response = client.post("/users", json={"email": "test@test.com", "password": "Password123"})
    assert response.status_code == status.HTTP_409_CONFLICT
    ExceptionSchema(**response.json())
