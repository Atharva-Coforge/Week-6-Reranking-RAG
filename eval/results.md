# Evaluation results

Recorded recall and answer-check results.

## Hybrid versus vector — `AP-5.1`

Pool size 12. RRF constant 60. No `superseded_by` filter.

`AP-5.1` is an exact section code. BM25 put both accounts-payable `AP-5.1` chunks first. Cosine ranked `AP-1.1` first and `AP-5.1` third and fourth. RRF used rank only and put both `AP-5.1` versions back at the top. `EXP-5.1` appears in BM25 (the `5.1` token) and not in cosine; fusion keeps it.

### BM25

1. `ap-us-0001:v1.0:AP-5.1:1`
2. `ap-us-0001:v2.0:AP-5.1:1`
3. `exp-us-0001:v1.0:EXP-5.1:2`
4. `ap-us-0001:v1.0:AP-7.1:2`
5. `ap-us-0001:v2.0:AP-7.1:2`
6. `ap-us-0001:v1.0:AP-6.1:2`
7. `ap-us-0001:v2.0:AP-6.1:2`
8. `ap-us-0001:v1.0:AP-4.1:1`
9. `ap-us-0001:v2.0:AP-4.1:1`
10. `ap-us-0001:v2.0:AP-1.1:1`
11. `ap-us-0001:v1.0:AP-1.1:1`
12. `ap-us-0001:v1.0:AP-3.2:1`

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
3. `ap-us-0001:v1.0:AP-1.1:1`
4. `ap-us-0001:v2.0:AP-1.1:1`
5. `ap-us-0001:v1.0:AP-7.1:2`
6. `ap-us-0001:v2.0:AP-7.1:2`
7. `ap-us-0001:v1.0:AP-4.1:1`
8. `ap-us-0001:v2.0:AP-4.1:1`
9. `ap-us-0001:v1.0:AP-6.1:2`
10. `ap-us-0001:v2.0:AP-6.1:2`
11. `exp-us-0001:v1.0:EXP-5.1:2`
12. `ap-us-0001:v1.0:AP-8.1:2`
13. `ap-us-0001:v2.0:AP-8.1:2`
14. `ap-us-0001:v1.0:AP-3.2:1`
