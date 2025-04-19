from ...utils.db import get_postgres_session, get_elasticsearch_client

def handle_webhook(data: dict) -> dict:
    """
    Handle webhook data to update knowledge base.
    """
    try:
        source = data.get("source", "unknown")
        content = data.get("content", "")
        metadata = data.get("metadata", {})

        # Lưu vào PostgreSQL
        with get_postgres_session() as session:
            session.execute(
                "INSERT INTO knowledge (source, content, metadata, category) VALUES (%s, %s, %s, %s)",
                (source, content, metadata, source)
            )
            session.commit()

        # Lưu vào Elasticsearch
        es_client = get_elasticsearch_client()
        es_client.index(
            index="knowledge",
            body={"source": source, "content": content, "category": source}
        )

        return {"message": "Webhook processed successfully"}
    except Exception as e:
        return {"error": str(e)}