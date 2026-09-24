"""Union of vector and keyword hits, rerank, prompt, and generate.

This file imports only adapters. `main` builds the real objects and
passes them in. The ask path searches the existing index. It does not
chunk, embed documents, or write Chroma.
"""

from dataclasses import dataclass

from .adapters import EmbeddingModelAdapter, SearchHit, VectorStoreAdapter

FIRST_POOL = 12


@dataclass(frozen=True)
class Retrieval:
    """One BM25 list and one cosine list. RRF merges them in the next step."""

    bm25: list[SearchHit]
    cosine: list[SearchHit]


class Pipeline:
    """Ask over an already-ingested store."""

    def __init__(
        self,
        embedder: EmbeddingModelAdapter,
        store: VectorStoreAdapter,
        pool_size: int = FIRST_POOL,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._pool_size = pool_size

    def ask(self, question: str) -> Retrieval:
        """Search the existing index. PDFs and `data/text/` are not read.

        The question is embedded once. Later retries reuse that vector.
        """
        query_vector = self._embedder.embed_query(question)
        return self._retrieve(question, query_vector)

    def _retrieve(self, question: str, query_vector: list[float]) -> Retrieval:
        """BM25 and cosine share this vector. Do not embed the question again."""
        return Retrieval(
            bm25=self._store.keyword_search(question, self._pool_size),
            cosine=self._store.query(query_vector, self._pool_size),
        )
