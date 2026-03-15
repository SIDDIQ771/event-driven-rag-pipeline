import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings:
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
    JIRA_EMAIL: str = os.getenv("JIRA_EMAIL")
    SHARED_FOLDER_PATH = os.getenv("SHARED_FOLDER_PATH")
    JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
    CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
    CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
    CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
    VECTOR_DB_PATH = os.path.join(BASE_DIR, "vectorstore", "chroma_db")

settings = Settings()

print("DEBUG: SHARED_FOLDER_PATH =", settings.SHARED_FOLDER_PATH)
print("DEBUG: VECTOR_DB_PATH =", settings.VECTOR_DB_PATH)
