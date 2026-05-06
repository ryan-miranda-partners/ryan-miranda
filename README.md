# ryan-miranda

Claude Code skills, brain, and playbooks for Ryan-Miranda Partners. Covers dev workflows (`/review`, `/ship`, `/plan`, `/cso`), ops (`/sweep`, `/standup`, `/priorities`, `/draft`), safety (`/careful`, `/verify`, `/guard-truthly`), and knowledge synthesis (`/synth`).

## Install — 3 steps

### 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Then authenticate with your Anthropic API key (get one at console.anthropic.com):

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # add to ~/.zshrc to persist
claude --version                       # confirm it works
```

### 2. Clone and run setup

```bash
git clone https://github.com/ryan-miranda-partners/ryan-miranda.git ~/Documents/ryan-miranda
cd ~/Documents/ryan-miranda && ./setup
```

`setup` symlinks `skills/` into `~/.claude/skills/rm` so Claude Code discovers the skills globally. Done once, works in every project.

Verify it worked:

```bash
./setup --check
# state: symlink — ~/.claude/skills/rm -> ~/Documents/ryan-miranda/skills
```

### 3. Set up credentials (Slack, Jira, GitHub)

```bash
cp .env.example .env          # fill in your keys
cp mcp.json.example .mcp.json # MCP server config — never commit this
```

See [`docs/CREDENTIALS.md`](docs/CREDENTIALS.md) for where to get each key (Jira API tokens, Slack bot token, GitHub, Figma).

Also authenticate GitHub CLI if you haven't:

```bash
gh auth login
```

---

## Using skills in Claude Code

Open a terminal in any project directory and start Claude Code:

```bash
cd ~/Documents/<your-project>
claude
```

Type a skill command at the prompt:

```
/sweep              — scan Slack + Gmail for blockers since last check
/review             — multi-pass code review on your current diff or a PR number
/ship               — prepare PR, wait for CI, request the right reviewer
/plan               — product + engineering review before building something new
/priorities         — generate per-person priority messages for the team
/state              — snapshot of open PRs, tickets, recent deploys
/verify             — adversarial fact-check before sending anything to a client
/careful            — gate before any destructive operation
```

Full skill list: [`skills/CLAUDE.md`](skills/CLAUDE.md)

### Example workflow

```
> /sweep
[scans Slack + Gmail, surfaces blockers]

> vaibhav has changes requested on PR 233 — action them and /verify the steps, then run adversarial agents

> /ship
[prepares PR, checks CI, runs Maestro for mobile PRs, requests review]
```

### Switching models mid-session

```
/model claude-opus-4-7        # Opus — most capable, use for planning and complex review
/model claude-sonnet-4-6      # Sonnet — default, balanced
/model claude-haiku-4-5-20251001  # Haiku — fastest, use for quick lookups
```

---

## Update

```bash
cd ~/Documents/ryan-miranda && git pull
./setup --check    # symlink stays valid after pull — no re-run needed
```

---

## Quick reference

| Docs | Link |
|------|------|
| Daily workflow | [`docs/GUIDE.md`](docs/GUIDE.md) |
| New teammate setup | [`docs/ONBOARDING.md`](docs/ONBOARDING.md) |
| Credential setup | [`docs/CREDENTIALS.md`](docs/CREDENTIALS.md) |
| Truthly engineering standards | [`docs/truthly-agent.md`](docs/truthly-agent.md) |
| When things break | [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) |
| Full skill table + principles | [`skills/CLAUDE.md`](skills/CLAUDE.md) |
| Builder philosophy | [`ETHOS.md`](ETHOS.md) |
| Multi-agent / non-Claude setup | [`AGENTS.md`](AGENTS.md) |
| Security + what stays outside this repo | [`SECURITY.md`](SECURITY.md) |

## Layout

```
ryan-miranda/
  skills/          — skill folders (symlinked into ~/.claude/skills/rm)
    CLAUDE.md      — principles, mandatory gates, full skill table
  brain/           — compiled-truth pages (people/, clients/, concepts/)
  docs/            — GUIDE, CREDENTIALS, ONBOARDING, TROUBLESHOOTING, truthly-agent
  tools/           — brain scripts, skill validator
  AGENTS.md        — platform-agnostic entry (Cursor, Codex, etc.)
  ETHOS.md         — builder philosophy
  .env.example     — credential template
  mcp.json.example — MCP server config template (copy to .mcp.json, never commit)
  setup            — install / rollback / check script
```

## Rules

- No Claude attribution in commits, PRs, or skill content.
- No secrets in this repo — credentials live in `.env` (gitignored).
- Don't edit `brain/` pages directly — changes go through `/synth` or a PR to Edward.
- Don't push directly to `main` — open a PR for any skill change.
