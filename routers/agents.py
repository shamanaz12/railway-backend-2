from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

# Additional agent-specific endpoints can be added here
# The main agent functionality is available through the main.py endpoints