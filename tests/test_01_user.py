from fastapi import status
import pytest
from app.schemas import UserCreateResponse, ExceptionSchema
from tests.conftest import client, setup_teardown

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
    assert len(response.json()) == 3


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