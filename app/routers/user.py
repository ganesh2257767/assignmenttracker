from app.models import User
from app.schemas import UserCreate, UserCreateResponse
from app.database import get_session
from fastapi import status, Depends, HTTPException, APIRouter
from sqlmodel import Session
from app.utils import get_hashed_password
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/{idx}", status_code=status.HTTP_200_OK, response_model=UserCreateResponse)
def get_user_by_id(idx: int, session: Session = Depends(get_session)):
    user = session.get(User, idx)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_a_user(user: UserCreate, session: Session = Depends(get_session)):
    email = user.email
    password_hash = get_hashed_password(user.password)
    new_user = User(email=email, password_hash=password_hash)
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )