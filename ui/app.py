import streamlit as st
from retrieval.query_rewriter import rewrite_query
from retrieval.retriever import retrieve_chunks
from retrieval.ranker import rank_results
from retrieval.context_assembler import assemble_context
from llm.answer_generator import generate_answer

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title("📘 Project RAG Assistant")
st.write("Ask anything about your project documents, JIRA tickets, or transcripts.")

user_query = st.text_input("Enter your question")

if user_query:
    with st.spinner("Retrieving and generating answer..."):
        rewritten = rewrite_query(user_query)
        retrieved = retrieve_chunks(rewritten)
        ranked = rank_results(retrieved)
        context = assemble_context(ranked)
        answer = generate_answer(user_query, context)

    st.subheader("💡 Answer")
    st.write(answer)

    st.subheader("📂 Retrieved Evidence")
    for r in ranked:
        with st.expander(f"Source: {r['metadata']['source']} | Score: {round(r['score'], 3)}"):
            st.write(r["text"])
