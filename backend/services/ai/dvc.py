import subprocess

def manage_dvc(action: str, params: dict) -> dict:
    """
    Manage DVC operations (e.g., version dataset).
    """
    try:
        if action == "version_dataset":
            # Phiên bản dataset
            dataset = params.get("dataset")
            result = subprocess.run(
                ["dvc", "add", dataset],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return {"error": f"Version dataset failed: {result.stderr}"}
            subprocess.run(["dvc", "push"], capture_output=True)
            return {"message": f"Dataset {dataset} versioned"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}