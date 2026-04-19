---
name: pr-status
description: |
  Use when: "pr status", "check PRs", "what's open", "stale PRs".
  Proactive: during /state or before /ship.
---

## Procedure

1. Check these repos in parallel using `gh pr list --state open --limit 10`:
   - ryan-miranda-partners/mozart-backend
   - ryan-miranda-partners/mozart-frontend
   - ryan-miranda-partners/mozart-rag
   - ryan-miranda-partners/mozart_mcp
   - ryan-miranda-partners/palmetto
   - ryan-miranda-partners/palmetto-infra
   - Truthly-App/Truthly-ios
   - Truthly-App/Truthly-android
   - Truthly-App/Truthly-backend
2. For each open PR: title, author, CI status, days open, review status.
3. Also check recently merged (last 3 days) with `gh pr list --state merged --limit 5` on each repo.
4. Flag stale PRs (>7 days without activity).
5. Flag PRs with failing CI.
6. Flag PRs with no reviewers assigned or changes requested without follow-up.

## Output

```
PR STATUS — [date]

| Repo | PR | Author | Age | CI | Review | Notes |
|------|-----|--------|-----|-----|--------|-------|
| mozart-backend | #454 | Edward | 2d | pass | pending | Ready to merge |

RECENTLY MERGED (last 3 days):
| Repo | PR | Title | Merged | Author |
|------|-----|-------|--------|--------|

STALE (>7 days): [list]
CI FAILING: [list]
NO REVIEWERS: [list]
```
