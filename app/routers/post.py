from app.models import Post, User
from app.schemas import PostCreate, PostResponse
from app.database import get_session
from fastapi import status, Depends, HTTPException, APIRouter
from sqlmodel import select, Session
from typing import List
from app.oauth2 import verify_and_get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def get_all_posts(session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    statement = select(Post).where(
        (Post.user_id == user.id)
    )
    posts = session.exec(statement).all()
    return posts


@router.get("/{idx}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post_by_id(idx: int, session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    statement = select(Post).where(
        (Post.user_id == user.id) & (Post.id == idx)
    )
    post = session.exec(statement).one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_a_post(task: PostCreate, session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    new_post = Post(**task.model_dump(), user_id=user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.delete("/{idx}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def delete_a_post(idx: int, session: Session = Depends(get_session), user: User = Depends(verify_and_get_current_user)):
    statement = select(Post).where(
        (Post.user_id == user.id) & (Post.id == idx)
    )
    post = session.exec(statement).one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    session.delete(post)
    session.commit()
    return post
