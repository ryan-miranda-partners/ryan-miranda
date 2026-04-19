---
name: extract-test
description: |
  Use when: "test extraction", "test template", "try extracting", after modifying extraction prompts.
  Proactive: after any change to services/extractionTemplates/.
---

## Procedure

1. Identify the template to test (credit agreement, 10-K, EOD reconciliation, or auto-detect).
2. Get a test document (upload, file path, or paste text).
3. Call the extraction endpoint: POST /api/v2/excel/extract with the document content.
4. Review the results:
   - Were required fields extracted?
   - Are values accurate (spot-check 5 fields against the source)?
   - What's missing?
   - What's hallucinated?
5. Score: fields extracted / total fields, accuracy of extracted values.
6. If accuracy < 80%, suggest prompt improvements to the extraction template.

## Output

```
EXTRACTION TEST — [template] — [document]

Fields: [extracted] / [total] ([%])
Missing: [list]
Accuracy: [checked] / [spot-checked] correct

ISSUES:
- [field]: expected [X], got [Y]

SCORE: [PASS / NEEDS_TUNING / FAIL]
```
