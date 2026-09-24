"""Print RRF order, Cohere order, and the final set.

Does not ingest. The question is embedded once. Cohere receives the raw
question plus the fused bodies. Final k on this run is 8. Writes
`eval/retrieval-before-rerank.md` and `eval/retrieval-after-rerank.md`.
"""

from pathlib import Path

from .adapters import SearchHit
from .chroma_store import ChromaStore
from .config import load_config
from .embeddings import NomicEmbeddingModel
from .pipeline import Pipeline, Retrieval
from .rerank import CohereReranker

QUESTION = "What is section AP-5.1 about?"
BEFORE = Path("eval/retrieval-before-rerank.md")
AFTER = Path("eval/retrieval-after-rerank.md")


def main() -> None:
    config = load_config()
    if not config.cohere_api_key:
        raise SystemExit("COHERE_API_KEY is unset")
    pipeline = Pipeline(
        NomicEmbeddingModel(config.embedding_model, config.embedding_dimensions),
        ChromaStore(config.chroma_dir),
        pool_size=config.pool_size,
        final_k=config.final_k,
        rrf_constant=config.rrf_constant,
        reranker=CohereReranker(config.cohere_model, config.cohere_api_key),
    )
    found = pipeline.ask(QUESTION)
    print("question", QUESTION)
    print(f"pool {config.pool_size} per search")
    print(f"final k {config.final_k}")
    _print_ids("bm25", found.bm25)
    _print_ids("cosine", found.cosine)
    _print_ids("fused (RRF)", found.fused)
    _print_ids("reranked (Cohere)", found.reranked)
    _print_list("final", found.final)
    BEFORE.write_text(_before(QUESTION, config.pool_size, found), encoding="utf-8")
    AFTER.write_text(_after(QUESTION, config.pool_size, config.final_k, found), encoding="utf-8")
    print(f"wrote {BEFORE}")
    print(f"wrote {AFTER}")


def _print_ids(title: str, hits: list[SearchHit]) -> None:
    print(f"{title}  {len(hits)}")
    for index, hit in enumerate(hits, start=1):
        print(f"{index}. {hit['id']}")


def _print_list(title: str, hits: list[SearchHit]) -> None:
    print(f"{title}  {len(hits)}")
    for index, hit in enumerate(hits, start=1):
        _print_chunk(index, hit)


def _print_chunk(index: int, hit: SearchHit) -> None:
    meta = hit["metadata"]
    print(f"{index}. {hit['id']}")
    print(
        f"   section={meta.get('section')}  "
        f"version={meta.get('version')}  "
        f"superseded_by={meta.get('superseded_by')}"
    )
    print(f"   {hit['document']}")
    print()


def _before(question: str, pool_size: int, found: Retrieval) -> str:
    lines = [
        "# Retrieval before rerank",
        "",
        f"Question: `{question}`",
        "",
        f"BM25 pool: {len(found.bm25)} (cap {pool_size}). ",
        f"Cosine / vector pool: {len(found.cosine)} (cap {pool_size}). ",
        f"Fused: {len(found.fused)}. This is the Cohere input: the raw ",
        "question plus these bodies, in RRF order. No vectors. No prefixes.",
        "",
    ]
    lines.extend(_section("BM25", found.bm25))
    lines.extend(_section("Cosine (vector)", found.cosine))
    lines.extend(_section("Fused (RRF / reranker input)", found.fused))
    return "\n".join(lines)


def _after(question: str, pool_size: int, final_k: int, found: Retrieval) -> str:
    lines = [
        "# Retrieval after rerank",
        "",
        f"Question: `{question}`",
        "",
        f"Pool {pool_size} per search. Final k {final_k}. ",
        "Compare this order with `eval/retrieval-before-rerank.md`.",
        "",
        "## Reranked (Cohere)",
        "",
    ]
    for index, hit in enumerate(found.reranked, start=1):
        lines.append(f"{index}. `{hit['id']}`")
    lines.extend(["", "## Final", ""])
    lines.extend(_section("Final", found.final)[2:])
    return "\n".join(lines)


def _section(title: str, hits: list[SearchHit]) -> list[str]:
    lines = [f"# {title}", ""]
    for index, hit in enumerate(hits, start=1):
        meta = hit["metadata"]
        lines.extend(
            [
                f"## {index}. `{hit['id']}`",
                "",
                f"- section: `{meta.get('section')}`",
                f"- version: `{meta.get('version')}`",
                f"- superseded_by: `{meta.get('superseded_by')}`",
                "",
                hit["document"],
                "",
            ]
        )
    return lines


if __name__ == "__main__":
    main()
