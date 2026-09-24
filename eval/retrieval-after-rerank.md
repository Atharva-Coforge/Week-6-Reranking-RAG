# Retrieval after rerank

Question: `What is section AP-5.1 about?`

Pool 12 per search. Final k 3. 
Compare this order with `eval/retrieval-before-rerank.md`.

## Reranked (Cohere)

1. `ap-us-0001:v1.0:AP-5.1:1`
2. `ap-us-0001:v2.0:AP-5.1:1`
3. `ap-us-0001:v1.0:AP-7.1:2`
4. `ap-us-0001:v2.0:AP-7.1:2`
5. `ap-us-0001:v1.0:AP-3.2:1`
6. `ap-us-0001:v2.0:AP-3.2:1`
7. `ap-us-0001:v2.0:AP-3.1:1`
8. `ap-us-0001:v1.0:AP-6.1:2`
9. `ap-us-0001:v2.0:AP-6.1:2`
10. `ap-us-0001:v1.0:AP-4.1:1`
11. `ap-us-0001:v2.0:AP-1.1:1`
12. `ap-us-0001:v1.0:AP-1.1:1`
13. `ap-us-0001:v1.0:AP-8.1:2`
14. `ap-us-0001:v2.0:AP-8.1:2`
15. `exp-us-0001:v1.0:EXP-5.1:2`
16. `exp-us-0001:v1.0:EXP-4.1:1`
17. `exp-us-0001:v1.0:EXP-8.1:2`
18. `exp-us-0001:v1.0:EXP-1.1:1`

## Final

## 1. `ap-us-0001:v1.0:AP-5.1:1`

- section: `AP-5.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-5.1 Approval thresholds An invoice of $7,500 or more requires the approval of the finance manager before payment. The AP clerk records that approval on the invoice before release. An invoice below this threshold may be released by the AP clerk after a successful three-way match, with no further approval.

## 2. `ap-us-0001:v2.0:AP-5.1:1`

- section: `AP-5.1`
- version: `v2.0`
- superseded_by: `none`

AP-5.1 Approval thresholds An invoice of $10,000 or more requires the approval of the finance manager before payment. The AP clerk records that approval on the invoice before release. An invoice below this threshold may be released by the AP clerk after a successful three-way match, with no further approval.

## 3. `ap-us-0001:v1.0:AP-7.1:2`

- section: `AP-7.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-7.1 Exception and escalation Where a discrepancy under Section AP-3.2 remains unresolved, or where an approval required under Section AP-5.1 has not been obtained as the payment period in Section AP-6.1 approaches, the AP supervisor escalates the invoice to the finance manager. The finance manager may approve payment, request further information, or direct that the invoice be returned to the vendor. Escalation is a written referral. The AP supervisor records the invoice number, the vendor, the amount, the date the three-way match failed or the approval was found missing, and the question the finance manager must decide. A spoken request does not start the escalation, and it does not release the hold. The finance manager answers in writing on the invoice record. Approving payment lets the clerk schedule it. Asking for further
