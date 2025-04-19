import requests

# MiniCPM server
MINICPM_URL = "http://localhost:8001"

def manage_minicpm(action: str, params: dict) -> dict:
    """
    Manage MiniCPM operations (e.g., run inference).
    """
    try:
        if action == "run_inference":
            # Gọi server MiniCPM
            response = requests.post(
                f"{MINICPM_URL}/inference",
                json={"text": params.get("text")}
            )
            if response.status_code != 200:
                return {"error": f"MiniCPM inference failed: {response.text}"}
            return {"response": response.json().get("response")}

        elif action == "monitor":
            # Giả lập theo dõi hiệu suất
            return {"metrics": {"vram_usage": "4GB", "inference_time": "0.5s"}}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}