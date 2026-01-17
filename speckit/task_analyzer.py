import re
from typing import Dict, List, Optional
from enum import Enum

class TaskCategory(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    CHAT_UI = "chat_ui"
    RESEARCH = "research"
    TESTING = "testing"
    SECURITY = "security"
    DEPLOYMENT = "deployment"
    GENERAL = "general"

class TaskAnalyzer:
    """
    Analyzes tasks to determine their category and complexity
    """
    
    def __init__(self):
        self.category_keywords = {
            TaskCategory.FRONTEND: [
                "ui", "interface", "design", "html", "css", "javascript", "react", 
                "vue", "angular", "frontend", "styling", "component", "mobile", 
                "responsive", "tailwind", "bootstrap", "nextjs", "frontend"
            ],
            TaskCategory.BACKEND: [
                "api", "server", "endpoint", "route", "backend", "rest", 
                "graphql", "microservice", "database", "integration", "authentication",
                "authorization", "oauth", "jwt", "session", "middleware"
            ],
            TaskCategory.DATABASE: [
                "database", "sql", "postgres", "mysql", "mongodb", "query", 
                "migration", "orm", "schema", "table", "index", "join", 
                "relational", "nosql", "storage", "transaction"
            ],
            TaskCategory.CHAT_UI: [
                "chat", "messaging", "conversation", "realtime", "websocket", 
                "message", "conversation", "ui", "interface", "communication", 
                "instant", "live", "typing", "presence"
            ],
            TaskCategory.RESEARCH: [
                "research", "investigate", "analyze", "study", "examine", 
                "explore", "gather", "collect", "information", "data", 
                "learn", "understand", "evaluate"
            ],
            TaskCategory.TESTING: [
                "test", "testing", "unit", "integration", "e2e", "qa", 
                "quality", "assertion", "validation", "verification", 
                "coverage", "mock", "spy", "stub"
            ],
            TaskCategory.SECURITY: [
                "security", "authentication", "authorization", "encryption", 
                "vulnerability", "penetration", "secure", "safe", "protect", 
                "password", "hash", "salt", "certificate", "ssl", "tls"
            ],
            TaskCategory.DEPLOYMENT: [
                "deploy", "deployment", "devops", "ci", "cd", "pipeline", 
                "docker", "kubernetes", "container", "cloud", "hosting", 
                "server", "infrastructure", "scaling", "monitoring"
            ]
        }
    
    def analyze_task(self, task_description: str) -> Dict:
        """
        Analyze a task description and return its category and metadata
        """
        category_scores = {}
        
        # Calculate scores for each category
        for category, keywords in self.category_keywords.items():
            score = self._calculate_category_score(task_description, keywords)
            category_scores[category.value] = score
        
        # Determine the best matching category
        best_category = max(category_scores, key=category_scores.get)
        best_score = category_scores[best_category]
        
        # Determine complexity based on length and technical terms
        complexity = self._estimate_complexity(task_description)
        
        return {
            "category": best_category,
            "confidence": best_score,
            "complexity": complexity,
            "keywords_found": self._find_matching_keywords(task_description),
            "estimated_time": self._estimate_time(complexity)
        }
    
    def _calculate_category_score(self, task: str, keywords: List[str]) -> float:
        """
        Calculate how well a task matches a category based on keywords
        """
        task_lower = task.lower()
        matches = 0
        
        for keyword in keywords:
            if keyword in task_lower:
                matches += 1
                
        # Return normalized score
        return matches / len(keywords) if keywords else 0.0
    
    def _estimate_complexity(self, task_description: str) -> str:
        """
        Estimate the complexity of a task based on length and technical terms
        """
        # Count technical terms (words with camelCase, PascalCase, or containing special characters)
        technical_terms = re.findall(r'\b[a-zA-Z][a-z]*[A-Z][a-zA-Z0-9]*\b|\b\w*[/_-]\w*\b', task_description)
        
        # Estimate based on length and technical terms
        word_count = len(task_description.split())
        technical_density = len(technical_terms) / max(word_count, 1)
        
        if word_count < 10:
            return "low"
        elif technical_density > 0.15 or word_count > 50:
            return "high"
        else:
            return "medium"
    
    def _find_matching_keywords(self, task_description: str) -> List[str]:
        """
        Find all keywords that match the task description
        """
        task_lower = task_description.lower()
        matching_keywords = []
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in task_lower:
                    matching_keywords.append(keyword)
                    
        return list(set(matching_keywords))  # Remove duplicates
    
    def _estimate_time(self, complexity: str) -> str:
        """
        Estimate the time required based on complexity
        """
        time_estimates = {
            "low": "10-30 minutes",
            "medium": "1-3 hours",
            "high": "3-8 hours"
        }
        return time_estimates.get(complexity, "Unknown")

# Global instance of the task analyzer
task_analyzer = TaskAnalyzer()