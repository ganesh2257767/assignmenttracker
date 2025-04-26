from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime


class TaskBase(BaseModel):
    task_name: str
    task_type: str
    deadline: datetime
    #
    # model_config = ConfigDict(from_attributes=True)
    #

class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    completed: bool
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
    task_id: int
    #
    # model_config = ConfigDict(from_attributes=True)
    #

class UpVoteCreate(VoteBase):
    pass


class DownVoteCreate(VoteBase):
    pass
