import pytest
from fastapi import status
from app.schemas import PostResponse, ExceptionSchema
from tests.conftest import client, setup_teardown, access_token, create_user

def test_get_all_posts_initial(client, create_user, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.get("/posts", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.parametrize("post_title, post_content", [
    ("Python", "Assignment"),
    ("Java", "Test"),
    ("Selenium", "Project")
])
def test_create_a_post(client, access_token, post_title, post_content):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/posts", json={"post_title": post_title, "post_content": post_content}, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    PostResponse(**response.json())



def test_get_all_posts(client, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.get("/posts", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.parametrize("idx", [1, 2, 3])
def test_get_post_by_id(client, access_token, idx):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(f"/posts/{idx}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    PostResponse(**post)
    assert post["id"] == idx


@pytest.mark.parametrize("idx", [4, 5, 6])
def test_get_post_that_does_not_exist(client, access_token, idx):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(f"/posts/{idx}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    ExceptionSchema(**response.json())


@pytest.mark.parametrize("idx", [1, 2, 3])
def test_delete_a_post(client, access_token, idx):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete(f"/posts/{idx}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    PostResponse(**post)
    assert post["id"] == idx
