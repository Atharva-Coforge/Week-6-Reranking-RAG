"""Protocols for the four adapters. No SDK imports in this file."""

from typing import Protocol, TypedDict


class SearchHit(TypedDict):
    """One retrieved chunk. `distance` is the cosine distance from Chroma."""

    id: str
    document: str
    metadata: dict[str, str | int | float]
    distance: float


class EmbeddingModelAdapter(Protocol):
    """Bi-encoder. Implementations add the nomic search prefixes."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed raw chunk texts. Returns one vector per text."""

    def embed_query(self, text: str) -> list[float]:
        """Embed one raw question."""


class VectorStoreAdapter(Protocol):
    """Chroma cosine search and BM25 keyword search over the same chunks."""

    def upsert(
        self,
        chunk_id: str,
        embedding: list[float],
        document: str,
        metadata: dict[str, str | int | float],
    ) -> None:
        """Store one chunk. `document` is the raw text, with no search prefix."""

    def query(self, embedding: list[float], n_results: int) -> list[SearchHit]:
        """Return the nearest chunks. Lower `distance` is a closer match."""

    def keyword_search(self, query: str, n_results: int) -> list[SearchHit]:
        """Return BM25 matches. `distance` is unused and set to 0."""


class ReRankerAdapter(Protocol):
    """Cross-encoder style rescoring of query and chunk text pairs."""

    def rerank(self, query: str, documents: list[str]) -> list[int]:
        """Return indexes into `documents`, best match first."""


class LLMAdapter(Protocol):
    """One chat completion. The caller chooses the prompt."""

    def complete(self, system: str, user: str) -> str:
        """Return the answer text with any thinking trace already removed."""
