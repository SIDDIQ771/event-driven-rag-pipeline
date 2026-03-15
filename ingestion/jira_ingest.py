import requests
from config.settings import settings
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_and_store

def extract_issue_text(issue):
    fields = issue.get("fields", {})

    summary = fields.get("summary", "")
    description = fields.get("description", "")

    comments = fields.get("comment", {}).get("comments", [])
    comment_text = "\n".join(
        c.get("body", {}).get("content", [{}])[0].get("content", [{}])[0].get("text", "")
        for c in comments
    )

    return f"""
    KEY: {issue['key']}
    SUMMARY: {summary}

    DESCRIPTION:
    {description}

    COMMENTS:
    {comment_text}
    """

def process_single_jira_issue(issue_key):
    print(f"[JIRA] Processing single issue: {issue_key}")

    url = f"{settings.JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    headers = {
        "Authorization": f"Bearer {settings.JIRA_API_TOKEN}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[JIRA] Failed to fetch issue {issue_key}")
        return

    issue = response.json()
    text = extract_issue_text(issue)
    chunks = chunk_text(text)

    embed_and_store(
        chunks,
        metadata={"source": f"JIRA-{issue_key}"}
    )

    print(f"[JIRA] Stored {len(chunks)} chunks from {issue_key}")

def process_jira():
    url = f"{settings.JIRA_BASE_URL}/rest/api/3/search"
    headers = {
        "Authorization": f"Bearer {settings.JIRA_API_TOKEN}",
        "Accept": "application/json"
    }
    params = {"jql": "ORDER BY created DESC", "maxResults": 50}

    response = requests.get(url, headers=headers, params=params)
    issues = response.json().get("issues", [])

    print(f"[JIRA] Retrieved {len(issues)} issues")

    for issue in issues:
        process_single_jira_issue(issue["key"])
