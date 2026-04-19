---
name: synth
description: |
  Use when: "synth", "synthesize logs", "update brain", "sync brain", weekly brain refresh, after finishing several sessions.
  Proactive: before /priorities or /draft if the brain last_reviewed is >7 days old; at end of week.
---

## Role
Brain-layer synthesizer. Reads new agent-logs since last watermark, appends timeline entries to the relevant `brain/` pages, advances the watermark.

## Procedure

1. Run the synth tool:
   ```bash
   ~/Documents/rm-skills/tools/synth-brain.py
   ```
2. Capture the output — note logs processed, entries added, and which entity pages changed.
3. If `logs processed: 0` — brain is up-to-date. Report "brain current, no action needed" and stop.
4. If entries were added, scan the agent-logs since the last watermark for entities NOT in the current roster that may warrant a new brain page. Focus on:
   - Named people mentioned repeatedly (3+ times in the new window) who don't have a `brain/people/<name>.md`
   - New clients, initiatives, or concepts that appear significant
5. Produce a concise report:

```
BRAIN SYNTH — <date>

Processed: <n> logs (since <watermark>)
Timeline entries added: <n>
Pages updated: <list of entity names>

NEW ENTITY CANDIDATES (for your review):
- <name> — <n> mentions in window — suggested category: people|clients|concepts

NEXT:
- <any flagged pages whose last_reviewed is >30 days, suggesting a compiled-truth refresh>
```

6. Do NOT automatically add new entities to the roster. That's a manual Edward decision — surface the candidate, wait for instruction.

## Mandatory gates

- **Never modify agent-logs.** Raw data principle — logs are evidence. Synth only READS them.
- **Never rewrite compiled-truth sections.** Synth only appends to `## Timeline`. The assessment is Edward's domain.
- **Do not run if a backfill is in progress.** If `tools/backfill-brain.py` is in the process list, stop and report.

## Output format

Compact. The brain is now larger than any single skill's output; surface the important changes, not the full diff.

## Stop conditions

- If the tool fails (script error, missing brain/, missing logs/), report the exact error and stop. Don't try to work around.
- If the watermark file appears corrupted (not a YYYY-MM-DD date), suggest `tools/synth-brain.py --reset` and stop.

## Related commands

- `tools/synth-brain.py --dry-run` — preview without writing
- `tools/synth-brain.py --since YYYY-MM-DD` — override watermark
- `tools/synth-brain.py --reset` — clear watermark (next run reprocesses ALL logs; dedup prevents duplicates)
- `tools/backfill-brain.py` — full regenerate from scratch (destructive to compiled-truth edits — use with care)

## Adapted from
RM-specific. Pattern inspired by gbrain's compiled-truth + timeline model — grep-based rather than LLM-based for simplicity and audit-ability.
