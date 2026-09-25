"""Expected facts are in the final-k excerpts. No Cohere and no Ollama."""

import json
from pathlib import Path
from typing import TypedDict

import pytest

from src.chroma_store import ChromaStore
from src.config import load_config
from src.embeddings import NomicEmbeddingModel
from src.pipeline import Pipeline
from src.prompts import excerpt_block


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
def test_expected_substrings_are_in_final_text(
    pipeline: Pipeline, item: Question
) -> None:
    """Every expected substring appears in the text of the final-k chunks."""
    found = pipeline.ask(item["question"])
    text = excerpt_block(found.final)
    missing = [part for part in item["expected_substrings"] if part not in text]
    assert not missing, f"{item['question']}: missing {missing}"
