import asyncio
from typing import List
from agents.main_agent import Agent, AgentStatus

class ChatUIAgent(Agent):
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description, ["chat", "ui", "websocket", "realtime", "messaging", "conversation"])

    async def process_request(self, message: 'Message') -> str:
        """Process chat UI-related requests"""
        return f"[Chat UI Agent] Processing chat UI request: {message.content[:50]}..."