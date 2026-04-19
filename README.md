# rm-skills

Claude Code skills + compiled-truth brain for Ryan-Miranda Partners ops + dev workflows. 22 skills covering team management (`/sweep`, `/standup`, `/priorities`, `/draft`), code lifecycle (`/review`, `/ship`, `/plan`, `/cso`), safety (`/careful`, `/freeze`, `/guard-truthly`, `/verify`), and brain synthesis (`/synth`).

## Start here

- **Daily use:** [`docs/GUIDE.md`](docs/GUIDE.md)
- **Onboarding a teammate:** [`docs/ONBOARDING.md`](docs/ONBOARDING.md)
- **When things break:** [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)
- **Full skill table + principles:** [`skills/CLAUDE.md`](skills/CLAUDE.md)
- **Brain schema:** [`brain/README.md`](brain/README.md)
- **Sensitivity + handling:** [`SECURITY.md`](SECURITY.md)

## Install

```bash
git clone git@github.com:ryan-miranda-partners/rm-skills.git ~/Documents/rm-skills
cd ~/Documents/rm-skills && ./setup
```

`setup` symlinks `skills/` into `~/.claude/skills/rm` so Claude Code discovers the skills globally. Any existing `~/.claude/skills/rm` is moved to `~/.claude/skills/rm.backup-<timestamp>` first.

### Requires
Claude Code + Python 3.10+ (for the brain tools). No other runtime dependencies.

### Update / uninstall
```bash
cd ~/Documents/rm-skills && git pull       # update
./setup --check                            # confirm symlink state
./setup --rollback                         # restore backup, remove symlink
```

## Layout

```
rm-skills/
  skills/               — 22 SKILL.md folders (symlinked into ~/.claude/skills/rm)
    CLAUDE.md           — principles, mandatory gates, full skill table
    careful/ review/ ship/ cso/ plan/ freeze/        (gstack-derived)
    sweep/ standup/ priorities/ draft/ state/         (RM ops core)
    verify/ guard-truthly/ client-recon/ synth/ ...    (RM-specific)
    memory/             — shared reference files (not skills)
    patterns/           — shared reference files (not skills)
  brain/                — compiled-truth pages
    people/ clients/ concepts/
    README.md           — schema, tier rules, brain-first lookup
  tools/                — scripts
    backfill-brain.py   — full regenerate (destructive — use with care)
    synth-brain.py      — incremental watermark-based synth
    brain_lib.py        — shared helpers
    validate-skills.sh  — frontmatter + name-matches-dir check
  docs/
    GUIDE.md            — daily playbook
    TROUBLESHOOTING.md  — symptom → fix
    ONBOARDING.md       — new-teammate intro
    README.md           — docs index
  setup                 — install / rollback script
  VERSION
  CHANGELOG.md
  README.md             — this file
  LICENSE SECURITY.md
```

## Conventions

- Every skill lives in its own folder under `skills/` with a `SKILL.md`.
- Frontmatter fields: `name` (required, matches dir), `description` (required), `allowed-tools` + `hooks` (optional).
- gstack-derived skills carry an "## Adapted from" footer citing source + modifications.
- Skills can read shared references from `skills/memory/` and `skills/patterns/`, and compiled-truth from `brain/`.
- No emojis unless explicitly requested.
- No Claude attribution in commits, PRs, or skill content.

## Design rationale

Research that led to this structure: `~/Documents/research/mozart-infra/` (7 docs, outside this repo). Covers gstack / gbrain / nimbalyst analysis and the unified-infra proposal.
