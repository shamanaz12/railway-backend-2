from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# User Models
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID

    class Config:
        from_attributes = True

# Task Models
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

# Conversation Models
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

# Chat Message Models
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

# Agent Models
class AgentBase(BaseModel):
    name: str
    description: str
    status: str

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Skills Definition Models
class SkillsDefinitionBase(BaseModel):
    agent_id: UUID
    skill_name: str
    description: str

class SkillsDefinitionCreate(SkillsDefinitionBase):
    pass

class SkillsDefinition(SkillsDefinitionBase):
    id: UUID
    keywords: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True