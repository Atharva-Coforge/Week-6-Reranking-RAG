"""Split policy markdown into section chunks.

A section heading such as ``AP-5.1`` or ``EXP-4.1`` is the unit. The heading
and its body stay together even when the body starts on the next page.
``AP-5.1`` is the last line of page 1 and the dollar amount is the first
paragraph of page 2.

A token is one id from the ``nomic-embed-text-v1.5`` tokenizer, not a word.
Every chunk's text is strictly under 190 of those tokens (we selected 190 because we have many instances of texts having ap-us-0001:v2.0:AP-7.1:2 so these are split into more than 1 tokens, so when we keep the token size as 190, we get all the tokens just under 300 tokens). A longer section
is cut into windows with 50 tokens of overlap. Each window keeps the same
section, section title, and document name. The window is moved to the next
word so a chunk does not start or end mid-word. The written file also has
lineage fields such as ``ap-us-0001:v2.0:AP-7.1:2``. Those strings split
into many ids, so the body cap stays at 200 and the whole file stays under
300 tokens.

A page with no heading, such as month-end close, uses the same 190/50 rule.
Its section is ``page-1`` and its section title is the document title.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CHUNK_TOKENS = 190
CHUNK_OVERLAP = 50
HEADING = re.compile(r"^([A-Z]+-\d+\.\d+)\s+([A-Z][^.]{0,60})$")
PAGE_HEADING = re.compile(r"^## Page (\d+)\s*$")
SOURCE_COMMENT = re.compile(r"^<!-- source: (text|image) -->\s*$")
PAGE_LABEL = re.compile(r"^Page \d+$")
HEADER_FIELD = re.compile(
    r"^(doc_id|record_id|family|version|effective_date|status|"
    r"superseded_by|currency|entity_types):\s*(.*)$"
)


@dataclass(frozen=True)
class Chunk:
    """One section, or one fallback window, with its lineage."""

    chunk_id: str
    document_id: str
    document_name: str
    version: str
    superseded_by: str
    section: str
    section_title: str
    page: int
    part: int
    source: str
    effective_date: str
    text: str


@dataclass(frozen=True)
class _Page:
    number: int
    source: str
    lines: list[str]


@dataclass
class _OpenSection:
    section: str
    section_title: str
    page: int
    source: str
    lines: list[str]


def chunk_text_dir(text_dir: Path, model_name: str) -> list[Chunk]:
    """Chunk every markdown file in `text_dir`. PDFs are not read."""
    tokenizer = _load_tokenizer(model_name)
    chunks: list[Chunk] = []
    for path in sorted(text_dir.glob("*.md")):
        chunks.extend(chunk_markdown(path, tokenizer))
    return chunks


def chunk_markdown(path: Path, tokenizer: Any) -> list[Chunk]:
    """Chunk one markdown file produced by `pdf_parse`."""
    pages = _pages(path.read_text(encoding="utf-8"))
    document_name, fields = _header(pages)
    document_id = fields.get("doc_id", path.stem)
    version = fields.get("version", "")
    superseded_by = fields.get("superseded_by", "none") or "none"
    effective_date = fields.get("effective_date", "")
    sections = _sections(pages)
    if sections:
        chunks: list[Chunk] = []
        for section in sections:
            chunks.extend(
                _emit(
                    text=" ".join(section.lines),
                    document_id=document_id,
                    document_name=document_name,
                    version=version,
                    superseded_by=superseded_by,
                    section=section.section,
                    section_title=section.section_title,
                    page=section.page,
                    source=section.source,
                    effective_date=effective_date,
                    tokenizer=tokenizer,
                )
            )
        return chunks
    chunks = []
    for page in pages:
        chunks.extend(
            _emit(
                text=_prose(page.lines, document_name),
                tokenizer=tokenizer,
                document_id=document_id,
                document_name=document_name,
                version=version,
                superseded_by=superseded_by,
                section=f"page-{page.number}",
                section_title=document_name,
                page=page.number,
                source=page.source,
                effective_date=effective_date,
            )
        )
    return chunks


def _pages(markdown: str) -> list[_Page]:
    pages: list[_Page] = []
    number = 0
    source = "text"
    lines: list[str] = []
    for raw in markdown.splitlines():
        page_match = PAGE_HEADING.match(raw.strip())
        if page_match:
            if number:
                pages.append(_Page(number, source, lines))
            number = int(page_match.group(1))
            source = "text"
            lines = []
            continue
        source_match = SOURCE_COMMENT.match(raw.strip())
        if source_match and number:
            source = source_match.group(1)
            continue
        if number:
            lines.append(raw)
    if number:
        pages.append(_Page(number, source, lines))
    return pages


def _header(pages: list[_Page]) -> tuple[str, dict[str, str]]:
    fields: dict[str, str] = {}
    document_name = ""
    if not pages:
        return document_name, fields
    for line in pages[0].lines:
        stripped = line.strip()
        if not stripped or PAGE_LABEL.match(stripped) or _banner(stripped):
            continue
        field = HEADER_FIELD.match(stripped)
        if field:
            fields[field.group(1)] = field.group(2).strip()
            continue
        if HEADING.match(stripped):
            break
        if not document_name:
            document_name = stripped
    return document_name, fields


def _sections(pages: list[_Page]) -> list[_OpenSection]:
    if not any(HEADING.match(line.strip()) for page in pages for line in page.lines):
        return []
    sections: list[_OpenSection] = []
    current: _OpenSection | None = None
    for page in pages:
        for line in page.lines:
            stripped = line.strip()
            if not stripped or _skip(stripped):
                continue
            heading = HEADING.match(stripped)
            if heading:
                if current is not None:
                    sections.append(current)
                current = _OpenSection(
                    section=heading.group(1),
                    section_title=heading.group(2).strip(),
                    page=page.number,
                    source=page.source,
                    lines=[stripped],
                )
                continue
            if current is not None and not HEADER_FIELD.match(stripped):
                current.lines.append(stripped)
    if current is not None:
        sections.append(current)
    return sections


def _prose(lines: list[str], document_name: str) -> str:
    kept: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or _skip(stripped) or HEADER_FIELD.match(stripped):
            continue
        kept.append(stripped)
    if document_name and kept and kept[0] == document_name:
        return "\n".join(kept)
    return "\n".join(kept)


def _load_tokenizer(model_name: str) -> Any:
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(model_name)


def _windows(text: str, tokenizer: Any) -> list[str]:
    """Cut prose into fewer than 190 Nomic tokens, overlapping by 50."""
    folded = " ".join(text.split())
    if not folded:
        return []
    encoded = tokenizer(
        folded,
        add_special_tokens=False,
        return_offsets_mapping=True,
    )
    offsets: list[tuple[int, int]] = list(encoded["offset_mapping"])
    count = len(offsets)
    limit = CHUNK_TOKENS - 1
    if count <= limit:
        return [folded]
    windows: list[str] = []
    start = 0
    while start < count:
        start = _snap_start(folded, offsets, start)
        if start >= count:
            break
        end = _snap_end(folded, offsets, start, min(start + limit, count))
        if end <= start:
            end = min(start + 1, count)
        piece = _fit(folded[offsets[start][0] : offsets[end - 1][1]], tokenizer)
        if piece:
            windows.append(piece)
        if end >= count:
            break
        next_start = max(end - CHUNK_OVERLAP, start + 1)
        next_start = _snap_start(folded, offsets, next_start)
        if next_start <= start:
            next_start = end
        start = next_start
    return windows


def _fit(text: str, tokenizer: Any) -> str:
    """Drop trailing words until the Nomic token count is under 190."""
    words = text.split()
    while words and len(tokenizer.encode(" ".join(words), add_special_tokens=False)) >= CHUNK_TOKENS:
        words.pop()
    return " ".join(words)


def _snap_start(text: str, offsets: list[tuple[int, int]], index: int) -> int:
    while index < len(offsets) and not _word_boundary(text, offsets[index][0]):
        index += 1
    return index


def _snap_end(
    text: str,
    offsets: list[tuple[int, int]],
    start: int,
    end: int,
) -> int:
    while end > start + 1 and not _ends_word(text, offsets[end - 1][1]):
        end -= 1
    return end


def _word_boundary(text: str, index: int) -> bool:
    return index <= 0 or text[index - 1].isspace()


def _ends_word(text: str, index: int) -> bool:
    return index >= len(text) or text[index].isspace()


def _emit(
    *,
    text: str,
    document_id: str,
    document_name: str,
    version: str,
    superseded_by: str,
    section: str,
    section_title: str,
    page: int,
    source: str,
    effective_date: str,
    tokenizer: Any,
) -> list[Chunk]:
    return [
        _make_chunk(
            document_id=document_id,
            document_name=document_name,
            version=version,
            superseded_by=superseded_by,
            section=section,
            section_title=section_title,
            page=page,
            part=part,
            source=source,
            effective_date=effective_date,
            text=window,
        )
        for part, window in enumerate(_windows(text, tokenizer), start=1)
    ]


def _make_chunk(
    *,
    document_id: str,
    document_name: str,
    version: str,
    superseded_by: str,
    section: str,
    section_title: str,
    page: int,
    part: int,
    source: str,
    effective_date: str,
    text: str,
) -> Chunk:
    chunk_id = f"{document_id}:{version}:{section}:{page}"
    if part > 1:
        chunk_id = f"{chunk_id}:{part}"
    return Chunk(
        chunk_id=chunk_id,
        document_id=document_id,
        document_name=document_name,
        version=version,
        superseded_by=superseded_by,
        section=section,
        section_title=section_title,
        page=page,
        part=part,
        source=source,
        effective_date=effective_date,
        text=text,
    )


def _skip(line: str) -> bool:
    return bool(PAGE_LABEL.match(line) or _banner(line))


def _banner(line: str) -> bool:
    return " | status: " in line


def write_chunks(chunks: list[Chunk], chunks_dir: Path) -> list[Path]:
    """Write one markdown file per chunk under `chunks_dir/<document>/`."""
    if chunks_dir.exists():
        for old in chunks_dir.rglob("*.md"):
            old.unlink()
    written: list[Path] = []
    for chunk in chunks:
        folder = chunks_dir / f"{chunk.document_id}-{chunk.version}"
        folder.mkdir(parents=True, exist_ok=True)
        name = chunk.section if chunk.part == 1 else f"{chunk.section}-{chunk.part}"
        path = folder / f"{name}.md"
        path.write_text(_chunk_file(chunk), encoding="utf-8")
        written.append(path)
    return written


def _chunk_file(chunk: Chunk) -> str:
    header = [
        f"chunk_id: {chunk.chunk_id}",
        f"document_id: {chunk.document_id}",
        f"document_name: {chunk.document_name}",
        f"version: {chunk.version}",
        f"superseded_by: {chunk.superseded_by}",
        f"section: {chunk.section}",
        f"section_title: {chunk.section_title}",
        f"page: {chunk.page}",
        f"part: {chunk.part}",
        f"source: {chunk.source}",
        f"effective_date: {chunk.effective_date}",
        "",
        chunk.text,
        "",
    ]
    return "\n".join(header)


def main() -> None:
    """Write `data/chunks/<document>/` and print each chunk id."""
    from .config import load_config

    config = load_config()
    chunks = chunk_text_dir(config.text_dir, config.embedding_model)
    written = write_chunks(chunks, config.chunks_dir)
    for path in written:
        print(path.relative_to(config.chunks_dir))
    print(f"{len(written)} chunks")


if __name__ == "__main__":
    main()
