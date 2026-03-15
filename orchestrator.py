import threading
from ingestion.folder_watcher import start_folder_watcher
from config.settings import settings
import uvicorn
from server import app
from ingestion.jira_ingest import process_jira


def start_webhook_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def start_orchestrator():
    print("\n=== Starting Event-Driven Ingestion Pipeline ===\n")

    # STEP 1 — Initial full JIRA ingestion
    print("[Startup] Running initial JIRA ingestion...")
    process_jira()
    print("[Startup] Initial JIRA ingestion complete.\n")

    # STEP 2 — Start folder watcher
    t1 = threading.Thread(target=start_folder_watcher, args=(settings.SHARED_FOLDER_PATH,))
    t1.daemon = True
    t1.start()

    # STEP 3 — Start webhook server
    t2 = threading.Thread(target=start_webhook_server)
    t2.daemon = True
    t2.start()

    print("\n=== Pipeline Running (Folder Watcher + Webhooks) ===")

    # Keep orchestrator alive
    while True:
        pass


if __name__ == "__main__":
    start_orchestrator()
