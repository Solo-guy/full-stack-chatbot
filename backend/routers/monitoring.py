from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..models.monitoring import MetricsQuery, LogQuery, ErrorQuery
from ..utils.auth import verify_jwt
import requests

router = APIRouter()

# Service URLs
PROMETHEUS_URL = "http://localhost:9090/api/v1"
ELK_URL = "http://localhost:9200"
SENTRY_URL = "http://localhost:9000/api"
PAGERDUTY_URL = "https://api.pagerduty.com"
MOOGSOFT_URL = "https://api.moogsoft.ai"
LOKI_URL = "http://localhost:3100"

@router.post("/monitor-metrics", response_model=dict)
async def monitor_metrics(query: MetricsQuery, token: str = Depends(verify_jwt)):
    """
    Fetch metrics from Prometheus.
    """
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/query",
            params={"query": query.metric, "time": query.timeframe}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch Prometheus metrics")

        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitor-logs", response_model=dict)
async def monitor_logs(query: LogQuery, token: str = Depends(verify_jwt)):
    """
    Fetch logs from ELK Stack and Loki.
    """
    try:
        # Fetch from ELK Stack
        elk_response = requests.get(
            f"{ELK_URL}/{query.index}/_search",
            json={"query": {"match": {"message": query.filter}}}
        )
        elk_logs = elk_response.json().get('hits', {}).get('hits', [])

        # Fetch from Loki
        loki_response = requests.get(
            f"{LOKI_URL}/loki/api/v1/query_range",
            params={"query": query.filter, "limit": 100}
        )
        loki_logs = loki_response.json().get('data', {}).get('result', [])

        return {"elk_logs": elk_logs, "loki_logs": loki_logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitor-errors", response_model=dict)
async def monitor_errors(query: ErrorQuery, token: str = Depends(verify_jwt)):
    """
    Fetch errors from Sentry and send alerts via PagerDuty/Moogsoft.
    """
    try:
        # Fetch from Sentry
        sentry_response = requests.get(
            f"{SENTRY_URL}/projects/{query.project}/issues",
            headers={"Authorization": f"Bearer {query.api_key}"}
        )
        errors = sentry_response.json()

        # Send alert to PagerDuty
        pagerduty_data = {
            "routing_key": query.pagerduty_key,
            "event_action": "trigger",
            "payload": {
                "summary": f"Error in {query.project}",
                "severity": "critical",
                "source": "Sentry"
            }
        }
        requests.post(f"{PAGERDUTY_URL}/events", json=pagerduty_data)

        # Send alert to Moogsoft
        moogsoft_data = {
            "source": query.project,
            "description": f"Error detected: {errors[0]['title']}",
            "severity": 5
        }
        requests.post(f"{MOOGSOFT_URL}/events", json=moogsoft_data)

        return {"errors": errors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))