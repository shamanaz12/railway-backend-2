import asyncio
from typing import List
from agents.main_agent import Agent, AgentStatus

class DatabaseAgent(Agent):
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description, ["database", "postgres", "sql", "neon", "queries", "migration", "orm"])

    async def process_request(self, message: 'Message') -> str:
        """Process database-related requests"""
        return f"[Database Agent] Processing database request: {message.content[:50]}..."