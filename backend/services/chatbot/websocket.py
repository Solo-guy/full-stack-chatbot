from fastapi import WebSocket
from .crewai import process_query

async def handle_websocket(websocket: WebSocket, token: str):
    """
    Handle WebSocket connection for real-time chatbot interaction.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("text", "")
            model = data.get("model", "MiniCPM")
            response = process_query(query, model)
            await websocket.send_json({"response": response})
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()