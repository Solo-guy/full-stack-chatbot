import requests

# Loki API
LOKI_URL = "http://localhost:3100"

def fetch_loki_logs(filter: str) -> dict:
    """
    Fetch logs from Loki.
    """
    try:
        response = requests.get(
            f"{LOKI_URL}/loki/api/v1/query_range",
            params={"query": filter, "limit": 100}
        )
        if response.status_code != 200:
            return {"error": f"Fetch logs failed: {response.text}"}
        return {"logs": response.json().get("data", {}).get("result", [])}
    except Exception as e:
        return {"error": str(e)}