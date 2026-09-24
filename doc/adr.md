# Architecture decision records

## ADR 1 — Use nomic-embed-text-v1.5

Status: accepted

We started from `sentence-transformers/all-MiniLM-L6-v2`. That model always emits a 384-dimension vector. It also keeps only the first 256 tokens of each input. Tokens after 256 are dropped, and the vector is computed from what remains. The vector is not shortened. It stays 384 dimensions either way.

A 300-character chunk is well under 256 tokens, so the fallback size does not trigger that cutoff. A whole section can. The main split is one section with overlap 0, and a long section is what MiniLM would cut off.

`nomic-ai/nomic-embed-text-v1.5` keeps up to 8192 tokens and emits a 768-dimension vector. The code loads that model today: cosine distance, full 768 dimensions, `search_document: ` on chunks, and `search_query: ` on questions. `NomicEmbeddingModel` receives the model id as `model_name`. It needs `trust_remote_code=True` and `einops`. The files from `nomic-ai/nomic-bert-2048` are the BERT code, not a second embedding model.

The longer token limit is the reason to leave MiniLM. The larger vector is a separate property of Nomic, not what stops the 256-token cutoff. This record stays open until that reason is confirmed.

## ADR 2 — Restore the attention mask helper

Status: accepted

`nomic-embed-text-v1.5` calls `get_extended_attention_mask` on `NomicBertModel`. Transformers 5.17 removed that method. sentence-transformers 6.1 requires Transformers 5, so pinning Transformers 4 was not available. The first two-sentence run failed with `AttributeError: 'NomicBertModel' object has no attribute 'get_extended_attention_mask'`.

`src/embeddings.py` puts the method back after the model loads. `_get_extended_attention_mask` builds the additive mask Transformers 4 used to build. `_restore_attention_mask_method` attaches it to the `NomicBertModel` class when the method is missing. The embedding model stays `nomic-embed-text-v1.5`.

## ADR 3 — Cap every chunk at 300 tokens

Status: accepted

Section chunks were previously left whole, so `AP-7.1` was one chunk of well over 300 words. The 300-character fallback applied only to pages with no heading. That fallback also stepped backward by 50 characters, which landed inside a word. Month-end chunks therefore started mid-word (`l records`, `olidays`).

Counting whitespace-separated words was not enough. `page-1` of month-end close was 300 words and 360 tokens from `nomic-embed-text-v1.5`, because that tokenizer splits some words into more than one id.

A token is one id from that tokenizer, with special tokens left off. Every chunk's text encodes to fewer than 300 ids. When a section is longer, it is cut into windows that overlap by 50 of those tokens. The cut moves to the next word so a chunk does not start or end mid-word. Each window keeps the same `section`, `section_title`, and `document_name`. A second window's `chunk_id` gains a part suffix so the two rows do not overwrite each other. A page with no heading, such as month-end close, uses the same cap. Its section stays `page-1`. The `search_document:` prefix is added later, only while embedding, and is not part of this count.

## ADR 4 — Tighten the body cap to 300 tokens

Status: accepted

ADR 3 capped the body at 300 Nomic tokens. The written chunk file also has lineage fields. A string such as `ap-us-0001:v2.0:AP-7.1:2` is one field, but a tokenizer splits it into many ids. `AP-7.1.md` was 372 tokens for the whole file when the body sat near the 300 cap.

The body cap is now 190 words of those same Nomic tokens, still with 50 tokens of overlap. That leaves room for the header so the written file stays under 300 tokens. The count is still body text only. Special tokens and the `search_document:` prefix are still left off.

## ADR 5 — Reset the policies collection before upsert

Status: accepted

Chroma `upsert` is keyed by `chunk_id`, so a second ingest of the same ids overwrites those rows and does not duplicate them. That is not enough when chunking changes. A section that used to be three windows and is now two leaves the old third `chunk_id` in the collection. Search would still return that leftover.

Ingest therefore drops the `policies` collection and creates it again, then writes the current chunks. A re-run is a snapshot of `data/text`, not a merge with the previous index. Recovery after a crash mid-write is the same command: embed every chunk, reset, upsert. The `two_sentence_check` collection is a different name and is not dropped.

Resume-from-the-failed-row was not used. There are 44 chunks. Re-embedding them is cheaper than tracking which ids already landed.

## Not recorded yet

- No `superseded_by` filter at search time. Both accounts-payable versions stay in the index.
- Retrieval sizes: pool 12, then 24, then 48. Final k 3, then 5, then 8. RRF constant 60.
- Hybrid search is BM25 plus cosine, merged with RRF, then Cohere `rerank-v4.0-pro`.
- PDFs live in `data/raw/`. Ingestion reads `data/text/`. `data/gold/` is not ingested.
- OCR runs only when a page has no text layer.
