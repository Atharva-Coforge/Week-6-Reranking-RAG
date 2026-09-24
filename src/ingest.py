"""Load chunks from `data/text`, embed their raw bodies, and upsert Chroma.

The document prefix is added only inside `embed_documents`. Chroma stores
the raw body. BM25 is rebuilt from those rows after the write.
"""

from pathlib import Path

from .adapters import EmbeddingModelAdapter, VectorStoreAdapter
from .cache import AnswerCache
from .chroma_store import ChromaStore
from .chunking import Chunk, chunk_text_dir
from .config import Config, load_config
from .embeddings import NomicEmbeddingModel
from .pdf_parse import parse_pdfs, write_markdown


def load_chunks(config: Config) -> list[Chunk]:
    """Chunk `data/text`. PDFs and `data/gold/` are not read."""
    return chunk_text_dir(config.text_dir, config.embedding_model)


def embed_chunks(
    embedder: EmbeddingModelAdapter,
    chunks: list[Chunk],
) -> list[list[float]]:
    """Embed every chunk body in one call. The prefix is not stored."""
    return embedder.embed_documents([chunk.text for chunk in chunks])


def upsert_chunks(
    store: VectorStoreAdapter,
    chunks: list[Chunk],
    vectors: list[list[float]],
) -> None:
    """Write one Chroma row per chunk after every vector exists."""
    if len(vectors) != len(chunks):
        raise ValueError(f"expected {len(chunks)} vectors, got {len(vectors)}")
    for chunk, vector in zip(chunks, vectors, strict=True):
        store.upsert(chunk.chunk_id, vector, chunk.text, _metadata(chunk))


def _metadata(chunk: Chunk) -> dict[str, str | int | float]:
    """Lineage fields only. `text` is the document, not metadata."""
    return {
        "document_id": chunk.document_id,
        "document_name": chunk.document_name,
        "version": chunk.version,
        "superseded_by": chunk.superseded_by,
        "section": chunk.section,
        "section_title": chunk.section_title,
        "page": chunk.page,
        "part": chunk.part,
        "source": chunk.source,
        "effective_date": chunk.effective_date,
    }


def run_ingest(config: Config) -> list[Chunk]:
    """Chunk `data/text`, replace Chroma, rebuild BM25, and clear the cache.

    Re-parses `data/raw` into `data/text` only when a PDF is new or newer
    than its markdown file. `data/gold/` is not read.
    """
    if _pdfs_changed(config.raw_dir, config.text_dir):
        write_markdown(parse_pdfs(config.raw_dir), config.text_dir)
    chunks = load_chunks(config)
    embedder = NomicEmbeddingModel(
        config.embedding_model,
        config.embedding_dimensions,
    )
    store = ChromaStore(config.chroma_dir)
    vectors = embed_chunks(embedder, chunks)
    store.reset()
    upsert_chunks(store, chunks, vectors)
    store.rebuild_bm25()
    AnswerCache(config.cache_dir).clear()
    return chunks


def _pdfs_changed(raw_dir: Path, text_dir: Path) -> bool:
    """True when a PDF has no markdown yet, or the PDF is newer."""
    for pdf in sorted(raw_dir.glob("*.pdf")):
        if not pdf.is_file():
            continue
        markdown = text_dir / f"{pdf.stem}.md"
        if not markdown.is_file() or pdf.stat().st_mtime > markdown.stat().st_mtime:
            return True
    return False


def main() -> None:
    """Embed all chunks, replace the policies collection, and upsert each row."""
    config = load_config()
    chunks = run_ingest(config)
    for chunk in chunks:
        print(chunk.chunk_id)
    store = ChromaStore(config.chroma_dir)
    print(f"{store.count()} rows")
    print("bm25 5.1")
    for hit in store.keyword_search("5.1", n_results=5):
        meta = hit["metadata"]
        print(f"{hit['id']}  {meta.get('section')}  {meta.get('version')}")


if __name__ == "__main__":
    main()
