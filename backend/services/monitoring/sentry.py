import requests

# Sentry API
SENTRY_URL = "http://localhost:9000/api"

def fetch_sentry_errors(project: str, api_key: str) -> dict:
    """
    Fetch errors from Sentry.
    """
    try:
        response = requests.get(
            f"{SENTRY_URL}/projects/{project}/issues",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code != 200:
            return {"error": f"Fetch errors failed: {response.text}"}
        return {"errors": response.json()}
    except Exception as e:
        return {"error": str(e)}