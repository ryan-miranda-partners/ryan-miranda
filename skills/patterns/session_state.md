# Session State Persistence

Source: ECC (hooks), CCPM (deterministic scripts), gstack (project files)

## State Files

- `~/Documents/rm-ops/daily/YYYY-MM-DD/state_snapshot.md` -- full operational state
- `~/.rm/last-sweep-ts` -- timestamp of last channel sweep
- `~/.claude/projects/.../memory/` -- persistent feedback and project context

## Decay Rules

- Snapshots <1 day: trust
- Snapshots 1-3 days: verify key items
- Snapshots >3 days: full rescan

## Delta Mode

When recent snapshot exists, only scan for changes since timestamp. Use `oldest` parameter in Slack reads.

## From ECC: Automate via Hooks

- SessionEnd hook: auto-write state_snapshot.md
- SessionStart hook: auto-load last snapshot and feedback files
- PreCompact hook: log what was summarized

## From CCPM: Bash for Collection

Parse daily/ directory, check file dates, list carry-forward items as bash. Save LLM for analysis.

## Token Optimization (ECC)

- `CLAUDE_CODE_SUBAGENT_MODEL=haiku` for sweep validation agents
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50` for session health
