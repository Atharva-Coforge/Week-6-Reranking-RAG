"""Nomic bi-encoder. Prefixes are applied here and are not stored."""

from sentence_transformers import SentenceTransformer

DOCUMENT_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "


class NomicEmbeddingModel:
    """Loads `nomic-embed-text-v1.5` and embeds raw text.

    The prefixes are added in this class only. Callers pass and store the raw text.
    `prompt_name` is left unset so the prefix is not applied a second time.
    """

    def __init__(self, model_name: str, dimensions: int) -> None:
        self._dimensions = dimensions
        self._model = SentenceTransformer(
            model_name,
            trust_remote_code=True,
            truncate_dim=dimensions,
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed raw chunk texts. Returns one 768-float vector per text."""
        if not texts:
            return []
        prefixed = [f"{DOCUMENT_PREFIX}{text}" for text in texts]
        vectors = self._model.encode(prefixed, normalize_embeddings=True)
        rows: list[list[float]] = vectors.tolist()
        self._check_dimensions(rows)
        return rows

    def embed_query(self, text: str) -> list[float]:
        """Embed one raw question."""
        vector = self._model.encode(
            f"{QUERY_PREFIX}{text}",
            normalize_embeddings=True,
        )
        row: list[float] = vector.tolist()
        self._check_dimensions([row])
        return row

    def _check_dimensions(self, rows: list[list[float]]) -> None:
        for row in rows:
            if len(row) != self._dimensions:
                raise ValueError(
                    f"expected {self._dimensions} dimensions, got {len(row)}"
                )
