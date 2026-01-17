from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agents.main_agent import main_agent
import json
import uuid
from datetime import datetime

router = APIRouter(tags=["websocket"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat communication
    """
    await websocket.accept()

    try:
        # Send connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "Main Agent Connected!",
            "timestamp": datetime.utcnow().isoformat()
        }))

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process the message through the agent system
            # Create a temporary message object
            temp_message = type('TempMessage', (), {
                'id': str(uuid.uuid4()),
                'conversation_id': str(uuid.uuid4()),  # Generate a new conversation ID for each session
                'sender_type': message_data.get('sender_type', 'user'),
                'sender_id': message_data.get('sender_id', 'temp-user-id'),
                'content': message_data.get('content', data),
                'message_type': message_data.get('message_type', 'text'),
                'agent_used': None,
                'timestamp': datetime.utcnow()
            })()

            # Process through main agent
            response_content = await main_agent.process_request(temp_message)

            # Send response back to client
            response = {
                "type": "response",
                "content": response_content,
                "message_id": str(uuid.uuid4()),
                "agent_used": getattr(temp_message, 'agent_used', 'Main Agent'),
                "timestamp": datetime.utcnow().isoformat()
            }

            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        error_response = {
            "type": "error",
            "content": f"An error occurred: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
        await websocket.send_text(json.dumps(error_response))