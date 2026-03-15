from transformers import pipeline
from llm.prompts import QUERY_REWRITE_PROMPT

# Lightweight HF model for rewriting queries
rewriter = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def rewrite_query(query: str) -> str:
    prompt = QUERY_REWRITE_PROMPT.format(query=query)
    result = rewriter(prompt, max_length=128, do_sample=False)
    return result[0]["generated_text"]
