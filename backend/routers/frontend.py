from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..models.frontend import FrontendConfig
from ..utils.auth import verify_jwt
import requests

router = APIRouter()

# APIsix admin API
APISIX_ADMIN_URL = "http://localhost:9080/admin"

@router.post("/update", response_model=dict)
async def update_frontend(config: FrontendConfig, token: str = Depends(verify_jwt)):
    """
    Update frontend configuration for Kotlin, Swift, C++, or React JS.
    """
    try:
        # Validate platform
        if config.platform not in ['kotlin', 'swift', 'cpp', 'react']:
            raise HTTPException(status_code=400, detail="Invalid platform")

        # Update APIsix route
        route_data = {
            "uri": f"/{config.platform}/*",
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

        # Store configuration (simulated)
        # In real implementation, store in PostgreSQL or CockroachDB
        config_data = {
            "platform": config.platform,
            "url": config.url,
            "settings": config.settings
        }
        # Example: Save to PostgreSQL (handled in services)
        # from ..utils.db import get_postgres_session
        # with get_postgres_session() as session:
        #     session.execute(
        #         "INSERT INTO frontend_configs (platform, url, settings) VALUES (%s, %s, %s)",
        #         (config.platform, config.url, config.settings)
        #     )

        return {"message": f"Frontend {config.platform} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))