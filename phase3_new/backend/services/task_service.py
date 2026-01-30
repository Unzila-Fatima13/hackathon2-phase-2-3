from sqlmodel import Session, select
from typing import List, Optional
import uuid
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User
from fastapi import HTTPException, status

class TaskService:
    @staticmethod
    def create_task(*, session: Session, task_create: TaskCreate, user_id: str) -> Task:
        """Create a new task for a user"""
        try:
            # Convert the user_id string to UUID format for proper assignment
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            # If conversion fails, raise an error as this indicates invalid user_id
            raise ValueError(f"Invalid user_id format: {user_id}")

        # Create task with validated data and user_id
        task_data = task_create.model_dump()
        db_task = Task(**task_data, user_id=user_uuid)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

    @staticmethod
    def get_task_by_id(*, session: Session, task_id: uuid.UUID, user_id: str) -> Optional[Task]:
        """Get a specific task by ID for a specific user"""
        try:
            # Convert the user_id string to UUID format for proper lookup
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            # If conversion fails, use the original string
            user_uuid = user_id

        statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
        return session.exec(statement).first()

    @staticmethod
    def get_tasks_for_user(*, session: Session, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """Get all tasks for a specific user, optionally filtered by completion status"""
        try:
            # Convert the user_id string to UUID format for proper lookup
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            # If conversion fails, use the original string
            user_uuid = user_id

        query = select(Task).where(Task.user_id == user_uuid)

        if completed is not None:
            query = query.where(Task.is_completed == completed)

        query = query.order_by(Task.created_at.desc())

        return session.exec(query).all()

    @staticmethod
    def update_task(*, session: Session, task_id: uuid.UUID, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """Update a task for a specific user"""
        try:
            # Convert the user_id string to UUID format for proper lookup
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            # If conversion fails, use the original string
            user_uuid = user_id

        db_task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_uuid)).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or you don't have permission to update it"
            )

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

    @staticmethod
    def delete_task(*, session: Session, task_id: uuid.UUID, user_id: str) -> bool:
        """Delete a task for a specific user"""
        try:
            # Convert the user_id string to UUID format for proper lookup
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            # If conversion fails, use the original string
            user_uuid = user_id

        db_task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_uuid)).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or you don't have permission to delete it"
            )

        session.delete(db_task)
        session.commit()

        return True