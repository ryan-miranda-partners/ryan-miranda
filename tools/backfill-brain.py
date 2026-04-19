#!/usr/bin/env python3
"""backfill-brain.py — one-time extractor: reads all agent-logs and emits
a full draft brain/ page per entity. Overwrites existing pages.

For incremental updates to an existing brain, use synth-brain.py instead.

Usage:
    ./tools/backfill-brain.py                  # process all entities, write to brain/
    ./tools/backfill-brain.py --entity Vaibhav  # one entity
    ./tools/backfill-brain.py --dry-run         # report counts, don't write
    ./tools/backfill-brain.py --logs-dir <path> # override agent-logs location
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brain_lib import (  # noqa: E402
    ALL_ENTITIES,
    Entity,
    find_all_entity_mentions,
    iter_logs,
    timeline_entry,
)

TODAY = "2026-04-19"


def render_page(entity: Entity, mentions: list[tuple[str, Path, str]]) -> str:
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
        "_Draft seed — Edward to refine._",
        "",
        f"- {entity.one_liner}",
        f"- Mention count in agent-logs: **{len(mentions)}**"
        + (f" (across {mentions[0][0]} → {mentions[-1][0]})" if mentions else ""),
        "- Role / relationship: _TBD_",
        "- Current focus: _TBD_",
        "- Working style: _TBD_",
        "- Risks / watch-outs: _TBD_",
        "",
        "## Timeline",
        "",
    ]
    if not mentions:
        lines.append("_No mentions found in agent-logs. Consider whether this entity is actually active._")
    else:
        for date, path, snippet in mentions:
            lines.append(timeline_entry(date, path, snippet))
    lines.append("")
    return "\n".join(lines)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    default_logs = Path.home() / "Documents" / "agent-logs"
    default_brain = repo_root / "brain"

    ap = argparse.ArgumentParser()
    ap.add_argument("--entity")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--logs-dir", default=str(default_logs))
    ap.add_argument("--brain-dir", default=str(default_brain))
    args = ap.parse_args()

    logs_dir = Path(args.logs_dir)
    brain_dir = Path(args.brain_dir)

    if not logs_dir.is_dir():
        print(f"error: logs-dir not found: {logs_dir}", file=sys.stderr)
        sys.exit(1)

    log_paths = iter_logs(logs_dir)

    entities = ALL_ENTITIES
    if args.entity:
        entities = [e for e in ALL_ENTITIES if e.name.lower() == args.entity.lower()]
        if not entities:
            print(f"error: entity '{args.entity}' not in roster", file=sys.stderr)
            sys.exit(1)

    written = 0
    for entity in entities:
        mentions = find_all_entity_mentions(entity, log_paths)
        action = "DRY-RUN" if args.dry_run else "write"
        print(f"[{action}] {entity.category}/{entity.name}.md — {len(mentions)} mention(s)")
        if args.dry_run:
            continue
        out_path = brain_dir / entity.category / f"{entity.name}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_page(entity, mentions), encoding="utf-8")
        written += 1

    if not args.dry_run:
        print(f"\nwrote {written} page(s) to {brain_dir}/")


if __name__ == "__main__":
    main()
