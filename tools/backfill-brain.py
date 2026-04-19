#!/usr/bin/env python3
"""
backfill-brain.py — one-time extractor that reads all agent-logs and emits
draft brain/ pages per entity.

Usage:
    ./tools/backfill-brain.py                          # process all entities, write to brain/
    ./tools/backfill-brain.py --entity Vaibhav          # process one entity only
    ./tools/backfill-brain.py --dry-run                 # report counts, don't write
    ./tools/backfill-brain.py --logs-dir <path>         # override agent-logs location

The extractor is intentionally dumb: it greps for entity names with word
boundaries, captures the filename + a one-line context snippet around each
mention, and emits a draft markdown page. Edward reviews + refines.

Noise is expected. False positives on common names (Matthew is both a person
and a word) get filtered during manual review.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# --- Entity roster -----------------------------------------------------------
# Each entity: canonical page name + list of aliases to grep (case-insensitive,
# word-boundary matched). Aliases cover common misspellings and variants.
# Tier is a starting hint; the real tier is set in the compiled-truth page.

@dataclass
class Entity:
    name: str              # filename base (e.g. "Vaibhav")
    category: str          # "people" | "clients" | "concepts"
    aliases: list[str]     # regex-escaped alternatives to match
    tier: int              # starting tier guess (1-3)
    one_liner: str         # seed description for compiled-truth


PEOPLE = [
    Entity("Vaibhav", "people", ["Vaibhav"], 1,
           "Lead engineer, Delhi team. Truthly-focused."),
    Entity("Dhrruv", "people", ["Dhrruv", "Dhruv"], 1,
           "Delhi team engineer. Palmetto GCP lead."),
    Entity("Vivek", "people", ["Vivek"], 1,
           "Delhi team engineer. Truthly backend."),
    Entity("Gaurav", "people", ["Gaurav"], 1,
           "Delhi team. Declined May 1 full-time offer on Apr 3 2026."),
    Entity("Luke", "people", ["Luke"], 1,
           "US-based reviewer/builder. Palmetto + Truthly reviews."),
    Entity("Matthew", "people", ["Matthew Ayers", "Matthew"], 2,
           "Truthly iOS engineer. Works with Edward on ship reviews."),
    Entity("Pijush", "people", ["Pijush"], 2,
           "Full-time May 2026 start."),
    Entity("Connor", "people", ["Connor"], 2,
           "Team member — role/context TBD."),
]

CLIENTS = [
    Entity("Truthly", "clients", ["Truthly", "TRUTHLYDEV"], 1,
           "Flagship client. iOS + Android + backend. Jacob, Zac, Karim primary contacts."),
    Entity("FCM", "clients", ["FCM", "Fernbridge", "Fernbridge Capital"], 1,
           "Financial-services client. Mark, Winston, David primary contacts."),
    Entity("Palmetto", "clients", ["Palmetto"], 1,
           "Jerome and Alexis primary. GCP infrastructure work."),
    Entity("RedDoor", "clients", ["Red Door", "RedDoor", "reddoorescape"], 1,
           "Sang and Nick. Escape-room business."),
    Entity("Intrinsic", "clients", ["Intrinsic Digital", "intrinsicdigital"], 1,
           "Matthew, Madchap, Charlotte, Danielle contacts."),
    Entity("Atlantis", "clients", ["Atlantis"], 2,
           "Chris Briggs + Mark Ryland."),
    Entity("Mozart", "clients", ["Mozart"], 1,
           "Paul Ryan, Robert Murner — ad-hoc, not weekly."),
]

CONCEPTS = [
    Entity("TRUTHLYDEV-board", "concepts", ["TRUTHLYDEV", "Truthly board", "TRUTHLYDEV board"], 1,
           "Truthly Jira project. Client-facing — no agentic bulk writes allowed."),
    Entity("mozart-promotion-pipeline", "concepts",
           ["staging promotion", "main promotion", "dev→staging→main", "promotion pipeline"], 1,
           "Mozart release flow. Backend was 73 days stale on Apr 18."),
    Entity("anthropic-extractor", "concepts",
           ["anthropic-extractor", "anthropic extractor"], 2,
           "Direct-Anthropic extraction path vs OpenAI proxy. Cost-reduction project."),
    Entity("worktree-cleanup", "concepts",
           ["worktree cleanup", "mw-worktree", "phantom dir"], 2,
           "Stale worktree backlog — phantom dirs, mw-* trees, mozart orphans. Plan dated 2026-04-13."),
]

ALL_ENTITIES = PEOPLE + CLIENTS + CONCEPTS


# --- Extraction logic --------------------------------------------------------

DATE_FROM_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def log_date(path: Path) -> str | None:
    m = DATE_FROM_FILENAME_RE.match(path.name)
    return m.group(1) if m else None


def extract_snippet(text: str, match_start: int, match_end: int, max_len: int = 160) -> str:
    """Return a compact snippet around the match — ideally one sentence."""
    # Find sentence boundaries
    start = text.rfind(". ", 0, match_start) + 2 if ". " in text[:match_start] else 0
    start = max(start, text.rfind("\n", 0, match_start) + 1)
    start = max(0, start)

    end_candidates = [text.find(p, match_end) for p in [". ", "\n", "! ", "? "]]
    end_candidates = [c for c in end_candidates if c != -1]
    end = min(end_candidates) if end_candidates else match_end + 80
    end = min(end, len(text))

    snippet = text[start:end].strip()
    # Collapse whitespace + markdown noise
    snippet = re.sub(r"\s+", " ", snippet)
    snippet = re.sub(r"^[#*\->\s]+", "", snippet)
    if len(snippet) > max_len:
        snippet = snippet[:max_len].rstrip() + "…"
    return snippet


def find_entity_mentions(entity: Entity, logs_dir: Path) -> list[tuple[str, Path, str]]:
    """Returns list of (date, path, snippet) for every mention of this entity."""
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(a) for a in entity.aliases) + r")\b",
        re.IGNORECASE,
    )
    results: list[tuple[str, Path, str]] = []
    for log_path in sorted(logs_dir.glob("*.md")):
        date = log_date(log_path)
        if not date:
            continue
        try:
            text = log_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = pattern.search(text)
        if not m:
            continue
        # One entry per log (even if the entity is mentioned multiple times — we'll pick the first)
        snippet = extract_snippet(text, m.start(), m.end())
        results.append((date, log_path, snippet))
    return results


# --- Page rendering ----------------------------------------------------------

def render_page(entity: Entity, mentions: list[tuple[str, Path, str]]) -> str:
    today = "2026-04-19"
    lines = []
    lines.append("---")
    lines.append(f"name: {entity.name}")
    lines.append(f"tier: {entity.tier}")
    lines.append(f"last_reviewed: {today}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {entity.name}")
    lines.append("")
    lines.append(f"## Compiled truth (as of {today})")
    lines.append("")
    lines.append(f"_Draft seed — Edward to refine._")
    lines.append("")
    lines.append(f"- {entity.one_liner}")
    lines.append(f"- Mention count in agent-logs: **{len(mentions)}** (across {mentions[0][0] if mentions else 'N/A'} → {mentions[-1][0] if mentions else 'N/A'})")
    lines.append("- Role / relationship: _TBD_")
    lines.append("- Current focus: _TBD_")
    lines.append("- Working style: _TBD_")
    lines.append("- Risks / watch-outs: _TBD_")
    lines.append("")
    lines.append("## Timeline")
    lines.append("")
    if not mentions:
        lines.append("_No mentions found in agent-logs. Consider whether this entity is actually active._")
    else:
        for date, path, snippet in mentions:
            rel = path.name
            lines.append(f"- {date} — {snippet} — `agent-logs/{rel}`")
    lines.append("")
    return "\n".join(lines)


# --- Main --------------------------------------------------------------------

def main():
    repo_root = Path(__file__).resolve().parent.parent
    default_logs = Path.home() / "Documents" / "agent-logs"
    default_brain = repo_root / "brain"

    ap = argparse.ArgumentParser()
    ap.add_argument("--entity", help="Process only this entity (by name)")
    ap.add_argument("--dry-run", action="store_true", help="Report counts, don't write")
    ap.add_argument("--logs-dir", default=str(default_logs))
    ap.add_argument("--brain-dir", default=str(default_brain))
    args = ap.parse_args()

    logs_dir = Path(args.logs_dir)
    brain_dir = Path(args.brain_dir)

    if not logs_dir.is_dir():
        print(f"error: logs-dir not found: {logs_dir}", file=sys.stderr)
        sys.exit(1)

    entities: Iterable[Entity] = ALL_ENTITIES
    if args.entity:
        entities = [e for e in ALL_ENTITIES if e.name.lower() == args.entity.lower()]
        if not entities:
            print(f"error: entity '{args.entity}' not in roster", file=sys.stderr)
            print("available:", ", ".join(e.name for e in ALL_ENTITIES), file=sys.stderr)
            sys.exit(1)

    total_written = 0
    for entity in entities:
        mentions = find_entity_mentions(entity, logs_dir)
        out_path = brain_dir / entity.category / f"{entity.name}.md"
        action = "DRY-RUN" if args.dry_run else "write"
        print(f"[{action}] {entity.category}/{entity.name}.md — {len(mentions)} mention(s)")
        if args.dry_run:
            continue
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_page(entity, mentions), encoding="utf-8")
        total_written += 1

    if not args.dry_run:
        print(f"\nwrote {total_written} page(s) to {brain_dir}/")


if __name__ == "__main__":
    main()
