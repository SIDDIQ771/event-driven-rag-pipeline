import requests
from config.settings import settings
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_and_store


def fetch_jira_tickets(max_results=50):
    url = f"{settings.JIRA_BASE_URL}/rest/api/3/search"

    headers = {
        "Authorization": f"Bearer {settings.JIRA_API_TOKEN}",
        "Accept": "application/json"
    }

    params = {
        "jql": "ORDER BY created DESC",
        "maxResults": max_results,
        "expand": "renderedFields"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"[JIRA] Error: {response.status_code} - {response.text}")
        return []

    data = response.json()
    issues = data.get("issues", [])

    print(f"[JIRA] Retrieved {len(issues)} issues")
    return issues


def extract_issue_text(issue):
    fields = issue.get("fields", {})

    summary = fields.get("summary", "")
    description = fields.get("description", "")

    # Comments
    comments = fields.get("comment", {}).get("comments", [])
    comment_text = "\n".join(
        c.get("body", {}).get("content", [{}])[0].get("content", [{}])[0].get("text", "")
        for c in comments
    )

    full_text = f"""
    KEY: {issue['key']}
    SUMMARY: {summary}

    DESCRIPTION:
    {description}

    COMMENTS:
    {comment_text}
    """

    return full_text


def process_jira():
    issues = fetch_jira_tickets()

    for issue in issues:
        text = extract_issue_text(issue)
        chunks = chunk_text(text)

        embed_and_store(
            chunks,
            metadata={"source": f"JIRA-{issue['key']}"}
        )

    print("[JIRA] Ingestion complete.")
