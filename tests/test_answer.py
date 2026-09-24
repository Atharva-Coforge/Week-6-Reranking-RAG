"""Answer text: expected substrings and a four-field citation.

Calls Cohere and Qwen. Skips when either service is missing, so recall
still runs. The pipeline is called directly, so the on-disk answer
cache is not read.
"""

import json
import re
import time
from pathlib import Path
from typing import TypedDict

import httpx
import pytest
from cohere.errors import TooManyRequestsError

from src.chroma_store import ChromaStore
from src.config import load_config
from src.embeddings import NomicEmbeddingModel
from src.llm import OllamaLLM
from src.pipeline import Pipeline
from src.rerank import CohereReranker

_CITATION = re.compile(
    r"\([^()\n]+,\s*[^()\n]+,\s*v\d+\.\d+,\s*[^()\n]+\)"
)


class Question(TypedDict):
    """One eval item from `eval/questions.json`."""

    question: str
    expected_chunk_ids: list[str]
    expected_substrings: list[str]


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS: list[Question] = json.loads(
    (ROOT / "eval" / "questions.json").read_text(encoding="utf-8")
)


def _services_ready() -> bool:
    """True when Cohere has a key and Ollama answers."""
    config = load_config()
    if not config.cohere_api_key:
        return False
    try:
        response = httpx.get(
            f"{config.ollama_url.rstrip('/')}/api/tags",
            timeout=2.0,
        )
    except httpx.HTTPError:
        return False
    return response.is_success


pytestmark = pytest.mark.skipif(
    not _services_ready(),
    reason="Ollama or COHERE_API_KEY is missing",
)


@pytest.fixture(scope="module")
def pipeline() -> Pipeline:
    """Full ask path: RRF, Cohere, then one Qwen answer call."""
    config = load_config()
    assert config.cohere_api_key is not None
    return Pipeline(
        NomicEmbeddingModel(config.embedding_model, config.embedding_dimensions),
        ChromaStore(config.chroma_dir),
        pool_size=config.pool_size,
        final_k=config.final_k,
        rrf_constant=config.rrf_constant,
        reranker=CohereReranker(config.cohere_model, config.cohere_api_key),
        llm=OllamaLLM(config.ollama_url, config.llm_model),
    )


@pytest.mark.parametrize("item", QUESTIONS, ids=[item["question"] for item in QUESTIONS])
def test_answer_has_substrings_and_citation(pipeline: Pipeline, item: Question) -> None:
    """The answer contains each expected substring and one citation."""
    question = item["question"]
    try:
        found = pipeline.ask(question)
    except TooManyRequestsError:
        time.sleep(65)
        found = pipeline.ask(question)
    answer = found.answer
    missing = [text for text in item["expected_substrings"] if text not in answer]
    assert not missing, f"{question}: missing {missing}\n{answer}"
    assert _CITATION.search(answer), f"{question}: no citation\n{answer}"
