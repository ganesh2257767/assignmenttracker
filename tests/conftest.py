from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import create_engine, Session, SQLModel
from app.database import get_session
from app.config import settings
import pytest


@pytest.fixture(scope='module', autouse=True)
def setup_teardown():
    DB_URL = f"postgresql://{settings.test_database_username}:{settings.test_database_password}@{settings.test_database_host}/{settings.test_database_name}"
    engine = create_engine(DB_URL)
    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def client():
    return TestClient(app)


@pytest.fixture
def create_user(client):
    return client.post("/users", json={"email": "login@test.com", "password": "login1234"}).json()


@pytest.fixture
def access_token(client):
    response = client.post("/login", data={"username":"login@test.com", "password": "login1234"})
    return response.json().get("access_token")


@pytest.fixture
def create_post(client, create_user, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    task = client.post("/posts", json={"post_title": "test", "post_content":"test"}, headers=headers).json()
    return task