from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime


class PostBase(BaseModel):
    post_title: str
    post_content: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user: "UserCreateResponse"
    upvotes: int
    downvotes: int


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserCreateResponse(UserBase):
    id: int
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class VoteBase(BaseModel):
    post_id: int


class UpVoteCreate(VoteBase):
    pass


class DownVoteCreate(VoteBase):
    pass

class ExceptionSchema(BaseModel):
    detail: str