import threading
from ingestion.folder_watcher import start_folder_watcher
import uvicorn
from server import app
from config.settings import settings

def start_webhook_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def start_orchestrator():
    print("\n=== Starting Event-Driven Ingestion Pipeline ===\n")

    # Start folder watcher
    t1 = threading.Thread(target=start_folder_watcher, args=(settings.SHARED_FOLDER_PATH,))
    t1.daemon = True
    t1.start()

    # Start webhook server
    t2 = threading.Thread(target=start_webhook_server)
    t2.daemon = True
    t2.start()

    print("\n=== Pipeline Running (Folder Watcher + Webhooks) ===")

    # Keep alive
    while True:
        pass

if __name__ == "__main__":
    start_orchestrator()
