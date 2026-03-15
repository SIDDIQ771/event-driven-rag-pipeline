from retrieval.query_rewriter import rewrite_query
from retrieval.retriever import retrieve_chunks
from retrieval.ranker import rank_results
from retrieval.context_assembler import assemble_context
from llm.answer_generator import generate_answer

def answer_query(user_query):
    # rewritten = rewrite_query(user_query)
    rewritten = user_query
    retrieved = retrieve_chunks(rewritten)
    ranked = rank_results(retrieved)
    context = assemble_context(ranked)
    # HARD LIMIT to avoid overflow
    MAX_CONTEXT_CHARS = 2000
    context = context[:MAX_CONTEXT_CHARS]
    answer = generate_answer(user_query, context)
    return answer

if __name__ == "__main__":
    q = input("Enter your query: ")
    print(answer_query(q))
