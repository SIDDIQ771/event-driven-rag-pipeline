import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings:
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
    SHARED_FOLDER_PATH = os.getenv("SHARED_FOLDER_PATH")
    VECTOR_DB_PATH = os.path.join(BASE_DIR, "vectorstore", "chroma_db")

settings = Settings()

print("DEBUG: SHARED_FOLDER_PATH =", settings.SHARED_FOLDER_PATH)
print("DEBUG: VECTOR_DB_PATH =", settings.VECTOR_DB_PATH)
