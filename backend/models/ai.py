from pydantic import BaseModel
from typing import Dict

class ModelConfig(BaseModel):
    model_id: str
    model_name: str
    params: Dict
    wandb_key: str

class TrainingConfig(BaseModel):
    model_id: str
    dataset: str