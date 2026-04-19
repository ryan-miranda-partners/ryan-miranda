# Changelog

## 0.1.1 — 2026-04-19

Hardening pass on the initial import:
- Added `LICENSE` (proprietary, © 2026 Ryan Miranda Partners).
- Added `SECURITY.md` documenting what's in-scope vs out-of-scope for this repo.
- Added `tools/validate-skills.sh` — frontmatter + name-matches-dir validator. Ran clean on all 21 skills.
- Extended `setup` with `--rollback`, `--check`, and `--help` subcommands.
- Corrected skill count (21, not 26 — `memory/` and `patterns/` are shared reference dirs, not skills).

## 0.1.0 — 2026-04-19

Initial import from `~/.claude/skills/rm/`. 21 skills live and in daily use since Mar 26.

**Skills included (21):**

Dev (6): `/review`, `/ship`, `/plan`, `/cso`, `/extract-test`, `/pdf`
Ops (7): `/sweep`, `/standup`, `/priorities`, `/state`, `/pr-status`, `/ticket-hygiene`, `/draft`
Strategy (3): `/competitor-scan`, `/client-recon`, `/fcm-demo`
Safety (4): `/careful`, `/freeze`, `/guard-truthly`, `/verify`
Meta (1): `/feedback-audit`

**Shared references (not skills):**
- `skills/CLAUDE.md` — principles, mandatory gates, full skill table
- `skills/memory/correction_tracker.md` — pre-output correction map
- `skills/patterns/{anti_rationalization,mandatory_validation,session_state}.md`

**Provenance:** gstack-derived skills (/careful, /freeze, /review, /ship, /plan, /cso) carry "Adapted from" footers. RM-specific skills are net-new.
