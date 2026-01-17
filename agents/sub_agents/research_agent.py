import asyncio
from typing import List
from agents.main_agent import Agent, AgentStatus

class ResearchAgent(Agent):
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description, ["research", "information", "gathering", "analysis", "data", "study", "examine", "explore", "collect", "learn", "understand", "evaluate"])

    async def process_request(self, message: 'Message') -> str:
        """Process research-related requests"""
        return f"[Research Agent] Processing research request: {message.content[:50]}..."