---
name: freeze
description: |
  Use when: "freeze", "lock to [dir]", "only edit [dir]", "unfreeze", "unlock", debugging a specific module.
  Proactive: when investigating a bug in one module.
---

## Freeze

1. Accept a directory path (e.g., "freeze to api/routes/v2/excel").
2. Set the freeze scope. All subsequent Edit/Write operations must target files within this directory.
3. If an edit is attempted outside the frozen scope, STOP and say: "Blocked: currently frozen to [dir]. Say 'unfreeze' to lift."
4. The freeze persists until explicitly lifted.

## Unfreeze

1. Clear the freeze scope.
2. Confirm: "Unfrozen. Edits are no longer restricted to [previous dir]."

## Adapted from
gstack /freeze — same concept, simplified.
