from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class TaskBase(BaseModel):
    title: str
    description: str
    user_id: UUID
    agent_assigned: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: UUID
    status: str  # e.g., "pending", "in_progress", "completed", "failed"
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True