from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime
import uuid

from backend.models import Task, User
from backend.schemas import TaskCreate, TaskUpdate


def get_user(db: Session, user_id: str):
    """
    Retrieve a user by ID
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_data: dict):
    """
    Create a new user
    """
    fake_user_id = str(uuid.uuid4())
    db_user = User(
        id=fake_user_id,
        name=user_data.get('name', ''),
        email=user_data.get('email', ''),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_task(db: Session, task_id: str):
    """
    Retrieve a task by ID
    """
    return db.query(Task).filter(Task.id == task_id).first()


def get_user_tasks(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    """
    Retrieve all tasks for a specific user
    """
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()


def create_user_task(db: Session, task: TaskCreate):
    """
    Create a new task for a user
    """
    fake_task_id = str(uuid.uuid4())
    db_task = Task(
        id=fake_task_id,
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        agent_assigned=task.agent_assigned,
        status=task.status if hasattr(task, 'status') else 'pending',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: str, task_update: TaskCreate):
    """
    Update a task by ID
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db_task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_task)
    return db_task


def update_task_status(db: Session, task_id: str, status: str):
    """
    Update the status of a task
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.status = status
        db_task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: str):
    """
    Delete a task by ID
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task