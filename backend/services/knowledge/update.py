import requests
from bs4 import BeautifulSoup
from ...utils.db import get_postgres_session, get_elasticsearch_client

def update_knowledge(input_data: dict) -> dict:
    """
    Update knowledge base with URL or text.
    """
    try:
        content = input_data.get("text")
        if input_data.get("url"):
            # Trích xuất nội dung từ URL
            response = requests.get(input_data["url"])
            if response.status_code != 200:
                return {"error": f"Fetch URL failed: {response.text}"}
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()

        # Lưu vào PostgreSQL
        with get_postgres_session() as session:
            session.execute(
                "INSERT INTO knowledge (source, content, metadata, category) VALUES (%s, %s, %s, %s)",
                (input_data.get("url", "manual"), content, input_data.get("metadata", {}), "general")
            )
            session.commit()

        # Lưu vào Elasticsearch
        es_client = get_elasticsearch_client()
        es_client.index(
            index="knowledge",
            body={"source": input_data.get("url", "manual"), "content": content, "category": "general"}
        )

        return {"message": "Knowledge base updated successfully"}
    except Exception as e:
        return {"error": str(e)}