"""Recall: each expected chunk id is in the RRF retrieved set.

No Cohere call and no Ollama call. The retrieved set is the fused list,
which is every chunk returned by BM25 or cosine. The on-disk answer
cache is not read.
"""

import json
from pathlib import Path
from typing import TypedDict

import pytest

from src.chroma_store import ChromaStore
from src.config import load_config
from src.embeddings import NomicEmbeddingModel
from src.pipeline import Pipeline


class Question(TypedDict):
    """One eval item from `eval/questions.json`."""

    question: str
    expected_chunk_ids: list[str]
    expected_substrings: list[str]


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS: list[Question] = json.loads(
    (ROOT / "eval" / "questions.json").read_text(encoding="utf-8")
)


@pytest.fixture(scope="module")
def pipeline() -> Pipeline:
    """Search the ingested index. No reranker and no answer model."""
    config = load_config()
    return Pipeline(
        NomicEmbeddingModel(config.embedding_model, config.embedding_dimensions),
        ChromaStore(config.chroma_dir),
        pool_size=config.pool_size,
        final_k=config.final_k,
        rrf_constant=config.rrf_constant,
    )


@pytest.mark.parametrize("item", QUESTIONS, ids=[item["question"] for item in QUESTIONS])
def test_expected_chunk_is_retrieved(pipeline: Pipeline, item: Question) -> None:
    """The gold chunk id appears in the fused BM25 and cosine list."""
    question = item["question"]
    expected = item["expected_chunk_ids"]
    found = pipeline.ask(question)
    retrieved = {hit["id"] for hit in found.fused}
    missing = [chunk_id for chunk_id in expected if chunk_id not in retrieved]
    assert not missing, f"{question}: missing {missing}"
