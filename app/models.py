from sqlmodel import Field, SQLModel, Relationship
import datetime
from sqlalchemy import Column, Boolean, text, String, TIMESTAMP, Integer
from sqlalchemy.sql import expression
from typing import List, Optional


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String, nullable=False, unique=True))
    password_hash: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC), sa_column=Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False))
    tasks: List["Task"] | None = Relationship(back_populates="user", cascade_delete=True)

    def __repr__(self) -> str:
        return f"User({self.id=}, {self.email=}, {self.created_at=})"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] | None = Field(default=None, primary_key=True)
    task_name: str = Field(sa_column=Column(String, nullable=False))
    task_type: str = Field(sa_column=Column(String, nullable=False))
    deadline: datetime.datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False))
    completed: bool = Field(default=False, sa_column=Column(Boolean, server_default=expression.false(), nullable=False))
    upvotes: Optional[int] = Field(default=0, sa_column=Column(Integer, server_default="0", nullable=False))
    downvotes: Optional[int] = Field(default=0, sa_column=Column(Integer, server_default="0", nullable=False))
    user_id: Optional[int] | None = Field(default=None, foreign_key="users.id", ondelete='CASCADE')
    user: User = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task({self.id=}, {self.task_name=}, {self.task_type=}, {self.deadline=}, {self.completed=})"


class UpVote(SQLModel, table=True):
    __tablename__ = "upvotes"
    user_id: int = Field(foreign_key="users.id", primary_key=True, ondelete='CASCADE')
    task_id: int = Field(foreign_key="tasks.id", primary_key=True, ondelete='CASCADE')


class DownVote(SQLModel, table=True):
    __tablename__ = "downvotes"
    user_id: int = Field(foreign_key="users.id", primary_key=True, ondelete='CASCADE')
    task_id: int = Field(foreign_key="tasks.id", primary_key=True, ondelete='CASCADE')