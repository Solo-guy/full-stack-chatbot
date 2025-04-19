from pydantic import BaseModel
from typing import Dict

class InfraCommand(BaseModel):
    service: str
    action: str
    params: Dict