import requests

# Dynatrace API
DYNATRACE_API = "https://your-dynatrace-instance.live.dynatrace.com/api/v2"

def manage_dynatrace(action: str, params: dict) -> dict:
    """
    Manage Dynatrace operations (e.g., monitor AIOps, auto-remediate).
    """
    try:
        headers = {"Authorization": f"Api-Token {params.get('api_token')}"}

        if action == "get_metrics":
            # Lấy metrics
            response = requests.get(
                f"{DYNATRACE_API}/metrics/query",
                params={"metricSelector": params.get("metric")},
                headers=headers
            )
            if response.status_code != 200:
                return {"error": f"Get metrics failed: {response.text}"}
            return {"metrics": response.json().get("result")}

        elif action == "trigger_remediation":
            # Kích hoạt sửa lỗi tự động
            response = requests.post(
                f"{DYNATRACE_API}/problems/remediate",
                json={"problem_id": params.get("problem_id")},
                headers=headers
            )
            if response.status_code != 200:
                return {"error": f"Trigger remediation failed: {response.text}"}
            return {"message": f"Remediation triggered for problem {params.get('problem_id')}"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}