def rank_results(results):
    ranked = []
    for r in results:
        score = 1 - r["distance"]
        if r["metadata"]["source"].endswith(".mp4"): score += 0.05
        ranked.append({**r, "score": score})
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
