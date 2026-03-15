import requests
from config.settings import settings
from vectorstore.chroma_client import get_chroma_client

db = get_chroma_client()


def _build_confluence_headers():
    return {
        "Authorization": f"Basic {settings.CONFLUENCE_API_TOKEN}",
        "Accept": "application/json"
    }


def process_confluence():
    """
    Fetch all Confluence pages from a given space and store them in Chroma.
    """
    url = f"{settings.CONFLUENCE_BASE_URL}/wiki/api/v2/spaces/{settings.CONFLUENCE_SPACE_KEY}/pages"
    headers = _build_confluence_headers()

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("\n❌ [Confluence] FETCH ERROR")
        print("URL:", url)
        print("Status:", response.status_code)
        print("Response:", response.text, "\n")
        return

    pages = response.json().get("results", [])
    print(f"[Confluence] Retrieved {len(pages)} pages")

    for page in pages:
        process_single_confluence_page(page["id"])


def process_single_confluence_page(page_id: str):
    """
    Fetch a single Confluence page and store its metadata + content.
    """
    url = f"{settings.CONFLUENCE_BASE_URL}/wiki/api/v2/pages/{page_id}?body-format=storage"
    headers = _build_confluence_headers()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch Confluence page {page_id}: {response.text}")
        return

    data = response.json()

    title = data.get("title", "Untitled Page")
    body = data.get("body", {}).get("storage", {}).get("value", "")

    metadata = {
        "source": f"CONFLUENCE-{page_id}",
        "page_id": page_id,
        "title": title
    }

    db.add(
        documents=[body],
        metadatas=[metadata],
        ids=[f"confluence-{page_id}"]
    )

    print(f"[Confluence] Stored page {page_id} ({title}) in vector DB.")
