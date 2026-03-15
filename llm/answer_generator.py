from transformers import pipeline
from llm.prompts import ANSWER_PROMPT

# HF model for answer generation
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_answer(query, context):
    # Handle missing context safely
    if not context:
        context = "No relevant context was retrieved from the knowledge base."

    prompt = ANSWER_PROMPT.format(
        question=query,
        context=context
    )

    result = generator(prompt, max_length=256, do_sample=False)
    return result[0]["generated_text"]
