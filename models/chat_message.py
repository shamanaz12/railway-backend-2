from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ChatMessageBase(BaseModel):
    conversation_id: UUID
    sender_type: str
    sender_id: UUID
    content: str
    message_type: str = "text"

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: UUID
    agent_used: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True