import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ...utils.db import get_postgres_session, get_elasticsearch_client

scheduler = AsyncIOScheduler()
scheduler.start()

def crawl_documents(url: str) -> dict:
    """
    Crawl documents from URL or GitHub.
    """
    try:
        # Trích xuất nội dung
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": f"Crawl failed: {response.text}"}
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()

        # Lưu vào PostgreSQL
        with get_postgres_session() as session:
            session.execute(
                "INSERT INTO knowledge (source, content, metadata, category) VALUES (%s, %s, %s, %s)",
                (url, content, {"crawler": "scrapy"}, "general")
            )
            session.commit()

        # Lưu vào Elasticsearch
        es_client = get_elasticsearch_client()
        es_client.index(
            index="knowledge",
            body={"source": url, "content": content, "category": "general"}
        )

        # Lên lịch quét định kỳ
        scheduler.add_job(
            lambda: requests.post("http://localhost:8000/knowledge/crawler", json={"url": url}),
            'interval',
            hours=24
        )

        return {"message": f"Crawled {url} successfully"}
    except Exception as e:
        return {"error": str(e)}