# Data-quality diagnosis

Question: `What changed in the invoice approval threshold?`

## Flawed answer

The invoice approval threshold changed from $7,500 (Accounts Payable Invoice Payment Procedure, AP-5.1, v1.0, ap-us-0001-v2.0) to $10,000 (Accounts Payable Invoice Payment Procedure, AP-5.1, v2.0, none).

This answer is flawed for someone who needs the rule. The same section states two thresholds, $7,500 and $10,000. The model did not invent either number.

## Why it is not retrieval or generation

Retrieval returned the chunk that is actually in the corpus, `ap-us-0001:v1.0:AP-5.1:1`, at rank 1. Generation repeated the text it was given.

## Source

`data/raw/ap-us-0001-v1.0.pdf`, section AP-5.1, says an invoice of $7,500 or more needs finance-manager approval. `data/raw/ap-us-0001-v2.0.pdf`, same section, says $10,000. v1.0 is the outdated duplicate. That file is the defect.
## Ask log

```
query: What changed in the invoice approval threshold?
question_type: what-changed
bm25: 12
  1. ap-us-0001:v1.0:AP-5.1:1
  2. ap-us-0001:v2.0:AP-5.1:1
  3. ap-us-0001:v2.0:AP-8.1:2
  4. ap-us-0001:v1.0:AP-8.1:2
  5. ap-us-0001:v1.0:AP-7.1:2
  6. ap-us-0001:v2.0:AP-7.1:2
  7. exp-us-0001:v1.0:EXP-5.2:2
  8. exp-us-0001:v1.0:EXP-6.1:2
  9. exp-us-0001:v1.0:EXP-5.1:2
  10. ap-us-0001:v1.0:AP-4.1:1
  11. ap-us-0001:v2.0:AP-4.1:1
  12. exp-us-0001:v1.0:EXP-7.1:2
cosine: 12
  1. ap-us-0001:v1.0:AP-5.1:1
  2. ap-us-0001:v2.0:AP-5.1:1
  3. ap-us-0001:v1.0:AP-7.1:2
  4. ap-us-0001:v2.0:AP-7.1:2
  5. ap-us-0001:v2.0:AP-1.1:1
  6. ap-us-0001:v1.0:AP-8.1:2
  7. ap-us-0001:v1.0:AP-7.1:2:2
  8. ap-us-0001:v2.0:AP-7.1:2:2
  9. ap-us-0001:v1.0:AP-1.1:1
  10. ap-us-0001:v2.0:AP-8.1:2
  11. ap-us-0001:v1.0:AP-3.1:1
  12. ap-us-0001:v2.0:AP-3.1:1
rrf: 18
  1. ap-us-0001:v1.0:AP-5.1:1
  2. ap-us-0001:v2.0:AP-5.1:1
  3. ap-us-0001:v1.0:AP-7.1:2
  4. ap-us-0001:v2.0:AP-7.1:2
  5. ap-us-0001:v1.0:AP-8.1:2
  6. ap-us-0001:v2.0:AP-8.1:2
  7. ap-us-0001:v2.0:AP-1.1:1
  8. ap-us-0001:v1.0:AP-7.1:2:2
  9. exp-us-0001:v1.0:EXP-5.2:2
  10. ap-us-0001:v2.0:AP-7.1:2:2
  11. exp-us-0001:v1.0:EXP-6.1:2
  12. ap-us-0001:v1.0:AP-1.1:1
  13. exp-us-0001:v1.0:EXP-5.1:2
  14. ap-us-0001:v1.0:AP-4.1:1
  15. ap-us-0001:v1.0:AP-3.1:1
  16. ap-us-0001:v2.0:AP-4.1:1
  17. ap-us-0001:v2.0:AP-3.1:1
  18. exp-us-0001:v1.0:EXP-7.1:2
cohere: 18
  1. ap-us-0001:v1.0:AP-5.1:1
  2. ap-us-0001:v2.0:AP-5.1:1
  3. ap-us-0001:v1.0:AP-1.1:1
  4. ap-us-0001:v2.0:AP-1.1:1
  5. exp-us-0001:v1.0:EXP-5.2:2
  6. ap-us-0001:v1.0:AP-7.1:2
  7. ap-us-0001:v2.0:AP-7.1:2
  8. exp-us-0001:v1.0:EXP-5.1:2
  9. ap-us-0001:v1.0:AP-4.1:1
  10. ap-us-0001:v2.0:AP-4.1:1
  11. exp-us-0001:v1.0:EXP-6.1:2
  12. ap-us-0001:v1.0:AP-3.1:1
  13. ap-us-0001:v2.0:AP-3.1:1
  14. ap-us-0001:v1.0:AP-8.1:2
  15. ap-us-0001:v1.0:AP-7.1:2:2
  16. ap-us-0001:v2.0:AP-7.1:2:2
  17. ap-us-0001:v2.0:AP-8.1:2
  18. exp-us-0001:v1.0:EXP-7.1:2
final_k_used: 8
```

`question_type` is `what-changed`. The stale v1 chunk `ap-us-0001:v1.0:AP-5.1:1` is rank 1 on BM25, cosine, RRF, and Cohere. `final_k_used` is 8, so that chunk was sent to Qwen.

## Answer

```
The invoice approval threshold changed from $7,500 (Accounts Payable Invoice Payment Procedure, AP-5.1, v1.0, ap-us-0001-v2.0) to $10,000 (Accounts Payable Invoice Payment Procedure, AP-5.1, v2.0, none).
(Accounts Payable Invoice Payment Procedure, AP-5.1, v1.0, ap-us-0001-v2.0)
(Accounts Payable Invoice Payment Procedure, AP-5.1, v2.0, none)
(Accounts Payable Invoice Payment Procedure, AP-1.1, v1.0, ap-us-0001-v2.0)
(Accounts Payable Invoice Payment Procedure, AP-1.1, v2.0, none)
(Employee Expense Reimbursement Procedure, EXP-5.2, v1.0, none)
(Accounts Payable Invoice Payment Procedure, AP-7.1, v1.0, ap-us-0001-v2.0)
(Accounts Payable Invoice Payment Procedure, AP-7.1, v2.0, none)
(Employee Expense Reimbursement Procedure, EXP-5.1, v1.0, none)
```

The answer cites the old value and the new value. The same log and answer are saved in `eval/ask-approval-threshold.md`.

## Conclusion

Retrieval was right. It returned the chunk that is in the corpus, `ap-us-0001:v1.0:AP-5.1:1`.

Generation was right. It used the text it was given and stated both `$7,500` and `$10,000`.

The defect is the outdated file in `data/`, not the retriever or the model. The conflicting number is in `data/raw/ap-us-0001-v1.0.pdf`.
