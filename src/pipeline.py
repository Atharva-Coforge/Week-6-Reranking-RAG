"""Union of vector and keyword hits, rerank, prompt, and generate.

This file imports only adapters. `main` builds the real objects and
passes them in. The ask path searches the existing index. It does not
chunk, embed documents, or write Chroma.
"""

from dataclasses import dataclass

from .adapters import (
    EmbeddingModelAdapter,
    LLMAdapter,
    ReRankerAdapter,
    SearchHit,
    VectorStoreAdapter,
)
from .prompts import ANSWER_SYSTEM, answer_user

_WHAT_CHANGED = (
    "what changed",
    "old vs new",
    "between versions",
    "before and after",
    "difference",
    "compare",
    "compared",
    "changed",
)

FIRST_POOL = 12
FINAL_K = 8
RRF_K = 60


@dataclass(frozen=True)
class Retrieval:
    """BM25 hits, cosine hits, the RRF merge, and the Cohere order."""

    bm25: list[SearchHit]
    cosine: list[SearchHit]
    fused: list[SearchHit]
    reranked: list[SearchHit]
    final: list[SearchHit]
    sufficient: bool
    sufficiency_text: str
    question_type: str
    answer: str
    final_k_used: int
    sufficiency_attempts: tuple[tuple[int, bool, str], ...]
    log: str


class Pipeline:
    """Ask over an already-ingested store."""

    def __init__(
        self,
        embedder: EmbeddingModelAdapter,
        store: VectorStoreAdapter,
        pool_size: int = FIRST_POOL,
        final_k: int = FINAL_K,
        rrf_constant: int = RRF_K,
        reranker: ReRankerAdapter | None = None,
        llm: LLMAdapter | None = None,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._pool_size = pool_size
        self._final_k = final_k
        self._rrf_constant = rrf_constant
        self._reranker = reranker
        self._llm = llm

    def ask(self, question: str) -> Retrieval:
        """Search the existing index. PDFs and `data/text/` are not read.

        The question is embedded once. Cohere's top 8 chunks go straight
        to the answer call. There is no sufficiency judge and no retry.
        """
        query_vector = self._embedder.embed_query(question)
        found = self._retrieve(question, query_vector)
        reranked = _apply_order(found.fused, self._rerank(question, found.fused))
        question_type = classify_question(question)
        final = reranked[:8]
        answer = self._answer(question, final, question_type)
        log = format_ask_log(
            question,
            question_type=question_type,
            bm25=found.bm25,
            cosine=found.cosine,
            fused=found.fused,
            reranked=reranked,
            attempts=(),
            final_k_used=len(final),
        )
        return Retrieval(
            bm25=found.bm25,
            cosine=found.cosine,
            fused=found.fused,
            reranked=reranked,
            final=final,
            sufficient=False,
            sufficiency_text="",
            question_type=question_type,
            answer=answer,
            final_k_used=len(final),
            sufficiency_attempts=(),
            log=log,
        )

    def ask_direct(self, question: str, final_k: int = 5) -> Retrieval:
        """Send Cohere's top `final_k` chunks to Qwen. No sufficiency judge.

        Retrieval matches `ask`: one query vector, pool 12, then RRF, then
        Cohere. The answer call sees only that fixed slice.
        """
        query_vector = self._embedder.embed_query(question)
        found = self._retrieve(question, query_vector)
        reranked = _apply_order(found.fused, self._rerank(question, found.fused))
        question_type = classify_question(question)
        final = reranked[:final_k]
        answer = self._answer(question, final, question_type)
        log = "path: direct\n" + format_ask_log(
            question,
            question_type=question_type,
            bm25=found.bm25,
            cosine=found.cosine,
            fused=found.fused,
            reranked=reranked,
            attempts=(),
            final_k_used=len(final),
        )
        return Retrieval(
            bm25=found.bm25,
            cosine=found.cosine,
            fused=found.fused,
            reranked=reranked,
            final=final,
            sufficient=False,
            sufficiency_text="",
            question_type=question_type,
            answer=answer,
            final_k_used=len(final),
            sufficiency_attempts=(),
            log=log,
        )

    def _retrieve(self, question: str, query_vector: list[float]) -> Retrieval:
        """BM25 and cosine share this vector. Do not embed the question again.

        Both accounts-payable versions stay in the lists. There is no
        `superseded_by` filter.
        """
        bm25 = self._store.keyword_search(question, self._pool_size)
        cosine = self._store.query(query_vector, self._pool_size)
        fused = reciprocal_rank_fusion(bm25, cosine, self._rrf_constant)
        return Retrieval(
            bm25=bm25,
            cosine=cosine,
            fused=fused,
            reranked=fused,
            final=fused[: self._final_k],
            sufficient=False,
            sufficiency_text="",
            question_type="",
            answer="",
            final_k_used=0,
            sufficiency_attempts=(),
            log="",
        )

    def _answer(
        self, question: str, hits: list[SearchHit], question_type: str
    ) -> str:
        """One answer call on the current final-k slice."""
        if self._llm is None or not hits:
            return ""
        return self._llm.complete(
            ANSWER_SYSTEM, answer_user(question, hits, question_type)
        )

    def _rerank(self, question: str, fused: list[SearchHit]) -> list[int]:
        """Send the raw question and fused bodies to Cohere.

        Vectors and search prefixes are not part of this call.
        """
        if self._reranker is None or not fused:
            return list(range(len(fused)))
        return self._reranker.rerank(question, rerank_documents(fused))


def format_ask_log(
    question: str,
    *,
    question_type: str,
    bm25: list[SearchHit],
    cosine: list[SearchHit],
    fused: list[SearchHit],
    reranked: list[SearchHit],
    attempts: tuple[tuple[int, bool, str], ...],
    final_k_used: int,
) -> str:
    """Query, ranked ids, and each sufficiency verdict. Used for diagnosis."""
    lines = [
        f"query: {question}",
        f"question_type: {question_type}",
        *_id_lines("bm25", bm25),
        *_id_lines("cosine", cosine),
        *_id_lines("rrf", fused),
        *_id_lines("cohere", reranked),
        f"final_k_used: {final_k_used}",
    ]
    if not attempts:
        lines.append("sufficiency: skipped")
        return "\n".join(lines)
    lines.append("sufficiency:")
    for k, sufficient, text in attempts:
        verdict = "YES" if sufficient else "NO"
        reason = text.strip().replace("\n", " / ")
        lines.append(f"  k={k} {verdict}  {reason}")
    return "\n".join(lines)


def _id_lines(title: str, hits: list[SearchHit]) -> list[str]:
    lines = [f"{title}: {len(hits)}"]
    for index, hit in enumerate(hits, start=1):
        lines.append(f"  {index}. {hit['id']}")
    return lines


def classify_question(question: str) -> str:
    """Keyword label for the answer prompt. Does not filter the index."""
    lowered = question.lower()
    if any(token in lowered for token in _WHAT_CHANGED):
        return "what-changed"
    return "rule-in-force"


def rerank_documents(hits: list[SearchHit]) -> list[str]:
    """Raw fused chunk texts. No prefixes. No vectors."""
    return [hit["document"] for hit in hits]


def _apply_order(hits: list[SearchHit], indexes: list[int]) -> list[SearchHit]:
    """Reorder `hits` by Cohere indexes. Unknown or repeat indexes are skipped."""
    ordered: list[SearchHit] = []
    seen: set[int] = set()
    for index in indexes:
        if index < 0 or index >= len(hits) or index in seen:
            continue
        ordered.append(hits[index])
        seen.add(index)
    for index, hit in enumerate(hits):
        if index not in seen:
            ordered.append(hit)
    return ordered


def reciprocal_rank_fusion(
    bm25: list[SearchHit],
    cosine: list[SearchHit],
    rrf_constant: int,
) -> list[SearchHit]:
    """Merge by `chunk_id` using rank only. Distances are ignored.

    Equal RRF scores break by cosine rank (missing cosine rank last),
    then by `chunk_id`. Dict insertion order is not used.
    """
    scores: dict[str, float] = {}
    rows: dict[str, SearchHit] = {}
    cosine_rank: dict[str, int] = {}
    for rank, hit in enumerate(bm25, start=1):
        chunk_id = hit["id"]
        scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (rrf_constant + rank)
        rows[chunk_id] = hit
    for rank, hit in enumerate(cosine, start=1):
        chunk_id = hit["id"]
        scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (rrf_constant + rank)
        rows[chunk_id] = hit
        cosine_rank[chunk_id] = rank
    ordered = sorted(
        scores,
        key=lambda chunk_id: (
            -scores[chunk_id],
            cosine_rank.get(chunk_id, float("inf")),
            chunk_id,
        ),
    )
    return [rows[chunk_id] for chunk_id in ordered]
