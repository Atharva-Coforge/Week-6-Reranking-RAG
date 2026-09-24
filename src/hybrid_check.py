"""Print BM25, cosine, and fused pools for one question. Does not ingest."""

from .chroma_store import ChromaStore
from .config import load_config
from .embeddings import NomicEmbeddingModel
from .pipeline import Pipeline

QUESTION = "AP-5.1"


def main() -> None:
    config = load_config()
    pipeline = Pipeline(
        NomicEmbeddingModel(config.embedding_model, config.embedding_dimensions),
        ChromaStore(config.chroma_dir),
        pool_size=config.pool_sizes[0],
        rrf_constant=config.rrf_constant,
    )
    found = pipeline.ask(QUESTION)
    print("question", QUESTION)
    print("bm25")
    for hit in found.bm25:
        print(hit["id"])
    print("cosine")
    for hit in found.cosine:
        print(hit["id"])
    print("fused")
    for hit in found.fused:
        print(hit["id"])


if __name__ == "__main__":
    main()
