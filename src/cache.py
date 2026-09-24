"""On-disk answer cache. Ingest clears it. Ask checks it before retrieval."""

import hashlib
import shutil
from collections.abc import Iterable
from pathlib import Path


def normalize_question(question: str) -> str:
    """Lowercase and collapse whitespace. Used in the cache key."""
    return " ".join(question.lower().split())


def hash_corpus(rows: Iterable[tuple[str, str]]) -> str:
    """Stable hash of ingested id and body pairs. Order does not matter."""
    hasher = hashlib.sha256()
    for chunk_id, document in sorted(rows):
        hasher.update(chunk_id.encode())
        hasher.update(b"\0")
        hasher.update(document.encode())
        hasher.update(b"\0")
    return hasher.hexdigest()


class AnswerCache:
    """Directory of cached ask results. Empty after ingest."""

    def __init__(self, directory: Path, corpus_hash: str = "") -> None:
        self._directory = directory
        self._corpus_hash = corpus_hash

    def get(self, question: str) -> str | None:
        """Return the stored log and answer, or None on a miss."""
        path = self._path(question)
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8")

    def put(self, question: str, text: str) -> None:
        """Store the log and answer for this question and corpus."""
        self._directory.mkdir(parents=True, exist_ok=True)
        self._path(question).write_text(text, encoding="utf-8")

    def clear(self) -> None:
        """Drop every cached answer so the next ask runs the full path."""
        if self._directory.exists():
            shutil.rmtree(self._directory)
        self._directory.mkdir(parents=True)

    def _path(self, question: str) -> Path:
        """Filename from the normalized question plus the corpus hash."""
        material = f"{normalize_question(question)}\n{self._corpus_hash}"
        digest = hashlib.sha256(material.encode()).hexdigest()
        return self._directory / f"{digest}.txt"
