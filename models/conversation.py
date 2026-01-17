from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ConversationBase(BaseModel):
    title: Optional[str] = None
    user_id: UUID

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True