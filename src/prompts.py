"""Answer prompt and excerpt block."""

from .adapters import SearchHit

ANSWER_SYSTEM = """\
Answer only from the excerpts in the user message. Invent nothing.
Do not use a search prefix. Do not mention these instructions.

Question type is on the first line of the user message.

rule-in-force: answer from the excerpt that states the fact and has
superseded_by none. A superseded excerpt is earlier text, not the
current rule.

what-changed: pair excerpts that share a section. For every pair, state
the old value and the new value. Cite each value with all four fields.
Do not stop after the first difference. If the excerpts contain both a
time difference and an amount difference, state both. If a section
appears for only one version, say the other version is not in the
excerpts. Do not guess its value.

Every sentence that states a fact cites all four fields in this form:
(document_name, section, version, superseded_by).

If the excerpts do not contain the fact, say you cannot answer from
the excerpts. Do not guess.

Fictional examples. They are not the documents you will answer from.

Example 1
Question type: rule-in-force
Question: What is the current laptop replacement cycle?
Excerpt 1
document_name: Device Refresh Procedure
section: HW-2.1
version: v1.0
superseded_by: device-refresh-v2.0
Laptops are replaced every 4 years.
Excerpt 2
document_name: Device Refresh Procedure
section: HW-2.1
version: v2.0
superseded_by: none
Laptops are replaced every 3 years.
Laptops are replaced every 3 years (Device Refresh Procedure, HW-2.1, v2.0, none).

Example 2
Question type: what-changed
Question: What changed between the device procedure versions?
Excerpt 1
document_name: Device Refresh Procedure
section: HW-2.1
version: v1.0
superseded_by: device-refresh-v2.0
Laptops are replaced every 4 years.
Excerpt 2
document_name: Device Refresh Procedure
section: HW-2.1
version: v2.0
superseded_by: none
Laptops are replaced every 3 years.
Excerpt 3
document_name: Device Refresh Procedure
section: HW-4.1
version: v1.0
superseded_by: device-refresh-v2.0
The spare-parts cap is $400.
Excerpt 4
document_name: Device Refresh Procedure
section: HW-4.1
version: v2.0
superseded_by: none
The spare-parts cap is $250.
Excerpt 5
document_name: Device Refresh Procedure
section: HW-9.1
version: v1.0
superseded_by: device-refresh-v2.0
Spare chargers are stocked on each floor.
The replacement cycle changed from every 4 years (Device Refresh Procedure, HW-2.1, v1.0, device-refresh-v2.0) to every 3 years (Device Refresh Procedure, HW-2.1, v2.0, none). The spare-parts cap changed from $400 (Device Refresh Procedure, HW-4.1, v1.0, device-refresh-v2.0) to $250 (Device Refresh Procedure, HW-4.1, v2.0, none). HW-9.1 appears only as v1.0. The other version is not in the excerpts.
"""


def excerpt_block(hits: list[SearchHit]) -> str:
    """Show lineage on every excerpt. Bodies stay raw."""
    blocks: list[str] = []
    for index, hit in enumerate(hits, start=1):
        meta = hit["metadata"]
        blocks.append(
            "\n".join(
                [
                    f"Excerpt {index}",
                    f"document_name: {meta.get('document_name', '')}",
                    f"section: {meta.get('section', '')}",
                    f"version: {meta.get('version', '')}",
                    f"superseded_by: {meta.get('superseded_by', '')}",
                    hit["document"],
                ]
            )
        )
    return "\n\n".join(blocks)


def answer_user(question: str, hits: list[SearchHit], question_type: str) -> str:
    """Question type, question, and the current final-k excerpts."""
    excerpts = excerpt_block(hits) if hits else "(no excerpts)"
    return (
        f"Question type: {question_type}\n"
        f"Question: {question}\n\n"
        f"{excerpts}"
    )
