---
name: priorities
description: |
  Use when: "priorities", "write priorities", "what should everyone work on".
  Proactive: after /sweep + /standup in the morning chain.
---

## Pre-Output Corrections
Before drafting or presenting priorities, check `memory/correction_tracker.md`:
- **Accuracy:** Run adversarial verification AFTER drafting, BEFORE posting (failed Mar 19, Mar 24, Mar 29). Verify every PR/ticket claim against live GitHub/JIRA.
- **Voice:** No em dashes. Keep priorities concise (3-4 items, not 7). Every item must have a ticket number.
- **Workflow:** Default to Slack drafts when posting. Ask how Edward wants messages grouped before splitting.

## Procedure

1. Read the latest state snapshot and carry-forward tracker from rm-ops/daily/.
2. Check Jira boards for overdue items and blockers (MOZ, TRUTHLYDEV projects).
3. Review any /sweep output from this session.
4. For each team member, draft 3-4 numbered priorities:
   - Lead with the highest priority item
   - Reference ticket numbers
   - Include hard deadlines if any
5. Format for Slack posting (one message per person, bold name).
6. Save to `~/Documents/rm-ops/daily/[date]/[date]_priorities.md`.

## Format

```
**Vaibhav**
1. TRUTHLYDEV-816 -- [description]. [target].
2. TRUTHLYDEV-800 -- [description].
3. [other item]

```

## Post Order
Vaibhav, Gaurav, Dhrruv, Luke.

## Stop Conditions
- If missing context for a person's current work, ask: "What should [person] focus on?"
- If >4 items for someone, ask which to cut.
