import pytest
from fastapi import status
from app.schemas import TaskResponse, ExceptionSchema
from tests.conftest import client, setup_teardown, access_token, create_user

def test_get_all_tasks_initial(client, create_user, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.get("/tasks", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.parametrize("task_name, task_type, deadline", [
    ("Python", "Assignment", "2025-05-01"),
    ("Java", "Test", "2025-05-01"),
    ("Selenium", "Project", "2025-05-01")
])
def test_create_a_task(client, access_token, task_name, task_type, deadline):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/tasks", json={"task_name": task_name, "task_type": task_type, "deadline": deadline}, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    TaskResponse(**response.json())



def test_get_all_tasks(client, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.get("/tasks", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.parametrize("idx", [1, 2, 3])
def test_get_task_by_id(client, access_token, idx):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(f"/tasks/{idx}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    task = response.json()
    TaskResponse(**task)
    assert task["id"] == idx


@pytest.mark.parametrize("idx", [4, 5, 6])
def test_get_task_that_does_not_exist(client, access_token, idx):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(f"/tasks/{idx}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    ExceptionSchema(**response.json())


@pytest.mark.parametrize("idx", [1, 2, 3])
def test_complete_a_task(client, access_token, idx):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.patch(f"/tasks/{idx}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    task = response.json()
    TaskResponse(**task)
    assert task["completed"] == True


@pytest.mark.parametrize("idx", [1, 2, 3])
def test_undo_complete_a_task(client, access_token, idx):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.patch(f"/tasks/{idx}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    task = response.json()
    TaskResponse(**task)
    assert task["completed"] == False


@pytest.mark.parametrize("idx", [1, 2, 3])
def test_delete_a_task(client, access_token, idx):
    input()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.delete(f"/tasks/{idx}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    task = response.json()
    TaskResponse(**task)
    assert task["id"] == idx
    input()