import requests

# Grafana API
GRAFANA_API = "http://localhost:3001/api"

def manage_grafana(action: str, params: dict) -> dict:
    """
    Manage Grafana operations (e.g., create dashboard).
    """
    try:
        headers = {"Authorization": f"Bearer {params.get('api_key')}"}

        if action == "create_dashboard":
            dashboard_data = {
                "dashboard": {
                    "id": null,
                    "uid": params.get("uid"),
                    "title": params.get("title"),
                    "panels": params.get("panels", [])
                }
            }
            response = requests.post(
                f"{GRAFANA_API}/dashboards/db",
                json=dashboard_data,
                headers=headers
            )
            if response.status_code != 200:
                return {"error": f"Create dashboard failed: {response.text}"}
            return {"dashboard_id": response.json().get("id")}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}