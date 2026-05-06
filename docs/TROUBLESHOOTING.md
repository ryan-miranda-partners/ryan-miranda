# Troubleshooting

Symptoms → fixes. Most common issues first.

## "A skill isn't loading / Claude says it doesn't know /<name>"

Check the symlink:
```bash
ls -la ~/.claude/skills/rm
```
Expected: `lrwxr-xr-x ... rm -> /Users/edward/Documents/maestro-hub/skills`

If missing or pointing elsewhere:
```bash
cd ~/Documents/maestro-hub && ./setup
```

If the symlink exists but the skill still doesn't load, reload Claude Code (new session). Skill registry is session-scoped.

## "setup --check shows unexpected backup"

```bash
~/Documents/maestro-hub/setup --check
```
If you see `backups available (most recent first): ...`, those are previous `~/.claude/skills/rm` directories the setup script moved aside. Safe to delete if the current install is working:
```bash
rm -rf ~/.claude/skills/rm.backup-*
```

## "validate-skills.sh fails on skill X"

Common causes:
- Missing or malformed YAML frontmatter (must start with `---`, have `name:` and `description:`).
- `name:` field doesn't match the parent directory name.
- Directory contains `SKILL.md` but no trailing newline.

Fix the frontmatter, rerun:
```bash
~/Documents/maestro-hub/tools/validate-skills.sh
```

## "synth-brain.py says no new logs but I wrote one today"

The watermark tracks dates, not timestamps. If you wrote a log dated today AND ran synth today, the log is on-or-before the watermark and gets skipped.

Workarounds:
```bash
# Process today's logs explicitly:
~/Documents/maestro-hub/tools/synth-brain.py --since 2026-04-18   # yesterday's date

# Or reset and let it reprocess (dedup prevents duplicates):
~/Documents/maestro-hub/tools/synth-brain.py --reset
~/Documents/maestro-hub/tools/synth-brain.py
```

This is a known V1 limitation. Fix TBD — move watermark to filename-set-based tracking.

## "synth duplicated a timeline entry"

Shouldn't happen — dedup matches exact lines. If you see it:
1. Confirm the entry is truly duplicated (same date, same source citation, same snippet).
2. If yes, check if the original line had trailing whitespace or different character encoding.
3. Open an issue (or amend `brain_lib.py` to normalize whitespace before dedup).
4. Short-term fix: manually delete the duplicate in the brain page.

## "backfill-brain.py overwrote my compiled-truth edits"

Backfill IS destructive — it regenerates pages from scratch. Recovery:
```bash
cd ~/Documents/maestro-hub && git log --oneline brain/   # find the last commit with your edits
git checkout <sha> -- brain/path/to/page.md            # restore one page
# OR
git checkout <sha> -- brain/                           # restore all brain pages
```
Lesson: commit brain edits before running `backfill-brain.py`.

## "I want to regenerate Vaibhav's page because the snippet extraction changed"

Use the scoped backfill:
```bash
~/Documents/maestro-hub/tools/backfill-brain.py --entity Vaibhav
```
This rewrites only that entity's page. You'll lose compiled-truth edits on that one page — so commit first, then decide whether to merge the new draft with your prior assessment.

## "Claude is writing Claude attribution ('Co-Authored-By: Claude Code') in commits"

Hard rule in Edward's auto-memory — never happens. If it does:
- Check the commit message was not auto-appended by a hook.
- Check `~/.claude/settings.json` and `~/.claude/settings.local.json` for any auto-trailer hook.
- If it slipped through, amend the commit: `git commit --amend` and remove the line.

## "PII appears in a brain page that shouldn't be there"

Immediate:
1. Delete the line from the brain page.
2. Commit + push the redaction.

History cleanup (if sensitive):
```bash
# install git-filter-repo first
git filter-repo --path brain/path/to/page.md --invert-paths   # DESTRUCTIVE, coordinate with any collaborators
git push --force-with-lease                                   # ask Edward first
```

Prevention: keep client recipient lists and emails in `~/Documents/rm-ops/client-updates/README.md`, never in this repo. See `SECURITY.md`.

## "/synth suggested a new entity that I don't want in the roster"

It's only a suggestion — it won't auto-add to `brain_lib.py`. If you don't want it tracked, ignore. Next `/synth` run will suggest again only if mention count grows.

## "I'm on a new machine and nothing works"

1. Install Claude Code.
2. `git clone https://github.com/ryan-miranda-partners/maestro-hub.git ~/Documents/maestro-hub`
3. `cd ~/Documents/maestro-hub && ./setup`
4. Open a new session. Type `/sweep`. If that resolves, you're in.
5. Agent-logs don't transfer automatically — they live in `~/Documents/agent-logs/` on the original machine. If you want the brain to know about pre-move history, rsync agent-logs and run `./tools/synth-brain.py --reset && ./tools/synth-brain.py`.

## "validate-skills.sh passes but /synth isn't in the skill registry"

Claude Code caches skills at session start. Start a new session. If still missing:
```bash
ls ~/.claude/skills/rm/synth/SKILL.md   # confirm file exists via symlink
```
If yes and still not loading, check for a typo in `name:` — must match dir name exactly.

## When to rebuild from scratch

Rare. If the brain is truly corrupt (many bad edits, inconsistent format, lost trust):
```bash
cd ~/Documents/maestro-hub
git checkout -- brain/                   # restore all from git
# or start over:
rm -rf brain/people brain/clients brain/concepts
./tools/backfill-brain.py                # rebuild from agent-logs
```
Commit as a new version bump so history shows the reset was intentional.
