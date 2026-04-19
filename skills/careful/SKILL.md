---
name: careful
description: |
  Use when: git force-push, rm -rf, DROP TABLE, DELETE without WHERE, Jira bulk ops, production deploys, sending client emails.
  Proactive: always, automatically on destructive commands.
---

## Role
Safety guardrail. Intercept dangerous commands and require explicit confirmation.

## When to Activate
Automatically, whenever the conversation involves:
- `git reset --hard`, `git push --force`, `git branch -D`
- `rm -rf`, `DROP TABLE`, `DELETE FROM` (without WHERE)
- Jira bulk transitions or deletions
- Sending emails to clients
- Modifying production environment variables
- Any command that affects shared state (push, deploy, send)

## Procedure

1. Detect the dangerous operation in the planned action.
2. STOP. Do not execute.
3. Present:
   ```
   ⚠️ CAREFUL — [what you're about to do]

   This will: [specific consequence]
   Reversible: [yes/no/partially]
   Blast radius: [local/shared/production]

   Proceed? (yes / no / show me the command first)
   ```
4. Wait for explicit "yes" or "proceed" before executing.
5. If "no", suggest a safer alternative.

## Stop Conditions
- Never proceed without confirmation on production-affecting operations.
- If the user says "just do it" or "skip warnings", comply for that single action but re-enable for the next.

## Adapted from
gstack /careful — same pattern, extended to cover Jira, email, and deployment operations.
