# Ask: What changed in the invoice approval threshold?

Verbatim output of `uv run python -m src.main ask "What changed in the invoice approval threshold?"`.

```
cache miss
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
answer
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
