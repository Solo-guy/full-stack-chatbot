import requests

# PagerDuty API
PAGERDUTY_URL = "https://api.pagerduty.com"

def send_pagerduty_alert(routing_key: str, summary: str) -> dict:
    """
    Send alert to PagerDuty.
    """
    try:
        data = {
            "routing_key": routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": summary,
                "severity": "critical",
                "source": "AdminSystem"
            }
        }
        response = requests.post(
            f"{PAGERDUTY_URL}/events",
            json=data
        )
        if response.status_code != 202:
            return {"error": f"Send alert failed: {response.text}"}
        return {"message": "Alert sent to PagerDuty"}
    except Exception as e:
        return {"error": str(e)}