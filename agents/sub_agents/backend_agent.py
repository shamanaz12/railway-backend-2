import asyncio
from typing import List
from agents.main_agent import Agent, AgentStatus

class BackendAgent(Agent):
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description, ["backend", "api", "rest", "graphql", "server", "fastapi", "python", "database"])

    async def process_request(self, message: 'Message') -> str:
        """Process backend-related requests"""
        return f"[Backend Agent] Processing backend request: {message.content[:50]}..."