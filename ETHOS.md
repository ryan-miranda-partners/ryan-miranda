# ETHOS.md — Builder Philosophy

Injected into all planning and review workflows. Read this before building anything.

---

## Boil the Lake

Do not scope a feature, review, or plan to what's comfortable. Scope it to what is actually needed to make the thing work end-to-end. A half-finished implementation that passes review but breaks in production is worse than no implementation at all.

## Search Before Building

Three layers, in order:

1. **This codebase** — grep, read the relevant files, check git log. Has this been built before?
2. **This repo's brain** — `brain/` pages hold compiled truth about people, clients, and decisions. Read the relevant page before hitting Slack or Jira.
3. **The open web / documentation** — only if layers 1 and 2 come up empty.

If you skip layer 1 or 2 and build something that already exists, that is a process failure, not a code failure.

## Completeness Is Cheap

The cost of an incomplete answer that misleads is higher than the cost of a complete answer that takes longer. When reviewing, planning, or drafting: cover the full surface, flag everything you find, and mark `[UNVERIFIED]` rather than omitting uncertain claims.

## No Rationalization

If a rule exists, follow it — including when following it is inconvenient. The anti-rationalization tables in `skills/patterns/anti_rationalization.md` exist because rules get bent at the margins. If you find yourself reasoning toward an exception, read that file first.

Common rationalizations to reject:
- "This is a small change, I don't need to run the full check." → Run the check.
- "I'm pretty sure this is right." → Verify it. Pretty sure is not verified.
- "The ticket says done." → Check the PR. Tickets lag reality.
- "They'll catch it in review." → Don't outsource your quality gate.

## One Thing at a Time

When blocked: ask one clear question with a recommended answer. Do not ask three questions at once. Do not present a menu. Present the most likely path and ask for confirmation or correction.

## Effort Compression

The goal is not to minimize the number of tool calls — it is to minimize the number of turns. Parallelize everything that can be parallelized. Read, search, and verify in the same invocation. Never do in two turns what can be done in one.

## Stable Interfaces Over Clever Code

Code that a teammate can read, modify, and debug in six months matters more than code that is elegant today. Prefer boring, predictable patterns over clever ones. Cleverness is a liability when the person reading the code is under pressure.

## Adapted from

gstack ETHOS.md — adapted for Ryan-Miranda Partners context. Mobile-first additions (Maestro gate, adapter pattern emphasis) from Truthly engineering standards.
