from fastapi import APIRouter, HTTPException
from typing import List
import json
import uuid
from datetime import datetime

from agents.main_agent import main_agent
from agents.agent_registry import agent_registry
from speckit.task_analyzer import task_analyzer

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

@router.post("/send")
async def send_message(content: str, conversation_id: str = None, sender_type: str = "user", sender_id: str = "default-user"):
    """
    Send a message to the AI agent system
    """
    try:
        # Create a new conversation if none provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            title = content[:50] + "..." if len(content) > 50 else content
        else:
            # In a real implementation, verify conversation exists
            title = f"Conversation {conversation_id}"

        # Create the user message object
        user_message = type('TempMessage', (), {
            'id': str(uuid.uuid4()),
            'conversation_id': conversation_id,
            'sender_type': sender_type,
            'sender_id': sender_id,
            'content': content,
            'message_type': 'text',
            'agent_used': None,
            'created_at': datetime.utcnow()
        })()

        # Process the message through the agent system
        response_content = await main_agent.process_request(user_message)

        return {
            "success": True,
            "message_id": str(uuid.uuid4()),
            "conversation_id": str(conversation_id),
            "response": response_content,
            "agent_used": getattr(user_message, 'agent_used', 'main_agent'),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/conversations")
async def get_conversations(limit: int = 20, offset: int = 0):
    """
    Get list of user's conversations (mock implementation)
    """
    # This would normally fetch from database
    # For now, returning a mock response
    return {
        "conversations": [],
        "total_count": 0,
        "limit": limit,
        "offset": offset
    }

@router.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str, limit: int = 50, offset: int = 0):
    """
    Get messages for a specific conversation (mock implementation)
    """
    # This would normally fetch from database
    # For now, returning a mock response
    return {
        "messages": [],
        "total_count": 0,
        "limit": limit,
        "offset": offset
    }