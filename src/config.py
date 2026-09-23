"""Model ids, retrieval sizes, Chroma path, and data path.

This module only reads settings. It does not call an embedding, rerank, or chat API.
"""

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
EMBEDDING_DIMENSIONS = 768
COHERE_MODEL = "rerank-v4.0-pro"
OLLAMA_URL = "http://127.0.0.1:11434"
LLM_MODEL = "qwen3:8b"
POOL_SIZES = (12, 24, 48)
FINAL_K = (3, 5, 8)
MAX_RETRIES = 3
RRF_CONSTANT = 60


@dataclass(frozen=True)
class Config:
    """Fixed settings for one run of the pipeline."""

    data_dir: Path
    raw_dir: Path
    text_dir: Path
    chunks_dir: Path
    chroma_dir: Path
    embedding_model: str
    embedding_dimensions: int
    cohere_model: str
    cohere_api_key: str | None
    ollama_url: str
    llm_model: str
    pool_sizes: tuple[int, int, int]
    final_k: tuple[int, int, int]
    max_retries: int
    rrf_constant: int


def _load_dotenv(path: Path) -> None:
    """Copy KEY=VALUE lines into the environment when the key is not already set."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        name, value = stripped.split("=", 1)
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        if name and name not in os.environ:
            os.environ[name] = value


def load_config() -> Config:
    """Build the config. `cohere_api_key` is None when COHERE_API_KEY is unset."""
    _load_dotenv(ROOT / ".env")
    return Config(
        data_dir=ROOT / "data",
        raw_dir=ROOT / "data" / "raw",
        text_dir=ROOT / "data" / "text",
        chunks_dir=ROOT / "data" / "chunks",
        chroma_dir=ROOT / ".chroma",
        embedding_model=EMBEDDING_MODEL,
        embedding_dimensions=EMBEDDING_DIMENSIONS,
        cohere_model=COHERE_MODEL,
        cohere_api_key=os.environ.get("COHERE_API_KEY"),
        ollama_url=OLLAMA_URL,
        llm_model=LLM_MODEL,
        pool_sizes=POOL_SIZES,
        final_k=FINAL_K,
        max_retries=MAX_RETRIES,
        rrf_constant=RRF_CONSTANT,
    )
