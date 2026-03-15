def extract_exact_answer(query: str, text: str):
    q = query.lower()

    # Status
    if "status" in q and "STATUS:" in text:
        return text.split("STATUS:")[1].split("\n")[0].strip()

    # Summary
    if "summary" in q and "SUMMARY:" in text:
        return text.split("SUMMARY:")[1].split("DESCRIPTION:")[0].strip()

    # Description
    if "description" in q and "DESCRIPTION:" in text:
        return text.split("DESCRIPTION:")[1].split("COMMENTS:")[0].strip()

    # Last comment
    if ("last comment" in q or "latest comment" in q) and "COMMENTS:" in text:
        return text.split("COMMENTS:")[1].strip()

    # Assignee
    if "assignee" in q and "ASSIGNEE:" in text:
        return text.split("ASSIGNEE:")[1].split("\n")[0].strip()

    # Priority
    if "priority" in q and "PRIORITY:" in text:
        return text.split("PRIORITY:")[1].split("\n")[0].strip()

    # Created
    if "created" in q and "CREATED:" in text:
        return text.split("CREATED:")[1].split("\n")[0].strip()

    # Updated
    if "updated" in q and "UPDATED:" in text:
        return text.split("UPDATED:")[1].split("\n")[0].strip()

    # Reporter
    if "reporter" in q and "REPORTER:" in text:
        return text.split("REPORTER:")[1].split("\n")[0].strip()

    # Default → return full text
    return text.strip()
