---
name: client-recon
description: Sweep all channels and sources for one client's full context.
---

## Procedure

1. Identify the client.
2. Search Slack (client channel + #everyone mentions).
3. Search Gmail (to/from client domain).
4. Search Jira (project board, recent tickets).
5. Read the latest client update draft and archive.
6. Compile: current status, recent wins, blockers, open questions, next steps.

## Output

```
CLIENT RECON — [client name] — [date]

STATUS: [active / standby / blocked]
LAST UPDATE: [date]
KEY CONTACT: [name, email]

RECENT ACTIVITY:
- [source]: [summary]

OPEN ITEMS:
- [what's pending]

NEXT STEPS:
- [recommended actions]
```
