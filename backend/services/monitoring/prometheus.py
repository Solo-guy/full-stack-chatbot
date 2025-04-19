import requests

# Prometheus API
PROMETHEUS_URL = "http://localhost:9090/api/v1"

def fetch_prometheus_metrics(metric: str, timeframe: str) -> dict:
    """
    Fetch metrics from Prometheus.
    """
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/query",
            params={"query": metric, "time": timeframe}
        )
        if response.status_code != 200:
            return {"error": f"Fetch metrics failed: {response.text}"}
        return {"metrics": response.json().get("data", {}).get("result", [])}
    except Exception as e:
        return {"error": str(e)}