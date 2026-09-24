"""Union of vector and keyword hits, rerank, prompt, and generate.

This file imports only adapters. `main` builds the real objects and
passes them in. The ask path searches the existing index. It does not
chunk, embed documents, or write Chroma.
"""

from dataclasses import dataclass

from .adapters import EmbeddingModelAdapter, SearchHit, VectorStoreAdapter

FIRST_POOL = 12
RRF_K = 60


@dataclass(frozen=True)
class Retrieval:
    """BM25 hits, cosine hits, and the RRF merge of those two lists."""

    bm25: list[SearchHit]
    cosine: list[SearchHit]
    fused: list[SearchHit]


class Pipeline:
    """Ask over an already-ingested store."""

    def __init__(
        self,
        embedder: EmbeddingModelAdapter,
        store: VectorStoreAdapter,
        pool_size: int = FIRST_POOL,
        rrf_constant: int = RRF_K,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._pool_size = pool_size
        self._rrf_constant = rrf_constant

    def ask(self, question: str) -> Retrieval:
        """Search the existing index. PDFs and `data/text/` are not read.

        The question is embedded once. Later retries reuse that vector.
        """
        query_vector = self._embedder.embed_query(question)
        return self._retrieve(question, query_vector)

    def _retrieve(self, question: str, query_vector: list[float]) -> Retrieval:
        """BM25 and cosine share this vector. Do not embed the question again.

        Both accounts-payable versions stay in the lists. There is no
        `superseded_by` filter.
        """
        bm25 = self._store.keyword_search(question, self._pool_size)
        cosine = self._store.query(query_vector, self._pool_size)
        return Retrieval(
            bm25=bm25,
            cosine=cosine,
            fused=reciprocal_rank_fusion(bm25, cosine, self._rrf_constant),
        )


def reciprocal_rank_fusion(
    bm25: list[SearchHit],
    cosine: list[SearchHit],
    rrf_constant: int,
) -> list[SearchHit]:
    """Merge by `chunk_id` using rank only. Scores and distances are ignored."""
    scores: dict[str, float] = {}
    rows: dict[str, SearchHit] = {}
    for rank, hit in enumerate(bm25, start=1):
        chunk_id = hit["id"]
        scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (rrf_constant + rank)
        rows[chunk_id] = hit
    for rank, hit in enumerate(cosine, start=1):
        chunk_id = hit["id"]
        scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (rrf_constant + rank)
        rows[chunk_id] = hit
    ordered = sorted(scores, key=lambda chunk_id: scores[chunk_id], reverse=True)
    return [rows[chunk_id] for chunk_id in ordered]
