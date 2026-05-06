# rm-skills Guide

Daily playbook for using rm-skills + the brain layer. Written for Edward; future teammates see `ONBOARDING.md` first.

## The mental model

Three layers, three lifespans:

| Layer | What it is | Where it lives | Lifespan |
|-------|------------|----------------|----------|
| **Skills** | Procedures Claude runs when you type `/<name>` | `skills/` (symlinked to `~/.claude/skills/rm`) | Change monthly-ish |
| **Brain** | Compiled-truth pages about people, clients, concepts | `brain/people`, `brain/clients`, `brain/concepts` | Assess monthly, timeline appends weekly |
| **Agent-logs** | Raw session narrative | `~/Documents/agent-logs/YYYY-MM-DD-*.md` | Append-only forever |

**Rule:** agent-logs are evidence. Brain is synthesis. Skills read from brain before hitting external APIs.

---

## Daily workflow

### Morning — the sweep loop

```
/sweep      — Slack + Gmail + PR deltas since last sweep
/standup    — confirm team posted daily goals
/priorities — per-person messages for #everyone
```

Before any of these, skills read the brain for stable facts (team roster, roles, client recipient rules) rather than re-deriving them from logs.

### Client day — Friday (or when you say "draft")

```
/draft <Client>   — reads brain/clients/<Client>.md + Gmail + Slack, produces current_draft.md
/verify           — adversarial check on the draft before send
```

### Dev work

```
/plan     — scope / design check before writing code
/review   — multi-pass review of a diff / PR
/cso      — security audit when touching auth/creds/PII
/ship     — PR prep, test gates, open the PR
```

### End of session

```
/state    — capture operational snapshot for next session
```

Write a session log in `~/Documents/agent-logs/YYYY-MM-DD-<slug>.md` summarizing what happened.

### Weekly (Sunday evening or Monday morning)

```
/synth    — read new agent-logs since last watermark, append timeline entries to brain pages
```

Review what `/synth` added. Flag any new-entity candidates it surfaces.

### Monthly — brain assessment refresh

Open each Tier-1 brain page (`brain/people/Vaibhav.md`, etc.). Re-read the timeline entries since `last_reviewed`. Update the `## Compiled truth` section if the pattern has shifted. Bump `last_reviewed` in the frontmatter.

---

## Common commands

### Running synth manually
```bash
~/Documents/maestro-hub/tools/synth-brain.py              # normal run
~/Documents/maestro-hub/tools/synth-brain.py --dry-run    # preview
~/Documents/maestro-hub/tools/synth-brain.py --since 2026-04-01   # override watermark
~/Documents/maestro-hub/tools/synth-brain.py --reset      # clear watermark
```

### Running backfill (rarely — only for full rebuilds)
```bash
~/Documents/maestro-hub/tools/backfill-brain.py           # rewrites every brain page
~/Documents/maestro-hub/tools/backfill-brain.py --entity Vaibhav   # one entity
```
**Warning:** backfill OVERWRITES brain pages — your compiled-truth edits get lost. Only run if you explicitly want a clean regenerate (e.g. you added a new entity to the roster). Commit brain changes before running.

### Validating skills after editing one
```bash
~/Documents/maestro-hub/tools/validate-skills.sh
```

### Rolling back the symlink install
```bash
~/Documents/maestro-hub/setup --rollback
```

### Checking install state
```bash
~/Documents/maestro-hub/setup --check
```

---

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with frontmatter:
   ```yaml
   ---
   name: <name>
   description: |
     Use when: <triggers>
     Proactive: <when Claude should propose it>
   ---
   ```
2. Write the procedure in prose. Steps, stop conditions, output format.
3. If it's adapted from gstack, add `## Adapted from` footer citing source.
4. Run `./tools/validate-skills.sh` to confirm frontmatter is clean.
5. Update `skills/CLAUDE.md` skill table.
6. Bump VERSION (minor bump for a new skill).
7. Add CHANGELOG entry.
8. Commit + push.

---

## Adding a new brain entity

1. Open `tools/brain_lib.py`.
2. Add an `Entity(...)` to the appropriate list (`PEOPLE`, `CLIENTS`, or `CONCEPTS`).
   - `aliases` should include all spellings and word-boundary variants.
   - `tier` starts at 3 unless you have reason to place higher.
   - `one_liner` is the seed for compiled-truth — one sentence.
3. Run `./tools/backfill-brain.py --entity <Name>` to generate the first page (this is safe — it only writes the one new entity).
4. Commit brain page + roster change together.

---

## Editing a brain page

**Do:** refine `## Compiled truth`. Rewrite assessments as patterns shift. Bump `last_reviewed`.
**Don't:** delete or edit timeline entries. That breaks the raw-data principle — timelines are citations to agent-logs.
**If a timeline entry is wrong or misleading:** leave it, but add a new timeline entry correcting it, citing the real source.

---

## Installation

### Fresh machine
```bash
git clone https://github.com/ryan-miranda-partners/maestro-hub.git ~/Documents/maestro-hub
cd ~/Documents/maestro-hub && ./setup
```

### Update to latest
```bash
cd ~/Documents/maestro-hub && git pull
./setup --check   # confirm symlink still points at the right place
```

### Uninstall
```bash
~/Documents/maestro-hub/setup --rollback   # restores most recent backup
```
Or manually: `rm ~/.claude/skills/rm` (drops the symlink; nothing else to clean).

---

## Key directories

```
~/Documents/maestro-hub/                     (this repo)
  skills/         — SKILL.md files (symlinked to ~/.claude/skills/rm)
  brain/          — compiled-truth pages
  tools/          — scripts (backfill, synth, validate)
  docs/           — this guide + troubleshooting + onboarding
~/Documents/agent-logs/                    (session narrative, untouched by rm-skills)
~/Documents/rm-ops/                        (ops workspace — client-updates/, daily/, scripts/)
~/.claude/skills/rm/                       (symlink → ~/Documents/maestro-hub/skills)
~/.claude/projects/<hashed>/memory/        (per-project auto-memory, unchanged by rm-skills)
~/.rm/synth-watermark                      (date of most recent processed agent-log)
```

---

## Related reading

- **Research / design rationale:** `~/Documents/research/mozart-infra/` — 7 docs covering why this shape exists, gstack/gbrain/nimbalyst analysis.
- **Security / sensitivity:** `SECURITY.md` at repo root.
- **Skill principles + mandatory gates:** `skills/CLAUDE.md`.
- **Brain schema + tier rules:** `brain/README.md`.
- **When things break:** `docs/TROUBLESHOOTING.md`.
