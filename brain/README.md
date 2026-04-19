# brain/ — Compiled Truth Layer

Synthesized, opinionated knowledge about people, clients, and concepts Edward works with. Built from raw agent-logs (`~/Documents/agent-logs/`) + project memory (`~/.claude/projects/*/memory/`). Read by `rm-skills` skills before they call external APIs.

## Layout

```
brain/
  README.md               (you are here — schema + tier rules)
  people/                 (team members, key external contacts)
    <FirstName>.md
  clients/                (client organizations)
    <Name>.md
  concepts/               (ongoing initiatives, boards, pipelines, code areas)
    <Name>.md
```

## Page schema

Every page follows the Compiled Truth + Timeline pattern:

```markdown
---
name: <Name>
tier: 1 | 2 | 3
last_reviewed: YYYY-MM-DD
---

# <Name>

## Compiled truth (as of YYYY-MM-DD)
<Assessment. What you'd tell a new colleague in 30 seconds.>

- Role / relationship: ...
- Current focus: ...
- Working style / preferences: ...
- Risks / watch-outs: ...

## Timeline
<Append-only. One line per observation. Cite the source.>

- YYYY-MM-DD — short summary of observation — `agent-logs/<file>.md`
- YYYY-MM-DD — ... — `<source>`
```

## Tier rules

Pages are promoted upward as mention density and direct engagement grow.

| Tier | Criteria | Content depth |
|------|----------|---------------|
| **3 (stub)** | 1-2 mentions, no direct interaction | name, role, one-line context |
| **2 (snapshot)** | 3-7 mentions, some back-and-forth | + working style, current focus, recent arc |
| **1 (full)** | 8+ mentions OR direct meetings / reports to Edward | + risks, recommendations, multi-month timeline |

Promotion is not automatic — it's reviewed. When `tools/audit-brain.sh` flags a candidate, Edward decides.

## Brain-first lookup

rm-skills read this layer BEFORE hitting Slack/Jira/GitHub for stable facts (someone's role, a client's recipient list, a project's purpose). External APIs are only for LIVE state (latest PR status, today's messages).

If a skill finds the brain page missing or `last_reviewed` > 30 days, it flags the gap in its output instead of silently reading stale info.

## Rules for editors

1. **Evidence, not opinion.** Every claim in `## Compiled truth` should have a citation or be derivable from `## Timeline`.
2. **Append to timeline, edit the assessment.** New data goes in timeline. Compiled truth gets rewritten when the underlying pattern shifts.
3. **Cite sources.** Agent-log path, Slack message URL, Jira ticket, or email timestamp. No bare claims.
4. **Respect the raw-data principle.** Never modify agent-logs. Only read and cite.
5. **Decay is a signal.** If `last_reviewed` is >30 days and you're writing new content, refresh the assessment first.
6. **First names only for pages.** `Vaibhav.md`, not `Vaibhav-Sharma.md`. Multi-Vaibhav collisions get handled via tier-1 compiled-truth fields, not filename.

## Out of scope (do NOT put in brain/)

- Live state (open PR counts, today's Slack messages) — use skills that hit APIs.
- Credentials, passwords, tokens, API keys.
- Meeting transcripts or personal notes — those belong in agent-logs.
- Commercial terms, signed contracts, financial statements.
- PII beyond what's already public (LinkedIn, company site, Slack handles).

See `SECURITY.md` at repo root.

## Sync cadence

- **Per-session:** manual via `/synth` (reads new logs since last watermark, appends to timeline).
- **Weekly:** manual review of pages flagged by `tools/audit-brain.sh` (promotion candidates, stale assessments).
- **Monthly:** Edward re-reads Tier-1 compiled-truth sections, rewrites where patterns have shifted.

Automation (post-session hook) is deferred until the manual shape is validated.
