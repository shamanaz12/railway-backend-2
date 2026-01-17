import asyncio
from typing import List
from agents.main_agent import Agent, AgentStatus

class FrontendAgent(Agent):
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description, ["frontend", "ui", "ux", "html", "css", "javascript", "react", "nextjs", "tailwind"])

    async def process_request(self, message: 'Message') -> str:
        """Process frontend-related requests"""
        return f"[Frontend Agent] Processing frontend request: {message.content[:50]}..."