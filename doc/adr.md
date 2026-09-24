# Architecture decision records

## ADR 1 — Use nomic-embed-text-v1.5

Status: accepted

We started from `sentence-transformers/all-MiniLM-L6-v2`. That model always emits a 384-dimension vector. It also keeps only the first 256 tokens of each input. Tokens after 256 are dropped, and the vector is computed from what remains. The vector is not shortened. It stays 384 dimensions either way.

A short window is well under 256 tokens. A whole section can exceed that. MiniLM would cut the section off. That cutoff is why we left MiniLM. How a long section is split is not decided here. Later records set the body cap and the overlap: ADR 3, then ADR 4 (190 body tokens), then ADR 8 (25-token overlap).

`nomic-ai/nomic-embed-text-v1.5` keeps up to 8192 tokens and emits a 768-dimension vector. The code loads that model today: cosine distance, full 768 dimensions, `search_document: ` on chunks, and `search_query: ` on questions. `NomicEmbeddingModel` receives the model id as `model_name`. It needs `trust_remote_code=True` and `einops`. The files from `nomic-ai/nomic-bert-2048` are the BERT code, not a second embedding model.

The longer token limit is the reason to leave MiniLM. The larger vector is a separate property of Nomic, not what stops the 256-token cutoff.

## ADR 2 — Restore the attention mask helper

Status: accepted

`nomic-embed-text-v1.5` calls `get_extended_attention_mask` on `NomicBertModel`. Transformers 5.17 removed that method. sentence-transformers 6.1 requires Transformers 5, so pinning Transformers 4 was not available. The first two-sentence run failed with `AttributeError: 'NomicBertModel' object has no attribute 'get_extended_attention_mask'`.

`src/embeddings.py` puts the method back after the model loads. `_get_extended_attention_mask` builds the additive mask Transformers 4 used to build. `_restore_attention_mask_method` attaches it to the `NomicBertModel` class when the method is missing. The embedding model stays `nomic-embed-text-v1.5`.

## ADR 3 — Cap every chunk at 300 tokens

Status: superseded by ADR 4 and ADR 8

Section chunks were previously left whole, so `AP-7.1` was one chunk of well over 300 words. The 300-character fallback applied only to pages with no heading. That fallback also stepped backward by 50 characters, which landed inside a word. Month-end chunks therefore started mid-word (`l records`, `olidays`).

Counting whitespace-separated words was not enough. `page-1` of month-end close was 300 words and 360 tokens from `nomic-embed-text-v1.5`, because that tokenizer splits some words into more than one id.

This record first capped every chunk body at 300 tokenizer ids with 50 tokens of overlap. That pair is not live. ADR 4 set the body cap to 190 ids so the written file stays under 300. ADR 8 set overlap to 25.

## ADR 4 — Tighten the body cap to 190 tokens

Status: accepted

ADR 3 capped the body at 300 Nomic tokens. The written chunk file also has lineage fields. A string such as `ap-us-0001:v2.0:AP-7.1:2` is one field, but a tokenizer splits it into many ids. `AP-7.1.md` was 372 tokens for the whole file when the body sat near the 300 cap.

The body cap is 190 ids from the `nomic-embed-text-v1.5` tokenizer (`CHUNK_TOKENS`), not 190 words. That leaves room for the header so the written file stays under 300 tokens. The count is still body text only. Special tokens and the `search_document:` prefix are still left off. Overlap is not decided here. ADR 8 set it to 25.

## ADR 5 — Reset the policies collection before upsert

Status: accepted

Chroma `upsert` is keyed by `chunk_id`, so a second ingest of the same ids overwrites those rows and does not duplicate them. That is not enough when chunking changes. A section that used to be three windows and is now two leaves the old third `chunk_id` in the collection. Search would still return that leftover.

Ingest therefore drops the `policies` collection and creates it again, then writes the current chunks. A re-run is a snapshot of `data/text`, not a merge with the previous index. Recovery after a crash mid-write is the same command: embed every chunk, reset, upsert. The `two_sentence_check` collection is a different name and is not dropped.

Resume-from-the-failed-row was not used. There are 44 chunks. Re-embedding them is cheaper than tracking which ids already landed.

## ADR 6 — Fold money and drop function words in BM25

Status: accepted

A question such as `$12000` failed to lock the chunk that says `$10,000`. The first tokenizer kept `$10,000` as `10` and `000`. Common words (`who`, `to`, `on`, `a`) also let month-end windows outrank a short policy section.

BM25 folds `$` and thousands commas to a single digit token, drops function words, and adds `document_name` next to `section + section_title + text`. There is no list of English number phrases. Cosine embeddings are unchanged. `12000` still does not equal `10000`; that comparison stays with the vector search and the later reranker. Hyphenated forms such as `ap-5.1` are a later change. See ADR 9.

## ADR 7 — Keep the pool at 12; grow only final k

Status: accepted

The first schedule was pool 12, then 24, then 48, with final k 3, then 5, then 8. This corpus has 44 chunks. A pool of 48 is the whole collection, so the last retry would send every row to Cohere. That hides ranking mistakes.

The gold chunk was already in the fused list at pool 12. It was ranked badly, not missing. Widening the pool does not fix that. Widening how many chunks Qwen sees does.

The live constants are pool 12, final k `(3, 5, 8)`, and RRF k 60. `Pipeline` stores `final_k`. `ask` still searches once and returns the full fused list. It does not slice by `final_k` and it does not retry. Sufficiency is not wired yet. When that path is added, the pool stays 12 and only final k grows. How equal RRF scores are ordered is ADR 10.

## ADR 8 — Overlap 25 tokens, not 50

Status: accepted

The 50-token overlap was leftover from the 300/50 split. After the body cap moved to 190, 50 tokens was about 26% of a window. A usual overlap is about 10–15%. The active value is 25 (about 13%). The old `CHUNK_OVERLAP = 50` line stays commented in `chunking.py`.

## ADR 9 — Keep the hyphenated form as a BM25 token

Status: accepted

ADR 6 split `AP-5.1` into `ap` and `5.1`, and `6100-TRAVEL` into `6100` and `travel`. A query of `AP-5.1` then shared only `5.1` with `EXP-5.1`. A query of `6100-TRAVEL` missed the exact ledger code.

BM25 still emits those split tokens. It also keeps the hyphenated form, taken from the lowercased text before hyphens become spaces. `AP-5.1` yields `ap-5.1`, `ap`, and `5.1`. `6100-TRAVEL` yields `6100-travel`, `6100`, and `travel`. Dotted numbers such as `5.1` stay one token. There is no second BM25 index. The existing index is rebuilt from Chroma on startup.

## ADR 10 — Break equal RRF scores by cosine rank

Status: accepted

Fusion stays rank-only. `1 / (60 + rank)` is still the score. Raw BM25 scores and cosine distances are not mixed. `hit["distance"]` is unused in the merge.

When two fused scores are equal, sort by cosine rank ascending (a chunk missing from cosine sorts last), then by `chunk_id`. Dict insertion order is not used. A chunk that is cosine rank 1 and BM25 rank 2 stays ahead of a chunk that is cosine rank 2 and BM25 rank 1.

## Not recorded yet

- No `superseded_by` filter at search time. Both accounts-payable versions stay in the index.
- Hybrid search is BM25 plus cosine, merged with RRF, then Cohere `rerank-v4.0-pro`. That Cohere call is not wired into `Pipeline` yet.
- PDFs live in `data/raw/`. Ingestion reads `data/text/`. `data/gold/` is not ingested.
- OCR runs only when a page has no text layer.
