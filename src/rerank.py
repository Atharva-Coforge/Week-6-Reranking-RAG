"""Cohere rerank. The caller sends raw question and raw chunk texts."""

import cohere


class CohereReranker:
    """Calls `rerank-v4.0-pro`. Prefixes and vectors stay out of this file."""

    def __init__(self, model: str, api_key: str) -> None:
        self._model = model
        self._client = cohere.ClientV2(api_key=api_key)

    def rerank(self, query: str, documents: list[str]) -> list[int]:
        """Return indexes into `documents`, best match first.

        `query` is the raw question. `documents` are the fused chunk
        bodies. Callers must not pass embeddings or search prefixes.
        """
        if not documents:
            return []
        result = self._client.rerank(
            model=self._model,
            query=query,
            documents=documents,
        )
        return [row.index for row in result.results]
