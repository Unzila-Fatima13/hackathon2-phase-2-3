from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Any, List
import uuid

from database.database import get_session
from auth.middleware import JWTBearer, get_current_user_id
from models.task import Task, TaskCreate, TaskUpdate
from services.task_service import TaskService
from schemas.task import TaskPublic

router = APIRouter()


@router.get("/", response_model=List[TaskPublic])
def get_tasks(
    completed: bool = Query(None, description="Filter by completion status"),
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> Any:
    """Get all tasks for the authenticated user"""
    tasks = TaskService.get_tasks_for_user(
        session=session,
        user_id=current_user_id,
        completed=completed
    )
    return tasks


@router.post("/", response_model=TaskPublic)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> Any:
    """Create a new task for the authenticated user"""
    db_task = TaskService.create_task(
        session=session,
        task_create=task,
        user_id=current_user_id
    )
    return db_task


@router.get("/{task_id}", response_model=TaskPublic)
def get_task(
    task_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> Any:
    """Get a specific task by ID for the authenticated user"""
    task = TaskService.get_task_by_id(
        session=session,
        task_id=task_id,
        user_id=current_user_id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return task


@router.put("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> Any:
    """Update a specific task for the authenticated user"""
    updated_task = TaskService.update_task(
        session=session,
        task_id=task_id,
        task_update=task_update,
        user_id=current_user_id
    )
    return updated_task


@router.delete("/{task_id}")
def delete_task(
    task_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> Any:
    """Delete a specific task for the authenticated user"""
    success = TaskService.delete_task(
        session=session,
        task_id=task_id,
        user_id=current_user_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )
    return {"message": "Task deleted successfully"}