from app.models import Task, User
from app.schemas import TaskCreate, TaskResponse
from app.database import get_session
from fastapi import status, Depends, HTTPException, APIRouter
from sqlmodel import select, Session
from typing import List
from app.oauth2 import verify_and_get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TaskResponse])
def get_all_tasks(session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    statement = select(Task).where(
        (Task.user_id == user.id)
    )
    tasks = session.exec(statement).all()
    return tasks


@router.get("/{idx}", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def get_task_by_id(idx: int, session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    statement = select(Task).where(
        (Task.user_id == user.id) & (Task.id == idx)
    )
    task = session.exec(statement).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_a_task(task: TaskCreate, session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    new_task = Task(**task.model_dump(), user_id=user.id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.patch("/{idx}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def complete_a_task(idx: int, session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    statement = select(Task).where(
        (Task.user_id == user.id) & (Task.id == idx)
    )
    task = session.exec(statement).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{idx}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def delete_a_task(idx: int, session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    statement = select(Task).where(
        (Task.user_id == user.id) & (Task.id == idx)
    )
    task = session.exec(statement).one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    session.delete(task)
    session.commit()
    return task
