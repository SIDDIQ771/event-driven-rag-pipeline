import re

def parse_intent(query: str):
    q = query.lower()

    intent = {
        "issue_key": None,
        "field": None,
        "resource": None,
        "lookup_ticket": False
    }

    # Detect JIRA issue key
    match = re.search(r"(rag-\d+)", q)
    if match:
        intent["issue_key"] = match.group(1).upper()
        intent["resource"] = "jira"

    # Detect field-level intent
    field_map = {
        "status": "status",
        "summary": "summary",
        "description": "description",
        "last comment": "last_comment",
        "latest comment": "last_comment",
        "assignee": "assignee",
        "priority": "priority",
        "created": "created",
        "updated": "updated",
        "reporter": "reporter"
    }
    for key, value in field_map.items():
        if key in q:
            intent["field"] = value

    # Detect lookup intent
    lookup_patterns = [
        "which jira ticket",
        "which ticket",
        "what ticket",
        "where is this tracked",
        "which issue covers",
        "which story",
        "which epic"
    ]
    if any(p in q for p in lookup_patterns):
        intent["lookup_ticket"] = True
        intent["resource"] = "jira"

    # Detect shared folder intent
    if any(word in q for word in ["document", "pdf", "shared folder", "file", "spec", "design"]):
        intent["resource"] = "docs"

    # Detect confluence intent
    if any(word in q for word in ["confluence", "wiki", "page", "space"]):
        intent["resource"] = "confluence"

    return intent
