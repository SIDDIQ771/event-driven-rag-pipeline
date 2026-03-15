from retrieval.intent_parser import parse_intent

def unified_retrieve(query: str, db):
    intent = parse_intent(query)

    # 1. Lookup ticket intent → JIRA-only semantic search
    if intent["lookup_ticket"]:
        results = db.query(
            query_texts=[query],
            n_results=3,
            where={"source": {"$contains": "JIRA"}}
        )

        if not results["metadatas"] or not results["metadatas"][0]:
            return None, []

        top_meta = results["metadatas"][0][0]
        issue_key = top_meta.get("issue_key")

        return f"The implementation is tracked in JIRA-{issue_key}.", [f"JIRA-{issue_key}"]

    # 2. Issue key present → exact match
    if intent["issue_key"]:
        key = intent["issue_key"]
        results = db.query(
            query_texts=[key],
            n_results=5,
            where={"issue_key": key}
        )

        if not results["documents"] or not results["documents"][0]:
            return None, []

        return results["documents"][0][0], [f"JIRA-{key}"]

    # 3. Resource-specific search
    if intent["resource"] == "docs":
        results = db.query(
            query_texts=[query],
            n_results=10,
            where={"source": {"$contains": "Shared_Folder"}}
        )
    elif intent["resource"] == "confluence":
        results = db.query(
            query_texts=[query],
            n_results=10,
            where={"source": {"$contains": "CONFLUENCE"}}
        )
    else:
        # 4. Global semantic search
        results = db.query(query_texts=[query], n_results=10)

    if not results["documents"] or not results["documents"][0]:
        return None, []

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    # Group by source
    grouped = {}
    for text, meta in zip(docs, metas):
        src = meta.get("source", "unknown")
        grouped.setdefault(src, []).append(text)

    # If only one source → exact answer
    if len(grouped) == 1:
        src = list(grouped.keys())[0]
        return grouped[src][0], [src]

    # Multi-source summary
    combined = "\n\n".join([t for group in grouped.values() for t in group])
    sources = list(grouped.keys())

    return combined, sources
