from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime
import uuid

# Import routers
from routers import chat, agents, websocket, tasks

# Import models and agents
from agents.main_agent import main_agent
from agents.agent_registry import agent_registry
from speckit.skills_matcher import skills_matcher
from speckit.task_analyzer import task_analyzer

load_dotenv()

app = FastAPI(title="Hackathon 2 Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production, restrict as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(agents.router)
app.include_router(websocket.router)
app.include_router(tasks.router)

@app.get("/")
async def root():
    return {"message": "Hackathon 2 Backend LIVE ✅"}

# 1. Get all agents status
@app.get("/agents")
async def get_all_agents():
    """
    Get status of all agents in the system
    """
    main_agent_info = {
        "id": main_agent.id,
        "name": main_agent.name,
        "description": main_agent.description,
        "status": main_agent.status,
        "skills": main_agent.skills,
        "active_tasks": 0
    }

    sub_agents_info = []
    for agent_id, agent in main_agent.sub_agents.items():
        sub_agents_info.append({
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "status": agent.status,
            "skills": agent.skills
        })

    return {
        "main_agent": main_agent_info,
        "sub_agents": sub_agents_info
    }

# 2. Get specific agent by ID
@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """
    Get details of a specific agent by ID
    """
    agent = agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "status": agent.status,
        "skills": agent.skills
    }

# 3. Get agent skills
@app.get("/agents/{agent_id}/skills")
async def get_agent_skills(agent_id: str):
    """
    Get skills of a specific agent
    """
    agent = agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "agent_id": agent.id,
        "agent_name": agent.name,
        "skills": agent.skills
    }

# 4. Route task to best agent
@app.post("/agents/route")
async def route_task(content: str = Query(..., description="Task content to route")):
    """
    Route a task to the best matching agent based on skills
    """
    best_agent, confidence = skills_matcher.find_best_agent(content, list(main_agent.sub_agents.values()))

    if best_agent:
        return {
            "task_content": content,
            "best_agent": {
                "id": best_agent.id,
                "name": best_agent.name,
                "description": best_agent.description
            },
            "confidence": confidence,
            "skills_matched": best_agent.skills
        }
    else:
        return {
            "task_content": content,
            "best_agent": None,
            "confidence": 0,
            "message": "No suitable agent found for this task"
        }

# 5. Process task with main agent
@app.post("/agents/process")
async def process_task(content: str = Query(..., description="Task content to process")):
    """
    Process a task using the main agent orchestrator
    """
    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await main_agent.process_request(temp_message)

    return {
        "original_task": content,
        "processed_by": getattr(temp_message, 'agent_used', 'Main Agent'),
        "response": response
    }

# 6. Get all skills in the system
@app.get("/skills")
async def get_all_skills():
    """
    Get all skills across all agents
    """
    all_skills = []

    for agent_id, agent in main_agent.sub_agents.items():
        for skill in agent.skills:
            all_skills.append({
                "agent_id": agent.id,
                "agent_name": agent.name,
                "skill_name": skill,
                "description": f"Skill for handling {skill}-related tasks"
            })

    return {"skills": all_skills}

# 7. Analyze a task
@app.post("/analyze/task")
async def analyze_task(content: str = Query(..., description="Task content to analyze")):
    """
    Analyze a task to determine its category and complexity
    """
    analysis = task_analyzer.analyze_task(content)

    return {
        "task_content": content,
        "analysis": analysis
    }

# 8. Get agent statistics
@app.get("/stats")
async def get_stats():
    """
    Get system statistics
    """
    total_agents = len(main_agent.sub_agents) + 1  # +1 for main agent
    active_agents = sum(1 for agent in main_agent.sub_agents.values() if agent.status == "active")

    return {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "main_agent_status": main_agent.status,
        "total_skills": sum(len(agent.skills) for agent in main_agent.sub_agents.values()),
        "timestamp": datetime.utcnow().isoformat()
    }

# 9. Get agent activity
@app.get("/activity")
async def get_activity():
    """
    Get recent activity in the system
    """
    # This would normally track actual activity
    # For now, returning a mock response
    return {
        "recent_tasks_processed": 0,
        "active_conversations": 0,
        "last_activity": datetime.utcnow().isoformat(),
        "system_uptime": "Just started"
    }

# 10. Health check
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Agent Backend"
    }

# 11. Get conversation history
@app.get("/conversations")
async def get_conversations(limit: int = 10, offset: int = 0):
    """
    Get list of conversations (mock implementation)
    """
    # This would normally fetch from database
    # For now, returning a mock response
    return {
        "conversations": [],
        "total_count": 0,
        "limit": limit,
        "offset": offset
    }

# 12. Get specific conversation
@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get details of a specific conversation (mock implementation)
    """
    return {
        "conversation_id": conversation_id,
        "messages": [],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

# 13. Create new conversation
@app.post("/conversations")
async def create_conversation(title: str = Query(..., description="Title for the new conversation")):
    """
    Create a new conversation (mock implementation)
    """
    conversation_id = str(uuid.uuid4())

    return {
        "conversation_id": conversation_id,
        "title": title,
        "created_at": datetime.utcnow().isoformat()
    }

# 14. Get agent logs
@app.get("/logs/agents/{agent_id}")
async def get_agent_logs(agent_id: str, limit: int = 10):
    """
    Get logs for a specific agent (mock implementation)
    """
    return {
        "agent_id": agent_id,
        "logs": [],
        "limit": limit,
        "total_count": 0
    }

# 15. Get all logs
@app.get("/logs")
async def get_all_logs(limit: int = 10):
    """
    Get system-wide logs (mock implementation)
    """
    return {
        "logs": [],
        "limit": limit,
        "total_count": 0
    }

# 16. Get system config
@app.get("/config")
async def get_config():
    """
    Get system configuration
    """
    return {
        "system_name": "AI Agent Chat System",
        "version": "1.0.0",
        "main_agent_id": main_agent.id,
        "total_sub_agents": len(main_agent.sub_agents),
        "supported_protocols": ["REST", "WebSocket"],
        "database_connected": True
    }

# 17. Get agent types
@app.get("/agents/types")
async def get_agent_types():
    """
    Get different types of agents available
    """
    return {
        "agent_types": [
            {"type": "main", "description": "Main orchestrator agent"},
            {"type": "sub", "description": "Specialized sub-agent"}
        ],
        "total_types": 2
    }

# 18. Get skills by category
@app.get("/skills/categories")
async def get_skills_by_category():
    """
    Get skills organized by categories
    """
    categories = {}

    for agent_id, agent in main_agent.sub_agents.items():
        for skill in agent.skills:
            # Simple categorization based on keywords
            if "frontend" in skill or "ui" in skill or "css" in skill or "html" in skill:
                cat = "frontend"
            elif "backend" in skill or "api" in skill or "server" in skill:
                cat = "backend"
            elif "database" in skill or "sql" in skill or "postgres" in skill:
                cat = "database"
            elif "chat" in skill or "messaging" in skill or "websocket" in skill:
                cat = "communication"
            elif "security" in skill or "auth" in skill or "encrypt" in skill:
                cat = "security"
            elif "test" in skill or "qa" in skill in skill:
                cat = "testing"
            elif "deploy" in skill or "devops" in skill or "docker" in skill:
                cat = "deployment"
            elif "research" in skill or "analyze" in skill or "data" in skill:
                cat = "research"
            else:
                cat = "general"

            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                "skill": skill,
                "agent_id": agent.id,
                "agent_name": agent.name
            })

    return {"categories": categories}

# 19. Get agent workload
@app.get("/agents/{agent_id}/workload")
async def get_agent_workload(agent_id: str):
    """
    Get current workload of an agent (mock implementation)
    """
    agent = agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "agent_id": agent.id,
        "agent_name": agent.name,
        "current_tasks": 0,
        "status": agent.status,
        "estimated_completion": None
    }

# 20. Get system performance
@app.get("/performance")
async def get_performance():
    """
    Get system performance metrics (mock implementation)
    """
    return {
        "response_time_ms": 0,
        "active_connections": 0,
        "cpu_usage_percent": 0,
        "memory_usage_mb": 0,
        "timestamp": datetime.utcnow().isoformat()
    }

# 21. Reset agent status
@app.put("/agents/{agent_id}/status")
async def reset_agent_status(agent_id: str, status: str = Query(..., description="New status for the agent")):
    """
    Update the status of an agent
    """
    agent = agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Validate status
    valid_statuses = ["active", "inactive", "busy"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid statuses: {valid_statuses}")

    agent.status = status

    return {
        "agent_id": agent.id,
        "new_status": status,
        "message": f"Status updated for agent {agent.name}"
    }

# 22. Main agent endpoint - User message → Main Agent
@app.post("/agents/main")
async def process_with_main_agent(content: str = Query(..., description="Content to process by the main agent")):
    """
    Process a user message through the main agent
    """
    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await main_agent.process_request(temp_message)

    return {
        "original_content": content,
        "processed_by": getattr(temp_message, 'agent_used', 'Main Agent'),
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 23. Frontend agent endpoint - Next.js tasks
@app.post("/agents/frontend")
async def process_frontend_task(content: str = Query(..., description="Frontend task content")):
    """
    Process frontend-related tasks (Next.js, UI, etc.)
    """
    # Find the frontend agent
    frontend_agent = None
    for agent in main_agent.sub_agents.values():
        if 'frontend' in agent.skills or 'ui' in agent.skills or 'nextjs' in agent.skills:
            frontend_agent = agent
            break

    if not frontend_agent:
        raise HTTPException(status_code=404, detail="Frontend agent not found")

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'frontend-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await frontend_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": frontend_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 24. Backend agent endpoint - FastAPI tasks
@app.post("/agents/backend")
async def process_backend_task(content: str = Query(..., description="Backend task content")):
    """
    Process backend-related tasks (FastAPI, APIs, etc.)
    """
    # Find the backend agent
    backend_agent = None
    for agent in main_agent.sub_agents.values():
        if 'backend' in agent.skills or 'api' in agent.skills or 'fastapi' in agent.skills:
            backend_agent = agent
            break

    if not backend_agent:
        raise HTTPException(status_code=404, detail="Backend agent not found")

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'backend-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await backend_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": backend_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 25. Database agent endpoint - Neon Postgres tasks
@app.post("/agents/database")
async def process_database_task(content: str = Query(..., description="Database task content")):
    """
    Process database-related tasks (Neon Postgres, queries, etc.)
    """
    # Find the database agent
    database_agent = None
    for agent in main_agent.sub_agents.values():
        if 'database' in agent.skills or 'postgres' in agent.skills or 'sql' in agent.skills:
            database_agent = agent
            break

    if not database_agent:
        raise HTTPException(status_code=404, detail="Database agent not found")

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'database-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await database_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": database_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 26. Chat agent endpoint - WebSocket chat tasks
@app.post("/agents/chat")
async def process_chat_task(content: str = Query(..., description="Chat task content")):
    """
    Process chat-related tasks (WebSocket, messaging, etc.)
    """
    # Find the chat agent
    chat_agent = None
    for agent in main_agent.sub_agents.values():
        if 'chat' in agent.skills or 'websocket' in agent.skills or 'messaging' in agent.skills:
            chat_agent = agent
            break

    if not chat_agent:
        raise HTTPException(status_code=404, detail="Chat agent not found")

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'chat-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await chat_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": chat_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 27. Auth agent endpoint - JWT login tasks
@app.post("/agents/auth")
async def process_auth_task(content: str = Query(..., description="Auth task content")):
    """
    Process authentication-related tasks (JWT, login, etc.)
    """
    # Find the auth agent (likely security or backend agent)
    auth_agent = None
    for agent in main_agent.sub_agents.values():
        if 'auth' in agent.skills or 'authentication' in agent.skills or 'jwt' in agent.skills or 'security' in agent.skills:
            auth_agent = agent
            break

    if not auth_agent:
        raise HTTPException(status_code=404, detail="Auth agent not found")

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'auth-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await auth_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": auth_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 28. DevOps agent endpoint - Railway deploy tasks
@app.post("/agents/devops")
async def process_devops_task(content: str = Query(..., description="DevOps task content")):
    """
    Process DevOps-related tasks (Railway, deployment, etc.)
    """
    # Find the devops agent
    devops_agent = None
    for agent in main_agent.sub_agents.values():
        if 'devops' in agent.skills or 'deployment' in agent.skills or 'docker' in agent.skills or 'railway' in agent.skills:
            devops_agent = agent
            break

    if not devops_agent:
        raise HTTPException(status_code=404, detail="DevOps agent not found")

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'devops-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await devops_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": devops_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 29. Test agent endpoint - Testing tasks
@app.post("/agents/test")
async def process_test_task(content: str = Query(..., description="Test task content")):
    """
    Process testing-related tasks (unit, integration, etc.)
    """
    # Find the testing agent
    test_agent = None
    for agent in main_agent.sub_agents.values():
        if 'test' in agent.skills or 'testing' in agent.skills or 'qa' in agent.skills:
            test_agent = agent
            break

    if not test_agent:
        raise HTTPException(status_code=404, detail="Test agent not found")

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'test-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await test_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": test_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }

# 30. Integration agent endpoint - Full system sync tasks
@app.post("/agents/integration")
async def process_integration_task(content: str = Query(..., description="Integration task content")):
    """
    Process integration-related tasks (full system sync, etc.)
    """
    # Find the integration agent (could be main agent or a specialized one)
    integration_agent = main_agent  # Using main agent for system-wide tasks

    # Create a temporary message object
    temp_message = type('TempMessage', (), {
        'id': str(uuid.uuid4()),
        'conversation_id': str(uuid.uuid4()),
        'sender_type': 'user',
        'sender_id': 'temp-user-id',
        'content': content,
        'message_type': 'integration-task',
        'agent_used': None,
        'timestamp': datetime.utcnow()
    })()

    response = await integration_agent.process_request(temp_message)

    return {
        "task_content": content,
        "processed_by": integration_agent.name,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }