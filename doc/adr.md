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

## Not recorded yet

- Chunk fallback of about 300 characters with 50 characters of overlap, and how a headingless chunk gets its title.
- No `superseded_by` filter at search time. Both accounts-payable versions stay in the index.
- Retrieval sizes: pool 12, then 24, then 48. Final k 3, then 5, then 8. RRF constant 60.
- Hybrid search is BM25 plus cosine, merged with RRF, then Cohere `rerank-v4.0-pro`.
- PDFs live in `data/raw/`. Ingestion reads `data/text/`. `data/gold/` is not ingested.
- OCR runs only when a page has no text layer.
