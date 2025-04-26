from fastapi import status
import pytest
from app.schemas import TokenResponse, ExceptionSchema
from tests.conftest import client, setup_teardown, create_user


@pytest.mark.parametrize("username, password",
                         [("login@test.com", "login1234")])
def test_login(client, create_user, username, password):
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == status.HTTP_200_OK
    TokenResponse(**response.json())


@pytest.mark.parametrize("username, password",
                         [("login1@test.com", "login1234")])
def test_login_invalid_username(client, username, password):
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    ExceptionSchema(**response.json())


@pytest.mark.parametrize("username, password",
                         [("login@test.com", "password1234")])
def test_login_invalid_password(client, username, password):
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    ExceptionSchema(**response.json())