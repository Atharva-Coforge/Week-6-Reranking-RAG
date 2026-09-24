"""Chroma collection with cosine distance.

BM25 keyword search is a later step. `keyword_search` is on the adapter
already, and this class refuses that call until then.
"""

from pathlib import Path

import chromadb
from chromadb.config import Settings

from .adapters import SearchHit

COLLECTION_NAME = "policies"


class ChromaStore:
    """One persistent collection. Lower query distance is a closer match."""

    def __init__(
        self,
        persist_dir: Path,
        collection_name: str = COLLECTION_NAME,
    ) -> None:
        self._client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset(self) -> None:
        """Drop the collection so a re-ingest does not keep leftover ids."""
        name = self._collection.name
        self._client.delete_collection(name)
        self._collection = self._client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )

    def count(self) -> int:
        """Return how many rows are in the collection."""
        return self._collection.count()

    def upsert(
        self,
        chunk_id: str,
        embedding: list[float],
        document: str,
        metadata: dict[str, str | int | float],
    ) -> None:
        """Store one chunk. `document` is the raw text, with no search prefix."""
        self._collection.upsert(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata],
        )

    def query(self, embedding: list[float], n_results: int) -> list[SearchHit]:
        """Return the nearest chunks. Chroma already orders these by distance."""
        count = self._collection.count()
        if count == 0 or n_results <= 0:
            return []
        found = self._collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, count),
            include=["documents", "metadatas", "distances"],
        )
        ids = found["ids"][0]
        documents = found["documents"]
        metadatas = found["metadatas"]
        distances = found["distances"]
        docs = [] if documents is None else documents[0]
        metas = [] if metadatas is None else metadatas[0]
        dists = [] if distances is None else distances[0]
        return [
            _hit(chunk_id, docs, metas, dists, index)
            for index, chunk_id in enumerate(ids)
        ]

    def keyword_search(self, query: str, n_results: int) -> list[SearchHit]:
        """BM25 is added when the real chunks are ingested."""
        raise NotImplementedError(
            "BM25 keyword search is added in step 4 "
            f"(query length {len(query)}, n_results {n_results})"
        )


def _hit(
    chunk_id: str,
    documents: list[str | None],
    metadatas: list[dict[str, str | int | float] | None],
    distances: list[float],
    index: int,
) -> SearchHit:
    document = documents[index] if index < len(documents) else None
    metadata = metadatas[index] if index < len(metadatas) else None
    distance = distances[index] if index < len(distances) else 0.0
    return SearchHit(
        id=chunk_id,
        document="" if document is None else document,
        metadata={} if metadata is None else dict(metadata),
        distance=float(distance),
    )
