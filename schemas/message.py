from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class MessageBase(BaseModel):
    conversation_id: UUID
    sender_type: str
    sender_id: UUID
    content: str
    message_type: str = "text"

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: UUID
    agent_used: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True