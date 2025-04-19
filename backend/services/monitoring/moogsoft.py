import requests

# Moogsoft API
MOOGSOFT_URL = "https://api.moogsoft.ai"

def send_moogsoft_alert(source: str, description: str) -> dict:
    """
    Send alert to Moogsoft for AIOps analysis.
    """
    try:
        data = {
            "source": source,
            "description": description,
            "severity": 5
        }
        response = requests.post(
            f"{MOOGSOFT_URL}/events",
            json=data
        )
        if response.status_code != 200:
            return {"error": f"Send alert failed: {response.text}"}
        return {"message": "Alert sent to Moogsoft"}
    except Exception as e:
        return {"error": str(e)}