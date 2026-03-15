import requests
from bs4 import BeautifulSoup
from config.settings import settings
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_and_store

def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator="\n")

def process_single_confluence_page(page_id):
    print(f"[Confluence] Processing single page: {page_id}")

    url = f"{settings.JIRA_BASE_URL}/wiki/rest/api/content/{page_id}"
    headers = {
        "Authorization": f"Bearer {settings.JIRA_API_TOKEN}",
        "Accept": "application/json"
    }
    params = {"expand": "body.storage"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"[Confluence] Failed to fetch page {page_id}")
        return

    page = response.json()
    html_body = page["body"]["storage"]["value"]
    text = clean_html(html_body)

    full_text = f"""
    TITLE: {page['title']}
    PAGE_ID: {page_id}

    CONTENT:
    {text}
    """

    chunks = chunk_text(full_text)

    embed_and_store(
        chunks,
        metadata={"source": f"CONFLUENCE-{page_id}"}
    )

    print(f"[Confluence] Stored {len(chunks)} chunks from page {page_id}")

def process_confluence():
    url = f"{settings.JIRA_BASE_URL}/wiki/rest/api/content"
    headers = {
        "Authorization": f"Bearer {settings.JIRA_API_TOKEN}",
        "Accept": "application/json"
    }
    params = {"type": "page", "limit": 50, "expand": "body.storage"}

    response = requests.get(url, headers=headers, params=params)
    pages = response.json().get("results", [])

    print(f"[Confluence] Retrieved {len(pages)} pages")

    for page in pages:
        process_single_confluence_page(page["id"])
