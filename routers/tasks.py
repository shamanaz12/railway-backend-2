from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from backend.crud import *
from backend.models import *
from backend.schemas import Task, TaskCreate, TaskUpdate
from backend.database import get_db

# Also import the schemas module to reference it directly
import backend.schemas as schemas

router = APIRouter(prefix="/api", tags=["tasks"])

@router.post("/{user_id}/tasks", response_model=schemas.Task)
def create_task(
    user_id: str, 
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new task for a specific user
    """
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Set the user_id from the path parameter to ensure consistency
    task_data = task.dict()
    task_data['user_id'] = user_id
    task_data['status'] = 'pending'  # Default status
    
    # Create the task
    db_task = crud.create_user_task(db, schemas.TaskCreate(**task_data))
    return db_task


@router.get("/{user_id}/tasks", response_model=List[schemas.Task])
def get_tasks(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all tasks for a specific user
    """
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    tasks = crud.get_user_tasks(db, user_id=user_id, skip=skip, limit=limit)
    return tasks


@router.get("/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def get_task(
    user_id: str,
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID for a specific user
    """
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify task belongs to user
    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    user_id: str,
    task_id: str,
    task_update: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Update a specific task by ID for a specific user
    """
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify task belongs to user
    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    updated_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a specific task by ID for a specific user
    """
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify task belongs to user
    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    crud.delete_task(db, task_id=task_id)
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete")
def toggle_task_completion(
    user_id: str,
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Toggle the completion status of a specific task
    """
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify task belongs to user
    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    # Toggle completion status
    new_status = "completed" if task.status != "completed" else "pending"
    task_update = schemas.TaskCreate(
        title=task.title,
        description=task.description,
        user_id=str(task.user_id),
        agent_assigned=task.agent_assigned
    )
    
    updated_task = crud.update_task_status(db, task_id=task_id, status=new_status)
    return {
        "id": updated_task.id,
        "title": updated_task.title,
        "description": updated_task.description,
        "status": updated_task.status,
        "completed": updated_task.status == "completed"
    }