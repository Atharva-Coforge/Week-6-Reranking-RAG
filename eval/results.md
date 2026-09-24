# Evaluation results

Recorded recall and answer-check results.

Pool size 12. RRF constant 60. Rank-only fusion. Ties break by cosine rank, then `chunk_id`. No `superseded_by` filter.

BM25 now keeps the hyphenated form (`ap-5.1`, `6100-travel`) as well as the split tokens. `$10,000` is still `10000`.

## Hybrid versus vector — `AP-5.1`

`AP-5.1` is an exact section code. BM25 puts both accounts-payable `AP-5.1` chunks first. The extra token `ap-5.1` keeps `EXP-5.1` from outranking them on the shared `5.1`. Cosine still ranks `AP-1.1` first. Fused rank keeps both `AP-5.1` chunks above both `AP-1.1` chunks.

### BM25

1. `ap-us-0001:v1.0:AP-5.1:1`
2. `ap-us-0001:v2.0:AP-5.1:1`
3. `ap-us-0001:v1.0:AP-7.1:2`
4. `ap-us-0001:v2.0:AP-7.1:2`
5. `exp-us-0001:v1.0:EXP-5.1:2`
6. `ap-us-0001:v1.0:AP-6.1:2`
7. `ap-us-0001:v2.0:AP-6.1:2`
8. `ap-us-0001:v1.0:AP-4.1:1`
9. `ap-us-0001:v2.0:AP-4.1:1`
10. `ap-us-0001:v1.0:AP-3.2:1`
11. `ap-us-0001:v2.0:AP-3.2:1`
12. `ap-us-0001:v1.0:AP-1.1:1`

### Cosine

1. `ap-us-0001:v1.0:AP-1.1:1`
2. `ap-us-0001:v2.0:AP-1.1:1`
3. `ap-us-0001:v1.0:AP-5.1:1`
4. `ap-us-0001:v2.0:AP-5.1:1`
5. `ap-us-0001:v1.0:AP-8.1:2`
6. `ap-us-0001:v1.0:AP-4.1:1`
7. `ap-us-0001:v2.0:AP-4.1:1`
8. `ap-us-0001:v1.0:AP-7.1:2`
9. `ap-us-0001:v2.0:AP-7.1:2`
10. `ap-us-0001:v2.0:AP-8.1:2`
11. `ap-us-0001:v2.0:AP-6.1:2`
12. `ap-us-0001:v1.0:AP-6.1:2`

### Fused (RRF)

1. `ap-us-0001:v1.0:AP-5.1:1`
2. `ap-us-0001:v2.0:AP-5.1:1`
3. `ap-us-0001:v1.0:AP-7.1:2`
4. `ap-us-0001:v1.0:AP-1.1:1`
5. `ap-us-0001:v2.0:AP-7.1:2`
6. `ap-us-0001:v1.0:AP-4.1:1`
7. `ap-us-0001:v2.0:AP-4.1:1`
8. `ap-us-0001:v1.0:AP-6.1:2`
9. `ap-us-0001:v2.0:AP-6.1:2`
10. `ap-us-0001:v2.0:AP-1.1:1`
11. `ap-us-0001:v1.0:AP-8.1:2`
12. `exp-us-0001:v1.0:EXP-5.1:2`
13. `ap-us-0001:v2.0:AP-8.1:2`
14. `ap-us-0001:v1.0:AP-3.2:1`
15. `ap-us-0001:v2.0:AP-3.2:1`

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
