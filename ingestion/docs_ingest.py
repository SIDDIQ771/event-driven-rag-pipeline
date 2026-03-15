import os
import sys
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_and_store

# Ensure project root is on PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SHARED_FOLDER_PATH = os.path.join(os.getcwd(), "Shared_Folder")

def load_document(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(filepath)
    elif ext == ".docx":
        loader = Docx2txtLoader(filepath)
    elif ext in [".txt", ".md"]:
        loader = TextLoader(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    docs = loader.load()
    return "\n".join([d.page_content for d in docs])

def process_document(filepath):
    print(f"[Ingest] Processing: {filepath}")
    text = load_document(filepath)
    chunks = chunk_text(text)
    embed_and_store(chunks, metadata={"source": filepath})
    print(f"[Ingest] Completed: {filepath}")

if __name__ == "__main__":
    print(f"[Ingest] Scanning folder: {SHARED_FOLDER_PATH}")
    for filename in os.listdir(SHARED_FOLDER_PATH):
        filepath = os.path.join(SHARED_FOLDER_PATH, filename)
        if os.path.isfile(filepath):
            process_document(filepath)
    print("[Ingest] Done.")
