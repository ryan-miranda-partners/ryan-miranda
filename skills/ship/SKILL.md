---
name: ship
description: |
  Use when: "ship", "create PR", "ready to merge", "push and review".
  Proactive: when all commits are clean and tests pass.
---

## Role
You are the release engineer. Prepare clean PRs with clear descriptions, verify CI passes, and request the right reviewer.

## Procedure

1. Check the current branch state:
   - `git status` — any uncommitted changes?
   - `git log <base>..HEAD` — what commits are included?
   - `git diff <base>..HEAD --stat` — what files changed?
2. Create or update the PR:
   - Title: short, under 70 chars, describes the change
   - Body: ## Summary (3-5 bullets), ## Test plan (what to verify)
   - Target: usually `development`
   - Use `gh pr create` or `gh pr edit`
3. Push if needed: `git push origin <branch>`
4. Wait for CI:
   - `gh pr checks <number> --watch`
   - If tests fail: read the log, fix the issue, push again
4b. **Maestro (mobile PRs only):** If the PR touches Truthly-ios or Truthly-android and modifies a user-visible flow, run `maestro test maestro/flows/` locally before requesting review. If Maestro is not installed: `brew install maestro`. A Maestro failure is CI_FAILING — do not request review.
5. Request review:
   - Mozart backend: Gaurav or Vaibhav
   - Mozart frontend: Vaibhav
   - Truthly: Matthew or Vaibhav
   - Palmetto: Dhrruv
6. Report status.

## Output Format

```
SHIP STATUS — [branch] → [target]

PR: [url]
CI: [pass/fail/pending]
Reviewer: [name]
Files: [count] changed, [additions]+, [deletions]-

Status: [READY_FOR_REVIEW / CI_FAILING / NEEDS_REBASE]
```

## Stop Conditions
- If CI fails, fix and re-push before requesting review.
- If there are merge conflicts, ask whether to rebase or merge.
- Never force-push to main/development without explicit permission.

## Chains
- Run /review before /ship to catch issues pre-PR.
- Run /cso before /ship if the PR touches auth, encryption, or data handling.

## Adapted from
gstack /ship — simplified (removed Greptile integration, production deploy steps). Added team-aware reviewer selection.
