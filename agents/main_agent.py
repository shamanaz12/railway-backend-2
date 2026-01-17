import asyncio
import json
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"

class AgentType(str, Enum):
    MAIN_AGENT = "main_agent"
    SUB_AGENT = "sub_agent"

class Message(BaseModel):
    id: str
    conversation_id: str
    sender_type: str
    sender_id: str
    content: str
    message_type: str = "text"
    agent_used: Optional[str] = None
    timestamp: datetime

class Agent:
    def __init__(self, agent_id: str, name: str, description: str, skills: List[str]):
        self.id = agent_id
        self.name = name
        self.description = description
        self.skills = skills
        self.status = AgentStatus.ACTIVE

    async def process_request(self, message: Message) -> str:
        """Process a request and return a response"""
        raise NotImplementedError("Subclasses must implement process_request")

class MainAgent(Agent):
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description, ["orchestration", "task_delegation"])
        self.sub_agents: Dict[str, Agent] = {}

    def register_sub_agent(self, agent: Agent):
        """Register a sub-agent with the main agent"""
        self.sub_agents[agent.id] = agent

    def find_best_agent(self, request: str) -> Optional[Agent]:
        """Find the best sub-agent to handle a request based on skills matching"""
        best_match = None
        best_score = 0

        for agent in self.sub_agents.values():
            score = self._calculate_skill_match(request, agent.skills)
            if score > best_score:
                best_score = score
                best_match = agent

        return best_match

    def _calculate_skill_match(self, request: str, skills: List[str]) -> int:
        """Calculate how well an agent's skills match a request"""
        request_lower = request.lower()
        score = 0

        for skill in skills:
            if skill.lower() in request_lower:
                score += 1

        return score

    async def process_request(self, message: Message) -> str:
        """Process a request by delegating to the appropriate sub-agent"""
        if not self.sub_agents:
            return "No sub-agents available for task delegation."

        # Find the best agent for the request
        best_agent = self.find_best_agent(message.content)

        if best_agent:
            # Update message to indicate which agent will process it
            message.agent_used = best_agent.name

            # Process the request with the selected agent
            response = await best_agent.process_request(message)
            return response
        else:
            return "No suitable agent found for this request."

# Import specialized agents
from .sub_agents.frontend_agent import FrontendAgent
from .sub_agents.backend_agent import BackendAgent
from .sub_agents.database_agent import DatabaseAgent
from .sub_agents.chat_ui_agent import ChatUIAgent
from .sub_agents.research_agent import ResearchAgent
from .sub_agents.testing_agent import TestingAgent
from .sub_agents.security_agent import SecurityAgent
from .sub_agents.deployment_agent import DeploymentAgent

# Initialize the main agent and sub-agents
main_agent = MainAgent(
    agent_id="main-agent-001",
    name="Main Agent",
    description="Central orchestrator that routes requests to appropriate sub-agents"
)

# Create and register sub-agents
frontend_agent = FrontendAgent(
    agent_id="sub-agent-001",
    name="Frontend Tasks Agent",
    description="Handles frontend development tasks"
)

backend_agent = BackendAgent(
    agent_id="sub-agent-002",
    name="Backend APIs Agent",
    description="Handles backend API development tasks"
)

database_agent = DatabaseAgent(
    agent_id="sub-agent-003",
    name="Database Agent",
    description="Handles database operations and queries"
)

chat_ui_agent = ChatUIAgent(
    agent_id="sub-agent-004",
    name="Chat UI Agent",
    description="Handles chat UI and real-time communication tasks"
)

research_agent = ResearchAgent(
    agent_id="sub-agent-005",
    name="Research Agent",
    description="Handles research and information gathering tasks"
)

testing_agent = TestingAgent(
    agent_id="sub-agent-006",
    name="Testing Agent",
    description="Handles testing and quality assurance tasks"
)

security_agent = SecurityAgent(
    agent_id="sub-agent-007",
    name="Security Agent",
    description="Handles security and compliance tasks"
)

deployment_agent = DeploymentAgent(
    agent_id="sub-agent-008",
    name="Deployment Agent",
    description="Handles deployment and DevOps tasks"
)

# Register all sub-agents with the main agent
main_agent.register_sub_agent(frontend_agent)
main_agent.register_sub_agent(backend_agent)
main_agent.register_sub_agent(database_agent)
main_agent.register_sub_agent(chat_ui_agent)
main_agent.register_sub_agent(research_agent)
main_agent.register_sub_agent(testing_agent)
main_agent.register_sub_agent(security_agent)
main_agent.register_sub_agent(deployment_agent)