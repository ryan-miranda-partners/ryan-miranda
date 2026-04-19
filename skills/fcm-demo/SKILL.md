---
name: fcm-demo
description: |
  Use when: "fcm demo", "test the demo", "validate extraction for FCM", "demo prep".
  Proactive: before any meeting with Mark or Fernbridge.
---

## Procedure

1. Check that the Excel workbench is functional (upload endpoint responds).
2. Get a sample FCM file (MSFS extract, EOD report, or capital database).
3. Upload via POST /api/v2/excel/upload.
4. Run analysis: POST /api/v2/excel/analyze with a financial question.
5. Run extraction: POST /api/v2/excel/extract with documentType: "eod_reconciliation".
6. Time each step. Compare to manual workflow (target: 5 min vs 4 hours).
7. Document what worked, what broke, what needs fixing.

## Output

```
FCM DEMO VALIDATION — [date]

STEP 1 (upload): [pass/fail] — [time]
STEP 2 (analyze): [pass/fail] — [time] — [quality of AI response]
STEP 3 (extract): [pass/fail] — [time] — [fields extracted / expected]

TOTAL TIME: [X min]
MANUAL BASELINE: [~4 hours]

ISSUES:
- [what broke]

DEMO READY: [YES / NO — fix these first: ...]
```
