QUERY_REWRITE_PROMPT = """
Rewrite the following user query into a detailed, explicit, context-rich search query
that will match technical documents, requirements, and project descriptions.

Original query:
{query}

Rewritten query:
"""


ANSWER_PROMPT = """
You are an AI assistant. Use the provided context to answer the user's question.

Question: {question}

Context:
{context}

Answer:
"""

