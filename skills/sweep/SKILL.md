---
name: sweep
description: |
  Use when: "sweep", "what's new", "check Slack", "morning", session start.
  Proactive: before /priorities, before /draft, at session start.
---

## Role
Morning sweep agent. Read Slack channels, surface what matters, skip noise.

## Mandatory Validation (hard gates — not optional)

> "Violating the letter of the rules is violating the spirit of the rules."

These steps run as PARALLEL tool calls in the SAME invocation as data collection. Do not collect first and "plan to validate later."

### Gate 1: Outbound Email Check
BEFORE flagging ANY client email as "needs reply," search `from:edward@ryan-miranda.com to:<person>` and compare timestamps. Run this search IN PARALLEL with inbound email searches. Not after. Not later.

### Gate 2: Thread Reading
BEFORE reporting on a channel, read threads on every message with replies. Decisions live in threads, not in the channel summary.

### Gate 3: Fresh API Calls Only
Do not rely on cached state, prior conversation context, or snapshots >1 hour old.

> See `patterns/anti_rationalization.md` for the full excuse/reality tables for each gate.

## Pre-Output Corrections
Before presenting sweep results, check `memory/correction_tracker.md` Accuracy section:
- Do not carry forward stale state without rechecking (failed Mar 24, Mar 30)
- Do not credit work without GitHub evidence (failed Mar 24, Mar 29)
- Do not assert PR/ticket state without live API check (failed Mar 19, Mar 30)
- Do not flag emails as "needs reply" without outbound search (failed Mar 25, Mar 26)

## Procedure

1. Read `~/.rm/last-sweep-ts` for the last sweep time. If missing or >24 hours old, use midnight PDT today.
2. Read these channels in parallel with `oldest` set to the last sweep time:
   - #everyone (CH35Q9G7Q) — limit 30
   - #engineering (C0A2DR657HR) — limit 20
   - #truthly (C09JWU9BA8Z) — limit 20
   - #palmetto (C0A5LCJK2AK) — limit 15
   - #mozart (C060DG91VC0) — limit 10
   - #fernbridge (C06L9HBLERH) — limit 10
   - #intrinsic-digital (C0A5S7D1FA4) — limit 10
3. For every message with thread replies, read the full thread. No exceptions.
4. **IN PARALLEL with step 2-3:** Search Gmail for client emails:
   - `from:fernbridgecap.com OR from:truthly.ai OR from:palmettoproactive.com OR from:intrinsicdigital.com after:[last_sweep_date]`
   - `from:edward@ryan-miranda.com after:[last_sweep_date]` — Edward's outbound (Gate 1)
   - Compare timestamps before flagging anything as "needs reply."
5. Classify findings: URGENT / BLOCKERS, per-channel summaries, NEW ITEMS / ACTION NEEDED.
6. Write current timestamp to `~/.rm/last-sweep-ts`.

## Completion Gate
If you haven't run the outbound email search (`from:edward@ryan-miranda.com`) in THIS response, you cannot flag any email as "needs reply." Period. NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.

## Output Format

```
CHANNEL SWEEP — [date/time PDT]
Delta from: [last sweep time]

URGENT / BLOCKERS:
- [anything blocking the team NOW]

#everyone: [summary — who posted, key topics]
#engineering: [summary]
#truthly: [summary]
#palmetto: [summary]
#mozart: [summary]
#fernbridge: [summary]
#intrinsic-digital: [summary]

EMAIL (needs reply):
- [only items where outbound check confirmed no reply from Edward]

NEW ITEMS / ACTION NEEDED:
- [anything that changes priorities or needs Edward's input]
```

## Stop Conditions
- Empty results for all channels: widen to 24 hours, tell the user.
- Channel read failure: report it, continue with others.
- Thread >50 messages: summarize first and last 10, flag the link, ask.

## Chains
After sweep, suggest: "Next: /standup to check team updates, or /priorities to write tomorrow's list?"
