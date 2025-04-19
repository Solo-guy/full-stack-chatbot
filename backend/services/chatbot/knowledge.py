from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import ElasticsearchStore

def search_knowledge(query: str) -> str:
    """
    Search knowledge base using LangChain and RAG.
    """
    try:
        # Khởi tạo LangChain với Elasticsearch
        embeddings = SentenceTransformerEmbeddings(model_name="distilbert-base-nli-mean-tokens")
        vector_store = ElasticsearchStore(
            index_name="knowledge",
            embedding=embeddings,
            es_url="http://localhost:9200"
        )

        # Tìm kiếm tài liệu liên quan
        results = vector_store.similarity_search(query, k=3)
        if not results:
            return "No relevant information found"

        # Kết hợp kết quả
        combined_result = "\n".join([doc.page_content for doc in results])
        return combined_result
    except Exception as e:
        return f"Error: {str(e)}"