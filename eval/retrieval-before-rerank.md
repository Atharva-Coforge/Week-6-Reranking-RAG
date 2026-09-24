# Retrieval before rerank

Question: `What is section AP-5.1 about?`

BM25 pool: 12 (cap 12). 
Cosine / vector pool: 12 (cap 12). 
Fused: 18. RRF is the union of the two pools, 
so it can be longer than 12 when the lists do not fully overlap.

A later Cohere step receives the question plus the fused raw texts, 
in fused order. No vectors. No prefixes.

# BM25

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

## 4. `ap-us-0001:v2.0:AP-7.1:2`

- section: `AP-7.1`
- version: `v2.0`
- superseded_by: `none`

AP-7.1 Exception and escalation Where a discrepancy under Section AP-3.2 remains unresolved, or where an approval required under Section AP-5.1 has not been obtained as the payment period in Section AP-6.1 approaches, the AP supervisor escalates the invoice to the finance manager. The finance manager may approve payment, request further information, or direct that the invoice be returned to the vendor. Escalation is a written referral. The AP supervisor records the invoice number, the vendor, the amount, the date the three-way match failed or the approval was found missing, and the question the finance manager must decide. A spoken request does not start the escalation, and it does not release the hold. The finance manager answers in writing on the invoice record. Approving payment lets the clerk schedule it. Asking for further

## 5. `exp-us-0001:v1.0:EXP-5.1:2`

- section: `EXP-5.1`
- version: `v1.0`
- superseded_by: `none`

EXP-5.1 Submission timing An employee files a claim within 30 days of the date the cost was incurred. A claim filed after that window needs supervisor approval before it is processed.

## 6. `ap-us-0001:v1.0:AP-3.2:1`

- section: `AP-3.2`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-3.2 Discrepancy handling Where the three-way match fails on quantity, price, or description, the invoice is placed on hold and sent to the AP supervisor. The supervisor works with the vendor or the requesting department until the discrepancy is resolved. An invoice on hold does not start the payment period in Section AP-6.1 until the match is confirmed.

## 7. `ap-us-0001:v2.0:AP-3.2:1`

- section: `AP-3.2`
- version: `v2.0`
- superseded_by: `none`

AP-3.2 Discrepancy handling Where the three-way match fails on quantity, price, or description, the invoice is placed on hold and sent to the AP supervisor. The supervisor works with the vendor or the requesting department until the discrepancy is resolved. An invoice on hold does not start the payment period in Section AP-6.1 until the match is confirmed.

## 8. `exp-us-0001:v1.0:EXP-4.1:1`

- section: `EXP-4.1`
- version: `v1.0`
- superseded_by: `none`

EXP-4.1 Meal expense caps A meal cost of $75 or less per meal is repayable when the claim is valid and, where Section EXP-3.2 requires it, a slip is attached. The cap applies to each meal. It does not limit what the employee may spend on meals across a full day.

## 9. `exp-us-0001:v1.0:EXP-8.1:2`

- section: `EXP-8.1`
- version: `v1.0`
- superseded_by: `none`

EXP-8.1 Staff celebrations Alcohol served at an internal staff celebration can be submitted for reimbursement from the site social fund. That request is paid outside the business-meal claim, and it does not follow the meal cap in Section EXP-4.1. The social fund pays only while a balance remains. Filed copy. Signature of Avery Chen, expense audit lead. The signature image carries no additional rule.

## 10. `ap-us-0001:v1.0:AP-6.1:2`

- section: `AP-6.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-6.1 Payment timing An invoice is paid within 45 days of the date the three-way match is confirmed. Where an invoice cannot be paid inside that period, the AP clerk records the reason for the delay and notifies the AP supervisor.

## 11. `ap-us-0001:v2.0:AP-6.1:2`

- section: `AP-6.1`
- version: `v2.0`
- superseded_by: `none`

AP-6.1 Payment timing An invoice is paid within 30 days of the date the three-way match is confirmed. Where an invoice cannot be paid inside that period, the AP clerk records the reason for the delay and notifies the AP supervisor.

## 12. `ap-us-0001:v1.0:AP-4.1:1`

- section: `AP-4.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-4.1 Intake and logging An invoice is logged when it is received. The AP clerk records the invoice date, vendor, amount, and purchase order number. An invoice with no purchase order is logged as unmatched and sent to the AP supervisor before any further step.

# Cosine (vector)

## 1. `ap-us-0001:v1.0:AP-1.1:1`

- section: `AP-1.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-1.1 Purpose This procedure (ap-us-0001, v1.0) governs how Halden & Co. reviews, checks, and pays vendor invoices. Amounts are in USD. It applies to every invoice any business unit submits for payment. This version is replaced by ap-us-0001-v2.0 and must not be used for payment decisions after 2025-09-01.

## 2. `ap-us-0001:v2.0:AP-1.1:1`

- section: `AP-1.1`
- version: `v2.0`
- superseded_by: `none`

AP-1.1 Purpose This procedure (ap-us-0001, v2.0) governs how Halden & Co. reviews, checks, and pays vendor invoices. Amounts are in USD. It applies to every invoice any business unit submits for payment. This version replaces ap-us-0001-v1.0, effective 2023-01-01, and is the current rule for payment decisions.

## 3. `ap-us-0001:v1.0:AP-7.1:2`

- section: `AP-7.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-7.1 Exception and escalation Where a discrepancy under Section AP-3.2 remains unresolved, or where an approval required under Section AP-5.1 has not been obtained as the payment period in Section AP-6.1 approaches, the AP supervisor escalates the invoice to the finance manager. The finance manager may approve payment, request further information, or direct that the invoice be returned to the vendor. Escalation is a written referral. The AP supervisor records the invoice number, the vendor, the amount, the date the three-way match failed or the approval was found missing, and the question the finance manager must decide. A spoken request does not start the escalation, and it does not release the hold. The finance manager answers in writing on the invoice record. Approving payment lets the clerk schedule it. Asking for further

## 4. `ap-us-0001:v2.0:AP-7.1:2`

- section: `AP-7.1`
- version: `v2.0`
- superseded_by: `none`

AP-7.1 Exception and escalation Where a discrepancy under Section AP-3.2 remains unresolved, or where an approval required under Section AP-5.1 has not been obtained as the payment period in Section AP-6.1 approaches, the AP supervisor escalates the invoice to the finance manager. The finance manager may approve payment, request further information, or direct that the invoice be returned to the vendor. Escalation is a written referral. The AP supervisor records the invoice number, the vendor, the amount, the date the three-way match failed or the approval was found missing, and the question the finance manager must decide. A spoken request does not start the escalation, and it does not release the hold. The finance manager answers in writing on the invoice record. Approving payment lets the clerk schedule it. Asking for further

## 5. `ap-us-0001:v2.0:AP-5.1:1`

- section: `AP-5.1`
- version: `v2.0`
- superseded_by: `none`

AP-5.1 Approval thresholds An invoice of $10,000 or more requires the approval of the finance manager before payment. The AP clerk records that approval on the invoice before release. An invoice below this threshold may be released by the AP clerk after a successful three-way match, with no further approval.

## 6. `ap-us-0001:v1.0:AP-5.1:1`

- section: `AP-5.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-5.1 Approval thresholds An invoice of $7,500 or more requires the approval of the finance manager before payment. The AP clerk records that approval on the invoice before release. An invoice below this threshold may be released by the AP clerk after a successful three-way match, with no further approval.

## 7. `ap-us-0001:v1.0:AP-8.1:2`

- section: `AP-8.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-8.1 Recording and outcome The match, the approval, and the payment are stored on the original invoice, including the date paid, the amount paid, and any approver. Any duplicate, discrepancy, or escalation stays with the invoice for audit. Image stamp for the replaced version.

## 8. `exp-us-0001:v1.0:EXP-1.1:1`

- section: `EXP-1.1`
- version: `v1.0`
- superseded_by: `none`

EXP-1.1 Purpose This procedure (exp-us-0001, v1.0) governs how Halden & Co. employees submit, review, and receive repayment of business costs. Amounts are in USD. It applies to every employee who incurs a business cost while doing the job. It is effective 2025-09-01, and no later version supersedes it.

## 9. `ap-us-0001:v1.0:AP-3.2:1`

- section: `AP-3.2`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-3.2 Discrepancy handling Where the three-way match fails on quantity, price, or description, the invoice is placed on hold and sent to the AP supervisor. The supervisor works with the vendor or the requesting department until the discrepancy is resolved. An invoice on hold does not start the payment period in Section AP-6.1 until the match is confirmed.

## 10. `ap-us-0001:v2.0:AP-3.2:1`

- section: `AP-3.2`
- version: `v2.0`
- superseded_by: `none`

AP-3.2 Discrepancy handling Where the three-way match fails on quantity, price, or description, the invoice is placed on hold and sent to the AP supervisor. The supervisor works with the vendor or the requesting department until the discrepancy is resolved. An invoice on hold does not start the payment period in Section AP-6.1 until the match is confirmed.

## 11. `ap-us-0001:v2.0:AP-8.1:2`

- section: `AP-8.1`
- version: `v2.0`
- superseded_by: `none`

AP-8.1 Recording and outcome The match, the approval, and the payment are stored on the original invoice, including the date paid, the amount paid, and any approver. Any duplicate, discrepancy, or escalation stays with the invoice for audit.

## 12. `ap-us-0001:v2.0:AP-3.1:1`

- section: `AP-3.1`
- version: `v2.0`
- superseded_by: `none`

AP-3.1 Matching requirements An invoice is paid only when the purchase order, the delivery record, and the invoice agree on vendor, item description, quantity, and price. The AP clerk performs this three-way match at intake and records the result on the invoice before payment.

# Fused (reranker input)

## 1. `ap-us-0001:v1.0:AP-7.1:2`

- section: `AP-7.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-7.1 Exception and escalation Where a discrepancy under Section AP-3.2 remains unresolved, or where an approval required under Section AP-5.1 has not been obtained as the payment period in Section AP-6.1 approaches, the AP supervisor escalates the invoice to the finance manager. The finance manager may approve payment, request further information, or direct that the invoice be returned to the vendor. Escalation is a written referral. The AP supervisor records the invoice number, the vendor, the amount, the date the three-way match failed or the approval was found missing, and the question the finance manager must decide. A spoken request does not start the escalation, and it does not release the hold. The finance manager answers in writing on the invoice record. Approving payment lets the clerk schedule it. Asking for further

## 2. `ap-us-0001:v1.0:AP-5.1:1`

- section: `AP-5.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-5.1 Approval thresholds An invoice of $7,500 or more requires the approval of the finance manager before payment. The AP clerk records that approval on the invoice before release. An invoice below this threshold may be released by the AP clerk after a successful three-way match, with no further approval.

## 3. `ap-us-0001:v2.0:AP-5.1:1`

- section: `AP-5.1`
- version: `v2.0`
- superseded_by: `none`

AP-5.1 Approval thresholds An invoice of $10,000 or more requires the approval of the finance manager before payment. The AP clerk records that approval on the invoice before release. An invoice below this threshold may be released by the AP clerk after a successful three-way match, with no further approval.

## 4. `ap-us-0001:v2.0:AP-7.1:2`

- section: `AP-7.1`
- version: `v2.0`
- superseded_by: `none`

AP-7.1 Exception and escalation Where a discrepancy under Section AP-3.2 remains unresolved, or where an approval required under Section AP-5.1 has not been obtained as the payment period in Section AP-6.1 approaches, the AP supervisor escalates the invoice to the finance manager. The finance manager may approve payment, request further information, or direct that the invoice be returned to the vendor. Escalation is a written referral. The AP supervisor records the invoice number, the vendor, the amount, the date the three-way match failed or the approval was found missing, and the question the finance manager must decide. A spoken request does not start the escalation, and it does not release the hold. The finance manager answers in writing on the invoice record. Approving payment lets the clerk schedule it. Asking for further

## 5. `ap-us-0001:v1.0:AP-3.2:1`

- section: `AP-3.2`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-3.2 Discrepancy handling Where the three-way match fails on quantity, price, or description, the invoice is placed on hold and sent to the AP supervisor. The supervisor works with the vendor or the requesting department until the discrepancy is resolved. An invoice on hold does not start the payment period in Section AP-6.1 until the match is confirmed.

## 6. `ap-us-0001:v2.0:AP-3.2:1`

- section: `AP-3.2`
- version: `v2.0`
- superseded_by: `none`

AP-3.2 Discrepancy handling Where the three-way match fails on quantity, price, or description, the invoice is placed on hold and sent to the AP supervisor. The supervisor works with the vendor or the requesting department until the discrepancy is resolved. An invoice on hold does not start the payment period in Section AP-6.1 until the match is confirmed.

## 7. `ap-us-0001:v1.0:AP-1.1:1`

- section: `AP-1.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-1.1 Purpose This procedure (ap-us-0001, v1.0) governs how Halden & Co. reviews, checks, and pays vendor invoices. Amounts are in USD. It applies to every invoice any business unit submits for payment. This version is replaced by ap-us-0001-v2.0 and must not be used for payment decisions after 2025-09-01.

## 8. `ap-us-0001:v2.0:AP-1.1:1`

- section: `AP-1.1`
- version: `v2.0`
- superseded_by: `none`

AP-1.1 Purpose This procedure (ap-us-0001, v2.0) governs how Halden & Co. reviews, checks, and pays vendor invoices. Amounts are in USD. It applies to every invoice any business unit submits for payment. This version replaces ap-us-0001-v1.0, effective 2023-01-01, and is the current rule for payment decisions.

## 9. `exp-us-0001:v1.0:EXP-5.1:2`

- section: `EXP-5.1`
- version: `v1.0`
- superseded_by: `none`

EXP-5.1 Submission timing An employee files a claim within 30 days of the date the cost was incurred. A claim filed after that window needs supervisor approval before it is processed.

## 10. `ap-us-0001:v1.0:AP-8.1:2`

- section: `AP-8.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-8.1 Recording and outcome The match, the approval, and the payment are stored on the original invoice, including the date paid, the amount paid, and any approver. Any duplicate, discrepancy, or escalation stays with the invoice for audit. Image stamp for the replaced version.

## 11. `exp-us-0001:v1.0:EXP-1.1:1`

- section: `EXP-1.1`
- version: `v1.0`
- superseded_by: `none`

EXP-1.1 Purpose This procedure (exp-us-0001, v1.0) governs how Halden & Co. employees submit, review, and receive repayment of business costs. Amounts are in USD. It applies to every employee who incurs a business cost while doing the job. It is effective 2025-09-01, and no later version supersedes it.

## 12. `exp-us-0001:v1.0:EXP-4.1:1`

- section: `EXP-4.1`
- version: `v1.0`
- superseded_by: `none`

EXP-4.1 Meal expense caps A meal cost of $75 or less per meal is repayable when the claim is valid and, where Section EXP-3.2 requires it, a slip is attached. The cap applies to each meal. It does not limit what the employee may spend on meals across a full day.

## 13. `exp-us-0001:v1.0:EXP-8.1:2`

- section: `EXP-8.1`
- version: `v1.0`
- superseded_by: `none`

EXP-8.1 Staff celebrations Alcohol served at an internal staff celebration can be submitted for reimbursement from the site social fund. That request is paid outside the business-meal claim, and it does not follow the meal cap in Section EXP-4.1. The social fund pays only while a balance remains. Filed copy. Signature of Avery Chen, expense audit lead. The signature image carries no additional rule.

## 14. `ap-us-0001:v1.0:AP-6.1:2`

- section: `AP-6.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-6.1 Payment timing An invoice is paid within 45 days of the date the three-way match is confirmed. Where an invoice cannot be paid inside that period, the AP clerk records the reason for the delay and notifies the AP supervisor.

## 15. `ap-us-0001:v2.0:AP-8.1:2`

- section: `AP-8.1`
- version: `v2.0`
- superseded_by: `none`

AP-8.1 Recording and outcome The match, the approval, and the payment are stored on the original invoice, including the date paid, the amount paid, and any approver. Any duplicate, discrepancy, or escalation stays with the invoice for audit.

## 16. `ap-us-0001:v2.0:AP-6.1:2`

- section: `AP-6.1`
- version: `v2.0`
- superseded_by: `none`

AP-6.1 Payment timing An invoice is paid within 30 days of the date the three-way match is confirmed. Where an invoice cannot be paid inside that period, the AP clerk records the reason for the delay and notifies the AP supervisor.

## 17. `ap-us-0001:v2.0:AP-3.1:1`

- section: `AP-3.1`
- version: `v2.0`
- superseded_by: `none`

AP-3.1 Matching requirements An invoice is paid only when the purchase order, the delivery record, and the invoice agree on vendor, item description, quantity, and price. The AP clerk performs this three-way match at intake and records the result on the invoice before payment.

## 18. `ap-us-0001:v1.0:AP-4.1:1`

- section: `AP-4.1`
- version: `v1.0`
- superseded_by: `ap-us-0001-v2.0`

AP-4.1 Intake and logging An invoice is logged when it is received. The AP clerk records the invoice date, vendor, amount, and purchase order number. An invoice with no purchase order is logged as unmatched and sent to the AP supervisor before any further step.
