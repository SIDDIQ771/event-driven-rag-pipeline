from vectorstore.chroma_client import get_chroma_client
from retrieval.unified_retriever import unified_retrieve
from retrieval.exact_answer_extractor import extract_exact_answer
from llm.answer_generator import generate_answer   # used only for multi-source summaries

db = get_chroma_client()

def answer_query(user_query):
    retrieved_text, sources = unified_retrieve(user_query, db)

    if not retrieved_text:
        return "No relevant context found. Refine your query."

    # EXACT ANSWER MODE
    if len(sources) == 1:
        exact = extract_exact_answer(user_query, retrieved_text)
        return f"{exact}\n\n[Source: {sources[0]}]"

    # MULTI-SOURCE SUMMARY MODE
    summary = generate_answer(user_query, retrieved_text)
    src_list = "\n".join(f"- {s}" for s in sources)

    return f"{summary}\n\n[Sources:]\n{src_list}"


if __name__ == "__main__":
    q = input("Enter your query: ")
    print(answer_query(q))
