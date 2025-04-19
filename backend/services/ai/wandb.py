import requests

# Weights & Biases API
WANDB_URL = "https://api.wandb.ai"

def manage_wandb(action: str, params: dict) -> dict:
    """
    Manage Weights & Biases operations (e.g., log metrics).
    """
    try:
        headers = {"Authorization": f"Bearer {params.get('api_key')}"}

        if action == "log_metrics":
            # Ghi metrics
            response = requests.post(
                f"{WANDB_URL}/runs/{params.get('run_id')}",
                json={"metrics": params.get("metrics")},
                headers=headers
            )
            if response.status_code != 200:
                return {"error": f"Log metrics failed: {response.text}"}
            return {"message": f"Metrics logged for run {params.get('run_id')}"}

        elif action == "get_metrics":
            # Lấy metrics
            response = requests.get(
                f"{WANDB_URL}/runs/{params.get('run_id')}/metrics",
                headers=headers
            )
            if response.status_code != 200:
                return {"error": f"Get metrics failed: {response.text}"}
            return {"metrics": response.json()}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}