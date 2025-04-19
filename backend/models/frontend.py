from pydantic import BaseModel
from typing import Dict

class FrontendConfig(BaseModel):
    platform: str
    url: str
    settings: Dict = {}