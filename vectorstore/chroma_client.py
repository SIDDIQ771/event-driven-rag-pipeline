import chromadb
from config.settings import settings

def get_chroma_client():
    client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
    return client.get_or_create_collection(name="rag_collection", metadata={"hnsw:space": "cosine"})
