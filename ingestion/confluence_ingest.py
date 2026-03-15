import requests
from bs4 import BeautifulSoup
from config.settings import settings
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_and_store


def fetch_confluence_pages(limit=50):
    url = f"{settings.JIRA_BASE_URL}/wiki/rest/api/content"

    headers = {
        "Authorization": f"Bearer {settings.JIRA_API_TOKEN}",
        "Accept": "application/json"
    }

    params = {
        "type": "page",
        "limit": limit,
        "expand": "body.storage"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"[Confluence] Error: {response.status_code} - {response.text}")
        return []

    pages = response.json().get("results", [])
    print(f"[Confluence] Retrieved {len(pages)} pages")

    return pages


def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator="\n")


def process_confluence():
    pages = fetch_confluence_pages()

    for page in pages:
        page_id = page["id"]
        title = page["title"]
        html_body = page["body"]["storage"]["value"]

        text = clean_html(html_body)

        full_text = f"""
        TITLE: {title}
        PAGE_ID: {page_id}

        CONTENT:
        {text}
        """

        chunks = chunk_text(full_text)

        embed_and_store(
            chunks,
            metadata={"source": f"CONFLUENCE-{page_id}"}
        )

    print("[Confluence] Ingestion complete.")
