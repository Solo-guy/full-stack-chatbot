import requests

# Traefik API
TRAFIK_API = "http://localhost:8081/api"

def manage_traefik(action: str, params: dict) -> dict:
    """
    Manage Traefik operations (e.g., configure service mesh).
    """
    try:
        if action == "add_route":
            # Thêm route
            response = requests.post(
                f"{TRAFIK_API}/http/routers",
                json={
                    "rule": params.get("rule"),
                    "service": params.get("service"),
                    "entryPoints": ["web"]
                }
            )
            if response.status_code != 201:
                return {"error": f"Add route failed: {response.text}"}
            return {"message": f"Route added for {params.get('service')}"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}