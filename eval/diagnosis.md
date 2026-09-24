# Data-quality diagnosis

Question: `What changed in the invoice approval threshold?`

The question is a what-changed question. A rule-in-force question would cite only the current version and hide the conflict.

## Answer

The invoice approval threshold changed from $7,500 (Accounts Payable Invoice Payment Procedure, AP-5.1, v1.0, ap-us-0001-v2.0) to $10,000 (Accounts Payable Invoice Payment Procedure, AP-5.1, v2.0, none).

The answer cites the old value and the new value.

## Log

`question_type: what-changed`. The stale v1 chunk was retrieved.

Cohere order, first two:

1. `ap-us-0001:v1.0:AP-5.1:1`
2. `ap-us-0001:v2.0:AP-5.1:1`

Both chunks are also rank 1 and 2 on BM25, cosine, and RRF. `final_k_used: 8`, so both were sent to Qwen.

## Source

`data/raw/ap-us-0001-v1.0.pdf` contains `$7,500` in AP-5.1 and does not contain `$10,000`. The parsed text of v2, `data/text/ap-us-0001-v2.0.md`, contains `$10,000` in AP-5.1. `data/gold/` is not in this checkout, so the gold PDF was not opened.

## Conclusion

Retrieval was right. It returned the chunk that is in the corpus, `ap-us-0001:v1.0:AP-5.1:1`.

Generation was right. It used the text it was given and stated both `$7,500` and `$10,000`.

The defect is the outdated file in `data/`, not the retriever or the model. The conflicting number is in `data/raw/ap-us-0001-v1.0.pdf`.
