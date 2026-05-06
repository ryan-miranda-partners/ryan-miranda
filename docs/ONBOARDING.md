# Onboarding — rm-skills

For a new teammate (Dhrruv, Luke, future hire) getting access to rm-skills for the first time.

## What rm-skills is

A set of Claude Code skills + a knowledge layer, tuned for Ryan-Miranda Partners ops + dev workflows. When you type `/<skill>` in Claude Code, it runs a pre-defined procedure tailored to how Edward actually works. 22 skills today.

**What it is NOT:** a Claude Code fork, an autonomous agent, or a replacement for anything you're already doing. It's a shortcut layer.

## Install (30 seconds)

```bash
git clone https://github.com/ryan-miranda-partners/maestro-hub.git ~/Documents/maestro-hub
cd ~/Documents/maestro-hub && ./setup
```

Opens a Claude Code session, type `/state`. If you see a state snapshot, you're in.

Requires: Claude Code already installed, Python 3.12+, `gh` auth to the `ryan-miranda-partners` org, Maestro CLI (`brew install maestro`) for mobile E2E testing.

For credentials (API keys, MCP servers, Slack/Jira/Figma tokens) see `docs/CREDENTIALS.md`.

## First-day skills to try

Start with these four — they're the most generally useful:

| Skill | When to use | What it does |
|-------|-------------|--------------|
| `/state` | Start of any session | Shows open PRs, in-progress tickets, recent deploys across all repos |
| `/sweep` | Checking Slack / Gmail / PRs | Scans for deltas since last sweep — blockers, needs-reply, stale items |
| `/review` | You have a diff or open PR | Multi-pass structured review + adversarial check |
| `/verify` | You wrote something for a client or the team | Independent fact-check of claims before you send |

## What to read before touching anything

1. **`docs/GUIDE.md`** — daily workflow.
2. **`skills/CLAUDE.md`** — the principles every skill enforces (verify before reporting, search before building, adversarial verification).
3. **`SECURITY.md`** — what's in the repo and what isn't.

## What NOT to do (early days)

- **Don't edit `brain/` pages.** Those are Edward's compiled-truth assessments. If you disagree with an assessment, tell him. If you want to add a timeline entry from your observation, tell him that too — he'll update through the normal synth flow.
- **Don't run `tools/backfill-brain.py`.** It overwrites every brain page. Scoped backfill (`--entity <Name>`) is safer but still destructive to that entity's edits.
- **Don't commit Claude attribution footers.** Hard rule. No `Co-Authored-By: Claude Code`, no `Generated with Claude Code`. Strip them.
- **Don't push directly to `main` yet.** Open a PR for any skill change. Edward reviews.
- **Don't add client emails, credentials, or tokens to this repo.** `SECURITY.md` lists what stays outside (`~/Documents/rm-ops/client-updates/README.md` is the right home for recipient lists).

## Proposing a new skill

1. Draft the `SKILL.md` in a feature branch.
2. Keep it short — 40-80 lines. Role, procedure, output format, stop conditions.
3. If you're borrowing from gstack or another framework, cite it with an `## Adapted from` footer.
4. Run `./tools/validate-skills.sh` locally.
5. Open a PR. Tag Edward.

## Proposing a new brain entity

Same as new skill — branch + PR. You'll edit `tools/brain_lib.py` to add the `Entity(...)` + run `./tools/backfill-brain.py --entity <Name>` to generate the first draft page. Commit both the roster change and the new page together.

## Who owns what

| Area | Primary | Review |
|------|---------|--------|
| `skills/` | Edward | You, for diffs affecting your workflow |
| `brain/` compiled-truth | Edward | None (his domain) |
| `brain/` timeline | Automated via `/synth` | Noise-prune by Edward |
| `tools/` | Edward | You, for bugs you hit |
| `docs/` | Whoever noticed the gap | Edward |
| `SECURITY.md` rules | Edward | Escalate, don't edit |

## Support

- Hit a bug? Open an issue on the repo.
- Confused by a skill's behavior? Read the `SKILL.md` first — procedures are in prose.
- Think a skill is wrong? DM Edward. Don't edit without discussion.
- Skill not loading? See `docs/TROUBLESHOOTING.md`.

## First-week checklist

- [ ] Install rm-skills (above).
- [ ] Run `/state`, `/sweep`, `/verify` at least once each.
- [ ] Read `docs/GUIDE.md` end-to-end.
- [ ] Skim `skills/CLAUDE.md` — note the mandatory validation gates.
- [ ] Skim 5 random `SKILL.md` files to get the shape.
- [ ] Commit your first session log to `~/Documents/agent-logs/YYYY-MM-DD-<slug>.md` using the format in that folder's `README.md`.
