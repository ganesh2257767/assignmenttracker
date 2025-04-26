
from fastapi import status
from tests.conftest import client, setup_teardown, access_token, create_user, create_task

user = None
task = None

def test_upvote(client, create_user, access_token, create_task):
    global user, task
    user = create_user
    task = create_task
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/up", json={"task_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} upvoted task: {task.get("id")}"


def test_remove_upvote(client, access_token):
    global user, task
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/up", json={"task_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} removed upvote from task: {task.get("id")}"


def test_downvote(client, access_token):
    global user, task
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/down", json={"task_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} downvoted task: {task.get("id")}"


def test_remove_downvote(client, access_token):
    global user, task
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/down", json={"task_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} removed downvote from task: {task.get("id")}"


def test_upvote_downvoted_task(client, access_token):
    global user, task
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    client.post("/vote/down", json={"task_id": 1}, headers=headers)
    response = client.post("/vote/up", json={"task_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} upvoted task: {task.get("id")}, downvote removed automatically"


def test_downvote_upvoted_task(client, access_token):
    global user, task
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/vote/down", json={"task_id": 1}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response.get("message") == f"User: {user.get("email")} downvoted task: {task.get("id")}, upvote removed automatically"
