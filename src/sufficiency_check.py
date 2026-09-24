"""Judge the sufficiency prompt on known excerpts, then one live retrieve.

Does not generate an answer. Needs Ollama. The live path also needs
Cohere and an ingested Chroma store.
"""

from .adapters import SearchHit
from .chroma_store import ChromaStore
from .config import load_config
from .embeddings import NomicEmbeddingModel
from .llm import OllamaLLM
from .pipeline import Pipeline
from .prompts import SUFFICIENCY_SYSTEM, parse_sufficiency, sufficiency_user
from .rerank import CohereReranker

V1_THRESHOLD = (
    "AP-5.1 Approval thresholds An invoice of $7,500 or more requires the "
    "approval of the finance manager before payment."
)
V2_THRESHOLD = (
    "AP-5.1 Approval thresholds An invoice of $10,000 or more requires the "
    "approval of the finance manager before payment."
)
ESCALATION = (
    "AP-7.1 Exception and escalation Where an approval required under "
    "Section AP-5.1 has not been obtained as the payment period in "
    "Section AP-6.1 approaches, the AP supervisor escalates the invoice."
)
EXP_TIMING = (
    "EXP-5.1 Submission timing An employee files a claim within 30 days "
    "of the date the cost was incurred."
)


def _hit(
    chunk_id: str,
    document: str,
    *,
    document_name: str,
    section: str,
    version: str,
    superseded_by: str,
) -> SearchHit:
    return {
        "id": chunk_id,
        "document": document,
        "metadata": {
            "document_name": document_name,
            "section": section,
            "version": version,
            "superseded_by": superseded_by,
        },
        "distance": 0.0,
    }


CASES: list[tuple[str, str, list[SearchHit], bool]] = [
    (
        "stale-only current-rule",
        "What is the current invoice approval threshold?",
        [
            _hit(
                "ap-v1-5.1",
                V1_THRESHOLD,
                document_name="Accounts Payable Invoice Payment Procedure",
                section="AP-5.1",
                version="v1.0",
                superseded_by="ap-us-0001-v2.0",
            )
        ],
        False,
    ),
    (
        "current rule present",
        "What is the current invoice approval threshold?",
        [
            _hit(
                "ap-v2-5.1",
                V2_THRESHOLD,
                document_name="Accounts Payable Invoice Payment Procedure",
                section="AP-5.1",
                version="v2.0",
                superseded_by="none",
            )
        ],
        True,
    ),
    (
        "compare both versions",
        "What changed in the invoice approval threshold?",
        [
            _hit(
                "ap-v1-5.1",
                V1_THRESHOLD,
                document_name="Accounts Payable Invoice Payment Procedure",
                section="AP-5.1",
                version="v1.0",
                superseded_by="ap-us-0001-v2.0",
            ),
            _hit(
                "ap-v2-5.1",
                V2_THRESHOLD,
                document_name="Accounts Payable Invoice Payment Procedure",
                section="AP-5.1",
                version="v2.0",
                superseded_by="none",
            ),
        ],
        True,
    ),
    (
        "compare missing old",
        "What changed in the invoice approval threshold?",
        [
            _hit(
                "ap-v2-5.1",
                V2_THRESHOLD,
                document_name="Accounts Payable Invoice Payment Procedure",
                section="AP-5.1",
                version="v2.0",
                superseded_by="none",
            )
        ],
        False,
    ),
    (
        "cross-reference only",
        "What is the invoice approval threshold in AP-5.1?",
        [
            _hit(
                "ap-v2-7.1",
                ESCALATION,
                document_name="Accounts Payable Invoice Payment Procedure",
                section="AP-7.1",
                version="v2.0",
                superseded_by="none",
            )
        ],
        False,
    ),
    (
        "wrong family",
        "How many days after the three-way match must an invoice be paid?",
        [
            _hit(
                "exp-5.1",
                EXP_TIMING,
                document_name="Employee Expense Reimbursement Procedure",
                section="EXP-5.1",
                version="v1.0",
                superseded_by="none",
            )
        ],
        False,
    ),
]


def main() -> None:
    config = load_config()
    llm = OllamaLLM(config.ollama_url, config.llm_model)
    failed = 0
    for name, question, hits, expected in CASES:
        text = llm.complete(SUFFICIENCY_SYSTEM, sufficiency_user(question, hits))
        got = parse_sufficiency(text)
        mark = "ok" if got == expected else "FAIL"
        if got != expected:
            failed += 1
        print(f"[{mark}] {name}  expected={expected}  got={got}")
        print(text)
        print()
    print(f"crafted {len(CASES) - failed}/{len(CASES)} matched")
    if not config.cohere_api_key:
        print("live retrieve skipped: COHERE_API_KEY is unset")
        raise SystemExit(failed)
    pipeline = Pipeline(
        NomicEmbeddingModel(config.embedding_model, config.embedding_dimensions),
        ChromaStore(config.chroma_dir),
        pool_size=config.pool_size,
        final_k=config.final_k,
        rrf_constant=config.rrf_constant,
        reranker=CohereReranker(config.cohere_model, config.cohere_api_key),
        llm=llm,
    )
    live_question = "What is section AP-5.1 about?"
    found = pipeline.ask(live_question)
    print("live", live_question)
    print("final", [hit["id"] for hit in found.final])
    print("sufficient", found.sufficient)
    print(found.sufficiency_text)
    print("question_type", found.question_type)
    print("answer")
    print(found.answer)
    raise SystemExit(failed)


if __name__ == "__main__":
    main()
