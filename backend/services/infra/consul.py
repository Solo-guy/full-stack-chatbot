import requests

# Consul API
CONSUL_API = "http://localhost:8500/v1"

def manage_consul(action: str, params: dict) -> dict:
    """
    Manage Consul operations (e.g., service discovery, configuration).
    """
    try:
        if action == "register_service":
            # Đăng ký dịch vụ
            service_data = {
                "ID": params.get("service_id"),
                "Name": params.get("service_name"),
                "Address": params.get("address"),
                "Port": params.get("port")
            }
            response = requests.put(
                f"{CONSUL_API}/agent/service/register",
                json=service_data
            )
            if response.status_code != 200:
                return {"error": f"Register service failed: {response.text}"}
            return {"message": f"Service {params.get('service_name')} registered"}

        elif action == "discover_service":
            # Khám phá dịch vụ
            response = requests.get(
                f"{CONSUL_API}/catalog/service/{params.get('service_name')}"
            )
            if response.status_code != 200:
                return {"error": f"Discover service failed: {response.text}"}
            return {"services": response.json()}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}