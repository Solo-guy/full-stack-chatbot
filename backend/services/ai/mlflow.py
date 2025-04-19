import requests

# MLflow API
MLFLOW_URL = "http://localhost:5000"

def manage_mlflow(action: str, params: dict) -> dict:
    """
    Manage MLflow operations (e.g., update experiment, log metrics).
    """
    try:
        if action == "update_experiment":
            # Cập nhật experiment
            response = requests.post(
                f"{MLFLOW_URL}/api/2.0/mlflow/experiments/update",
                json={
                    "experiment_id": params.get("experiment_id"),
                    "name": params.get("experiment_name"),
                    "params": params.get("params", {})
                }
            )
            if response.status_code != 200:
                return {"error": f"Update experiment failed: {response.text}"}
            return {"message": f"Experiment {params.get('experiment_id')} updated"}

        elif action == "log_metrics":
            # Ghi metrics
            response = requests.post(
                f"{MLFLOW_URL}/api/2.0/mlflow/runs/log-metric",
                json={
                    "run_id": params.get("run_id"),
                    "key": params.get("metric_key"),
                    "value": params.get("metric_value")
                }
            )
            if response.status_code != 200:
                return {"error": f"Log metrics failed: {response.text}"}
            return {"message": f"Metric {params.get('metric_key')} logged"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}