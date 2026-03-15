from vectorstore.chroma_client import get_chroma_client

def retrieve_chunks(query: str, top_k: int = 1):
    db = get_chroma_client()
    results = db.query(query_texts=[query], n_results=top_k)
    return [
        {
            "text": results["documents"][0][i][:1500],  # truncate each chunk
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        }
        for i in range(len(results["documents"][0]))
    ]

