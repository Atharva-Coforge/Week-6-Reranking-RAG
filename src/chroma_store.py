"""Chroma cosine search and BM25 over the same rows.

BM25 is not stored. It is rebuilt from Chroma on startup and after ingest.
The indexed string is ``section + section_title + text`` so a code such as
``5.1`` can match ``AP-5.1``. The Chroma document field stays the body.
"""

import re
from pathlib import Path

import chromadb
from chromadb.config import Settings
from rank_bm25 import BM25Okapi

from .adapters import SearchHit

COLLECTION_NAME = "policies"
_TOKEN = re.compile(r"[a-z0-9]+(?:\.[0-9]+)*")


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
        self._chunk_ids: list[str] = []
        self._bm25: BM25Okapi | None = None
        self.rebuild_bm25()

    def reset(self) -> None:
        """Drop the collection so a re-ingest does not keep leftover ids."""
        name = self._collection.name
        self._client.delete_collection(name)
        self._collection = self._client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
        self.rebuild_bm25()

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

    def rebuild_bm25(self) -> None:
        """Read every Chroma row and rebuild the BM25 index from it."""
        rows = self._collection.get(include=["documents", "metadatas"])
        self._chunk_ids = list(rows["ids"])
        documents = rows["documents"] or []
        metadatas = rows["metadatas"] or []
        corpus: list[list[str]] = []
        for index, _chunk_id in enumerate(self._chunk_ids):
            document = documents[index] if index < len(documents) else ""
            metadata = metadatas[index] if index < len(metadatas) else None
            corpus.append(_tokens(_bm25_text(document, metadata)))
        self._bm25 = BM25Okapi(corpus) if corpus else None

    def keyword_search(self, query: str, n_results: int) -> list[SearchHit]:
        """Return BM25 matches. `distance` is unused and set to 0."""
        tokens = _tokens(query)
        if self._bm25 is None or not self._chunk_ids or not tokens or n_results <= 0:
            return []
        scores = self._bm25.get_scores(tokens)
        ranked = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
        picked: list[str] = []
        for index in ranked:
            if scores[index] <= 0:
                break
            picked.append(self._chunk_ids[index])
            if len(picked) >= n_results:
                break
        return self._rows(picked)

    def _rows(self, chunk_ids: list[str]) -> list[SearchHit]:
        """Load full Chroma rows for BM25 ids, keeping BM25 order."""
        if not chunk_ids:
            return []
        found = self._collection.get(ids=chunk_ids, include=["documents", "metadatas"])
        documents = found["documents"] or []
        metadatas = found["metadatas"] or []
        by_id = {
            chunk_id: (document, metadata)
            for chunk_id, document, metadata in zip(
                found["ids"], documents, metadatas, strict=False
            )
        }
        hits: list[SearchHit] = []
        for chunk_id in chunk_ids:
            document, metadata = by_id.get(chunk_id, ("", {}))
            hits.append(
                SearchHit(
                    id=chunk_id,
                    document="" if document is None else document,
                    metadata={} if metadata is None else dict(metadata),
                    distance=0.0,
                )
            )
        return hits


def _tokens(text: str) -> list[str]:
    """Split so ``AP-5.1`` yields ``ap`` and ``5.1``."""
    return _TOKEN.findall(text.lower())


def _bm25_text(
    document: str | None,
    metadata: dict[str, str | int | float] | None,
) -> str:
    fields = metadata or {}
    section = str(fields.get("section", ""))
    title = str(fields.get("section_title", ""))
    body = "" if document is None else document
    return f"{section} {title} {body}"


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
