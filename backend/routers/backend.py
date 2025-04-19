from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..models.backend import BackendConfig, BackendStatus
from ..utils.auth import verify_jwt
from ..utils.db import get_cockroach_session, get_scylla_session
from kafka import KafkaProducer
import requests
import json

router = APIRouter()

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# APIsix admin API
APISIX_ADMIN_URL = "http://localhost:9080/admin"

@router.post("/add-backend", response_model=dict)
async def add_backend(config: BackendConfig, token: str = Depends(verify_jwt)):
    """
    Add a new backend (e.g., sales, healthcare) to FastAPI module.
    """
    try:
        # Validate backend config
        if config.name not in ['sales', 'healthcare', 'education', 'chat']:
            raise HTTPException(status_code=400, detail="Invalid backend name")

        # Create router file (simulated)
        router_content = f"""
from fastapi import APIRouter
router = APIRouter()
@router.get("/{config.name}/status")
async def get_status():
    return {{"status": "active", "name": "{config.name}"}}
"""
        with open(f"src/fastapi/routers/{config.name}.py", "w") as f:
            f.write(router_content)

        # Create service file (simulated)
        service_content = f"""
def manage_{config.name}():
    return {{"status": "active", "name": "{config.name}"}}
"""
        with open(f"src/fastapi/services/backend/{config.name}.py", "w") as f:
            f.write(service_content)

        # Update APIsix route
        route_data = {
            "uri": f"/{config.name}/*",
            "upstream": {
                "nodes": [{"host": config.url, "port": 80, "weight": 1}]
            }
        }
        response = requests.post(
            f"{APISIX_ADMIN_URL}/routes",
            json=route_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 201:
            raise HTTPException(status_code=500, detail="Failed to update APIsix route")

        # Send Kafka notification
        producer.send('backend_updates', {
            'name': config.name,
            'url': config.url,
            'status': 'added'
        })

        # Update CockroachDB
        with get_cockroach_session() as session:
            session.execute(
                "INSERT INTO backends (name, url, status) VALUES (%s, %s, %s)",
                (config.name, config.url, 'active')
            )
            session.commit()

        return {"message": f"Backend {config.name} added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitor", response_model=BackendStatus)
async def monitor_backend(name: str, token: str = Depends(verify_jwt)):
    """
    Monitor backend status and metrics.
    """
    try:
        # Check CockroachDB for backend status
        with get_cockroach_session() as session:
            result = session.execute(
                "SELECT status FROM backends WHERE name = %s",
                (name,)
            ).fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Backend not found")

        # Check ScyllaDB for message stats
        with get_scylla_session() as session:
            message_count = session.execute(
                "SELECT COUNT(*) FROM messages WHERE backend = %s",
                (name,)
            ).one()[0]

        # Fetch metrics from Prometheus
        prometheus_response = requests.get(
            "http://localhost:9090/api/v1/query",
            params={"query": f'backend_requests{{name="{name}"}}'}
        )
        metrics = prometheus_response.json().get('data', {}).get('result', [])

        return BackendStatus(
            name=name,
            status=result[0],
            message_count=message_count,
            metrics=metrics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))