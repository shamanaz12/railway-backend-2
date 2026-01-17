from typing import Dict, Optional
from agents.main_agent import main_agent, Agent

class AgentRegistry:
    """
    Registry to manage and access agents by ID
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """
        Initialize the registry with the main agent and all sub-agents
        """
        # Add main agent
        self.agents[main_agent.id] = main_agent
        
        # Add all sub-agents from main agent
        for agent_id, agent in main_agent.sub_agents.items():
            self.agents[agent_id] = agent
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        Retrieve an agent by its ID
        """
        return self.agents.get(agent_id)
    
    def get_main_agent(self) -> Agent:
        """
        Get the main orchestrator agent
        """
        return self.agents.get(main_agent.id)
    
    def get_all_agents(self) -> Dict[str, Agent]:
        """
        Get all registered agents
        """
        return self.agents.copy()
    
    def register_agent(self, agent: Agent):
        """
        Register a new agent in the registry
        """
        self.agents[agent.id] = agent

# Global instance of the registry
agent_registry = AgentRegistry()