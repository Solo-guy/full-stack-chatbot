from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..models.ai import ModelConfig, TrainingConfig
from ..utils.auth import verify_jwt
import requests

router = APIRouter()

# Service URLs
MLFLOW_URL = "http://localhost:5000"
KUBEFLOW_URL = "http://localhost:8080"
WANDB_URL = "https://api.wandb.ai"
DVC_URL = "http://localhost:8081"
OPTUNA_URL = "http://localhost:8082"

@router.post("/adjust-model", response_model=dict)
async def adjust_model(config: ModelConfig, token: str = Depends(verify_jwt)):
    """
    Adjust model parameters (e.g., learning rate).
    """
    try:
        # Update MLflow experiment
        mlflow_response = requests.post(
            f"{MLFLOW_URL}/api/2.0/mlflow/experiments/update",
            json={"experiment_id": config.model_id, "params": config.params}
        )
        if mlflow_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to update MLflow experiment")

        # Update Weights & Biases
        wandb_response = requests.post(
            f"{WANDB_URL}/runs/{config.model_id}",
            json={"params": config.params},
            headers={"Authorization": f"Bearer {config.wandb_key}"}
        )

        return {"message": f"Model {config.model_name} adjusted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitor-model", response_model=dict)
async def monitor_model(model_id: str, token: str = Depends(verify_jwt)):
    """
    Monitor model performance (accuracy, loss).
    """
    try:
        # Fetch from Weights & Biases
        wandb_response = requests.get(
            f"{WANDB_URL}/runs/{model_id}/metrics",
            headers={"Authorization": f"Bearer {token}"}
        )
        metrics = wandb_response.json()

        # Fetch from MLflow
        mlflow_response = requests.get(
            f"{MLFLOW_URL}/api/2.0/mlflow/runs/{model_id}"
        )
        run_data = mlflow_response.json()

        return {"metrics": metrics, "run_data": run_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train", response_model=dict)
async def train_model(config: TrainingConfig, token: str = Depends(verify_jwt)):
    """
    Train a model using Kubeflow pipeline.
    """
    try:
        # Start Kubeflow pipeline
        kubeflow_response = requests.post(
            f"{KUBEFLOW_URL}/pipeline/run",
            json={"model_id": config.model_id, "dataset": config.dataset}
        )
        if kubeflow_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to start Kubeflow pipeline")

        # Update DVC for data versioning
        dvc_response = requests.post(
            f"{DVC_URL}/data/version",
            json={"dataset": config.dataset}
        )

        # Optimize hyperparameters with Optuna
        optuna_response = requests.post(
            f"{OPTUNA_URL}/study",
            json={"model_id": config.model_id}
        )

        return {"message": f"Training started for model {config.model_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))