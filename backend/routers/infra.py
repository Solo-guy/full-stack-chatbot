from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..models.infra import InfraCommand
from ..utils.auth import verify_jwt
from kubernetes import client, config
import redis
import requests

router = APIRouter()

# APIsix admin API
APISIX_ADMIN_URL = "http://localhost:9080/admin"

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Kubernetes client
config.load_kube_config()
k8s_api = client.CoreV1Api()

@router.post("/manage-kubernetes", response_model=dict)
async def manage_kubernetes(command: InfraCommand, token: str = Depends(verify_jwt)):
    """
    Execute Kubernetes commands (e.g., scale pods).
    """
    try:
        if command.service != 'kubernetes':
            raise HTTPException(status_code=400, detail="Invalid service")

        # Example: Scale deployment
        if command.action == 'scale':
            apps_api = client.AppsV1Api()
            apps_api.patch_namespaced_deployment_scale(
                name=command.params['deployment'],
                namespace='default',
                body={'spec': {'replicas': command.params['replicas']}}
            )

            # Update APIsix upstream
            upstream_data = {
                "nodes": [{"host": command.params['url'], "port": 80, "weight": 1}]
            }
            response = requests.put(
                f"{APISIX_ADMIN_URL}/upstreams/{command.params['deployment']}",
                json=upstream_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to update APIsix upstream")

        return {"message": f"Kubernetes command {command.action} executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/manage-redis", response_model=dict)
async def manage_redis(command: InfraCommand, token: str = Depends(verify_jwt)):
    """
    Execute Redis commands (e.g., set cache).
    """
    try:
        if command.service != 'redis':
            raise HTTPException(status_code=400, detail="Invalid service")

        if command.action == 'set':
            redis_client.set(command.params['key'], command.params['value'])
        elif command.action == 'get':
            value = redis_client.get(command.params['key'])
            return {"value": value.decode('utf-8') if value else None}

        return {"message": f"Redis command {command.action} executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/manage-cloudflare", response_model=dict)
async def manage_cloudflare(command: InfraCommand, token: str = Depends(verify_jwt)):
    """
    Execute Cloudflare commands (e.g., update DNS).
    """
    try:
        if command.service != 'cloudflare':
            raise HTTPException(status_code=400, detail="Invalid service")

        # Example: Update DNS via Cloudflare API
        cloudflare_api = "https://api.cloudflare.com/client/v4"
        headers = {"Authorization": f"Bearer {command.params['api_key']}"}
        response = requests.put(
            f"{cloudflare_api}/zones/{command.params['zone_id']}/dns_records",
            json={"type": "A", "name": command.params['name'], "content": command.params['ip']},
            headers=headers
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to update Cloudflare DNS")

        return {"message": f"Cloudflare command {command.action} executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add similar endpoints for Ansible, GitLab, Vault, Consul, Traefik, Dynatrace