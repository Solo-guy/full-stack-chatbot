import requests
from ..utils.db import get_postgres_session

def call_grok(query: str) -> str:
    """
    Call Grok API for complex query processing.
    """
    try:
        # Gửi yêu cầu đến API Grok
        response = requests.post(
            "https://api.x.ai/grok",
            json={"query": query},
            headers={"Authorization": "Bearer YOUR_GROK_API_KEY"}  # Thay YOUR_GROK_API_KEY bằng key thực
        )
        if response.status_code != 200:
            return f"Error calling Grok: {response.text}"

        result = response.json().get("response", "No response")

        # Lưu kết quả vào cơ sở tri thức
        with get_postgres_session() as session:
            session.execute(
                "INSERT INTO knowledge (source, content, metadata, category) VALUES (%s, %s, %s, %s)",
                ("Grok", result, {"query": query}, "grok_response")
            )
            session.commit()

        return result
    except Exception as e:
        return f"Error: {str(e)}"