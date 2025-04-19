import requests

# GitLab API
GITLAB_API = "https://gitlab.com/api/v4"

def manage_gitlab(action: str, params: dict) -> dict:
    """
    Manage GitLab operations (e.g., trigger CI/CD, check repository).
    """
    try:
        headers = {"Private-Token": params.get("access_token")}

        if action == "trigger_pipeline":
            # Kích hoạt pipeline CI/CD
            response = requests.post(
                f"{GITLAB_API}/projects/{params.get('project_id')}/pipeline",
                headers=headers
            )
            if response.status_code != 201:
                return {"error": f"Trigger pipeline failed: {response.text}"}
            return {"pipeline_id": response.json().get("id")}

        elif action == "check_repository":
            # Kiểm tra repository
            response = requests.get(
                f"{GITLAB_API}/projects/{params.get('project_id')}",
                headers=headers
            )
            if response.status_code != 200:
                return {"error": f"Check repository failed: {response.text}"}
            return {"repository": response.json().get("name")}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}