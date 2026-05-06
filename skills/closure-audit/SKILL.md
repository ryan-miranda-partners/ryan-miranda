---
name: closure-audit
description: |
  Use when: "closure audit", "regenerate closure list", "ticket closeout", "what can I close", "sprint cleanup before new sprint", "update jira closure doc".
  Proactive: at end of any sprint (≤2 days before sprint endDate); before opening a new sprint on a board; after a release cut where multiple PRs merged.
  Args: board name (TRUTHLYDEV / MOZ / PLT). Defaults to TRUTHLYDEV if omitted.
---

Recreate the per-board closure-queue audit doc that lists every flippable ticket (with paste-ready evidence comments) so Edward can batch-close before opening the next sprint. This is heavier than `/ticket-hygiene` — it produces a copy-paste action doc, not a status report.

## Board → repo + Jira mapping

| Board arg | Jira host | MCP | Repos to scan for merged PRs |
|---|---|---|---|
| TRUTHLYDEV (default) | truthly-ai.atlassian.net | mcp__claude_ai_Atlassian__* | truthly-inc/Truthly-ios, truthly-inc/Truthly-android, truthly-inc/auth.truthly.ai, truthly-inc/truthly-web, truthly-inc/Truthly-backend, truthly-inc/signup.truthly.ai |
| MOZ | ryan-miranda.atlassian.net | mcp__jira-mozart__* | ryan-miranda-partners/mozart-frontend, mozart-backend, mozart-rag |
| PLT | ryan-miranda.atlassian.net | mcp__jira-mozart__* | ryan-miranda-partners/palmetto, palmetto-infra |

If the user names a board not in this table, ask which Jira host + repo set it maps to before proceeding.

## Procedure

1. **Look for the most recent prior audit** under `rm-ops/<workspace>/drafts/closure-queue-audit-*.md` (Truthly = `rm-ops/truthly/drafts/`; Mozart/Palmetto = client-specific drafts dir). Read it. The new doc is an *update*, not a fresh start — preserve verified PR mappings, evidence sentences, and "hold" classifications.

2. **Pull current sprint context (Atlassian MCP):**
   - JQL: `project = <BOARD> AND sprint in openSprints()` with `fields: ["status","summary","customfield_10020"]`, `maxResults: 1` — extract sprint name + endDate from `customfield_10020`.
   - JQL: `project = <BOARD> AND sprint in openSprints() ORDER BY status, assignee` — count distribution. **If the result exceeds the in-line token limit, the MCP saves it to a file; use `jq` on that file to extract just `key / status / assignee / summary`. Don't try to read the full JSON inline.**

3. **Pull current state of every ticket cited in the prior audit** in one batched JQL `key in (...)` query. Compare to the prior audit's expected status to discover what Edward closed since.

4. **Scan for new merged PRs since the prior audit's date** across the board's repo set. Use `gh pr list --repo <repo> --state merged --limit 30 --search "merged:>=<prior-audit-date>" --json number,title,mergedAt,headRefName`. PR titles or `headRefName` typically cite the ticket key (`TRUTHLYDEV-1234`, `feature/TRUTHLYDEV-1234-foo`).

5. **For each new PR, find the ticket it closes** and check current Jira status. If RFR or To Do, it's a candidate for the new audit's §2 backlog.

6. **Workflow constraint reminder (TRUTHLYDEV):**
   - "Ready for Review" → "Done" via the **Review Approved** transition (id 3) — standard.
   - "To Do" has NO direct transition to Done or Won't Do — admin override required.
   - Always paste a closing comment citing the supersede/dup/PR link before flipping.

7. **Spec-reviewer distrust on PR scope.** Before listing a PR as "ready to close the ticket," scan the PR body (`gh pr view <n> --json body`) for these red flags — they mean the work is **NOT** a fix and should go to §3 hold, not §2 close:
   - "Diagnostic-only", "instrumentation", "telemetry", "signpost"
   - "Revert this PR after..."
   - "Hypothesis ... is confirmed if..."
   - PR is a parent/umbrella whose acceptance criteria depend on other PRs landing
   Soft-caveats like "verify diag-only scope" are NOT enough — actively reclassify.

8. **Write the new audit doc** at `rm-ops/<workspace>/drafts/closure-queue-audit-<YYYY-MM-DD>.md` with this structure (mirror the prior audit; use a `(rev N)` suffix on the heading if same-day re-run):
   ```
   # <BOARD> closure-queue audit — <date>
   **Sprint:** <name> (<startDate> → <endDate>, <N> days remaining)
   **Method:** <one-line method>
   **Last refreshed:** <ISO timestamp>

   ## What changed since <prior-audit-date>
   - Closed in this session: <ticket list>
   - Other status changes: <e.g. To Do → RFR>
   - New merged PRs in <repo>: <list> | "none" if []
   - Net effect: <one-line summary>

   ## Section 1 — Done
   <ticket-list each with paste-ready closing comment; "Empty" if cleared>

   ## Section 2 — Backlog: N still-open tickets verifiably shipped
   <subsection per cluster (iOS/Android/auth/etc.); table cols: Ticket | Status now | PR | Evidence to paste>

   ## Section 3 — Tickets to hold (need human judgment)
   <table cols: Ticket | Status now | Why hold>

   ## Section 4 — Updated headline
   <table cols: Outcome | Original plan | Closed by <date> | Still actionable>
   <bottom line: "N still-flippable + ~M holds">

   ## Section 5 — Sprint <N+1> prep (after closures)
   <In Progress carry-over, active To Do, held-by-design, Vivek-style reassign callouts, dup relinks, suggested next sprint goal>

   ## Section 6 — Adversarial flags
   <legacy + new flags surfaced this pass>

   ## Quick action checklist
   ```
   ----- Section 2 (N left) -----
   [ ]  <ticket>  → flip <transition>; comment from §2
   ...
   ----- Section 3 (verify per row before flip) -----
   [ ]  <ticket list>
   ```
   *Generated <date>. Sources: Jira ... ; gh pr list ... . Re-verified against prior audit at <path>.*
   ```

9. **Convert to .docx and open:**
   ```
   pandoc <md-path> -o <docx-path> && open <docx-path>
   ```

10. **Hand back to Edward.** Headline summary: how many newly-closed since prior audit, how many still-flippable now, any reclassifications. Offer `/verify` as the natural follow-up before he starts batch-flipping.

## Stop conditions

- **Never flip a ticket.** Edward handles all status flips as admin. This skill produces the action doc; it does not act on the board.
- **Never bulk-action the TRUTHLYDEV board** — client-facing, manual review only.
- If Jira returns >100k chars and the MCP saves to a file, use `jq` on the file rather than re-reading JSON inline.
- If the prior audit doesn't exist (first run on a board), say so and produce the audit from scratch — don't fabricate a history.
- If a PR cites a ticket but its body has diagnostic-only / revert-target language, classify into §3 with a clear "DO NOT close" note.

## Output (verbal handback)

```
CLOSURE AUDIT — <board> — <date>

Doc: rm-ops/<workspace>/drafts/closure-queue-audit-<date>.md (+ .docx, opened)

What changed since <prior-audit-date>:
- Closed: <count> (<ticket list>)
- Still flippable: <count> in §2, <count> in §3 holds
- Reclassifications: <ticket → §3 with reason>, if any

Suggested next: /verify before batch-flipping.
```

## Chains

- Often run AFTER a release cut where multiple PRs landed.
- Often followed by `/verify` before Edward starts flipping.
- Strongly precedes opening a new sprint — use within 2 days of sprint endDate.
- Sister to `/ticket-hygiene` (which is lighter — status report only, no paste-ready comments).
