# AGENTS.md — Ryan Miranda Partners Skills

Platform-agnostic entry point. Works with Claude Code, Cursor, Codex, and any agent that reads `AGENTS.md`.

Claude Code users: see `skills/CLAUDE.md` for the full skill table and mandatory gates.

---

## What this repo is

Skills, brain, and playbooks for Ryan-Miranda Partners dev + ops workflows. Install once; use from any working repo.

## Install

```bash
git clone https://github.com/ryan-miranda-partners/ryan-miranda.git ~/Documents/ryan-miranda
cd ~/Documents/ryan-miranda && ./setup
```

## Credentials

See `docs/CREDENTIALS.md`. Requires: `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` (or `gh auth login`), Jira API tokens for both Truthly and Mozart, Slack bot token.

## Core principles (apply to all agents)

1. **Verify before reporting.** Every factual claim cites its source. Mark `[UNVERIFIED]` if you can't.
2. **Search before building.** Check the codebase and `brain/` before creating anything new.
3. **Adversarial verification.** Any output consumed by a client or the full team gets an independent second pass.
4. **Stop and ask on ambiguity.** Present options with a recommendation. One question at a time.
5. **No AI attribution.** No `Co-Authored-By: Claude` trailers, no `Generated with [tool]` footers — anywhere.

## Mandatory gates (always enforced, every agent)

- **Before flagging an email as needs-reply:** search your sent history first. Confirm no reply was sent.
- **Before asserting a ticket or PR state:** query the API. Don't assume.
- **Before including a win in a client update:** verify the work timestamp is after the last update.
- **Before any destructive operation (rm, reset --hard, DROP, bulk-close):** invoke `/careful` or pause and confirm.

## Skills quick reference

| / command | What it does |
|-----------|-------------|
| `/sweep` | Scan Slack + Gmail for new activity, surface blockers |
| `/standup` | Check team daily updates, flag gaps |
| `/priorities` | Generate per-person priority messages |
| `/draft [client]` | Draft weekly client update from evidence |
| `/review` | Multi-pass code review with adversarial subagent |
| `/ship` | Prepare PR, verify CI, Maestro gate, request review |
| `/plan` | Product + engineering review for new features |
| `/cso` | OWASP + STRIDE security audit |
| `/verify` | Adversarial fact-check of any output |
| `/careful` | Gate before destructive operations |
| `/freeze` | Lock edits to one directory while debugging |
| `/state` | Full operational state snapshot |
| `/ticket-hygiene` | Find merged code where Jira was not updated |
| `/closure-audit` | Sprint closeout action doc with paste-ready evidence |
| `/pr-status` | Open/stale/merged PR dashboard |
| `/synth` | Append new agent-log entries to brain/ pages |
| `/guard-truthly` | Block Jira writes on TRUTHLYDEV without confirmation |
| `/client-recon` | Full context sweep for one client |
| `/competitor-scan` | Market research and positioning analysis |
| `/pdf` | Convert markdown to paginated PDF |

## Maestro (mobile E2E)

PRs touching Truthly iOS or Android that add/modify user-visible flows must have a corresponding flow in `maestro/flows/`. Install: `brew install maestro`. Run: `maestro test maestro/flows/`.

## Repo layout

```
skills/        — SKILL.md folders (symlinked to ~/.claude/skills/rm after ./setup)
brain/         — compiled-truth pages (people/, clients/, concepts/)
docs/          — GUIDE.md, CREDENTIALS.md, ONBOARDING.md, TROUBLESHOOTING.md, truthly-agent.md
tools/         — brain scripts, skill validator
.env.example   — credential template
mcp.json.example — MCP server config template (copy to .mcp.json, never commit)
AGENTS.md      — this file
ETHOS.md       — builder philosophy
```
