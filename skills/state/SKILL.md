---
name: state
description: |
  Use when: "state", "save state", "state snapshot", "capture state", end of session.
  Proactive: at session end if significant work was done.
---

## Procedure

1. Run /sweep (or use existing sweep data from this session).
2. For each active project, capture current state:
   - Truthly: sprint status, key tickets, blockers, next milestones
   - Palmetto: GCP migration status, blockers
   - Mozart: PR status, current branch work, CI status
   - FCM: report pipeline status, recent issues
   - Intrinsic: active/standby, pending meetings
   - Atlantis: OCR status, client feedback
   - Red Door: phase status
3. Capture open communication loops (who owes what to whom).
4. Capture Edward's priority list.
5. Write to `~/Documents/rm-ops/daily/[date]/state_snapshot.md`.

## Output
Full state snapshot following the format in existing state_snapshot.md files.
