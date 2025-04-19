from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..models.knowledge import KnowledgeInput
from ..utils.auth import verify_jwt
from ..utils.db import get_postgres_session, get_elasticsearch_client
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
import requests
import scrapy
from sentence_transformers import SentenceTransformer

router = APIRouter()

# Elasticsearch client
es_client = get_elasticsearch_client()

# DistilBERT for NLP
nlp_model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# APScheduler
scheduler = AsyncIOScheduler()
scheduler.start()

@router.post("/update", response_model=dict)
async def update_knowledge(input: KnowledgeInput, token: str = Depends(verify_jwt)):
    """
    Update knowledge base with URL or text.
    """
    try:
        content = input.text
        if input.url:
            # Fetch content from URL
            response = requests.get(input.url)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch URL")
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()

        # Classify content with DistilBERT
        embedding = nlp_model.encode(content)
        category = "unknown"  # Simplified; use a classifier in production

        # Store in PostgreSQL
        with get_postgres_session() as session:
            session.execute(
                "INSERT INTO knowledge (source, content, metadata, category) VALUES (%s, %s, %s, %s)",
                (input.url or "manual", content, input.metadata, category)
            )
            session.commit()

        # Store in Elasticsearch
        es_client.index(
            index="knowledge",
            body={"source": input.url or "manual", "content": content, "category": category}
        )

        return {"message": "Knowledge base updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook", response_model=dict)
async def handle_webhook(data: dict, token: str = Depends(verify_jwt)):
    """
    Handle webhooks from services (APIsix, Keycloak, etc.).
    """
    try:
        source = data.get('source', 'unknown')
        content = data.get('content', '')
        metadata = data.get('metadata', {})

        # Store in PostgreSQL
        with get_postgres_session() as session:
            session.execute(
                "INSERT INTO knowledge (source, content, metadata, category) VALUES (%s, %s, %s, %s)",
                (source, content, metadata, source)
            )
            session.commit()

        # Store in Elasticsearch
        es_client.index(
            index="knowledge",
            body={"source": source, "content": content, "category": source}
        )

        return {"message": "Webhook processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/crawler", response_model=dict)
async def crawl_documents(url: str, token: str = Depends(verify_jwt)):
    """
    Crawl documents from GitHub or services.
    """
    try:
        # Simplified; use Scrapy spider in production
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to crawl URL")
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()

        # Classify content
        embedding = nlp_model.encode(content)
        category = "unknown"

        # Store in PostgreSQL
        with get_postgres_session() as session:
            session.execute(
                "INSERT INTO knowledge (source, content, metadata, category) VALUES (%s, %s, %s, %s)",
                (url, content, {"crawler": "scrapy"}, category)
            )
            session.commit()

        # Store in Elasticsearch
        es_client.index(
            index="knowledge",
            body={"source": url, "content": content, "category": category}
        )

        # Schedule next crawl
        scheduler.add_job(
            lambda: requests.post(f"http://localhost:8000/knowledge/crawler", json={"url": url}),
            'interval',
            hours=24
        )

        return {"message": "Crawling completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))