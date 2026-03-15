import requests
from config.settings import settings
from vectorstore.chroma_client import get_chroma_client

db = get_chroma_client()


def _build_jira_headers():
    return {
        "Authorization": f"Basic {settings.JIRA_API_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def process_jira():
    """
    Fetch all issues from the JIRA project using the new /search/jql API.
    """
    url = f"{settings.JIRA_BASE_URL}/rest/api/3/search/jql"
    headers = _build_jira_headers()

    payload = {
        "jql": f"project = {settings.JIRA_PROJECT_KEY} ORDER BY created DESC",
        "maxResults": 100,
        "fields": [
            "summary", "description", "comment", "status",
            "priority", "assignee", "reporter", "created", "updated"
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("\n❌ [JIRA] SEARCH ERROR")
        print("URL:", url)
        print("Status:", response.status_code)
        print("Response:", response.text, "\n")
        return

    issues = response.json().get("issues", [])
    print(f"[JIRA] Retrieved {len(issues)} issues")

    for issue in issues:
        process_single_jira_issue(issue["key"])


def process_single_jira_issue(issue_key: str):
    """
    Fetch a single JIRA issue and store its metadata + chunked text in Chroma.
    """
    url = f"{settings.JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    headers = _build_jira_headers()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch issue {issue_key}: {response.text}")
        return

    data = response.json()
    fields = data["fields"]

    # Extract metadata fields
    metadata = {
        "source": f"JIRA-{issue_key}",
        "issue_key": issue_key,
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "status": fields["status"]["name"] if fields.get("status") else None,
        "priority": fields["priority"]["name"] if fields.get("priority") else None,
        "assignee": fields["assignee"]["displayName"] if fields.get("assignee") else None,
        "reporter": fields["reporter"]["displayName"] if fields.get("reporter") else None,
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "last_comment": (
            fields["comment"]["comments"][-1]["body"]
            if fields.get("comment") and fields["comment"]["comments"]
            else None
        )
    }

    # Chunk text contains only description + last comment
    description = metadata["description"] or "No description provided."
    last_comment = metadata["last_comment"] or "No comments available."

    text_chunk = f"""
DESCRIPTION:
{description}

COMMENTS:
{last_comment}
"""

    # Store in vector DB
    db.add(
        documents=[text_chunk],
        metadatas=[metadata],
        ids=[f"jira-{issue_key}"]
    )

    print(f"[JIRA] Stored issue {issue_key} in vector DB.")
