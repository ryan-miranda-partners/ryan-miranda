# rm-skills

Claude Code skills for Ryan-Miranda Partners ops + dev workflows. 26 skills covering team management (sweep, standup, priorities, draft), code lifecycle (review, ship, plan, cso), and safety (careful, freeze, guard-truthly, verify).

See [skills/CLAUDE.md](skills/CLAUDE.md) for the principles and the full skill table.

## Install

```bash
git clone git@github.com:ryan-miranda-partners/rm-skills.git ~/Documents/rm-skills
cd ~/Documents/rm-skills && ./setup
```

`setup` symlinks `skills/` into `~/.claude/skills/rm` so Claude Code discovers the skills globally. Any existing `~/.claude/skills/rm` is moved to `~/.claude/skills/rm.backup-<timestamp>` first.

Requires: Claude Code. No other dependencies.

## Uninstall

```bash
rm ~/.claude/skills/rm
# restore the backup if you want
mv ~/.claude/skills/rm.backup-<timestamp> ~/.claude/skills/rm
```

## Layout

```
rm-skills/
  skills/               — the 26 SKILL.md folders (symlinked into ~/.claude/skills/rm)
    CLAUDE.md           — principles, mandatory gates, full skill table
    careful/ review/ ship/ cso/ plan/ freeze/       (gstack-derived)
    sweep/ standup/ priorities/ draft/ state/        (RM ops core)
    verify/ guard-truthly/ client-recon/ ...          (RM-specific)
    memory/             — shared reference files (not skills)
    patterns/           — shared reference files (not skills)
  setup                 — symlink installer
  VERSION
  CHANGELOG.md
  README.md             — this file
```

## Conventions

- Every skill lives in its own folder under `skills/` with a `SKILL.md`.
- Frontmatter fields: `name` (required), `description` (required), `allowed-tools` + `hooks` (optional).
- gstack-derived skills carry an "## Adapted from" footer citing the source + the modifications.
- Skills can read shared references from `skills/memory/` and `skills/patterns/`.
- No emojis unless explicitly requested.
- No Claude attribution in commits, PRs, or skill content.

## Upstream

`skills/CLAUDE.md` was last reviewed 2026-04-03. Team + client info inlined there may drift from current state — cross-reference against memory and the `brain/` compiled-truth layer (planned, see `~/Documents/research/mozart-infra/`) before relying on it.
