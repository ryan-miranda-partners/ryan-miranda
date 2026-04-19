---
name: ticket-hygiene
description: |
  Use when: "ticket hygiene", "what tickets need updating", "stale tickets", "merged but not closed".
  Proactive: weekly board cleanup, after /pr-status.
---

## Procedure

1. **TRUTHLYDEV board** — search Jira (truthly-ai.atlassian.net, Atlassian MCP):
   - JQL: `project = TRUTHLYDEV AND sprint in openSprints() AND status NOT IN (Done) ORDER BY status`
   - Get: key, summary, status, assignee
2. **Palmetto board** — search Jira (ryan-miranda.atlassian.net, mcp__jira-mozart):
   - JQL: `project = PLT AND status NOT IN (Done) ORDER BY status`
3. **Mozart board** — search Jira (ryan-miranda.atlassian.net, mcp__jira-mozart):
   - JQL: `project = MOZ AND status NOT IN (Done) ORDER BY status`
4. For each "Ready for Review" ticket, check if PR is merged via `gh pr view`.
5. For "In Progress" tickets with no update >5 days, flag as stale.
6. Flag unassigned tickets.
7. **Action list for Edward:** list tickets to transition (he handles flips as admin). Suggest Backlog for stale/unassigned.

## Output

```
TICKET HYGIENE — [date]

MERGED BUT NOT CLOSED:
- [TICKET] — PR merged [date], Jira still "[status]"

STALE IN PROGRESS:
- [TICKET] — assigned to [person], no activity since [date]

UNASSIGNED:
- [TICKET] — status "[status]", no assignee

BLOCKED (verify still blocked):
- [TICKET] — assigned to [person], blocker: [what]

ACTION LIST FOR EDWARD:
- Transition to Done: [list]
- Move to Backlog: [list]
- Needs triage: [list]
```

## Stop Conditions
- Do NOT transition tickets. Report only. Edward handles ticket flips.
