---
name: review
description: |
  Use when: "review", "code review", "check my diff", "pre-landing review", about to merge.
  Proactive: when user has uncommitted changes or an open PR.
---

## Role
You are a senior code reviewer. You review for correctness, security, performance, and fit with existing patterns.

## Procedure

1. Determine the diff scope:
   - If a PR number is given: `gh pr diff <number> --repo <repo>`
   - If a branch: `git diff <base>...<branch>`
   - If unstaged: `git diff`
2. Count changed lines. Scale the review:
   - **Small (<50 lines):** structured review only (skip adversarial).
   - **Medium (50-199 lines):** structured review + adversarial subagent.
   - **Large (200+ lines):** 4-pass: structure, security, patterns, adversarial.
3. **Pass 1 — Structural Review:**
   - Does the code do what it claims?
   - Are edge cases handled?
   - Are error paths correct?
   - Is the logic clear without comments?
4. **Pass 2 — Security (medium+ diffs):**
   - SQL injection, XSS, OWASP Top 10
   - Auth/authz checks on every endpoint
   - Secrets in code, leaked in errors
   - Input validation at system boundaries
5. **Pass 3 — Pattern Fit (large diffs):**
   - Does it match existing codebase conventions?
   - Logger pattern: `logger.error(error, "routes")`
   - Response format: `sendSuccess` / `sendError`
   - Route pattern: `async function(app, path)`
   - Test pattern: minimal mocks (like priorities.test.ts)
   - **Maestro flows (mobile PRs):** If the diff adds or modifies a user-visible flow (auth, onboarding, paywall, navigation), check whether a corresponding Maestro flow exists in `maestro/flows/`. Missing coverage for a new critical-path screen is a FIXABLE finding. List any existing flows that touch the changed screen so the author knows to re-run them.
6. **Pass 4 — Adversarial (medium+ diffs):**
   - Dispatch a fresh Agent with NO context from passes 1-3
   - Agent reads the diff cold and thinks like an attacker
   - Findings classified: FIXABLE, INVESTIGATE, ACCEPT

## Output Format

```
CODE REVIEW — [branch/PR] — [line count] — [small/medium/large]

PASS 1 (STRUCTURAL): [pass/fail]
- [findings]

PASS 2 (SECURITY): [pass/fail]
- [findings]

PASS 3 (PATTERN FIT): [pass/fail]
- [findings]

PASS 4 (ADVERSARIAL): [count] findings
- [file:line — severity — finding — fix]

VERDICT: [APPROVE / APPROVE_WITH_COMMENTS / REQUEST_CHANGES / BLOCK]
```

## Stop Conditions
- If Pass 1 finds a fundamental logic error, stop and flag before continuing.
- If Pass 2 finds a critical security issue, stop immediately.
- If the diff adds a new critical-path screen (auth, paywall, onboarding) and no Maestro flow covers it, flag INVESTIGATE before approving.

## Adapted from
gstack /review — added pattern-fit pass, finserv security focus, team-aware reviewer context.
