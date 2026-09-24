"""Nomic bi-encoder. Prefixes are applied here and are not stored."""

from typing import Any, cast

import torch
from sentence_transformers import SentenceTransformer

DOCUMENT_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "


def _get_extended_attention_mask(self, attention_mask, input_shape, device=None, dtype=None):
    """Transformers 4 helper that nomic-bert-2048 still calls.

    Transformers 5 removed this method from the base model. The mask stays
    1 for real tokens and 0 for padding, then becomes an additive mask.
    """
    del input_shape, device
    if attention_mask is None:
        return None
    if dtype is None:
        dtype = getattr(self, "dtype", torch.float32)
    if attention_mask.dim() == 3:
        extended = attention_mask[:, None, :, :]
    elif attention_mask.dim() == 2:
        extended = attention_mask[:, None, None, :]
    else:
        raise ValueError(f"unexpected attention mask shape {tuple(attention_mask.shape)}")
    extended = extended.to(dtype=dtype)
    return (1.0 - extended) * torch.finfo(dtype).min


def _restore_attention_mask_method(model: SentenceTransformer) -> None:
    """Put the removed helper back on the nomic backbone class."""
    for module in model.modules():
        cls = module.__class__
        if cls.__name__ != "NomicBertModel":
            continue
        target = cast(Any, cls)
        if not hasattr(target, "get_extended_attention_mask"):
            target.get_extended_attention_mask = _get_extended_attention_mask
        return


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
        _restore_attention_mask_method(self._model)

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
