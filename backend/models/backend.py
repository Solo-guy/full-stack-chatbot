from pydantic import BaseModel
from typing import List, Dict

class BackendConfig(BaseModel):
    name: str
    url: str
    api_key: str = None

class BackendStatus(BaseModel):
    name: str
    status: str
    message_count: int
    metrics: List[Dict]