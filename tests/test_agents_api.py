import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the backend directory to the path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from main import app

client = TestClient(app)

def test_get_all_agents():
    """Test the GET /agents endpoint"""
    response = client.get("/agents")
    assert response.status_code == 200
    
    data = response.json()
    assert "main_agent" in data
    assert "sub_agents" in data
    assert isinstance(data["sub_agents"], list)
    assert len(data["sub_agents"]) == 8  # Expecting 8 sub-agents


def test_get_specific_agent():
    """Test the GET /agents/{agent_id} endpoint"""
    # First get all agents to find a valid agent ID
    agents_response = client.get("/agents")
    agents_data = agents_response.json()
    
    # Use the first sub-agent's ID for testing
    if agents_data["sub_agents"]:
        agent_id = agents_data["sub_agents"][0]["id"]
        response = client.get(f"/agents/{agent_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert data["id"] == agent_id


def test_get_agent_skills():
    """Test the GET /agents/{agent_id}/skills endpoint"""
    # First get all agents to find a valid agent ID
    agents_response = client.get("/agents")
    agents_data = agents_response.json()
    
    # Use the first sub-agent's ID for testing
    if agents_data["sub_agents"]:
        agent_id = agents_data["sub_agents"][0]["id"]
        response = client.get(f"/agents/{agent_id}/skills")
        assert response.status_code == 200
        
        data = response.json()
        assert "agent_id" in data
        assert data["agent_id"] == agent_id
        assert "skills" in data
        assert isinstance(data["skills"], list)


def test_route_task():
    """Test the POST /agents/route endpoint"""
    response = client.post("/agents/route?content=How do I center a div in CSS?")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "best_agent" in data


def test_process_task():
    """Test the POST /agents/process endpoint"""
    response = client.post("/agents/process?content=How do I create a React component?")
    assert response.status_code == 200
    
    data = response.json()
    assert "original_task" in data
    assert "processed_by" in data
    assert "response" in data


def test_get_all_skills():
    """Test the GET /skills endpoint"""
    response = client.get("/skills")
    assert response.status_code == 200
    
    data = response.json()
    assert "skills" in data
    assert isinstance(data["skills"], list)


def test_analyze_task():
    """Test the POST /analyze/task endpoint"""
    response = client.post("/analyze/task?content=How do I implement authentication in my app?")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "analysis" in data
    assert "category" in data["analysis"]


def test_get_stats():
    """Test the GET /stats endpoint"""
    response = client.get("/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_agents" in data
    assert "active_agents" in data
    assert "main_agent_status" in data


def test_health_check():
    """Test the GET /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_get_config():
    """Test the GET /config endpoint"""
    response = client.get("/config")
    assert response.status_code == 200
    
    data = response.json()
    assert "system_name" in data
    assert "version" in data


def test_get_skills_by_category():
    """Test the GET /skills/categories endpoint"""
    response = client.get("/skills/categories")
    assert response.status_code == 200
    
    data = response.json()
    assert "categories" in data


def test_reset_agent_status():
    """Test the PUT /agents/{agent_id}/status endpoint"""
    # First get all agents to find a valid agent ID
    agents_response = client.get("/agents")
    agents_data = agents_response.json()
    
    # Use the first sub-agent's ID for testing
    if agents_data["sub_agents"]:
        agent_id = agents_data["sub_agents"][0]["id"]
        response = client.put(f"/agents/{agent_id}/status?status=busy")
        assert response.status_code == 200
        
        data = response.json()
        assert "agent_id" in data
        assert data["agent_id"] == agent_id
        assert data["new_status"] == "busy"


def test_process_with_main_agent():
    """Test the POST /agents/main endpoint"""
    response = client.post("/agents/main?content=How do I center a div in CSS?")
    assert response.status_code == 200
    
    data = response.json()
    assert "original_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_frontend_task():
    """Test the POST /agents/frontend endpoint"""
    response = client.post("/agents/frontend?content=How do I implement server-side rendering in Next.js?")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_backend_task():
    """Test the POST /agents/backend endpoint"""
    response = client.post("/agents/backend?content=How do I create a CRUD endpoint in FastAPI?")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_database_task():
    """Test the POST /agents/database endpoint"""
    response = client.post("/agents/database?content=Write a query to join users and orders tables")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_chat_task():
    """Test the POST /agents/chat endpoint"""
    response = client.post("/agents/chat?content=How do I implement real-time notifications?")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_auth_task():
    """Test the POST /agents/auth endpoint"""
    response = client.post("/agents/auth?content=Implement JWT authentication in FastAPI")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_devops_task():
    """Test the POST /agents/devops endpoint"""
    response = client.post("/agents/devops?content=How do I deploy a FastAPI app to Railway?")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_test_task():
    """Test the POST /agents/test endpoint"""
    response = client.post("/agents/test?content=Write a unit test for a FastAPI endpoint")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data


def test_process_integration_task():
    """Test the POST /agents/integration endpoint"""
    response = client.post("/agents/integration?content=How do I integrate frontend and backend?")
    assert response.status_code == 200
    
    data = response.json()
    assert "task_content" in data
    assert "processed_by" in data
    assert "response" in data