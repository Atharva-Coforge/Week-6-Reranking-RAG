"""Read policy PDFs from `data/raw` and write one markdown file per PDF.

`data/text` is what chunking, embedding, and ingestion read. `data/gold/`
is never opened.

Every current page already has a text layer. Pictures on those pages are a
logo, a "REPLACED" stamp, a signature, and a flowchart whose words are
already written beside the drawing. OCR runs only when a page has no text
layer at all.
"""

from dataclasses import dataclass
from pathlib import Path

import pymupdf


@dataclass(frozen=True)
class ParsedPage:
    """One PDF page after the text layer, or OCR, has been read."""

    path: Path
    page: int
    text: str
    source: str


def parse_pdfs(raw_dir: Path) -> list[ParsedPage]:
    """Return every page of the PDFs in `raw_dir`. Subfolders are not read."""
    pages: list[ParsedPage] = []
    for path in sorted(raw_dir.glob("*.pdf")):
        if not path.is_file():
            continue
        document = pymupdf.open(path)
        try:
            for index, page in enumerate(document, start=1):
                text = page.get_text("text").strip()
                if text:
                    source = "text"
                else:
                    text = _ocr_page(page).strip()
                    source = "image"
                pages.append(
                    ParsedPage(path=path, page=index, text=text, source=source)
                )
        finally:
            document.close()
    return pages


def write_markdown(pages: list[ParsedPage], text_dir: Path) -> list[Path]:
    """Write one markdown file per PDF. Page breaks stay marked for chunking."""
    text_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[Path, list[ParsedPage]] = {}
    for parsed in pages:
        grouped.setdefault(parsed.path, []).append(parsed)
    written: list[Path] = []
    for path, page_list in grouped.items():
        parts = ["---", f"source_pdf: {path.name}", "---", ""]
        for parsed in page_list:
            parts.append(f"## Page {parsed.page}")
            parts.append(f"<!-- source: {parsed.source} -->")
            parts.append("")
            parts.append(parsed.text)
            parts.append("")
        destination = text_dir / f"{path.stem}.md"
        destination.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
        written.append(destination)
    return written


def _ocr_page(page: pymupdf.Page) -> str:
    """OCR one page that has no text layer. Requires Tesseract."""
    try:
        textpage = page.get_textpage_ocr(language="eng", dpi=300, full=True)
    except Exception as exc:
        raise RuntimeError(
            "A page has no text layer, and Tesseract is not available to OCR it."
        ) from exc
    return page.get_text("text", textpage=textpage)


def main() -> None:
    """Build `data/text` from `data/raw` and print the files written."""
    from .config import load_config

    config = load_config()
    pages = parse_pdfs(config.raw_dir)
    written = write_markdown(pages, config.text_dir)
    for path in written:
        print(path.relative_to(config.data_dir))
    print(f"{len(pages)} pages in {len(written)} files")


if __name__ == "__main__":
    main()
