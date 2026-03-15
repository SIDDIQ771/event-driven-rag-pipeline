from intent_parser import parse_intent

def unified_retrieve(query: str, db):
    intent = parse_intent(query)

    # 1. If JIRA issue key is present → exact match
    if intent["issue_key"]:
        key = intent["issue_key"]
        results = db.query(
            query_texts=[key],
            n_results=5,
            where={"source": f"JIRA-{key}"}
        )

        if not results["documents"] or not results["documents"][0]:
            return None, []

        return results["documents"][0][0], [f"JIRA-{key}"]

    # 2. Resource-specific search
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
        # 3. Global semantic search
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

    # If only one source matched → exact answer
    if len(grouped) == 1:
        src = list(grouped.keys())[0]
        return grouped[src][0], [src]

    # Multi-source summary
    combined = "\n\n".join([t for group in grouped.values() for t in group])
    sources = list(grouped.keys())

    return combined, sources
