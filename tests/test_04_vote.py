
from fastapi import status
from tests.conftest import client, setup_teardown, access_token, create_user, create_post

user = None
post = None

def test_upvote(client, create_user, access_token, create_post):
    global user, post
    user = create_user
    post = create_post
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/up", json={"post_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} upvoted post: {post.get("id")}"


def test_remove_upvote(client, access_token):
    global user, post
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/up", json={"post_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} removed upvote from post: {post.get("id")}"


def test_downvote(client, access_token):
    global user, post
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/down", json={"post_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} downvoted post: {post.get("id")}"


def test_remove_downvote(client, access_token):
    global user, post
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/down", json={"post_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} removed downvote from post: {post.get("id")}"


def test_upvote_downvoted_post(client, access_token):
    global user, post
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    client.post("/vote/down", json={"post_id": 1}, headers=headers)
    response = client.post("/vote/up", json={"post_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} upvoted post: {post.get("id")}, downvote removed automatically"


def test_downvote_upvoted_post(client, access_token):
    global user, post
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/down", json={"post_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} downvoted post: {post.get("id")}, upvote removed automatically"
