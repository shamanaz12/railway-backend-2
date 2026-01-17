import re
from typing import List, Dict, Tuple
from agents.main_agent import Agent

class SkillsMatcher:
    """
    Matches incoming requests to the most appropriate agent based on skills
    """
    
    def __init__(self):
        pass
    
    def find_best_agent(self, request: str, agents: List[Agent]) -> Tuple[Agent, float]:
        """
        Find the best agent to handle a request based on skills matching
        Returns the best agent and a confidence score
        """
        best_agent = None
        best_score = 0.0
        
        for agent in agents:
            score = self.calculate_skill_match(request, agent.skills)
            if score > best_score:
                best_score = score
                best_agent = agent
                
        return best_agent, best_score
    
    def calculate_skill_match(self, request: str, skills: List[str]) -> float:
        """
        Calculate how well an agent's skills match a request
        Returns a normalized score between 0 and 1
        """
        if not skills:
            return 0.0
            
        request_lower = request.lower()
        matched_keywords = 0
        
        for skill in skills:
            skill_lower = skill.lower()
            # Check for exact matches, partial matches, and regex patterns
            if skill_lower in request_lower:
                matched_keywords += 1
            elif self._has_synonym_match(skill_lower, request_lower):
                matched_keywords += 0.5  # Partial credit for synonym matches
        
        # Normalize the score
        score = matched_keywords / len(skills)
        return min(score, 1.0)  # Cap at 1.0
    
    def _has_synonym_match(self, skill: str, request: str) -> bool:
        """
        Check if the request contains synonyms or related terms to the skill
        """
        # Define some basic synonyms for common skills
        synonyms = {
            "frontend": ["ui", "interface", "client", "design", "html", "css", "javascript", "react", "vue", "angular"],
            "backend": ["server", "api", "database", "infrastructure", "rest", "graphql", "microservices"],
            "database": ["sql", "postgres", "mysql", "mongodb", "storage", "queries", "migration"],
            "api": ["endpoint", "route", "request", "response", "rest", "graphql", "integration"],
            "chat": ["messaging", "conversation", "realtime", "websocket", "communication"],
            "security": ["authentication", "authorization", "encryption", "vulnerability", "penetration"],
            "testing": ["qa", "quality", "unit", "integration", "e2e", "validation", "verification"],
            "deployment": ["devops", "ci", "cd", "pipeline", "docker", "kubernetes", "cloud", "hosting"]
        }
        
        skill_synonyms = synonyms.get(skill, [])
        request_words = request.split()
        
        for word in request_words:
            # Remove punctuation and convert to lowercase
            clean_word = re.sub(r'[^\w\s]', '', word).lower()
            if clean_word in skill_synonyms:
                return True
                
        return False

# Global instance of the skills matcher
skills_matcher = SkillsMatcher()