# Changelog

## 0.3.0 — 2026-04-19

Forward-synth layer. Brain now stays current automatically (when `/synth` is invoked).

- `tools/brain_lib.py` — shared helpers (entity roster, extraction fns, rendering) used by both backfill and synth.
- `tools/synth-brain.py` — incremental, watermark-based forward synthesizer. Reads agent-logs newer than `~/.rm/synth-watermark`, appends NEW timeline entries to relevant `brain/` pages, advances watermark. Idempotent — re-runs skip already-seen lines.
- `tools/backfill-brain.py` refactored to share logic via `brain_lib.py`.
- `skills/synth/SKILL.md` — `/synth` slash command. Runs the tool, reports changes, surfaces new-entity candidates for manual roster review.
- `skills/CLAUDE.md` updated: added Brain section + brain-first lookup note.

**Validation:** Tested synth with `--since 2026-04-17` — processed 15 logs, added 20 timeline entries across 17 entity pages. Dedup caught pre-existing entries (0 duplicates). Watermark advanced to 2026-04-19.

**Hook-free by design.** `/synth` is manually invoked — no SessionEnd hook yet. Auto-hook deferred until shape is validated over a few weeks.

## 0.2.0 — 2026-04-19

Added the compiled-truth brain layer (draft).

- `brain/README.md` — schema, tier rules, sync cadence, brain-first lookup principle.
- `brain/people/` — 8 draft pages (Vaibhav, Dhrruv, Vivek, Gaurav, Luke, Matthew, Pijush, Connor).
- `brain/clients/` — 7 draft pages (Truthly, FCM, Palmetto, RedDoor, Intrinsic, Atlantis, Mozart).
- `brain/concepts/` — 4 draft pages (TRUTHLYDEV-board, mozart-promotion-pipeline, anthropic-extractor, worktree-cleanup).
- `tools/backfill-brain.py` — one-time extractor. Grep-based, entity-roster-driven. Writes draft timeline per entity from all 250 agent-logs.

**Status:** every compiled-truth section is a `_Draft seed_` placeholder. Timelines are real and cited. Edward to refine compiled-truth assessments. Mention counts range from 2 (worktree-cleanup) to 172 (Truthly).

**Known issues / expected manual cleanup:**
- `people/Matthew.md` (99 mentions) likely conflates Matthew Ayers (Truthly iOS) with Matthew at Intrinsic Digital. Split manually during review.
- `clients/Mozart.md` (135 mentions) mixes client-business mentions with internal mozart code work — both relevant, but assessments should distinguish.
- `people/Vivek.md` timeline captures "Vivek is no longer on the team as of 2026-04-15" — confirm + update compiled-truth accordingly.
- Early entries from roster-listing logs (Mar 15) surface low-value "name in a list" mentions. Prune during review.

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
