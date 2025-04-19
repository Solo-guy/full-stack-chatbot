import requests

# Kubeflow API
KUBEFLOW_URL = "http://localhost:8080"

def manage_kubeflow(action: str, params: dict) -> dict:
    """
    Manage Kubeflow operations (e.g., run pipeline).
    """
    try:
        if action == "run_pipeline":
            # Chạy pipeline huấn luyện
            response = requests.post(
                f"{KUBEFLOW_URL}/pipeline/run",
                json={
                    "model_id": params.get("model_id"),
                    "dataset": params.get("dataset")
                }
            )
            if response.status_code != 200:
                return {"error": f"Run pipeline failed: {response.text}"}
            return {"pipeline_id": response.json().get("pipeline_id")}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}