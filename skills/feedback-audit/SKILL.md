---
name: feedback-audit
description: |
  Use when: "feedback audit", "check feedback", "what mistakes keep happening", "review lessons learned".
  Proactive: monthly, or after a session with 2+ corrections from Edward.
---

## Role
Auditor of the feedback memory system. Read all raw feedback, update the compiled synthesis, check recurrence, and flag enforcement gaps.

## Design Principle
Raw feedback files are immutable intake. NEVER modify originals. All synthesis, tracking, and enforcement layers are built on top.

## Procedure

### Step 1: Scan raw feedback
Read all `feedback_*.md` files across all project memory directories:
```
ls /Users/edward/.claude/projects/
```
Then glob `**/feedback*.md` in each project's memory/ directory.

### Step 2: Compare against compiled synthesis
Read `~/.claude/projects/-Users-edward/memory/feedback_compiled.md`. Identify:
- New raw feedback files not yet synthesized
- Existing entries that need updating based on new incidents
- Patterns that have shifted tier (e.g., Tier 3 context becoming Tier 1 hard rule due to recurrence)

### Step 3: Check recurrence log
Read `~/.claude/projects/-Users-edward/memory/feedback_recurrence_log.md`. For any pattern with 3+ violations in 14 days:
- Check if a hookify rule exists at `~/.claude/hookify.*.local.md`
- If not, recommend creating one
- Update trend assessments

### Step 4: Check enforcement coverage
- Read `~/.claude/hookify.*.local.md` for active hookify rules
- Read `~/.claude/skills/rm/memory/correction_tracker.md` for the trigger map
- Identify Tier 1 rules without programmatic enforcement

### Step 5: Check for staleness
For each feedback memory:
- If it references a specific date/deadline, check if that's passed
- If it references a specific file/function, check if it still exists
- If it references a team member's status (part-time, notice period), verify current state

### Step 6: Check for positive patterns
Scan the conversation history and recent agent logs for validated approaches that should be captured. The system is correction-heavy — balance it with what works.

### Step 7: Report

Output format:
```
FEEDBACK AUDIT — [date]

Raw feedback count: [X] across [Y] projects
New since last audit: [list]
Recurrence alerts: [patterns with 3+ violations]
Enforcement gaps: [Tier 1 rules without hooks]
Stale memories: [list with reason]
Duplicate candidates: [groups that could consolidate]
Missing positive feedback: [validated approaches not yet captured]

RECOMMENDATIONS:
1. [action] — [why]
2. ...
```

### Step 8: Update compiled files (with confirmation)
After presenting the report, ask Edward before updating:
- `feedback_compiled.md` — add new patterns, update tiers
- `feedback_recurrence_log.md` — add new incidents
- `correction_tracker.md` — add new checklist items

NEVER modify raw feedback files.

## Stop Conditions
- If no new feedback since last audit, say so and skip
- If a raw file appears corrupted or has no frontmatter, flag it

## Chains
- Run after any session where Edward makes 2+ corrections
- Run monthly as part of system maintenance
- Can be triggered standalone: `/feedback-audit`
