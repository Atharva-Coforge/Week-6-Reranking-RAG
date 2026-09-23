"""Prove embed, store, and retrieve on two known sentences.

Uses its own Chroma collection so the later `policies` collection stays empty.
Run from the repo root:

    uv run python -m src.two_sentence_check
"""

from .adapters import EmbeddingModelAdapter, VectorStoreAdapter
from .chroma_store import ChromaStore
from .config import load_config
from .embeddings import NomicEmbeddingModel

INVOICE_ID = "invoice-approval"
MEAL_ID = "meal-caps"
INVOICE = "The Chief Technical Officer (Lalit Wadhwa) approves an invoice before it is paid."
MEAL = "A meal expense is reimbursable up to the meal cap of $75 per meal."
QUESTION = "who approves an invoice"
COLLECTION_NAME = "two_sentence_check"


def main() -> None:
    """Store both sentences and require the invoice sentence to rank first."""
    config = load_config()
    embedder: EmbeddingModelAdapter = NomicEmbeddingModel(
        config.embedding_model,
        config.embedding_dimensions,
    )
    store: VectorStoreAdapter = ChromaStore(
        config.chroma_dir,
        collection_name=COLLECTION_NAME,
    )
    vectors = embedder.embed_documents([INVOICE, MEAL])
    store.upsert(INVOICE_ID, vectors[0], INVOICE, {"label": "invoice"})
    store.upsert(MEAL_ID, vectors[1], MEAL, {"label": "meal"})

    hits = store.query(embedder.embed_query(QUESTION), n_results=2)
    for hit in hits:
        print(f"{hit['distance']:.4f}  {hit['id']}  {hit['document']}")
    if not hits or hits[0]["id"] != INVOICE_ID:
        raise SystemExit("invoice sentence was not first")
    print("invoice sentence came back first")


if __name__ == "__main__":
    main()
