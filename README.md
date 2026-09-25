# Week-6-Reranking-RAG

Hybrid search over the policy PDFs, then a Cohere rerank and one local Qwen answer.

## Setup

From a clean checkout:

```bash
uv sync
```

`ask` needs two services:

- `COHERE_API_KEY` in the environment. `rerank-v4.0-pro` reranks the fused chunks.
- Local Ollama at `http://127.0.0.1:11434` with `qwen3:8b`. That model writes the answer. Thinking is off.

## Ingest

```bash
uv run python -m src.main ingest
```

This reads `data/text`, embeds the chunks, and writes the Chroma index. Run it again after a PDF changes.

## Ask

```bash
uv run python -m src.main ask "What changed in the invoice approval threshold?"
```

`ask` does not ingest. It searches the existing index.
