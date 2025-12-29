"""
WebSocket Streaming Pattern for Real-Time Agent Updates
========================================================

Demonstrates streaming Claude responses to frontend via WebSocket.
This pattern is used in production for ADEV Dashboard real-time updates.

Pattern Benefits:
- Real-time user feedback (no waiting for complete response)
- Better UX (users see thinking process)
- Efficient (stream tokens as generated)
- Cancellable (can abort long responses)

NOTE: This is a sanitized example showing the pattern, not production code.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from anthropic import Anthropic
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WebSocket Streaming Agent API")

# CORS configuration (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
client = Anthropic()


class ConnectionManager:
    """
    Manages active WebSocket connections.

    Responsibilities:
    - Track active connections
    - Broadcast messages
    - Handle disconnections
    """

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept and register new connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, client_id: str):
        """Remove connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_message(self, client_id: str, message: Dict[str, Any]):
        """Send JSON message to specific client."""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_json(message)

    async def broadcast(self, message: Dict[str, Any]):
        """Send message to all connected clients."""
        disconnected = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected:
            self.disconnect(client_id)


manager = ConnectionManager()


@app.websocket("/ws/agent/{client_id}")
async def agent_websocket(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for streaming agent responses.

    Message format (client -> server):
    {
        "type": "message",
        "content": "User message text",
        "context": {}  // Optional context
    }

    Message format (server -> client):
    {
        "type": "content_delta",
        "content": "Streamed text chunk"
    }
    {
        "type": "tool_use",
        "tool": "tool_name",
        "input": {...}
    }
    {
        "type": "message_complete",
        "usage": {...}
    }
    {
        "type": "error",
        "error": "Error message"
    }
    """
    await manager.connect(websocket, client_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data["type"] == "message":
                await stream_agent_response(
                    websocket,
                    client_id,
                    message_data["content"],
                    message_data.get("context")
                )

            elif message_data["type"] == "ping":
                # Keep-alive ping
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected normally")

    except Exception as e:
        logger.error(f"Error in websocket for {client_id}: {e}")
        manager.disconnect(client_id)
        try:
            await websocket.send_json({
                "type": "error",
                "error": str(e)
            })
        except:
            pass


async def stream_agent_response(
    websocket: WebSocket,
    client_id: str,
    user_message: str,
    context: Optional[Dict] = None
):
    """
    Stream Claude response to client in real-time.

    Handles:
    - Text streaming (delta updates)
    - Tool usage notifications
    - Completion metadata
    - Error handling
    """
    try:
        # Prepare messages
        messages = [{"role": "user", "content": user_message}]

        # Add context to system prompt if provided
        system_prompt = "You are a helpful AI assistant."
        if context:
            context_str = json.dumps(context, indent=2)
            system_prompt += f"\n\nContext:\n{context_str}"

        # Send start indicator
        await websocket.send_json({
            "type": "message_start",
            "timestamp": datetime.utcnow().isoformat()
        })

        # Stream response
        with client.messages.stream(
            model="claude-sonnet-4",
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            # tools=[]  # Add tools if needed
        ) as stream:

            # Stream text deltas
            for text in stream.text_stream:
                await websocket.send_json({
                    "type": "content_delta",
                    "content": text
                })

                # Small delay to prevent overwhelming client
                # (adjust based on your needs)
                await asyncio.sleep(0.01)

            # Get final message
            final_message = stream.get_final_message()

            # Send completion
            await websocket.send_json({
                "type": "message_complete",
                "usage": {
                    "input_tokens": final_message.usage.input_tokens,
                    "output_tokens": final_message.usage.output_tokens
                },
                "timestamp": datetime.utcnow().isoformat()
            })

    except Exception as e:
        logger.error(f"Error streaming response for {client_id}: {e}")
        await websocket.send_json({
            "type": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })


@app.websocket("/ws/agent-with-tools/{client_id}")
async def agent_with_tools_websocket(websocket: WebSocket, client_id: str):
    """
    Enhanced WebSocket endpoint with tool usage support.

    Demonstrates how to stream tool calls and results.
    """
    await manager.connect(websocket, client_id)

    # Example tools
    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        },
        {
            "name": "search_database",
            "description": "Search a database for information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "number"}
                },
                "required": ["query"]
            }
        }
    ]

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data["type"] == "message":
                messages = [{"role": "user", "content": message_data["content"]}]

                # Stream with tools
                with client.messages.stream(
                    model="claude-sonnet-4",
                    max_tokens=4096,
                    messages=messages,
                    tools=tools
                ) as stream:

                    current_tool_use = None

                    for event in stream:
                        # Handle different event types
                        if event.type == "content_block_start":
                            if hasattr(event.content_block, "type"):
                                if event.content_block.type == "tool_use":
                                    # Tool use started
                                    current_tool_use = {
                                        "id": event.content_block.id,
                                        "name": event.content_block.name,
                                        "input": {}
                                    }
                                    await websocket.send_json({
                                        "type": "tool_use_start",
                                        "tool": event.content_block.name
                                    })

                        elif event.type == "content_block_delta":
                            if hasattr(event.delta, "type"):
                                if event.delta.type == "text_delta":
                                    # Stream text
                                    await websocket.send_json({
                                        "type": "content_delta",
                                        "content": event.delta.text
                                    })
                                elif event.delta.type == "input_json_delta":
                                    # Tool input being built
                                    if current_tool_use:
                                        # Update tool input
                                        pass

                        elif event.type == "content_block_stop":
                            if current_tool_use:
                                # Tool use complete
                                await websocket.send_json({
                                    "type": "tool_use_complete",
                                    "tool": current_tool_use["name"],
                                    "input": current_tool_use["input"]
                                })
                                current_tool_use = None

                    # Send completion
                    final_message = stream.get_final_message()
                    await websocket.send_json({
                        "type": "message_complete",
                        "usage": {
                            "input_tokens": final_message.usage.input_tokens,
                            "output_tokens": final_message.usage.output_tokens
                        }
                    })

    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"Error in tool websocket for {client_id}: {e}")
        manager.disconnect(client_id)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections),
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================
# Production Considerations
# ============================================

"""
For production deployment, add:

1. Authentication:
   - API key validation
   - JWT token verification
   - Rate limiting per user

2. Error Handling:
   - Retry logic for API failures
   - Graceful degradation
   - Proper error messages

3. Monitoring:
   - Connection metrics
   - Response times
   - Error rates
   - Token usage tracking

4. Security:
   - Input validation
   - Output sanitization
   - CORS configuration
   - SSL/TLS encryption

5. Scalability:
   - Connection pooling
   - Load balancing
   - Horizontal scaling
   - Redis for session management

Example authentication middleware:

from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.websocket("/ws/agent/{client_id}")
async def agent_websocket(
    websocket: WebSocket,
    client_id: str,
    api_key: str = Depends(verify_api_key)  # Add authentication
):
    # ... rest of implementation
"""


if __name__ == "__main__":
    import uvicorn

    print("WebSocket Streaming Agent API")
    print("=" * 50)
    print("Endpoints:")
    print("  - ws://localhost:8000/ws/agent/{client_id}")
    print("  - ws://localhost:8000/ws/agent-with-tools/{client_id}")
    print("  - http://localhost:8000/health")
    print()
    print("NOTE: Requires ANTHROPIC_API_KEY environment variable")
    print()

    # Run server
    uvicorn.run(app, host="0.0.0.0", port=8000)
