# Evaluation results

Recorded recall and answer-check results.

Pool size 12. RRF constant 60. Rank-only fusion. Ties break by cosine rank, then `chunk_id`. No `superseded_by` filter.

BM25 now keeps the hyphenated form (`ap-5.1`, `6100-travel`) as well as the split tokens. `$10,000` is still `10000`.

## Recall

16 questions in `eval/questions.json`. 21 expected chunk ids. A hit is an expected id inside that list's pool. The pool is 12 for BM25 and 12 for cosine. Fused is the RRF merge of those two lists. `tests/test_recall.py` checks the fused list and passed 16/16.

| List | Expected ids found | Recall |
| ---- | ------------------ | ------ |
| BM25 | 21/21 | 1.00 |
| Cosine | 19/21 | 0.90 |
| Fused (RRF) | 21/21 | 1.00 |

Cosine missed `exp-us-0001:v1.0:EXP-8.1:2` (`What does code EXP-8.1 say?`) and `exp-us-0001:v1.0:EXP-4.5:1` (`Quote the rule numbered EXP-4.5.`). BM25 ranked both first, so both are in the fused list.

## Hybrid versus vector — `What is section AP-5.1 about?`

`AP-5.1` is an exact section code. BM25 puts both accounts-payable `AP-5.1` chunks first. Cosine ranks `AP-1.1` first and does not reach either `AP-5.1` chunk until ranks 5 and 6. Fused rank keeps both `AP-5.1` chunks above both `AP-1.1` chunks.

### BM25

1. `ap-us-0001:v1.0:AP-5.1:1`
2. `ap-us-0001:v2.0:AP-5.1:1`
3. `ap-us-0001:v1.0:AP-7.1:2`
4. `ap-us-0001:v2.0:AP-7.1:2`
5. `exp-us-0001:v1.0:EXP-5.1:2`
6. `ap-us-0001:v1.0:AP-3.2:1`
7. `ap-us-0001:v2.0:AP-3.2:1`
8. `exp-us-0001:v1.0:EXP-4.1:1`
9. `exp-us-0001:v1.0:EXP-8.1:2`
10. `ap-us-0001:v1.0:AP-6.1:2`
11. `ap-us-0001:v2.0:AP-6.1:2`
12. `ap-us-0001:v1.0:AP-4.1:1`

### Cosine

1. `ap-us-0001:v1.0:AP-1.1:1`
2. `ap-us-0001:v2.0:AP-1.1:1`
3. `ap-us-0001:v1.0:AP-7.1:2`
4. `ap-us-0001:v2.0:AP-7.1:2`
5. `ap-us-0001:v2.0:AP-5.1:1`
6. `ap-us-0001:v1.0:AP-5.1:1`
7. `ap-us-0001:v1.0:AP-8.1:2`
8. `exp-us-0001:v1.0:EXP-1.1:1`
9. `ap-us-0001:v1.0:AP-3.2:1`
10. `ap-us-0001:v2.0:AP-3.2:1`
11. `ap-us-0001:v2.0:AP-8.1:2`
12. `ap-us-0001:v1.0:AP-3.1:1`

### Fused (RRF)

1. `ap-us-0001:v1.0:AP-7.1:2`
2. `ap-us-0001:v1.0:AP-5.1:1`
3. `ap-us-0001:v2.0:AP-5.1:1`
4. `ap-us-0001:v2.0:AP-7.1:2`
5. `ap-us-0001:v1.0:AP-3.2:1`
6. `ap-us-0001:v2.0:AP-3.2:1`
7. `ap-us-0001:v1.0:AP-1.1:1`
8. `ap-us-0001:v2.0:AP-1.1:1`
9. `exp-us-0001:v1.0:EXP-5.1:2`
10. `ap-us-0001:v1.0:AP-8.1:2`
11. `exp-us-0001:v1.0:EXP-1.1:1`
12. `exp-us-0001:v1.0:EXP-4.1:1`
13. `exp-us-0001:v1.0:EXP-8.1:2`
14. `ap-us-0001:v1.0:AP-6.1:2`
15. `ap-us-0001:v2.0:AP-8.1:2`
16. `ap-us-0001:v2.0:AP-6.1:2`
17. `ap-us-0001:v1.0:AP-3.1:1`
18. `ap-us-0001:v1.0:AP-4.1:1`

## Hybrid versus vector — airport / `6100-TRAVEL`

Question: `Which airport car service rule uses ledger code 6100-TRAVEL?`

The month-end window that contains `6100-TRAVEL` (`mec-us-0001:v1.0:page-1:1:4`) is rank 1 on BM25, cosine, and fused. The hyphenated token `6100-travel` is what locks that row for BM25.

### BM25

1. `mec-us-0001:v1.0:page-1:1:4`
2. `exp-us-0001:v1.0:EXP-4.6:2`
3. `exp-us-0001:v1.0:EXP-3.3:1`
4. `mec-us-0001:v1.0:page-1:1:2`
5. `mec-us-0001:v1.0:page-1:1:3`
6. `mec-us-0001:v1.0:page-2:2`
7. `ap-us-0001:v2.0:AP-1.1:1`
8. `exp-us-0001:v1.0:EXP-8.1:2`
9. `mec-us-0001:v1.0:page-1:1`

### Cosine

1. `mec-us-0001:v1.0:page-1:1:4`
2. `exp-us-0001:v1.0:EXP-4.6:2`
3. `ap-us-0001:v2.0:AP-1.1:1`
4. `ap-us-0001:v1.0:AP-1.1:1`
5. `ap-us-0001:v1.0:AP-7.1:2`
6. `ap-us-0001:v2.0:AP-7.1:2`
7. `ap-us-0001:v2.0:AP-5.1:1`
8. `exp-us-0001:v1.0:EXP-1.1:1`
9. `ap-us-0001:v1.0:AP-5.1:1`
10. `mec-us-0001:v1.0:page-1:1:3`
11. `ap-us-0001:v1.0:AP-3.1:1`
12. `ap-us-0001:v2.0:AP-3.1:1`

### Fused (RRF)

1. `mec-us-0001:v1.0:page-1:1:4`
2. `exp-us-0001:v1.0:EXP-4.6:2`
3. `ap-us-0001:v2.0:AP-1.1:1`
4. `mec-us-0001:v1.0:page-1:1:3`
5. `exp-us-0001:v1.0:EXP-3.3:1`
6. `ap-us-0001:v1.0:AP-1.1:1`
7. `mec-us-0001:v1.0:page-1:1:2`
8. `ap-us-0001:v1.0:AP-7.1:2`
9. `ap-us-0001:v2.0:AP-7.1:2`
10. `mec-us-0001:v1.0:page-2:2`
11. `ap-us-0001:v2.0:AP-5.1:1`
12. `exp-us-0001:v1.0:EXP-1.1:1`
13. `exp-us-0001:v1.0:EXP-8.1:2`
14. `ap-us-0001:v1.0:AP-5.1:1`
15. `mec-us-0001:v1.0:page-1:1`
16. `ap-us-0001:v1.0:AP-3.1:1`
17. `ap-us-0001:v2.0:AP-3.1:1`
