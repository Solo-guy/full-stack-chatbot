from sentence_transformers import SentenceTransformer

nlp_model = SentenceTransformer('distilbert-base-nli-mean-tokens')

def analyze_content(content: str) -> dict:
    """
    Analyze content using DistilBERT for classification or extraction.
    """
    try:
        # Tạo embedding
        embedding = nlp_model.encode(content)

        # Phân loại giả lập (cần mô hình phân loại thực tế)
        category = "general"  # Thay bằng mô hình phân loại nếu có

        return {"category": category, "embedding": embedding.tolist()}
    except Exception as e:
        return {"error": str(e)}