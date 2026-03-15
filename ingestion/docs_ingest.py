import os
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_and_store
from ingestion.pdf_loader import load_pdf
from config.settings import settings
from ingestion.docx_loader import load_docx

def load_document_text(file_path):
    ext = file_path.lower()

    if ext.endswith(".pdf"):
        return load_pdf(file_path)

    if ext.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return ""

def process_single_document(file_path):
    print(f"[Docs] Processing file: {file_path}")

    text = load_document_text(file_path)
    if not text.strip():
        print(f"[Docs] Skipped empty or unsupported file: {file_path}")
        return

    chunks = chunk_text(text)

    embed_and_store(
        chunks,
        metadata={"source": f"DOC-{os.path.basename(file_path)}"}
    )

    print(f"[Docs] Stored {len(chunks)} chunks from {file_path}")

def process_documents():
    folder = settings.SHARED_FOLDER_PATH

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            process_single_document(path)

def load_document_text(file_path):
    ext = file_path.lower()

    if ext.endswith(".pdf"):
        return load_pdf(file_path)

    if ext.endswith(".docx"):
        return load_docx(file_path)

    if ext.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return ""

