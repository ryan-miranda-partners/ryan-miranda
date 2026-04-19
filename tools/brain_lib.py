"""Shared helpers for the brain-backfill and brain-synth scripts.

The entity roster, extraction logic, and page rendering live here so that
`backfill-brain.py` (one-shot full rewrite) and `synth-brain.py` (incremental
append) use the same definitions.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DATE_FROM_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


@dataclass
class Entity:
    name: str              # filename base (e.g. "Vaibhav")
    category: str          # "people" | "clients" | "concepts"
    aliases: list[str]     # case-insensitive word-boundary matched
    tier: int              # starting tier guess (1-3)
    one_liner: str         # seed description for compiled-truth


PEOPLE = [
    Entity("Vaibhav", "people", ["Vaibhav"], 1,
           "Lead engineer, Delhi team. Truthly-focused."),
    Entity("Dhrruv", "people", ["Dhrruv", "Dhruv"], 1,
           "Delhi team engineer. Palmetto GCP lead."),
    Entity("Vivek", "people", ["Vivek"], 1,
           "Delhi team engineer. Truthly backend. Departed 2026-04-15 (verify)."),
    Entity("Gaurav", "people", ["Gaurav"], 1,
           "Delhi team. Declined May 1 full-time offer on Apr 3 2026."),
    Entity("Luke", "people", ["Luke"], 1,
           "US-based reviewer/builder. Palmetto + Truthly reviews."),
    Entity("Matthew", "people", ["Matthew Ayers", "Matthew"], 2,
           "Name conflates Matthew Ayers (Truthly iOS) with Matthew at Intrinsic Digital. Split during review."),
    Entity("Pijush", "people", ["Pijush"], 2,
           "Full-time May 2026 start."),
    Entity("Connor", "people", ["Connor"], 2,
           "Connor Dailey. Truthly-embedded per Apr 12 note."),
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
           "Paul Ryan, Robert Murner — ad-hoc, not weekly. Also internal product code, mentions conflate."),
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
           "Stale worktree backlog — phantom dirs, mw-* trees, mozart orphans."),
]

ALL_ENTITIES = PEOPLE + CLIENTS + CONCEPTS


def log_date(path: Path) -> str | None:
    m = DATE_FROM_FILENAME_RE.match(path.name)
    return m.group(1) if m else None


def extract_snippet(text: str, match_start: int, match_end: int, max_len: int = 160) -> str:
    """Compact snippet around the match. Collapses markdown/whitespace."""
    start = text.rfind(". ", 0, match_start) + 2 if ". " in text[:match_start] else 0
    start = max(start, text.rfind("\n", 0, match_start) + 1)
    start = max(0, start)

    end_candidates = [text.find(p, match_end) for p in [". ", "\n", "! ", "? "]]
    end_candidates = [c for c in end_candidates if c != -1]
    end = min(end_candidates) if end_candidates else match_end + 80
    end = min(end, len(text))

    snippet = text[start:end].strip()
    snippet = re.sub(r"\s+", " ", snippet)
    snippet = re.sub(r"^[#*\->\s]+", "", snippet)
    if len(snippet) > max_len:
        snippet = snippet[:max_len].rstrip() + "…"
    return snippet


def compile_entity_regex(entity: Entity) -> re.Pattern:
    return re.compile(
        r"\b(" + "|".join(re.escape(a) for a in entity.aliases) + r")\b",
        re.IGNORECASE,
    )


def find_entity_mentions_in_log(entity: Entity, log_path: Path) -> tuple[str, str] | None:
    """Return (date, snippet) if the entity is mentioned in this log, else None.
    Captures the first mention only (to keep timeline one-entry-per-log)."""
    date = log_date(log_path)
    if not date:
        return None
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = compile_entity_regex(entity).search(text)
    if not m:
        return None
    return date, extract_snippet(text, m.start(), m.end())


def find_all_entity_mentions(entity: Entity, log_paths: list[Path]) -> list[tuple[str, Path, str]]:
    """Return list of (date, path, snippet) for every log that mentions the entity."""
    out: list[tuple[str, Path, str]] = []
    for log_path in log_paths:
        hit = find_entity_mentions_in_log(entity, log_path)
        if hit:
            date, snippet = hit
            out.append((date, log_path, snippet))
    return out


def iter_logs(logs_dir: Path, since_date: str | None = None) -> list[Path]:
    """Return sorted list of agent-log paths. If since_date is given (YYYY-MM-DD),
    only include logs with filename date strictly greater than that."""
    paths: list[Path] = []
    for p in sorted(logs_dir.glob("*.md")):
        d = log_date(p)
        if not d:
            continue
        if since_date and d <= since_date:
            continue
        paths.append(p)
    return paths


def timeline_entry(date: str, path: Path, snippet: str) -> str:
    return f"- {date} — {snippet} — `agent-logs/{path.name}`"
