---
name: guard-truthly
description: |
  Use when: any Jira write (post, put, patch, delete) targets TRUTHLYDEV project.
  Proactive: always, automatically intercepts TRUTHLYDEV writes.
---

## Role
Safety guardrail for the live Truthly product board. Prevent accidental ticket modifications.

## Rule
NEVER perform write operations on the TRUTHLYDEV Jira project:
- No creating tickets
- No transitioning tickets
- No editing summaries, descriptions, or fields
- No bulk operations
- No commenting (unless Edward explicitly requests it)

## Allowed
- Reading tickets (jira_get)
- Searching with JQL
- Reading comments and worklogs

## When to Activate
Automatically, whenever a Jira write tool (jira_post, jira_put, jira_patch, jira_delete) targets the TRUTHLYDEV project.

## Procedure

1. Detect that a Jira write operation targets TRUTHLYDEV.
2. STOP. Do not execute.
3. Say: "Blocked: TRUTHLYDEV is read-only. Edward handles ticket updates for the live product. Want me to draft the change for you to apply manually?"
4. If Edward explicitly overrides ("do it", "I authorize this"), proceed with the single operation.

## Why
The Truthly board has 95+ tickets. Bulk or accidental modifications could disrupt the active sprint, confuse the client team, or lose tracking state. Edward reviews all ticket changes personally.
