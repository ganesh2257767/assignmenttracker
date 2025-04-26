from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from app.database import get_session
from sqlmodel import Session, select
from app.models import User
from app.schemas import TokenResponse
from app.utils import compare_passwords
from app.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_credentials.username)
    user: Optional[User] = session.scalars(statement).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")

    if not compare_passwords(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")

    token = create_access_token({
        "user_id": user.id
    })

    return TokenResponse(access_token=token, token_type="bearer")