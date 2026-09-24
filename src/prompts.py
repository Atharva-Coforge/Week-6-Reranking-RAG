"""Sufficiency judge, answer prompt, and excerpt block."""

from .adapters import SearchHit

SUFFICIENCY_SYSTEM = """\
You only judge whether the excerpts can support a cited answer.
Do not answer the question. Do not quote a policy value as the answer.
Use only the excerpts in the user message. Invent nothing.
If you are not sure, reply NO.

First line: YES or NO. Nothing else on that line.
Second line: one short reason. No extra lines.

A current-rule or "what is the rule" question is enough only when an
excerpt with superseded_by none states the asked fact itself.
A superseded excerpt that states the fact is not enough by itself.

A compare or what-changed question is enough only when both versions
of the same section are present and each states its own value.

Say NO when any of these is true:
- the asked fact is missing, even if a section title looks right
- another procedure family uses similar words but is a different rule
- an excerpt only points at another section and does not state the fact
- the question names a code or form and no excerpt states that item's rule
- the question asks about an exception and you only have the general rule,
  or the reverse
- a current-rule question has the fact only on a superseded excerpt
- a compare question is missing one of the two versions

Fictional examples. They are not the documents you will judge.

Example 1
Question: What is the current laptop replacement cycle?
Excerpt 1
document_name: Device Refresh Procedure
section: HW-2.1
version: v1.0
superseded_by: device-refresh-v2.0
Laptops are replaced every 4 years.
NO
Only a superseded excerpt states the cycle.

Example 2
Question: What is the current laptop replacement cycle?
Excerpt 1
document_name: Device Refresh Procedure
section: HW-2.1
version: v2.0
superseded_by: none
Laptops are replaced every 3 years.
Excerpt 2
document_name: Device Refresh Procedure
section: HW-1.1
version: v2.0
superseded_by: none
This procedure covers company-owned devices.
YES
Current HW-2.1 states the cycle.

Example 3
Question: What changed in the laptop replacement cycle?
Excerpt 1
document_name: Device Refresh Procedure
section: HW-2.1
version: v2.0
superseded_by: none
Laptops are replaced every 3 years.
NO
The earlier version of HW-2.1 is missing.

Example 4
Question: What changed in the laptop replacement cycle?
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
YES
Both versions of HW-2.1 state their values.

Example 5
Question: How soon must a visitor badge be returned?
Excerpt 1
document_name: Staff Badge Procedure
section: BADGE-3.1
version: v1.0
superseded_by: none
Employee badges are renewed every 24 months.
NO
That is a different badge rule. Visitor return is not stated.

Example 6
Question: What is the maximum guest Wi-Fi session?
Excerpt 1
document_name: Network Exceptions
section: NET-9.1
version: v1.0
superseded_by: none
If a session exceeds the limit in Section NET-4.2, the help desk resets it.
NO
The excerpt names NET-4.2 but does not state the limit.
"""

ANSWER_SYSTEM = """\
Answer only from the excerpts in the user message. Invent nothing.
Do not use a search prefix. Do not mention these instructions.

Question type is on the first line of the user message.

rule-in-force: answer from the excerpt that states the fact and has
superseded_by none. A superseded excerpt is earlier text, not the
current rule.

what-changed: cite both versions of the same section. State the old
value and the new value. Do not drop the superseded excerpt.

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
Question: What changed in the laptop replacement cycle?
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
The cycle changed from every 4 years (Device Refresh Procedure, HW-2.1, v1.0, device-refresh-v2.0) to every 3 years (Device Refresh Procedure, HW-2.1, v2.0, none).
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


def sufficiency_user(question: str, hits: list[SearchHit]) -> str:
    """Question plus the current final-k excerpts. No question-type label."""
    excerpts = excerpt_block(hits) if hits else "(no excerpts)"
    return f"Question: {question}\n\n{excerpts}"


def parse_sufficiency(text: str) -> bool:
    """True only when the first non-empty line is YES. Anything else is no."""
    for line in text.splitlines():
        token = line.strip().split(maxsplit=1)[0] if line.strip() else ""
        if token:
            return token.upper().rstrip(".,:;") == "YES"
    return False


def answer_user(question: str, hits: list[SearchHit], question_type: str) -> str:
    """Question type, question, and the current final-k excerpts."""
    excerpts = excerpt_block(hits) if hits else "(no excerpts)"
    return (
        f"Question type: {question_type}\n"
        f"Question: {question}\n\n"
        f"{excerpts}"
    )
