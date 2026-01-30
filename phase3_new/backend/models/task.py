from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, max_length=10000)
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None

class TaskPublic(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID