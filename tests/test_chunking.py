"""One over-long section splits under the 190-token cap with overlap."""

from pathlib import Path

from src.chunking import CHUNK_TOKENS, _load_tokenizer, chunk_markdown
from src.config import load_config


def test_long_section_windows_overlap_and_keep_lineage(tmp_path: Path) -> None:
    """Bodies stay under 190 tokens, windows overlap, and lineage is set."""
    sentence = "The clerk records the invoice before release and notifies the supervisor."
    body = " ".join([sentence] * 80)
    markdown = f"""## Page 1
<!-- source: text -->

Fixture Procedure
doc_id: fx-us-0001
version: v1.0
effective_date: 2025-09-01
superseded_by: none
FX-9.9 Overlap window test
{body}
"""
    path = tmp_path / "fx-us-0001-v1.0.md"
    path.write_text(markdown, encoding="utf-8")
    tokenizer = _load_tokenizer(load_config().embedding_model)
    chunks = chunk_markdown(path, tokenizer)
    assert len(chunks) >= 2
    for chunk in chunks:
        count = len(tokenizer.encode(chunk.text, add_special_tokens=False))
        assert count < CHUNK_TOKENS
        assert chunk.section == "FX-9.9"
        assert chunk.document_name == "Fixture Procedure"
        assert chunk.chunk_id.startswith("fx-us-0001:v1.0:FX-9.9:1")
    tail = " ".join(chunks[0].text.split()[-8:])
    assert tail in chunks[1].text
