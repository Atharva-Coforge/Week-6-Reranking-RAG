"""A fake reranker reorders the fused list and final_k limits the slice."""

from src.pipeline import Pipeline


def _hit(index: int) -> dict[str, object]:
    return {
        "id": f"id-{index}",
        "document": f"doc {index}",
        "metadata": {},
        "distance": 0.1,
    }


class _Embedder:
    def embed_query(self, text: str) -> list[float]:
        return [0.0]


class _Store:
    def query(self, embedding: list[float], n_results: int) -> list[dict[str, object]]:
        return [_hit(index) for index in range(n_results)]

    def keyword_search(self, query: str, n_results: int) -> list[dict[str, object]]:
        return [_hit(index) for index in range(n_results)]


class _ReverseReranker:
    def rerank(self, query: str, documents: list[str]) -> list[int]:
        return list(range(len(documents) - 1, -1, -1))


def test_ask_applies_rerank_order_and_final_k() -> None:
    """The first final chunk is the one the reranker put first, and k is 2."""
    pipeline = Pipeline(
        _Embedder(),
        _Store(),
        pool_size=4,
        final_k=2,
        reranker=_ReverseReranker(),
    )
    found = pipeline.ask("who approves an invoice")
    assert len(found.final) == 2
    assert found.final[0]["id"] == found.fused[-1]["id"]
