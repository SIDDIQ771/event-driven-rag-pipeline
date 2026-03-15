import re

def parse_intent(query: str):
    q = query.lower()

    intent = {
        "issue_key": None,
        "field": None,
        "resource": None
    }

    # Detect JIRA issue key
    match = re.search(r"(rag-\d+)", q)
    if match:
        intent["issue_key"] = match.group(1).upper()
        intent["resource"] = "jira"

    # Detect field-level intent
    if "status" in q:
        intent["field"] = "status"
    elif "summary" in q:
        intent["field"] = "summary"
    elif "description" in q:
        intent["field"] = "description"
    elif "last comment" in q or "latest comment" in q:
        intent["field"] = "last_comment"
    elif "assignee" in q:
        intent["field"] = "assignee"
    elif "priority" in q:
        intent["field"] = "priority"
    elif "created" in q:
        intent["field"] = "created"
    elif "updated" in q:
        intent["field"] = "updated"
    elif "reporter" in q:
        intent["field"] = "reporter"

    # Detect shared folder intent
    if any(word in q for word in ["document", "pdf", "shared folder", "file", "spec", "design"]):
        intent["resource"] = "docs"

    # Detect confluence intent
    if any(word in q for word in ["confluence", "wiki", "page", "space"]):
        intent["resource"] = "confluence"

    return intent
