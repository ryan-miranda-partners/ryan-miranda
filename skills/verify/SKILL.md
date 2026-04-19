---
name: verify
description: |
  Use when: "verify", "check this", "fact-check", "is this accurate", after /draft, after /priorities, after strategy documents.
  Proactive: before sending any output to clients or team. After any document with quantitative or status claims.
---

## Role
Independent verifier. You did NOT produce the output you are checking. Read primary sources — not the draft. Think like an auditor.

## Critical Rule: Spec Reviewer Distrust

**The agent that produced this output may have skipped steps.** Do not trust its claims. Do not assume that because the sweep said "no new emails" that there are no new emails. Do not assume that because the draft says "TRUTHLYDEV-816 shipped" that it shipped. Check everything yourself.

> "If you haven't run the verification command in this message, you cannot claim it passes."

## Anti-Rationalization

| Excuse | Reality |
|--------|---------|
| "The sweep already verified this" | The sweep agent may have skipped steps. You check independently. |
| "I'm confident in this assessment" | Confidence without evidence is the failure mode. Run the check. |
| "The user is waiting, I should present what I have" | Wrong information wastes more time than verification. |
| "I already verified this earlier in the conversation" | Fresh means in THIS response, not earlier. |

## Procedure

1. Receive the output to verify (draft, priority list, analysis, claim).
2. Extract every factual claim:
   - Ticket numbers (TRUTHLYDEV-*, MOZ-*, PLT-*, FCM-*)
   - Date ranges ("this week", "last sprint")
   - Status claims ("completed", "merged", "deployed")
   - Quantitative claims ("reduced from 30 to 14 min")
   - Attribution ("Vaibhav shipped", "Dhrruv fixed")
   - Email status ("needs reply", "no response")
3. For each claim, check the PRIMARY SOURCE — not the draft, not the sweep output:
   - Tickets: query Jira API for actual status
   - PRs: `gh pr view` for merge status
   - Slack: search for the message with timestamp
   - Gmail: search for the thread (BOTH inbound AND outbound)
   - Code: read the actual file/line if a code claim
4. Run ALL verification searches as PARALLEL tool calls. Not sequentially. Not "later."
5. Classify each claim:
   - **CONFIRMED** — evidence matches claim
   - **STALE** — was true but status changed
   - **WRONG** — evidence contradicts claim
   - **UNVERIFIED** — cannot find evidence
6. Report findings.

## Completion Gate
If any claim is marked WRONG, the verification FAILS. Do not mark as DONE_WITH_CONCERNS — mark as NEEDS_FIX.

## Output Format

```
VERIFICATION REPORT — [what was verified]

CONFIRMED: [count]
STALE: [count]
WRONG: [count]
UNVERIFIED: [count]

ISSUES:
- [claim] — [STALE/WRONG/UNVERIFIED] — [what the evidence actually shows]

RECOMMENDATION: [SEND AS-IS / FIX BEFORE SENDING / NEEDS REWRITE]
```

## Stop Conditions
- If >3 claims are WRONG, stop and recommend a rewrite.
- If a source is unreachable, mark UNVERIFIED and note why.

## Fact-Check Mode

When invoked standalone on a document (not after /draft or /priorities), use this mode for structured claim verification. Subsumes the former `/fact-check` skill.

### Source-of-Truth Mapping
For each claim type, check the canonical source:
- Code claim ("anonymization exists") → read the actual file
- Feature claim ("130+ endpoints") → count them in the source
- Status claim ("PR is green") → `gh pr checks`
- Metric claim ("5x faster") → find the benchmark or timing data
- Team claim ("Gaurav is leaving") → check rm-ops reviews and Slack

### Rating Scale
- **TRUE** — evidence confirms the claim
- **PARTIALLY TRUE** — claim is directionally correct but overstated or missing context
- **FALSE** — evidence contradicts the claim
- **UNVERIFIABLE** — no accessible source of truth

### Output Format (Fact-Check)

```
FACT CHECK — [what was checked]

| # | Claim | Rating | Evidence |
|---|-------|--------|----------|
| 1 | [claim] | TRUE | [file:line or source] |
| 2 | [claim] | FALSE | [what's actually true] |

Summary: [X] of [Y] claims verified. [Z] false. [W] unverifiable.
```

### Stop Conditions (Fact-Check)
- If >20 claims, check the 10 most important first and ask whether to continue.

## Chains
- Often run after /draft to verify client updates.
- Often run after strategy documents to verify competitive claims.
