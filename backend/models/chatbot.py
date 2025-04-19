from pydantic import BaseModel

class ChatbotQuery(BaseModel):
    text: str
    model: str = "MiniCPM"

class ChatbotResponse(BaseModel):
    response: str