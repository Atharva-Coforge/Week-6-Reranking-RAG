"""CLI: ingest and ask. Builds the real adapters from config and injects them."""

import sys

from .cache import AnswerCache, hash_corpus
from .chroma_store import ChromaStore
from .config import load_config
from .embeddings import NomicEmbeddingModel
from .ingest import run_ingest
from .llm import OllamaLLM
from .pipeline import Pipeline
from .rerank import CohereReranker


def main() -> None:
    """`ingest` rebuilds the index. `ask` searches it and does not ingest."""
    if len(sys.argv) < 2 or sys.argv[1] not in {"ingest", "ask"}:
        raise SystemExit(
            'usage: python -m src.main ingest\n'
            '       python -m src.main ask "your question"'
        )
    if sys.argv[1] == "ingest":
        _ingest()
        return
    _ask()


def _ingest() -> None:
    """Read `data/text`, upsert Chroma, rebuild BM25, and clear the cache."""
    config = load_config()
    chunks = run_ingest(config)
    print(f"ingested {len(chunks)} chunks")
    print("cache cleared")


def _ask() -> None:
    """Search the existing index. The cache is checked before retrieval."""
    question = " ".join(sys.argv[2:]).strip()
    if not question:
        raise SystemExit('usage: python -m src.main ask "your question"')
    config = load_config()
    store = ChromaStore(config.chroma_dir)
    cache = AnswerCache(config.cache_dir, hash_corpus(store.ingested_rows()))
    cached = cache.get(question)
    if cached is not None:
        print("cache hit")
        print(cached)
        return
    print("cache miss")
    if not config.cohere_api_key:
        raise SystemExit("COHERE_API_KEY is unset")
    pipeline = Pipeline(
        NomicEmbeddingModel(config.embedding_model, config.embedding_dimensions),
        store,
        pool_size=config.pool_size,
        final_k=config.final_k,
        rrf_constant=config.rrf_constant,
        reranker=CohereReranker(config.cohere_model, config.cohere_api_key),
        llm=OllamaLLM(config.ollama_url, config.llm_model),
    )
    found = pipeline.ask(question)
    stored = f"{found.log}\nanswer\n{found.answer}"
    cache.put(question, stored)
    print(stored)


if __name__ == "__main__":
    main()
