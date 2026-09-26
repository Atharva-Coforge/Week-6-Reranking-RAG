"""Basic RAG on one question: chunk, embed, store, cosine, answer.

No BM25 search, no RRF, no Cohere, and no answer cache. Rows go into the
`basic_rag` collection. The `policies` collection used by `python -m src.main`
is left in place.

Run from the repo root:

    uv run python -m src.assignment_runner
    uv run python -m src.assignment_runner "What is the meal expense cap?"
"""

import sys

from .chroma_store import ChromaStore
from .config import load_config
from .embeddings import NomicEmbeddingModel
from .ingest import embed_chunks, load_chunks, upsert_chunks
from .llm import OllamaLLM
from .prompts import excerpt_block

BASIC_COLLECTION = "basic_rag"
BASIC_K = 5
SAMPLE_QUESTION = "What is the current invoice approval threshold in AP-5.1?"

_SYSTEM = """\
Answer only from the excerpts in the user message. Invent nothing.
Cite the document name and section for each fact, in this form:
(document_name, section).
If the excerpts do not contain the fact, say you cannot answer from the excerpts.
"""


def run(question: str) -> str:
    """Chunk `data/text`, replace `basic_rag`, and answer from cosine top-k."""
    config = load_config()
    chunks = load_chunks(config)
    if not chunks:
        raise SystemExit(f"no chunks in {config.text_dir}")
    embedder = NomicEmbeddingModel(
        config.embedding_model,
        config.embedding_dimensions,
    )
    vectors = embed_chunks(embedder, chunks)
    store = ChromaStore(config.chroma_dir, BASIC_COLLECTION)
    store.reset()
    upsert_chunks(store, chunks, vectors)
    hits = store.query(embedder.embed_query(question), BASIC_K)
    print(f"chunks: {len(chunks)}")
    print(f"collection: {BASIC_COLLECTION}  rows: {store.count()}")
    print(f"cosine top {BASIC_K}:")
    for index, hit in enumerate(hits, start=1):
        meta = hit["metadata"]
        print(
            f"  {index}. {hit['id']}  {meta.get('section')}  "
            f"distance {hit['distance']:.4f}"
        )
    if not hits:
        raise SystemExit("cosine search returned no chunks")
    excerpts = excerpt_block(hits)
    user = f"Question: {question}\n\n{excerpts}"
    answer = OllamaLLM(config.ollama_url, config.llm_model).complete(_SYSTEM, user)
    print("answer")
    print(answer)
    return answer


def main() -> None:
    """Answer the sample question, or the question passed on the command line."""
    question = " ".join(sys.argv[1:]).strip() or SAMPLE_QUESTION
    print(f"question: {question}")
    run(question)


if __name__ == "__main__":
    main()
