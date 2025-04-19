# Chatbot router for handling chatbot interactions
from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import JSONResponse
from ..models.chatbot import ChatbotQuery, ChatbotResponse
from ..services.chatbot.crewai import process_query
from ..services.chatbot.websocket import handle_websocket
from ..utils.auth import verify_jwt

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(verify_jwt)):
    await handle_websocket(websocket, token)

@router.post("/ask", response_model=ChatbotResponse)
async def ask_query(query: ChatbotQuery, token: str = Depends(verify_jwt)):
    response = await process_query(query.text, query.model)
    return ChatbotResponse(response=response)

@router.get("/models")
async def get_models(token: str = Depends(verify_jwt)):
    return {
        "models": [
            {"name": "MiniCPM", "version": "2.4B", "capabilities": "Chatbot management"},
            {"name": "Grok", "version": "3.0", "capabilities": "Complex analysis"},
            {"name": "DeepSeek", "version": "1.0", "capabilities": "General purpose"},
            {"name": "OpenAI", "version": "GPT-4", "capabilities": "Advanced NLP"}
        ]
    }

@router.post("/forms")
async def render_form(form_data: dict, token: str = Depends(verify_jwt)):
    # Logic to render dynamic forms from JSON schema
    return {"form": form_data}

@router.post("/workflow")
async def manage_workflow(workflow_data: dict, token: str = Depends(verify_jwt)):
    # Logic for workflow engine (flowchart, undo/redo)
    return {"workflow": workflow_data}

@router.post("/tracker")
async def track_progress(tracker_data: dict, token: str = Depends(verify_jwt)):
    # Logic for progress tracker (Gantt chart, ETA)
    return {"tracker": tracker_data}

@router.post("/datatools")
async def data_tools(data: dict, token: str = Depends(verify_jwt)):
    # Logic for data tables, charts, export
    return {"data": data}