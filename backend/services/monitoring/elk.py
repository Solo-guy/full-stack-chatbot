import requests

# Elasticsearch API
ELK_URL = "http://localhost:9200"

def fetch_elk_logs(index: str, filter: str) -> dict:
    """
    Fetch logs from ELK Stack.
    """
    try:
        response = requests.get(
            f"{ELK_URL}/{index}/_search",
            json={"query": {"match": {"message": filter}}}
        )
        if response.status_code != 200:
            return {"error": f"Fetch logs failed: {response.text}"}
        return {"logs": response.json().get('hits', {}).get('hits', [])}
    except Exception as e:
        return {"error": str(e)}