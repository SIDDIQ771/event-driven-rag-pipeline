import PyPDF2

def load_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"[PDF Loader] Error reading {file_path}: {e}")

    return text
