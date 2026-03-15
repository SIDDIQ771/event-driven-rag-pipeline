# Event-Driven RAG Pipeline

A production-ready, multi-source Retrieval-Augmented Generation (RAG) system 
that ingests project artifacts (documents, transcripts, JIRA tickets), stores them 
in a vector database, and answers queries using Llama-3.1-8B-Instant.

## Features
- Event-driven ingestion (docs, videos, JIRA)
- Hybrid Whisper transcription
- Chunking + embedding + ChromaDB
- Unified retrieval (no intent routing)
- Query rewriting
- Ranking + context assembly
- LLM answer generation with citations
- Streamlit UI with evidence viewer
- Evaluation framework

## Setup
```bash
pip install -r requirements.txt
