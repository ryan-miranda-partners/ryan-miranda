#!/usr/bin/env python3
"""synth-brain.py — incremental forward synthesizer.

Reads agent-logs newer than the watermark (`~/.rm/synth-watermark`),
appends new timeline entries to the relevant brain/ pages, and updates
the watermark.

Safe to run repeatedly — the watermark tracks the most recent processed log
so each log is synthesized exactly once.

Usage:
    ./tools/synth-brain.py                # normal incremental run
    ./tools/synth-brain.py --since DATE   # override watermark (YYYY-MM-DD)
    ./tools/synth-brain.py --dry-run      # report without writing
    ./tools/synth-brain.py --reset        # delete the watermark (next run reprocesses everything)

Existing brain pages are AMENDED, not rewritten. New timeline entries are
appended to the `## Timeline` section. Stub pages are created for entities
that have no page yet.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brain_lib import (  # noqa: E402
    ALL_ENTITIES,
    Entity,
    find_entity_mentions_in_log,
    iter_logs,
    log_date,
    timeline_entry,
)

TODAY = "2026-04-19"

DEFAULT_WATERMARK_PATH = Path.home() / ".rm" / "synth-watermark"
TIMELINE_HEADER_RE = re.compile(r"^## Timeline\s*$", re.MULTILINE)


def read_watermark(path: Path) -> str | None:
    if not path.exists():
        return None
    val = path.read_text(encoding="utf-8").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", val):
        return None
    return val


def write_watermark(path: Path, date: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(date + "\n", encoding="utf-8")


def stub_page(entity: Entity) -> str:
    lines = [
        "---",
        f"name: {entity.name}",
        f"tier: {entity.tier}",
        f"last_reviewed: {TODAY}",
        "---",
        "",
        f"# {entity.name}",
        "",
        f"## Compiled truth (as of {TODAY})",
        "",
        "_Stub seeded by synth. Edward to refine._",
        "",
        f"- {entity.one_liner}",
        "- Role / relationship: _TBD_",
        "- Current focus: _TBD_",
        "",
        "## Timeline",
        "",
    ]
    return "\n".join(lines)


def append_timeline_entries(existing: str, new_entries: list[str]) -> str:
    """Append entries to the Timeline section of a brain page.
    Idempotent: skips entries already present in the file (by exact-line match)."""
    if not new_entries:
        return existing
    existing_lines = set(existing.splitlines())
    to_add = [e for e in new_entries if e not in existing_lines]
    if not to_add:
        return existing

    m = TIMELINE_HEADER_RE.search(existing)
    if not m:
        # No timeline section — append one.
        sep = "" if existing.endswith("\n") else "\n"
        return existing + sep + "\n## Timeline\n\n" + "\n".join(to_add) + "\n"

    # Insert at end of file (timeline is the last section by convention).
    trimmed = existing.rstrip("\n")
    return trimmed + "\n" + "\n".join(to_add) + "\n"


def bump_last_reviewed(existing: str, new_date: str) -> str:
    return re.sub(
        r"^last_reviewed:.*$",
        f"last_reviewed: {new_date}",
        existing,
        count=1,
        flags=re.MULTILINE,
    )


def synth(
    logs_dir: Path,
    brain_dir: Path,
    since_date: str | None,
    dry_run: bool,
) -> tuple[int, int, str | None]:
    """Returns (logs_processed, entries_added, new_watermark)."""
    log_paths = iter_logs(logs_dir, since_date=since_date)
    if not log_paths:
        return 0, 0, None

    # Collect new mentions grouped by entity.
    per_entity: dict[str, list[str]] = {}
    for log_path in log_paths:
        for entity in ALL_ENTITIES:
            hit = find_entity_mentions_in_log(entity, log_path)
            if not hit:
                continue
            date, snippet = hit
            key = f"{entity.category}/{entity.name}"
            per_entity.setdefault(key, []).append(timeline_entry(date, log_path, snippet))

    entries_added = 0
    for entity in ALL_ENTITIES:
        key = f"{entity.category}/{entity.name}"
        new_lines = per_entity.get(key, [])
        if not new_lines:
            continue
        page_path = brain_dir / entity.category / f"{entity.name}.md"
        if page_path.exists():
            existing = page_path.read_text(encoding="utf-8")
        else:
            existing = stub_page(entity)
        updated = append_timeline_entries(existing, new_lines)
        if updated == existing:
            continue
        added_here = len([ln for ln in new_lines if ln not in existing])
        entries_added += added_here
        updated = bump_last_reviewed(updated, TODAY)
        action = "DRY-RUN" if dry_run else "write"
        print(f"[{action}] {entity.category}/{entity.name}.md — +{added_here} entry(ies)")
        if not dry_run:
            page_path.parent.mkdir(parents=True, exist_ok=True)
            page_path.write_text(updated, encoding="utf-8")

    new_watermark = log_date(log_paths[-1])
    return len(log_paths), entries_added, new_watermark


def main():
    repo_root = Path(__file__).resolve().parent.parent
    default_logs = Path.home() / "Documents" / "agent-logs"
    default_brain = repo_root / "brain"

    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="Override watermark (YYYY-MM-DD)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reset", action="store_true", help="Delete watermark file")
    ap.add_argument("--logs-dir", default=str(default_logs))
    ap.add_argument("--brain-dir", default=str(default_brain))
    ap.add_argument("--watermark", default=str(DEFAULT_WATERMARK_PATH))
    args = ap.parse_args()

    watermark_path = Path(args.watermark)
    if args.reset:
        if watermark_path.exists():
            watermark_path.unlink()
            print(f"removed watermark: {watermark_path}")
        else:
            print(f"no watermark at {watermark_path}")
        return

    logs_dir = Path(args.logs_dir)
    brain_dir = Path(args.brain_dir)

    if not logs_dir.is_dir():
        print(f"error: logs-dir not found: {logs_dir}", file=sys.stderr)
        sys.exit(1)
    if not brain_dir.is_dir():
        print(f"error: brain-dir not found: {brain_dir}", file=sys.stderr)
        sys.exit(1)

    since = args.since or read_watermark(watermark_path)
    if since:
        print(f"watermark: {since} — processing logs AFTER this date")
    else:
        print("watermark: <none> — processing ALL logs (first run or post-reset)")

    logs_processed, entries_added, new_watermark = synth(
        logs_dir=logs_dir,
        brain_dir=brain_dir,
        since_date=since,
        dry_run=args.dry_run,
    )

    print(f"\nlogs processed: {logs_processed}")
    print(f"timeline entries added: {entries_added}")

    if logs_processed == 0:
        print("no new logs since watermark. brain is up-to-date.")
        return

    if args.dry_run:
        print(f"(dry-run) would advance watermark to {new_watermark}")
        return

    if new_watermark:
        write_watermark(watermark_path, new_watermark)
        print(f"watermark advanced to {new_watermark} ({watermark_path})")


if __name__ == "__main__":
    main()
