from pydantic import BaseModel
from typing import Dict, Optional

class KnowledgeInput(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    metadata: Dict = {}