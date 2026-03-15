from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import settings
import chromadb

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
collection = client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"}
)

def embed_and_store(chunks, metadata):
    for i, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk)
        collection.add(
            ids=[f"{metadata['source']}_chunk_{i}"],
            documents=[chunk],
            embeddings=[vector],
            metadatas=[{**metadata, "chunk_id": i}]
        )

    print(f"[Embedder] Stored {len(chunks)} chunks from {metadata['source']}")
