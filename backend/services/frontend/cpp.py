import requests

# APIsix gateway
APISIX_URL = "http://localhost:9080/admin"

def configure_cpp(settings: dict) -> dict:
    """
    Configure C++ frontend settings (UI components).
    """
    try:
        # Cập nhật route APIsix cho C++
        route_data = {
            "uri": "/cpp/*",
            "upstream": {
                "nodes": [{"host": settings.get("url", "localhost"), "port": 80, "weight": 1}]
            }
        }
        response = requests.post(
            f"{APISIX_URL}/routes",
            json=route_data
        )
        if response.status_code != 201:
            return {"error": f"Failed to update APIsix route: {response.text}"}

        # Lưu settings (giả lập, có thể lưu vào PostgreSQL)
        return {"message": "C++ frontend configured successfully", "settings": settings}
    except Exception as e:
        return {"error": str(e)}